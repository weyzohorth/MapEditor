from sys import argv
from PyQt4 import Qt as qt

DATA_PATH	= "../"
TILESET_PATH	= DATA_PATH + "images_for_tests/"
MAP_PATH	= DATA_PATH + "map/"
ENEMY_PATH 	= DATA_PATH + "/sprites-rtype/"
ELEMENT_PATH	= DATA_PATH + "/sprites-rtype/"
CORE_PATH	= DATA_PATH + "/Mobs/"
EVENT_PATH	= DATA_PATH + "/"

#DATA_PATH		= "data/"
#TILESET_PATH	= DATA_PATH + "tileset/"
#MAP_PATH			= DATA_PATH + "map/"
#ENEMY_PATH 		= DATA_PATH + "/sprite/enemy/"
#ELEMENT_PATH	= DATA_PATH + "/sprite/element/"
#CORE_PATH		= DATA_PATH + "/core/"
#EVENT_PATH		= DATA_PATH + "/event/"
DEFAULT_MAP_LENGTH	= 100
DEFAULT_MAP_WIDTH	= 30
DEFAULT_TILE_WIDTH	= 16
DEFAULT_TILE_HEIGHT	=	16

class Test(qt.QWidget):
	def __init__(__):
		qt.QWidget.__init__(__)
		winsize = 400
		__.setFixedSize(winsize, winsize)
		__.timer = qt.QTimer()
		__.timer.setSingleShot(False)
		__.timer.setInterval(100)
		
		__.img = qt.QPixmap("data/stainedglass05.jpg")
		size = __.img.size()
		__.nb_tile = 5
		__.tiles = []
		__.w = size.width() / __.nb_tile
		__.h = size.height() / __.nb_tile
		__.ecart = 0
		__.ecart_max = (winsize - __.w * __.nb_tile) / (__.nb_tile - 1)
		__.sens = True
		for x in range(__.nb_tile):
			for y in range(__.nb_tile):
				widget = qt.QLabel(__)
				widget.setPixmap(__.img.copy(__.w*x, __.h*y, __.w, __.h))
				__.tiles.append(widget)
		
		qt.qApp.connect(__.timer, qt.SIGNAL("timeout()"), __.drawtiles)
		__.timer.start()
		
	def drawtiles(__):
		for index, tile in enumerate(__.tiles):
			tile.move((__.w + __.ecart)*(index / __.nb_tile), (__.h + __.ecart)*(index % __.nb_tile))
		if __.sens:
			if __.ecart < __.ecart_max: __.ecart += 1
			else: __.sens = not __.sens
		else:
			if __.ecart > 0: __.ecart -= 1
			else: __.sens = not __.sens

class IWidget:
	def __init__(__):
		__.init_widget()
		__.init_layout()
		__.init_connect()
		__.setLayout(__.layout)
		
	def init_widget(__):
		pass
	def init_layout(__):
		pass
	def init_connect(__):
		pass
