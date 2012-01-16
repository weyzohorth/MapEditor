from mod.win.__init__ import *
from Layer import *
from Display import *

class MapDisplay(AMdi):
	def __init__(__, master):
		__.idGraphic = 0
		__.length = 0
		__.lengthGraphic = 0
		AMdi.__init__(__)
		__.master = master
	
	def init_widget(__):
		__.tab = qt.QTabWidget()
		__.tab.setMaximumHeight(80)
		__.tab.setMovable(True)
		__.initCollisionLayer()
		__.tab.addTab(Layer(Layer.EVENT, length=DEFAULT_MAP_LENGTH * DEFAULT_TILE_WIDTH), "Events")
		__.tab.addTab(Layer(Layer.ENEMY, length=DEFAULT_MAP_LENGTH * DEFAULT_TILE_WIDTH), "Enemies")
		
		__.showTab = qt.QPushButton("Hide")
		__.showTab.setMaximumWidth(40)
		
		__.display = Display(__)
		
	
	def init_layout(__):
		__.hlay = qt.QHBoxLayout()
		__.hlay.addWidget(__.tab)
		__.hlay.addWidget(__.showTab)
		__.hlay.setAlignment(__.showTab, qt.Qt.AlignTop)
		
		__.layout = qt.QVBoxLayout()
		__.layout.addLayout(__.hlay)
		__.layout.addWidget(__.display)
	
	def init_connect(__):
		qt.qApp.connect(__.tab.tabBar(), qt.SIGNAL("tabMoved(int, int)"), __.slot_moved)
		qt.qApp.connect(__.tab, qt.SIGNAL("currentChanged(int)"), __.slot_changed)
		qt.qApp.connect(__.showTab, qt.SIGNAL("clicked()"), __.slot_showTab)
	
	def slot_changed(__, x):
		if Layer.field.GRID:
			Layer.field.update()
	
	def slot_moved(__, from_, to):
		i = 0
		while i < __.tab.count():
			if __.tab.tabText(i) == "Collisions":
				__.tab.tabBar().moveTab(i, __.idGraphic)
			elif __.tab.tabText(i) == "Events":
				__.tab.tabBar().moveTab(i, __.idGraphic + 1)
			elif __.tab.tabText(i) == "Enemies":
				__.tab.tabBar().moveTab(i, __.idGraphic + 2)
			elif __.idGraphic <= i:
				__.tab.tabBar().moveTab(i, __.idGraphic - 1)
				i = -1
			i += 1
		for i in range(__.idGraphic):
			__.tab.setTabText(i, str(i + 1))
	
	def slot_showTab(__):
		if __.showTab.text() == "Hide":
			__.showTab.setText("Show")
			__.tab.setMaximumHeight(25)
		else:
			__.showTab.setText("Hide")
			__.tab.setMaximumHeight(80)
		for i in range(__.tab.count()):
			__.tab.widget(i).setVisible(not __.tab.widget(i).isVisible())

	def removeAllGraphicLayer(__):
		i = 0
		while i < __.tab.count():
			if __.tab.widget(i).type != Layer.GRAPHIC:
				i += 1
				break
			widget = __.tab.widget(i)
			__.tab.removeTab(i)
		__.idGraphic = 0
	
	def removeGraphicLayer(__, i):
		if type(i) != type(1):
			i = __.tab.indexOf(i)
		if __.idGraphic <= i:
			return
		__.tab.removeTab(i)
		__.idGraphic -= 1
		length = 0
		lengthGraphic = 0
		for i in range(i, __.idGraphic):
			__.tab.setTabText(i, str(i + 1))
		for i in range(__.idGraphic):
			if length < __.tab.widget(i).mapLength():
				length = __.tab.widget(i).mapLength()
			if lengthGraphic < __.tab.widget(i).mapLength() * __.tab.widget(i).tileWidth():
				lengthGraphic = __.tab.widget(i).mapLength() * __.tab.widget(i).tileWidth()
		if length < __.length:
			__.length = length
			print length
			__.reinitCollisionLayer(length)
		if lengthGraphic < __.lengthGraphic:
			__.lengthGraphic = lengthGraphic
			Layer.field.setFixedWidth(__.lengthGraphic)

	def newGraphicLayer(__, tileSize=(DEFAULT_TILE_WIDTH, DEFAULT_TILE_HEIGHT), length=DEFAULT_MAP_LENGTH):
		__.tab.insertTab(__.idGraphic, Layer(Layer.GRAPHIC, tileSize, __, length), str(__.idGraphic + 1))
		__.tab.setCurrentIndex(__.idGraphic)
		__.idGraphic +=1
		if __.length < length:
			__.length = length
			__.reinitCollisionLayer(length * int((float(tileSize[0] / DEFAULT_TILE_WIDTH)) * 4))
		if __.lengthGraphic < length * tileSize[0]:
			__.lengthGraphic = length * tileSize[0]
			Layer.field.setFixedWidth(__.lengthGraphic)
		return __.tab.widget(__.idGraphic - 1)
	
	def resizeGraphicLayer(__, length):
		layer = __.tab.currentWidget()
		if layer == None or layer.type != Layer.GRAPHIC:
			return
		size = len(layer.map)
		layer.length = length
		layer.config.refresh()
		if length < size:
			layer.map = layer.map[ : length]
		elif size < length:
			for x in range(size, length):
				line = [Tile(Layer.field, (x, y)) for y in range(len(layer.map[0]))]
				layer.map.append(line)
		length = 0
		lengthGraphic = 0
		for i in range(__.idGraphic):
			if length < __.tab.widget(i).mapLength():
				length = __.tab.widget(i).mapLength()
			if lengthGraphic < __.tab.widget(i).mapLength() * __.tab.widget(i).tileWidth():
				lengthGraphic = __.tab.widget(i).mapLength() * __.tab.widget(i).tileWidth()
		if length < __.length or __.length < length:
			__.length = length
			__.reinitCollisionLayer(length)
		if lengthGraphic < __.lengthGraphic or __.lengthGraphic < lengthGraphic:
			__.lengthGraphic = lengthGraphic
			Layer.field.setFixedWidth(__.lengthGraphic)
	
	def initCollisionLayer(__, tileSize=(DEFAULT_TILE_WIDTH / 4, DEFAULT_TILE_HEIGHT / 4)):
		__.tab.addTab(Layer(Layer.COLLISION, tileSize, __, DEFAULT_MAP_LENGTH * tileSize[0]), "Collisions")
	
	def reinitCollisionLayer(__, length, width=DEFAULT_MAP_WIDTH * 4, tileSize=(DEFAULT_TILE_WIDTH / 4, DEFAULT_TILE_HEIGHT / 4)):
		for i in range(2):
			layer = __.tab.widget(__.idGraphic + i + 1)
			layer.length = length * tileSize[0]
			layer.config.refresh()
		layer = __.tab.widget(__.idGraphic)
		layer.length = length
		layer.config.refresh()
		if layer == None:
			return layer
		if length < len(layer.map):
			layer.map = layer.map[ : length]
		if width < len(layer.map[0]):
			for i in range(len(layer.map)):
				layer.map[i][ : width]
		if len(layer.map[0]) < width:
			miss = width - len(layer.map[0])
			for i in range(len(layer.map)):
				for j in range(miss):
					layer.map[i].append(Tile(Layer.field, (i, width - miss + j), True))
		if len(layer.map) < length:
			miss = length - len(layer.map)
			for x in range(miss):
				layer.map.append([Tile(Layer.field, (length - miss + x, y), True) for y in range(width)])
		print "Reinit OK"
		return layer
	
	def currentTileWidth(__):
		return __.tab.currentWidget().config.tileSize_x.text().toInt()[0]
	
	def currentTileHeight(__):
		return __.tab.currentWidget().config.tileSize_y.text().toInt()[0]
	
	def currentVisible(__):
		return __.tab.currentWidget().config.visible.text().toBool()[0]
	
	def selectedTile(__):
		if __.master.tileset == None:
			return None
		return __.master.tileset.selectedTile()
	
	def selectedTileset(__):
		if __.master.tileset == None:
			return None
		return __.master.tileset.selectedTileset()
	
	def tilesets(__):
		if __.master.tileset == None:
			return None
		return [__.master.tileset.tab.widget(i).tileset.tileset for i in range(__.master.tileset.tab.count())]
	
	def currentLayer(__):
		return __.tab.currentWidget()

	
