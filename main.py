from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle

from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton, MDFabButton
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout

class Sidebar(BoxLayout):
    def __init__(self, smtp_callback, emails_callback, db_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, 1)
        self.width = 200
        self.x = -200
        self.padding = [10, 10, 10, 10]
        self.spacing = 1

        with self.canvas.before:
            Color(0.92, 0.92, 0.95, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.add_widget(
            MDButton(
                MDButtonText(text="Configure SMTP"),
                style="text",
                size_hint_y=None,
                height=40,
                on_release=smtp_callback,
            )
        )
        self.add_widget(
            MDButton(
                MDButtonText(text="Configure Emails"),
                style="text",
                size_hint_y=None,
                height=40,
                on_release=emails_callback,
            )
        )
        self.add_widget(
            MDButton(
                MDButtonText(text="Configure Database"),
                style="text",
                size_hint_y=None,
                height=40,
                on_release=db_callback,
            )
        )

        self.add_widget(Widget(size_hint_y=1))

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def show_sidebar(self):
        Animation.cancel_all(self)
        Animation(x=0, duration=0.2).start(self)

    def hide_sidebar(self):
        Animation.cancel_all(self)
        Animation(x=-self.width, duration=0.2).start(self)

    def is_open(self):
        return self.x >= 0

class Overlay(Widget):
    def __init__(self, on_dismiss, **kwargs):
        super().__init__(**kwargs)
        self.on_dismiss = on_dismiss
        self.size_hint = (1, 1)
        self.pos = (0, 0)
        with self.canvas:
            Color(0, 0, 0, 0.2)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_touch_down(self, touch):
        if touch.x > 200:
            self.on_dismiss()
            return True
        return False

class CenteredSquareButtonPage(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        self.dialog = None
        self.smtp_dialog = None
        self.emails_dialog = None
        self.db_dialog = None

        self.settings_btn = MDIconButton(
            icon="cog",
            icon_color=(0.035, 0.247, 0.706, 1),
            pos_hint={'x': 0, 'top': 1},
        )
        self.settings_btn.bind(on_press=self.toggle_sidebar)
        self.add_widget(self.settings_btn)

        self.button = MDFabButton(
            icon="send",
            md_bg_color=(0.035, 0.247, 0.706, 1),
            icon_color=(1, 1, 1, 1),
            style="large",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_release=self.show_otp_sent_dialog,
        )
        self.add_widget(self.button)

        self.sidebar = Sidebar(
            smtp_callback=self.show_smtp_dialog,
            emails_callback=self.show_emails_dialog,
            db_callback=self.show_db_dialog
        )
        self.sidebar.pos = (-self.sidebar.width, 0)
        self.add_widget(self.sidebar)

        self.overlay = Overlay(on_dismiss=self._hide_sidebar)
        self.overlay.opacity = 0
        self.overlay.disabled = True
        self.add_widget(self.overlay)

    def toggle_sidebar(self, instance):
        if self.sidebar.is_open():
            self._hide_sidebar()
        else:
            self._show_sidebar()

    def _show_sidebar(self):
        self.sidebar.show_sidebar()
        self.overlay.opacity = 1
        self.overlay.disabled = False

    def _hide_sidebar(self, *args):
        self.sidebar.hide_sidebar()
        self.overlay.opacity = 0
        self.overlay.disabled = True

    def show_otp_sent_dialog(self, *args):
        if not self.dialog:
            self.dialog = MDDialog(
                MDDialogHeadlineText(text="Success"),
                MDDialogSupportingText(text="OTP sent Successfully"),
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="OK"),
                        style="text",
                        on_release=self.close_dialog,
                    ),
                ),
            )
        self.dialog.open()

    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()

    def show_smtp_dialog(self, *args):
        if not self.smtp_dialog:
            self.email_field = MDTextField(
                hint_text="Email",
                mode="outlined",
                size_hint_y=None,
                height=48,
                size_hint_x=1
            )
            self.password_field = MDTextField(
                hint_text="Password",
                password=True,
                mode="outlined",
                size_hint_y=None,
                height=48,
                size_hint_x=1
            )

            content_box = MDBoxLayout(
                orientation='vertical',
                spacing=10,
                size_hint_y=None,
                height=48*2 + 10,
            )
            content_box.add_widget(self.email_field)
            content_box.add_widget(self.password_field)

            self.smtp_dialog = MDDialog(
                MDDialogHeadlineText(text="Configure SMTP"),
                MDDialogSupportingText(text="Enter your SMTP email and password."),
                MDDialogContentContainer(content_box),
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="Save"),
                        style="text",
                        on_release=self.save_smtp_config,
                    ),
                    MDButton(
                        MDButtonText(text="Cancel"),
                        style="text",
                        on_release=self.close_smtp_dialog,
                    ),
                ),
            )
        self.smtp_dialog.open()

    def save_smtp_config(self, *args):
        email = self.email_field.text
        password = self.password_field.text
        self.smtp_dialog.dismiss()

    def close_smtp_dialog(self, *args):
        if self.smtp_dialog:
            self.smtp_dialog.dismiss()

    def show_emails_dialog(self, *args):
        if not self.emails_dialog:
            self.email_input = MDTextField(
                hint_text="Email",
                mode="outlined",
                size_hint_y=None,
                height=48,
                size_hint_x=1
            )

            content_box = MDBoxLayout(
                orientation='vertical',
                spacing=10,
                size_hint_y=None,
                height=48,
            )
            content_box.add_widget(self.email_input)

            self.emails_dialog = MDDialog(
                MDDialogHeadlineText(text="Configure Emails"),
                MDDialogSupportingText(text="Enter the email address."),
                MDDialogContentContainer(content_box),  # <-- wrap your box here!
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="Save"),
                        style="text",
                        on_release=self.save_emails_config,
                    ),
                    MDButton(
                        MDButtonText(text="Cancel"),
                        style="text",
                        on_release=self.close_emails_dialog,
                    ),
                ),
            )

        self.emails_dialog.open()

    def save_emails_config(self, *args):
        email = self.email_input.text
        self.emails_dialog.dismiss()

    def close_emails_dialog(self, *args):
        if self.emails_dialog:
            self.emails_dialog.dismiss()

    def show_db_dialog(self, *args):
        if not self.db_dialog:
            self.db_name_field = MDTextField(
                hint_text="Database Name",
                mode="outlined",
                size_hint_y=None,
                height=48,
                size_hint_x=1
            )
            self.db_user_field = MDTextField(
                hint_text="Username",
                mode="outlined",
                size_hint_y=None,
                height=48,
                size_hint_x=1
            )
            self.db_pass_field = MDTextField(
                hint_text="Password",
                password=True,
                mode="outlined",
                size_hint_y=None,
                height=48,
                size_hint_x=1
            )

            content_box = MDBoxLayout(
                orientation='vertical',
                spacing=10,
                size_hint_y=None,
                height=10 + 48*3 + 10*2,
            )
            spacer = Widget(size_hint_y=None, height=10)
            content_box.add_widget(spacer)
            content_box.add_widget(self.db_name_field)
            content_box.add_widget(self.db_user_field)
            content_box.add_widget(self.db_pass_field)

            self.db_dialog = MDDialog(
                MDDialogHeadlineText(text="Configure Database"),
                MDDialogSupportingText(text="Enter database info (dbname, username, password)."),
                MDDialogContentContainer(content_box),  # <-- wrap your box here!
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="Save"),
                        style="text",
                        on_release=self.save_db_config,
                    ),
                    MDButton(
                        MDButtonText(text="Cancel"),
                        style="text",
                        on_release=self.close_db_dialog,
                    ),
                ),
            )

        self.db_dialog.open()

    def save_db_config(self, *args):
        db_name = self.db_name_field.text
        db_user = self.db_user_field.text
        db_pass = self.db_pass_field.text
        self.db_dialog.dismiss()

    def close_db_dialog(self, *args):
        if self.db_dialog:
            self.db_dialog.dismiss()

class SimpleApp(MDApp):
    def build(self):
        return CenteredSquareButtonPage()

if __name__ == "__main__":
    SimpleApp().run()
