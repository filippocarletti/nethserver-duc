#!/usr/bin/env python
import xml.etree.ElementTree as ET
tree = ET.parse('tree.xml')
root = tree.getroot()

for child in root:
    if(child.attrib['name'] == 'dev' or child.attrib['name'] == 'selinux'):
        root.remove(child)

for child in root:
    if(child.attrib['name'] == 'sys' or child.attrib['name'] == 'proc'):
        root.remove(child)

tree.write('tree.xml')
