# Gộp 6 hiệu ứng mẫu CodyWinch vào một file .blend, mỗi hiệu ứng một Scene (để mở một cửa sổ Blender xem cho nhẹ).
import bpy, os
R = "D:/PokiClash/ArtGen/Spine/vfx_blender/ref_codywinch"
SRC = [("1 Cloudy Explosion", "Cloudy Explosion 2 8"), ("2 Blue Puffy Explosion", "Blue Puffy Explosion 2 8"),
       ("3 Directional Explosion", "Directional Explosion 2 79"), ("4 Energy Ball", "Energy Ball 2 8"),
       ("5 Swirling Energy", "Swirling Energy 2 8"), ("6 Twisting Effect", "Twisting Effect 2 8")]
bpy.ops.wm.read_factory_settings(use_empty=True)
blank = bpy.context.scene
for nm, f in SRC:
    with bpy.data.libraries.load(os.path.join(R, f + ".blend"), link=False) as (df, dt):
        dt.scenes = df.scenes[:1]
    sc = dt.scenes[0]
    sc.name = nm
    sc.frame_current = (sc.frame_start + sc.frame_end) // 2
    print("ok", nm, sc.frame_start, sc.frame_end, len(sc.objects))
bpy.context.window_manager.windows[0].scene = bpy.data.scenes["1 Cloudy Explosion"] if bpy.context.window_manager.windows else None
bpy.data.scenes.remove(blank)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(R, "TAT_CA_6_hieu_ung.blend"))
print("saved")
