"""
repo_manage.py

A script for managing a set of Git repositories. It provides three commands:

    store: Initial setup, generates a list of repositories in a specified directory.
    pull: Pulls updates for all repositories in the list that are found in the directory.
    update: Updates local repositories if there are new commits.

Usage:

    python repo_manage.py store [directory]
    python repo_manage.py pull [directory]
    python repo_manage.py update [directory]

"""
import os
import git
import yaml
import datetime
import argparse
from pathlib import Path

REPO_LIST_PATH = 'repo_list.yaml'
DEFAULT_DIRECTORY = "~/Repos"

def get_repo(directory: str, repo_name: str) -> git.Repo:
    """
    Get a git.Repo object for the repo_name if it exists in the directory.
    Returns None if the repo does not exist.
    """
    repo_dir = os.path.join(directory, repo_name)
    if os.path.exists(repo_dir):
        try:
            return git.Repo(repo_dir)
        except git.InvalidGitRepositoryError:
            print(f"Warning: {repo_dir} is not a valid git repository.")
    return None

def store(directory: str) -> None:
    """
    Initializes or updates the list of repositories in the specified directory.
    New repositories are added to repos.yaml, existing entries are updated.
    """
    repos = load_repos()
    for repo_info in repos.values():
        repo_info['in_directory'] = False

    for subdir in os.listdir(directory):
        repo = get_repo(directory, subdir)
        if repo:
            if subdir not in repos:
                repos[subdir] = {
                    'last_pulled': None,
                    'last_updated': None,
                    'in_directory': True
                }
            else:
                repos[subdir]['in_directory'] = True

            repos[subdir]['last_updated'] = repo.head.commit.committed_date

    save_repos(repos)


def update(directory: str) -> None:
    """
    Updates repositories if there are new commits.
    Only updates repositories found in the directory.
    """
    repos = load_repos()
    updated = False

    for repo_name, repo_info in repos.items():
        repo = get_repo(directory, repo_name)
        if repo and repo_info['in_directory']:
            if repo_info['last_pulled'] is None or repo_info['last_updated'] > repo_info['last_pulled']:
                pull_repo(repo_name, repo, repos)
                updated = True

    if updated:
        save_repos(repos)


def pull(directory: str) -> None:
    """
    Pulls all repositories found in the directory.
    """
    repos = load_repos()

    for repo_name, repo_info in repos.items():
        repo = get_repo(directory, repo_name)
        if repo and repo_info['in_directory']:
            pull_repo(repo_name, repo, repos)

    save_repos(repos)


def pull_repo(repo_name: str, repo: git.Repo, repos: dict) -> None:
    """
    Pulls a specific repository and updates the last_pulled time.
    """
    print(f'Pulling repo: {repo_name}')
    try:
        repo.remotes.origin.pull()
        repos[repo_name]['last_pulled'] = datetime.datetime.now().timestamp()
    except Exception as e:
        print(f"Warning: Failed to pull {repo_name}. Error: {e}")


def load_repos():
    """
    Loads the list of repositories from repos.yaml.
    If the file does not exist, returns an empty dictionary.
    """
    if not os.path.exists(REPO_LIST_PATH):
        return {}

    with open(REPO_LIST_PATH, 'r') as file:
        return yaml.safe_load(file)


def save_repos(repos):
    """
    Saves the list of repositories to repos.yaml.
    """
    with open(REPO_LIST_PATH, 'w') as file:
        yaml.safe_dump(repos, file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage Git repositories')
    parser.add_argument('command', choices=['store', 'pull', 'update'], help='The command to execute')
    parser.add_argument('directory', nargs='?', default=DEFAULT_DIRECTORY, help='The directory containing the repositories')
    args = parser.parse_args()

    directory = os.path.expanduser(args.directory)  # Converts '~/Repos' to '/home/user/Repos'

    commands = {
        'store': store,
        'pull': pull,
        'update': update
    }

    # Execute the selected command
    command_function = commands.get(args.command)
    command_function(directory)