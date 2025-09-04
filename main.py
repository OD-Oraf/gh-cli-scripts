#!/usr/bin/env python3
"""
Main execution script for GitHub App Repository Management
"""
from dotenv import load_dotenv
import os

from gh_api_client import list_user_repos
from gh_api_client import add_repo_to_app_installation
from gen_app_token import get_github_app_token
from gh_api_client import authenticate_with_github_app_token
import gh_api_client


import gen_app_token as generate_github_token

# Load environment variables from .env file
load_dotenv()

def log_banner():
    print("=" * 60)
    print("\n" + "=" * 60)
    return[]


def main():
    """Main execution function"""
    print("🚀 GitHub App Repository Management with GitHub CLI")
    log_banner()

    # Step 1: Authenticate with PAT to get List of repositories
    print("🚀 Listing GitHub Repositories")
    gh_api_client.authenticate_with_pat(os.getenv("GITHUB_PAT"))

    # Step 1: Create list of repository IDs
    print("🚀 Listing GitHub Repositories")
    repo_ids = []
    repo_list = list_user_repos()
    for repo in repo_list:
        repo_ids.append(repo["id"])
    print("repo_ids: ", repo_ids)

    # Get GitHub App Token for adding repositories to the installation
    # print("🚀 Getting GitHub App Token")
    # github_app_token = get_github_app_token()
    # print("github_app_token: ", github_app_token)

    # Add repositories to GitHub App installation
    # for repo_id in repo_ids:
    #     add_repo_to_app_installation(os.getenv("GITHUB_APP_INSTALLATION_ID"), repo_id, github_app_token)
    #
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
