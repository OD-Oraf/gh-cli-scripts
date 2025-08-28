# GitHub CLI Commands Reference

This document contains all the GitHub CLI commands used in the project for easy reference and independent execution.

## Table of Contents
- [Authentication & Setup](#authentication--setup)
- [Repository Management](#repository-management)
- [GitHub App Management](#github-app-management)
- [API Calls](#api-calls)
- [Collaborator Management](#collaborator-management)
- [Repository Operations](#repository-operations)

## Authentication & Setup

### Get your GitHub token
```bash
gh auth token
```

### Set environment variable for scripts
```bash
export GITHUB_TOKEN=$(gh auth token)
```

## Repository Management

### List repositories
```bash
# List repositories under current user
gh repo list

# With JSON output and specific fields
gh repo list --json name,id,isPrivate,url --limit 10

# With detailed info
gh repo list --json name,id,url,isPrivate,description,updatedAt --limit 20
```

### Create repository
```bash
# Public repository
gh repo create my-repo --public

# Private repository with description
gh repo create my-repo --private --description "My new repository"
```

### Clone repository
```bash
gh repo clone owner/repo-name
gh repo clone owner/repo-name local-directory
```

### Fork repository
```bash
gh repo fork owner/repo-name
```

### Edit repository settings
```bash
# Change visibility to private
gh repo edit owner/repo-name --visibility private

# Change visibility to public
gh repo edit owner/repo-name --visibility public
```

## GitHub App Management
NOTE REQUIRES AUTHENTICATION WITH GITHUB APP TOKEN
### List GitHub App installations
```bash
gh api /user/installations
```

### Get installation repositories
```bash
gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" /installation/repositories
```

### Add repository to GitHub App installation
```bash
gh api --method PUT /user/installations/{installation_id}/repositories/{repo_id}
```

### List repositories in an installation
```bash
gh api /user/installations/{installation_id}/repositories
```

## API Calls

### Get repository information
```bash
gh api /repos/owner/repo-name
```

### Get repository collaborators
```bash
gh api /repos/owner/repo-name/collaborators
```

### Add collaborator to repository
```bash
gh api --method PUT /repos/owner/repo-name/collaborators/username --input - <<< '{"permission": "push"}'
```

### Create GitHub App access token
```bash
# This requires a JWT token first
curl --request POST \
--url "https://api.github.com/app/installations/{installation_id}/access_tokens" \
--header "Accept: application/vnd.github+json" \
--header "Authorization: Bearer {JWT_TOKEN}" \
--header "X-GitHub-Api-Version: 2022-11-28"
```

### Get GitHub App information
```bash
gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  /app
```

## Collaborator Management

### List collaborators
```bash
gh api /repos/owner/repo-name/collaborators
```

### Add collaborator with specific permission
```bash
# Push permission
gh api --method PUT /repos/owner/repo-name/collaborators/username --input - <<< '{"permission": "push"}'

# Pull permission
gh api --method PUT /repos/owner/repo-name/collaborators/username --input - <<< '{"permission": "pull"}'

# Admin permission
gh api --method PUT /repos/owner/repo-name/collaborators/username --input - <<< '{"permission": "admin"}'
```

## Repository Operations

### Get repository ID (for use with GitHub Apps)
```bash
gh api /repos/owner/repo-name | jq '.id'
```

### Check repository details
```bash
gh repo view owner/repo-name
```

### List repository issues
```bash
gh issue list --repo owner/repo-name
```

### List repository pull requests
```bash
gh pr list --repo owner/repo-name
```

## Example Usage Scenarios

### Scenario 1: Add a repository to GitHub App installation
```bash
# 1. Get repository ID
REPO_ID=$(gh api /repos/owner/repo-name | jq '.id')

# 2. Add to installation
gh api --method PUT /user/installations/{installation_id}/repositories/$REPO_ID

# 3. Verify addition
gh api /user/installations/{installation_id}/repositories
```

### Scenario 2: Create and setup a new repository
```bash
# 1. Create repository
gh repo create my-new-repo --private --description "My new project"

# 2. Clone it locally
gh repo clone owner/my-new-repo

# 3. Add collaborators
gh api --method PUT /repos/owner/my-new-repo/collaborators/username --input - <<< '{"permission": "push"}'
```

### Scenario 3: Manage GitHub App installations
```bash
# 1. List all installations
gh api /user/installations

# 2. List repositories in specific installation
gh api /user/installations/{installation_id}/repositories

# 3. Add repository to installation
gh api --method PUT /user/installations/{installation_id}/repositories/{repo_id}
```

## Notes

- Replace `{installation_id}`, `{repo_id}`, `owner`, `repo-name`, and `username` with actual values
- Some commands require specific permissions or GitHub App installations
- For GitHub App operations, you may need to generate JWT tokens first using the `gen_app_token.py` script
- Always verify operations by checking the results with list commands

## Related Files in Project

- `gen_app_token.py` - Generates JWT tokens for GitHub App authentication
- `gh_script.py` - Python wrapper for GitHub App operations
- `gh_repo_manager.py` - Python wrapper for repository management
- `script.sh` - Bash script for adding repositories to GitHub App installations
