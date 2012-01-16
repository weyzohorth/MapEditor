from mod.dock.__init__ import *
from mod.fct.mod_file import get_name, get_ext
from Tileset import *

class DockTileset(ADock):
	def __init__(__, config):
		__.config = config
		ADock.__init__(__)
		
	def init_widget(__):
		__.tab = qt.QTabWidget()
		__.layout = qt.QVBoxLayout()
	
	def init_layout(__):
		__.layout.addWidget(__.tab)
	
	def selectedTile(__):
		if __.selectedTileset() == None:
			return None
		return __.selectedTileset().selectedTile()
	
	def selectedTileset(__):
		return __.tab.currentWidget()

	def addTileset(__, tilesetname):
		ext = get_ext(tilesetname)
		__.tab.addTab(Tileset(TILESET_PATH + tilesetname, __.config), get_name(tilesetname)[ : -len(ext) - 1])
	
	def removeAllTileset(__):
		__.tab.clear()

	def slot_open(__):
		file = qt.QFileDialog.getOpenFileName(None, "Ajouter un tileset", TILESET_PATH)
		if file:
			__.addTileset(get_name(file))
	
	def slot_delete(__):
		if 0 <= __.tab.currentIndex():
			__.tab.removeTab(__.tab.currentIndex())
