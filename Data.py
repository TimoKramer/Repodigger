#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'


from kivy.network.urlrequest import UrlRequest
import json, datetime

class Data:

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

    _repo_string = ''
    _issues = ''
    _milestones = ''

    def get_repo_string(self):
        return self._repo_string

    def set_repo_string(self, repo_string):
        self._repo_string = repo_string

    def get_issues(self):
        return self._issues

    def set_issues(self, issues):
        self._issues = issues

    def get_all_issues_as_list(self):
        all_issues_list = [issue['title'] for issue in self._issues]
        return all_issues_list

    def get_open_issues_as_list(self):
        open_issues_list = []
        for issue in self._issues:
            if issue['state'] == 'open':
                open_issues_list.append(issue['title'])
        return open_issues_list

    def get_closed_issues_as_list(self):
        closed_issues_list = []
        for issue in self.get_issues():
            if issue['state'] == 'closed':
                closed_issues_list.append(issue['title'])
        return closed_issues_list

    def get_issues_with_delta(self, title, created):
        closed_issues = []
        for issue in self.get_issues():
            # TODO: Issues die keine Milestones haben
            if issue['milestone']['title'] == title:
                new_issue = {}
                new_issue['title'] = issue['title']
                if issue['closed_at'] is not None:
                    new_issue['state'] = 'closed'
                    closed_at = datetime.datetime.strptime(issue['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
                    timedelta = closed_at - created
                    new_issue['timedelta'] = abs(timedelta).days
                else:
                    new_issue['state'] = 'open'
                    new_issue['timedelta'] = None
                closed_issues.append(new_issue)
        return closed_issues

    def set_milestones(self, milestones):
        self._milestones = milestones

    def get_milestones(self):
        return self._milestones

    def get_open_milestones(self):
        milestones_list = []
        for milestone in self.get_milestones():
            if milestone['state'] == 'open':
                milestones_list.append(milestone)
        return milestones_list

    def get_milestone_data(self):
        milestone_data = []
        # TODO: What time's best? What time uses Github?
        for milestone in self.get_open_milestones():
            new_milestone = {'title': milestone['title']}
            new_milestone['created_at'] =  datetime.datetime.strptime(milestone['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            if milestone['due_on'] == None:
                new_milestone['due_on'] = datetime.datetime.now()
                new_milestone['has_due_date'] = 'True'
            else:
                new_milestone['due_on'] = datetime.datetime.strptime(milestone['due_on'], "%Y-%m-%dT%H:%M:%SZ")
                new_milestone['has_due_date'] = False
            # timedelta
            diff = new_milestone['due_on'] - new_milestone['created_at']
            new_milestone['timedelta'] = diff.days
            new_milestone['total_issues'] = milestone['open_issues'] + milestone['closed_issues']
            new_milestone['open_issues'] = milestone['open_issues']
            new_milestone['issue_closings'] = self.get_issues_with_delta(milestone['title'], new_milestone['created_at'])
            # append extracted milestone-data as dict to list
            milestone_data.append(new_milestone)
        return milestone_data

    def request_all_issues(self, rd, text_input):
        headers = {'User-Agent': 'timokramer/repodigger'}
        req = UrlRequest(
            'https://api.github.com/repos/' + text_input + '/issues?state=all',
            on_success=self.parse_issues_request,
            on_failure=self.parse_failure,
            on_error=self.parse_error,
            req_headers=headers,
            debug=True
        )
        req.wait()
        if req.is_finished:
            print("Request Finished")
            self.set_repo_string(text_input)
            rd.request_success()
            #print(json.dumps(req.result, sort_keys=True, indent=4, separators=(',', ': ')))

    def parse_issues_request(self, req, results):
        parsed = True
        if parsed:
            self.set_issues(results)

    def request_all_milestones(self):
        headers = {'User-Agent': 'timokramer/repodigger'}
        url = 'https://api.github.com/repos/' + self.get_repo_string() + '/milestones?state=all'
        req = UrlRequest(
            url,
            on_success=self.parse_milestones_request,
            on_failure=self.parse_failure,
            on_error=self.parse_error,
            req_headers=headers,
            debug=True
        )
        req.wait()
        if req.is_finished:
            print("Request Finished")
            #print(json.dumps(req.result, sort_keys=True, indent=4, separators=(',', ': ')))

    def parse_milestones_request(self, req, result):
        parsed = True
        if parsed:
            self.set_milestones(result)
            self.get_milestone_data()

    def parse_failure(self, req, result):
        print('There was a problem: "', result['message'], '"')

    def parse_error(self, req, error):
        print('There was an error: ', error)



class DataSingleton(Data):
    def __init__(self):
        Data.__init__(self)


if __name__ == '__main__':
    x = DataSingleton()
    print(x)
    y = DataSingleton()
    print(y)
    x.set_repo_string('cinderella')
    y.set_repo_string('böse hexe')
    print(x.get_repo_string())
    print(y.get_repo_string())
