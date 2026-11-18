"""Đọc mọi prefab ParticleSystem trong một thư mục (Epic Toon FX, bản đục Clash of Critters...) ra JSONL, không cần PyYAML.
Chạy: py -3 -I ps_dump.py "<thư mục gốc chứa .prefab + .meta>" <ra.jsonl>
Mỗi dòng: {"prefab": đường dẫn, "ps": [mỗi emitter: path, dur, loop, delay, life, speed, size, rot, grav, color, max, shape,
rate, bursts, mods{size_life, color_life, rot_life, sheet, vel, limit, noise, force, sub, trail, ...}, render, stretch, mat{shader,
tex, _DstBlend (1 = cộng sáng ADD, 10 = alpha AB)}, mesh}]. Đường cong ghi [(t, giá trị)], gradient {"c": [(t, màu)], "a": [(t, alpha)]}.
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

FLOW = re.compile(r"(\w+): ([^,{}]+|\{[^{}]*\})")


def _scalar(v):
    v = v.strip()
    if v.startswith("{") and v.endswith("}"):
        return {k: _scalar(x) for k, x in FLOW.findall(v[1:-1])}
    if v.startswith("[") and v.endswith("]"):
        return [_scalar(x) for x in v[1:-1].split(",") if x.strip()]
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return v


def _parse(lines, i, ind):
    """trả (obj, i). lines: [(indent, text)]."""
    obj = {}
    lst = None
    while i < len(lines):
        li, t = lines[i]
        if li < ind:
            break
        if t.startswith("- ") or t == "-":
            if li < ind:
                break
            if lst is None:
                lst = []
            body = t[2:] if t.startswith("- ") else ""
            if ":" in body and not body.startswith("{"):
                # mapping trong list: dòng đầu là "- k: v", các dòng sau thụt li+2
                sub = [(li + 2, body)]
                j = i + 1
                while j < len(lines) and lines[j][0] >= li + 2 and not (lines[j][0] == li and lines[j][1].startswith("-")):
                    sub.append(lines[j])
                    j += 1
                o, _ = _parse(sub, 0, li + 2)
                lst.append(o)
                i = j
            else:
                lst.append(_scalar(body))
                i += 1
            continue
        if li > ind and lst is None and not obj:
            ind = li
        if li != ind:
            i += 1
            continue
        if ":" not in t:
            i += 1
            continue
        k, _, v = t.partition(":")
        v = v.strip()
        if v == "":
            # con: thụt sâu hơn, hoặc list cùng mức
            if i + 1 < len(lines) and (lines[i + 1][0] > li or (lines[i + 1][0] == li and lines[i + 1][1].startswith("-"))):
                nxt = lines[i + 1][0]
                if lines[i + 1][1].startswith("-"):
                    sub = []
                    j = i + 1
                    while j < len(lines) and (lines[j][0] > li or (lines[j][0] == li and lines[j][1].startswith("-"))):
                        sub.append(lines[j])
                        j += 1
                    o, _ = _parse(sub, 0, nxt)
                    obj[k] = o
                    i = j
                else:
                    o, i = _parse(lines, i + 1, nxt)
                    obj[k] = o
            else:
                obj[k] = None
                i += 1
        else:
            obj[k] = _scalar(v)
            i += 1
    if lst is not None and not obj:
        return lst, i
    return obj, i


def load(path):
    src = open(path, encoding="utf-8", errors="replace").read()
    parts = re.split(r"^--- !u!(\d+) &(-?\d+).*$", src, flags=re.M)
    objs = {}
    for k in range(1, len(parts), 3):
        cls, fid, body = int(parts[k]), parts[k + 1], parts[k + 2]
        lines = []
        for raw in body.splitlines():
            if not raw.strip():
                continue
            s = raw.lstrip(" ")
            lines.append((len(raw) - len(s), s))
        if not lines:
            continue
        top, _ = _parse(lines, 0, 0)
        if isinstance(top, dict) and len(top) == 1:
            top = next(iter(top.values()))
        objs[fid] = (cls, top)
    return objs


# ---------- trích số ----------
def mmc(c):
    """MinMaxCurve -> dạng gọn: số, [min,max], hoặc {'curve': [(t,v)], 'mul': s}."""
    if not isinstance(c, dict):
        return c
    st, s, mn = c.get("minMaxState", 0), c.get("scalar", 0), c.get("minScalar", 0)
    def keys(cv):
        try:
            return [(round(float(k["time"]), 3), round(float(k["value"]), 3)) for k in cv["m_Curve"]]
        except Exception:
            return []
    if st == 0:
        return s
    if st == 3:
        return [mn, s]
    if st == 1:
        return {"curve": keys(c.get("maxCurve", {})), "mul": s}
    return {"curve_min": keys(c.get("minCurve", {})), "curve_max": keys(c.get("maxCurve", {})), "mul": s}


def col(c):
    if isinstance(c, dict) and "r" in c:
        return "#%02x%02x%02x%02x" % tuple(int(max(0, min(1, float(c[x]))) * 255) for x in "rgba")
    return c


def grad(g):
    if not isinstance(g, dict):
        return None
    nc, na = g.get("m_NumColorKeys", 0), g.get("m_NumAlphaKeys", 0)
    cks = [(round(g.get(f"ctime{i}", 0) / 65535, 2), col(g.get(f"key{i}"))[:7]) for i in range(nc)]
    aks = [(round(g.get(f"atime{i}", 0) / 65535, 2), round(float(g.get(f"key{i}", {}).get("a", 1)), 2)) for i in range(na)]
    return {"c": cks, "a": aks}


def mmg(c):
    if not isinstance(c, dict):
        return c
    st = c.get("minMaxState", 0)
    if st == 0:
        return col(c.get("maxColor"))
    if st == 2:
        return [col(c.get("minColor")), col(c.get("maxColor"))]
    if st in (1, 4):
        return grad(c.get("maxGradient"))
    return [grad(c.get("minGradient")), grad(c.get("maxGradient"))]


SHAPES = {0: "sphere", 1: "hemisphere", 2: "cone", 3: "box", 4: "cone", 5: "boxshell", 6: "mesh", 7: "coneshell", 8: "conevol",
          9: "conevolshell", 10: "circle", 11: "circleedge", 12: "edge", 13: "meshrenderer", 14: "skinned", 15: "boxedge",
          16: "donut", 17: "rectangle", 18: "sprite", 19: "spriterenderer"}
RMODE = {0: "billboard", 1: "stretched", 2: "horizontal", 3: "vertical", 4: "mesh", 5: "none"}


def ps_info(ps):
    d = {}
    d["dur"] = ps.get("lengthInSec")
    d["loop"] = ps.get("looping")
    d["delay"] = mmc(ps.get("startDelay"))
    d["space"] = {0: "local", 1: "world", 2: "custom"}.get(ps.get("moveWithTransform"), ps.get("moveWithTransform"))
    d["scaling"] = ps.get("scalingMode")
    init = ps.get("InitialModule", {}) or {}
    for k, n in (("startLifetime", "life"), ("startSpeed", "speed"), ("startSize", "size"), ("startRotation", "rot"),
                 ("gravityModifier", "grav")):
        d[n] = mmc(init.get(k))
    d["color"] = mmg(init.get("startColor"))
    d["max"] = init.get("maxNumParticles")
    sh = ps.get("ShapeModule", {}) or {}
    if sh.get("enabled") == 1:
        d["shape"] = {"type": SHAPES.get(sh.get("type"), sh.get("type")), "angle": sh.get("angle"),
                      "r": (sh.get("radius") or {}).get("value"), "arc": (sh.get("arc") or {}).get("value"),
                      "thick": sh.get("radiusThickness"), "rnd": sh.get("randomDirectionAmount"),
                      "rotY": (sh.get("m_Rotation") or {}).get("y")}
    em = ps.get("EmissionModule", {}) or {}
    d["rate"] = mmc(em.get("rateOverTime"))
    rd = mmc(em.get("rateOverDistance"))
    if rd:
        d["rate_dist"] = rd
    b = em.get("m_Bursts") or []
    if isinstance(b, list) and b:
        d["bursts"] = [(x.get("time"), mmc(x.get("countCurve")), x.get("cycleCount"), x.get("repeatInterval")) for x in b
                       if isinstance(x, dict)]
    mods = {}
    def on(name):
        m = ps.get(name) or {}
        return m if m.get("enabled") == 1 else None
    m = on("SizeModule")
    if m:
        mods["size_life"] = mmc(m.get("curve"))
    m = on("ColorModule")
    if m:
        mods["color_life"] = mmg(m.get("gradient"))
    m = on("RotationModule")
    if m:
        mods["rot_life"] = mmc(m.get("curve"))
    m = on("UVModule")
    if m:
        mods["sheet"] = {"tiles": (m.get("tilesX"), m.get("tilesY")), "anim": m.get("animationType"),
                         "fot": mmc(m.get("frameOverTime")), "start": mmc(m.get("startFrame")), "cycles": m.get("cycles"),
                         "mode": m.get("mode"), "fps": m.get("fps"), "timeMode": m.get("timeMode")}
    m = on("VelocityModule")
    if m:
        mods["vel"] = {k: mmc(m.get(k)) for k in ("x", "y", "z", "orbitalX", "orbitalY", "orbitalZ", "radial", "speedModifier")
                       if m.get(k) is not None and mmc(m.get(k)) not in (0, 0.0, 1, 1.0)}
    m = on("ClampVelocityModule")
    if m:
        mods["limit"] = {"mag": mmc(m.get("magnitude")), "dampen": m.get("dampen"), "drag": mmc(m.get("drag"))}
    m = on("NoiseModule")
    if m:
        mods["noise"] = {"str": mmc(m.get("strength")), "freq": m.get("frequency"), "scroll": mmc(m.get("scrollSpeed")),
                         "oct": m.get("octaves"), "pos": mmc(m.get("positionAmount")), "rotA": mmc(m.get("rotationAmount")),
                         "sizeA": mmc(m.get("sizeAmount"))}
    m = on("ForceModule")
    if m:
        mods["force"] = {k: mmc(m.get(k)) for k in "xyz"}
    m = on("SubModule")
    if m:
        mods["sub"] = [(x.get("type"), (x.get("emitter") or {}).get("fileID")) for x in (m.get("subEmitters") or [])
                       if isinstance(x, dict)]
    m = on("TrailModule")
    if m:
        mods["trail"] = {"ratio": m.get("ratio"), "life": mmc(m.get("lifetime")), "width": mmc(m.get("widthOverTrail"))}
    for nm, key in (("CollisionModule", "collision"), ("LightsModule", "lights"), ("InheritVelocityModule", "inherit"),
                    ("SizeBySpeedModule", "size_speed"), ("RotationBySpeedModule", "rot_speed"),
                    ("ColorBySpeedModule", "color_speed"), ("ExternalForcesModule", "ext"), ("CustomDataModule", "custom"),
                    ("TriggerModule", "trigger")):
        if on(nm):
            mods[key] = True
    d["mods"] = mods
    return d


class Index:
    """guid -> đường dẫn (png, mat, shader, mesh) trong một thư mục gốc."""

    def __init__(self, root):
        self.g = {}
        for dp, _, fs in os.walk(root):
            for f in fs:
                if f.endswith(".meta"):
                    p = os.path.join(dp, f)
                    try:
                        with open(p, encoding="utf-8", errors="replace") as fh:
                            for ln in fh:
                                if ln.startswith("guid:"):
                                    self.g[ln.split()[1]] = p[:-5]
                                    break
                    except OSError:
                        pass
        self.mat_cache = {}

    def mat(self, guid):
        if guid in self.mat_cache:
            return self.mat_cache[guid]
        p = self.g.get(guid)
        info = {"name": os.path.basename(p) if p else guid}
        if p and p.endswith(".mat"):
            o = load(p)
            for _, (cls, m) in o.items():
                if cls == 21:
                    sh = m.get("m_Shader") or {}
                    sg = sh.get("guid")
                    info["shader"] = os.path.basename(self.g[sg]) if sg in self.g else f"builtin:{sh.get('fileID')}"
                    info["kw"] = m.get("m_ShaderKeywords") or m.get("m_ValidKeywords")
                    props = m.get("m_SavedProperties") or {}
                    texs = props.get("m_TexEnvs") or []
                    for t in texs if isinstance(texs, list) else []:
                        for k, v in t.items():
                            if k == "_MainTex" or k == "_BaseMap":
                                tg = (v.get("m_Texture") or {}).get("guid")
                                if tg in self.g:
                                    info["tex"] = os.path.relpath(self.g[tg], ROOT).replace("\\", "/")
                    fl = props.get("m_Floats") or []
                    for t in fl if isinstance(fl, list) else []:
                        for k, v in t.items():
                            if k in ("_Mode", "_Surface", "_Blend", "_SrcBlend", "_DstBlend", "_InvFade", "_ColorMode"):
                                info[k] = v
                    cl = props.get("m_Colors") or []
                    for t in cl if isinstance(cl, list) else []:
                        for k, v in t.items():
                            if k in ("_TintColor", "_Color", "_BaseColor"):
                                info[k] = col(v)
        self.mat_cache[guid] = info
        return info


ROOT = "."


def prefab(path, idx):
    o = load(path)
    names, father, comp_go = {}, {}, {}
    for fid, (cls, m) in o.items():
        if cls == 1:
            names[fid] = m.get("m_Name")
    for fid, (cls, m) in o.items():
        if cls == 4 and isinstance(m, dict):
            go = (m.get("m_GameObject") or {}).get("fileID")
            comp_go[fid] = str(go)
            father[str(go)] = str((m.get("m_Father") or {}).get("fileID"))
    tr_go = {k: v for k, v in comp_go.items()}
    def path_of(go):
        out = []
        seen = 0
        while go and go in names and seen < 20:
            out.append(names[go])
            f = father.get(go)
            go = tr_go.get(f)
            seen += 1
        return "/".join(reversed(out))
    systems = {}
    for fid, (cls, m) in o.items():
        if cls == 198 and isinstance(m, dict):
            go = str((m.get("m_GameObject") or {}).get("fileID"))
            info = ps_info(m)
            info["path"] = path_of(go)
            info["_fid"] = fid
            systems[go] = info
    for fid, (cls, m) in o.items():
        if cls == 199 and isinstance(m, dict):
            go = str((m.get("m_GameObject") or {}).get("fileID"))
            if go in systems:
                r = systems[go]
                r["render"] = RMODE.get(m.get("m_RenderMode"), m.get("m_RenderMode"))
                if m.get("m_RenderMode") == 1:
                    r["stretch"] = {"len": m.get("m_LengthScale"), "vel": m.get("m_VelocityScale")}
                r["order"] = (m.get("m_SortingFudge"), m.get("m_SortingOrder"))
                mats = m.get("m_Materials") or []
                if isinstance(mats, list) and mats and isinstance(mats[0], dict):
                    r["mat"] = idx.mat(mats[0].get("guid"))
                if m.get("m_RenderMode") == 4:
                    mg = (m.get("m_Mesh") or {}).get("guid")
                    r["mesh"] = os.path.basename(idx.g.get(mg, str(mg)))
    # sub-emitter: đổi fileID thành tên
    by_fid = {s["_fid"]: s["path"].split("/")[-1] for s in systems.values()}
    for s in systems.values():
        if "sub" in s["mods"]:
            s["mods"]["sub"] = [({0: "birth", 1: "collision", 2: "death", 3: "trigger", 4: "manual"}.get(t, t), by_fid.get(str(f), f))
                                for t, f in s["mods"]["sub"]]
        s.pop("_fid", None)
    return list(systems.values())


if __name__ == "__main__":
    ROOT = sys.argv[1]
    idx = Index(ROOT)
    out = open(sys.argv[2], "w", encoding="utf-8")
    n = 0
    for dp, _, fs in os.walk(ROOT):
        for f in fs:
            if f.endswith(".prefab"):
                p = os.path.join(dp, f)
                try:
                    s = prefab(p, idx)
                except Exception as e:  # noqa
                    s = {"error": repr(e)}
                out.write(json.dumps({"prefab": os.path.relpath(p, ROOT).replace("\\", "/"), "ps": s}, ensure_ascii=False) + "\n")
                n += 1
    print("prefabs", n)
