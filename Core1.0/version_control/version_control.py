"""
version_control Module
----------------------
Dedicated module for version control operations, including interactions with GitHub repositories.
Supports committing changes, pushing files, and cloning repositories.
"""

import subprocess
import logging
from pathlib import Path
from github import Github, GithubException
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clone_repository(repo_url: str, dest_dir: Path):
    """
    Clones a GitHub repository to a local directory.
    
    :param repo_url: URL of the GitHub repository to clone.
    :param dest_dir: Local directory path to clone the repository into.
    """
    try:
        subprocess.run(['git', 'clone', repo_url, str(dest_dir)], check=True)
        logging.info(f"Repository cloned: {repo_url} into {dest_dir}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to clone repository {repo_url}: {e}")

def push_files_to_repository(file_paths: List[Path], repo_name: str, commit_message: str, github_token: str):
    """
    Adds, commits, and pushes files to a GitHub repository.
    
    :param file_paths: List of file paths to add and commit.
    :param repo_name: Name of the GitHub repository (e.g., 'username/repo').
    :param commit_message: Commit message.
    :param github_token: GitHub token for authentication.
    """
    try:
        # Authentication
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        
        # File upload preparation (simplified example; consider using GitPython for comprehensive functionality)
        for file_path in file_paths:
            with open(file_path, 'r') as file:
                content = file.read()
                repo.create_file(str(file_path.relative_to(Path.cwd())), commit_message, content, branch="main")
        
        logging.info(f"Files pushed to repository: {repo_name}")
    except GithubException as e:
        logging.error(f"GitHub operation failed: {e}")

# Example usage
if __name__ == "__main__":
    github_token = "your_github_token_here"
    repo_name = "your_username/your_repo_name"
    file_paths = [Path("/path/to/your/file1.py"), Path("/path/to/your/file2.py")]
    commit_message = "Update files"
    
    push_files_to_repository(file_paths, repo_name, commit_message, github_token)
