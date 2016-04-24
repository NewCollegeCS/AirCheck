# -*- coding: utf-8 -*-
import kivymd.snackbar as Snackbar
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch
from kivymd.navigationdrawer import NavigationDrawer
from kivymd.selectioncontrols import MDCheckbox
from kivymd.theming import ThemeManager
from kivymd.dialog import MDDialog
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
import os
import requests
from hashlib import sha1

main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import NavigationDrawer kivymd.navigationdrawer.NavigationDrawer
#:import MDList kivymd.list.MDList
#:import OneLineListItem kivymd.list.OneLineListItem
#:import SingleLineTextField kivymd.textfields.SingleLineTextField
#:import MDCard kivymd.card.MDCard
#:import MDFlatbutton kivymd.button.MDFlatButton
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors

BoxLayout:
    orientation: 'vertical'
    Toolbar:
        id: toolbar
        title: 'AirCheck'
        left_action_items: [['menu', lambda x: app.nav_drawer.toggle()]]

    ScreenManager:
        id: manager
        Screen:
            name: 'card'
            MDCard:
                orientation: 'vertical'
                size_hint: None, None
                size: dp(388), dp(480)
                background_color: 0,0,0,.27
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                BoxLayout:
                    size: root.size
                    orientation: 'vertical'
                    halign: 'center'
                    Image:
                        id: _header_bg
                        source: './assets/Collaborator Male-96.png'
                        keep_ratio: True
                    MDLabel:
                        font_style:'Body1'
                        size_hint: None, None
                        width: dp(388)
                        height: dp(40)
                        font_size: 25
                        halign: 'center'
                        text: 'Have you been coughing?'
                BoxLayout:
                    size: root.size
                    pos: root.pos
                    orientation: 'horizontal'
                    MDFlatButton:
                        text: 'Yes'
                        size_hint: (2, .3)
                        on_press: root.login()
                        background_color: 0,.8,0,.4
                    MDFlatButton:
                        text: 'No'
                        on_press: root.login()
                        size_hint: (2, .3)
                        background_color: .8,0,0,.4



        Screen:
            name: 'list'
            ScrollView:
                do_scroll_x: False
                MDList:
                    id: ml
                    OneLineListItem:
                        text: "One-line item"

        Screen:
            name: 'textfields'
            ScrollView:
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: dp(1000)
                    BoxLayout:
                        size_hint_y: None
                        height: dp(144)
                        SingleLineTextField:
                            id: text_field
                            size_hint: 0.8, None
                            height: dp(48)
                            hint_text: "Write something"

        Screen:
            name: 'welcome'
            BoxLayout:
                orientation: 'vertical'
                spacing: 50
                MDLabel:
                    orientation: 'vertical'
                    text: 'Bruber'
                    font_size: 25
                BoxLayout:
                    MDRaisedButton:
                        text: 'Sign In'
                        font_size: 18
                        halign: 'center'
                        text_size: root.width - 20, 20
                        on_press: root.login()
                    MDRaisedButton:
                        text: 'Sign Up'
                        font_size: 18
                        halign: 'center'
                        text_size: root.width + 20, 20
                        on_press: root.register()

        Screen:
            name: 'dash'
            ScrollView:
                BoxLayout:
                    orientation: 'vertical'
                    MDRaisedButton:
                        text: "Let's rate!"
                        font_size: 24
                        on_press: root.start_rate()
                    MDLabel:
                        text: "Your dashboard"
                        font_size: 32
                    MDRaisedButton:
                        text: "Disconnect"
                        font_size: 24
                        on_press: root.disconnect()

        Screen:
            name: 'rate'
            ScrollView:
                BoxLayout:
                    orientation: 'vertical'
                    MDRaisedButton:
                        text: "Smokey?"
                        font_size: 22
                        on_press: root.notice_me()
                    MDRaisedButton:
                        text: "Smarmy?"
                        font_size: 22
                        on_press:root.notice_me()

        Screen:
            name: 'login'
            ScrollView:
                BoxLayout:
                    id: login_layout
                    orientation: 'vertical'
                    MDLabel:
                        text: 'Login'
                        font_size: 32
                    BoxLayout:
                        orientation: 'vertical'
                        MDLabel:
                            text: 'Login'
                            font_size: 18
                            halign: 'left'
                        TextInput:
                            id: login
                            multiline: False
                            font_size: 28
                    BoxLayout:
                        orientation: 'vertical'
                        Label:
                        MDLabel:
                            text: 'Password'
                            halign: 'left'
                            font_size: 18
                        TextInput:
                            id: password
                            multiline: False
                            password: True
                            font_size: 28
                    MDRaisedButton:
                        text: 'Connection'
                        font_size: 24
                        on_press: root.do_login(login.text, password.text)

        Screen:
            name: 'register'
            ScrollView:
                BoxLayout:
                    id: register_layout
                    orientation: 'vertical'
                    MDLabel:
                        text: 'Register'
                        font_size: 32
                    BoxLayout:
                        orientation: 'vertical'
                        MDLabel:
                            text: 'Username'
                            halign: 'left'
                            font_size: 18
                        TextInput:
                            id: username
                            multiline: False
                            font_size: 28
                    BoxLayout:
                        orientation: 'vertical'
                        MDLabel:
                            text: 'Email'
                            halign: 'left'
                            font_size: 18
                        TextInput:
                            id: email
                            multiline: False
                            font_size: 28
                    BoxLayout:
                        orientation: 'vertical'
                        MDLabel:
                            text: 'Password'
                            halign: 'left'
                            font_size: 18
                        TextInput:
                            id: password
                            multiline: False
                            password: True
                            font_size: 28
                    MDRaisedButton:
                        text: 'Register'
                        font_size: 24
                        on_press: root.do_register(username.text, email.text, password.text)

