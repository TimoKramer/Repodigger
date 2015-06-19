#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.selectableview import SelectableView
from kivy.properties import ObjectProperty, ListProperty
from kivy.network.urlrequest import UrlRequest
from kivy.adapters.dictadapter import DictAdapter
from kivy.factory import Factory
import re

Factory.register('SelectableView', cls=SelectableView)
Factory.register('ListItemButton', cls=ListItemButton)


class RepodiggerApp(App):
    def build(self):
        return Manager()


class Manager(ScreenManager):
    login_screen = ObjectProperty(None)
    issue_screen = ObjectProperty(None)


class LoginScreen(Screen):
    def get_input(self, text_input):
        if text_input != "":
            self.parse_input(text_input)

    def parse_input(self, text_input):
        if re.search(".[/].", text_input):
            self.make_request(text_input)
        else:
            print("not a valid repo!")

    def make_request(self, text_input):
        headers = {'User-Agent': 'timokramer/repodigger'}
        req = UrlRequest(
            'https://api.github.com/repos/' + text_input + '/issues',
            on_success=self.parse_request,
            on_failure=self.parse_failure,
            on_error=self.parse_error,
            req_headers=headers,
            debug=True
        )
        req.wait()
        if req.is_finished:
            print("Request Finished")

    def parse_request(self, req, results):
        print('Succeeded requesting Github Issues')
        self.parent.current = 'Issue Screen'
        self.parent.get_screen('Issue Screen')

    def parse_failure(self, req, result):
        print('There was a problem: "', result['message'], '"')

    def parse_error(self, req, error):
        print('There was an error: ', error)


class IssueScreen(Screen):
    item_strings = ListProperty(None)
    issues = ListProperty(None)

    def __init__(self, **kwargs):
        kwargs['cols'] = 1
        super(IssueScreen, self).__init__(**kwargs)
        print("Erfolg!")
        list_item_args_converter = lambda row_index, rec: {'title': rec['title'],
                                                           'is_selected': rec['is_selected'],
                                                           'size_hint_y': None,
                                                           'height': 25}
        dict_adapter = DictAdapter(sorted_keys=[str(i) for i in self.issues],
                                   data=self.issues,
                                   args_converter=list_item_args_converter,
                                   template='CustomListItem')
        list_view = ListView(item_strings=[str(issues) for issues in self.item_strings])
        print(item for item in self.item_strings)

        self.add_widget(list_view)

    def build_issue_widgets(self, issues):
        self.issues = issues
        for issue in issues:
            #print(issue['title'])
            self.item_strings.append(issue['title'])


if __name__ == '__main__':
    RepodiggerApp().run()
