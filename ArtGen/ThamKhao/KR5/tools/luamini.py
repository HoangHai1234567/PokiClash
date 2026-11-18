# Bộ chạy Lua thu gọn (Lua 5.1, đủ cho file khai báo template của KR5) viết bằng Python.
# Không gọi ra ngoài, không đọc/ghi file: chỉ tính bảng dữ liệu. Giá trị không biết -> STUB (lan truyền).
import re, math, random

random.seed(1)


class _Stub:
    _inst = None
    def __new__(cls):
        if cls._inst is None: cls._inst = super().__new__(cls)
        return cls._inst
    def __repr__(self): return 'STUB'
    def __bool__(self): return True


STUB = _Stub()


class LTab:
    __slots__ = ('d',)
    def __init__(self, d=None): self.d = d if d is not None else {}
    def get(self, k):
        if isinstance(k, float) and k.is_integer(): k = int(k)
        return self.d.get(k)
    def set(self, k, v):
        if isinstance(k, float) and k.is_integer(): k = int(k)
        if v is None: self.d.pop(k, None)
        else: self.d[k] = v
    def length(self):
        n = 0
        while (n + 1) in self.d: n += 1
        return n
    def __repr__(self): return 'LTab(%d)' % len(self.d)


class LFunc:
    def __init__(self, params, vararg, body, scope, name=None):
        self.params, self.vararg, self.body, self.scope, self.name = params, vararg, body, scope, name


class PyFunc:
    def __init__(self, fn, name=''): self.fn, self.name = fn, name


class _Ret(Exception):
    def __init__(self, vals): self.vals = vals


class _Brk(Exception): pass


# ------------------------------------------------------------ tokenizer
TOK = re.compile(r'''\s*(?:
    (?P<cm>--\[(?P<eq0>=*)\[.*?\](?P=eq0)\]|--[^\n]*)
  | (?P<ls>\[(?P<eq>=*)\[.*?\](?P=eq)\])
  | (?P<num>0[xX][0-9a-fA-F]+|(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)
  | (?P<str>"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*')
  | (?P<name>[A-Za-z_]\w*)
  | (?P<op>\.\.\.|\.\.|==|~=|<=|>=|::|[-+*/%^#<>=(){}\[\];:,.])
)''', re.S | re.X)
ESC = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'", 'a': '\a', 'b': '\b', 'f': '\f', 'v': '\v', '\n': '\n'}
KW = {'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for', 'function', 'goto', 'if', 'in', 'local', 'nil',
      'not', 'or', 'repeat', 'return', 'then', 'true', 'until', 'while'}


def unescape(s):
    out = []; i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            n = s[i + 1]
            if n.isdigit():
                m = re.match(r'\d{1,3}', s[i + 1:]); out.append(chr(int(m.group()))); i += 1 + len(m.group()); continue
            out.append(ESC.get(n, n)); i += 2; continue
        out.append(c); i += 1
    return ''.join(out)


def tokenize(src):
    toks = []; pos = 0; n = len(src)
    while pos < n:
        m = TOK.match(src, pos)
        if not m:
            if src[pos:].strip() == '': break
            raise SyntaxError('token lạ ở %d: %r' % (pos, src[pos:pos + 40]))
        pos = m.end()
        if m.group('cm') is not None: continue
        if m.group('ls') is not None:
            t = m.group('ls'); k = len(m.group('eq')) + 2; body = t[k:-k]
            if body.startswith('\n'): body = body[1:]
            toks.append(('str', body))
        elif m.group('num') is not None:
            t = m.group('num')
            toks.append(('num', int(t, 16) if t[:2] in ('0x', '0X') else (float(t) if any(c in t for c in '.eE') else int(t))))
        elif m.group('str') is not None:
            toks.append(('str', unescape(m.group('str')[1:-1])))
        elif m.group('name') is not None:
            w = m.group('name'); toks.append(('kw' if w in KW else 'name', w))
        else:
            toks.append(('op', m.group('op')))
    toks.append(('eof', None))
    return toks


