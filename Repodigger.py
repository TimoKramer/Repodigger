#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty, ListProperty
from kivy.network.urlrequest import UrlRequest
import re


class RepodiggerApp(App):

    def build(self):
        root = Manager()
        global global_screen_manager
        global_screen_manager = root
        return root


class Manager(ScreenManager):
    login_screen = ObjectProperty(None)
    issue_screen = ObjectProperty(None)
    detail_screen = ObjectProperty(None)
    burndown_screen = ObjectProperty(None)


class DetailScreen(Screen):

    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)

    def populate_details(self):
        pass


class BurndownScreen(Screen):
    def __init__(self, **kwargs):
        super(BurndownScreen, self).__init__(**kwargs)


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
        global_screen_manager.current = 'Issue Screen'
        global_screen_manager.get_screen('Issue Screen').build_issue_widgets(results)

    def parse_failure(self, req, result):
        print('There was a problem: "', result['message'], '"')

    def parse_error(self, req, error):
        print('There was an error: ', error)


class IssueScreen(Screen):
    my_item_strings = ListProperty([])

    def __init__(self, **kwargs):
        kwargs['cols'] = 1
        super(IssueScreen, self).__init__(**kwargs)

    def build_issue_widgets(self, issues):
        for issue in issues:
            if issue['state'] == 'open':
                self.my_item_strings.append(issue['title'])
        self.issues_list.item_strings = self.my_item_strings
        self.issues_list.adapter.data.clear()
        self.issues_list.adapter.data.extend(self.my_item_strings)
        self.issues_list._trigger_reset_populate()

    def on_burndown_press(self):
        global_screen_manager.current = 'Burndown Screen'

    def on_change_press(self):
        global_screen_manager.current = 'Login Screen'

    def on_detail_press(self):
        global_screen_manager.current = 'Detail Screen'
        global_screen_manager.get_screen('Detail Screen').populate_details()


class IssueButton(ListItemButton):
    def on_detail_press(self):
        print(self.parent)
        print(self.parent.parent)
        print(self.parent.parent.parent)
        print(self.parent.parent.parent.parent)
        print(self.parent.parent.parent.parent.parent)
        self.parent.parent.parent.parent.parent.on_detail_press()


if __name__ == '__main__':
    RepodiggerApp().run()
