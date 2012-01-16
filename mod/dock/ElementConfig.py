from __init__ import *
from mod.fct.mod_file import get_name

class ElementConfig(qt.QWidget, IWidget):
	elements = []
	
	class Element:
		def __init__(__):
			__.name = ""
			__.width = 32
			__.height = 32
			__.image = ""
	
	def __init__(__, master):
		__.master = master
		__.obj = None
		__.edit_mode = False
		qt.QWidget.__init__(__)
		IWidget.__init__(__)
	
	def init_widget(__):
		__.name = qt.QLineEdit()
		__.width = qt.QLineEdit()
		__.height =qt.QLineEdit()
		__.image = qt.QPushButton()
		__.image.path = ""
		__.ok = qt.QPushButton("OK")
		
	def init_layout(__):
		__.layout = qt.QFormLayout()
		__.layout.addRow("name:", __.name)
		__.layout.addRow("width:", __.width)
		__.layout.addRow("height:", __.height)
		__.layout.addRow("image:", __.image)
		__.layout.addWidget(__.ok)
	
	def init_connect(__):
		qt.qApp.connect(__.ok, qt.SIGNAL("clicked()"), __.slot_save)
		qt.qApp.connect(__.image, qt.SIGNAL("clicked()"), __.slot_image)
		
	def slot_save(__):
		if __.name.text() == "" or __.image.path == "" or\
			not __.width.text().toInt()[1] or not __.height.text().toInt()[1]:
			return
		if __.edit_mode == False:
			for i in __.master.elements:
				if i.name == __.name.text():
					return
		__.obj.name = __.name.text()
		__.obj.width = __.width.text().toInt(10)[0]
		__.obj.height = __.height.text().toInt(10)[0]
		__.obj.image = __.image.path
		__.master.addElement(__.obj)
	
	def slot_image(__):
		path = qt.QFileDialog.getOpenFileName(__, "Load an image", ELEMENT_PATH)
		__.image.path = get_name(path)
		__.image.setText(__.image.path)
	
	def add(__):
		__.edit_mode = False
		qt.QWidget.setVisible(__, True)
		__.obj = __.Element()
		__.name.setText("")
		__.width.setText("")
		__.height.setText("")
		__.image.setText("")
		__.image.path = ""

	def edit(__, id):
		__.edit_mode = True
		qt.QWidget.setVisible(__, True)
		__.obj = __.master.elements[id]
		__.name.setText(__.obj.name)
		__.width.setText(str(__.obj.width))
		__.height.setText(str(__.obj.height))
		__.image.setText(get_name(__.obj.image))
		__.image.path = __.obj.image
