#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'


from kivy.network.urlrequest import UrlRequest
from kivy.properties import ListProperty


class Data:

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

    repo_string = ''
    issues = ''

    def get_repo_string(self):
        return self.repo_string

    def set_repo_string(self, repo_string):
        self.repo_string = repo_string
        print(type(self.repo_string))

    def get_issues(self):
        return self.issues

    def get_all_issues_as_list(self):
        issues = self.get_issues()
        all_issues_list = [issue['title'] for issue in issues]
        return all_issues_list

    def set_issues(self, issues):
        self.issues = issues

    def request_all_issues(self, rd, text_input):
        headers = {'User-Agent': 'timokramer/repodigger'}
        req = UrlRequest(
            'https://api.github.com/repos/' + text_input + '/issues?state=all',
            on_success=self.parse_request,
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

    def parse_request(self, req, results):
        parsed = True
        if parsed:
            self.set_issues(results)

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
