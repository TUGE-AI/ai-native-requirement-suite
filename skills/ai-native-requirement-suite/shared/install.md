# AI-native Requirement Suite Install Notes

status: `v0.25-public-preview`

推荐安装 suite 级入口：`ai-native-requirement-suite`。

不推荐单独安装 `requirement-asset-validator` 或 `requirement-wiki-generator`。它们是 suite 的 shared 内部能力。

## 安装命令

在仓库根目录执行：

```powershell
$env:CODEX_HOME = '<你的 CODEX_HOME>'
$py = '<你的可用 Python 路径>'
& $py tools\skill-installer\install_skill.py --manifest install-manifests\ai-native-requirement-suite.user.json --dry-run
& $py tools\skill-installer\install_skill.py --manifest install-manifests\ai-native-requirement-suite.user.json --install
& $py tools\skill-installer\install_skill.py --manifest install-manifests\ai-native-requirement-suite.user.json --verify
```

已安装时使用：

```powershell
& $py tools\skill-installer\install_skill.py --manifest install-manifests\ai-native-requirement-suite.user.json --upgrade
```

完整使用说明见项目根目录 `USER-GUIDE.md`。
