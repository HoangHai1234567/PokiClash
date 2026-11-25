# Đo phân bố trọng số W (trước Mask) của lớp "kem" ở vài khung: chạy sau phun_blender.py đã --save
import bpy, sys
import numpy as np
ob = bpy.data.objects["kem"]
for m in ob.modifiers:
    if m.type in ("MASK", "SMOOTH", "NODES"):
        m.show_render = m.show_viewport = False
gi = ob.vertex_groups["W"].index
for f in (1, 6, 12, 20, 28):
    bpy.context.scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    me = ob.evaluated_get(dg).to_mesh()
    w = np.array([next((g.weight for g in v.groups if g.group == gi), -1) for v in me.vertices])
    w = w[w >= 0]
    print("F", f, "n", len(w), "pct", np.round(np.percentile(w, [5, 20, 40, 60, 80, 95]), 3))
    ob.evaluated_get(dg).to_mesh_clear()
