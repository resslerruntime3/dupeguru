#!/usr/bin/env python
"""
Unit Name: dupeguru.tests.export
Created By: Virgil Dupras
Created On: 2006/09/16
Last modified by:$Author: virgil $
Last modified on:$Date: 2009-05-28 15:22:39 +0200 (Thu, 28 May 2009) $
                 $Revision: 4385 $
Copyright 2004-2006 Hardcoded Software (http://www.hardcoded.net)
"""
import unittest
from xml.dom import minidom
from StringIO import StringIO

from hsutil.testcase import TestCase

from .export import *
from . import export

class TCoutput_columns_xml(TestCase):
    def test_empty_columns(self):
        f = StringIO()
        output_column_xml(f,[])
        f.seek(0)
        doc = minidom.parse(f)
        root = doc.documentElement
        self.assertEqual('columns',root.nodeName)
        self.assertEqual(0,len(root.childNodes))
    
    def test_some_columns(self):
        f = StringIO()
        output_column_xml(f,[('foo',True),('bar',False),('baz',True)])
        f.seek(0)
        doc = minidom.parse(f)
        columns = doc.getElementsByTagName('column')
        self.assertEqual(3,len(columns))
        c1,c2,c3 = columns
        self.assertEqual('foo',c1.getAttribute('display'))
        self.assertEqual('bar',c2.getAttribute('display'))
        self.assertEqual('baz',c3.getAttribute('display'))
        self.assertEqual('y',c1.getAttribute('enabled'))
        self.assertEqual('n',c2.getAttribute('enabled'))
        self.assertEqual('y',c3.getAttribute('enabled'))
    

class TCmerge_css_into_xhtml(TestCase):
    def test_main(self):
        css = StringIO()
        css.write('foobar')
        css.seek(0)
        xhtml = StringIO()
        xhtml.write("""<?xml version="1.0" encoding="utf-8"?>
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <title>dupeGuru - Duplicate file scanner</title>
                <link rel="SHORTCUT ICON" href="/favicon.ico" />
                <link rel="stylesheet" href="../hardcoded.css" type="text/css" />
            </head>
            <body>
            </body>
            </html>""")
        xhtml.seek(0)
        self.assert_(merge_css_into_xhtml(xhtml,css))
        xhtml.seek(0)
        doc = minidom.parse(xhtml)
        head = doc.getElementsByTagName('head')[0]
        #A style node should have been added in head.
        styles = head.getElementsByTagName('style')
        self.assertEqual(1,len(styles))
        style = styles[0]
        self.assertEqual('text/css',style.getAttribute('type'))
        self.assertEqual('foobar',style.firstChild.nodeValue.strip())
        #all <link rel="stylesheet"> should be removed
        self.assertEqual(1,len(head.getElementsByTagName('link')))
    
    def test_empty(self):
        self.assert_(not merge_css_into_xhtml(StringIO(),StringIO()))
    
    def test_malformed(self):
        xhtml = StringIO()
        xhtml.write("""<?xml version="1.0" encoding="utf-8"?>
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">""")
        xhtml.seek(0)
        self.assert_(not merge_css_into_xhtml(xhtml,StringIO()))
    

if __name__ == "__main__":
    unittest.main()