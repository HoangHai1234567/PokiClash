"""Đảo Mộc (10 dòng, 24 dạng), 2026-11-07: người dùng chốt concept bằng chữ, giao làm một mạch bằng Codex.

Chạy ở máy ổ E (bộ công cụ aola của máy này: part_map, region_map, orig_refs, ghep_nhom, anim_moi). Đặc tả từng dạng ở
tools/moc_spec/<dòng>.py (mỗi file một danh sách SPEC, khai bằng hàm F dưới đây). Script ghi cho từng dạng:
  <aola>/reskin/moc_<id>/regions.json, groups.json, ghep.json (vùng concept = nhóm mảnh);
  ảnh rig (region_map.py, orig_refs.py), chép Silhouette, RegionMap, Rig_Numbered (cắt theo bóng xám, lề 6%) và orig/
  sang ArtGen/Heroes/refs/moc/<mã>/; độ dày viền mỗi nhóm (0,85% chiều cao con × tỉ lệ phóng của orig);
  mục FORMS vào ArtGen/Heroes/forms_moc/<mã>.json (build.py nạp cả thư mục).

    py -3 -I ArtGen/Heroes/tools/lo_moc.py [mã ...]

Cần part_map.py đã chạy cho dạng đó: <aola>/reskin/pet<id>_parts/front_idle/ (parts.json, part_NN.png, part_map.png).
"""
import glob
import importlib.util
import json
import os
import shutil
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
HEROES = os.path.normpath(os.path.join(HERE, ".."))
AOLA = next(p for p in ("E:/ProjectAtomik/aola", "D:/Aola-20261029T161238Z-1-001/Aola/AolaRipper/AolaRipper")
            if os.path.isdir(p))
OUT = os.path.join(HEROES, "forms_moc")  # <mã>.json mỗi dạng
sys.stdout.reconfigure(encoding="utf-8")


def G(code, parts, kind, en, vi, old, new, joint=None, hide=(), frame=None):
    """Một nhóm mảnh.
    parts: mảnh vẽ trong ảnh gốc của nhóm (số theo part_map); mảnh đầu là mảnh chính.
    kind: "giu" (giữ viền: thân, tay, chân) hoặc "doi" (đổi dáng: đầu, tai, đuôi, phụ kiện; joint = đầu khớp giữ chỗ).
    hide: mảnh có trong ảnh gốc (để GPT biết chỗ, như mắt cũ) nhưng khi ghép thì ẩn, vì mảnh chính đã vẽ luôn.
    frame: mảnh dùng để căn khung ảnh gốc (mặc định = parts), thêm mảnh bên cạnh để chừa chỗ khi đổi dáng to hơn."""
    return dict(code=code, parts=list(parts), kind=kind, en=en, vi=vi, old=old, new=new, joint=joint, hide=list(hide),
                frame=list(frame) if frame else None)


def F(code, aola, hero, n, forms, name, stage, design_vi, intro, stance, attitude, colours, avoid, groups, keep=(1,),
      drop=(), prev=None, anim=None, note=""):
    """Một dạng.
    stage: "ải 1 đảo Mộc, dạng 1/3" (ghi vào role_vi).
    keep: mảnh giữ hình gốc (bóng); drop: mảnh bỏ hẳn (hiệu ứng aola không hợp thiết kế mới).
    prev: mã dạng 1 của dòng (dạng 2, 3 đính concept đã duyệt của nó).
    anim: dữ liệu cho khuôn animation (anim_moc.py): root (mảnh gốc, thường là thân), head, swing (vung khi đánh),
          wob (đung đưa), fly (bay rời, cha null), cast (mảnh, fx, fy: chỗ bắn tia theo khung bao mảnh), parent {mảnh: cha}."""
    return dict(code=code, aola=aola, hero=hero, form=n, forms=forms, form_name=name, stage=stage, design_vi=design_vi,
                intro=intro, stance=stance, attitude=attitude, colours=colours, avoid=avoid, groups=groups,
                keep=list(keep), drop=list(drop), prev=prev, anim=anim or {}, note=note)


