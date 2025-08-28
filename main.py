#!/usr/bin/env python3
"""
Main execution script for GitHub App Repository Management
"""

from gh_script import list_user_repos


def main():
    """Main execution function"""
    print("🚀 GitHub App Repository Management with GitHub CLI")
    print("=" * 60)
    
    # Step 1: Check GitHub Apps
    # installations = list_github_apps()
    
    print("\n" + "=" * 60)
    
    # Step 2: List your repositories
    list_user_repos()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
