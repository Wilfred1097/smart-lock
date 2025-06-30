from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout

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

        smtp_btn = MDFlatButton(
            text="Configure SMTP",
            size_hint_y=None,
            height=40,
            md_bg_color=(0.92, 0.92, 0.95, 1),      # White background
            text_color=(0, 0, 0, 1),       # Black text
            on_release=smtp_callback
        )
        self.add_widget(smtp_btn)

        emails_btn = MDFlatButton(
            text="Configure Emails",
            size_hint_y=None,
            height=40,
            md_bg_color=(0.92, 0.92, 0.95, 1),
            text_color=(0, 0, 0, 1),
            on_release=emails_callback,
        )
        self.add_widget(emails_btn)

        db_btn = MDFlatButton(
            text="Configure Database",
            size_hint_y=None,
            height=40,
            md_bg_color=(0.92, 0.92, 0.95, 1),
            text_color=(0, 0, 0, 1),
            on_release=db_callback,
        )
        self.add_widget(db_btn)

        self.add_widget(Widget(size_hint_y=1))  # Only one spacer at the end!

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
        self.dialog = None  # For OTP dialog
        self.smtp_dialog = None
        self.emails_dialog = None
        self.db_dialog = None

        self.settings_btn = MDIconButton(
            icon="cog",
            theme_text_color="Custom",
            text_color=(0.035, 0.247, 0.706, 1),
            pos_hint={'x': 0, 'top': 1},
            icon_size="32sp"
        )
        self.settings_btn.bind(on_press=self.toggle_sidebar)
        self.add_widget(self.settings_btn)

        self.button = MDFlatButton(
            text="Send OTP",
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color=(0.92, 0.92, 0.95, 1),
            text_color=(1, 1, 1, 1),  # <-- White text
            font_size='16sp',
        )
        self.button.bind(on_release=self.show_otp_sent_dialog)
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
                title="Success",
                text="OTP sent Successfully",
                size_hint=(0.8, None),
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()

    def show_smtp_dialog(self, *args):
        if not self.smtp_dialog:
            self.email_field = MDTextField(
                hint_text="Email",
                mode="rectangle",
                size_hint_y=None,
                height=48,
                size_hint_x=1
            )
            self.password_field = MDTextField(
                hint_text="Password",
                password=True,
                mode="rectangle",
                size_hint_y=None,
                height=48,
                size_hint_x=1
            )

            box = MDBoxLayout(
                orientation='vertical',
                spacing=10,
                size_hint_y=None,
                width=200,
                size_hint_x=None,
                height=48*2 + 10,
            )
            box.add_widget(self.email_field)
            box.add_widget(self.password_field)

            self.smtp_dialog = MDDialog(
                title="Configure SMTP",
                type="custom",
                content_cls=box,
                size_hint=(0.8, None),  # Ensure dialog width is consistent
                buttons=[
                    MDFlatButton(
                        text="Save",
                        on_release=self.save_smtp_config
                    ),
                    MDFlatButton(
                        text="Cancel",
                        on_release=self.close_smtp_dialog
                    ),
                ],
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
                mode="rectangle",
                size_hint_y=None,
                height=48,
                size_hint_x=1
            )

            box = MDBoxLayout(
                orientation='vertical',
                spacing=10,
                size_hint_y=None,
                width=200,
                size_hint_x=None,
                height=48,
            )
            box.add_widget(self.email_input)

            self.emails_dialog = MDDialog(
                title="Configure Emails",
                type="custom",
                content_cls=box,
                size_hint=(0.8, None),  # Same width as others
                buttons=[
                    MDFlatButton(
                        text="Save",
                        on_release=self.save_emails_config
                    ),
                    MDFlatButton(
                        text="Cancel",
                        on_release=self.close_emails_dialog
                    ),
                ],
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
                mode="rectangle",
                size_hint_y=None,
                height=48,
                size_hint_x=1
            )
            self.db_user_field = MDTextField(
                hint_text="Username",
                mode="rectangle",
                size_hint_y=None,
                height=48,
                size_hint_x=1
            )
            self.db_pass_field = MDTextField(
                hint_text="Password",
                password=True,
                mode="rectangle",
                size_hint_y=None,
                height=48,
                size_hint_x=1
            )

            box = MDBoxLayout(
                orientation='vertical',
                spacing=10,
                size_hint_y=None,
                width=200,
                size_hint_x=None,
                height=10 + 48*3 + 10*2,  # 10 for spacer, 3 fields, 2 spacings
            )
            # Add a spacer at the top for space between title and first input
            spacer = Widget(size_hint_y=None, height=10)
            box.add_widget(spacer)
            box.add_widget(self.db_name_field)
            box.add_widget(self.db_user_field)
            box.add_widget(self.db_pass_field)

            self.db_dialog = MDDialog(
                title="Configure Database",
                type="custom",
                content_cls=box,
                size_hint=(0.8, None),  # Same width as other dialogs
                buttons=[
                    MDFlatButton(
                        text="Save",
                        on_release=self.save_db_config
                    ),
                    MDFlatButton(
                        text="Cancel",
                        on_release=self.close_db_dialog
                    ),
                ],
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
