from github import Github
from git import Repo
import shutil
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

def github_clone(repo_name='vishal2376/telegram-bot'):
    git_url = "https://github.com/" + repo_name
    repo_path = 'github/git_clones/'+ repo_name
    zip_path = 'github/git_clones/'+ repo_name + '.zip'

    if os.path.exists('github/git_clones'):
        shutil.rmtree('github/git_clones')

    repo = Repo.clone_from(git_url,repo_path)
    
    with open(zip_path,'wb') as zipfile:
        repo.archive(zipfile,format='zip')

    shutil.rmtree(repo_path)

    return zip_path

def get_repo_list(name):
	repository = g.search_repositories(query='user:'+name)
	repo_list = []
	for repo in repository:
		user_name = (repo.full_name).split('/')[0]
		repo_list.append((repo.full_name).split('/')[1])

	with open('github/user_name.txt','w') as f:
		f.write(user_name)
	
	return repo_list