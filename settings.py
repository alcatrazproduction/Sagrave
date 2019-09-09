from PyQt5					import 	QtCore, uic
from PyQt5.QtWidgets 	import   QTableWidgetItem
import pickle

from constant 				import const

class settings:
	elems = [{
		'WANumber':0, 
		'DBHost':'', 
		'DBPort':3306, 
		'DBUser':'', 
		'DBPass':'', 
		'DBdb':'', 
		'Nom':''
		}]
	
	fileName	= "settings.pref"
	
	def __init__(self,  theApp):
		self.app 		= theApp
		self.readFile()

	def actionSave(self):
		pt = self.dlg.pref_table
		self.elems[ self.last -1 ]
		for i in range(0, len( self.elems[ self.last -1 ]) ):
			e = pt.item(i, 0).text()
			self.elems[ self.last -1 ][ e ] = pt.item(i, 1).text()
		self.elems[0] = self.elems[ self.last -1 ]
		self.writeFile()
	
	def actionCombo( self, item ):
		print( item )
		if item == 0:
			i	= len( self.elems )
			e = {
				'WANumber':self.elems[ self.last - 1 ]['WANumber'], 
				'DBHost':self.elems[ self.last - 1 ]['DBHost'], 
				'DBPort':self.elems[ self.last - 1 ]['DBPort'], 
				'DBUser':self.elems[ self.last - 1 ]['DBUser'], 
				'DBPass':self.elems[ self.last - 1 ]['DBPass'], 
				'DBdb':self.elems[ self.last - 1 ]['DBdb'], 
				'Nom':'Nouveau ' + self.elems[ self.last - 1 ][ 'Nom' ]
				}

			self.elems.append( e )
			row = 0
			for d in self.elems[ i ]:
				self.dlg.pref_table.setItem(row, 1,QTableWidgetItem(str( self.elems[ i ][d] )))
				row +=1
			self.dlg.menu.addItem( self.elems[ i ]['Nom'], self.elems[ i ] )
			self.dlg.menu.setCurrentIndex( i+1 )
		else:
			self.last = item
			row = 0
			for d in self.elems[ item - 2 ]:
				self.dlg.pref_table.setItem(row, 1,QTableWidgetItem(str( self.elems[ item - 1 ][d] )))
				print( str( self.elems[ item - 1 ][d] ) )
				row +=1
		
	def showDialog(self):
		self.dlg = uic.loadUi( const.prefDialog )
		pt = self.dlg.pref_table
		me	= self.dlg.menu
		
		pt.setColumnCount( 2 )
		me.addItem('Ajouter une connection...')
		me.insertSeparator(2)
		row=0
		for s	in self.elems:
			if row == 0:
				pt.setRowCount( len( s ))
				for d in s:
					print(d)
					i= QTableWidgetItem(d )
					i.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
					pt.setItem(row, 0,QTableWidgetItem(i ))
					i = QTableWidgetItem(str( s[d] ))
					pt.setItem(row, 1, i)
					row +=1
			else:
				me.addItem( s['Nom'], s )
		self.last	= me.findText( self.elems[0]['Nom'] )
		me.setCurrentIndex( self.last )
	
		
		pt.resizeColumnToContents(0)
		self.dlg.buttonBox.accepted.connect( self.actionSave )
		self.dlg.menu.activated.connect( self.actionCombo )
		self.dlg.show()
		self.dlg.setModal( True )
		ret 	= self.dlg.exec()
		return ret
		
	def readFile(self):
		theFile		= open( self.fileName,  "rb")
		self.elems 	= pickle.load(  theFile )
		theFile.close()
		try:
			if self.elems[0]['Nom'] is None:
				self.elems[0]['Nom'] = self.elems[0]['DBHost'] + ' ' + str( self.elems[0]['WANumber'] )
			
		except:
			print( self.elems )
			newelems = [{
				'WANumber':self.elems['WANumber'], 
				'DBHost':self.elems['DBHost'], 
				'DBPort':self.elems['DBPort'], 
				'DBUser':self.elems['DBUser'], 
				'DBPass':self.elems['DBPass'], 
				'DBdb':self.elems['DBdb'], 
				'Nom':self.elems['DBHost'] + ' ' + str( self.elems['WANumber'] )
				}]
			print( newelems )
			self.elems = newelems
			self.writeFile()
		if len( self.elems ) < 2:
			self.elems.append( self.elems[0] )
			
	def writeFile(self):
		theFile		= open( self.fileName,  "wb")
		pickle.dump( self.elems, theFile )
		theFile.close()
