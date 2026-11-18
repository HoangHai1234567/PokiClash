# Nạp component + template của KR5 bằng luamini (chỉ tính bảng dữ liệu, không chạy game).
#   from kr5_templates import load_templates; T = load_templates(ROOT)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from luamini import Interp, LTab, LFunc, PyFunc, STUB, make_stdlib, deepclone


def load_templates(root, verbose=True):
    LUA = os.path.join(root, 'lua_src')
    it = Interp(); make_stdlib(it)
    G = it.G.vars
    G['KR_GAME'] = 'kr5'; G['KR_TARGET'] = 'phone'; G['KR_PATH_GAME'] = 'kr5'; G['KR_PATH_ALL'] = 'all'
    comps = {}; ents = {}; order = []

    def register_t(self, name, base=None):
        if name in ents: return None
        if isinstance(base, str): base = ents.get(base)
        t = deepclone(base) if isinstance(base, LTab) else LTab()
        t.set('template_name', name); ents[name] = t; order.append(name)
        return t

    def register_c(self, name, base=None):
        if isinstance(base, str): base = comps.get(base)
        c = deepclone(base) if isinstance(base, LTab) else LTab()
        comps[name] = c
        return c

    def clone_c(self, name): return deepclone(comps.get(name)) if name in comps else None

    def add_comps(self, ent, *names):
        if isinstance(ent, LTab):
            for n in names:
                if n in comps: ent.set(n, deepclone(comps[n]))
        return None

    def get_component(self, c): return comps.get(c) if isinstance(c, str) else c
    def get_template(self, t): return ents.get(t) if isinstance(t, str) else t

    def set_template(self, name, t):
        if name not in ents: order.append(name)
        ents[name] = t

    def create_entity(self, t):
        tpl = ents.get(t) if isinstance(t, str) else t
        return deepclone(tpl) if isinstance(tpl, LTab) else None

    def append_templates(self, ent, *names):
        for n in names:
            tpl = ents.get(n)
            if isinstance(tpl, LTab) and isinstance(ent, LTab):
                for k, v in tpl.d.items(): ent.d[k] = deepclone(v)

    E = LTab({k: PyFunc(v, k) for k, v in dict(register_t=register_t, register_c=register_c, clone_c=clone_c,
                                                    add_comps=add_comps, get_component=get_component, get_template=get_template,
                                                    set_template=set_template, create_entity=create_entity,
                                                    append_templates=append_templates).items()})
    E.set('entities', STUB); E.set('components', STUB)
    loaded = {}

    def run_file(rel):
        p = os.path.join(LUA, rel)
        src = open(p, encoding='utf-8').read()
        return it.run(src, rel)

    FILES = {'constants': 'all/constants.lua', 'components': 'all/components.lua', 'templates': 'all/templates.lua',
             'game_templates': 'kr5/game_templates.lua', 'balance/balance': 'kr5/balance/balance.lua'}

    def require(name):
        if name in loaded: return loaded[name]
        if name == 'bit': v = G['bit']
        elif name == 'entity_db': v = E
        elif name in FILES:
            loaded[name] = STUB
            try:
                v = run_file(FILES[name])
            except Exception as ex:
                if verbose: print('  lỗi chạy %s: %s' % (name, ex))
                v = STUB
            if v is None: v = True
        else:
            v = STUB
        loaded[name] = v
        return v

    G['require'] = PyFunc(require)
    G['package'] = LTab({'loaded': LTab()})
    G['love'] = STUB
    sys.setrecursionlimit(20000)
    require('constants')
    require('components')
    require('templates')
    require('game_templates')
    if verbose:
        print('component:', len(comps), ' template:', len(ents), ' lời gọi:', it.steps)
    return ents, order, comps, G


def to_py(v, depth=0):
    """LTab -> dict/list; bỏ hàm và STUB."""
    if isinstance(v, LTab):
        if depth > 12: return None
        d = v.d
        n = v.length()
        if n and n == len(d):
            return [to_py(d[i], depth + 1) for i in range(1, n + 1)]
        out = {}
        for k, x in d.items():
            if k == 'template_name' and depth > 0: continue
            px = to_py(x, depth + 1)
            if px is None and x is not None and not isinstance(x, LTab): continue
            out[str(k)] = px
        return out
    if v is STUB or isinstance(v, (LFunc, PyFunc)): return None
    if isinstance(v, float):
        if v != v or v in (float('inf'), float('-inf')): return None
        return round(v, 5)
    return v


if __name__ == '__main__':
    import json, time
    sys.stdout.reconfigure(encoding='utf-8')
    t0 = time.time()
    ents, order, comps, G = load_templates(sys.argv[1] if len(sys.argv) > 1 else '.')
    print('xong sau %.1fs' % (time.time() - t0))
    for n in sys.argv[2:]:
        print(n, json.dumps(to_py(ents.get(n)), ensure_ascii=False, indent=1)[:3000])
