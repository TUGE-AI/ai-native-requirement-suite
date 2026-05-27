# idea-to-demand Examples

status: `public_preview`

## Positive Example: Team Knowledge Search Assistant

Input:

> I want to build a knowledge search assistant for project teams. It should help members find decision records and requirement background faster, but the features are not clear yet.

Expected output:

```yaml
target_users:
  - "Project team members who need to understand requirement context"
  - "Product, engineering, and testing leads who review past decisions"
problem: "Project knowledge is scattered across documents, chats, and issue discussions, making it hard to find reliable context before making product or engineering decisions."
business_goal: "Reduce time spent searching for requirement background and improve consistency of project decisions."
scenarios:
  - "A product manager wants to find why a feature was scoped out."
  - "An engineer wants to confirm the latest accepted behavior before coding."
  - "A tester wants to find related decisions before writing test cases."
first_scope:
  - "Index selected project documents and requirement assets."
  - "Support natural-language search over approved source material."
  - "Return answer summaries with source references."
non_goals:
  - "Do not automatically edit source documents in the first version."
  - "Do not replace human review for conflicting decisions."
  - "Do not ingest private documents without explicit configuration."
assumptions:
  - "The team has at least some structured documents or requirement assets."
  - "Users care about source references, not only generated summaries."
open_questions:
  - "Which document sources should be supported first?"
  - "Who can mark an answer or source as authoritative?"
  - "How should stale or conflicting documents be shown?"
risks:
  - "If source quality is low, generated answers may look confident but remain unreliable."
  - "If access control is unclear, the assistant may expose material to the wrong audience."
next_step: demand-to-prd-spec
```

## Low-Information Example

Input:

> Help me work on this requirement.

Expected output:

```yaml
target_users: []
problem: ""
business_goal: ""
scenarios: []
first_scope: []
non_goals: []
assumptions: []
open_questions:
  - "Which users or roles is this requirement for?"
  - "What core problem should it solve?"
  - "Is the current material an idea, demand brief, PRD/spec, or existing Feature/Story?"
  - "Do you want a demand brief, PRD/spec, AI-ready asset package, or quality review next?"
risks:
  - "The current input is too thin; generating a full requirement would invent users, scope, and value assumptions."
next_step: more_clarification
```
