from github import Github
import os

TOKEN = os.getenv('GITHUB_TOKEN')

g = Github(TOKEN)

# testing data
'''
user_keyword = 'vishal2376'
repo_keyword = 'virtual-assistant'

repo_name = user_keyword + '/' + repo_keyword
'''

def get_repo_stars(repo_name):
	repo = g.get_repo(repo_name)
	text = repo.stargazers_count
	return text

def get_repo_filename(repo_name):
	repo = g.get_repo(repo_name)
	text = []
	for content_file in repo.get_contents(""):
		text.append(content_file.path)
	return text

def get_repo_issues(repo_name):
	repo = g.get_repo(repo_name)
	title = []
	number = []
	for issue in repo.get_issues(state='open'):
		title.append(issue.title)
		number.append(issue.number)
	return title , number


def search_repo_by_language(programming_language='python'):
	language = 'language:' + programming_language
	repository = g.search_repositories(query=language)
	count = 0
	text = []
	for repo in repository:
		text.append(repo.full_name)
		count += 1
		if count == 10:
			break;
	return text	


def search_repo(name='hello world'):
	repository = g.search_repositories(query=name)
	count = 0
	text = []
	for repo in repository:
		text.append(repo.full_name)
		count += 1
		if count == 10:
			break;		
	return text	

def search_repo_by_issue(issue_tag='good-first-issue:>3'):
	repository = g.search_repositories(query=issue_tag)
	text = []
	count = 0
	for repo in repository:
		text.append(repo.full_name)
		count += 1
		if count == 10:
			break;		
	return text