#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty, StringProperty
import re


class RepodiggerApp(App):
    def build(self):
        return Manager(transition=FadeTransition())


class Manager(ScreenManager):
    login = ObjectProperty(None)
    issues = ObjectProperty(None)


class LoginScreen(Screen):
    text_input = StringProperty('')

    def get_input(self, text_input):
        if text_input != "":
            self.parse_input(text_input)

    def parse_input(self, text_input):
        if re.search(".[/].", text_input):
            self.parent.open_issues(text_input)
        else:
            print("not a valid repo!")


class IssueScreen(Screen):
    pass


if __name__ == '__main__':
    RepodiggerApp().run()