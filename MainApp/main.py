from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.factory import Factory
from kivymd.toast import toast
from libs.screens.root import Root
import threading
import time
from kivy.clock import Clock

if platform=="android":
    from kivyauth.google_auth import initialize_google, login_google, logout_google

def emulate_android_device(
    pixels_horizontal=1080, pixels_vertical=2240, android_dpi=394, monitor_dpi=157
):
    scale_factor = monitor_dpi / android_dpi
    Window.size = (scale_factor * pixels_horizontal, scale_factor * pixels_vertical)


if platform != "android":
    emulate_android_device()
    LIVE_UI = 0
else:
    from libs.modules.AndroidAPI import statusbar

    LIVE_UI = 0

Window.softinput_mode = "below_target"

KV = """
#: import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer
HotReloadViewer:
    path: app.PATH
    
"""
font_file = "kivymd/fonts/Montserrat-Bold.ttf"


class MyApp(MDApp):
    PATH = "LIVE_UI.kv"
    user_name = StringProperty()
    user_mail = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.font_styles.update(
            {
                "H1": [font_file, 96, False, -1.5],
                "H2": [font_file, 60, False, -0.5],
                "H3": [font_file, 48, False, 0],
                "H4": [font_file, 34, False, 0.25],
                "H5": [font_file, 24, False, 0],
                "H6": [font_file, 20, False, 0.15],
                "Button": [font_file, 14, True, 1.25],
                "Body1": [font_file, 16, False, 0.5],
                "Body2": [font_file, 14, False, 0.25],
            }
        )

    def build(self):
        Builder.load_file("libs/classes.kv")
        self.root = Root()
        self.theme_cls.primary_palette = "Red"
        self.root.set_current("OnBoarding")
        # self.root.set_current("Home")
        if platform == "android":
            initialize_google(self.successful_login, self.error_listener)
        if LIVE_UI:
            return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            statusbar(status_color="DC5555", white_text=True)

    def change_statusbar(self):
        if platform == "android":
            statusbar(status_color="FDF7F7", white_text=False)

        # self.root.ids.box.export_to_png("assets/gradient.png")
        # self.root.ids.on_boarding_2.export_to_png("screenshots/on_boarding_2.png")
        # self.root.ids.on_boarding_3.export_to_png("screenshots/on_boarding_3.png")
        # self.root.ids.register_screen.export_to_png("screenshots/Signup.png")

    def login(self):
        """
        Login with Google
        """
        if platform == "android":
            login_google()
        else:
            self.successful_login("demo_name", "demo_email", "demo_photo_uri", 123456)

    def successful_login(self, name, email, photo_uri, user_id):
        toast(f"Logged in {name} with email {email}")
        print(f"{user_id = }")
        self.user_name = name
        self.user_mail = email
        self.root.set_current("CreateAccount")

    def add_hospital_list(self, text, time_remaining):
        list = Factory.HospitalList()
        list.text = text
        list.time_remaining = time_remaining
        Clock.schedule_once(lambda *args: self.root.Home.ids.details.ids.box.add_widget(list, index = 1), 5)

    def send_notif(self):
        import plyer
        title = "Shortage of AB+ blood at capital hospital"
        message = "Time left: 2hrs Remaining"
        if platform=="android":
            plyer.notification.notify(
            title=title,
            message=message,
        )
        self.add_hospital_list(title, message)
        

    def error_listener(self):
        toast("Some error occured.")


if __name__ == "__main__":
    MyApp().run()
