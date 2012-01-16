from mod.__init__ import *
from Layer import *
from mod.fct.mod_file import get_name
from mod.dock.EnemyDialog import *

class Field(qt.QWidget):
	EMPTY			= None
	GRID				= False
	
	def __init__(__, master):
		qt.QWidget.__init__(__)
		__.master = master
		__.setBackgroundRole(qt.QPalette.Dark)
		__.setFixedSize(DEFAULT_MAP_LENGTH * DEFAULT_TILE_WIDTH, DEFAULT_MAP_WIDTH * DEFAULT_TILE_WIDTH)
		if __.EMPTY == None:
			Field.EMPTY = qt.QPixmap()
		__.pixmap = Field.EMPTY
	
	def event(__, e):
		import mod.Win as win
		if e.__class__ is qt.QMouseEvent:
			if e.button() == qt.Qt.LeftButton or e.button() == qt.Qt.RightButton:
				w = __.master.currentTileWidth()
				h = __.master.currentTileHeight()
				if w == 0 or h == 0:
					return False
				__.x2 = e.x() - e.x() % w
				__.y2 = e.y() - e.y() % h
				type = __.master.currentLayer().type
				if e.type() == qt.QEvent.MouseButtonPress:
					__.x1, __.y1 = __.x2, __.y2
					if type == Layer.EVENT:
						__.manageEvent(e)
					elif type == Layer.ENEMY:
						__.manageEnemy(e)
					return True
				if __.x2 < __.x1:
					__.x1, __.x2 = __.x2, __.x1
				if __.y2 < __.y1:
					__.y1, __.y2 = __.y2, __.y1
				__.x2 -= __.x1
				__.y2 -= __.y1
				__.x2 += w
				__.y2 += h
				if type == Layer.GRAPHIC or type == Layer.COLLISION:
					if __.master.selectedTile() == None:
						return True
					tw = __.master.selectedTile().pixmap().width() / w
					th = __.master.selectedTile().pixmap().height() / h
					if __.master.master.tool == win.Win.FILL:
						__.drawFill(e, (__.x1, __.y1), (w, h), (tw, th), type)
					else:
						__.drawPen(e, w, h, tw, th, type)
				return True
		return qt.QWidget.event(__, e)

	def drawPen(__, e, w, h, tw, th, type):
		for x in range(__.x2/ w):
			if len(__.master.currentLayer().map) <= __.x1 / w + x:
					continue
			for y in range(__.y2 / h):
				if len(__.master.currentLayer().map[0]) <= __.y1 / h + y:
					continue
				tile = __.master.currentLayer().map[__.x1 / w + x][__.y1 / h + y]
				if e.button() == qt.Qt.LeftButton:
					if type == Layer.GRAPHIC:
						tile.x = __.master.selectedTile().x + (x % tw) #* w
						tile.y = __.master.selectedTile().y + (y % th) #* h
						tmp = __.master.selectedTileset().tileset.pixmap().width() / w
						tile.id = tile.y * tmp + tile.x
						tile.tileset = __.master.selectedTile().tileset
					else:
						tile.tileset = True
				else:
					if type == Layer.GRAPHIC:
						tile.x = 0
						tile.y = 0
						tile.tileset = ""
					else:
						tile.tileset = False
				tile.width = w
				tile.width = h
				__.repaint(qt.QRegion((__.x1 / w + x) * w, (__.y1 / h + y) * h, w, h))
	
	def drawFill(__, e, (x, y), (w, h), (tw, th), type, rec=10):
		if not rec:
			return
		rec -= 1
		ref = __.master.currentLayer().map[x / w][y / h]
		id = ref.id
		tileset = ref.tileset[:]
		__.x1 = x
		__.y1 = y
		__.drawPen(e, w, h, tw, th, type)
		if 0 <= x / w - tw:
			tile = __.master.currentLayer().map[x / w - tw][y / h]
			if tile.id == id and tile.tileset == tileset:
				__.drawFill(e, (x - tw * w, y), (w, h), (tw, th), type, rec)
		if x / w + tw < len(__.master.currentLayer().map):
			tile = __.master.currentLayer().map[x / w + tw][y / h]
			if tile.id == id and tile.tileset == tileset:
				__.drawFill(e, (x + tw * w, y), (w, h), (tw, th), type, rec)
		if 0 <= y / h - th:
			tile = __.master.currentLayer().map[x / w][y / h - th * h]
			if tile.id == id and tile.tileset == tileset:
				__.drawFill(e, (x, y - th * h), (w, h), (tw, th), type, rec)
		if y / h + th < len(__.master.currentLayer().map[0]):
			tile = __.master.currentLayer().map[x / w][y / h + th]
			if tile.id == id and tile.tileset == tileset:
				__.drawFill(e, (x, y + th * h), (w, h), (tw, th), type, rec)
		
	def paintEvent(__, event):
		painter = qt.QPainter(__)
		v = __.master.display.scrollArea.viewport()
		for i in range(__.master.idGraphic + 1):
			layer = __.master.tab.widget(i)
			w = layer.tileWidth()
			h = layer.tileHeight()
			for x in range(event.rect().width() / w):
				x += event.rect().x() / w
				for y in range(event.rect().height() / h):
					y += event.rect().y() / h
					if not layer.isVisible():
						painter.drawPixmap(event.rect(), Field.EMPTY)
						continue
					if len(layer.map) <= x or len(layer.map[0]) <= y:
						continue
					tile = layer.map[x][y]
					rect = qt.QRect(x * w, y * h, w, h)
					if layer.type == Layer.COLLISION:
						if tile.tileset:
							painter.fillRect(rect, qt.QColor(255, 0, 0, 128))
						else:
							painter.drawPixmap(rect, Field.EMPTY)
					else:
						if tile.tileset == "":
							painter.drawPixmap(rect, Field.EMPTY)
						else:
							for id in range(__.master.master.tileset.tab.count()):
								if __.master.master.tileset.tab.widget(id).tilesetName() == tile.tileset:
									painter.drawPixmap(rect, __.master.master.tileset.tab.widget(id).tileset.pixmap().copy(tile.x * w, tile.y * h, w, h))
									break
			if layer == __.master.currentLayer() and len(layer.map):
				x = len(layer.map) * w
				y = len(layer.map[0]) * h
				brush = qt.QBrush(qt.QColor(30, 30, 30), qt.Qt.Dense5Pattern)
				painter.fillRect(0, y, Layer.field.width(), Layer.field.height() - y, brush)
				painter.fillRect(x, 0, Layer.field.width() - x, Layer.field.height(), brush)
		pens = [qt.QColor("blue"), qt.QColor("red")]
		for i in range(__.master.idGraphic + 1, __.master.tab.count()):
			layer = __.master.tab.widget(i)
			if not layer.isVisible():
				continue
			painter.setPen(pens[i % len(pens)])
			last = -1
			default = event.rect().y() + __.master.display.scrollArea.viewport().y() + 15
			y = default
			for e in layer.list:
				if event.rect().x() + event.rect().width() < e[0]:
					break
				if last <= e[0] and e[0] < last + 100:
					y += 15
				else:
					y = default
				last = e[0]
				if layer.type == Layer.EVENT:
					tmp = default + __.master.display.scrollArea.viewport().height() - 30 - (y - default)
					painter.drawLine(e[0], 0, e[0], tmp)
					painter.drawText(e[0] + 5, tmp, get_name(e[1]))
				else:
					painter.drawLine(e[0], y - 10, e[0], DEFAULT_MAP_WIDTH * DEFAULT_TILE_HEIGHT)
					painter.drawText(e[0] + 5, y, get_name(e[1]))
		print Field.GRID
		if Field.GRID == True:
			__.drawGrid(painter, event)
		painter.end()
	
	def drawGrid(__, painter, event):
		layer = __.master.currentLayer()
		if layer.type != Layer.COLLISION and layer.type != Layer.GRAPHIC:
			return
		w = layer.tileWidth()
		h = layer.tileHeight()
		painter.setPen(qt.QColor("gray"))
		xs = event.rect().x() - event.rect().x() % w
		ys = event.rect().y() - event.rect().y() % h
		default = event.rect().y() + __.master.display.scrollArea.viewport().height()
		for x in range(event.rect().width() / w):
			painter.drawLine(xs + x * w, 0, xs + x * w, default)
		default = event.rect().x() + __.master.display.scrollArea.viewport().width()
		for y in range(event.rect().height() / h):
			painter.drawLine(0, ys + y * h, default, ys + y * h)

	def manage(__, e, fct):
		layer = __.master.currentLayer()
		if e.button() == qt.Qt.LeftButton:
			event = fct()
			if event:
				layer.list.append((__.x1, event))
				layer.list.sort()
		elif e.button() == qt.Qt.RightButton:
			dist = -1
			ev = None
			for event in layer.list:
				if dist == -1 or abs(event[0] - __.x1) < dist:
					dist = abs(event[0] - __.x1)
					ev = event
					if dist == 0:
						break
			if 100 < dist:
				return
			layer.list.remove(ev)
		__.update()
	
	def manageEvent(__, e):
		__.manage(e, lambda : qt.QFileDialog.getOpenFileName(__, "Load an event", EVENT_PATH))

	def manageEnemy(__, e):
		def selectEnemy():
			dialog = EnemyDialog()
			if dialog.exec_() == qt.QDialog.Accepted and dialog.select != -1:
				return DockEnemy.enemies[dialog.select].name
			return ""
		__.manage(e, selectEnemy)
		
