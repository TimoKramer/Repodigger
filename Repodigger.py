#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty, ListProperty
from kivy.network.urlrequest import UrlRequest
from kivy.graphics import *
import re, json, Data


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


class BurndownScreen(Screen):
    def __init__(self, **kwargs):
        super(BurndownScreen, self).__init__(**kwargs)

    def on_back_press(self):
        self.parent.current = 'Issue Screen'

    def draw_burndown(self):
        self.request_milestones()
        with self.canvas:
            Line(points=[100, 100, 200, 100, 100, 200], width=1.0)

    def request_milestones(self):
        pass


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
        Data.DataSingleton().request_all_issues(self, text_input)

    def request_success(self):
        self.parent.current = 'Issue Screen'
        self.parent.get_screen('Issue Screen').build_issue_widgets()
        # global_screen_manager.current = 'Issue Screen'
        # global_screen_manager.get_screen('Issue Screen').build_issue_widgets()


class IssueScreen(Screen):
    issues_archive = ListProperty(None)

    def __init__(self, **kwargs):
        kwargs['cols'] = 1
        super(IssueScreen, self).__init__(**kwargs)

    def build_issue_widgets(self):
        issues = Data.DataSingleton().get_issues()
        print(issues)
        self.issues_archive = [issue['title'] for issue in issues]
        self.issues_list.adapter.data.clear()
        self.issues_list.adapter.data.extend(self.issues_archive)
        self.issues_list._trigger_reset_populate()

    def on_burndown_press(self):
        self.parent.current = 'Burndown Screen'
        self.parent.get_screen('Burndown Screen').draw_burndown()

    def on_change_press(self):
        self.parent.current = 'Login Screen'

    def on_detail_press(self):
        self.parent.current = 'Detail Screen'
        self.parent.get_screen('Detail Screen').populate_details()


class IssueButton(ListItemButton):
    def on_detail_press(self):
        print(self.parent)
        print(self.parent.parent)
        print(self.parent.parent.parent)
        print(self.parent.parent.parent.parent)
        print(self.parent.parent.parent.parent.parent)
        self.parent.parent.parent.parent.parent.on_detail_press()


class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)

    def populate_details(self):
        pass

    def on_back_press(self):
        print("back")
        self.parent.current = 'Issue Screen'


if __name__ == '__main__':
    RepodiggerApp().run()
