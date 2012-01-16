from __init__ import *
from dock.tileset.DockTileset import *
from dock.DockConfig import *
from dock.DockEnemy import *
from dock.DockElement import *
from win.MapDisplay import *
from win.NewLayerDialog import *
from win.NewLayerDialog import *
from fct.Map import *

class Win(qt.QWidget):
	PEN	= 0
	FILL	= 1
	
	def __init__(__):
		qt.QWidget.__init__(__)
		__.setWindowTitle("MapEditor")
		
		__.tool = Win.PEN

		__.central = MapDisplay(__)
		__.tileset = DockTileset(__.central)
		#__.config = DockConfig()
		__.enemy = DockEnemy()
		__.tileset.setMaximumWidth(250)
		__.element = DockElement()
		__.enemy.setVisible(False)
		__.element.setVisible(False)
		
		__.menu= qt.QMenuBar()
		__.menu.setFixedHeight(25)
		menu = __.menu.addMenu("File")
		__.a_save = menu.addAction("Save")
		__.a_load = menu.addAction("Load")
		
		menu = __.menu.addMenu("Layer")
		__.a_add = menu.addAction("Add")
		__.a_delete = menu.addAction("Delete")
		menu.addSeparator()
		__.a_resize = menu.addAction("Resize")
		
		menu = __.menu.addMenu("Tileset")
		__.a_addTileset = menu.addAction("Add")
		__.a_deleteTileset = menu.addAction("Delete")
		
		menu = __.menu.addMenu("Tool")
		__.a_pen = menu.addAction("Pen")
		__.a_pen.setCheckable(True)
		__.a_pen.setChecked(True)
		__.a_fill = menu.addAction("Fill")
		__.a_fill.setCheckable(True)
		__.group = qt.QActionGroup(__)
		__.group.addAction(__.a_pen)
		__.group.addAction(__.a_fill)
		__.group.setExclusive(True)
		
		
		menu = __.menu.addMenu("Display")
		__.a_grid = menu.addAction("Grid")
		__.a_grid.setCheckable(True)
		menu.addSeparator()
		__.a_tileset = menu.addAction("Tileset")
		__.a_tileset.setCheckable(True)
		__.a_tileset.setChecked(True)
		__.a_enemy = menu.addAction("Enemy")
		__.a_enemy.setCheckable(True)
		__.a_enemy.setChecked(False)
		__.a_element = menu.addAction("Element")
		__.a_element.setCheckable(True)
		__.a_element.setChecked(False)
		
		__.init_layout()
		__.init_connect()
	
	def init_layout(__):
		__.layout = qt.QGridLayout()
		__.layout.addWidget(__.menu, 0, 0, 1, 6)
		__.layout.addWidget(__.tileset, 1, 0, 4, 1)
		#__.layout.addWidget(__.config, 3, 0, 2, 1)
		__.layout.addWidget(__.central, 1, 1, 4, 4)
		__.layout.addWidget(__.enemy, 1, 5, 2, 1)
		__.layout.addWidget(__.element, 3, 5, 2, 1)
		__.setLayout(__.layout)
		
	def init_connect(__):
		qt.qApp.connect(__.a_save, qt.SIGNAL("triggered()"), __.slot_save)
		qt.qApp.connect(__.a_load, qt.SIGNAL("triggered()"), __.slot_load)
		qt.qApp.connect(__.a_add, qt.SIGNAL("triggered()"), __.slot_add)
		qt.qApp.connect(__.a_delete, qt.SIGNAL("triggered()"), __.slot_delete)
		qt.qApp.connect(__.a_resize, qt.SIGNAL("triggered()"), __.slot_resize)
		qt.qApp.connect(__.a_addTileset, qt.SIGNAL("triggered()"), __.slot_addTileset)
		qt.qApp.connect(__.a_deleteTileset, qt.SIGNAL("triggered()"), __.slot_deleteTileset)
		qt.qApp.connect(__.a_tileset, qt.SIGNAL("toggled(bool)"), __.slot_tileset)
		qt.qApp.connect(__.a_enemy, qt.SIGNAL("toggled(bool)"), __.slot_enemy)
		qt.qApp.connect(__.a_element, qt.SIGNAL("toggled(bool)"), __.slot_element)
		qt.qApp.connect(__.a_grid, qt.SIGNAL("toggled(bool)"), __.slot_grid)
		qt.qApp.connect(__.group, qt.SIGNAL("triggered(QAction *)"), __.slot_tool)
	
	def slot_save(__):
		Map(__.central, "test").save()
	
	def slot_load(__):
		Map(__.central, "test").load()
	
	def slot_add(__):
		dialog = NewLayerDialog()
		if dialog.exec_() == qt.QDialog.Accepted:
			size = dialog.size.text().toInt()[0]
			w = dialog.tile_w.text().toInt()[0]
			h = dialog.tile_h.text().toInt()[0]
			if not size or not w or not h:
				return
			__.central.newGraphicLayer((w, h), size)
	
	def slot_delete(__):
		__.central.removeGraphicLayer(__.central.tab.currentWidget())

	def slot_resize(__):
		layer = __.central.tab.currentWidget()
		if layer == None:
			return
		dialog = NewLayerDialog(layer.mapLength(), (layer.tileWidth(), layer.tileHeight()), True)
		if dialog.exec_() == qt.QDialog.Accepted:
			size = dialog.size.text().toInt()[0]
			if not size:
				return
			__.central.resizeGraphicLayer(size)
	
	def slot_addTileset(__):
		__.tileset.slot_open()
	
	def slot_deleteTileset(__):
		__.tileset.slot_delete()
	
	def slot_tileset(__, visible):
		__.tileset.setVisible(visible)
	
	def slot_enemy(__, visible):
		__.enemy.setVisible(visible)
	
	def slot_element(__, visible):
		__.element.setVisible(visible)
	
	def slot_tool(__, action):
		if action.text() == "Pen":
			__.tool = Win.PEN
		elif action.text() == "Fill":
			__.tool = Win.FILL

	def slot_grid(__, grid):
		import mod.win.Layer as layer
		import mod.win.Field as field
		field.Field.GRID = grid
		layer.Layer.field.update()
