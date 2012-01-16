from mod.__init__ import *

class NewLayerDialog(qt.QDialog):
	def __init__(__, length=DEFAULT_MAP_LENGTH, tilesize=(DEFAULT_TILE_WIDTH, DEFAULT_TILE_HEIGHT), readonly=False):
		qt.QDialog.__init__(__)
		__.setWindowTitle("Add a layer")
		__.size = qt.QLineEdit(str(length))
		__.tile_w = qt.QLineEdit(str(tilesize[0]))
		__.tile_h = qt.QLineEdit(str(tilesize[1]))
		__.ok = qt.QPushButton("OK")
		__.layout = qt.QFormLayout()
		__.layout.addRow("Layout length :", __.size)
		__.layout.addRow("Tiles width :", __.tile_w)
		__.layout.addRow("Tiles height :", __.tile_h)
		if readonly:
			__.tile_w.setEnabled(False)
			__.tile_h.setEnabled(False)
		__.layout.addWidget(__.ok)
		__.setLayout(__.layout)
		qt.qApp.connect(__.ok, qt.SIGNAL("clicked()"), __.accept)
