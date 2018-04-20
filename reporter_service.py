# -*- coding: utf-8 -*-
import datetime

from repository import Repository
from github import Github #pip install pygithub

#https://github.com/PyGithub/PyGithub
#http://pygithub.readthedocs.io/en/latest/introduction.html

class Report(object):
    name=""
    number_of_issues=None
    issues=None

class UserGithub(object):
    github_connection=None

    def __init__(self,user, password):
        self.github_connection=Github(user,password, per_page=10000)

    def get_repo_issues(self, repository):

        issues_days_ago ={}
        number_of_issues_days_ago ={}
        for i in range(1, 7):
            issues_day=self.github_connection.get_repo(repository.replace(" ", "")).get_issues(since=(datetime.datetime.now() - datetime.timedelta(days=i+1)))
            issues_days_ago[i] = [issue for issue in issues_day]
            number_of_issues_days_ago[i] = len(issues_days_ago[i])
            if i > 1:
                issues_days_ago[i]= set(issues_days_ago[i]) - set(issues_days_ago[i-1])
                number_of_issues_days_ago[i] = len(issues_days_ago[i])


        issues = self.github_connection.get_repo(repository.replace(" ", "")).get_issues(
            since=(datetime.datetime.now() - datetime.timedelta(days=7)))
        total_issues= [issue for issue in issues]
        return total_issues, issues_days_ago, number_of_issues_days_ago

class Issue(object):
    id = None
    state = None
    title = None
    repository = None
    created_at = None

    def __init__(self):
        self.id


class Reporter(object):
    list_of_repositories = []
    reports = []

    def __init__(self, repositories):
        list_of_repositories = repositories.split(',')
        if isinstance(list_of_repositories, (list,)):
            self.list_of_repositories = list_of_repositories

    def run(self):
        user = UserGithub("mirespace@gmail.com", "5de7de97")
        print "Logged"
        if len(self.list_of_repositories) > 0:
            print "Repositories: {number}".format(number=len(self.list_of_repositories))
            for repo_name in self.list_of_repositories:
                issues, issues_day, number_of_issues_per_day = user.get_repo_issues(repo_name)
                report={}
                report['repo']=repo_name
                report['issues']=issues
                report['issues_per_day'] = issues_day
                report['number_of_issues_per_day'] = number_of_issues_per_day
                report['size']=len(issues)
                self.reports.append(report)
                print repo_name
                print len(issues)
                print report['issues_per_day']
                print "<---------------------------->"
        else:
            pass

        if len(self.reports) > 0:
            pass
        else:
            pass

    pass
