#!/usr/bin/env python3
"""
Main execution script for GitHub App Repository Management
"""
from dotenv import load_dotenv
import os

from gh_api_client import list_user_repos, create_codeowners_file
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
    print("🚀 Authenticating with PAT")
    gh_api_client.authenticate_with_pat(os.getenv("GITHUB_PAT"))

    # # Step 1: Create list of repository IDs
    # print("🚀 Listing GitHub Repositories")
    # search_criteria = ""
    # repo_id_list = []
    # repo_list = gh_api_client.get_user_repos("OD-Oraf")
    #
    # for repo in repo_list:
    #     if search_criteria.strip() != "" and search_criteria not in repo["name"]:
    #         continue
    #     repo_id_list.append(repo["id"])
    #     print(repo)
    #
    # print("repo_id_list: ", repo_id_list)
    #
    # # Add repositories to GitHub App installation
    # for repo_id in repo_id_list:
    #     add_repo_to_app_installation(os.getenv("GITHUB_APP_INSTALLATION_ID"), repo_id)

    # gh_api_client.add_repos_to_app_installation(username="OD-Oraf")

    create_codeowners_file("https://github.com/OD-Oraf/gh-cli-scripts", code_owners="OD-ORAF")
    #
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
