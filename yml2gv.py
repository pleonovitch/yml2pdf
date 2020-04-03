#!/usr/bin/env python3
# pylint: disable=W0603,R0914,R1702,R0912,R0915
"""
yml2gv is a simple script that traverses yaml and prepares graphviz graph out of it
Usage:
    yml2gv.py --input input.yaml --outout input.gv
You can create actual graph using dot utility. For example:
    dot input.gv -Tpdf -o input.pdf
"""
__author__ = "Pavel Leonovitch"
__copyright__ = "Copyright 2019, Pavel Leonovitch"

import uuid
import random
import argparse
import yaml

# ................. GLOBALS
# stores shapes in dot diagram
DOT_SHAPES = """ digraph {
    graph [pad="0.5", nodesep="0.5", ranksep="2"];
    node [shape=plain]
    rankdir=LR;

    """
# stores relationship in dot diagram
DOT_RELS = ""
# COLORS to assing to elements
COLORS = ['#f3f0f0', '#bdf5dd', '#dadcfc', '#fcfed5', '#f9dbfb', '#d4ffca']
# ................. EOF GLOBALS

def get_id():
    """
    returns id based on uid that can be used to identify element
    """
    uid = str(uuid.uuid4())
    uid2 = uid.replace("-", "")
    return "Item"+uid2

def generate_dot(dot_id, name, in_data, bgcolor="white"):
    """
    generates shape and relationship data (globals DOT_SHAPES and DOT_RELS)
    Note: recursive execution is used
    """
    global DOT_SHAPES
    global DOT_RELS
    global COLORS

    color = ''

    extensions = list()
    local_shape = """
{} [label=<
<table bgcolor="{}" border="0" cellborder="1" cellspacing="0">
\t<tr><td><b>{}</b></td></tr>
""".format(dot_id, bgcolor, name)
    if isinstance(in_data, dict):
        for key in in_data:
            if isinstance(in_data[key], str): #end leaf
                item = "\t<tr><td>{}:{}</td></tr>\n".format(key, in_data[key])
                local_shape += item
            if isinstance(in_data[key], dict): # key->dict
                src_id = get_id()
                dst_id = get_id()
                item = "\t<tr><td port=\"{}\">{}</td></tr>\n".format(src_id, key)
                local_shape += item
                rel = "{}:{} -> {}\n".format(dot_id, src_id, dst_id)
                DOT_RELS += rel
                if dot_id == 'main':
                    color = random.choice(COLORS)
                else:
                    color = bgcolor
                extensions.append({'id':dst_id, 'name': name+"."+key, 'input': in_data[key],
                                   'bgcolor':color})
            if isinstance(in_data[key], list): # list of things
                src_id = get_id()
                item = "\t<tr><td port=\"{}\">{}</td></tr>\n".format(src_id, key)
                local_shape += item
                l_leaves = list()
                l_dicts = list()
                for item in in_data[key]:
                    if isinstance(item, str):
                        l_leaves.append(item)
                    if isinstance(item, dict):
                        l_dicts.append(item)
                if len(l_leaves) > 0:
                    input_l = dict()
                    dst_id = get_id()
                    rel = "{}:{} -> {}\n".format(dot_id, src_id, dst_id)
                    DOT_RELS += rel
                    i = 1
                    for l_leave in l_leaves:
                        input_l[i] = l_leave
                        i += 1
                    if dot_id == 'main':
                        color = random.choice(COLORS)
                    else:
                        color = bgcolor
                    extensions.append({'id':dst_id, 'name': name+"."+key, 'input': input_l,
                                       'bgcolor':color})
                if len(l_dicts) > 0:
                    for item in l_dicts:
                        dst_id = get_id()
                        rel = "{}:{} -> {}\n".format(dot_id, src_id, dst_id)
                        DOT_RELS += rel
                        if dot_id == 'main':
                            color = random.choice(COLORS)
                        else:
                            color = bgcolor
                        extensions.append({'id':dst_id, 'name': name+"."+key, 'input': item,
                                           'bgcolor':color})
    # add current shape to globa shape defs
    local_shape += "</table>>];\n\n"
    DOT_SHAPES += local_shape
    # go after sub-trees
    for ext in extensions:
        generate_dot(dot_id=ext['id'], name=ext['name'], in_data=ext['input'],
                     bgcolor=ext['bgcolor'])

def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", help="input yaml file")
    parser.add_argument("--output", "-o", help="output graphviz file")
    args = parser.parse_args()
    if args.input:
        with open(args.input) as file:
            in_data = yaml.load(file, Loader=yaml.FullLoader)
            generate_dot(dot_id="main", name=" ", in_data=in_data, bgcolor="#efefef")
        if args.output:
            with open(args.output, 'w+') as file:
                file.write(DOT_SHAPES)
                file.write(DOT_RELS)
                file.write("}")
        else:
            print(DOT_SHAPES)
            print(DOT_RELS)
            print("}")

if __name__ == "__main__":
    main()
