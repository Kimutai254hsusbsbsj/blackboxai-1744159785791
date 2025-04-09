import os
import re
from git import Repo
from git.exc import GitError
from typing import Optional
import requests
from bs4 import BeautifulSoup

def is_valid_git_url(url: str) -> bool:
    """Check if URL is a valid git repository URL"""
    patterns = [
        r'^https?://github\.com/.*\.git$',
        r'^https?://gitlab\.com/.*\.git$',
        r'^https?://bitbucket\.org/.*\.git$'
    ]
    return any(re.match(pattern, url) for pattern in patterns)

def clone_website(url: str, target_dir: str = '.') -> Optional[str]:
    """Clone website content from URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        website_name = url.split('//')[-1].split('/')[0].replace('.', '_')
        output_path = os.path.join(target_dir, website_name)
        
        os.makedirs(output_path, exist_ok=True)
        
        with open(os.path.join(output_path, 'index.html'), 'w') as f:
            f.write(response.text)
            
        return output_path
    except Exception as e:
        print(f"Error cloning website: {e}")
        return None

def clone_repository(repo_url: str, target_dir: str = '.') -> Optional[str]:
    """Clone either a git repository or website based on input"""
    if is_valid_git_url(repo_url):
        try:
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            elif os.listdir(target_dir):
                return None

            repo_name = repo_url.split('/')[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]

            full_path = os.path.join(target_dir, repo_name)
            
            if os.path.exists(full_path):
                return None

            print(f"Cloning repository: {repo_url}")
            Repo.clone_from(repo_url, full_path)
            return full_path
        except GitError as e:
            print(f"Git error: {e}")
        except Exception as e:
            print(f"Error cloning repository: {e}")
        return None
    else:
        return clone_website(repo_url, target_dir)
