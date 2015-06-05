#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'

import requests, json


class GithubRequest():

    repo = 'timokramer/RepoDigger'

    def __init__(self, repo):

        self.repo = repo

        url = 'https://api.github.com/repos/' + repo + '/issues'

        self.response = requests.get(url)

    def print_to_console(self):

        print(json.dumps(self.response.json(), sort_keys=True, indent=4, separators=(',', ': ')))

    def return_json(self):

        return self.response.json()

    def return_string(self):

        return self.response.text()

    def return_structured_data(self):

        issues = json.loads(self.response.text)
        return issues


if __name__ == "__main__":
    req = GithubRequest('timokramer/PatFra')
    res = req.return_structured_data()
    for entry in res:
        print(entry)