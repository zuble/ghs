import json
import os
import os.path as osp
import time

import click
import requests
from bs4 import BeautifulSoup
from rich import print as pprint

from ghs.app import app
from ghs.cfg import cfg
from ghs.utils import read_json


def get_repos_from_list(username, list_name):
  page = 1
  full_url = f'https://github.com/stars/{username}/lists/{list_name}'
  list_repo_info = {
    'href': [],
    'description': [],
  }
  has_next_page = True

  while has_next_page:
    try:
      params = {'page': page}
      response = requests.get(full_url, headers=cfg.HEADERS, params=params)
      if response.status_code != 200:
        pprint(f'Failed to fetch page {page}. Status code: {response.status_code}')
        break

      soup = BeautifulSoup(response.text, 'html.parser')
      repos_div = soup.find('div', {'id': 'user-list-repositories'})

      if not repos_div:
        has_next_page = False
        break

      repo_items = repos_div.find_all(
        'div', class_='col-12 d-block width-full py-4 border-bottom color-border-muted'
      )
      # repo_items = repos_div.find_all("div", recursive=False)

      if not repo_items:
        has_next_page = False
        break

      for div in repo_items:
        title_section = div.find('div', class_='d-inline-block mb-1')
        if title_section:
          h2_tag = title_section.find('h2', class_='h3')
          if h2_tag:
            link_tag = h2_tag.find('a')
            if link_tag and link_tag.get('href'):
              repo_href = link_tag['href'][1:]
              list_repo_info['href'].append(repo_href)

              desc_p = div.find('p', class_='d-inline-block col-9 color-fg-muted pr-4')
              description = (
                desc_p.text.strip() if desc_p else 'No description available'
              )
              list_repo_info['description'].append(description)

      pagination = soup.find('div', class_='pagination')
      if pagination:
        next_button = pagination.find('a', class_='next_page')
        if not next_button or 'disabled' in next_button.get('class', []):
          has_next_page = False
      else:
        has_next_page = False

      page += 1
      time.sleep(1)

    except requests.RequestException as e:
      pprint(f'Error fetching page {page}: {e}')
      has_next_page = False

  return list_repo_info


# def get_repo_readme(repo_name):
# 	"""
# 	Fetch the README file content of a given repository (/{owner}/{repo}).
# 	"""
# 	url = f"{GH_API_URL}/repos{repo_name}/readme"
# 	headers = {
# 		"Accept": "application/vnd.github.v3.raw",
# 		"Authorization": f"token {GH_TOKEN}",
# 	}
# 	response = requests.get(url, headers=headers)

# 	if response.status_code == 200:
# 		return response.text
# 	else:
# 		pprint(f"Failed to fetch README for {repo_name}. Status code: {response.status_code}")
# 		return None


def get_star_lists_href(username):
  list_stars_name = []
  try:
    response = requests.get(
      f'https://github.com/{username}?tab=stars', headers=cfg.HEADERS
    )
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      list_links = soup.find_all(
        'a', href=lambda x: x and f'/stars/{username}/lists/' in x
      )
      # pprint(list_links)
      for link in list_links:
        list_name = link['href'].replace(f'/stars/{username}/lists/', '')
        list_stars_name.append(list_name)
        pprint(f'\nList: {list_name=}')
        pprint('-' * 50)

  except requests.RequestException as e:
    pprint(f'Error fetching lists: {e}')

  return list_stars_name


def jsonify_star_lists(username):
  list_stars_name = get_star_lists_href(username)

  list_stars_data = {}
  for list_name in list_stars_name:
    pprint(list_name)
    list_repo_info = get_repos_from_list(username, list_name)

    if list_repo_info:
      pprint(list_repo_info)
      list_stars_data[list_name] = list_repo_info
    else:
      pprint('No repositories found in this list')

  with open(cfg.JSON_FILE, 'w') as outfile:
    json.dump(list_stars_data, outfile, indent=4, sort_keys=False)

  # pd.DataFrame(repos).to_json(f"{GH_UNAME}_stars.json", orient='records', lines=True)
  # pd.DataFrame(repos).to_parquet(f  "{GH_UNAME}_stars.parquet")
  # a = pd.read_parquet("{cfg.GH_UNAME}stars.parquet", columns=['href'])
  # pprint(a)


@click.command()
@click.option(
  '-u', '--update', is_flag=True, default=False, help='overwrites json file'
)
@click.option(
  '-c', '--cwd', is_flag=True, default=False, help='sets download path to cwd'
)
@click.option('-l', '--log', is_flag=True, default=False, help='prints json and exits')
def main(update, cwd, log):
  if log:
    pprint(read_json(cfg.JSON_FILE))
    return

  target_dir_path = None
  if cwd:
    target_dir_path = os.getcwd()

  if not osp.exists(cfg.JSON_FILE) or update:
    jsonify_star_lists(cfg.GH_UNAME)

  app(target_dir_path)


if __name__ == '__main__':
  main()

  # def get_starred_repos(username):
  # 	url = f"https://api.github.com/users/{username}/starred"
  # 	response = requests.get(url)
  # 	if response.status_code == 200:
  # 		return response.json()
  # 	return None
  # repos = get_starred_repos(f"{GH_UNAME}")
  # for repo in repos:
  # 	print(f"Repository: {repo['full_name']}")
  # 	print(f"Description: {repo['description']}")
  # 	print(f"Stars: {repo['stargazers_count']}")
  # 	print("---")
