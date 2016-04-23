from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os

class Welcome(Screen):

    def login(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'login'

    def register(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'register'


class Login(Screen):

    def do_login(self, login_text, password_text):
        app = App.get_running_app()

        app.username = login_text
        app.password = password_text

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'dashboard'

        app.config.read(app.get_application_config())
        app.config.write()

    def reset_form(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

class Register(Screen):

    def do_register(self, name_text, email_text, password_text):
        app = App.get_running_app()

        # Create a connection to our server and
        #     attempt to make a new user

        valid_registration = True

        if valid_registration:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'dashboard'
        else:
            # Flash errors and redisplay the form
            self.reset_form()

    def reset_form(self):
        self.ids['username'].text = ""
        self.ids['name'].text = ""
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
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Welcome(name='welcome'))
        manager.add_widget(Login(name='login'))
        manager.add_widget(Register(name='register'))
        manager.add_widget(Dashboard(name='dashboard'))
        manager.add_widget(Rate(name="rate"))

        return manager

    def get_application_config(self):
        if (not self.username):
            return super(AircheckApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if (not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(AircheckApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )
