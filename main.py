#!/usr/bin/env python3
"""
Main execution script for GitHub App Repository Management
"""

from gh_script import list_user_repos
from gh_script import add_repo_to_app_installation
from gen_app_token import get_github_app_token

def log_banner():
    print("=" * 60)
    print("\n" + "=" * 60)
    return[]


def main():
    """Main execution function"""
    print("🚀 GitHub App Repository Management with GitHub CLI")
    log_banner()

    # Step 1 Use GitHub App Authentication Token
    github_app_token = get_github_app_token()
    print("github_app_token: ", github_app_token)
    
    # Step 1: List your repositories
    print("🚀 Listing GitHub Repositories")
    list_user_repos()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
