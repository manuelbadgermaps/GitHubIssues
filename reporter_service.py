# -*- coding: utf-8 -*-
import datetime
import operator

from github import Github  

DAYS_AGO = 7

class UserGithub(object):
    github_connection = None

    def __init__(self, user, password):
        self.github_connection = Github(user, password, per_page=1000)

    def get_repo_issues(self, repository):
        seven_days_ago = (datetime.datetime.today() - datetime.timedelta(days=DAYS_AGO)).replace(hour=0, minute=0,
                                                                                                 second=0,
                                                                                                 microsecond=0)
        return self.github_connection.get_repo(repository).get_issues(sort='created', direction='asc',
                                                                      since=seven_days_ago)


class Issue(object):
    id = None
    state = None
    title = None
    repository = None
    created_at = None

    def __init__(self, id, state, title, repository, created_at):
        self.id = id
        self.state = state
        self.title = title
        self.repository = repository
        self.created_at = created_at

    def json_print_issue(self):
        json = '"id":{id},"state":{state},"title":{title},"repository":{repository},"created_at":{created_at}'.format(
            id=self.id, state=self.state, title=self.title, repository=self.repository, created_at=self.created_at)
        return '{' + json + '}'


class Reporter(object):
    list_of_repositories = []

    def __init__(self, repositories):
        list_of_repositories = repositories.split(',')
        if isinstance(list_of_repositories, (list,)):
            self.list_of_repositories = list_of_repositories

    def run(self,username,password):
        user = UserGithub(username, password) 
        if len(self.list_of_repositories) > 0:
            self.list_of_issues = {}
            for repo_name in self.list_of_repositories:
                try:
                    issues = user.get_repo_issues(repo_name)
                    for issue_to_handle in issues:
                        issue = self.convert_to_report_issue(issue_to_handle, repo_name)
                        self.add_issue_to_list(issue)
                except:
                    None

            sorted_list = sorted(self.list_of_issues.items(), key=operator.itemgetter(0))
            sorted_list = self.reduce_list(sorted_list)
            top_day, issues_per_repo = self.extract_top_day_details(sorted_list)
            return self.create_json_report(top_day, issues_per_repo, sorted_list)

        else:
            print "No valid repositories found"

        print "No valid issues found"

    @staticmethod
    def reduce_list(list):  #It seems there is a bug in pygithub when filtering by date
        copy = []
        for (key, value) in list:
            if key > (datetime.datetime.today() - datetime.timedelta(days=7)):
                copy.append((key, value))
        return copy

    @staticmethod
    def convert_to_report_issue(issue, repo):
        return Issue(issue.id, issue.state, issue.title, repo, issue.created_at)

    def add_issue_to_list(self, issue):
        timestamp = self.convert_to_timestamp(issue.created_at)
        if timestamp in self.list_of_issues:
            self.list_of_issues[timestamp].append(issue)
        else:
            self.list_of_issues[timestamp] = (issue,)

    @staticmethod
    def convert_to_timestamp(datetime):
        return datetime.strptime(str(datetime), '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def extract_top_day_details(sorted_list):
        max_day = DAYS_AGO
        current_day = DAYS_AGO
        beginning_index = 0
        ending_index = 0
        current_index = -1
        current_period_beginning = 0
        number_of_issues_max = 0
        number_of_issues = 0
        days_ago = (datetime.datetime.today() - datetime.timedelta(days=max_day)).replace(hour=0, minute=0, second=0,
                                                                                          microsecond=0)
        next_day_ago = days_ago + datetime.timedelta(days=1)
        for i in sorted_list:
            if days_ago < i[0]:
                number_of_issues += len(i[1])
                current_index += 1
                if i[0] > next_day_ago:
                    if number_of_issues - len(i[1]) > number_of_issues_max:
                        number_of_issues_max = number_of_issues
                        max_day = current_day
                        ending_index = current_index
                        beginning_index = current_period_beginning
                    current_period_beginning = current_index + 1
                    current_day -= 1
                    days_ago = next_day_ago
                    next_day_ago = days_ago + datetime.timedelta(days=1)
                    number_of_issues = len(i[1])
        final_list = sorted_list[ending_index] if beginning_index == ending_index else sorted_list[
                                                                                       beginning_index:ending_index]
        return max_day, final_list

    @staticmethod
    def create_json_report(top_day, issues_per_repo, issues):
        json_issues, json_occurences = Reporter.get_json_issues_and_ocurrences(issues)

        special_day = datetime.datetime.today() - datetime.timedelta(days=top_day)
        return '{issues:[' + json_issues + '],"top_day":{"day":"' + datetime.datetime.strftime(special_day,
                                                        '%Y-%m-%d') + '","ocurrences":{' + json_occurences + '}}}'

    @staticmethod
    def get_json_issues_and_ocurrences(issues):
        json_issues = ""
        json_ocurrences = ""
        ocurrences = {}
        for issue in issues:
            for item in issue[1]:
                temp_json_issue = '"id":{id},"state":"{state}","title":"{title}","repository":"{repository}",' \
                                  '"created_at":"{created_at}"'.format(id=item.id, state=item.state,
                                                                       title=item.title.encode('utf8'),
                                                                       repository=item.repository,
                                                                       created_at=datetime.datetime.strftime(issue[0],
                                                                                                "%Y-%m-%dT%H:%M:%SZ"))
                json_issues += '{' + temp_json_issue + '}' + ','
                if item.repository in ocurrences:
                    ocurrences[item.repository] += 1
                else:
                    ocurrences[item.repository] = 1

        for item in ocurrences:
            json_ocurrences += '"' + item + '": ' + str(ocurrences[item]) + ','

        json_issues = Reporter.remove_last_comma(json_issues)
        json_ocurrences = Reporter.remove_last_comma(json_ocurrences)

        return json_issues, json_ocurrences

    @staticmethod
    def remove_last_comma(json_issues):
        temp = len(json_issues)
        json_issues = json_issues[:temp - 1]
        return json_issues
