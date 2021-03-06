#!/usr/bin/env python


# TODO
#
# Read ports from component-ports.txt for the files in etc.
#
#

import sys, os, subprocess


from robocomp_general import config_robocomp
config_information = config_robocomp("/opt/robocomp/share/robocompdsl/robocompdsl_config.json").config


def generateDummyCDSL(path):
	'''
	function to generate CDSL file
	'''
	if os.path.exists(path):
		print "File", path, "already exists.\nExiting..."
	else:
		print "Generating dummy CDSL file:", path
		string = '''import "'''+config_information["pathfiles"]["path2interfaces"]+'''/IDSLs/import1.idsl";
import "'''+config_information["pathfiles"]["path2interfaces"]+'''/IDSLs/import2.idsl";

Component <CHANGETHECOMPONENTNAME>
{
	Communications
	{
		implements interfaceName;
		requires otherName;
		subscribesTo topicToSubscribeTo;
		publishes topicToPublish;
	};
	language Cpp;
	gui Qt(QWidget);
};\n\n'''
		file_name, file_extension = os.path.splitext(path)
		string = string.replace('<CHANGETHECOMPONENTNAME>', file_name)
		open(path, "w").write(string)

correct = True
if len(sys.argv) < 3:
	if len(sys.argv) == 2 and sys.argv[1].endswith(".cdsl"):
		generateDummyCDSL(sys.argv[1])
		sys.exit(0)
	else: correct = False
if not correct:
	print 'Usage:'
	print '\ta) to generate code from a CDSL file:     '+sys.argv[0].split('/')[-1]+'   INPUT_FILE.CDSL   OUTPUT_DIRECTORY'
	print '\tb) to generate a new CDSL file:           '+sys.argv[0].split('/')[-1]+'   NEW_COMPONENT_DESCRIPTOR.CDSL'
	sys.exit(-1)

inputFile  = sys.argv[1]
outputPath = sys.argv[2]


sys.path.append(config_information["pathfiles"]["path2cogapp"])
from cogapp import Cog



from parseCDSL import *
component = CDSLParsing.fromFile(inputFile)

#########################################
# Directory structure and other checks  #
#########################################
def creaDirectorio(directory, force=False):
	''' 
	Function to create directories
	''' 
	if force:
		try:
			shutil.rmtree(directory)  # remove folder and all contains
		except:
			pass
	try:
		print 'Creating', directory,
		os.mkdir(directory)
		print ''
	except:
		if os.path.isdir(directory):
			print '(already existed)'
			pass
		else:
			print '\nCOULDN\'T CREATE', directory
			sys.exit(-1)

def replaceTagsInFile(path):
	'''
	Misc functions
	'''
	i = open(path, 'r')
	text = i.read()
	reps = []
	reps.append(["\n<@@<" ,""])
	reps.append([">@@>\n" ,""])
	reps.append(["<TABHERE>", '\t'])
	reps.append(["<S1>", ' '])
	reps.append(["<S2>", '  '])
	reps.append(["<S4>", '    '])
	for r in reps:
		text = text.replace(r[0], r[1])
	i.close()
	w = open(path, 'w')
	w.write(text)
	w.close()



imports = ''.join( [ imp.split('/')[-1]+'#' for imp in component['imports'] ] )

