from PyQt5				import QtWidgets,QtCore, uic
from PyQt5.QtWidgets 	import QApplication,  QTableWidgetItem, QTreeWidgetItem
import pickle



class settings:
	elems = {
		'WANumber':0, 
		'DBHost':'', 
		'DBPort':3306, 
		'DBUser':'', 
		'DBPass':'', 
		'DBdb':''
		}
	fileName	= "settings.pref"
	
	def __init__(self,  theApp):
		self.app 		= theApp
		self.readFile()

	def actionSave(self):
		pt = self.dlg.pref_table
		for i in range(0, len( self.elems) ):
			e = pt.item(i, 0).text()
			self.elems[ e ] = pt.item(i, 1).text()
		self.writeFile()
		
	def showDialog(self):
		self.dlg = uic.loadUi("modal_pref.ui")
		pt = self.dlg.pref_table
		
		pt.setColumnCount( 2 )
		pt.setRowCount( len( self.elems))
		row=0
		for d in self.elems:
			print(d)
			i=QTableWidgetItem(d )
			i.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
			pt.setItem(row, 0,QTableWidgetItem(i ))
			pt.setItem(row, 1,QTableWidgetItem(str( self.elems[d] )))
			row +=1
		
		
		pt.resizeColumnToContents(0)
	#	pt.resizeColumnToContents(1)
		self.dlg.buttonBox.accepted.connect(self.actionSave)

		self.dlg.show()
		ret 	= self.dlg.exec()
		#self.app.exec()
		return ret
		
	def readFile(self):
		theFile		= open( self.fileName,  "rb")
		self.elems 	= pickle.load(  theFile )
		theFile.close()
		
	def writeFile(self):
		theFile		= open( self.fileName,  "wb")
		pickle.dump( self.elems, theFile )
		theFile.close()
