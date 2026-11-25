# Render vài khung bằng Eevee với vật liệu gốc (xem đúng màu của file mẫu): -- <thư_mục_ra> <khung,khung,...> [rộng]
import bpy, os, sys
a = sys.argv[sys.argv.index("--") + 1:]
out, frames = a[0], [int(x) for x in a[1].split(",")]
w = int(a[2]) if len(a) > 2 else 480
os.makedirs(out, exist_ok=True)
sc = bpy.context.scene
for ob in sc.objects:
    if ob.name.lower().startswith("floor"):
        ob.hide_render = True
r = sc.render
r.engine = "BLENDER_EEVEE"
r.resolution_x, r.resolution_y, r.resolution_percentage = w, int(w * 9 / 16), 100
r.film_transparent = True
r.image_settings.file_format, r.image_settings.color_mode = "PNG", "RGBA"
for f in frames:
    sc.frame_set(f)
    r.filepath = os.path.join(out, f"f{f:03d}.png")
    bpy.ops.render.render(write_still=True)
print("OK eevee", out)
