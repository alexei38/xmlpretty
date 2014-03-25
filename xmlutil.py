#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom.minidom import parseString, parse, _write_data, Node, _get_StringIO, Text, Comment, Element, DocumentType, parseString
import sys, os

file_path = None

def writexml_doctype(self, writer, indent="", addindent="", newl=""):
    writer.write("<!DOCTYPE ")
    writer.write(self.name)
    if self.publicId:
        writer.write("%s PUBLIC \"%s\"%s  \"%s\""
                     % (newl, self.publicId, '', self.systemId))
    elif self.systemId:
        writer.write("%s SYSTEM \"%s\"" % ('', self.systemId))
    if self.internalSubset is not None:
        writer.write(" [")
        writer.write(self.internalSubset)
        writer.write("]")
    writer.write(">"+newl)

def writexml_text(self, writer, indent="", addindent="", newl=""):
    _write_data(writer, "%s%s%s" % ('', self.data.strip(), newl))

def writexml_comment(self, writer, indent="", addindent="", newl=""):
    if "--" in self.data:
        raise ValueError("'--' is not allowed in a comment node")
    if self.data.strip():
        if self.data.strip() == '-':
            data = 'UNSUPPORTCOMMENT'
        else:
            data = self.data.strip()
        writer.write("%s<!--%s-->%s" % (indent, data, newl))

def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    # indent = current indentation
    # addindent = indentation to add to higher levels
    # newl = newline string
    writer.write(indent+"<" + self.tagName)

    attrs = self._get_attributes()
    a_names = attrs.keys()
    a_names.sort()

    for a_name in a_names:
        if len(a_names) > 1:
            writer.write(newl)
            writer.write(indent)
            data_indent = "    "
        else:
            data_indent = " "
        writer.write("%s%s=\"" % (data_indent, a_name))
        _write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 and self.childNodes[0].nodeType == Node.TEXT_NODE:
            writer.write(">")
            if len(a_names) > 1:
                writer.write(newl)
                writer.write(indent+addindent)
            self.childNodes[0].writexml(writer, "", "", "")
            if len(a_names) > 1:
                data_newl = newl
                data_indent = indent
            else:
                data_newl = ''
                data_indent = ''
            writer.write("%s%s</%s>%s" % (data_newl, data_indent, self.tagName, newl))
            return
        writer.write(">%s"%(newl))
        for node in self.childNodes:
            node.writexml(writer,indent+addindent,addindent,newl)
        writer.write("%s</%s>%s" % (indent,self.tagName,newl))
    else:
        writer.write("/>%s"%(newl))

Element.writexml = fixed_writexml
DocumentType.writexml = writexml_doctype
Comment.writexml = writexml_comment
Text.writexml = writexml_text

def pretty_parse(file):
    try:
        dom_file = parse(file)
    except:
        sys.stdout.write("Pass formatting xml for file %s\n" % file)
        return 0
    xml_text = dom_file.toxml(encoding ='UTF-8')
    try:
        dom_text = parseString(xml_text)
    except:
        sys.stdout.write("Pass formatting xml for file %s\n" % file)
        return 0
    pretty_text = dom_text.toprettyxml(encoding ='UTF-8', indent="    ")
    with open(file, 'w') as f:
        f.write(pretty_text)
    f.close

if __name__ == "__main__":
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        os.stderr.write("not found file %s\n" % file_path)
        sys.exit(1)
    pretty_parse(file_path)

