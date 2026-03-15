# Test Plan: GitHub Group Manager Skill

## 1. Introduction

This document outlines the test plan for the `github-group-manager` skill, ensuring all functionalities, including the newly implemented dynamic listing of existing teams in approval issues, perform as expected. The objective is to verify the skill's reliability, accuracy, and adherence to specified workflows in both automated and manual modes.

## 2. Test Scope

The test scope covers all features of the GitHub Group Manager skill:
- Listing existing GitHub Teams within the `ACME/example` organization.
- Creating new GitHub Teams and initiating the DevOps approval process.
- Requesting to join existing GitHub Teams and initiating the DevOps approval process.
- Removing members from GitHub Teams and initiating the documentation process.
- Verification of the dynamic inclusion of existing team lists in all generated GitHub issues.
- Validation of both automated (CLI-based) and manual (guided) workflows.

## 3. Test Environment

### Prerequisites:
- **GitHub Account**: A GitHub user account with permissions to create issues in the `example/team-requests` repository and, for automated tests, `admin:org` permissions for the `example` organization.
- **GitHub CLI (`gh`)**: Installed and authenticated with a `GH_TOKEN` for automated tests.
- **Python 3.11+**: Installed for running the `gh_team_manager.py` script.
- **Skill Files**: The `github-group-manager` skill directory, including `SKILL.md`, `scripts/gh_team_manager.py`, and `templates/approval_issue_body.md`.
- **`GH_TOKEN` Environment Variable**: Set for automated tests, unset for manual workflow tests.

## 4. Test Cases

### 4.1. Automated Workflow (GH_TOKEN is set)

| Test ID | Description | Steps | Expected Result |
|---|---|---|---|
| **AT-001** | **List Existing Teams** | 1. Set `GH_TOKEN` environment variable. <br> 2. Run `python3 scripts/gh_team_manager.py list` | A formatted list of all teams in the `example` organization is printed to stdout. |
| **AT-002** | **Create New Team** | 1. Set `GH_TOKEN`. <br> 2. Run `python3 scripts/gh_team_manager.py create --name "NewTeam" --description "Test team"` | 1. Console output confirms team creation. <br> 2. A new GitHub issue is created in `example/team-requests` with title "Request to create team: NewTeam". <br> 3. The issue body contains "Please review and approve..." and a Markdown table of existing teams. |
| **AT-003** | **Request to Join Team** | 1. Set `GH_TOKEN`. <br> 2. Run `python3 scripts/gh_team_manager.py join --team "existing-team-slug" --username "testuser"` | 1. Console output confirms membership request. <br> 2. A new GitHub issue is created in `example/team-requests` with title "Request to add testuser to existing-team-slug". <br> 3. The issue body contains "Please approve adding..." and a Markdown table of existing teams. |
| **AT-004** | **Remove Member from Team** | 1. Set `GH_TOKEN`. <br> 2. Run `python3 scripts/gh_team_manager.py remove --team "existing-team-slug" --username "testuser"` | 1. Console output confirms member removal. <br> 2. A new GitHub issue is created in `example/team-requests` with title "Removed testuser from existing-team-slug". <br> 3. The issue body contains "testuser has been removed..." and a Markdown table of existing teams. |
| **AT-005** | **Missing GH_TOKEN** | 1. Unset `GH_TOKEN`. <br> 2. Run any command, e.g., `python3 scripts/gh_team_manager.py list` | Script exits with an error message indicating `GH_TOKEN` is not set. |

### 4.2. Manual Workflow (GH_TOKEN is not set)

| Test ID | Description | Steps | Expected Result |
|---|---|---|---|
| **MT-001** | **Create New Team** | 1. Unset `GH_TOKEN`. <br> 2. Invoke the skill for team creation. | The skill provides clear, step-by-step instructions to create a team via the GitHub web UI and to manually create an approval issue in `example/team-requests`. |
| **MT-002** | **Request to Join Team** | 1. Unset `GH_TOKEN`. <br> 2. Invoke the skill for joining a team. | The skill provides clear, step-by-step instructions to request to join a team via the GitHub web UI. |
| **MT-003** | **List Existing Teams** | 1. Unset `GH_TOKEN`. <br> 2. Invoke the skill for listing teams. | The skill provides clear instructions to navigate to `https://github.com/orgs/example/teams` to view existing teams. |
| **MT-004** | **Remove Member from Team** | 1. Unset `GH_TOKEN`. <br> 2. Invoke the skill for removing a member. | The skill provides clear, step-by-step instructions to remove a member via the GitHub web UI and to manually create a documentation issue. |

## 5. Pass/Fail Criteria

- **Pass**: All test cases execute successfully, and the actual results match the expected results without any errors or deviations.
- **Fail**: Any test case does not meet its expected result, encounters an error, or deviates from the defined behavior.

## 6. Conclusion

Successful execution of this test plan will confirm the robust functionality of the GitHub Group Manager skill, ensuring it effectively streamlines GitHub team management while maintaining the necessary DevOps oversight and auditability. This includes verifying the dynamic inclusion of existing team information in all relevant GitHub issues, enhancing the approval process.

