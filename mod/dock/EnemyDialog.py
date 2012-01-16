from DockEnemy import *

class EnemyDialog(qt.QDialog):
	def __init__(__):
		qt.QDialog.__init__(__)
		__.setWindowTitle("Select an enemy")
		__.select = -1
		__.list = qt.QListWidget()
		for i in DockEnemy.enemies:
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
