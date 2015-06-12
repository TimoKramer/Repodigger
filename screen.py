#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'


from kivy.app import App
from kivy.event import EventDispatcher
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


Builder.load_file('screen.kv')


class RepodiggerApp(App):

    def build(self):
        return RepodiggerController()


class RepodiggerController(FloatLayout):
    def build(self, **kwargs):
        self.register_event_type('on_ok')
        super(RepodiggerController, self).__init__(**kwargs)

    def check_status(self):
        print('button statis is: {state}'.format(state=self.ids.ok_button.state))
        print('text input text is: {txt}'.format(txt=self.ids.text_input.text))


class LoginScreen(BoxLayout):

    def get_input(self, input):
        print(input)


class MyBackground(FloatLayout):
    pass


if __name__ == '__main__':
    RepodiggerApp().run()