# ------------------------------------------------------------ parser -> AST (tuple)
BINP = {'or': (1, 1), 'and': (2, 2), '<': (3, 3), '>': (3, 3), '<=': (3, 3), '>=': (3, 3), '~=': (3, 3), '==': (3, 3),
        '..': (5, 4), '+': (6, 6), '-': (6, 6), '*': (7, 7), '/': (7, 7), '%': (7, 7), '^': (10, 9)}
UNP = 8


class Parser:
    def __init__(self, src):
        self.t = tokenize(src); self.i = 0

    def peek(self, k=0): return self.t[self.i + k]
    def nxt(self): v = self.t[self.i]; self.i += 1; return v
    def check(self, kind, val=None):
        t = self.t[self.i]; return t[0] == kind and (val is None or t[1] == val)
    def accept(self, kind, val=None):
        if self.check(kind, val): self.i += 1; return True
        return False
    def expect(self, kind, val=None):
        t = self.nxt()
        if t[0] != kind or (val is not None and t[1] != val):
            raise SyntaxError('cần %s %r, gặp %r (token %d)' % (kind, val, t, self.i))
        return t[1]

    def block(self):
        out = []
        while True:
            t = self.peek()
            if t[0] == 'eof' or (t[0] == 'kw' and t[1] in ('end', 'else', 'elseif', 'until')): return out
            if t == ('kw', 'return'):
                self.nxt(); vals = []
                if not (self.check('eof') or self.check('op', ';') or (self.peek()[0] == 'kw' and self.peek()[1] in ('end', 'else', 'elseif', 'until'))):
                    vals = self.explist()
                self.accept('op', ';'); out.append(('return', vals)); return out
            s = self.stat()
            if s is not None: out.append(s)

    def stat(self):
        t = self.peek()
        if t == ('op', ';'): self.nxt(); return None
        if t == ('op', '::'): self.nxt(); self.expect('name'); self.expect('op', '::'); return None
        if t[0] == 'kw':
            k = t[1]
            if k == 'break': self.nxt(); return ('break',)
            if k == 'goto': self.nxt(); self.expect('name'); return None
            if k == 'do': self.nxt(); b = self.block(); self.expect('kw', 'end'); return ('do', b)
            if k == 'while':
                self.nxt(); c = self.exp(); self.expect('kw', 'do'); b = self.block(); self.expect('kw', 'end'); return ('while', c, b)
            if k == 'repeat':
                self.nxt(); b = self.block(); self.expect('kw', 'until'); c = self.exp(); return ('repeat', b, c)
            if k == 'if':
                self.nxt(); arms = []
                c = self.exp(); self.expect('kw', 'then'); arms.append((c, self.block()))
                els = None
                while True:
                    if self.accept('kw', 'elseif'):
                        c = self.exp(); self.expect('kw', 'then'); arms.append((c, self.block()))
                    elif self.accept('kw', 'else'):
                        els = self.block(); self.expect('kw', 'end'); break
                    else:
                        self.expect('kw', 'end'); break
                return ('if', arms, els)
            if k == 'for':
                self.nxt(); n1 = self.expect('name')
                if self.accept('op', '='):
                    a = self.exp(); self.expect('op', ','); b = self.exp(); c = None
                    if self.accept('op', ','): c = self.exp()
                    self.expect('kw', 'do'); body = self.block(); self.expect('kw', 'end')
                    return ('fornum', n1, a, b, c, body)
                names = [n1]
                while self.accept('op', ','): names.append(self.expect('name'))
                self.expect('kw', 'in'); exps = self.explist(); self.expect('kw', 'do'); body = self.block(); self.expect('kw', 'end')
                return ('forin', names, exps, body)
            if k == 'function':
                self.nxt(); path = [self.expect('name')]; method = False
                while self.accept('op', '.'): path.append(self.expect('name'))
                if self.accept('op', ':'): path.append(self.expect('name')); method = True
                f = self.funcbody(method)
                return ('funcdef', path, f)
            if k == 'local':
                self.nxt()
                if self.accept('kw', 'function'):
                    n = self.expect('name'); f = self.funcbody(False); return ('localfunc', n, f)
                names = [self.expect('name')]
                while self.accept('op', ','): names.append(self.expect('name'))
                exps = self.explist() if self.accept('op', '=') else []
                return ('local', names, exps)
        e = self.suffixexp()
        if self.check('op', '=') or self.check('op', ','):
            targets = [e]
            while self.accept('op', ','): targets.append(self.suffixexp())
            self.expect('op', '='); exps = self.explist()
            return ('assign', targets, exps)
        if e[0] not in ('call', 'mcall'): raise SyntaxError('câu không hợp lệ %r' % (e,))
        return ('callst', e)

    def funcbody(self, method):
        self.expect('op', '('); params = ['self'] if method else []; va = False
        if not self.accept('op', ')'):
            while True:
                if self.accept('op', '...'): va = True; break
                params.append(self.expect('name'))
                if not self.accept('op', ','): break
            self.expect('op', ')')
        body = self.block(); self.expect('kw', 'end')
        return ('func', params, va, body)

    def explist(self):
        out = [self.exp()]
        while self.accept('op', ','): out.append(self.exp())
        return out

    def exp(self, lim=0):
        t = self.peek()
        if t == ('kw', 'not') or t == ('op', '-') or t == ('op', '#'):
            self.nxt(); v = ('un', t[1], self.exp(UNP))
        else:
            v = self.simple()
        while True:
            t = self.peek()
            op = t[1] if t[0] in ('op', 'kw') else None
            p = BINP.get(op)
            if p is None or p[0] <= lim: break
            self.nxt(); rhs = self.exp(p[1]); v = ('bin', op, v, rhs)
        return v

    def simple(self):
        t = self.peek()
        if t[0] in ('num', 'str'): self.nxt(); return ('const', t[1])
        if t == ('kw', 'nil'): self.nxt(); return ('const', None)
        if t == ('kw', 'true'): self.nxt(); return ('const', True)
        if t == ('kw', 'false'): self.nxt(); return ('const', False)
        if t == ('op', '...'): self.nxt(); return ('vararg',)
        if t == ('op', '{'): return self.table()
        if t == ('kw', 'function'): self.nxt(); return self.funcbody(False)
        return self.suffixexp()

    def suffixexp(self):
        t = self.nxt()
        if t[0] == 'name': e = ('name', t[1])
        elif t == ('op', '('): e = ('paren', self.exp()); self.expect('op', ')')
        else: raise SyntaxError('biểu thức lạ %r ở token %d' % (t, self.i))
        while True:
            t = self.peek()
            if t == ('op', '.'): self.nxt(); e = ('index', e, ('const', self.expect('name')))
            elif t == ('op', '['): self.nxt(); k = self.exp(); self.expect('op', ']'); e = ('index', e, k)
            elif t == ('op', ':'):
                self.nxt(); m = self.expect('name'); e = ('mcall', e, m, self.args())
            elif t == ('op', '(') or t == ('op', '{') or t[0] == 'str':
                e = ('call', e, self.args())
            else:
                return e

    def args(self):
        t = self.peek()
        if t[0] == 'str': self.nxt(); return [('const', t[1])]
        if t == ('op', '{'): return [self.table()]
        self.expect('op', '(')
        if self.accept('op', ')'): return []
        a = self.explist(); self.expect('op', ')'); return a

    def table(self):
        self.expect('op', '{'); items = []
        while not self.accept('op', '}'):
            t = self.peek()
            if t == ('op', '['):
                self.nxt(); k = self.exp(); self.expect('op', ']'); self.expect('op', '='); items.append(('kv', k, self.exp()))
            elif t[0] == 'name' and self.peek(1) == ('op', '='):
                self.nxt(); self.nxt(); items.append(('kv', ('const', t[1]), self.exp()))
            else:
                items.append(('pos', self.exp()))
            if not (self.accept('op', ',') or self.accept('op', ';')):
                self.expect('op', '}'); break
        return ('table', items)


