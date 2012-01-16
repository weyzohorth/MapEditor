from __init__ import *
from ElementConfig import *
from mod.fct.mod_file import get_name, get_ext

class EnemyConfig(ElementConfig):
	class Enemy(ElementConfig.Element):
		def __init__(__):
			ElementConfig.Element.__init__(__)
			__.core = ""
			__.elements = []
	
	def __init__(__, master):
		ElementConfig.__init__(__, master)
	
	def init_widget(__):
		ElementConfig.init_widget(__)
		__.core = qt.QPushButton()
		__.core.path = ""
		__.addElement = qt.QPushButton("add element")
		__.delElement = qt.QPushButton("delete element")
		
	def init_layout(__):
		ElementConfig.init_layout(__)
		__.layout.removeWidget(__.ok)
		__.layout.addRow("core:", __.core)
		__.layout.addWidget(__.addElement)
		__.layout.addWidget(__.delElement)
		__.layout.addWidget(__.ok)
	
	def init_connect(__):
		ElementConfig.init_connect(__)
		qt.qApp.connect(__.core, qt.SIGNAL("clicked()"), __.slot_core)
		qt.qApp.connect(__.addElement, qt.SIGNAL("clicked()"), __.slot_addElement)
		qt.qApp.connect(__.delElement, qt.SIGNAL("clicked()"), __.slot_delElement)
		
	def slot_save(__):
		if __.name.text() == "" or\
			not __.width.text().toInt()[1] or not __.height.text().toInt()[1] or \
			not __.core.text():
			return
		if __.edit_mode == False:
			for i in __.master.enemies:
				if i.name == __.name.text():
					return
		__.obj.name = __.name.text()
		__.obj.width = __.width.text().toInt(10)[0]
		__.obj.height = __.height.text().toInt(10)[0]
		__.obj.image = __.image.path
		__.obj.core = __.core.path
		__.master.addEnemy(__.obj)
	
	def slot_image(__):
		path = qt.QFileDialog.getOpenFileName(__, "Load an picture", ENEMY_PATH)
		name = get_name(path)
		__.image.path = name
		__.image.setText(name)
	
	def slot_core(__):
		path = qt.QFileDialog.getOpenFileName(__, "Load an AI", CORE_PATH)
		ext = get_ext(path)
		name = get_name(path)[ : -len(ext) - 1]
		__.core.path = name
		__.core.setText(name)
	
	def add(__):
		ElementConfig.add(__)
		__.obj = __.Enemy()
		__.core.setText("")
		__.core.path = ""

	def edit(__, id):
		__.edit_mode = True
		qt.QWidget.setVisible(__, True)
		__.obj = __.master.enemies[id]
		__.name.setText(__.obj.name)
		__.width.setText(str(__.obj.width))
		__.height.setText(str(__.obj.height))
		__.image.setText(get_name(__.obj.image))
		__.image.path = __.obj.image
		__.core.setText(get_name(__.obj.core))
		__.core.path = __.obj.core
	
	def slot_addElement(__):
		import ElementDialog as ed
		import DockElement as de
		dialog = ed.ElementDialog()
		if dialog.exec_() == qt.QDialog.Accepted and dialog.select != -1:
			for i in __.obj.elements:
				if i.name == de.DockElement.elements[dialog.select].name:
					return
			__.obj.elements.append(de.DockElement.elements[dialog.select])
		
	
	def slot_delElement(__):
		import ElementDialog as ed
		dialog = ed.ElementDialog(__.obj)
		if dialog.exec_() == qt.QDialog.Accepted and dialog.select != -1:
			__.obj.elements.pop(dialog.select)
