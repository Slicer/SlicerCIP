import sys
import os, sys
from lxml import etree

# Add manually the common folder to the pythonpath
# this_dir = os.path.dirname(os.path.realpath(__file__))
# path = os.path.normpath(this_dir + '/../..')
# sys.path.append(path)
from CIP.logic.geometry_topology_data import *


this_dir = os.path.dirname(os.path.realpath(__file__))     # Directory where this file is contained
xml_file = os.path.join(this_dir, "geometryTopologyData.xml")
xsd_file = os.path.abspath(os.path.join(this_dir, "..", "logic", "GeometryTopologyData.xsd"))


def test_geometry_topology_data_schema():
    """ Validate the current sample xml file (geometryTopologyData.xml) with the current schema
    """
    # Read xml
    with open(xml_file, 'r+b') as f:
        xml = f.read()

    # Validate schema with lxml
    with open(xsd_file, 'r+b') as f:
        xsd = f.read()
    schema = etree.XMLSchema(etree.XML(xsd))
    xmlparser = etree.XMLParser(schema=schema)
    etree.fromstring(xml, xmlparser)


def test_geometry_topology_data_write_read():
    """ Create a GeometryTopology object that must be equal to the one in xml_file.
    It also validates the xml schema against the xsd file
    """
    # Create a new object from scratch
    g = GeometryTopologyData()
    g.num_dimensions = 3
    g.coordinate_system = g.RAS
    g.lps_to_ijk_transformation_matrix = [[-1.9, 0, 0, 250], [0, -1.9, 0, 510], [0, 0, 2, 724], [0, 0, 0, 1]]
    g.spacing = (0.7, 0.7, 0.5)
    g.origin = (180.0, 180.0, -700.5)
    g.dimensions = (512, 512, 600)

    p1 = Point(2, 5, 1, [2, 3.5, 3], description="My desc")
    p1.__id__ = 1
    p1.timestamp = "2015-10-21 04:00:00"
    p1.user_name = "mcfly"
    p1.machine_name = "DELOREAN"
    g.add_point(p1, fill_auto_fields=False)
    p2 = Point(3, 2, 0, [2.0, 1.5, 3.75])
    p2.__id__ = 2
    p2.timestamp = p1.timestamp
    p2.user_name = p1.user_name
    p2.machine_name = p1.machine_name
    g.add_point(p2, fill_auto_fields=False)
    bb1 = BoundingBox(3, 2, 0, [2, 3.5, 3], [1, 1, 4])
    bb1.__id__ = 3
    bb1.timestamp = p1.timestamp
    bb1.user_name = p1.user_name
    bb1.machine_name = p1.machine_name
    g.add_bounding_box(bb1, fill_auto_fields=False)
    bb2 = BoundingBox(2, 5, 1, [2, 3.5, 3], [2.0, 2, 5], description="My desc")
    bb2.__id__ = 4
    bb2.timestamp = p1.timestamp
    bb2.user_name = p1.user_name
    bb2.machine_name = p1.machine_name
    g.add_bounding_box(bb2, fill_auto_fields=False)

    # Get xml representation for the object
    xml = g.to_xml(pretty_print=True)

    # Compare XML output with the example file
    with open(xml_file, 'r+b') as f:
        expectedOutput = f.read()
    assert xml == expectedOutput, "XML generated: " + xml

    # Validate schema with lxml
    with open(xsd_file, 'r+b') as f:
        xsd = f.read()
    schema = etree.XMLSchema(etree.XML(xsd))
    xmlparser = etree.XMLParser(schema=schema)
    etree.fromstring(xml, xmlparser)

    # Make sure that the seed is set to a right value
    g.update_seed()
    assert g.seed_id == 5, "Seed in the object should be 5, while the current value is {}".format(g.seed_id)