# ------------------------------------------------------------ interpreter
class Scope:
    __slots__ = ('vars', 'parent')
    def __init__(self, parent=None): self.vars = {}; self.parent = parent
    def find(self, n):
        s = self
        while s is not None:
            if n in s.vars: return s
            s = s.parent
        return None


def truthy(v): return v is not None and v is not False


def tostr(v):
    if v is None: return 'nil'
    if v is True: return 'true'
    if v is False: return 'false'
    if isinstance(v, float) and v.is_integer() and abs(v) < 1e15: return str(int(v))
    return str(v)


def lua_eq(a, b):
    if a is b: return True
    if isinstance(a, bool) or isinstance(b, bool): return False
    if isinstance(a, (int, float)) and isinstance(b, (int, float)): return a == b
    if isinstance(a, str) and isinstance(b, str): return a == b
    return False


def arith(op, a, b):
    if a is STUB or b is STUB: return STUB
    try:
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/':
            if b == 0: return math.inf if a > 0 else (-math.inf if a < 0 else math.nan)
            return a / b
        if op == '%': return a - math.floor(a / b) * b
        if op == '^': return float(a) ** b
        if op == '..': return tostr(a) + tostr(b)
        if op == '<': return a < b
        if op == '>': return a > b
        if op == '<=': return a <= b
        if op == '>=': return a >= b
    except Exception:
        return STUB
    return STUB


