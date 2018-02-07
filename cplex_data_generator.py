import xml.etree.ElementTree as ET
import os
import errno
import math
import re
import random

data_path = "cplex_project/data"

def parse_xml(filepath,filename, cap):
    tree = ET.parse(filepath)
    root = tree.getroot()
    nodes = []
    links = []
    demands = []
    for node in root.iter('{http://sndlib.zib.de/network}node'):
        nodes.append({ "name":node.attrib['id'], "x" : float(node[0][0].text) , "y" : float(node[0][1].text)})

    for x in nodes:
        for y in nodes:
            if x != y:
                distance = math.sqrt((x["x"] - y["x"])*(x["x"] - y["x"]) + (x["y"] - y["y"])*(x["y"] - y["y"]))
                cost = int(round(distance * distance))
                links.append({"src" : x["name"], "dst":y["name"], "cost": cost, "cap": cap, "base_topo": 0})

    for link in root.iter('{http://sndlib.zib.de/network}link'):
        for l in links:
            if (l["src"] == link[0].text and l["dst"] == link[1].text) or (l["src"] == link[1].text and l["dst"] == link[0].text):
                l["base_topo"] = 1

    for idx, x in enumerate(nodes):
        for jdx, y in enumerate(nodes):
            if idx != jdx:
                demands.append({"src": x["name"], "dst" : y["name"], "volume" : abs(idx - jdx) * 10})


    file = re.sub('\.xml$', '', filename)
    create_dir(data_path)
    path = data_path + "/" + file + "_" + str(cap) + ".dat"
    save(path,nodes,links,demands)


def save(filepath,nodes,links,demands):
    with open(filepath,"w") as f :
        f.write("Nodes = {")
        for idx, n in enumerate(nodes):
            if idx == len(nodes) - 1:
                f.write("\""+ n["name"] + "\"")
            else:
                 f.write("\""+ n["name"] + "\", ")
        f.write("};\n")
        f.write("Arcs = {")
        for idx, l in enumerate(links):
            if idx == len(links) - 1:
                f.write("<\""+ l["src"] + "\",\""+ l["dst"] + "\"," + str(l["cap"]) + "," + str(l["cost"]) + "," + str(l["base_topo"]) + ">")
            else:
                f.write("<\""+ l["src"] + "\",\""+ l["dst"] + "\"," + str(l["cap"]) + "," + str(l["cost"]) + "," + str(l["base_topo"]) + ">, ")

        f.write("};\n")
        f.write("Demands = {")
        for idx, d in enumerate(demands):
            if idx == len(demands) - 1:
                f.write("<\""+ d["src"] + "\",\""+ d["dst"] + "\"," + str(d["volume"]) + ">")
            else:
                f.write("<\""+ d["src"] + "\",\""+ d["dst"] + "\"," + str(d["volume"]) + ">, ")
        f.write("};\n")

def create_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


for filename in os.listdir("networks"):
    parse_xml('networks/' + filename, filename, 1)
    parse_xml('networks/' + filename, filename, 5)
    parse_xml('networks/' + filename, filename, 10)
