from __init__ import *
from DockEnemy import *
from ElementConfig import *

class DockElement(DockEnemy):
	elements = []
	
	class Element:
		def __init__(__):
			__.name = ""
			__.width = 32
			__.height = 32
			__.image = ""
	
	def init_widget(__):
		DockEnemy.init_widget(__)
		__.setTitle("Elements")
		__.config = ElementConfig(__)
		__.config.setVisible(False)

	def addElement(__, e):
		if __.config.edit_mode == False:
			__.elements.append(e)
			__.list.addItem(e.name)
		__.slot_list()
