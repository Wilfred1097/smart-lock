from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import (
    MDTabsItemIcon,
    MDTabsItemText,
    MDTabsItem,
)

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    # Your other content here...

    MDTabsPrimary:
        id: tabs
        size_hint_x: 1
        size_hint_y: None
        pos_hint: {"center_x": 0.5, "y": 0}
        tab_width: 'auto'

        MDDivider:

        MDTabsCarousel:
            id: related_content_container
            size_hint_y: None
            height: dp(530)
'''


class Smart_Lock(MDApp):
    def on_start(self):
        tab_data = {
            "lock": "OTP",
            "email": "SMTP",
            "email-open": "Emails",
            "database": "Database",
        }

        for icon_name, tab_name in tab_data.items():
            self.root.ids.tabs.add_widget(
                MDTabsItem(
                    MDTabsItemIcon(
                        icon=icon_name,
                    ),
                    MDTabsItemText(
                        text=tab_name,
                    ),
                )
            )
            self.root.ids.related_content_container.add_widget(
                MDLabel(
                    text=tab_name,
                    halign="center",
                )
            )
        # Switch to the first tab (or whichever tab you prefer)
        self.root.ids.tabs.switch_tab(icon=list(tab_data.keys())[0])
        

    def build(self):
        self.theme_cls.primary_palette = "Magenta"
        return Builder.load_string(KV)


Smart_Lock().run()
