#!/usr/bin/env python3
"""
Main execution script for GitHub App Repository Management
"""
from dotenv import load_dotenv
import os

from gh_script import list_user_repos
from gh_script import add_repo_to_app_installation
from gen_app_token import get_github_app_token
from gh_script import authenticate_with_github_app_token
import gh_script


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
    # Step 1: List your repositories
    print("🚀 Listing GitHub Repositories")
    gh_script.authenticate_with_pat(os.getenv("GITHUB_PAT"))

    # Step 1 Use GitHub App Authentication Token

    
    # Step 1: List your repositories
    print("🚀 Listing GitHub Repositories")
    repo_ids = []
    repo_list = list_user_repos()
    for repo in repo_list:
        repo_ids.append(repo["id"])
    print("repo_ids: ", repo_ids)

    print("🚀 Authenticating with GitHub App Token")
    github_app_token = get_github_app_token()
    print("github_app_token: ", github_app_token)
    authenticate_with_github_app_token(github_app_token)
    
    # Step 1: List your repositories
    print("🚀 Listing GitHub Repositories")
    list_user_repos()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
