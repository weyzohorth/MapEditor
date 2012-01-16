from mod.__init__ import *
from Tile import *

class Layer(qt.QWidget, IWidget):
	field = None
	scrollArea = None
	GRAPHIC		= 0
	COLLISION	= 1
	EVENT		= 2
	ENEMY		= 3
	
	class ConfigLayer(qt.QWidget, IWidget):
		def __init__(__, master, tileSize, size, speed=True):
			__.master = master
			__.tileSize = tileSize
			__.size = size
			__.disp_speed = speed
			qt.QWidget.__init__(__)
			IWidget.__init__(__)
			
		def init_widget(__):
			__.text_tileSize_x = qt.QLabel("Tile width:")
			__.text_tileSize_y = qt.QLabel("Tile height:")
			__.text_visible = qt.QLabel("Visible:")
			__.text_size = qt.QLabel("Length:")
			__.text_speed = qt.QLabel("Speed:")
			__.tileSize_x = qt.QLineEdit(str(__.tileSize[0]))
			__.tileSize_y = qt.QLineEdit(str(__.tileSize[1]))
			__.tileSize_x.setReadOnly(True)
			__.tileSize_y.setReadOnly(True)
			__.visible = qt.QCheckBox()
			__.visible.setCheckState(qt.Qt.Checked)
			__.size = qt.QLineEdit(str(__.size))
			__.size.setReadOnly(True)
			__.speed = qt.QLineEdit(str(0.5))
			if not __.disp_speed:
				__.text_speed.setVisible(False)
				__.speed.setVisible(False)
		
		def init_layout(__):
			__.layout = qt.QHBoxLayout()
			__.layout.addWidget(__.text_visible)
			__.layout.addWidget(__.visible)
			__.layout.addWidget(__.text_tileSize_x)
			__.layout.addWidget(__.tileSize_x)
			__.layout.addWidget(__.text_tileSize_y)
			__.layout.addWidget(__.tileSize_y)
			__.layout.addWidget(__.text_size)
			__.layout.addWidget(__.size)
			__.layout.addWidget(__.text_speed)
			__.layout.addWidget(__.speed)
		
		def init_connect(__):
			qt.qApp.connect(__.visible, qt.SIGNAL("stateChanged(int)"), __.slot_visible)
		
		def slot_visible(__, visible):
			__.emit(qt.SIGNAL("stateChanged(bool)"), bool(visible))
		
		def refresh(__):
			__.size.setText(str(__.master.length))
	
	
	def __init__(__, type, tileSize=(DEFAULT_TILE_WIDTH, DEFAULT_TILE_HEIGHT), master=None, length=DEFAULT_MAP_LENGTH):
		qt.QWidget.__init__(__)
		__.length = length
		__.master = master
		__.tileSize = tileSize
		__.type = type
		IWidget.__init__(__)
		col = False
		if type == Layer.COLLISION:
			col = True
		if type == Layer.GRAPHIC or type == Layer.COLLISION:
			__.map = []
			for x in range(__.length * DEFAULT_TILE_HEIGHT / tileSize[1]):
				line = []
				for y in range(DEFAULT_MAP_WIDTH * DEFAULT_TILE_WIDTH / tileSize[0]):
					tile = Tile(Layer.field, (x, y), col)
					line.append(tile)
				__.map.append(line)
		else:
			__.list = []
	
	def init_widget(__):
		import Field
		if Layer.field == None:
			Layer.field = Field.Field(__.master)
			Layer.field.setFixedSize(DEFAULT_MAP_LENGTH * DEFAULT_TILE_WIDTH,
			                         DEFAULT_MAP_WIDTH * DEFAULT_TILE_HEIGHT)
		__.config = __.ConfigLayer(__, __.tileSize, __.length, bool(__.type == Layer.GRAPHIC))
	
	def init_layout(__):
		__.layout = qt.QVBoxLayout()
		__.layout.addWidget(__.config)
	
	def init_connect(__):
		qt.qApp.connect(__.config, qt.SIGNAL("stateChanged(bool)"), __.slot_visible)
	
	def slot_visible(__, visible):
		#if __.type == Layer.GRAPHIC or __.type == Layer.COLLISION:
		Layer.field.repaint()
	
	def mapLength(__):
		return __.config.size.text().toInt()[0]
		
	def tileWidth(__):
		return __.config.tileSize_x.text().toInt()[0]
	
	def tileHeight(__):
		return __.config.tileSize_y.text().toInt()[0]
	
	def isVisible(__):
		return __.config.visible.isChecked()

