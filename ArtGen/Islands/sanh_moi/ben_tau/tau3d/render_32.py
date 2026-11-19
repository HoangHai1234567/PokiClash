# Render tàu 3D (Tripo, tau3d/goc/tau.glb) ra 32 hướng cho game (người dùng 2026-11-19: "làm thẳng tàu thành model 3d ... để nó xoay
# cho mượt"). Blender chạy nền:
#   "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b -P render_32.py -- <glb> <thư mục ra> [số hướng=32] [góc nhìn=42]
# - Camera trực giao đứng phía nam nhìn chếch xuống (như góc nhìn bản đồ: bắc = lên màn), cố định; tàu xoay quanh trục đứng qua tâm.
# - Màu gốc không ánh sáng (emission từ ảnh màu Tripo) + viền mực nâu #2B2118 bằng vỏ lộn ngược (solidify, lật pháp tuyến, cull mặt sau).
# - Ra <thư mục>/hd_00..NN.png (512 x 512, nền trong) và meta.json: góc hướng trên màn của từng khung (độ, 0 = sang phải, 90 = lên),
#   toạ độ px trên ảnh của gốc (tâm thân ở mớn nước), mũi tàu, đèn lồng.
# Mô hình: dài theo X (mũi +X, đuôi có đèn lồng -X), Z lên, đáy z = 0.
import json
import math
import os
import sys

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:]
src, outdir = argv[0], argv[1]
N = int(argv[2]) if len(argv) > 2 else 32
ELEV = float(argv[3]) if len(argv) > 3 else 42.0
RES = 512
WATER = 0.13  # mớn nước (tỉ lệ chiều cao thân tính từ đáy): phần dưới bị cắt (chìm), mép nước có đường bọt
os.makedirs(outdir, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]

# gom về một gốc xoay ở tâm đáy
root = bpy.data.objects.new("goc", None)
bpy.context.scene.collection.objects.link(root)
lo = Vector((1e9, 1e9, 1e9))
hi = Vector((-1e9, -1e9, -1e9))
for o in meshes:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        lo = Vector((min(lo.x, w.x), min(lo.y, w.y), min(lo.z, w.z)))
        hi = Vector((max(hi.x, w.x), max(hi.y, w.y), max(hi.z, w.z)))
center = Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, lo.z))
for o in meshes:
    mw = o.matrix_world.copy()
    o.parent = root
    o.matrix_world = Matrix.Translation(-center) @ mw
L = hi.x - lo.x
Hh = hi.z - lo.z
wl = Hh * WATER

# vật liệu: emission màu gốc; viền mực
ink = bpy.data.materials.new("muc")
ink.use_nodes = True
nt = ink.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
em = nt.nodes.new("ShaderNodeEmission")
em.inputs["Color"].default_value = (0.0242, 0.0144, 0.0091, 1)  # #2B2118 tuyến tính
outn = nt.nodes.new("ShaderNodeOutputMaterial")
nt.links.new(em.outputs["Emission"], outn.inputs["Surface"])
ink.use_backface_culling = True


def water_cut(mat, surface_socket_out, foam=True, side_only=True):
    """Phần dưới mớn nước trong suốt (thân chìm); dải mảnh sát mớn nước tô bọt trắng."""
    t = mat.node_tree
    out = next(n for n in t.nodes if n.type == "OUTPUT_MATERIAL")
    geo = t.nodes.new("ShaderNodeNewGeometry")
    sep = t.nodes.new("ShaderNodeSeparateXYZ")
    t.links.new(geo.outputs["Position"], sep.inputs["Vector"])
    below0 = t.nodes.new("ShaderNodeMath")
    below0.operation = "LESS_THAN"
    below0.inputs[1].default_value = wl
    t.links.new(sep.outputs["Z"], below0.inputs[0])
    # chỉ mặt hông / đáy (pháp tuyến không ngửa lên): sàn tàu thấp gần mớn nước không bị cắt, không bị tô bọt
    nsep = t.nodes.new("ShaderNodeSeparateXYZ")
    t.links.new(geo.outputs["Normal"], nsep.inputs["Vector"])
    side = t.nodes.new("ShaderNodeMath")
    side.operation = "LESS_THAN"
    side.inputs[1].default_value = 0.55 if side_only else 2.0  # viền mực (pháp tuyến lật): cắt hết dưới mớn nước
    t.links.new(nsep.outputs["Z"], side.inputs[0])
    below = t.nodes.new("ShaderNodeMath")
    below.operation = "MULTIPLY"
    t.links.new(below0.outputs[0], below.inputs[0])
    t.links.new(side.outputs[0], below.inputs[1])
    shader = surface_socket_out
    if foam:
        band0 = t.nodes.new("ShaderNodeMath")
        band0.operation = "LESS_THAN"
        band0.inputs[1].default_value = wl + Hh * 0.022
        t.links.new(sep.outputs["Z"], band0.inputs[0])
        band = t.nodes.new("ShaderNodeMath")
        band.operation = "MULTIPLY"
        t.links.new(band0.outputs[0], band.inputs[0])
        t.links.new(side.outputs[0], band.inputs[1])
        white = t.nodes.new("ShaderNodeEmission")
        white.inputs["Color"].default_value = (0.92, 0.98, 1.0, 1)
        mixf = t.nodes.new("ShaderNodeMixShader")
        t.links.new(band.outputs[0], mixf.inputs["Fac"])
        t.links.new(shader, mixf.inputs[1])
        t.links.new(white.outputs["Emission"], mixf.inputs[2])
        shader = mixf.outputs["Shader"]
    tr = t.nodes.new("ShaderNodeBsdfTransparent")
    mix = t.nodes.new("ShaderNodeMixShader")
    t.links.new(below.outputs[0], mix.inputs["Fac"])
    t.links.new(shader, mix.inputs[1])
    t.links.new(tr.outputs["BSDF"], mix.inputs[2])
    t.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    else:
        mat.blend_method = "CLIP"


