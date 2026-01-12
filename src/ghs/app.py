import json
import subprocess
import sys
from pathlib import Path
from rich import print as pprint

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator

import cfg


def app(target_dir_path):
    """Main function orchestrating the workflow."""

    data = read_json(cfg.JSON_FILE)

    selected_repo_hrefs = display_and_select_repos(data)
    if not selected_repo_hrefs:
        pprint("No repos selected. Exiting.")
        return

    if not target_dir_path:
        target_dir_path = inquirer.filepath(
            message="Enter path to download:",
            default=cfg.HOME_PATH,
            validate=PathValidator(is_dir=True, message="Input is not a directory"),
            only_directories=True,
        ).execute()
        if not target_dir_path:
            pprint("Target directory cannot be empty. Exiting.")
            return

    ok_to_clone, conflicts = check_conflicts(selected_repo_hrefs, target_dir_path)
    if conflicts:
        pprint(f"\nsel repos already exist @ {target_dir_path}:")
        for repo in conflicts:
            pprint(f" - {repo}")
        response = input(f"\nskip {len(conflicts)} conflicting repos? (y/N): ")
        if response.lower() not in ("y", "yes"):
            pprint("Cloning cancelled by user.")
            return

    if ok_to_clone:
        pprint(f"\nProceeding to clone {len(ok_to_clone)} repos...")
        clone_repositories(ok_to_clone, target_dir_path)
    else:
        pprint("No repos left to clone after conflict check.")


def display_and_select_repos(data_dict):
    """
    Displays categories and repositories from the data dictionary,
    allowing the user to select repositories using InquirerPy's fuzzy search.
    Searches within both href and description.
    Returns a list of selected 'href' values (user/repo strings).
    """
    choices = []
    for list_name, details in data_dict.items():
        hrefs = details.get("href", [])
        descriptions = details.get("description", [])
        for href, desc in zip(hrefs, descriptions):
            choices.append(
                Choice(
                    href,  # Value returned when selected
                    name=f"[{list_name}] {href}",  # Text shown to the user and searched
                    instruction=desc,  # Text shown to the user and searched
                )
            )

    list_names = ["STAR LISTS: "]
    for i, (list_name, _) in enumerate(data_dict.items()):
        list_names.append(f"{list_name}")
    info = "sel: c-space | exact match: c-e | open gh url: c-o | sel/unsel all: c-a/c-r"
    pprint(list_names, info)

    repos = inquirer.fuzzy(
        message="STAR LISTS ",
        choices=choices,
        multiselect=True,
        match_exact=True,
        exact_symbol=" E",
        keybindings=cfg.kbs if hasattr(cfg, "kbs") else None,
        style=cfg.style if hasattr(cfg, "style") else None,
        wrap_lines=True,
        height=100,
        border=True,
    ).execute()

    if repos is None:
        sys.exit(0)
    return repos


def read_json(file_path):
    """Loads data from the specified JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        pprint(f"Error: JSON file '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        pprint(f"Error: Invalid JSON format in '{file_path}': {e}")
        sys.exit(1)


def get_existing_git_repos(target_dir_path):
    """Finds subdirectories within target_dir_path that contain a .git folder."""
    existing_repos = set()
    target_path = Path(target_dir_path)
    for item in target_path.iterdir():
        if item.is_dir() and (item / ".git").is_dir():
            existing_repos.add(item.name)
    return existing_repos


def check_conflicts(selected_repo_hrefs, target_dir_path):
    """
    Checks if any of the selected repos already exist in the target directory.
    """
    existing_repos = get_existing_git_repos(target_dir_path)

    ok_to_clone = []
    conflicts = []

    for repo_href in selected_repo_hrefs:
        # repo_name: 'user/repo_name'
        repo_name = repo_href.split("/")[-1]

        if repo_name in existing_repos:
            conflicts.append(repo_href)
        else:
            ok_to_clone.append(repo_href)

    return ok_to_clone, conflicts


def clone_repositories(repo_hrefs, target_dir_path):
    """Clones the given list of repos into the target directory."""
    target_path = Path(target_dir_path)
    target_path.mkdir(parents=True, exist_ok=True)

    success_count = 0
    for repo_href in repo_hrefs:
        repo_url = f"https://github.com/{repo_href}.git"
        dest_path = (
            target_path / repo_href.split("/")[-1]
        )  # Use repo name part as directory name

        pprint(f"git clone {repo_url} {(dest_path)}")
        try:
            _ = subprocess.run(
                ["git", "clone", repo_url, str(dest_path)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            pprint(f"Successfully cloned {repo_href}.")
            success_count += 1
        except subprocess.CalledProcessError as e:
            pprint(f"Error cloning {repo_href}: {e.stderr.strip()}")
            break
        except FileNotFoundError:
            pprint("Error: 'git' command not found.")
            break
    pprint(f"\nCloned {success_count}/{len(repo_hrefs)} repos.")


if __name__ == "__main__":
    app()
