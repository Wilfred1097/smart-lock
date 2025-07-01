import random
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from kivy.clock import Clock
# from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)
from kivymd.uix.fitimage import FitImage
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHintText,
    MDTextFieldLeadingIcon,
)
from secure_storage import SecureStorage

KV = '''
<BaseMDNavigationItem>:
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
            text: "Send OTP"
            halign: "center"
            font_style: "Title"
            adaptive_height: True
            role: "small"

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
            role: "small"

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
            on_release: app.save_smtp_settings()
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
            role: "small"

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
            on_release: app.save_recipient_email()
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
            role: "small"

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
            on_release: app.save_database_settings()
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


class OTPScreen(MDScreen): pass
class SMTPScreen(MDScreen): pass
class EmailsScreen(MDScreen): pass
class DatabaseScreen(MDScreen): pass


class Example(MDApp):
    dialog = None

    def build(self):
        self.storage = SecureStorage()
        return Builder.load_string(KV)

    def on_start(self):
        self.load_all_settings()

    def load_all_settings(self):
        sm_screen = self.root.ids.screen_manager.get_screen('SMTP')
        sm_screen.ids.email_field.text = self.storage.get_value('smtp_email', default='')
        sm_screen.ids.password_field.text = self.storage.get_value('smtp_password', default='', is_encrypted=True)

        em_screen = self.root.ids.screen_manager.get_screen('Emails')
        em_screen.ids.recipient_email_field.text = self.storage.get_value('recipient_email', default='')

        db_screen = self.root.ids.screen_manager.get_screen('Database')
        db_screen.ids.server_field.text = self.storage.get_value('db_server', default='')
        db_screen.ids.dbname_field.text = self.storage.get_value('db_name', default='')
        db_screen.ids.user_field.text = self.storage.get_value('db_user', default='')
        db_screen.ids.db_password_field.text = self.storage.get_value('db_password', default='', is_encrypted=True)
        print("All settings loaded.")

    def show_alert_dialog(self, message, title="Notification", icon="information-outline"):
        """Displays a standard alert dialog with an OK button."""
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            MDDialogIcon(icon=icon),
            MDDialogHeadlineText(text=title),
            MDDialogSupportingText(text=message),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="OK"),
                    style="text",
                    on_release=self.close_dialog,
                ),
            ),
        )
        self.dialog.open()

    def show_progress_dialog(self, message, title="Sending..."):
        """Displays a non-dismissible progress dialog."""
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            MDDialogIcon(icon="clock-outline"),
            MDDialogHeadlineText(text=title),
            MDDialogSupportingText(text=message),
        )
        self.dialog.open()

    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    def on_switch_tabs(self, bar, item, item_icon, item_text):
        self.root.ids.screen_manager.current = item_text

    def send_otp(self):
        """Checks credentials and starts the OTP sending process in a new thread."""
        sender_email = self.storage.get_value('smtp_email')
        password = self.storage.get_value('smtp_password', is_encrypted=True)
        receiver_email = self.storage.get_value('recipient_email')

        if not all([sender_email, password, receiver_email]):
            self.show_alert_dialog(
                "Please configure your SMTP and recipient email settings first.",
                title="Configuration Missing",
                icon="alert-circle-outline"
            )
            return

        # Show the "Sending..." dialog immediately
        self.show_progress_dialog("Please wait while the OTP is being sent to your email.")

        # Run the actual email sending in a separate thread
        threading.Thread(
            target=self._send_otp_thread,
            args=(sender_email, password, receiver_email),
            daemon=True
        ).start()

    def _send_otp_thread(self, sender_email, password, receiver_email):
        """This function runs in a separate thread to avoid freezing the UI."""
        try:
            otp = str(random.randint(100000, 999999))
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "Your One-Time Password"
            body = f"Hello,\n\nYour OTP is: {otp}\n\nThis password is valid for one-time use.\n\nThank you."
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            server.quit()
            
            # Schedule the success dialog to be shown on the main thread
            Clock.schedule_once(lambda dt: self.show_alert_dialog(
                "OTP sent successfully!", icon="check-circle-outline"
            ))

        except Exception as e:
            # Schedule the error dialog to be shown on the main thread
            Clock.schedule_once(lambda dt: self.show_alert_dialog(
                f"Failed to send email.\nError: {e}", title="SMTP Error", icon="close-circle-outline"
            ))

    def save_smtp_settings(self):
        screen = self.root.ids.screen_manager.get_screen('SMTP')
        email = screen.ids.email_field.text
        password = screen.ids.password_field.text
        self.storage.set_value('smtp_email', email)
        self.storage.set_value('smtp_password', password, is_encrypted=True)
        self.show_alert_dialog("SMTP settings saved.", "SMTP Configuration")

    def save_recipient_email(self):
        screen = self.root.ids.screen_manager.get_screen('Emails')
        email = screen.ids.recipient_email_field.text
        self.storage.set_value('recipient_email', email)
        self.show_alert_dialog("Recipient email saved.", "Recipient Configuration")

    def save_database_settings(self):
        screen = self.root.ids.screen_manager.get_screen('Database')
        servername = screen.ids.server_field.text
        dbname = screen.ids.dbname_field.text
        username = screen.ids.user_field.text
        password = screen.ids.db_password_field.text
        self.storage.set_value('db_server', servername)
        self.storage.set_value('db_name', dbname)
        self.storage.set_value('db_user', username)
        self.storage.set_value('db_password', password, is_encrypted=True)
        self.show_alert_dialog("Database settings saved.", "Database Configuration")


# Window.size = (360, 740)
Example().run()
