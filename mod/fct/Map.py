from mod.__init__ import *
from mod.win.MapDisplay import *
from mod_file import *
from mod.dock.DockElement import *

class Map:
	def __init__(__, master, filename):
		__.master = master
		__.name = filename
		__.tileset_nb_chr = 1
		__.tileset = []
		__.layer = []
		__.collision = []
		__.event = []
		__.enemy = []
	
	def save(__):
		__.name = qt.QFileDialog.getSaveFileName(__.master, "Save the map.", MAP_PATH)
		if not __.name:
			return
		__.file = file(__.name, "w")
		__.save_header()
		__.save_enemydata()
		__.save_layer()
		__.save_event()
		__.save_collision()
		__.save_enemy()
	
	def load(__):
		__.name = qt.QFileDialog.getOpenFileName(__.master, "Load the map.", MAP_PATH)
		if not __.name:
			return
		__.file = file(__.name, "r")
		__.load_header()
		__.load_enemydata()
		__.load_layer()
		__.load_event()
		__.load_collision()
		__.load_enemy()
	
	def load_header(__):
		__.master.length = 0
		__.master.lengthGraphic = 0
		__.file.readline()
		__.length = int(__.file.readline())
		Layer.field.setFixedWidth(0)
		__.length = __.length / DEFAULT_TILE_WIDTH
		__.nb_layer = int(__.file.readline())
		__.master.removeAllGraphicLayer()
		__.nb_char = int(__.file.readline())
		__.master.master.tileset.removeAllTileset()
		for i in range(int(__.file.readline())):
			__.master.master.tileset.addTileset(__.file.readline()[ : -1])
			__.file.readline()
	
	def load_enemydata(__):
		DockEnemy.enemies = []
		DockElement.elements = []
		for i in range(__.master.master.enemy.list.count()):
			__.master.master.enemy.list.takeItem(0)
		for i in range(__.master.master.element.list.count()):
			__.master.master.element.list.takeItem(0)
		nb_enemy = int(__.file.readline())
		nb_element = int(__.file.readline())
		while 0 < nb_enemy:
			nb_enemy -= 1
			new = EnemyConfig.Enemy()
			new.name = __.file.readline()[ : -1]
			new.core = __.file.readline()[ : -1]
			new.image = __.file.readline()[ : -1]
			new.width = int(__.file.readline()[ : -1])
			new.height = int(__.file.readline()[ : -1])
			__.master.master.enemy.addEnemy(new)
			
		while 0 < nb_element:
			nb_element -= 1
			new = ElementConfig.Element()
			new.name = __.file.readline()[ : -1]
			parent = __.file.readline()[ : -1]
			for i in DockEnemy.enemies:
				if i.name == parent:
					i.elements.append(new)
					break
			new.image = __.file.readline()[ : -1]
			new.width = int(__.file.readline()[ : -1])
			new.height = int(__.file.readline()[ : -1])
			__.master.master.element.addElement(new)
	
	def load_layer(__):
		while 0 < __.nb_layer:
			__.nb_layer -= 1
			nb_line = int(__.file.readline()) - 3
			speed = float(__.file.readline())
			w = int(__.file.readline())
			h = int(__.file.readline())
			layer = __.master.newGraphicLayer((w, h), nb_line)
			layer.config.speed.setText(str(speed))
			lines = []
			null = "".join(["0" for i in range(__.nb_char)])
			while 0 < nb_line:
				lines.append(__.file.readline()[ : -1].split(" "))
				nb_line -= 1
			tilesets = __.master.tilesets()
			ymax = len(lines[0])
			if DEFAULT_MAP_WIDTH < ymax:
				ymax = DEFAULT_MAP_WIDTH
			for x in range(len(lines)):
				for yl in range(ymax):
					y = ymax - yl - 1
					print x,  y, len(layer.map), len(layer.map[0])
					cell = layer.map[x][y]
					cell.width = w
					cell.height = h
					if lines[x][yl] == null:
						cell.tileset = ""
						cell.id = 0
						cell.x = 0
						cell.y = 0
					else:
						id_tileset = int(lines[x][yl][ : __.nb_char]) - 1
						cell.id = int(lines[x][yl][__.nb_char : ])
						tilesetWidth = __.master.master.tileset.tab.widget(id_tileset).tileset.pixmap().width() / w
						cell.x = cell.id % tilesetWidth
						cell.y = cell.id / tilesetWidth
						cell.tileset = __.master.master.tileset.tab.widget(id_tileset).tilesetName()
						#cell.setPixmap(__.master.master.tileset.tab.widget(id_tileset).tileset.pixmap().copy(cell.x * w, cell.y * h, w, h))
			layer.slot_visible(True)
	
	def load_event(__):
		layer = __.master.tab.widget(__.master.idGraphic + 1)
		__.load_list(layer)
	
	def load_collision(__):
		nb_line = int(__.file.readline())
		layer = __.master.reinitCollisionLayer(nb_line)
		print __.master.idGraphic
		lines = []
		while 0 < nb_line:
			lines.append(__.file.readline()[ : -1])
			nb_line -= 1
		tilesets = __.master.tilesets()
		print "x", len(layer.map),
		print "y", len(layer.map[0])
		ymax = len(layer.map[0])
		for x in range(len(layer.map)):
			for yl in range(ymax):
				y = ymax - yl - 1
				#print x, yl
				cell = layer.map[x][y]
				if lines[x][yl] == "0":
					cell.tileset = False
					#cell.setPixmap(Layer.field.EMPTY)
				else:
					cell.tileset = True
					#cell.setPixmap(Layer.field.COLLISION)
		layer.slot_visible(False)
		
	def load_enemy(__):
		layer = __.master.tab.widget(__.master.idGraphic + 2)
		__.load_list(layer)
	
	def load_list(__, layer):
		layer.list = []
		nb_line = int(__.file.readline())
		while 0 < nb_line:
			nb_line -= 1
			line = __.file.readline()[ : -1].split(" ")
			nb = int(line[0])
			line = " ".join(line[1 : ])
			layer.list.append((nb, line))

	def save_header(__):
		nb_layer = 0
		for i in range(__.master.tab.count()):
			layer = __.master.tab.widget(i)
			if layer.type == Layer.GRAPHIC:
				nb_layer += 1
		tilesets = __.master.tilesets()
		__.tileset_nb_char = len(str(len(tilesets)))
		buf = str(DEFAULT_MAP_WIDTH * DEFAULT_TILE_HEIGHT) + "\n" + \
				str(__.master.length * DEFAULT_TILE_WIDTH) + "\n" + \
				str(nb_layer) + "\n" + \
				str(__.tileset_nb_char) + "\n" + \
				str(len(tilesets)) + "\n"
		for i, name in enumerate(tilesets):
			buf += get_name(name) + "\n" + str(__.master.master.tileset.tab.widget(i).tileset.pixmap().width()) + "\n"
		__.file.write(buf)
	
	def save_enemydata(__):
		buf = str(len(DockEnemy.enemies)) + "\n" + str(sum([len(i.elements) for i in DockEnemy.enemies])) + "\n"
		for i in DockEnemy.enemies:
			buf += i.name + "\n" + \
				i.core + "\n" + \
				i.image + "\n" + \
				str(i.width) + "\n" + \
				str(i.height) + "\n"
		for e in DockEnemy.enemies:
			for i in e.elements:
				buf += i.name + "\n" + \
					e.name + "\n" + \
					i.image + "\n" + \
					str(i.width) + "\n" + \
					str(i.height) + "\n"
		__.file.write(buf)
	
	def save_layer(__):
		tilesets = __.master.tilesets()
		for i in range(__.master.idGraphic):
			layer = __.master.tab.widget(i)
			if layer.type == Layer.GRAPHIC:
				map = []
				ymax = len(layer.map[0]) - 1
				for x in range(len(layer.map)):
					tmp = []
					for y in range(len(layer.map[0])):
						cell = layer.map[x][ymax - y]
						if cell.tileset == "":
							tmp.append("".join(["0" for i in range(__.tileset_nb_char)]))
						else:
							nb = str(tilesets.index(cell.tileset) + 1)
							nb = "".join(["0" for i in range(__.tileset_nb_char - len(nb))]) + nb
							tmp.append(nb + str(cell.id))
					map.append(tmp)
				buf = str(len(map) + 3) + "\n" + \
						layer.config.speed.text() + "\n" + \
						layer.config.tileSize_x.text() + "\n" + \
						layer.config.tileSize_y.text() + "\n" + \
						"\n".join([" ".join([i for i in line]) for line in map])
				__.file.write(buf + "\n")
		
	def save_event(__):
		layer = __.master.tab.widget(__.master.idGraphic + 1)
		__.save_list(layer)
	
	def save_collision(__):
		for i in range(__.master.tab.count()):
			layer = __.master.tab.widget(i)
			if layer.type == Layer.COLLISION:
				map = []
				ymax = len(layer.map[0]) - 1
				for x in range(len(layer.map)):
					tmp = []
					for y in range(len(layer.map[0])):
						cell = layer.map[x][ymax - y]
						tmp.append(str(int(cell.tileset)))
					map.append(tmp)
				buf = str(len(map)) + "\n" + \
						"\n".join(["".join([i for i in line]) for line in map])
				__.file.write(buf + "\n")
		
	def save_enemy(__):
		layer = __.master.tab.widget(__.master.idGraphic + 2)
		__.save_list(layer)
	
	def save_list(__, layer):
		buf = str(len(layer.list)) + "\n"
		for i in layer.list:
			buf += str(i[0]) + " " + i[1] + "\n"
		__.file.write(buf)

