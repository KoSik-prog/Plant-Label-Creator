import cadquery as cq
import os

def create_text(label, fontsize):
    text = cq.Workplane("XY").text(label, fontsize, distance=4)
    text_width = text.val().BoundingBox().xmax - text.val().BoundingBox().xmin
    text_height = text.val().BoundingBox().ymax - text.val().BoundingBox().ymin
    print(f"Text width: {text_width}, Text height: {text_height}")
    return text, text_width, text_height

def get_font_path(relative_path):
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, relative_path)

def create_marker_box(label, font_size=8, min_width=40, min_height=20):
    border_height = 3
    label_list = []
    text_width_max = 0
    text_height_max = 0

    if not isinstance(label, list):
        label = [label]

    if len(label) > 1:
        y_offset = 4
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
    print(f"outside width: {box_border_width}, outside height: {box_border_height}")

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
    marker = base.cut(border_cut) 
    for text_cut in label_list:
        marker = marker.cut(text_cut) 
    marker = marker.union(net)
    return marker

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





# label = ["Pomidor", "San Marzano"]
label = "Marchew"
if isinstance(label, list):
    name = label[0].replace(" ", "_").replace(".", "_").replace(",", "_")
else:
    name = label.replace(" ", "_").replace(".", "_").replace(",", "_")


marker_box = create_marker_box(label, font_size=9, min_width=30, min_height=20)
pin = create_pin(70, -3)
marker = marker_box.union(pin)

# marker_box_big = create_marker_box(label, font_size=16, min_width=80, min_height=40)
# pin = create_pin(130, -10)
# marker = marker_box_big.union(pin)

marker.val().exportStl(f"{name}_marker.stl")

print(f"Marker '{name}' saved as {name}_marker.stl")
