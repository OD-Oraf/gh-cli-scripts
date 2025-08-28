# Environment Variable Setup Guide

This guide explains how to configure and use environment variables in your GitHub App scripts using a `.env` file.

## Quick Setup

1. **Install dependencies:**
   ```bash
   pip install python-dotenv
   # or install all dependencies
   pip install -r requirements.txt
   ```

2. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` with your actual values:**
   ```bash
   nano .env  # or use your preferred editor
   ```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GITHUB_APP_PEM_FILE` | Path to your GitHub App's private key file | `od-oraf-test-app.2025-08-27.private-key.pem` |
| `GITHUB_APP_CLIENT_ID` | Your GitHub App's Client ID | `Iv23likDpjHD1hbh2mQW` |
| `GITHUB_APP_INSTALLATION_ID` | Your GitHub App's Installation ID | `69770355` |

### Optional Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GITHUB_TOKEN` | Personal access token (alternative to `gh auth token`) | `ghp_xxxxxxxxxxxx` |

## File Structure

```
PyCharmMiscProject/
├── .env                    # Your actual configuration (DO NOT COMMIT)
├── .env.example           # Template file (safe to commit)
├── requirements.txt       # Python dependencies
├── gen_app_token.py      # Updated to use .env
├── gh_script.py          # Updated to use .env
├── gh_repo_manager.py    # Updated to use .env
└── ENVIRONMENT_SETUP.md  # This guide
```

## How It Works

### Priority Order

The scripts follow this priority order for configuration:

1. **Command line arguments** (highest priority)
2. **Environment variables from .env file**
3. **Default hardcoded values** (fallback)

### Example Usage

```python
# In gen_app_token.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

# Get values with fallbacks
pem = os.getenv('GITHUB_APP_PEM_FILE', 'default-file.pem')
client_id = os.getenv('GITHUB_APP_CLIENT_ID', 'default-id')
installation_id = os.getenv('GITHUB_APP_INSTALLATION_ID', '12345')
```

## Updated Scripts

All Python scripts have been updated to use environment variables:

### `gen_app_token.py`
- Loads PEM file path, client ID, and installation ID from `.env`
- Command line arguments still override environment variables
- Generates JWT tokens using configured values

### `gh_script.py`
- Uses environment variables for GitHub App operations
- Manages installations and repositories

### `gh_repo_manager.py`
- Uses environment variables for repository management
- Handles collaborators and repository settings

## Security Best Practices

### ✅ Do This
- Keep `.env` file in your `.gitignore`
- Use `.env.example` for sharing configuration templates
- Set appropriate file permissions: `chmod 600 .env`
- Use different `.env` files for different environments

### ❌ Don't Do This
- Never commit `.env` files to version control
- Don't hardcode sensitive values in scripts
- Don't share `.env` files via email or chat

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'dotenv'**
   ```bash
   pip install python-dotenv
   ```

2. **Environment variables not loading**
   - Check that `.env` file exists in the same directory as your script
   - Verify file permissions and syntax
   - Ensure no spaces around the `=` sign

3. **File not found errors**
   - Check that file paths in `.env` are correct
   - Use absolute paths if relative paths don't work

### Debugging

Add this to your scripts to debug environment loading:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Debug: Print loaded values (remove in production)
print(f"PEM File: {os.getenv('GITHUB_APP_PEM_FILE')}")
print(f"Client ID: {os.getenv('GITHUB_APP_CLIENT_ID')}")
print(f"Installation ID: {os.getenv('GITHUB_APP_INSTALLATION_ID')}")
```

## Alternative: System Environment Variables

Instead of using a `.env` file, you can set system environment variables:

```bash
# In your shell profile (.bashrc, .zshrc, etc.)
export GITHUB_APP_PEM_FILE="od-oraf-test-app.2025-08-27.private-key.pem"
export GITHUB_APP_CLIENT_ID="Iv23likDpjHD1hbh2mQW"
export GITHUB_APP_INSTALLATION_ID="69770355"
```

## Integration with GitHub CLI

You can also use GitHub CLI for token management:

```bash
# Set GitHub token from gh CLI
export GITHUB_TOKEN=$(gh auth token)
```

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Copy and configure your `.env` file
3. Test your scripts: `python gen_app_token.py`
4. Add `.env` to your `.gitignore` if not already there

Your scripts are now configured to use environment variables for better security and flexibility!
