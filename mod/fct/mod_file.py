#=[site officiel]================
#<<<<<mod_file by W3YZOH0RTH>>>>>
#=====[http://progject.free.fr/]=
from os import chdir,getcwd,listdir, mkdir, rmdir, remove
from mod_unicode import decode
try:
	import hashlib
	md5_fct = hashlib.md5
	sha_fct = hashlib.sha1
except:
	import md5
	import sha
	md5_fct = md5.new
	sha_fct = sha.new

# fonctions
#	get_name(name)
#		-> unicode
#	get_ext(name)
#		-> unicode
#	get_path(name)
#		-> unicode
#	name_exists(name)
#		-> bool
#	dir_exists(dir)
#		-> bool
#	file_exists(fichier)
#		-> bool
#	is_file(name)
#		-> bool
#	is_dir(name)
#		-> bool
#	try_name(name)
#		-> unicode
#	try_dir(name)
#		-> unicode
#	try_file(name)
#		-> unicode
#	get_dirfile(path = getcwd())
#		-> list
#	get_files(path = getcwd())
#		-> generator
#	get_dirs(path = getcwd())
#		-> generator
#	get_allfiles(path = getcwd())
#		-> generator
#	get_allfiles2(path = getcwd())
#		-> generator
#	get_allpaths(path = getcwd())
#		-> list
#	get_paths(path = getcwd())
#		-> list
#	get_paths2(path = getcwd())
#		-> generator
#	nbr_dirfile(name = getcwd())
#		-> list
#	size_dir(name = getcwd())
#		-> int
#	supprdir(dossier)
#		-> None
#	copydir(dossier_original, dossier_copy)
#		-> None
#	partition_test(parti = "")
#		-> list

# class file(file)
#	read_lines(fichier)
#		-> None
#	size(fichier, close=False)
#		-> int
#	copy(fichier, copy, close=False)
#		-> None
#	set_mode(fichier, mode="rb")
#		-> None


#:::::::::::::::::::::::::::::::::::::::::::::::::
def get_name(name):
	name = decode(name).replace("\\","/")
	if name:
		if name[-1] == "/": name = name[ : -1]
	return name.split("/")[-1]

#:::::::::::::::::::::::::::::::::::::::::::::::::
def get_ext(name):
	name = get_name(decode(name))
	temp = name.split(".")[-1]
	if temp != name: return temp
	else: return ""

#:::::::::::::::::::::::::::::::::::::::::::::::::
def get_path(name):
	if name:
		if name != "/":
			name = decode(name)
			name = name.replace("\\","/")
			if name[-1] == "/": name = name[:-1]
			path = "/".join(name.split("/")[:-1])
			if name[0] == "/" and not path: return "/"
			return path+"/"*bool(path)
		else:	return "/"
	else: return ""

#:::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::
def name_exists(name):
	name = decode(name)
	path = get_path(name)
	if not path: path = getcwd()
	if get_name(name) in listdir(path): return True
	else: return False

#:::::::::::::::::::::::::::::::::::::::::::::::::
def dir_exists(dir):
	if name_exists(dir): return is_dir(dir)
	else: return False

#:::::::::::::::::::::::::::::::::::::::::::::::::
def file_exists(fichier):
	if name_exists(fichier): return is_file(fichier)
	else: return False

#:::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::
def is_file(name):
	if name:
		if name[-1] == "/" or name[-1] == "\\": name = name[ : -1]
		try: file(name).close()
		except: return False
		return True
	return False

#:::::::::::::::::::::::::::::::::::::::::::::::::
def is_dir(name):
	path = getcwd()
	try:chdir(name)
	except: return False
	chdir(path)
	return True

#:::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::
def try_name(name):
	name = decode(name)
	path = get_path(name)
	ext = "."+get_ext(name)
	if ext == ".": ext = ""
	name = get_name(name)
	if ext: name = name[:-len(ext)]
	if path: liste = listdir(path)
	else: liste = listdir(getcwd())
	erreur = 0
	temp = name[:]+ext
	while temp in liste:
		erreur += 1
		temp = name + " ("+str(erreur)+")"+ext
	return path+temp

#:::::::::::::::::::::::::::::::::::::::::::::::::
def try_dir(name):
	path = get_path(name)
	name = get_name(name)
	if path != "" : path += "/"
	erreur =  0
	temp_name = name[:]
	while dir_exists(path + temp_name):
		erreur += 1
		temp_name = name+" ("+str(erreur)+")"

	return path+temp_name

