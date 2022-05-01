from kivy import platform
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ColorProperty, StringProperty, BooleanProperty, NumericProperty, ListProperty
from kivy.utils import get_color_from_hex
from kivy.uix.textinput import TextInput

from kivymd.app import MDApp
from kivymd.color_definitions import colors
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout


Builder.load_string('''

# kv_start
<CardTextField>
    height: '60dp'
    size_hint_y:None
    size_hint_x:1
    radius: RADIUS
    label_name:'Hi there'
    md_bg_color: [1,1,1,1] if app.theme_cls.theme_style=='Light' else get_color_from_hex("565656")
    label_size:'15sp'
    hint_text:''
    adaptive_height:True
    spacing:'20dp'
    orientation:'vertical'
	md_bg_color: LIGHT_ACCENT_COLOR
    
	MDCard:
        id: card
        height: root.height
        size_hint_y: None
        radius: root.radius
        elevation: 0
        md_bg_color:root.md_bg_color

    MDBoxLayout:
        id: card_box
        padding:(dp(20),0,0,0)if root.icon_left_action is None else (0,0,0,0)
        spacing:'5dp'
        TextInput:
            id: textfield
            size_hint_y:None
            hint_text:root.hint_text
            height: card.height
            background_color:[0,0,0,0]
            font_size:root.text_font_size
            padding:[dp(10),(self.height-self.font_size)/2,0,dp(0)] if not root.icon_left_action\
             else [0,(self.height-self.font_size)/2,0,dp(6)]
            foreground_color: app.theme_cls.primary_dark if app.theme_cls.theme_style=='Light'\
             else app.theme_cls.primary_light
            hint_text_color: root.hint_text_color if root.hint_text_color is not None else [.5,.5,.5,.8]
            cursor_color: app.theme_cls.primary_color
            multiline: root.multiline
            text: root.text
            on_text:
                root.text = self.text
            on_focus:
                root.focus = self.focus
            y: card.y
            center_x: card.center_x
# kv_end
''')


class CardTextField(MDRelativeLayout, ThemableBehavior):
	inactive_color = ColorProperty([.5, .5, .5, .1])
	border_color = ColorProperty([.5, .5, .5, .1])
	active_color = [0, .7, 1, .7]
	focus = BooleanProperty(False)
	text_font_size = StringProperty('17sp')
	hint_text_color = ColorProperty(None)
	text = StringProperty('')
	thickness = NumericProperty(dp(1) if platform == 'android' else dp(1.4))
	hint_text = StringProperty('')
	label_size = StringProperty('20dp')
	label_name = StringProperty('')
	icon_left_action = ListProperty(None)
	multiline = BooleanProperty(False)
	icon_color = ColorProperty([.5, .5, .5, 1])
	icon_right_action = ListProperty(None)
	dark_bg_hex = ""
	icon_font_size = NumericProperty()
	win = True if platform == 'win' else False

	app = None
	c = 0

	def on_icon_left_action(self, instance, icon_list):
		box = self.ids.card_box
		rm = 0
		for inst in box.children:
			if isinstance(inst, TextInput):
				rm = 1
			else:
				if rm:
					box.remove_widget(inst)

		if len(icon_list) and type(icon_list[0]) != list:
			if len(icon_list) == 1:
				self.icon_left = MDIconButton(icon=self.icon_left_action[0], theme_text_color='Custom',
											  text_color=self.icon_color, user_font_size=self.icon_font_size,
											  pos_hint={'center_y': .5})

			else:
				self.icon_left = MDIconButton(icon=self.icon_left_action[0], theme_text_color='Custom',
											  text_color=self.icon_color, user_font_size=self.icon_font_size,
											  pos_hint={'center_y': .5}, on_release=self.icon_left_action[1])
			self.ids.card_box.add_widget(self.icon_left, index=1)
		elif type(icon_list[0]) == list:
			for icons in icon_list:
				if len(icons) == 1:
					self.icon_left = MDIconButton(icon=icons[0], theme_text_color='Custom',
												  text_color=self.icon_color, user_font_size=self.icon_font_size,
												  pos_hint={'center_y': .5})

				else:
					self.icon_left = MDIconButton(icon=icons[0], theme_text_color='Custom',
												  text_color=self.icon_color, user_font_size=self.icon_font_size,
												  pos_hint={'center_y': .5}, on_release=icons[1])
				self.ids.card_box.add_widget(self.icon_left, index=1)

	def on_icon_right_action(self, instance, icon_list):
		if len(icon_list) and type(icon_list[0]) != list:
			if len(icon_list) == 1:
				self.icon_right = MDIconButton(icon=self.icon_right_action[0], theme_text_color='Custom',
											   text_color=self.icon_color, user_font_size=self.icon_font_size,
											   pos_hint={'center_y': .5})

			else:
				self.icon_right = MDIconButton(icon=self.icon_right_action[0], theme_text_color='Custom',
											   text_color=self.icon_color, user_font_size=self.icon_font_size,
											   pos_hint={'center_y': .5}, on_release=self.icon_right_action[1])
			self.ids.card_box.add_widget(self.icon_right)
		elif type(icon_list[0]) == list:
			for icons in icon_list:
				if len(icons) == 1:
					self.icon_right = MDIconButton(icon=icons[0], theme_text_color='Custom',
												   text_color=self.icon_color, user_font_size=self.icon_font_size,
												   pos_hint={'center_y': .5})

				else:
					self.icon_right = MDIconButton(icon=icons[0], theme_text_color='Custom',
												   text_color=self.icon_color, user_font_size=self.icon_font_size,
												   pos_hint={'center_y': .5}, on_release=icons[1])
				self.ids.card_box.add_widget(self.icon_right)

	def on_icon_color(self, instance, color):
		if self.icon_left_action is not None:
			self.icon_left.text_color = color
		if self.icon_right_action is not None:
			self.icon_right.text_color = color

	def on_inactive_color(self, *args):
		self.border_color = self.inactive_color

	def on_text(self, instance, text):
		"""Use this to do what you want"""

	def on_focus(self, instance, focus):
		if self.app is None:
			self.app = MDApp.get_running_app()


		if focus:
			self.border_color = self.active_color
		else:
			self.border_color = self.inactive_color


if __name__ == '__main__':
	class TestCard(MDApp):
		def build(self):
			Window.size = (500, 900)
			return Builder.load_string('''
#: import get_color_from_hex kivy.utils.get_color_from_hex
<CardTextField>
MDScreen:
	CardTextField:
		pos_hint:{"center_y":.5,"center_x":.5}      
		hint_text:"Full Name"     
		''')


	TestCard().run()
