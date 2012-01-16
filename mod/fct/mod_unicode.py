#=[site officiel]=======================
#<<<<<mod_unicode by W3YZOH0RTH>>>>>
#=========[http://progject.free.fr/]======

# fonctions
#	encode(unicod)
#		-> str
#	decode(string)
#		-> unicode

def encode(unicod):
    """Convertie une chaine de type unicode en type string"""
    if type(unicod) != type(""): return unicod.encode("cp1252")
    return unicod

def decode(string):
    """Convertie une chaine de type string en type unicode si possible"""
    if type(string) != type(u""): return unicode(string, "cp1252")
    return string