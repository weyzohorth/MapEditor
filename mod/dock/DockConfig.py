from __init__ import *

class DockConfig(ADock):
	def init_widget(__):
		__.map_length = qt.QLineEdit(str(DEFAULT_MAP_LENGTH))
	
	def init_layout(__):
		__.layout = qt.QFormLayout()
		__.layout.addRow("longueur:",  __.map_length)

	def length(__):
		return int(__.map_length.text())
	
	def setLength(__, maplength):
		__.map_length.setText(str(maplength))
