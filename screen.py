#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'

import kivy, github, json
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

kivy.require('1.0.6')


class MainScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Dummy'))
        issues = github.GithubRequest('timokramer/PatFra').return_json()
        self.raw_json = Label(text='issues')
        self.add_widget(self.raw_json)

class MyApp(App):

    def build(self):
        return MainScreen()

if __name__ == '__main__':
    MyApp().run()