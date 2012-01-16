from mod.__init__ import *
from Layer import *

class Display(qt.QWidget, IWidget):
	def __init__(__, master):
		qt.QWidget.__init__(__)
		IWidget.__init__(__)
		__.layers = master.tab
		__.master = master

	def init_widget(__):
		__.scrollArea = qt.QScrollArea()
		__.scrollArea.setWidget(Layer.field)
		__.scrollArea.setBackgroundRole(qt.QPalette.Shadow)
	
	def init_layout(__):
		__.layout = qt.QVBoxLayout()
		__.layout.addWidget(__.scrollArea)
	
	def init_connect(__):
		qt.qApp.connect(__.scrollArea.horizontalScrollBar(), qt.SIGNAL("sliderReleased()"), Layer.field.update)
		qt.qApp.connect(__.scrollArea.verticalScrollBar(), qt.SIGNAL("sliderReleased()"), Layer.field.update)
		

