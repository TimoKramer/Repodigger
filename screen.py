#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'

import kivy, data
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

kivy.require('1.0.6')


class MainScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Dummy'))
        issues = data.GithubRequest('timokramer/repodigger').return_structured_data()
        self.raw_json = Label(text=issues[0])
        self.add_widget(self.raw_json)


class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.size_hint = (0.5, 0.5)
        self.cols = 2
        self.add_widget(Label(text='Insert Repo'))
        self.add_widget(TextInput(text='e.g. "timokramer/repodigger"'))
        self.add_widget(Button(text='OK'))


class Screen(AnchorLayout):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.add_widget(LoginScreen())


class MainApp(App):
    def build(self):
        return Screen()

if __name__ == '__main__':
    MainApp().run()
