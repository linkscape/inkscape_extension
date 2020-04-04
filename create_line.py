#!/usr/bin/env python 
'''
This extension Create a clipping layer

Copyright (C) 2020 Linkscape
(this is the modified program of the EraserLayer,
Copyright (C) 2012 Jabiertxo Arraiza, jabier.arraiza@marker.es)
--4/4 first!!


\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

import inkex, sys, simplestyle, copy
from lxml import etree

class CreateLine(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self) 
        
        
    def write(self,text):
        path_w = 'C:\Users\owner\inkscapelog.txt'
        with open(path_w, mode='a') as f:
            f.write("\n##################\n")
            f.write(str(text))
        
    def getCurrent(self,svg):
        xpathStr = '//sodipodi:namedview'
        namedview = svg.xpath(xpathStr, namespaces=inkex.NSS)
        #get current layer method
        idLayer = namedview[0].get('{http://www.inkscape.org/namespaces/inkscape}current-layer');
        return idLayer;
    
    def CheckStartWith(self, obj, strlist):
        for str in strlist:
            if obj.startswith(str) == True:
                return False
        return True;
            

    ##crea el grupo contenedor que hara de borrador
    def createNewObj(self, obj):
        for position, item in enumerate(obj.getparent().getchildren()):
            if item == obj:
                break;
        newNode = copy.deepcopy(obj)
        newNode.set("style","fill:#000000")
        obj.getparent().insert(position,newNode)

    def effect(self):
        saveout = sys.stdout
        sys.stdout = sys.stderr
        svg = self.document.getroot()
        #get current layer method
        idLayer = self.getCurrent(svg);
        for id, node in self.selected.iteritems():
            self.write(node)
            self.createNewObj(node)
        sys.stdout = saveout
        
effect = CreateLine()
effect.affect()
