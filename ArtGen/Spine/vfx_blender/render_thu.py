# -*- coding: utf-8 -*-
"""Render nhẹ vài khung của một file .blend để xem dáng (Workbench, tô phẳng theo màu Emission, nền trong).

    blender.exe -b --disable-autoexec <file.blend> --python render_thu.py -- <thư_mục_ra> <số_khung> [rộng]
"""
import os
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
out_dir, n = argv[0], int(argv[1])
width = int(argv[2]) if len(argv) > 2 else 480
os.makedirs(out_dir, exist_ok=True)
sc = bpy.context.scene
for ob in sc.objects:
    if ob.name.lower().startswith("floor"):
        ob.hide_render = True
# màu hiển thị = màu Emission để Workbench tô phẳng đúng màu
for m in bpy.data.materials:
    col = None
    if m.use_nodes and m.node_tree:
        for nd in m.node_tree.nodes:
            if nd.bl_idname == "ShaderNodeEmission" and not nd.inputs["Color"].is_linked:
                col = list(nd.inputs["Color"].default_value)
            if nd.bl_idname == "ShaderNodeValToRGB" and col is None:
                col = list(nd.color_ramp.elements[-1].color)
    if col:
        m.diffuse_color = (min(col[0], 1), min(col[1], 1), min(col[2], 1), 1)
r = sc.render
r.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading
sh.light = "FLAT"
sh.color_type = "MATERIAL"
sh.show_object_outline = False
r.film_transparent = True
sc.view_settings.view_transform = "Standard"
r.resolution_x = width
r.resolution_y = int(width * 9 / 16)
r.resolution_percentage = 100
r.image_settings.file_format = "PNG"
r.image_settings.color_mode = "RGBA"
f0, f1 = sc.frame_start, sc.frame_end
for i in range(n):
    f = round(f0 + (f1 - f0) * i / max(n - 1, 1))
    sc.frame_set(f)
    r.filepath = os.path.join(out_dir, f"f{f:03d}.png")
    bpy.ops.render.render(write_still=True)
print("OK render", out_dir)
