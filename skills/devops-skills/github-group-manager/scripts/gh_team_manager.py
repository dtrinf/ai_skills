#!/usr/bin/env python3
"""
GitHub Team Manager
Manages GitHub Teams in the ACME/example organization.
Requires GH_TOKEN environment variable with appropriate org permissions.
"""

import os
import sys
import json
import argparse
import subprocess


ORG = "example"
REQUESTS_REPO = "example/team-requests"


def run_gh(args: list[str]) -> dict | list | None:
    """Run a gh CLI command and return parsed JSON output."""
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("ERROR: GH_TOKEN environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    env = os.environ.copy()
    env["GH_TOKEN"] = token

    result = subprocess.run(
        ["gh"] + args,
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        print(f"ERROR: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(result.returncode)

    if result.stdout.strip():
        return json.loads(result.stdout)
    return None


def create_approval_issue(title: str, body: str) -> None:
    """Create a GitHub issue in the team-requests repo for DevOps approval."""
    run_gh([
        "issue", "create",
        "--repo", REQUESTS_REPO,
        "--title", title,
        "--body", body,
    ])
    print(f"Approval issue created in {REQUESTS_REPO}: {title}")


def list_teams() -> None:
    """List all teams in the organization."""
    teams = run_gh([
        "api",
        "--method", "GET",
        "-H", "Accept: application/vnd.github+json",
        f"/orgs/{ORG}/teams",
    ])
    if not teams:
        print("No teams found.")
        return
    print(f"{'Name':<30} {'Slug':<30} {'Privacy':<10} {'Members'}")
    print("-" * 80)
    for team in teams:
        print(f"{team['name']:<30} {team['slug']:<30} {team['privacy']:<10} {team['members_count']}")


def create_team(name: str, description: str) -> None:
    """Create a new team and open an approval issue."""
    result = run_gh([
        "api",
        "--method", "POST",
        "-H", "Accept: application/vnd.github+json",
        f"/orgs/{ORG}/teams",
        "-f", f"name={name}",
        "-f", f"description={description}",
        "-f", "privacy=closed",
    ])
    print(f"Team '{name}' created (slug: {result['slug']}).")
    create_approval_issue(
        title=f"Request to create team: {name}",
        body=f"Please review and approve the creation of the new team: **{name}**.\n\nDescription: {description}",
    )


def request_membership(team_slug: str, username: str) -> None:
    """Request to add a user to an existing team and open an approval issue."""
    run_gh([
        "api",
        "--method", "PUT",
        "-H", "Accept: application/vnd.github+json",
        f"/orgs/{ORG}/teams/{team_slug}/memberships/{username}",
    ])
    print(f"Membership request submitted for '{username}' in team '{team_slug}'.")
    create_approval_issue(
        title=f"Request to add {username} to {team_slug}",
        body=f"Please approve adding **{username}** to the **{team_slug}** team.",
    )


def remove_member(team_slug: str, username: str) -> None:
    """Remove a user from a team and open a documentation issue."""
    run_gh([
        "api",
        "--method", "DELETE",
        "-H", "Accept: application/vnd.github+json",
        f"/orgs/{ORG}/teams/{team_slug}/memberships/{username}",
    ])
    print(f"'{username}' has been removed from team '{team_slug}'.")
    create_approval_issue(
        title=f"Removed {username} from {team_slug}",
        body=f"**{username}** has been removed from the **{team_slug}** team.",
    )


def main():
    parser = argparse.ArgumentParser(description="GitHub Team Manager for ACME/example org")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    subparsers.add_parser("list", help="List all teams in the organization")

    # create
    p_create = subparsers.add_parser("create", help="Create a new team")
    p_create.add_argument("--name", required=True, help="Team name")
    p_create.add_argument("--description", default="", help="Team description")

    # join
    p_join = subparsers.add_parser("join", help="Request to join a team")
    p_join.add_argument("--team", required=True, help="Team slug")
    p_join.add_argument("--username", required=True, help="GitHub username to add")

    # remove
    p_remove = subparsers.add_parser("remove", help="Remove a member from a team")
    p_remove.add_argument("--team", required=True, help="Team slug")
    p_remove.add_argument("--username", required=True, help="GitHub username to remove")

    args = parser.parse_args()

    if args.command == "list":
        list_teams()
    elif args.command == "create":
        create_team(args.name, args.description)
    elif args.command == "join":
        request_membership(args.team, args.username)
    elif args.command == "remove":
        remove_member(args.team, args.username)


if __name__ == "__main__":
    main()