def load_specs():
    out = []
    for path in sorted(glob.glob(os.path.join(HERE, "moc_spec", "*.py"))):
        spec = importlib.util.spec_from_file_location("moc_spec_" + os.path.basename(path)[:-3], path)
        mod = importlib.util.module_from_spec(spec)
        mod.F, mod.G = F, G
        spec.loader.exec_module(mod)
        out += mod.SPEC
    return out


def concept_text(f):
    gs = f["groups"]
    keep = "; ".join(f"{i} {g['en']}" for i, g in enumerate(gs, 1))
    change = "\n".join(f"{i} {g['en']}: {g['new']}." for i, g in enumerate(gs, 1))
    prev = (" Image 6 is the approved first stage of this creature: keep its colours, face and drawing style; this stage is "
            "the same creature grown up.") if f["prev"] else ""
    return (f"Character concept for a 2D cut-out animation game. Draw ONE original creature: {f['intro']}, in the same view "
            f"and pose as image 1, {f['stance']}, on a plain white background. A cute, chunky creature, but an original design "
            "that must look clearly DIFFERENT from the figure the silhouette came from; not any existing character.\n\n"
            "Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new "
            "creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do "
            "not trace their outline. Viewer-left and viewer-right mean as seen in the picture.\n\n"
            "KEEP FROM THE RIG (the animation moves these parts around these joints):\n"
            f"- the same parts, no more, no fewer, each where its numbered region is: {keep};\n"
            "- every joint where it is and every part pointing the same way as in image 1; eyes where the old eyes are;\n"
            "- each part about the size and shape of its region; the whole figure about the same size.\n\n"
            f"CHANGE (the new look, region by region):\n{change}\n\n"
            f"ATTITUDE: {f['attitude']}; cute, never scary, never a cheerful mascot.\n\n"
            "{RENDER}\n{DESIGN}\n"
            "The style sheet is image 3; the hand-drawn map is image 4. Image 5 is an approved character of this game: copy "
            "its ink line weight and its pencil and crayon texture, not its design; it has a few white shine spots and some "
            f"darker shading: do NOT copy those.{prev}\n\n"
            f"COLOURS: {f['colours']}. Few colours.\n\n"
            f"AVOID: {f['avoid']}, text, labels, numbers, the region colours, frames, background scenery, a second view, "
            "shading, shadows, white highlights, glossy shine, glow, gradients.")


def group_tuple(g, px):
    n = len(g["parts"])
    pieces = "one piece" if n == 1 else f"{n} pieces"
    keep = ", with the same outline" if g["kind"] == "giu" else ""
    prompt = (f"Image 1 is {pieces} of a 2D cut-out animation puppet (the old design): {g['old']}. Redraw THESE pieces as the "
              f"{g['en']} of image 2 (the approved concept): {g['new']}. Keep every piece where it is in image 1{keep}.\n"
              "Do NOT draw: any other part of the creature, the old colours, extra pieces.")
    check = (f"- đúng chỗ, cỡ như mảnh cũ{'' if g['kind'] == 'doi' else ', giữ viền'};\n- như concept: {g['vi']};\n"
             "- không vẽ phần khác.")
    return [g["code"], g["vi"], g["en"], g["kind"], px, g["old"], f"{g['vi']} cũ (1024 × 1024, nền trắng)", check, prompt,
            g["joint"]]


def crop_box(sil_path, margin=0.06):
    im = Image.open(sil_path).convert("L")
    bb = Image.eval(im, lambda v: 255 if v < 250 else 0).getbbox()
    m = round(margin * max(bb[2] - bb[0], bb[3] - bb[1]))
    return (max(0, bb[0] - m), max(0, bb[1] - m), min(im.width, bb[2] + m), min(im.height, bb[3] + m))


def crop_save(src, dst, box):
    im = Image.open(src).convert("RGB")
    out = Image.new("RGB", (box[2] - box[0], box[3] - box[1]), "white")
    out.paste(im.crop((max(0, box[0]), max(0, box[1]), box[2], box[3])), (0, 0))
    out.save(dst)


