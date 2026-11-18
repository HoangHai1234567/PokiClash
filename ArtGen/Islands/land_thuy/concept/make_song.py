# Bản thử sóng đập bờ (GD_Claude/18): dò biển trên ảnh concept, tính khoảng cách tới bờ, xuất trang HTML chạy shader WebGL
# (vạch bọt chạy vào bờ, đập bờ, rút ra, bụi nước), cùng cách shader InkWater sẽ làm trong Unity.
# Dùng: py -3 -I make_song.py <ảnh concept> <file html ra>
import sys, io, base64, json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, out = sys.argv[1], sys.argv[2]
img = Image.open(src).convert("RGB"); W, H = img.size
a = np.asarray(img).astype(int); R, G, B = a[..., 0], a[..., 1], a[..., 2]
seaish = (B > 195) & (G > 165) & (R < 190) & (B - R > 45)
seaish = ndi.binary_closing(seaish, iterations=2)
lab, n = ndi.label(seaish)
band = np.zeros_like(seaish); band[:15] = band[-15:] = True; band[:, :15] = band[:, -15:] = True
cnt = ndi.sum(seaish, lab, range(1, n + 1))
edge = set(np.unique(lab[band & seaish])) - {0}
edge = {i for i in edge if cnt[i - 1] > 2000}
sea = np.isin(lab, list(edge))
sea = ndi.binary_opening(sea, iterations=1)
# lỗ nhỏ trong biển (mây, thuyền, vệt trắng) coi như biển khi tính khoảng cách, để không có bọt quanh mây
holes = ndi.binary_fill_holes(sea) & ~sea
hl, hn = ndi.label(holes)
sizes = ndi.sum(holes, hl, range(1, hn + 1))
small = np.isin(hl, [i + 1 for i, s in enumerate(sizes) if s < 30000])
sea_for_dist = sea | small
# ngoài mép ảnh coi là biển: dải mép nối với biển thì bật lên, rồi đệm 100 px để mép ảnh không thành "bờ"
M = 24; bandm = np.zeros_like(sea); bandm[:M] = bandm[-M:] = True; bandm[:, :M] = bandm[:, -M:] = True
near = ndi.binary_dilation(sea_for_dist, iterations=M)
sea_for_dist = sea_for_dist | (bandm & near & ~ndi.binary_dilation(~sea_for_dist & ~bandm, iterations=3))
pad = np.pad(sea_for_dist, 100, constant_values=True)
dist = ndi.distance_transform_edt(pad)[100:-100, 100:-100]
draw = (sea | (sea_for_dist & bandm)) & ~ndi.binary_dilation(small, iterations=2)   # không vẽ sóng đè lên mây, thuyền
rg = np.zeros((H, W, 3), np.uint8)
rg[..., 0] = np.clip(dist * 4, 0, 255).astype(np.uint8)
rg[..., 1] = draw.astype(np.uint8) * 255
def b64(im, fmt, **kw):
    bio = io.BytesIO(); im.save(bio, fmt, **kw); return base64.b64encode(bio.getvalue()).decode()
base64img = b64(img, "JPEG", quality=92)
base64dist = b64(Image.fromarray(rg), "PNG")
Image.fromarray(rg).save(out.replace(".html", "_dist.png"))

