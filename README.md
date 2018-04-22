# GitHubIssues
Explore repos, find issues from last week and return description of worst day.

Requirements:

- Pygithub: 
Install:
pip install pygithub
https://github.com/PyGithub/PyGithub
http://pygithub.readthedocs.io/en/latest/introduction.html

Usage: python reporter.py list_of_repositories

list_of_repositories format : owner/repo,owner/repo...


Technical debs:

- github user/password not hardcoded inside. It is needed to define a external setting files not added to the repo.
- refactor extract_top_day_details method
