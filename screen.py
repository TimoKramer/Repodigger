#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder


Builder.load_file('screen.kv')

class RootWidget(FloatLayout):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()