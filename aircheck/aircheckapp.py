from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.window import Window
import os
import requests
from hashlib import sha1

class Header(Widget):
    "TODO"

class Welcome(Screen):

    def login(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'login'

    def register(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'register'


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
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'dashboard'
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
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'dashboard'
        else:
            self.reset_form()

    def reset_form(self):
        self.ids['username'].text = ""
        self.ids['email'].text = ""
        self.ids['password'].text = ""

class Dashboard(Screen):

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').reset_form()

    def start_rate(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'rate'
        self.manager.get_screen('rate')

class Rate(Screen):
    pass

class AircheckApp(App):
    user_id = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Welcome(name='welcome'))
        manager.add_widget(Login(name='login'))
        manager.add_widget(Register(name='register'))
        manager.add_widget(Dashboard(name='dashboard'))
        manager.add_widget(Rate(name="rate"))

        return manager

    def get_application_config(self):
        if (not self.user_id):
            return super(AircheckApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.user_id

        if (not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(AircheckApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )

class Utils():
    @classmethod
    def salt(cls, msg):
        return Utils.hash(Utils.hash(msg))

    @classmethod
    def hash(cls, msg):
        return sha1(msg.encode('utf-8')).hexdigest()
