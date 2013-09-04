#!/usr/bin/python
import io
import urllib2
import json
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from lxml import etree

URL = 'http://curiosityrover.com/drives'

route = json.loads( urllib2.urlopen(URL).read() )

pList = ''
for point in route:
    pList = pList + str(point['lon']) + ',' + str(point['lat']) +',1,'

pm = KML.Placemark(
    KML.name('Curiosity traversal'),
    KML.LookAt(
        KML.longitude(route[0]['lon']),
        KML.latitude(route[0]['lat']),
        KML.heading('0'),
        KML.tilt('40'),
        KML.range('2000'),
        GX.altitudeMode('relativeToSeaFloor'),
        ),
    KML.LineStyle(
        KML.color('#00FFFF'),
        KML.width(10)
    ),
    KML.altitudeMode('clampToGround'),
    KML.LineString(KML.extrude('1'), GX.altitudeMode('relativeToSeaFloor'), KML.coordinates(pList))
    )

folder = KML.Folder()
folder.append(pm)

# create a document element with a single label style
kmlobj = KML.kml(
    KML.Document(
        KML.Style(
            KML.LabelStyle( KML.scale(1) ),
            id="big_label"
        )
    )
)
kmlobj.Document.append(folder)

with io.open('MSLRoute.kml','w') as out:
    out.write(unicode(etree.tostring(etree.ElementTree(kmlobj),pretty_print=True)))
