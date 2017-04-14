# copier.py

This script copies files in accordance with xml-configuration file.
Xml - file must be in Utf-8 encoding.

## First implementation:
### copier.py
This script copies file without saving the metadata. If file "/new/path/to/file/filename.ext" exists, 
script creates copy with the name "filenameN.ext", where N - number that guarantee unique filename.

## Second implementation:
### ecopier.py
This script has some control attributes, that allows to regulate its behavior.