from DockElement import *

class ElementDialog(qt.QDialog):
	def __init__(__, enemy=None):
		qt.QDialog.__init__(__)
		__.select = -1
		__.list = qt.QListWidget()
		if enemy:
			__.setWindowTitle("Delete an element")
			for i in enemy.elements:
				__.list.addItem(i.name)
		else:
			__.setWindowTitle("Add an element")
			for i in DockElement.elements:
				__.list.addItem(i.name)
		__.ok = qt.QPushButton("Ok")
		
		__.layout = qt.QVBoxLayout()
		__.layout.addWidget(__.list)
		__.layout.addWidget(__.ok)
		__.setLayout(__.layout)
		
		qt.qApp.connect(__.ok, qt.SIGNAL("clicked()"), __.accept)
		qt.qApp.connect(__.list, qt.SIGNAL("currentRowChanged(int)"), __.slot_select)
	
	def slot_select(__, select):
		__.select = select
