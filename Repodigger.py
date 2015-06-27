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
import re, json, Data, datetime


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
    milestone_data = []
    milestone_index = 0

    def __init__(self, **kwargs):
        super(BurndownScreen, self).__init__(**kwargs)

    def initialize_burndown(self):
        self.milestone_index = 0
        Data.DataSingleton().request_all_milestones()
        self.milestone_data = Data.DataSingleton().get_milestone_data()
        self.draw_burndown()

    def draw_text(self):
        current_milestone = self.get_current_milestone()
        self.ids.get('milestone_label').text = current_milestone['title']
        actual_milestone = self.milestone_data[self.milestone_index]
        closed_issues = actual_milestone['total_issues']-actual_milestone['open_issues']
        total_issues = actual_milestone['total_issues']
        self.ids.get('closed_label').text = 'Closed: ' + str(closed_issues) + '/' + str(total_issues)

    def draw_burndown(self):
        canvas_widget = self.ids.get('canvas_widget')
        canvas_widget.canvas.clear()
        self.draw_text()
        with self.canvas:
            self.target_line = Line(points=[self.parent.width*0.1, self.parent.height*0.2,
                         self.parent.width*0.1, self.parent.height*0.9,
                         self.parent.width*0.9, self.parent.height*0.2,
                         self.parent.width*0.1, self.parent.height*0.2], width=1.0)
            self.actual_line = Line(points=self.get_points_for_actual_line(), width=3.0)
        print(self.target_line.points)
        print(self.actual_line.points)

    def on_back_press(self):
        self.parent.current = 'Issue Screen'

    def get_current_milestone(self):
        try:
            return self.milestone_data[self.milestone_index]
        except IndexError:
            print('No milestone with index ' + str(self.milestone_index))

    def previous_milestone(self):
        try:
            self.milestone_index -= 1
            self.draw_burndown()
        except IndexError:
            print('No more Milestones:(')

    def next_milestone(self):
        try:
            self.milestone_index += 1
            self.draw_burndown()
        except IndexError:
            print('No more Milestones:(')

    def get_width_height_of_single_issue(self, milestone_data):
        try:
            issue_width = self.parent.width*0.8/milestone_data['days_of_milestone']
        except ZeroDivisionError:
            issue_width = self.parent.width*0.8/2
        try:
            issue_height = self.parent.height*0.8/milestone_data['total_issues']
        except ZeroDivisionError:
            issue_height = self.parent.height*0.8/2
        return issue_width, issue_height

    def get_offset_x_y_burndown(self):
        return self.parent.width*0.1, self.parent.height*0.1

    def get_points_for_actual_line(self):
        width_of_issue = self.get_width_height_of_single_issue(self.get_current_milestone())[0]
        height_of_issue = self.get_width_height_of_single_issue(self.get_current_milestone())[1]
        position_offset_x = self.get_offset_x_y_burndown()[0]
        position_offset_y = self.get_offset_x_y_burndown()[1]
        daylist = self.get_issue_count()
        coordinate_list = []
        for day in range(len(daylist)):
            coordinate_list.append(day*width_of_issue + position_offset_x)
            coordinate_list.append(daylist[day]*height_of_issue + position_offset_y)
        return coordinate_list

    def get_issue_count(self):
        actual_milestone = self.get_current_milestone()
        days_of_milestone = actual_milestone['days_of_milestone']
        total_issues_of_milestone = actual_milestone['total_issues']
        issue_counter_list = [None for _ in range(days_of_milestone)]
        issues_left_of_milestone = total_issues_of_milestone
        for i in range(days_of_milestone):
            issues_left_of_milestone -= self.get_issues_closed_on_day(i)
            issue_counter_list[i] = issues_left_of_milestone
        return issue_counter_list

    def get_issues_closed_on_day(self, day):
        counter = 0
        actual_milestone = self.get_current_milestone()
        for issues_closing in actual_milestone['closed_issues']:
            if issues_closing['closing_day'] is day:
                counter += 1
        return counter


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
        self.parent.get_screen('Issue Screen').build_issue_widgets(Data.DataSingleton().get_all_issues_as_list())


class IssueScreen(Screen):
    issues_archive = ListProperty(None)

    def __init__(self, **kwargs):
        kwargs['cols'] = 1
        super(IssueScreen, self).__init__(**kwargs)

    def build_issue_widgets(self, issues):
        self.issues_list.adapter.data.clear()
        self.issues_list.adapter.data.extend(issues)
        self.issues_list._trigger_reset_populate()

    def on_burndown_press(self):
        self.parent.current = 'Burndown Screen'
        self.parent.get_screen('Burndown Screen').initialize_burndown()

    def on_change_press(self):
        self.parent.current = 'Login Screen'

    def on_detail_press(self):
        self.parent.current = 'Detail Screen'
        self.parent.get_screen('Detail Screen').populate_details()

    def on_show_all_press(self):
        self.build_issue_widgets(Data.DataSingleton().get_all_issues_as_list())

    def on_show_open_press(self):
        self.build_issue_widgets(Data.DataSingleton().get_open_issues_as_list())

    def on_show_closed_press(self):
        self.build_issue_widgets(Data.DataSingleton().get_closed_issues_as_list())


class IssueButton(ListItemButton):
    def on_detail_press(self):
        self.parent.parent.parent.parent.parent.on_detail_press()


class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)

    def populate_details(self):
        pass

    def on_back_press(self):
        self.parent.current = 'Issue Screen'


if __name__ == '__main__':
    RepodiggerApp().run()
