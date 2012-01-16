from mod.__init__ import *

class Tile:#(qt.QPixmap):
	def __init__(__, parent, coord=(0, 0, DEFAULT_TILE_WIDTH, DEFAULT_TILE_HEIGHT), collision=False):
		#qt.QPixmap.__init__(__)
		#qt.QLabel.__init__(__, parent)
		if collision:
			__.width = DEFAULT_TILE_WIDTH / 4
			__.height = DEFAULT_TILE_HEIGHT / 4
		else:
			__.width = DEFAULT_TILE_WIDTH
			__.height = DEFAULT_TILE_HEIGHT
		if len(coord) == 4:
			__.x, __.y, __.width, __.height = coord
		else:
			__.x, __.y = coord
		#__.x = __.y = 0
		__.id = 0
		if collision:
			__.tileset = False
		else:
			__.tileset = ""
