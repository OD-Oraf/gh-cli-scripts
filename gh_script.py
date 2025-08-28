#!/usr/bin/env python3
"""
GitHub App Repository Management using GitHub CLI
This script uses 'gh' commands instead of direct API calls for better reliability.
"""

import subprocess
import json
import sys
import os
from dotenv import load_dotenv

import gen_app_token as generate_github_token

# Load environment variables from .env file
load_dotenv()


def run_gh_command(command):
    """Run a GitHub CLI command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return {"success": True, "output": result.stdout.strip(), "error": None}
    except subprocess.CalledProcessError as e:
        return {"success": False, "output": None, "error": e.stderr.strip()}


def list_github_apps():
    """List GitHub Apps you have access to"""
    print("🔍 Checking GitHub Apps...")
    
    # Check if you have any GitHub Apps
    result = run_gh_command("gh api /user/installations")
    
    if result["success"]:
        try:
            installations = json.loads(result["output"])
            if installations.get("total_count", 0) > 0:
                print(f"✅ Found {installations['total_count']} GitHub App installation(s):")
                for install in installations["installations"]:
                    print(f"   - App: {install['app_slug']} (ID: {install['id']})")
                    print(f"     Account: {install['account']['login']}")
                return installations["installations"]
            else:
                print("❌ No GitHub App installations found")
                return []
        except json.JSONDecodeError:
            print(f"❌ Failed to parse installations response: {result['output']}")
            return []
    else:
        print(f"❌ Failed to list installations: {result['error']}")
        return []


def get_repo_info(owner, repo_name):
    """Get repository information using GitHub CLI"""
    print(f"🔍 Getting info for repository: {owner}/{repo_name}")
    
    result = run_gh_command(f"gh api /repos/{owner}/{repo_name}")
    
    if result["success"]:
        try:
            repo_data = json.loads(result["output"])
            print(f"✅ Repository found:")
            print(f"   - Name: {repo_data['full_name']}")
            print(f"   - ID: {repo_data['id']}")
            print(f"   - Node ID: {repo_data['node_id']}")
            print(f"   - Private: {repo_data['private']}")
            return repo_data
        except json.JSONDecodeError:
            print(f"❌ Failed to parse repository response: {result['output']}")
            return None
    else:
        print(f"❌ Repository not found or access denied: {result['error']}")
        return None


def list_user_repos():
    """List your repositories"""
    print("🔍 Listing your repositories...")
    
    result = run_gh_command("gh repo list --json name,id,url --limit 10")
    
    if result["success"]:
        try:
            repos = json.loads(result["output"])
            # Pretty print the JSON response
            print("📋 Repository JSON Response:")
            print(json.dumps(repos, indent=2))
            return repos
        except json.JSONDecodeError:
            print(f"❌ Failed to parse repositories response: {result['output']}")
            return []
    else:
        print(f"❌ Failed to list repositories: {result['error']}")
        return []


def add_repo_to_app_installation(installation_id, repo_id):
    """Add a repository to a GitHub App installation using gh CLI"""
    print(f"🔧 Adding repository (ID: {repo_id}) to installation (ID: {installation_id})...")
    
    # Use GitHub CLI to make the API call
    command = f"gh api --method PUT /user/installations/{installation_id}/repositories/{repo_id}"
    result = run_gh_command(command)
    
    if result["success"]:
        print("✅ Repository successfully added to GitHub App installation!")
        return True
    else:
        print(f"❌ Failed to add repository: {result['error']}")
        return False