html = """<!doctype html><html><head><meta charset="utf-8"><title>Sóng đập bờ</title>
<style>html,body{margin:0;background:#2b2b2b;color:#ddd;font:14px sans-serif}canvas{display:block;margin:8px auto;max-width:98vw;height:auto}
#ui{text-align:center}label{margin:0 10px}</style></head><body>
<div id="ui">Bản thử sóng đập bờ (shader). <label>Tốc độ <input id="sp" type="range" min="0.3" max="3" step="0.1" value="1"></label>
<label><input id="on" type="checkbox" checked> Bật sóng</label></div>
<canvas id="c" width="__W__" height="__H__"></canvas>
<script>
const W=__W__,H=__H__;const gl=document.getElementById('c').getContext('webgl');
const vs=`attribute vec2 p;varying vec2 uv;void main(){uv=vec2(p.x*.5+.5,.5-p.y*.5);gl_Position=vec4(p,0,1);}`;
const fs=`precision highp float;varying vec2 uv;uniform sampler2D uB,uD;uniform float t,on;uniform vec2 res;
float h(vec2 q){return fract(sin(dot(q,vec2(127.1,311.7)))*43758.5453);}
float vn(vec2 q){vec2 i=floor(q),f=fract(q);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
void main(){vec4 b=texture2D(uB,uv);vec2 m=texture2D(uD,uv).rg;float d=m.r*64.;
 if(m.g<.5||on<.5){gl_FragColor=b;return;}
 vec2 p=uv*res;float n=(vn(p*.018+vec2(t*.04,0.))-.5)*14.;float dd=d+n;
 float per=22.,sp=9.;float f=fract((dd+t*sp)/per);
 float line=smoothstep(0.,.04,f)*(1.-smoothstep(.11,.19,f));
 float ink=smoothstep(.19,.22,f)*(1.-smoothstep(.22,.28,f));
 float fade=1.-smoothstep(5.,46.,d);
 float br=(vn(p*.006)-.5)*.6;                      // mảng sóng không đều theo chỗ
 float w=.5+.5*sin(t*1.3+vn(p*.009)*6.283);        // nhịp đập bờ
 float reach=3.+w*11.;
 float wash=(1.-smoothstep(reach-1.5,reach+1.5,d));
 float washEdge=1.-smoothstep(1.,3.2,abs(d-reach));
 float hatch=.72+.28*step(.5,fract((p.x+p.y)*.22));
 float spray=step(.9,h(floor(p/3.)+floor(t*9.)))*(1.-smoothstep(0.,7.,d))*smoothstep(.78,1.,w);
 float foam=max(line*fade*(.9+br),max(wash*.72*hatch,washEdge));foam=max(foam,spray);
 vec3 c=mix(b.rgb,vec3(.16,.42,.62),ink*fade*.45);
 c=mix(c,vec3(.985,1.,1.),clamp(foam,0.,1.)*.92);
 gl_FragColor=vec4(c,1.);}`;
function sh(t,s){const o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);if(!gl.getShaderParameter(o,gl.COMPILE_STATUS))alert(gl.getShaderInfoLog(o));return o}
const pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,vs));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,fs));gl.linkProgram(pr);gl.useProgram(pr);
const bf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,bf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
const lp=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(lp);gl.vertexAttribPointer(lp,2,gl.FLOAT,false,0,0);
function tex(src,unit,cb){const im=new Image();im.onload=()=>{const t=gl.createTexture();gl.activeTexture(gl.TEXTURE0+unit);gl.bindTexture(gl.TEXTURE_2D,t);
 gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
 gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
 gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,im);cb()};im.src=src}
let n=0;const go=()=>{if(++n<2)return;gl.uniform1i(gl.getUniformLocation(pr,'uB'),0);gl.uniform1i(gl.getUniformLocation(pr,'uD'),1);
 gl.uniform2f(gl.getUniformLocation(pr,'res'),W,H);const ut=gl.getUniformLocation(pr,'t'),uo=gl.getUniformLocation(pr,'on');
 let T=0,last=performance.now();(function f(now){T+=(now-last)/1000*parseFloat(document.getElementById('sp').value);last=now;
 gl.uniform1f(ut,T);gl.uniform1f(uo,document.getElementById('on').checked?1:0);gl.drawArrays(gl.TRIANGLE_STRIP,0,4);requestAnimationFrame(f)})(last)};
tex('data:image/jpeg;base64,__IMG__',0,go);tex('data:image/png;base64,__DIST__',1,go);
</script></body></html>"""
html = html.replace("__W__", str(W)).replace("__H__", str(H)).replace("__IMG__", base64img).replace("__DIST__", base64dist)
open(out, "w", encoding="utf-8").write(html)
print("sea px", int(sea.sum()), "of", W * H, "->", out)
