import os
import sys
import git
import yaml
import datetime
import argparse
from pathlib import Path

REPO_LIST_PATH = 'repo_list.yaml'


def store(directory):
    repos = load_repos()
    for repo_info in repos.values():
        repo_info['in_directory'] = False

    for subdir in os.listdir(directory):
        repo_dir = os.path.join(directory, subdir)
        if os.path.isdir(repo_dir) and os.path.exists(os.path.join(repo_dir, '.git')):
            if subdir not in repos:
                repos[subdir] = {
                    'last_pulled': None,
                    'last_updated': None,
                    'in_directory': True
                }
            else:
                repos[subdir]['in_directory'] = True

            repo = git.Repo(repo_dir)
            repos[subdir]['last_updated'] = repo.head.commit.committed_date

    save_repos(repos)


def update(directory):
    repos = load_repos()
    updated = False

    for repo_name, repo_info in repos.items():
        repo_dir = os.path.join(directory, repo_name)
        if repo_info['in_directory'] and os.path.exists(repo_dir):
            repo = git.Repo(repo_dir)

            if repo_info['last_pulled'] is None or repo_info['last_updated'] > repo_info['last_pulled']:
                pull(repo_name, repo, repos)
                updated = True

    if updated:
        save_repos(repos)


def pull_all(directory):
    repos = load_repos()

    for repo_name, repo_info in repos.items():
        repo_dir = os.path.join(directory, repo_name)
        if repo_info['in_directory'] and os.path.exists(repo_dir):
            repo = git.Repo(repo_dir)
            pull(repo_name, repo, repos)

    save_repos(repos)


def pull(repo_name, repo, repos):
    print(f'Pulling repo: {repo_name}')
    repo.remotes.origin.pull()
    repos[repo_name]['last_pulled'] = datetime.datetime.now().timestamp()


def load_repos():
    if not os.path.exists(REPO_LIST_PATH):
        return {}

    with open(REPO_LIST_PATH, 'r') as file:
        return yaml.safe_load(file)


def save_repos(repos):
    with open(REPO_LIST_PATH, 'w') as file:
        yaml.safe_dump(repos, file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage Git repositories')
    parser.add_argument('command', choices=['store', 'pull', 'update'], help='The command to execute')
    parser.add_argument('directory', help='The directory containing the repositories')
    args = parser.parse_args()

    directory = os.path.expanduser(args.directory)  # Converts '~/Repos' to '/home/user/Repos'

    commands = {
        'store': store,
        'pull': pull_all,
        'update': update
    }

    # Execute the selected command
    command_function = commands.get(args.command)
    command_function(directory)
