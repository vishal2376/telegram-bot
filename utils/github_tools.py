from github import Github
import os
import json
import requests

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


def get_repo_list(user_name,flag=0):
	repo_list = []
	url = 'https://api.github.com/users/'+user_name+'/repos'
	r = requests.get(url)
	if r.status_code == 200:
		data = json.loads(r.text)
		if flag == 0:
			for repos in data:
				repo_list.append(repos['name'])
			with open('user_name.txt','w') as f:
				f.write(user_name)
		else:
			for repos in data:
				repo_list.append(repos['full_name'])			
	else:
		print(r.status_code)

	return repo_list