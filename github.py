#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'

import requests, json


class GithubRequest():

    repo = 'timokramer/PatFra'
    response = None

    def __init__(self, repo):

        self.repo = repo

        url = 'https://api.github.com/repos/' + repo + '/issues'

        self.response = requests.get(url)

    def print_to_console(self):

        print(json.dumps(self.response.json(), sort_keys=True, indent=4, separators=(',', ': ')))

    def return_json(self):

        return self.response.json()


if __name__ == "__main__":
    req = GithubRequest('timokramer/PatFra')
    req.print_to_console()
    #print(json.dumps(req.return_json(), sort_keys=True, indent=4, separators=(',', ': ')))