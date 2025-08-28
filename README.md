# GitHub CLI Management Tools

A comprehensive collection of Python scripts and tools for managing GitHub repositories and GitHub Apps using the GitHub CLI and API.

## 🚀 Features

- **GitHub App Authentication**: Generate JWT tokens and access tokens for GitHub Apps
- **Repository Management**: List, create, clone, and manage repositories
- **Collaborator Management**: Add and manage repository collaborators
- **GitHub App Integration**: Manage GitHub App installations and repository access
- **Environment Configuration**: Secure configuration management with `.env` files
- **CLI Interface**: Easy-to-use command-line interface for GitHub operations

## 📁 Repository Structure

```
PyCharmMiscProject/
├── main.py                           # Main execution script
├── gen_app_token.py                  # GitHub App JWT and access token generation
├── gh_script.py                      # GitHub App repository management
├── gh_repo_manager.py                # Direct repository operations
├── script.py                         # Additional utility scripts
├── script.sh                         # Bash script for repository operations
├── .env                              # Environment variables (not in git)
├── .env.example                      # Environment template
├── requirements.txt                  # Python dependencies
├── ENVIRONMENT_SETUP.md              # Environment setup guide
├── IMPROVEMENT_TODO.md               # Future improvement roadmap
├── gh-cli-commands-reference.md      # GitHub CLI commands reference
└── github-cli-commands               # Raw CLI commands collection
```

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- [GitHub CLI](https://cli.github.com/) installed and authenticated
- GitHub App (if using App-based authentication)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd PyCharmMiscProject
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   nano .env
   ```

4. **Authenticate with GitHub CLI:**
   ```bash
   gh auth login
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# GitHub App Configuration
GITHUB_APP_PEM_FILE=your-app-private-key.pem
GITHUB_APP_CLIENT_ID=your_client_id
GITHUB_APP_INSTALLATION_ID=your_installation_id

# Optional: GitHub Personal Access Token
GITHUB_TOKEN=your_personal_access_token
```

See [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) for detailed configuration instructions.

## 🎯 Usage

### Quick Start

Run the main interface:
```bash
python main.py
```

### Individual Scripts

#### Generate GitHub App Token
```bash
python gen_app_token.py [pem_file] [client_id]
```

#### List Repositories
```bash
python gh_script.py
```

#### Repository Management
```bash
python gh_repo_manager.py
```

### GitHub CLI Commands

For direct CLI usage, see [gh-cli-commands-reference.md](gh-cli-commands-reference.md) for a comprehensive list of GitHub CLI commands.

## 📚 Core Components

### `main.py`
Main execution script that orchestrates GitHub operations and provides a unified interface.

### `gen_app_token.py`
- Generates JWT tokens for GitHub App authentication
- Creates installation access tokens
- Supports both environment variables and command-line arguments
- Uses RSA256 signing with private key files

### `gh_script.py`
- GitHub App installation management
- Repository listing and management through GitHub Apps
- Installation-based repository operations
- JSON pretty-printing for API responses

### `gh_repo_manager.py`
- Direct repository operations (create, clone, fork)
- Collaborator management
- Repository visibility settings
- Comprehensive repository information retrieval

### `script.sh`
- Bash-based repository management
- GitHub App installation operations
- Error handling and verification
- Colored output for better user experience

## 🔧 Key Features

### Authentication Methods
- **GitHub App**: JWT-based authentication with installation tokens
- **Personal Access Token**: Direct API access with personal tokens
- **GitHub CLI**: Leverages `gh` CLI authentication

### Repository Operations
- List repositories with detailed information
- Create public/private repositories
- Clone and fork repositories
- Manage repository collaborators
- Change repository visibility

### GitHub App Management
- List GitHub App installations
- Add repositories to installations
- Generate and manage access tokens
- Installation-based operations

## 📖 Documentation

- **[Environment Setup Guide](ENVIRONMENT_SETUP.md)**: Detailed setup instructions
- **[GitHub CLI Commands Reference](gh-cli-commands-reference.md)**: Complete CLI command reference
- **[Improvement Roadmap](IMPROVEMENT_TODO.md)**: Future enhancement plans

## 🔒 Security

- Environment variables stored in `.env` (excluded from git)
- Private keys and tokens never hardcoded
- Secure credential management practices
- GitHub App-based authentication for enhanced security

## 🚦 Error Handling

- Comprehensive error messages with suggested fixes
- HTTP status code handling
- JSON parsing error management
- GitHub API rate limit awareness

## 📋 Dependencies

```
PyJWT==2.8.0          # JWT token generation
cryptography==41.0.7   # Cryptographic operations
requests==2.31.0       # HTTP requests
python-dotenv==1.0.0   # Environment variable management
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 Future Improvements

See [IMPROVEMENT_TODO.md](IMPROVEMENT_TODO.md) for a comprehensive roadmap of planned enhancements including:

- Interactive CLI interface with argparse
- Async operations and rate limiting
- Enhanced error handling and validation
- Workflow automation
- Integration capabilities
- Visual improvements

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install dependencies with `pip install -r requirements.txt`
2. **Authentication errors**: Verify GitHub CLI authentication with `gh auth status`
3. **Environment variables not loading**: Check `.env` file exists and has correct syntax
4. **Permission errors**: Ensure GitHub App has necessary permissions for operations

### Debug Mode

Add debug output to scripts:
```python
import os
print(f"PEM File: {os.getenv('GITHUB_APP_PEM_FILE')}")
print(f"Client ID: {os.getenv('GITHUB_APP_CLIENT_ID')}")
```

## 📄 License

[Add your license information here]

## 📞 Support

- Create an issue for bug reports
- Check existing documentation before asking questions
- Follow the contribution guidelines for feature requests

---

**Note**: This project is designed to work with GitHub's API and CLI. Ensure you have proper permissions and authentication set up before using these tools in production environments.