<KitchenSinkNavDrawer>
    title: "NavigationDrawer"
    NavigationDrawerIconButton:
        icon: 'circle'
        text: "Welcome"
        on_release: app.root.ids.manager.current = 'welcome'
    NavigationDrawerIconButton:
        icon: 'circle'
        text: "Cards"
        on_release: app.root.ids.manager.current = 'card'
    NavigationDrawerIconButton:
        icon: 'circle'
        text: "Lists"
        on_release: app.root.ids.manager.current = 'list'
    NavigationDrawerIconButton:
        icon: 'circle'
        text: "Dash"
        on_release: app.root.ids.manager.current = 'dash'
    NavigationDrawerIconButton:
        icon: 'circle'
        text: "Rate"
        on_release: app.root.ids.manager.current = 'rate'
    NavigationDrawerIconButton:
        icon: 'circle'
        text: "Login"
        on_release: app.root.ids.manager.current = 'login'
    NavigationDrawerIconButton:
        icon: 'circle'
        text: "Register"
        on_release: app.root.ids.manager.current = 'register'
'''
class KitchenSinkNavDrawer(NavigationDrawer):
        pass

class Header(Widget):
    "TODO"

class Welcome(Screen):

    def login(self):
        app.root.ids.manager.transition = SlideTransition(direction="left")
        app.root.ids.manager.current = 'login'
        pass

    def register(self):
        app.root.ids.manager.transition = SlideTransition(direction="left")
        app.root.ids.manager.current = 'register'
        pass


class Login(Screen):

    def do_login(self, username, password):
        app = App.get_running_app()

        # Query our server and database with a person's
        #     credentials

        credentials = {
            'user_id': Utils.hash(username),
            'password': Utils.salt(password)
        }

        r = requests.get("http://aircheck.ncf.space" + "/LoginUser", json=credentials)

        # Check whether it has been a valid request, we assume it does
        #     and that we've been sent back a user_id

        print(r.status_code)
        print(r.json())

        valid_login = False
        if r.status_code == 200:
            r = r.json()
            if r['status'] == 'ok':
                valid_login = True

        if valid_login:
            app.user_id = r['log_in']
            app.root.ids.manager.transition = SlideTransition(direction="left")
            app.root.ids.manager.current = 'dashboard'
        else:
            self.reset_form()

        app.config.read(app.get_application_config())
        app.config.write()

    def reset_form(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

class Register(Screen):

    def do_register(self, username, email, password):
        app = App.get_running_app()

        user_id = Utils.hash(username)

        check_registration = {
            'user_id': user_id,
            'email': email,
        }

        r = requests.get("http://aircheck.ncf.space" + "/checkNew", json=check_registration)

        user_exists = True
        if r.status_code == 200 and r.json()['status'] == 'ok':
            user_exists = False

        if user_exists:
            print("Error: User exits")
            self.reset_form()

        registration_info = {
            'user_id': user_id,
            'email': email,
            'password': Utils.salt(password),
            'provider':'bruber'
        }

        r = requests.post("http://aircheck.ncf.space" + "/postUser", json=registration_info)

        valid_registration = False
        if r.status_code == 200:
            r = requests.get("http://aircheck.ncf.space" + "/checkNew", json=check_registration)
            if r.status_code == 200 and r.json()['status'] == 'fail':
                valid_registration = True

        if valid_registration:
            app.user_id = user_id
            app.root.ids.manager.transition = SlideTransition(direction="left")
            app.root.ids.manager.current = 'dashboard'
        else:
            self.reset_form()

    def reset_form(self):
        self.ids['username'].text = ""
        self.ids['email'].text = ""
        self.ids['password'].text = ""

class Dashboard(Screen):

    def disconnect(self):
        app.root.ids.manager.transition = SlideTransition(direction="right")
        app.root.ids.manager.current = 'login'
        app.root.ids.manager.get_screen('login').reset_form()
        pass

    def start_rate(self):
        app.root.ids.manager.transition = SlideTransition(direction="right")
        app.root.ids.manager.current = 'rate'
        app.root.ids.manager.get_screen('rate')
        pass

class Rate(Screen):
    def notice_me(self):
        print 'lol'


class Utils():
    @classmethod
    def salt(cls, msg):
        return Utils.hash(Utils.hash(msg))

    @classmethod
    def hash(cls, msg):
        return sha1(msg.encode('utf-8')).hexdigest()

class AircheckApp(App):
    user_id = StringProperty(None)
    theme_cls = ThemeManager()
    nav_drawer = ObjectProperty()

    def build(self):
#        Window.bind(on_motion=tap_direction)
        main_widget = Builder.load_string(main_widget_kv)
        self.nav_drawer = KitchenSinkNavDrawer()
        return main_widget

    def get_application_config(self):
        if (not self.user_id):
            return super(AircheckApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.user_id

        if (not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(AircheckApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )

def tap_direction(self, etype, motionevent):
    if motionevent.pos[0] > 400:
        print "swiped right"
    else:
        print "swiped left"


if __name__ == '__main__':
    AircheckApp().run()
