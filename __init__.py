#!/usr/bin/env python3
#####################################################################################################
#	Main application entry point																																										#
#	Only import the main loop class and call all the init stuff, the run the application																											#
#	Creator:		Yves Huguenin																																									#
#	Date:			06.09.2019																																										#
#	Version:		0.1																																													#
#																																																		#
#####################################################################################################
name = "Sagrave"

from vr22		import gestion
try:
	main 	= gestion()
	main.initDatabase()
	main.initApplication()
	main.mainLoop()
except :
	None
