#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'


class Data:

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

    repo_string = ''
    issues = ''

    def foo(self):
        return id(self)

    def get_repo_string(self):
        return self.repo_string

    def set_repo_string(self, repo_string):
        print(repo_string)
        self.repo_string = repo_string

    def get_issues(self):
        return self.issues

    def set_issues(self, issues):
        print(issues)
        self.issues = issues


class Singleton(Data):
    def __init__(self):
        Data.__init__(self)


if __name__ == '__main__':
    x = Singleton()
    print(x)
    y = Singleton()
    print(y)
    x.set_repo_string('cinderella')
    y.set_repo_string('böse hexe')
    print(x.get_repo_string())
    print(y.get_repo_string())