if component['language'].lower() == 'cpp':
	#
	# Check output directory
	#
	if not os.path.exists(outputPath):
		creaDirectorio(outputPath)
	# Create directories within the output directory
	try:
		creaDirectorio(outputPath+"/bin")
		creaDirectorio(outputPath+"/etc")
		creaDirectorio(outputPath+"/src")
	except:
		print 'There was a problem creating a directory'
		sys.exit(1)
		pass
	#
	# Generate regular files
	#
	files = [ 'CMakeLists.txt', 'DoxyFile', 'README-STORM.txt', 'README.md', 'etc/config', 'src/main.cpp', 'src/CMakeLists.txt', 'src/CMakeListsSpecific.txt', 'src/commonbehaviorI.h', 'src/commonbehaviorI.cpp', 'src/genericmonitor.h', 'src/genericmonitor.cpp', 'src/config.h', 'src/specificmonitor.h', 'src/specificmonitor.cpp', 'src/genericworker.h', 'src/genericworker.cpp', 'src/specificworker.h', 'src/specificworker.cpp', 'src/mainUI.ui' ]

	specificFiles = [ 'src/specificworker.h', 'src/specificworker.cpp', 'src/CMakeListsSpecific.txt', 'src/mainUI.ui', 'src/specificmonitor.h', 'src/specificmonitor.cpp', 'README.md', 'etc/config' ]
	for f in files:
		ofile = outputPath + '/' + f
		if f in specificFiles and os.path.exists(ofile):
			print 'Not overwriting specific file "'+ ofile +'", saving it to '+ofile+'.new'
			ofile += '.new'
		ifile = config_information["pathfiles"]["path2templates"]+"/templateCPP/" + f
		if f != 'src/mainUI.ui' or component['gui'] != 'none':
			print 'Generating', ofile, 'from', ifile
			run = "cog.py -z -d -D theCDSL="+inputFile + " -D theIDSLs="+imports + " -o " + ofile + " " + ifile
			run = run.split(' ')
			ret = Cog().main(run)
			if ret != 0:
				print 'ERROR'
				sys.exit(-1)
			replaceTagsInFile(ofile)
	#
	# Generate interface-dependent files
	#
	for ima in component['implements']:
		if type(ima) == str:
			im = ima
		else:
			im = ima[0]
		if type(im) == type([]):
			im = im[0]
		for f in [ "SERVANT.H", "SERVANT.CPP"]:
			ofile = outputPath + '/src/' + im.lower() + 'I.' + f.split('.')[-1].lower()
			print 'Generating', ofile, ' (servant for', im + ')'
			# Call cog
			run = "cog.py -z -d -D theCDSL="+inputFile  + " -D theIDSLs="+imports + " -D theInterface="+im + " -o " + ofile + " " + config_information["pathfiles"]["path2templates"]+"/templateCPP/" + f
			run = run.split(' ')
			ret = Cog().main(run)
			if ret != 0:
				print 'ERROR'
				sys.exit(-1)
			replaceTagsInFile(ofile)
	for im in component['subscribesTo']:
		if type(im) != type(''):
			im = im[0]
		for f in [ "SERVANT.H", "SERVANT.CPP"]:
			ofile = outputPath + '/src/' + im.lower() + 'I.' + f.split('.')[-1].lower()
			print 'Generating', ofile, ' (servant for', im + ')'
			# Call cog
			theInterfaceStr = im
			if type(theInterfaceStr) == type([]):
				theInterfaceStr = str(';'.join(im))
			run = "cog.py -z -d -D theCDSL="+inputFile  + " -D theIDSLs="+imports + " -D theInterface="+theInterfaceStr + " -o " + ofile + " " + config_information["pathfiles"]["path2templates"]+"/templateCPP/" + f
			#print run
			run = run.split(' ')
			ret = Cog().main(run)
			if ret != 0:
				print 'ERROR'
				sys.exit(-1)
			replaceTagsInFile(ofile)
elif component['language'].lower() == 'python':
	#
	# Check output directory
	#
	if not os.path.exists(outputPath):
		creaDirectorio(outputPath)
	# Create directories within the output directory
	try:
		creaDirectorio(outputPath+"/etc")
		creaDirectorio(outputPath+"/src")
	except:
		print 'There was a problem creating a directory'
		sys.exit(1)
		pass
	#
	# Generate regular files
	#
	files = [ 'CMakeLists.txt', 'DoxyFile', 'README-STORM.txt', 'README.md', 'etc/config', 'src/main.py', 'src/genericworker.py', 'src/specificworker.py', 'src/mainUI.ui' ]
	specificFiles = [ 'src/specificworker.py', 'src/mainUI.ui', 'README.md', 'etc/config' ]
	for f in files:
		if f == 'src/main.py':
			ofile = outputPath + '/src/' + component['name'] + '.py'
		else:
			ofile = outputPath + '/' + f
		if f in specificFiles and os.path.exists(ofile):
			print 'Not overwriting specific file "'+ ofile +'", saving it to '+ofile+'.new'
			ofile += '.new'
		ifile = config_information["pathfiles"]["path2templates"]+"/templatePython/" + f
		print 'Generating', ofile, 'from', ifile
		run = "cog.py -z -d -D theCDSL="+inputFile + " -D theIDSLs="+imports + " -o " + ofile + " " + ifile
		run = run.split(' ')
		ret = Cog().main(run)
		if ret != 0:
			print 'ERROR'
			sys.exit(-1)
		replaceTagsInFile(ofile)
		if f == 'src/main.py': os.chmod(ofile, os.stat(ofile).st_mode | 0111 )
	#
	# Generate interface-dependent files
	#
	for ima in component['implements']+component['subscribesTo']:
		if type(ima) == type(''):
			im = ima
		else:
			im = ima[0]
		for f in [ "SERVANT.PY"]:
			#print (outputPath, im, f)
			ofile = outputPath + '/src/' + im.lower() + 'I.' + f.split('.')[-1].lower()
			print 'Generating', ofile, ' (servant for', im + ')'
			# Call cog
			run = "cog.py -z -d -D theCDSL="+inputFile  + " -D theIDSLs="+imports + " -D theInterface="+im + " -o " + ofile + " " + config_information["pathfiles"]["path2templates"]+"/templatePython/" + f
			run = run.split(' ')
			ret = Cog().main(run)
			if ret != 0:
				print 'ERROR'
				sys.exit(-1)
			replaceTagsInFile(ofile)
else:
	print 'Unsupported language', component['language']