class Interp:
    def __init__(self):
        self.G = Scope()
        self.steps = 0

    def setg(self, n, v): self.G.vars[n] = v

    def run(self, src, name='?', scope=None):
        ast = Parser(src).block()
        sc = Scope(scope or self.G)
        try:
            self.block(ast, sc)
        except _Ret as r:
            return r.vals[0] if r.vals else None
        return None

    # ---- statements
    def block(self, stmts, sc):
        for s in stmts:
            self.stat(s, sc)

    def stat(self, s, sc):
        k = s[0]
        if k == 'assign':
            vals = self.explist(s[2], sc)
            for i, tg in enumerate(s[1]):
                v = vals[i] if i < len(vals) else None
                self.assign(tg, v, sc)
        elif k == 'local':
            vals = self.explist(s[2], sc) if s[2] else []
            for i, n in enumerate(s[1]):
                sc.vars[n] = vals[i] if i < len(vals) else None
        elif k == 'callst':
            self.eval_multi(s[1], sc)
        elif k == 'localfunc':
            f = LFunc(*s[2][1:3], s[2][3], sc, s[1]); sc.vars[s[1]] = f; f.scope = sc
        elif k == 'funcdef':
            path = s[1]; f = LFunc(s[2][1], s[2][2], s[2][3], sc, '.'.join(path))
            if len(path) == 1:
                self.assign(('name', path[0]), f, sc)
            else:
                obj = self.ev(('name', path[0]), sc)
                for p in path[1:-1]: obj = self.index(obj, p)
                self.setindex(obj, path[-1], f)
        elif k == 'if':
            for c, b in s[1]:
                cv = self.ev(c, sc)
                if cv is STUB: cv = False      # điều kiện không biết: coi như sai
                if truthy(cv):
                    self.block(b, Scope(sc)); return
            if s[2] is not None: self.block(s[2], Scope(sc))
        elif k == 'fornum':
            a = self.ev(s[2], sc); b = self.ev(s[3], sc); c = self.ev(s[4], sc) if s[4] else 1
            if not all(isinstance(x, (int, float)) for x in (a, b, c)): return
            i = a
            try:
                while (i <= b) if c > 0 else (i >= b):
                    ns = Scope(sc); ns.vars[s[1]] = i
                    self.block(s[5], ns); i += c
            except _Brk:
                pass
        elif k == 'forin':
            vals = self.explist(s[2], sc)
            f = vals[0] if vals else None
            st = vals[1] if len(vals) > 1 else None
            ctl = vals[2] if len(vals) > 2 else None
            try:
                n = 0
                while True:
                    r = self.call(f, [st, ctl])
                    if not r or r[0] is None: break
                    ctl = r[0]; ns = Scope(sc)
                    for j, nm in enumerate(s[1]): ns.vars[nm] = r[j] if j < len(r) else None
                    self.block(s[3], ns); n += 1
                    if n > 100000: break
            except _Brk:
                pass
        elif k == 'while':
            n = 0
            try:
                while truthy(self.ev(s[1], sc)) and self.ev(s[1], sc) is not STUB and n < 10000:
                    self.block(s[2], Scope(sc)); n += 1
            except _Brk:
                pass
        elif k == 'repeat':
            n = 0
            try:
                while n < 10000:
                    ns = Scope(sc); self.block(s[1], ns); n += 1
                    c = self.ev(s[2], ns)
                    if truthy(c): break
            except _Brk:
                pass
        elif k == 'do':
            self.block(s[1], Scope(sc))
        elif k == 'return':
            raise _Ret(self.explist(s[1], sc))
        elif k == 'break':
            raise _Brk()

    def assign(self, tg, v, sc):
        if tg[0] == 'name':
            s = sc.find(tg[1])
            (s.vars if s is not None else self.G.vars)[tg[1]] = v
        elif tg[0] == 'index':
            obj = self.ev(tg[1], sc); key = self.ev(tg[2], sc)
            self.setindex(obj, key, v)

    def setindex(self, obj, key, v):
        if isinstance(obj, LTab) and key is not None and key is not STUB:
            obj.set(key, v)

    def index(self, obj, key):
        if isinstance(obj, LTab):
            v = obj.get(key)
            return v
        if obj is STUB: return STUB
        if isinstance(obj, str):
            return self.G.vars['string'].get(key)
        return STUB if obj is not None else None

    # ---- expressions
    def explist(self, exps, sc):
        out = []
        for i, e in enumerate(exps):
            if i == len(exps) - 1 and e[0] in ('call', 'mcall', 'vararg'):
                out.extend(self.eval_multi(e, sc))
            else:
                out.append(self.ev(e, sc))
        return out

    def eval_multi(self, e, sc):
        k = e[0]
        if k == 'call':
            f = self.ev(e[1], sc); args = self.explist(e[2], sc)
            return self.call(f, args)
        if k == 'mcall':
            o = self.ev(e[1], sc); f = self.index(o, e[2]); args = [o] + self.explist(e[3], sc)
            return self.call(f, args)
        if k == 'vararg':
            s = sc.find('...'); return list(s.vars['...']) if s else []
        return [self.ev(e, sc)]

    def ev(self, e, sc):
        k = e[0]
        if k == 'const': return e[1]
        if k == 'name':
            s = sc.find(e[1])
            return s.vars[e[1]] if s is not None else None
        if k == 'index':
            return self.index(self.ev(e[1], sc), self.ev(e[2], sc))
        if k in ('call', 'mcall', 'vararg'):
            r = self.eval_multi(e, sc); return r[0] if r else None
        if k == 'paren': return self.ev(e[1], sc)
        if k == 'bin':
            op = e[1]
            if op == 'and':
                a = self.ev(e[2], sc)
                return self.ev(e[3], sc) if truthy(a) else a
            if op == 'or':
                a = self.ev(e[2], sc)
                if a is STUB:
                    b = self.ev(e[3], sc); return b if b is not None else STUB
                return a if truthy(a) else self.ev(e[3], sc)
            a = self.ev(e[2], sc); b = self.ev(e[3], sc)
            if op == '==': return lua_eq(a, b)
            if op == '~=': return not lua_eq(a, b)
            return arith(op, a, b)
        if k == 'un':
            v = self.ev(e[2], sc)
            if e[1] == 'not': return not truthy(v) if v is not STUB else STUB
            if e[1] == '-': return -v if isinstance(v, (int, float)) else STUB
            if isinstance(v, LTab): return v.length()
            if isinstance(v, str): return len(v)
            return STUB
        if k == 'table':
            t = LTab(); n = 1; items = e[1]
            for j, it in enumerate(items):
                if it[0] == 'kv':
                    t.set(self.ev(it[1], sc), self.ev(it[2], sc))
                else:
                    if j == len(items) - 1 and it[1][0] in ('call', 'mcall', 'vararg'):
                        for v in self.eval_multi(it[1], sc): t.set(n, v); n += 1
                    else:
                        t.set(n, self.ev(it[1], sc)); n += 1
            return t
        if k == 'func':
            return LFunc(e[1], e[2], e[3], sc)
        raise RuntimeError('ast lạ %r' % (k,))

    def call(self, f, args):
        self.steps += 1
        if isinstance(f, PyFunc):
            r = f.fn(*args)
            if isinstance(r, tuple): return list(r)
            return [r]
        if isinstance(f, LFunc):
            ns = Scope(f.scope)
            for i, p in enumerate(f.params): ns.vars[p] = args[i] if i < len(args) else None
            if f.vararg: ns.vars['...'] = args[len(f.params):]
            try:
                self.block(f.body, ns)
            except _Ret as r:
                return r.vals
            except RecursionError:
                return [STUB]
            return []
        return [STUB]