for o in meshes:
    for m in o.data.materials:
        if not m or not m.use_nodes:
            continue
        t = m.node_tree
        tex = next((n for n in t.nodes if n.type == "TEX_IMAGE" and n.image and not any(k in n.image.name.lower() for k in ("normal", "rough", "metal", "_rm"))), None)
        out = next((n for n in t.nodes if n.type == "OUTPUT_MATERIAL"), None)
        if tex and out:
            e2 = t.nodes.new("ShaderNodeEmission")
            t.links.new(tex.outputs["Color"], e2.inputs["Color"])
            t.links.new(e2.outputs["Emission"], out.inputs["Surface"])
    o.data.materials.append(ink)
    mod = o.modifiers.new("vien", "SOLIDIFY")
    mod.thickness = -L * 0.012
    mod.offset = 1.0
    mod.use_flip_normals = True
    mod.material_offset = len(o.data.materials) - 1
    mod.use_rim = False

# đường mớn nước: lát cắt ngang thân ở z = wl (toạ độ của gốc xoay), chiếu lên ảnh từng khung để hậu kỳ cắt phần chìm, vẽ bọt
wl_pts = []
for o in meshes:
    bm = bmesh.new()
    dg = bpy.context.evaluated_depsgraph_get()
    bm.from_mesh(o.data)
    bm.transform(Matrix.Translation(-center) @ o.matrix_basis if o.parent is None else o.matrix_local)
    res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, wl), plane_no=(0, 0, 1))
    for g in res["geom_cut"]:
        if isinstance(g, bmesh.types.BMVert):
            wl_pts.append(Vector((g.co.x, g.co.y, wl)))
    bm.free()
print("WL_PTS", len(wl_pts))

scene = bpy.context.scene
engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
scene.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in engines else "BLENDER_EEVEE_NEXT"
scene.render.film_transparent = True
scene.render.resolution_x = RES
scene.render.resolution_y = RES
scene.render.filter_size = 1.2
if hasattr(scene, "eevee"):
    try:
        scene.eevee.taa_render_samples = 48
    except Exception:
        pass
scene.view_settings.view_transform = "Standard"
cam_data = bpy.data.cameras.new("cam")
cam_data.type = "ORTHO"
cam_data.ortho_scale = max(L, Hh) * 1.32
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
e = math.radians(ELEV)
d = Vector((0, -math.cos(e), math.sin(e)))  # đứng phía nam (-Y), nhìn chếch xuống
look_at = Vector((0, 0, Hh * 0.42))
cam.location = look_at + d * (max(L, Hh) * 6)
cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()


def px(world):
    v = world_to_camera_view(scene, cam, world)
    return [round(v.x * RES, 2), round((1 - v.y) * RES, 2)]


meta = {"res": RES, "elev": ELEV, "frames": []}
for k in range(N):
    yaw = 2 * math.pi * k / N
    root.rotation_euler = (0, 0, yaw)
    bpy.context.view_layer.update()
    fwd = Vector((math.cos(yaw), math.sin(yaw), 0))
    pivot = Vector((0, 0, wl))
    a0, a1 = px(pivot), px(pivot + fwd * L * 0.3)
    ang = math.degrees(math.atan2(-(a1[1] - a0[1]), a1[0] - a0[0]))
    rot = Matrix.Rotation(yaw, 4, "Z")
    bow = rot @ Vector((L * 0.47, 0, wl))
    lantern = rot @ Vector((-L * 0.42, 0, Hh * 0.62))
    scene.render.filepath = os.path.join(outdir, f"hd_{k:02d}.png")
    bpy.ops.render.render(write_still=True)
    step = max(1, len(wl_pts) // 400)
    wl_px = [px(rot @ q) for q in wl_pts[::step]]
    meta["frames"].append({"k": k, "yaw": round(math.degrees(yaw), 3), "angle": round(ang, 3), "pivot": a0, "bow": px(bow),
                           "lantern": px(lantern), "waterline": wl_px})
json.dump(meta, open(os.path.join(outdir, "meta.json"), "w"), indent=1)
print("DONE", N)
