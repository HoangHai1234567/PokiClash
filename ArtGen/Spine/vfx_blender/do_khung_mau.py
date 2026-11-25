# Đo hộp bao (toạ độ thế giới) của các lớp lốc trong file mẫu ở vài khung
import bpy
from mathutils import Vector
sc = bpy.context.scene
names = ["Orange", "Shadow", "Highlight", "Smoke", "Red Sparks", "Blue Lightning"]
for f in (5, 20, 40, 70, 100, 115, 125, 135):
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    out = []
    for n in names:
        ob = sc.objects.get(n)
        if not ob:
            continue
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        if len(me.vertices) == 0:
            out.append(f"{n}:0"); ev.to_mesh_clear(); continue
        ps = [ev.matrix_world @ v.co for v in me.vertices]
        xs = [p.x for p in ps]; zs = [p.z for p in ps]
        out.append(f"{n}:{len(ps)} x[{min(xs):.2f},{max(xs):.2f}] z[{min(zs):.2f},{max(zs):.2f}]")
        ev.to_mesh_clear()
    print("F", f, " | ".join(out))
