from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.fitimage import FitImage
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHintText,
    MDTextFieldLeadingIcon,
)

KV = '''
<BaseMDNavigationItem>
    MDNavigationItemIcon:
        icon: root.icon
    MDNavigationItemLabel:
        text: root.text

<OTPScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        spacing: "20dp"
        pos_hint: {"center_x": .5, "center_y": .5}

        MDLabel:
            text: "Send OTP to added Email"
            halign: "center"
            font_style: "Title"
            adaptive_height: True

        MDButton:
            style: "filled"
            pos_hint: {"center_x": .5}
            on_release: app.send_otp()

            MDButtonText:
                text: "Send"

<SMTPScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        spacing: "20dp"
        padding: "20dp"
        pos_hint: {"center_x": .5, "center_y": .5}

        MDLabel:
            text: "Configure SMTP"
            halign: "center"
            font_style: "Title"
            adaptive_height: True

        MDTextField:
            id: email_field
            mode: "outlined"
            size_hint_x: .8
            pos_hint: {"center_x": .5}
            MDTextFieldHintText:
                text: "Email"
            MDTextFieldLeadingIcon:
                icon: "email"

        MDTextField:
            id: password_field
            mode: "outlined"
            size_hint_x: .8
            pos_hint: {"center_x": .5}
            password: True
            password_mask: "*"
            MDTextFieldHintText:
                text: "Password"
            MDTextFieldLeadingIcon:
                icon: "key"

        MDButton:
            style: "filled"
            pos_hint: {"center_x": .5}
            on_release: app.save_smtp_settings(email_field.text, password_field.text)
            MDButtonText:
                text: "Save"

<EmailsScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        spacing: "20dp"
        padding: "20dp"
        pos_hint: {"center_x": .5, "center_y": .5}

        MDLabel:
            text: "Configure Email to Send the OTP"
            halign: "center"
            font_style: "Title"
            adaptive_height: True

        MDTextField:
            id: recipient_email_field
            mode: "outlined"
            size_hint_x: .8
            pos_hint: {"center_x": .5}
            MDTextFieldHintText:
                text: "Recipient Email"
            MDTextFieldLeadingIcon:
                icon: "account"

        MDButton:
            style: "filled"
            pos_hint: {"center_x": .5}
            on_release: app.save_recipient_email(recipient_email_field.text)
            MDButtonText:
                text: "Save"

<DatabaseScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        spacing: "15dp"
        padding: "20dp"
        pos_hint: {"center_x": .5, "center_y": .5}

        MDLabel:
            text: "Configure Database"
            halign: "center"
            font_style: "Title"
            adaptive_height: True

        MDTextField:
            id: server_field
            mode: "outlined"
            size_hint_x: .9
            pos_hint: {"center_x": .5}
            MDTextFieldHintText:
                text: "Servername"
            MDTextFieldLeadingIcon:
                icon: "server"

        MDTextField:
            id: dbname_field
            mode: "outlined"
            size_hint_x: .9
            pos_hint: {"center_x": .5}
            MDTextFieldHintText:
                text: "Database Name"
            MDTextFieldLeadingIcon:
                icon: "database"

        MDTextField:
            id: user_field
            mode: "outlined"
            size_hint_x: .9
            pos_hint: {"center_x": .5}
            MDTextFieldHintText:
                text: "Username"
            MDTextFieldLeadingIcon:
                icon: "account"

        MDTextField:
            id: db_password_field
            mode: "outlined"
            size_hint_x: .9
            pos_hint: {"center_x": .5}
            password: True
            password_mask: "*"
            MDTextFieldHintText:
                text: "Password"
            MDTextFieldLeadingIcon:
                icon: "key"

        MDButton:
            style: "filled"
            pos_hint: {"center_x": .5}
            on_release: app.save_database_settings(server_field.text, dbname_field.text, user_field.text, db_password_field.text)
            MDButtonText:
                text: "Save"

# Main layout of the application
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: self.theme_cls.backgroundColor

    MDScreenManager:
        id: screen_manager

        OTPScreen:
            name: "OTP"
        SMTPScreen:
            name: "SMTP"
        EmailsScreen:
            name: "Emails"
        DatabaseScreen:
            name: "Database"

    MDNavigationBar:
        on_switch_tabs: app.on_switch_tabs(*args)

        BaseMDNavigationItem:
            text: "OTP"
            icon: "lock"
            active: True
        BaseMDNavigationItem:
            text: "SMTP"
            icon: "email-fast"
        BaseMDNavigationItem:
            text: "Emails"
            icon: "email-open"
        BaseMDNavigationItem:
            text: "Database"
            icon: "database"
'''


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class OTPScreen(MDScreen):
    """A custom screen with a label and a send button."""
    pass


class SMTPScreen(MDScreen):
    """A custom screen for SMTP configuration with input fields."""
    pass


class EmailsScreen(MDScreen):
    """A custom screen for configuring the recipient email address."""
    pass


class DatabaseScreen(MDScreen):
    """A custom screen for database configuration."""
    pass


class Example(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        """Called when a tab is switched."""
        self.root.ids.screen_manager.current = item_text

    def send_otp(self):
        """A placeholder function for the send button's action."""
        print("Send button pressed, OTP logic would go here.")

    def save_smtp_settings(self, email, password):
        """A placeholder function for the save button's action."""
        print(f"Saving SMTP settings. Email: {email}, Password: {'*' * len(password)}")

    def save_recipient_email(self, email):
        """A placeholder function for saving the recipient's email address."""
        print(f"Saving recipient email for OTP: {email}")

    def save_database_settings(self, servername, dbname, username, password):
        """A placeholder for saving the database connection details."""
        print(f"Saving Database settings. Server: {servername}, DB: {dbname}, User: {username}, Pass: {'*' * len(password)}")


Example().run()
