#!/usr/bin/env python3
"""Install and verify Skill R&D Kit project-local skills from a manifest."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"ERROR: manifest not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    return current


def harness_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_project_path(raw: str, root: Path, repo_root: Path) -> Path:
    path = Path(expand_placeholders(raw, root, repo_root, None))
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] == "subprojects":
        return (repo_root / path).resolve()
    return (root / path).resolve()


def expand_placeholders(raw: str, root: Path, repo_root: Path, skill_dir: Path | None) -> str:
    codex_home = os.environ.get("CODEX_HOME", "")
    replacements = {
        "{CODEX_HOME}": codex_home,
        "{repo_root}": str(repo_root),
        "{harness_root}": str(root),
        "{python}": sys.executable,
    }
    if skill_dir is not None:
        replacements["{skill_dir}"] = str(skill_dir)

    result = raw
    for key, value in replacements.items():
        result = result.replace(key, value)
    return result


def require_codex_home(manifest: dict[str, Any]) -> None:
    target = str(manifest.get("target_path", ""))
    if "{CODEX_HOME}" in target and not os.environ.get("CODEX_HOME"):
        raise SystemExit("ERROR: CODEX_HOME is required because target_path uses {CODEX_HOME}")


def codex_home_path() -> Path:
    raw = os.environ.get("CODEX_HOME")
    if not raw:
        raise SystemExit("ERROR: CODEX_HOME is required for install lifecycle operations")
    return Path(raw).resolve()


def check_required_manifest_fields(manifest: dict[str, Any]) -> None:
    required = [
        "skill_name",
        "version",
        "source_path",
        "install_target",
        "target_path",
        "promotion_evidence",
        "verify_commands",
        "post_install_checks",
    ]
    missing = [field for field in required if field not in manifest]
    if missing:
        raise SystemExit(f"ERROR: manifest missing required fields: {', '.join(missing)}")


def evidence_status(paths: list[str], root: Path, repo_root: Path) -> list[tuple[str, bool]]:
    return [(path, resolve_project_path(path, root, repo_root).exists()) for path in paths]


def check_paths_exist(skill_dir: Path, checks: list[str]) -> list[tuple[str, bool]]:
    results: list[tuple[str, bool]] = []
    for raw in checks:
        relative = raw.strip()
        if relative.endswith(" exists"):
            relative = relative[: -len(" exists")].strip()
        results.append((raw, (skill_dir / relative).exists()))
    return results


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def record_path(target: Path) -> Path:
    return target / ".skill-install-record.json"


def backup_root(manifest: dict[str, Any]) -> Path:
    return codex_home_path() / "skill-backups" / manifest["skill_name"]


def read_install_record(target: Path) -> dict[str, Any] | None:
    path = record_path(target)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"record_error": "invalid_json", "record_path": str(path)}


def write_install_record(
    manifest: dict[str, Any],
    manifest_path: Path,
    source: Path,
    target: Path,
    action: str,
    backup_path: Path | None,
    verify_result: str,
    version_status: str,
) -> None:
    data = {
        "skill_name": manifest["skill_name"],
        "manifest_path": str(manifest_path),
        "source_path": str(source),
        "target_path": str(target),
        "manifest_version": manifest["version"],
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "backup_path": str(backup_path) if backup_path else None,
        "verify_result": verify_result,
        "version_status": version_status,
    }
    record_path(target).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def latest_backup(manifest: dict[str, Any]) -> Path | None:
    root = backup_root(manifest)
    if not root.exists():
        return None
    candidates = sorted([path for path in root.iterdir() if path.is_dir()])
    return candidates[-1] if candidates else None


def create_backup(manifest: dict[str, Any], target: Path, reason: str) -> Path:
    if not target.exists():
        raise SystemExit(f"ERROR: cannot backup missing target: {target}")
    root = backup_root(manifest)
    root.mkdir(parents=True, exist_ok=True)
    base = root / f"{now_stamp()}-{reason}"
    backup = base
    counter = 1
    while backup.exists():
        counter += 1
        backup = Path(f"{base}-{counter}")
    shutil.copytree(target, backup)
    return backup


def version_status(manifest: dict[str, Any], previous_record: dict[str, Any] | None) -> str:
    if previous_record is None:
        return "previous_version_unknown"
    previous = previous_record.get("manifest_version")
    if not previous:
        return "previous_version_unknown"
    if str(previous) == str(manifest["version"]):
        return "same_version_upgrade"
    return f"version_change:{previous}->{manifest['version']}"


def print_action_result(
    action: str,
    manifest: dict[str, Any],
    source: Path,
    target: Path,
    backup: Path | None,
    verify_result: str,
    exit_code: int,
    extra: dict[str, str] | None = None,
) -> None:
    print(f"action: {action}")
    print(f"skill_name: {manifest['skill_name']}")
    print(f"version: {manifest['version']}")
    print(f"source_path: {source}")
    print(f"target_path: {target}")
    print(f"backup_path: {backup if backup else 'none'}")
    if extra:
        for key, value in extra.items():
            print(f"{key}: {value}")
    print(f"verify_result: {verify_result}")
    print(f"exit_code: {exit_code}")


def print_plan(manifest: dict[str, Any], source: Path, target: Path, root: Path, repo_root: Path) -> None:
    print(f"skill_name: {manifest['skill_name']}")
    print(f"version: {manifest['version']}")
    print(f"install_target: {manifest['install_target']}")
    print(f"source_path: {source}")
    print(f"target_path: {target}")
    print(f"source_exists: {'yes' if source.exists() else 'no'}")
    print(f"target_exists: {'yes' if target.exists() else 'no'}")
    print("promotion_evidence:")
    for raw, exists in evidence_status(manifest.get("promotion_evidence", []), root, repo_root):
        print(f"  - {'pass' if exists else 'missing'}: {raw}")
    print("post_install_checks:")
    for raw in manifest.get("post_install_checks", []):
        print(f"  - {raw}")
    print("verify_commands:")
    for command in manifest.get("verify_commands", []):
        print(f"  - {command}")
    evidence_ok = all(exists for _, exists in evidence_status(manifest.get("promotion_evidence", []), root, repo_root))
    print(f"dry_run_result: {'pass' if source.exists() and evidence_ok else 'fail'}")


def run_verify(manifest: dict[str, Any], target: Path, root: Path, repo_root: Path) -> int:
    print(f"verify_skill: {manifest['skill_name']}")
    print(f"target_path: {target}")
    if not target.exists():
        print(f"ERROR: target skill directory does not exist: {target}", file=sys.stderr)
        print("verify_result: fail")
        return 1

    failed = False
    for raw, exists in check_paths_exist(target, manifest.get("post_install_checks", [])):
        print(f"check: {raw}: {'pass' if exists else 'fail'}")
        if not exists:
            failed = True

    for raw in manifest.get("verify_commands", []):
        command = expand_placeholders(raw, root, repo_root, target)
        print(f"run: {command}")
        completed = subprocess.run(
            command,
            cwd=str(target),
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.stdout:
            print(completed.stdout.rstrip())
        if completed.stderr:
            print(completed.stderr.rstrip(), file=sys.stderr)
        print(f"exit_code: {completed.returncode}")
        if completed.returncode != 0:
            failed = True

    print(f"verify_result: {'fail' if failed else 'pass'}")
    return 1 if failed else 0


def install_skill(
    manifest: dict[str, Any],
    manifest_path: Path,
    source: Path,
    target: Path,
) -> int:
    if not source.exists():
        print(f"ERROR: source skill directory does not exist: {source}", file=sys.stderr)
        return 1
    if target.exists():
        print(f"ERROR: target already exists and overwrite is not supported: {target}", file=sys.stderr)
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    write_install_record(manifest, manifest_path, source, target, "install", None, "not_run", "fresh_install")
    print_action_result("install", manifest, source, target, None, "not_run", 0, {"install_result": "pass"})
    return 0


def upgrade_skill(
    manifest: dict[str, Any],
    manifest_path: Path,
    source: Path,
    target: Path,
    root: Path,
    repo_root: Path,
) -> int:
    if not source.exists():
        print(f"ERROR: source skill directory does not exist: {source}", file=sys.stderr)
        return 1
    if not target.exists():
        print(f"ERROR: target does not exist; use --install before --upgrade: {target}", file=sys.stderr)
        return 1
    previous_record = read_install_record(target)
    status = version_status(manifest, previous_record)
    backup = create_backup(manifest, target, "upgrade")
    shutil.rmtree(target)
    shutil.copytree(source, target)
    write_install_record(manifest, manifest_path, source, target, "upgrade", backup, "pending", status)
    verify_code = run_verify(manifest, target, root, repo_root)
    verify_result = "pass" if verify_code == 0 else "fail"
    write_install_record(manifest, manifest_path, source, target, "upgrade", backup, verify_result, status)
    print_action_result("upgrade", manifest, source, target, backup, verify_result, verify_code, {"version_status": status})
    return verify_code


def uninstall_skill(
    manifest: dict[str, Any],
    source: Path,
    target: Path,
) -> int:
    if manifest.get("lifecycle_status") == "compatibility" and manifest.get("provided_by_suite"):
        print(
            f"note: {manifest['skill_name']} is a compatibility standalone entry provided by suite "
            f"{manifest['provided_by_suite']}; uninstall only affects this standalone target.",
        )
    if not target.exists():
        print_action_result("uninstall", manifest, source, target, None, "not_applicable", 0, {"uninstall_result": "target_absent"})
        return 0
    backup = create_backup(manifest, target, "uninstall")
    shutil.rmtree(target)
    print_action_result("uninstall", manifest, source, target, backup, "not_applicable", 0, {"uninstall_result": "pass"})
    return 0


def rollback_skill(
    manifest: dict[str, Any],
    manifest_path: Path,
    source: Path,
    target: Path,
    root: Path,
    repo_root: Path,
) -> int:
    backup = latest_backup(manifest)
    if backup is None:
        print(f"ERROR: no backup available for rollback: {manifest['skill_name']}", file=sys.stderr)
        return 1
    pre_rollback_backup = create_backup(manifest, target, "pre-rollback") if target.exists() else None
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(backup, target)
    verify_code = run_verify(manifest, target, root, repo_root)
    verify_result = "pass" if verify_code == 0 else "fail"
    write_install_record(
        manifest,
        manifest_path,
        source,
        target,
        "rollback",
        pre_rollback_backup or backup,
        verify_result,
        "rollback_to_latest_backup",
    )
    print_action_result(
        "rollback",
        manifest,
        source,
        target,
        backup,
        verify_result,
        verify_code,
        {"rollback_source": str(backup), "pre_rollback_backup": str(pre_rollback_backup) if pre_rollback_backup else "none"},
    )
    return verify_code


def run(args: argparse.Namespace) -> int:
    root = harness_root()
    repo_root = find_repo_root(root)
    manifest_path = resolve_project_path(args.manifest, root, repo_root)
    manifest = read_json(manifest_path)
    check_required_manifest_fields(manifest)
    require_codex_home(manifest)

    source = resolve_project_path(manifest["source_path"], root, repo_root)
    target = Path(expand_placeholders(manifest["target_path"], root, repo_root, None)).resolve()

    if args.dry_run:
        print_plan(manifest, source, target, root, repo_root)
        return 0 if source.exists() else 1

    if args.install:
        return install_skill(manifest, manifest_path, source, target)

    if args.verify:
        return run_verify(manifest, target, root, repo_root)

    if args.upgrade:
        return upgrade_skill(manifest, manifest_path, source, target, root, repo_root)

    if args.uninstall:
        return uninstall_skill(manifest, source, target)

    if args.rollback:
        return rollback_skill(manifest, manifest_path, source, target, root, repo_root)

    raise SystemExit("ERROR: choose one of --dry-run, --install, --verify, --upgrade, --uninstall, or --rollback")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install or verify a packaged Codex skill from a manifest.")
    parser.add_argument("--manifest", required=True, help="Path to skill install manifest JSON.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Validate manifest and print install plan.")
    mode.add_argument("--install", action="store_true", help="Install the skill without overwriting existing target.")
    mode.add_argument("--verify", action="store_true", help="Verify installed skill files and commands.")
    mode.add_argument("--upgrade", action="store_true", help="Backup existing target, replace from source, write install record, then verify.")
    mode.add_argument("--uninstall", action="store_true", help="Backup and remove the installed target.")
    mode.add_argument("--rollback", action="store_true", help="Restore the most recent backup and verify.")
    return run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