#:::::::::::::::::::::::::::::::::::::::::::::::::
def try_file(name):
	name = decode(name)
	path = get_path(name)
	name = get_name(name)
	ext = "." + get_ext(name)
	if ext != ".": name = name[:-len(ext)]
	else: ext = ""

	erreur = 0
	temp_name = name + ext
	while file_exists(path + temp_name):
		erreur += 1
		temp_name = name+(" ("+str(erreur)+")")+ext

	return path+temp_name


#:::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::
def get_dirfile(path=getcwd()):
	"""path=getcwd() ---> tuple(dirs,files)"""
	if path == "" : path = getcwd()
	path = decode(path)
	if path[-1] != "/" : path += "/"
	dos = listdir(path)
	fichier = []
	dossier = []
	for i in dos :
		if is_file(path + i): fichier.append(i)
		elif is_dir(path + i): dossier.append(i)
	return [dossier,fichier]

#:::::::::::::::::::::::::::::::::::::::::::::::::
def get_files(path=getcwd()):
	"""path=getcwd() ---> generateur(path) ---> files in path"""
	if path == "" : path = getcwd()
	path = decode(path).replace("\\","/")
	if path[-1] != "/" : path += "/"
	files = listdir(path)
	for i in files:
		i = decode(i)
		if is_file(path + i): yield i

#:::::::::::::::::::::::::::::::::::::::::::::::::
def get_dirs(path=getcwd()):
	"""path=getcwd() ---> generateur(dirs)"""
	if path == "" : path = getcwd()
	path = decode(path).replace("\\","/")
	if path[-1] != "/" : path += "/"
	dirs = listdir(path)
	path_start = getcwd()
	for i in dirs:
		i = decode(i)
		if is_dir(path + i): yield i + "/"


#:::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::
def get_allfiles(path=getcwd()):
	if path == "" : path = getcwd()
	path = decode(path)
	for p in get_paths2(path):
		for f in get_files(p) : yield p+f

#:::::::::::::::::::::::::::::::::::::::::::::::::
def get_allfiles2(path=getcwd()):
	"""generateur renvoyant toutes les paths filles du dossier parent"""
	if path == "" : path = getcwd()
	path = decode(path).replace("\\","/")
	if path[-1] != "/" : path += "/"
	dirfile = get_dirfile(path)
	yield (path,dirfile[1])
	for i in dirfile[0]:
		try:
			for d,f in get_allfiles2(path+i):yield (d,f)
		except:
			yield ("erreur",[])


#:::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::
def get_allpaths(path=getcwd()):
	"""retourne toutes les urls du dossier parent (les urls peuvent etre en plusieurs exemplaires)"""
	if path == "" : path = getcwd()
	path = decode(path).replace("\\","/")
	if path[-1] != "/" : path += "/"
	list_path = []
	list_dossiers = [path]
	for i in get_dirs(path):
		i = path + decode(i)
		list_dossiers.append(i)
		recup=get_allpaths(i)
		if recup != []:
			for x in recup: list_dossiers.append(decode(x))

	return list_dossiers

#:::::::::::::::::::::::::::::::::::::::::::::::::
def get_paths(path=getcwd()):
	"""version ameliore de "get_allpaths(), les urls ne sont qu'en un seul exemplaire"""
	if path == "" : path = getcwd()
	path = decode(path)
	p = get_allpaths(path)
	paths = []
	for i in p :
		if i not in paths : paths.append(i)
	return paths

#:::::::::::::::::::::::::::::::::::::::::::::::::
def get_paths2(path=getcwd()):
	"""generateur renvoyant toutes les urls filles du dossier parent"""
	if path == "" : path = getcwd()
	path = decode(path).replace("\\","/")
	if path[-1] != "/" : path += "/"
	yield path
	for i in get_dirs(path):
		try :
			i = decode(i)
			for p in get_paths2(path+i) : yield p
		except :
			yield "erreur"


#:::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::
def nbr_dirfile(name=getcwd()):
	"""path---> [nbr dossiers,nbr fichiers]"""
	nbr_fichier = 0
	nbr_dossier = 0
	p = get_allpaths(name)
	path = []
	for i in p:
		if not path.count(i):
			path.append(i)

	for p in path:
		dirfile = get_dirfile(p)
		nbr_dossier += len(dirfile[0])
		nbr_fichier += len(dirfile[1])

	return [nbr_dossier,nbr_fichier]

