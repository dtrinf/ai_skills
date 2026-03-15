# GitHub Group Manager Skill

This skill provides a standardized way to manage GitHub Teams within the **ACME** GitHub Enterprise account, specifically under the **example** organization. It is designed to be used by Manus agents to automate group creation and enrollment requests while ensuring all changes are approved by the DevOps team.

## Features

- **Automated Workflow**: Uses the `gh` CLI to perform actions directly if a `GH_TOKEN` is available.
- **Manual Workflow**: Provides step-by-step guidance for users to perform actions through the GitHub web interface when no token is present.
- **DevOps Approval**: Every modification (creating a team, joining a team, or removing a member) automatically triggers an approval request via a GitHub Issue in the `example/team-requests` repository.
- **Team Management**: Supports listing teams, creating new teams, requesting membership, and removing members.

## Skill Structure

```text
github-group-manager/
├── SKILL.md                 # Core instructions and workflows
├── README.md                # Skill documentation (this file)
├── scripts/
│   └── gh_team_manager.py   # CLI tool for automated management
└── templates/
    └── approval_issue_body.md # Template for DevOps approval issues
```

## How to Use

### For Manus Agents

When this skill is active, Manus will:
1. Check for the `GH_TOKEN` environment variable.
2. If found, use the `scripts/gh_team_manager.py` script to perform the requested action.
3. If not found, guide the user through the manual steps outlined in `SKILL.md`.

### Manual CLI Usage

If you have the `gh` CLI installed and a valid `GH_TOKEN`, you can run the helper script directly:

```bash
# List all teams
python3 scripts/gh_team_manager.py list

# Create a new team (requires DevOps approval)
python3 scripts/gh_team_manager.py create --name "Frontend-Devs" --description "Frontend engineering team"

# Request to join a team (requires DevOps approval)
python3 scripts/gh_team_manager.py join --team "frontend-devs" --username "jdoe"

# Remove a member (documents the removal)
python3 scripts/gh_team_manager.py remove --team "frontend-devs" --username "jdoe"
```

## Approval Workflow

All write operations are logged in the `example/team-requests` repository. The DevOps team must review and close the generated issues to finalize the process.

---
*Created by Manus AI*
