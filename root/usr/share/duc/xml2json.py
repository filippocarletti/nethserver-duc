#!/usr/bin/env python
"""xml2json.py  Convert XML to JSON

Relies on ElementTree for the XML parsing.  This is based on
pesterfish.py but uses a different XML->JSON mapping.
The XML->JSON mapping is described at
http://www.xml.com/pub/a/2006/05/31/converting-between-xml-and-json.html

Rewritten to a command line utility by Hay Kranen < github.com/hay > with
contributions from George Hamilton (gmh04) and Dan Brown (jdanbrown)

XML                              JSON
<e/>                             "e": null
<e>text</e>                      "e": "text"
<e name="value" />               "e": { "@name": "value" }
<e name="value">text</e>         "e": { "@name": "value", "#text": "text" }
<e> <a>text</a ><b>text</b> </e> "e": { "a": "text", "b": "text" }
<e> <a>text</a> <a>text</a> </e> "e": { "a": ["text", "text"] }
<e> text <a>text</a> </e>        "e": { "#text": "text", "a": "text" }

This is very similar to the mapping used for Yahoo Web Services
(http://developer.yahoo.com/common/json.html#xml).

This is a mess in that it is so unpredictable -- it requires lots of testing
(e.g. to see if values are lists or strings or dictionaries).  For use
in Python this could be vastly cleaner.  Think about whether the internal
form can be more self-consistent while maintaining good external
characteristics for the JSON.

Look at the Yahoo version closely to see how it works.  Maybe can adopt
that completely if it makes more sense...

R. White, 2006 November 6
"""

import json
import optparse
import sys
import os
import ast

import xml.etree.cElementTree as ET

MIN_SIZE = 10000000
COMMAND = '/sbin/e-smith/config getprop backup-data Mount'
size = None


def splitall():
    path = os.popen(COMMAND).read().strip()
    allparts = []

    if(path):
        while 1:
            parts = os.path.split(path)
            if parts[0] == path:  # sentinel for absolute paths
                allparts.insert(0, parts[0])
                break
            elif parts[1] == path: # sentinel for relative paths
                allparts.insert(0, parts[1])
                break
            else:
                path = parts[0]
                allparts.insert(0, parts[1])

    return allparts

def elem_to_internal(elem, strip_ns=1, strip=1):
    """Convert an Element into an internal dictionary (not JSON!)."""

    d = {}
    elem_tag = elem.tag

    for key, value in list(elem.attrib.items()):
        d[key] = value

    for subelem in elem:
        v = elem_to_internal(subelem, strip_ns=strip_ns, strip=strip)
        tag = subelem.tag
        value = v[tag]
        tag = 'children'

        try:
            d[tag].append(value)
        except AttributeError:
            d[tag] = [d[tag], value]
        except KeyError:
            d[tag] = ast.literal_eval('['+str(value)+']')

    return {elem_tag: d}

def recToDelete(elem, backupdirs):
    global size

    if(elem.attrib['name'] == backupdirs[-1]):
        size = int(elem.attrib['size'])
    else:
        for obj in list(elem):
            if(obj.attrib['name'] == backupdirs[-1]):
                size = int(obj.attrib['size'])
                obj.attrib['size'] = str(int(obj.attrib['size']) - size)
                if(int(obj.attrib['size']) < MIN_SIZE):
                    elem.remove(obj)
            else:
                size = recToDelete(obj, backupdirs)
                if(obj.attrib['name'] in backupdirs):
                    obj.attrib['size'] = str(int(obj.attrib['size']) - size)
                    if(int(obj.attrib['size']) < MIN_SIZE):
                        elem.remove(obj)

    return size

def elem2json(elem, options, strip_ns=1, strip=1):

    """Convert an ElementTree or Element into a JSON string."""

    if hasattr(elem, 'getroot'):
        elem = elem.getroot()

    a = splitall()
    if a:
        a = a[1:]
        if(a[-1] == ""):
            a = a[:-1]

        # remove backup dir elem
        for child in elem:
            if(child.attrib['name'] == a[0]):
                size = recToDelete(child, a)
                child.attrib['size'] = str(int(child.attrib['size']) - size)
                if(int(child.attrib['size']) < MIN_SIZE):
                    elem.remove(child)

    # remove fake folder
    for child in elem:
        if( child.attrib['name'] == 'dev' or
            child.attrib['name'] == 'proc' or
            child.attrib['name'] == 'sys' or
            child.attrib['name'] == 'selinux'):
            elem.remove(child)

    if options.pretty:
        return json.dumps(elem_to_internal(elem, strip_ns=strip_ns, strip=strip), sort_keys=True, indent=4, separators=(',', ': '))
    else:
        return json.dumps(elem_to_internal(elem, strip_ns=strip_ns, strip=strip))

def xml2json(xmlstring, options, strip_ns=1, strip=1):

    """Convert an XML string into a JSON string."""

    elem = ET.fromstring(xmlstring)
    return elem2json(elem, options, strip_ns=strip_ns, strip=strip)

def main():
    p = optparse.OptionParser(
        description='Converts XML to JSON or the other way around.  Reads from standard input by default, or from file if given.',
        prog='xml2json',
        usage='%prog [file]'
    )
    p.add_option(
        '--pretty', action="store_true",
        dest="pretty", help="Format JSON output so it is easier to read")

    options, arguments = p.parse_args()

    inputstream = sys.stdin
    if len(arguments) == 1:
        try:
            inputstream = open(arguments[0])
        except:
            sys.stderr.write("Problem reading '{0}'\n".format(arguments[0]))
            p.print_help()
            sys.exit(-1)

    input = inputstream.read()

    strip = 1
    strip_ns = 1
    out = xml2json(input, options, strip_ns, strip)

    print out

if __name__ == "__main__":
    main()
