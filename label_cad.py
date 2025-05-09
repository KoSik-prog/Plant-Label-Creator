#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        label_cad.py
# Purpose:
#
# Author:      KoSik
#
# Created:     07.05.2025
# Copyright:   (c) kosik 2025
# -------------------------------------------------------------------------------
import cadquery as cq
import os

def create_text(label, fontsize):
    text = cq.Workplane("XY").text(label, fontsize, distance=4)
    text_width = text.val().BoundingBox().xmax - text.val().BoundingBox().xmin
    text_height = text.val().BoundingBox().ymax - text.val().BoundingBox().ymin
    print(f"Text dimensions: {text_width:.1f} / {text_height:.1f}")
    return text, text_width, text_height

def get_font_path(relative_path):
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, relative_path)

def create_label_box(label, font_size=8, min_width=40, min_height=20):
    border_height = 3
    label_list = []
    text_width_max = 0
    text_height_max = 0

    if not isinstance(label, list):
        label = [label]

    if len(label) > 1:
        y_offset = 3
    else:
        y_offset = 0
        

    for lab in label:
        if len(lab) > 20:
            return None
        text, text_width, text_height = create_text(lab, fontsize=font_size)
        text = text.translate((0, y_offset, 0))
        label_list.append(text)
        if text_width > text_width_max:
            text_width_max = text_width
        text_height_max += text_height
        y_offset -= text_height + 1
        font_size = font_size / 2

    box_width = text_width_max if text_width_max > min_width else min_width
    box_height = text_height_max if text_height_max > min_height else min_height
    box_border_width = box_width + border_height*2
    box_border_height = box_height + border_height*2
    print(f"Outside dimensions: {box_border_width:.1f} / {box_border_height:.1f}")

    base = (
        cq.Workplane("XY")
        .rect(box_border_width, box_border_height)
        .extrude(4)
        .edges("|Z")
        .fillet(3.0)
    )
    net = (
        cq.Workplane("XY")
        .rarray(0, 0.8, 1, int(box_height*0.8))
        .box(text_width_max, 0.3, 0.3)
        .translate((0, 0, 0.15))
    )
    border_cut = 2 if border_height >=2 else 0
    border_cut= (
        cq.Workplane("XY")
        .rect(box_border_width-border_cut, box_border_height-border_cut)
        .extrude(1)
        .edges("|Z")
        .fillet(3.0)
        .translate((0, 0, 3))
    )
    label = base.cut(border_cut) 
    for text_cut in label_list:
        label = label.cut(text_cut) 
    label = label.union(net)
    return label

def create_pin(length, y_offset=0):
    reduction_factor = 0.8

    pin = (
        cq.Workplane("XY")
        .moveTo(-4, 0)
        .lineTo(0, -10)
        .lineTo(4, 0)
        .lineTo(4, length - 10)
        .lineTo(-4, length - 10)
        .close()
        .extrude(4)
        .translate((0, -length, 0))
    )
    
    border_cut = (   
    cq.Workplane("XY")
        .moveTo(-4 * reduction_factor, 0)
        .lineTo(0, -10 * reduction_factor)
        .lineTo(4 * reduction_factor, 0)
        .lineTo(4 * reduction_factor, length - 10 * reduction_factor)
        .lineTo(-4 * reduction_factor, length - 10 * reduction_factor)
        .close()
        .extrude(4)
        .translate((0, -length, 1.5))
    )
    pin = pin.cut(border_cut)
    pin = pin.translate((0, y_offset, 0))
    return pin


def create_label_small(label):
    if isinstance(label, list):
        name = label[0].replace(" ", "_").replace(".", "_").replace(",", "_")
    else:
        name = label.replace(" ", "_").replace(".", "_").replace(",", "_")

    label_box = create_label_box(label, font_size=9, min_width=30, min_height=20)
    pin = create_pin(70, -3)
    label = label_box.union(pin)
    label.val().exportStl(f"{name}_label.stl")
    print(f"Label '{name}' saved as {name}_label.stl")


def create_label_big(label):
    if isinstance(label, list):
        name = label[0].replace(" ", "_").replace(".", "_").replace(",", "_")
    else:
        name = label.replace(" ", "_").replace(".", "_").replace(",", "_")

    label_box_big = create_label_box(label, font_size=16, min_width=80, min_height=40)
    pin = create_pin(130, -13)
    label = label_box_big.union(pin)
    label.val().exportStl(f"{name}_label.stl")
    print(f"Label '{name}' saved as {name}_label.stl")