def make(f):
    pid, code = f["aola"], f["code"]
    pdir = os.path.join(AOLA, "reskin", f"pet{pid}_parts")
    pm = os.path.join(pdir, "front_idle")
    rdir = os.path.join(AOLA, "reskin", f"moc_{pid}")
    os.makedirs(rdir, exist_ok=True)
    parts = json.load(open(os.path.join(pm, "parts.json"), encoding="utf-8"))
    # kiểm: mỗi mảnh đúng một vai (nhóm, giữ, bỏ), hai mảnh chung hình thì phải cùng bỏ hoặc cùng giữ
    allp = {p["n"]: p for p in parts["parts"]}
    role = {}
    for g in f["groups"]:
        for n in g["parts"]:
            if n in role:
                raise SystemExit(f"{code}: mảnh {n} ở hai chỗ ({role[n]}, {g['code']})")
            role[n] = g["code"] + ("-an" if n in g["hide"] else "")
    for n in f["keep"]:
        role.setdefault(n, "giu")
    for n in f["drop"]:
        if n in role:
            raise SystemExit(f"{code}: mảnh {n} vừa bỏ vừa ở {role[n]}")
        role[n] = "bo"
    missing = sorted(set(allp) - set(role))
    if missing:
        raise SystemExit(f"{code}: mảnh chưa có vai: {missing}")
    by_char = {}
    for n, p in allp.items():
        by_char.setdefault(p["character"], []).append(n)
    def gvai(n):  # vai khi ghép: t thay hình, d ẩn (bỏ hoặc gộp vào mảnh chính), k giữ
        r = role[n]
        return "k" if r == "giu" else "d" if r == "bo" or r.endswith("-an") else "t"

    shared = []
    for c, ns in by_char.items():
        vs = {gvai(n) for n in ns}
        if len(ns) < 2 or vs in ({"d"}, {"k"}):
            continue
        if vs == {"t"} and len({role[n] for n in ns}) == 1:
            # cặp mảnh giống nhau (hai tai, hai chân) cùng nhóm: ghép phải dùng chung một hình mới cho cả cặp
            shared.append((c, ns))
            print(f"  CẢNH BÁO {code}: mảnh {ns} chung hình c{c} (cùng nhóm {role[ns[0]]}), lúc ghép dùng chung một hình")
            continue
        raise SystemExit(f"{code}: mảnh {ns} chung hình c{c} nhưng vai {[role[n] for n in ns]} "
                         "(chỉ được cùng bỏ, cùng gộp ẩn, cùng giữ, hoặc cùng một nhóm)")
    excl = f["keep"] + f["drop"]
    regions = {"note": f"{code} (lo_moc.py): vùng concept = nhóm mảnh", "exclude": excl,
               "regions": [{"n": i, "name": g["en"], "parts": g["parts"]} for i, g in enumerate(f["groups"], 1)]}
    groups = {"note": f"{code} (lo_moc.py)", "clip": "1_1", "keep": f["keep"], "drop": f["drop"],
              "groups": [{"code": g["code"], "name": g["en"], "anchor": g["parts"][0], "draw": g["parts"],
                          **({"frame": g["frame"]} if g["frame"] else {})} for g in f["groups"]]}
    refs_dir = os.path.join(HEROES, "refs", "moc", code)
    ghep_path = os.path.join(rdir, "ghep.json")
    old_ghep = json.load(open(ghep_path, encoding="utf-8")) if os.path.exists(ghep_path) else {}
    ghep = {"_ghi_chu": f"{f['hero']} dạng {f['form']}/{f['forms']} ({code}) ghép lên rig aola #{pid} (lo_moc.py). "
                        f"Chạy: py -3 -I tools/ghep_nhom.py reskin/moc_{pid}",
            "base": f"goc_{pid}", "refs": refs_dir.replace("\\", "/") + "/orig/",
            "inbox": os.path.join(HEROES, "inbox", code, "tai_ve").replace("\\", "/") + "/",
            "head_group": next((g["code"] for g in f["groups"] if g["hide"]), f["groups"][0]["code"]),
            "groups": {g["code"]: {"pieces": [n for n in g["parts"] if n not in g["hide"]],
                                   **({"drop": g["hide"]} if g["hide"] else {})} for g in f["groups"]},
            "drop": f["drop"]}
    if shared:  # cặp mảnh chung hình trong một nhóm (ghép dùng hình mới của mảnh đầu cho cả cặp)
        ghep["shared"] = [ns for _, ns in shared]
    for k in ("drop_chars", "keep_chars", "variants", "extra", "to_nuoc"):  # chỉnh tay lúc ghép: giữ khi chạy lại
        if k in old_ghep:
            ghep[k] = old_ghep[k]
    for name, data in (("regions.json", regions), ("groups.json", groups), ("ghep.json", ghep)):
        json.dump(data, open(os.path.join(rdir, name), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # ảnh rig
    prefix = os.path.join(rdir, "refs", f"{pid}_Front")
    os.makedirs(os.path.dirname(prefix), exist_ok=True)
    for args in ([os.path.join(AOLA, "tools", "region_map.py"), pm, os.path.join(rdir, "regions.json"), prefix],
                 [os.path.join(AOLA, "tools", "orig_refs.py"), rdir, pdir]):
        p = subprocess.run([sys.executable, "-I"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if p.returncode:
            raise SystemExit(f"{code}: {os.path.basename(args[0])} lỗi\n{p.stdout}{p.stderr}")
    os.makedirs(os.path.join(refs_dir, "orig"), exist_ok=True)
    box = crop_box(prefix + "_Silhouette.png")
    crop_save(prefix + "_Silhouette.png", os.path.join(refs_dir, "Silhouette.png"), box)
    crop_save(prefix + "_RegionMap.png", os.path.join(refs_dir, "RegionMap.png"), box)
    crop_save(os.path.join(pm, "part_map.png"), os.path.join(refs_dir, "Rig_Numbered.png"), box)
    for g in f["groups"]:
        shutil.copy2(os.path.join(rdir, "refs", "orig", g["code"] + ".png"), os.path.join(refs_dir, "orig", g["code"] + ".png"))
    # độ dày viền: 0,85% chiều cao con (đơn vị clip) × px mỗi đơn vị của ảnh gốc nhóm
    sc = parts["scale"]
    bs = [allp[n]["box"] for n in allp if n not in excl]
    H = (max(b[3] for b in bs) - min(b[1] for b in bs)) / sc
    meta = json.load(open(os.path.join(rdir, "refs", "orig", "orig_groups.json"), encoding="utf-8"))
    px = {k: max(6, round(0.0085 * H * v["k"])) for k, v in meta.items()}
    entry = {"code": code, "elem": "moc", "aola": pid, "hero": f["hero"], "form": f["form"], "forms": f["forms"],
             "form_name": f["form_name"], "role_vi": f"tướng hệ Mộc ({f['stage']}), rig aola #{pid}",
             "design_vi": f["design_vi"], "rig_vi": f"con gốc #{pid} (xem Rig_Numbered.png)",
             "regions_vi": ", ".join(f"{i} {g['vi']}" for i, g in enumerate(f["groups"], 1)), "anchor": True,
             "concept": concept_text(f), "groups": [group_tuple(g, px[g["code"]]) for g in f["groups"]], "extra": [],
             "first": [f["groups"][0]["code"], f["groups"][1]["code"] if len(f["groups"]) > 1 else f["groups"][0]["code"]],
             "anim": f["anim"]}
    if f["prev"]:
        entry["prev"] = [[f["prev"], "the approved FIRST stage of this evolution line: keep its colours, face and drawing "
                                     "style; this stage is the same creature grown up", "dạng 1 đã duyệt của dòng này"]]
    print(code, f"cao {H:.0f}", px)
    return entry


def main(only):
    # mỗi dạng một file (nhiều phiên chạy cùng lúc không ghi đè nhau); build.py nạp cả thư mục
    os.makedirs(OUT, exist_ok=True)
    for f in load_specs():
        if only and f["code"] not in only:
            continue
        json.dump(make(f), open(os.path.join(OUT, f["code"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(set(sys.argv[1:]))
