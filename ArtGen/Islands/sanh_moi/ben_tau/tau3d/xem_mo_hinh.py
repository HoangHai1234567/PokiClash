# Blender chạy nền: nhập mô hình tàu Tripo, in kích thước / vật liệu, render 4 góc xem nhanh (không ánh sáng: màu gốc).
# "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b -P xem_mo_hinh.py -- <file .glb/.fbx> <ảnh ra .png>
import math
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
src, out = argv[0], argv[1]

bpy.ops.wm.read_factory_settings(use_empty=True)
if src.lower().endswith(".fbx"):
    bpy.ops.import_scene.fbx(filepath=src)
else:
    bpy.ops.import_scene.gltf(filepath=src)

meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
lo = Vector((1e9, 1e9, 1e9))
hi = Vector((-1e9, -1e9, -1e9))
for o in meshes:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        lo = Vector((min(lo.x, w.x), min(lo.y, w.y), min(lo.z, w.z)))
        hi = Vector((max(hi.x, w.x), max(hi.y, w.y), max(hi.z, w.z)))
print("MESHES", [(o.name, len(o.data.vertices), len(o.data.polygons)) for o in meshes])
print("BOUNDS", tuple(round(v, 3) for v in lo), tuple(round(v, 3) for v in hi))
for o in meshes:
    for m in o.data.materials:
        print("MAT", o.name, m.name if m else None)

# màu gốc không ánh sáng: thay mọi vật liệu bằng emission từ ảnh màu gốc
for o in meshes:
    for m in o.data.materials:
        if not m or not m.use_nodes:
            continue
        nt = m.node_tree
        tex = next((n for n in nt.nodes if n.type == "TEX_IMAGE" and n.image and "normal" not in n.image.name.lower()
                    and "rough" not in n.image.name.lower() and "metal" not in n.image.name.lower()), None)
        outn = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
        if tex and outn:
            em = nt.nodes.new("ShaderNodeEmission")
            nt.links.new(tex.outputs["Color"], em.inputs["Color"])
            nt.links.new(em.outputs["Emission"], outn.inputs["Surface"])

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE_NEXT"
scene.render.film_transparent = True
scene.render.resolution_x = 512
scene.render.resolution_y = 512
scene.view_settings.view_transform = "Standard"
center = (lo + hi) / 2
size = max(hi - lo)
cam_data = bpy.data.cameras.new("cam")
cam_data.type = "ORTHO"
cam_data.ortho_scale = size * 1.25
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam

# 4 góc quanh trục đứng (Blender: Z lên), nhìn chếch xuống 40 độ
elev = math.radians(40)
dist = size * 4
up_axis = "Z"
for k, az in enumerate((0, 90, 180, 270)):
    a = math.radians(az)
    d = Vector((math.cos(a) * math.cos(elev), math.sin(a) * math.cos(elev), math.sin(elev)))
    cam.location = center + d * dist
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = out.replace(".png", f"_{k}.png")
    bpy.ops.render.render(write_still=True)
print("DONE")
