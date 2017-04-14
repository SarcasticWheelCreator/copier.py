#!/usr/bin/env python3
#coding = utf-8

import shutil
import sys
import argparse
from os.path import join, exists, splitext

try:		
	import xml.etree.cElementTree as xml_tree
except ImportError:
	import xml.etree.ElementTree as xml_tree

manual = "ecopier.py - extended version of copier.py.\nXml - file must be in Utf-8 encoding!\n"

def create_arguments_parser():
	parser = argparse.ArgumentParser(description = manual)
	parser.add_argument("filename", help = "path to xml-configure file")
	parser.add_argument("-f", "--forced", action = "store_true", default = False, help = "In case of conflict script will rewrite file with the same name, and won't rename a copy.")
	parser.add_argument("-v", "--verbose", action = "store_true", default = False, help =  "Script generates more verbouse output.")
	parser.add_argument("-s", "--save-metadata", dest = "metadata", action = "store_true", default = False, help = "Script copies files, saving it's metadata like file permittions and so on (this attribure works correct only on UNIX systems).")
	return parser


def break_programm(msg, code = 0):
	print(msg)
	sys.exit(code)
	
def copy_by_config(namespace):
	
	xml_parser = xml_tree.XMLParser(encoding = "utf-8")
	try:
		tree = xml_tree.parse(namespace.filename, xml_parser)
	except IOError as IOErr:
		break_programm(IOErr, 1)
		
	#		Обход xml-файла		#
	
	root = tree.getroot()
	error_counter = copied_files = 0 
	for file in  root:
		old_path = join(file.find("oldpath").text, file.find("filename").text)
		if not exists(old_path):
			if namespace.verbose:
				print("Error - no such file \"%s\" %s" % (old_path, file.attrib))
			error_counter += 1
			continue
		new_path = join(file.find("newpath").text, file.find("filename").text)
		
		#		Защита от затирания файла с таким же именем		#
		if not namespace.forced:
			if exists(new_path):
				number = 1
				fname, fext = splitext(new_path)
				while( exists(fname + str(number) + fext) ):
					number += 1
				new_path = fname + str(number) + fext
		try:
			if namespace.metadata:
				shutil.copy2(old_path, new_path)
			else:
				shutil.copyfile(old_path, new_path)
		except IOError as IOErr:
			if namespace.verbose:
				print("Error when copying file \"%s\" to \"%s\" %s:\n%s" % (old_path, new_path, file.attrib, IOErr))
			error_counter += 1
			continue
		copied_files += 1
		if namespace.verbose:
			print("File \"%s\" was successfully copied to \"%s" % (old_path, new_path))
	print("Copied files: %d\nErrors: %d" % ( copied_files, error_counter))

if __name__ == "__main__":
	parser = create_arguments_parser()
	copy_by_config(parser.parse_args())	