#:::::::::::::::::::::::::::::::::::::::::::::::::
def size_dir(name=getcwd()):
	"""nom du dossier ---> taille du dossier"""
	size = 0
	p = get_allpaths(name)
	path = []
	for i in p:
		if not path.count(i):
			path.append(i)

	for p in path:
		fichiers = get_dirfile(p)[1]
		for f in fichiers:
			size += file(p+"/"+f).size()
	return size


#:::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::
def supprdir(dossier):
	"""supprime un dossier, tous ses sous-dossiers et tous les fichiers contenus"""
	dossier = decode(dossier)
	if dossier[-1] != "/" : dossier += "/"
	try:
		dirfile = get_dirfile(dossier)
		for f in dirfile[1]: remove(dossier+f)
		for d in dirfile[0]: supprdir(dossier+d)
		rmdir(dossier)
		return ""
	except Exception, err: return err[-1]

#:::::::::::::::::::::::::::::::::::::::::::::::::
def copydir(dossier_original,dossier_copy):
	"""copie un dossier, tous ses sous-dossiers et tous les fichiers contenus"""
	dossier_original = decode(dossier_original)
	dossier_copy = decode(dossier_copy)
	if dossier_original[-1] != "/": dossier_original += "/"
	if dossier_copy[-1] != "/": dossier_copy += "/"
	try:
		dossier_copy = name_exists(dossier_copy+get_name(dossier_original[:-1]))
		try: mkdir(dossier_copy)
		except Exception, err: print err

		dirfile = get_dirfile(dossier_original)
		for d in dirfile[0]:
			copydir(dossier_original+d,dossier_copy)

		for f in dirfile[1]:
			file(dossier_original+f).copy(dossier_copy+f, true)

		return ""
	except Exception, err: return err[-1]

#:::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::
def partition_test(parti=""):
	"""string="",bool=0 ---> ["partitions",[list_dirs],[list_files]]"""
	partition = []
	if parti == "": parti = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	for i in parti:
		try:
			i = i+":"
			chdir(i)
			partition.append(i)
		except: pass
	return partition

#:::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::
def sum_md5_dir(dir=getcwd()):
	sum = ""
	for i in get_allfiles(dir):
		sum += file(i).sum_md5()
	return md5_fct(sum).hexdigest()

def sum_sha_dir(dir=getcwd()):
	sum = ""
	for i in get_allfiles(dir):
		sum += file(i).sum_sha()
	return sha_fct(sum).hexdigest()

#:::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::
class file(file):
	fichier = ""
	def read_lines(fichier):
		"""generateur(fichier) ---> fichier.ligne puis ferme fichier"""
		for string in fichier: yield string
		fichier.close()

	def size(fichier, close=False, index=0):
		"""nom du fichier ---> taille du fichier en octet"""
		index = fichier.tell()
		fichier.seek(0, 2)
		size = fichier.tell()
		fichier.seek(index)
		return size

	def somme(fichier, close=False, index=0):
		fichier.set_mode("rb")
		if index >= 0: fichier.seek(index)
		somme = 0
		c = fichier.read(1)
		while c:
			somme += ord(c)
			c = fichier.read(1)
		if close: fichier.close()
		else: fichier.seek(0)
		return somme

	def somdif(fichier, close=False, index=0):
		fichier.set_mode("rb")
		if index >= 0: fichier.seek(index)
		somme = 0
		c = fichier.read(1)
		while c:
			x = ord(c)
			if x % 2: somme -= x
			else:	somme += x
			c = fichier.read(1)
		if close: fichier.close()
		else: fichier.seek(0)
		return somme

	def copy(fichier, copy, close=False):
		copy = file(copy, "wb")
		old_pos = fichier.tell()
		old_mode = fichier.mode
		fichier.seek(0)
		fichier.set_mode("rb")
		for i in fichier: copy.write(i)
		copy.close()
		if close: fichier.close()
		else:
			fichier.set_mode(old_mode)
			fichier.seek(old_pos)
	
	def add(add, fichier, close=False):
		fichier = file(fichier, "rb")
		old_mode = add.mode
		add.set_mode("ab")
		for i in fichier: add.write(i)
		fichier.close()
		if close: add.close()
		else: add.set_mode(old_mode)

	def set_mode(fichier, mode="rb"):
		if fichier.mode!= mode:
			name = fichier.name
			fichier.__init__(name, mode)

	def sum_md5(fichier):
		index = fichier.tell()
		fichier.seek(0)
		sum = md5_fct(fichier.read()).hexdigest()
		fichier.seek(index)
		return sum

	def sum_sha(fichier):
		index = fichier.tell()
		fichier.seek(0)
		sum = sha_fct(fichier.read()).hexdigest()
		fichier.seek(index)
		return sum
