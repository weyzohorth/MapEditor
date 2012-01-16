from __init__ import *
from mod.fct.mod_file import get_name
from EnemyConfig import *

class DockEnemy(ADock):
	enemies = []
	
	def init_widget(__):
		__.setTitle("Enemies")
		__.setMaximumWidth(250)
		__.config = EnemyConfig(__)
		__.config.setVisible(False)
		__.container = qt.QWidget()
		__.list = qt.QListWidget()
		__.add = qt.QPushButton("Add")
		__.edit = qt.QPushButton("Edit")
		__.delete = qt.QPushButton("Delete")
	
	def init_layout(__):
		__.layout = qt.QVBoxLayout()
		__.layout.addWidget(__.config)
		__.layout.addWidget(__.container)
		
		__.layout_container = qt.QVBoxLayout()
		__.layout_container.addWidget(__.list)
		__.layout_container.addWidget(__.add)
		__.layout_container.addWidget(__.edit)
		__.layout_container.addWidget(__.delete)
		__.container.setLayout(__.layout_container)
	
	def init_connect(__):
		qt.qApp.connect(__.add, qt.SIGNAL("clicked()"), __.slot_add)
		qt.qApp.connect(__.edit, qt.SIGNAL("clicked()"), __.slot_edit)
		qt.qApp.connect(__.delete, qt.SIGNAL("clicked()"), __.slot_delete)
		qt.qApp.connect(__.config, qt.SIGNAL("ok()"), __.slot_list)
	
	def slot_add(__):
		__.container.setVisible(False)
		__.config.setVisible(True)
	
	def slot_add(__):
		__.container.setVisible(False)
		__.config.add()
	
	def slot_edit(__):
		if __.list.count() == 0:
			return
		__.container.setVisible(False)
		__.config.edit(__.list.currentRow())
	
	def slot_delete(__):
		if __.list.count() == 0:
			return
		__.enemies.pop(__.list.currentRow())
		__.list.takeItem(__.list.currentRow())
	
	def slot_list(__):
		__.container.setVisible(True)
		__.config.setVisible(False)
	
	def addEnemy(__, e):
		if __.config.edit_mode == False:
			__.enemies.append(e)
			__.list.addItem(e.name)
		__.slot_list()
	
