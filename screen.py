#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Timo Kramer'
__immanr__ = '20119022'

import kivy, data
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

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
        self.size_hint = (0.6, 0.05)
        self.spacing = 10
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.add_widget(Label(text='Enter Repo: ', size_hint=(.2, 1)))
        self.add_widget(TextInput(text='e.g. "timokramer/repodigger"', size_hint = (.7, 1)))
        self.add_widget(Button(text='OK', font_size=14, size_hint_x=.1))


class Screen(AnchorLayout):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.add_widget(LoginScreen())


class BaseLayout(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(BaseLayout, self).__init__(**kwargs)

        with self.canvas.before:
            Color(.1, .1, .1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class RootWidget(BoxLayout):
    pass


class MainApp(App):
    def build(self):
        root = RootWidget()
        c = BaseLayout()
        root.add_widget(c)
        c.add_widget(
            Image(
                source="assets/cc-wallpaper-ipad.png",
                size_hint=(1.5, 1.5),
                pos_hint={'center_x': .5, 'center_y': .5}
            )
        )
        c.add_widget(LoginScreen())
        return root

if __name__ == '__main__':
    MainApp().run()
