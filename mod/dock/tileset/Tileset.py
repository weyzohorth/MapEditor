from mod.__init__ import *
from mod.win.Tile import *

class Tileset(qt.QWidget):
	class Tileset(qt.QLabel):
		def __init__(__, tileset, parent):
			qt.QLabel.__init__(__, parent)
			__.tileset = tileset
			__.x1 = __.y1 = 0
			__.x2 = DEFAULT_TILE_WIDTH
			__.y2 = DEFAULT_TILE_HEIGHT
			__.master = parent
			__.setPixmap(qt.QPixmap(tileset))
			
			__.selected = qt.QLabel(__)
			__.selected.setFrameStyle(qt.QFrame.WinPanel | qt.QFrame.Raised)
			__.selected.setLineWidth(1)
			__.selected.setPixmap(__.pixmap().copy(0, 0, DEFAULT_TILE_WIDTH, DEFAULT_TILE_HEIGHT))
			__.selected.move(-1, -1)
			__.selected.tileset = tileset
			__.selected.x = 0
			__.selected.y = 0
			__.selected.width = DEFAULT_TILE_WIDTH
			__.selected.height = DEFAULT_TILE_HEIGHT
		
		def event(__, e):
			if e.__class__ is qt.QMouseEvent:
				if e.button() == qt.Qt.LeftButton:
					w = __.master.currentTileWidth()
					h = __.master.currentTileHeight()
					if w == 0 or h == 0:
						return False
					__.x2 = e.x() - e.x() % w
					__.y2 = e.y() - e.y() % h
					if e.type() == qt.QEvent.MouseButtonPress:
						__.x1, __.y1 = __.x2, __.y2
						return True
					if __.x2 < __.x1:
						__.x1, __.x2 = __.x2, __.x1
					if __.y2 < __.y1:
						__.y1, __.y2 = __.y2, __.y1
					__.x2 -= __.x1
					__.y2 -= __.y1
					__.x2 += w
					__.y2 += h
					__.selected.setPixmap(__.pixmap().copy(__.x1, __.y1, __.x2, __.y2))
					__.selected.setGeometry(__.x1 - 1, __.y1 - 1, __.x2 + 2, __.y2 + 2)
					__.selected.x = __.x1 / w
					__.selected.y = __.y1 / h
					__.selected.width = __.x2
					__.selected.height = __.y2
					__.selected.tileset = __.tileset
					return True
			return qt.QLabel.event(__, e)
			
	def __init__(__, tileset, config):
		qt.QWidget.__init__(__)
		__.setMaximumWidth(250)
		__.init_widget(tileset, config)
		__.init_layout()
		__.setLayout(__.layout)
	
	def init_widget(__, tileset,  config):
		__.layout = qt.QVBoxLayout()
		__.tileset = __.Tileset(tileset, config)
		
		__.scrollArea = qt.QScrollArea()
		__.scrollArea.setWidget(__.tileset)
		__.scrollArea.setBackgroundRole(qt.QPalette.Dark)
		
		__.tileSize_layout = qt.QFormLayout()
		__.tileSize_x = qt.QLineEdit("32")
		__.tileSize_y = qt.QLineEdit("32")
	
	def init_layout(__):
		#__.tileSize_layout.addRow("tile width:", __.tileSize_x)
		#__.tileSize_layout.addRow("tile height:", __.tileSize_y)
		
		__.layout.addWidget(__.scrollArea)
		#__.layout.addLayout(__.tileSize_layout)
	
	def selectedTile(__):
		return __.tileset.selected
	
	def tilesetName(__):
		return __.tileset.tileset
