## Step 1: Create an Issue Template
Create a file at .github/ISSUE_TEMPLATE/team-request.yml:

```YAML
name: 🚀 New Team Request
description: Request a new GitHub Team for your project
title: "[Team Request]: "
labels: ["team-management"]
body:
  - type: input
    id: team_name
    attributes:
      label: Team Name
      placeholder: e.g., frontend-alpha
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Team Description
      placeholder: What is this team for?
    validations:
      required: true
```

## Step 2: Create the IssueOps Workflow
Create .github/workflows/issue-ops.yml. This workflow uses a "Slash Command" or "Label" pattern to trigger the skill.

```YAML
name: IssueOps Team Manager
on:
  issues:
    types: [labeled]

jobs:
  manage-team:
    if: github.event.label.name == 'approved' # Only run when DevOps adds 'approved' label
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Skill
        uses: actions/checkout@v4

      - name: Parse Issue Body
        id: parse
        uses: peter-murray/issue-forms-body-parser@v3
        with:
          issue_id: ${{ github.event.issue.number }}
          separator: '###'

      - name: Run Team Manager
        env:
          GH_TOKEN: ${{ secrets.ORG_ADMIN_TOKEN }}
        run: |
          # Extract data from the parsed JSON
          TEAM_NAME=$(echo '${{ steps.parse.outputs.payload }}' | jq -r '.team_name')
          TEAM_DESC=$(echo '${{ steps.parse.outputs.payload }}' | jq -r '.description')
          
          python3 scripts/gh_team_manager.py create \
            --name "$TEAM_NAME" \
            --description "$TEAM_DESC"

      - name: Comment on Issue
        uses: peter-evans/create-or-update-comment@v4
        with:
          issue-number: ${{ github.event.issue.number }}
          body: |
            ✅ **Action Completed!**
            The team **${{ steps.parse.outputs.team_name }}** has been requested. 
            An approval issue has been opened in `example/team-requests`.
```