# ------------------------------------------------------------ thư viện chuẩn tối thiểu
def deepclone(v, memo=None):
    if not isinstance(v, LTab): return v
    if memo is None: memo = {}
    if id(v) in memo: return memo[id(v)]
    t = LTab(); memo[id(v)] = t
    for k, x in v.d.items(): t.d[deepclone(k, memo)] = deepclone(x, memo)
    return t


def mk(d): return LTab({k: (PyFunc(v, k) if callable(v) else v) for k, v in d.items()})


def lua_format(fmt, *args):
    out = []; ai = 0
    for m in re.finditer(r'%([-+ #0]*\d*(?:\.\d+)?)([sdifgxXqc%])|[^%]+|%', fmt):
        if m.group(2) is None:
            out.append(m.group(0)); continue
        spec, c = m.groups()
        if c == '%': out.append('%'); continue
        a = args[ai] if ai < len(args) else None; ai += 1
        if a is STUB: out.append('?'); continue
        try:
            if c == 's': out.append(('%' + spec + 's') % tostr(a))
            elif c in 'di': out.append(('%' + spec + 'd') % int(a))
            elif c == 'q': out.append('"%s"' % tostr(a))
            elif c == 'c': out.append(chr(int(a)))
            else: out.append(('%' + spec + c) % a)
        except Exception:
            out.append(tostr(a))
    return ''.join(out)


