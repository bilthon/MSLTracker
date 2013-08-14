#!/usr/bin/python
import io
import urllib2
import json
from pykml.factory import KML_ElementMaker as KML
from lxml import etree

URL = 'http://curiosityrover.com/drives'

route = json.loads( urllib2.urlopen(URL).read() )

pList = []
for point in route:
    pm = KML.Placemark(
        KML.name('Sol ' + str(point['sol'])),
        KML.Point(
            KML.coordinates( str(point['lon']) + ',' + str(point['lat']))
            ),
        KML.altitudeMode('clampToGround')
        )
    pList.append(pm)

folder = KML.Folder()
for placemark in pList:
    folder.append(placemark)

# create a document element with a single label style
kmlobj = KML.kml(
    KML.Document(
        KML.Style(
            KML.LabelStyle(
                KML.scale(2)
            ),
            KML.IconStyle(KML.Icon(KML.scale(0.5))),
            id="big_label"
        )
    )
)
kmlobj.Document.append(folder)

with io.open('MSLRoute.kml','w') as out:
    out.write(unicode(etree.tostring(etree.ElementTree(kmlobj),pretty_print=True)))
