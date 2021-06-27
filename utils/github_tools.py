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


get_repo_stars(repo_name)
def get_repo_issues(repo_name):
	repo = g.get_repo(repo_name)
	# title = []
	count = 0
	# number = []
	for issue in repo.get_issues(state='open'):
		count += 1
		# title.append(issue.title)
		# number.append(issue.number)
	# return title , number
	return count 

def search_repo(name):
	repository = g.search_repositories(query=name)
	count = 0
	text = []
	for repo in repository:
		text.append(repo.full_name)
		count += 1
		if count == 10:
		    break
	return text   


def get_repo_list(name):
	repository = g.search_repositories(query='user:'+name)
	repo_list = []
	for repo in repository:
		user_name = (repo.full_name).split('/')[0]
		repo_list.append((repo.full_name).split('/')[1])

	with open('user_name.txt','w') as f:
		f.write(user_name)
	
	return repo_list

def search_user_repo(name):
	repository = g.search_repositories(query='user:'+name)
	repo_list = []
	for repo in repository:
		repo_list.append(repo.full_name)

	return repo_list

