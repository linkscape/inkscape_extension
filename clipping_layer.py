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

import inkex, sys, simplestyle
from lxml import etree

class ClippingLayer(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self) 

    #inserta el flltro que pasa a negro la mascara
    def insertFilter(self, svg):
        return;
        xpathStr = '//filter[@id="Decolorize_0001"]'
        filterElement = svg.xpath(xpathStr, namespaces=inkex.NSS)
        if filterElement == []:
            xpathStr = '//svg:defs'
            defs = svg.xpath(xpathStr, namespaces=inkex.NSS)
            flt = inkex.etree.SubElement(defs[0],inkex.addNS('filter','svg'))
            for k, v in [('id', 'Decolorize_0001'), ('color-interpolation-filters', 'sRGB'),
                        ('height', '100'), ('width', '100'),
                        ('x', '-50'), ('y', '-50')]:
                flt.set(k, v)
            fltColorMatrix = inkex.etree.SubElement(flt,inkex.addNS('feColorMatrix','svg'))
            for k, v in [('id', 'feColorMatrix_0001'),('values','1'), ('in', 'SourceGraphic'),
                        ('type', 'saturate'), ('result', 'result2')]:
                fltColorMatrix.set(k, v)
            fltFlood = inkex.etree.SubElement(flt,inkex.addNS('feFlood','svg'))
            for k, v in [('id', 'feFlood_0001'),('flood-color','rgb(255,255,255)'), ('flood-opacity', '1'),
                        ('result', 'result1')]:
                fltFlood.set(k, v)
            fltComposite = inkex.etree.SubElement(flt,inkex.addNS('feComposite','svg'))
            for k, v in [('id', 'feComposite_0001'),('operator', 'atop'),('in2', 'SourceGraphic')
            ,('k2', '1'),('result', 'result4')]:
                fltComposite.set(k, v)
           
            fltInverse = inkex.etree.SubElement(defs[0],inkex.addNS('filter','svg'))
            for k, v in [('id', 'Inverse_0001'), ('color-interpolation-filters', 'sRGB'),
                        ('height', '100'), ('width', '100'),
                        ('x', '-50'), ('y', '-50')]:
                fltInverse.set(k, v)
            fltColorMatrixInverse = inkex.etree.SubElement(fltInverse,inkex.addNS('feColorMatrix','svg'))
            for k, v in [('id', 'feColorMatrixInverse_0001'),('values','1'),
                        ('type', 'saturate'), ('result', 'fbSourceGraphic')]:
                fltColorMatrixInverse.set(k, v)
            fltColorMatrixInverse = inkex.etree.SubElement(fltInverse,inkex.addNS('feColorMatrix','svg'))
            for k, v in [('id', 'feColorMatrixInverse_0002'),('in','fbSourceGraphic'),
                        ('values', '-1 0 0 0 1 0 -1 0 0 1 0 0 -1 0 1 0 0 0 1 0 ')]:
                fltColorMatrixInverse.set(k, v)

    #Inserta la mascara desde el grupo eraser
    def insertMask(self, idLayer, layer, svg):
        xpathStr = '//mask[@id="MaskEraser_' + idLayer + '"]'
        maskElement = svg.xpath(xpathStr, namespaces=inkex.NSS)
        if maskElement == []:
            xpathStr = '//svg:defs'
            defs = svg.xpath(xpathStr, namespaces=inkex.NSS)
            msk = inkex.etree.SubElement(defs[0],inkex.addNS('clipPath','svg'))
            for k, v in [('id', 'Eraser_' + idLayer), ('clipPathUnits', 'userSpaceOnUse')]:
                msk.set(k, v)
            use = inkex.etree.SubElement(msk,inkex.addNS('use','svg'))
            for k, v in [('id', 'Use_Eraser_' + idLayer), ('{http://www.w3.org/1999/xlink}href',
            "#" + layer.get("id")),('style',"filter:url(#Inverse_0001)")]:
                use.set(k, v)


    ##crea el grupo contenedor que hara de borrador
    def createEraserLayer(self, layer,idLayer):
        container = etree.Element("g")
        container.set("id","ContainerEraserLayer_" + idLayer)
        container.set("{http://www.inkscape.org/namespaces/inkscape}groupmode","layer")
        container.set("{http://www.inkscape.org/namespaces/inkscape}label", "[CE] " + layer[0].get("{http://www.inkscape.org/namespaces/inkscape}label"))
        for position, item in enumerate(layer[0].getparent().getchildren()):
            if item == layer[0]:
                break;
        layer[0].getparent().insert(position+1,container)
        eraser = etree.Element("g")
        eraser.set("id","EraserLayer_" + idLayer)
        eraser.set('style',"filter:url(#Decolorize_0001)")
        eraser.set('transform',"rotate(360)")
        eraser.set("{http://www.inkscape.org/namespaces/inkscape}groupmode","layer") 
        eraser.set("{http://www.inkscape.org/namespaces/inkscape}label", "[E] " + layer[0].get("{http://www.inkscape.org/namespaces/inkscape}label"))
        #
        container.set('clip-path',"url(#Eraser_" + idLayer + ")")
        #layer[0].set('mask',"url(#Eraser_" + idLayer + ")")
        selected = []
        for id, node in self.selected.iteritems():
            eraser.insert(1,node)
        container.insert(1,eraser)

    def effect(self):
        saveout = sys.stdout
        sys.stdout = sys.stderr
        svg = self.document.getroot()
        xpathStr = '//sodipodi:namedview'
        namedview = svg.xpath(xpathStr, namespaces=inkex.NSS)
        idLayer = namedview[0].get('{http://www.inkscape.org/namespaces/inkscape}current-layer');
        if idLayer.startswith("[mask] ") == False and idLayer.startswith("[eraser] ") == False:
            xpathStr = '//svg:g[@id="EraserLayer_'+idLayer+'"]'
            filterElement = svg.xpath(xpathStr, namespaces=inkex.NSS)
            if filterElement == []:
                xpathStr = '//svg:g[@id="'+idLayer+'"]'
                layer = svg.xpath(xpathStr, namespaces=inkex.NSS)
                if layer[0] is not None and layer[0].get("{http://www.inkscape.org/namespaces/inkscape}label") is not None:
                    self.insertFilter(svg)
                    self.insertMask(idLayer, layer[0], svg)
                    self.createEraserLayer(layer,idLayer)
                else:
                    print "Layer not found, Maybe insisde a group?"
            else:
                for id, node in self.selected.iteritems():
                    filterElement[0].insert(1,node)
        sys.stdout = saveout
        
effect = ClippingLayer()
effect.affect()