def make_stdlib(it):
    def ipairs(t):
        def nx(t, i):
            i = (i or 0) + 1
            v = t.get(i) if isinstance(t, LTab) else None
            return (None,) if v is None else (i, v)
        return PyFunc(nx), t, 0

    def pairs(t):
        keys = list(t.d.keys()) if isinstance(t, LTab) else []
        ints = sorted(k for k in keys if isinstance(k, (int, float)))
        others = [k for k in keys if not isinstance(k, (int, float))]
        order = ints + others; pos = {}
        def nx(tt, k):
            i = 0 if k is None else pos.get(id(k) if isinstance(k, LTab) else k, len(order)) + 1
            while i < len(order):
                kk = order[i]
                if isinstance(t, LTab) and kk in t.d:
                    pos[id(kk) if isinstance(kk, LTab) else kk] = i
                    return kk, t.d[kk]
                i += 1
            return (None,)
        return PyFunc(nx), t, None

    def tinsert(t, a, b=None, *rest):
        if not isinstance(t, LTab): return None
        if b is None and not rest:
            t.set(t.length() + 1, a)
        else:
            n = t.length()
            for i in range(n, int(a) - 1, -1): t.set(i + 1, t.get(i))
            t.set(int(a), b)
        return None

    def tappend(t, src, *a):
        if isinstance(t, LTab) and isinstance(src, LTab):
            for i in range(1, src.length() + 1): t.set(t.length() + 1, src.get(i))
        return t

    def tmerge(t, src, *a):
        if isinstance(t, LTab) and isinstance(src, LTab):
            for k, v in src.d.items(): t.d[k] = v
        return t

    def ttype(v):
        if v is None: return 'nil'
        if isinstance(v, bool): return 'boolean'
        if isinstance(v, (int, float)): return 'number'
        if isinstance(v, str): return 'string'
        if isinstance(v, LTab): return 'table'
        if isinstance(v, (LFunc, PyFunc)): return 'function'
        return 'userdata'

    def unpack(t, i=1, j=None):
        if not isinstance(t, LTab): return ()
        j = t.length() if j is None else j
        return tuple(t.get(k) for k in range(int(i), int(j) + 1))

    def num(f):
        def g(*a):
            if any(x is STUB or not isinstance(x, (int, float)) for x in a): return STUB
            try: return f(*a)
            except Exception: return STUB
        return g

    def rnd(a=None, b=None):
        if a is None: return random.random()
        if b is None: return random.randint(1, int(a))
        return random.randint(int(a), int(b))

    G = it.G.vars
    G['math'] = mk({'pi': math.pi, 'huge': math.inf, 'floor': num(lambda x: math.floor(x)), 'ceil': num(lambda x: math.ceil(x)),
                    'abs': num(abs), 'max': num(max), 'min': num(min), 'sqrt': num(math.sqrt), 'sin': num(math.sin),
                    'cos': num(math.cos), 'tan': num(math.tan), 'atan2': num(math.atan2), 'atan': num(math.atan),
                    'rad': num(math.radians), 'deg': num(math.degrees), 'random': rnd, 'fmod': num(math.fmod),
                    'pow': num(math.pow), 'exp': num(math.exp), 'log': num(lambda x, b=math.e: math.log(x, b))})
    G['string'] = mk({'format': lua_format, 'upper': lambda s: s.upper() if isinstance(s, str) else STUB,
                      'lower': lambda s: s.lower() if isinstance(s, str) else STUB,
                      'sub': lambda s, i=1, j=-1: (s[(int(i) - 1 if i > 0 else len(s) + int(i)):(len(s) + int(j) + 1 if j < 0 else int(j))]) if isinstance(s, str) else STUB,
                      'len': lambda s: len(s) if isinstance(s, str) else STUB,
                      'rep': lambda s, n: s * int(n) if isinstance(s, str) else STUB,
                      'find': lambda *a: STUB, 'gsub': lambda s, *a: (s, 0), 'match': lambda *a: None})
    G['table'] = mk({'insert': tinsert, 'deepclone': deepclone, 'append': tappend, 'merge': tmerge,
                     'remove': lambda t, i=None: None, 'concat': lambda t, sep='': sep.join(tostr(t.get(k)) for k in range(1, t.length() + 1)) if isinstance(t, LTab) else STUB,
                     'contains': lambda t, v: isinstance(t, LTab) and v in t.d.values(),
                     'sort': lambda *a: None})
    G['bit'] = mk({'bor': num(lambda *a: __import__('functools').reduce(lambda x, y: int(x) | int(y), a, 0)),
                   'band': num(lambda *a: __import__('functools').reduce(lambda x, y: int(x) & int(y), a, -1)),
                   'bnot': num(lambda a: ~int(a)), 'lshift': num(lambda a, b: int(a) << int(b)), 'rshift': num(lambda a, b: int(a) >> int(b))})
    G['ipairs'] = PyFunc(ipairs); G['pairs'] = PyFunc(pairs); G['type'] = PyFunc(ttype); G['unpack'] = PyFunc(unpack)
    G['tostring'] = PyFunc(tostr)
    G['tonumber'] = PyFunc(lambda v, b=10: (float(v) if isinstance(v, str) and re.fullmatch(r'\s*-?[\d.]+(e-?\d+)?\s*', v) else (v if isinstance(v, (int, float)) else None)))
    G['print'] = PyFunc(lambda *a: None); G['assert'] = PyFunc(lambda v=None, *a: (v,) + a)
    G['error'] = PyFunc(lambda *a: None); G['pcall'] = PyFunc(lambda f, *a: (True,) + tuple(it.call(f, list(a))))
    G['setmetatable'] = PyFunc(lambda t, m=None: t); G['getmetatable'] = PyFunc(lambda t: None)
    G['rawget'] = PyFunc(lambda t, k: t.get(k) if isinstance(t, LTab) else None)
    G['select'] = PyFunc(lambda n, *a: (len(a),) if n == '#' else tuple(a[int(n) - 1:]))
    G['next'] = PyFunc(lambda t, k=None: (None,))
    G['_G'] = STUB
