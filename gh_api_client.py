#!/usr/bin/env python3
"""
GitHub App Repository Management using GitHub CLI
This script uses 'gh' commands instead of direct API calls for better reliability.
"""
import shutil
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
        print(f"🔍 DEBUG: Running command: {command}")
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"🔍 DEBUG: Command succeeded. Output length: {len(result.stdout)} chars")
        return {"success": True, "output": result.stdout.strip(), "error": None}
    except subprocess.CalledProcessError as e:
        print(f"🔍 DEBUG: Command failed with exit code: {e.returncode}")
        print(f"🔍 DEBUG: stderr: {e.stderr.strip()}")
        print(f"🔍 DEBUG: stdout: {e.stdout.strip() if e.stdout else 'None'}")
        return {"success": False, "output": e.stdout.strip() if e.stdout else None, "error": e.stderr.strip()}


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


def get_user_repos(username):
    """Get repositories for a specific user using GitHub API"""
    print(f"🔍 Getting repositories for user: {username}")
    
    command = (
        f"gh api "
        f"-H 'Accept: application/vnd.github+json' "
        f"-H 'X-GitHub-Api-Version: 2022-11-28' "
        f"/users/{username}/repos"
    )
    
    result = run_gh_command(command)
    
    if result["success"]:
        try:
            repos = json.loads(result["output"])
            print(f"✅ Found {len(repos)} repositories for user {username}")
            return repos
        except json.JSONDecodeError:
            print(f"❌ Failed to parse repositories response: {result['output']}")
            return []
    else:
        print(f"❌ Failed to get repositories for user {username}: {result['error']}")
        return []


def get_org_repos(org_name):
    """Get repositories for a specific organization using GitHub API"""
    print(f"🔍 Getting repositories for organization: {org_name}")
    
    command = (
        f"gh api "
        f"-H 'Accept: application/vnd.github+json' "
        f"-H 'X-GitHub-Api-Version: 2022-11-28' "
        f"/orgs/{org_name}/repos"
    )
    
    result = run_gh_command(command)
    
    if result["success"]:
        try:
            repos = json.loads(result["output"])
            print(f"✅ Found {len(repos)} repositories for organization {org_name}")
            return repos
        except json.JSONDecodeError:
            print(f"❌ Failed to parse repositories response: {result['output']}")
            return []
    else:
        print(f"❌ Failed to get repositories for organization {org_name}: {result['error']}")
        return []


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
    command = (
        f"gh api --method PUT "
        f"-H 'Accept: application/vnd.github+json' "
        f"-H 'X-GitHub-Api-Version: 2022-11-28' "
        f"/user/installations/{installation_id}/repositories/{repo_id}"
    )
    
    print(f"🔍 DEBUG: Executing command: {command}")
    result = run_gh_command(command)
    
    print(f"🔍 DEBUG: Command result: {result}")
    
    if result["success"]:
        print("✅ Repository successfully added to GitHub App installation!")
        return True
    else:
        print(f"❌ Failed to add repository: {result['error']}")
        return False


def authenticate_with_github_app_token(github_app_token):
    """Authenticate with GitHub CLI using a GitHub App token"""
    print("🔐 Authenticating with GitHub App...")
    
    try:
        # Use subprocess directly to pipe token via stdin for security
        result = subprocess.run(
            ["gh", "auth", "login", "--with-token"],
            input=github_app_token,
            text=True,
            capture_output=True,
            check=True
        )
        print("✅ Successfully authenticated with GitHub App Token")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to authenticate with GitHub App Token:")
        print(f"   Error: {e.stderr.strip()}")
        if e.stdout:
            print(f"   Output: {e.stdout.strip()}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during authentication: {str(e)}")
        return False


def authenticate_with_pat(pat):
    """Authenticate with GitHub CLI using a Personal Access Token (PAT)"""
    print("🔐 Authenticating with Personal Access Token...")
    
    try:
        # Use subprocess directly to pipe token via stdin for security
        result = subprocess.run(
            ["gh", "auth", "login", "--with-token"],
            input=pat,
            text=True,
            capture_output=True,
            check=True
        )
        print("✅ Successfully authenticated with Personal Access Token")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to authenticate with Personal Access Token:")
        print(f"   Error: {e.stderr.strip()}")
        if e.stdout:
            print(f"   Output: {e.stdout.strip()}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during authentication: {str(e)}")
        return False


def add_repos_to_app_installation(username=None, org_name=None, search_criteria=""):
    """Add repositories to GitHub App installation with optional search filtering"""
    
    # Get repos from user or org
    if username:
        repo_list = get_user_repos(username)
    elif org_name:
        repo_list = get_org_repos(org_name)
    else:
        print("❌ Provide either username or org_name")
        return
    
    # Filter and add repos to installation
    for repo in repo_list:
        if search_criteria.strip() != "" and search_criteria not in repo["name"]:
            continue
        add_repo_to_app_installation(os.getenv("GITHUB_APP_INSTALLATION_ID"), repo["id"])


def create_codeowners_file(repo_url, code_owners="OD-ORAF"):
    """
    Checkout a repository and create a CODEOWNERS file at .github/CODEOWNERS
    
    Args:
        repo_url (str): The URL of the repository to checkout
        code_owners (str, optional): The GitHub username or team to set as code owner. 
                                   Defaults to "OD-ORAF".
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Extract repository name from URL for directory naming
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        
        print(f"Cloning repository: {repo_url}")
        
        # Clone the repository
        clone_result = subprocess.run(['git', 'clone', repo_url], 
                                    capture_output=True, text=True)
        if clone_result.returncode != 0:
            print(f"Error cloning repository: {clone_result.stderr}")
            return False
        
        # Change to the repository directory
        repo_dir = repo_name
        if not os.path.exists(repo_dir):
            print(f"Repository directory {repo_dir} not found after cloning")
            return False
        
        # Create .github directory if it doesn't exist
        github_dir = os.path.join(repo_dir, '.github')
        os.makedirs(github_dir, exist_ok=True)
        
        # Create CODEOWNERS file
        codeowners_path = os.path.join(github_dir, 'CODEOWNERS')
        codeowners_content = f"""# Global code owners \n * @{code_owners}

        """
        
        with open(codeowners_path, 'w') as f:
            f.write(codeowners_content)
        
        print(f"Created CODEOWNERS file at {codeowners_path}")
        
        # Change to repository directory for git operations
        original_dir = os.getcwd()
        os.chdir(repo_dir)
        
        try:
            # Add the CODEOWNERS file to git
            add_result = subprocess.run(['git', 'add', '.github/CODEOWNERS'], 
                                     capture_output=True, text=True)
            if add_result.returncode != 0:
                print(f"Error adding CODEOWNERS file: {add_result.stderr}")
                return False
            
            # Commit the changes
            commit_result = subprocess.run(['git', 'commit', '-m', f'Add CODEOWNERS file with {code_owners} as owner'],
                                        capture_output=True, text=True)
            if commit_result.returncode != 0:
                print(f"Error committing CODEOWNERS file: {commit_result.stderr}")
                return False
            
            # Push the changes
            push_result = subprocess.run(['git', 'push'], capture_output=True, text=True)
            if push_result.returncode != 0:
                print(f"Error pushing CODEOWNERS file: {push_result.stderr}")
                return False
            
            print("Successfully created and pushed CODEOWNERS file")
            return True
            
        finally:
            # Change back to original directory
            os.chdir(original_dir)
    
    except Exception as e:
        print(f"Error creating CODEOWNERS file: {str(e)}")
        return False