---
name: github-group-manager
description: Manages GitHub Teams within the ACME organization. Use for creating new teams, requesting to join existing teams, listing teams, and removing team members. Handles both automated (via GitHub token) and manual workflows.
---

# GitHub Group Manager

This skill manages GitHub Teams within the `ACME` GitHub Enterprise account, under the `example` organization. It supports both automated management via the `gh` CLI (if a token is available) and a guided manual workflow.

## Core Workflows

The skill first checks for the `GH_TOKEN` environment variable to decide which workflow to follow.

1.  **Check for GitHub Token**: Run `echo $GH_TOKEN` to check if the token is set.
2.  **Automated Workflow**: If the token exists and has a value, follow the "Automated Workflow" instructions.
3.  **Manual Workflow**: If the token is not found or is empty, follow the "Manual Workflow" instructions.

---

## Automated Workflow (GH_TOKEN available)

This workflow uses the `gh` CLI to perform actions directly. All team creation and membership changes will create a GitHub Issue in the `example/team-requests` repository to be approved by the DevOps team. Each approval issue automatically includes a table of all existing teams in the organization for reference and to help prevent duplicate team creation.

### 1. Create a New Team

**Action**: Create a new GitHub Team.

**Command**:

```bash
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /orgs/example/teams \
  -f name=\"{team_name}\" \
  -f description=\"{team_description}\" \
  -f privacy=\"closed\" 
```

**Post-Action**: Create a GitHub issue to request approval, including a list of existing teams.

```bash
gh issue create \
  --repo example/team-requests \
  --title "Request to create team: {team_name}" \
  --body "Please approve the creation of the new team: **{team_name}**. Description: {team_description}.

## Existing Teams

| Team Name | Slug | Privacy | Members |
|-----------|------|---------|---------|
| ... | ... | ... | ... |"
```

### 2. Request to Join a Team

**Action**: Request to add a user to an existing team.

**Command**:

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  /orgs/example/teams/{team_slug}/memberships/{username}
```

**Post-Action**: Create a GitHub issue to request approval, including a list of existing teams.

```bash
gh issue create \
  --repo example/team-requests \
  --title "Request to add {username} to {team_name}" \
  --body "Please approve adding **{username}** to the **{team_name}** team.

## Existing Teams

| Team Name | Slug | Privacy | Members |
|-----------|------|---------|---------|
| ... | ... | ... | ... |"
```

### 3. List Existing Teams

**Action**: List all teams in the `example` organization.

**Command**:

```bash
gh api \
  --method GET \
  -H "Accept: application/vnd.github+json" \
  /orgs/example/teams
```

### 4. Remove a Member from a Team

**Action**: Remove a user from a team.

**Command**:

```bash
gh api \
  --method DELETE \
  -H "Accept: application/vnd.github+json" \
  /orgs/example/teams/{team_slug}/memberships/{username}
```

**Post-Action**: Create a GitHub issue to document the removal, including a list of existing teams.

```bash
gh issue create \
  --repo example/team-requests \
  --title "Removed {username} from {team_name}" \
  --body "**{username}** has been removed from the **{team_name}** team.

## Existing Teams

| Team Name | Slug | Privacy | Members |
|-----------|------|---------|---------|
| ... | ... | ... | ... |"
```

---

## Manual Workflow (GH_TOKEN not available)

This workflow guides the user to perform the actions manually through the GitHub web interface.

### 1. Create a New Team

1.  **Guide the user**: Instruct the user to navigate to `https://github.com/orgs/example/teams` and click the "New team" button.
2.  **Collect information**: Ask the user for the **Team name** and **Description**.
3.  **Approval Request**: Instruct the user to create a new issue in the `example/team-requests` repository with the title `Request to create team: {team_name}` and a description of the request. Include a list of existing teams for reference.

### 2. Request to Join a Team

1.  **Guide the user**: Instruct the user to navigate to the team's page at `https://github.com/orgs/example/teams/{team_slug}`.
2.  **Request to join**: Instruct the user to click the "Request to join" button.
3.  **Approval Request**: The request will be sent to the team maintainers for approval.

### 3. List Existing Teams

1.  **Guide the user**: Instruct the user to navigate to `https://github.com/orgs/example/teams` to see a list of all teams.

### 4. Remove a Member from a Team

1.  **Guide the user**: Instruct the user (who must be a team maintainer) to navigate to the team's "Members" tab at `https://github.com/orgs/example/teams/{team_slug}/members`.
2.  **Remove member**: Instruct the user to find the member to be removed and select "Remove from team" from the dropdown menu.
3.  **Documentation**: Instruct the user to create a new issue in the `example/team-requests` repository to document the removal.
