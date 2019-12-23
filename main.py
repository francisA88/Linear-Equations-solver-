'''The Simultaneous Linear Equation solver'''

'''There are some things this app can't do yet, like collecting and evaluating like terms. Please try to do those yourself and feed the already arranged equations to the equation entry field.
	It doesn't matter in what order an equation is arranged as long as the like terms in that equation has already been collected and evaluated.

'''
#Author: Francis Ali
#2019.12.14
#Version 0.1

#In case I forget, remove these next two lines
import sys
sys.path.append("/storage/4251-1617/site-packages")
import string
from copy import deepcopy

from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.app import App
from kivy.factory import Factory
from kivy.clock import Clock
#from kivy.graphics import Color, Rectangle

from kivymd.uix.toolbar import MDToolbar as Toolbar
from kivymd.theming import ThemeManager

#Class declarations which are necessary for use in the kv files{{{

class Main(ScreenManager):
	def __init__(self):
		super().__init__()
		
class Group(FloatLayout):
	pass
		
class Lbutton(Button):
	pass

class Keyboard(ScreenManager):
	pass

class SplashScreen(Screen):
	pass

class EqnField(GridLayout):
	n=1
	def __init__(self, **kw):
		super().__init__(**kw)
		self.add_widget(Factory.TopLevelInfoButton())
		for i in range(2):
			self.add_widget(Group())
			
	def add_widget(self, widget, *args):
		super().add_widget(widget, *args)
		if isinstance(widget, FloatLayout):
			for child in widget.children:
				if isinstance(child, Button):
					child.text = "[color=#eeeeee]Eqn %s[/color]"%(str(self.n))
					self.n+=1
	def remove_widget(self, widget):
		super(EqnField, self).remove_widget(widget)
		'''Just to be sure that this part is implemented on only widgets of type Group which technically, inherits the FloatLayout class'''
		if isinstance(widget, FloatLayout):
			self.n -=1

class EqnInput(TextInput, FocusBehavior):
	def __init__(self, **kwarg):
		super().__init__(**kwarg)
		self.bind(on_focus= self.hide)
		self.curcolor = self.cursor_color
		
	def _bind_keyboard(self):
		pass
		
	def hide(self, *arg):
		FocusBehavior.hide_keyboard()
	
	def on_touch_down(self, touch):
		super().on_touch_down(touch)
		
	def _on_textinput_focused(self, tinput, x):
		self.current = tinput
		Clock.schedule_interval(self.checkStillActive, 1/60)
		self.bind(on_touch_down = self.unfocus)
	
	def checkStillActive(self, dt):
		if self.current.focused:
			MyApp.current = self.current
		else: MyApp.current = None
		
	def unfocus(self,x, touch):
		if not self.collide_point(*touch.pos):
			self.focus = False
			#self.cursor_color = 0,0,0,0
#}}}
Builder.load_file("mainlayout.kv")
Builder.load_file("keyboard.kv")
Builder.load_file("eqninput.kv")

class MyApp(App):
	theme_cls = ThemeManager()
	theme_cls.primary_palette = "BlueGray"
	screens = ["main1", "examples", "settings"]
	eqns = []
	def __init__(self, *arg, **kwargs):
		super().__init__(*arg, **kwargs)
		self.main = Main()
		def close(*args, **kws):
			if self.main.current == self.screens[0]:
				Factory.ExitRequest().open()
			else:
				self.main.current = self.screens[self.screens.index(self.main.current)-1]
			return True
	
		Window.bind(on_request_close=close)
		
	def build(self):
		Clock.schedule_interval(self.importSolver, 2)
		return self.main
	
	def importSolver(self, dt):
		global solver
		import solver
		
	def solve(self):
		mat = []
		consts = []
		for eqns in self.eqns:
			mat.append(solver.split(eqns)[:-1])
			consts.append(solver.split(eqns)[-1])
			if type(solver.split(eqns)) == str:
				self.eqns.clear()
				return solver.split(eqns)
		results = solver.EqnSolver(mat, consts).solve()
		try:
			var = "".join(sorted(i for i in self.eqns[0] if i.isalpha()))
			s = zip(var, results)
			l = ""
			for i in s:
				l+="{} = {}\n".format(i[0], i[1])
			self.eqns.clear()
			return l
		except:
			return "Error. No output"


if __name__ == '__main__':
	MyApp().run()
	