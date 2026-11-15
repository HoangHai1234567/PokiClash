import sys, os
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import io, contextlib
import rua_lua_rig as R
ref = R.CD["idle_01"][1]
for clip in ("idle_01", "run_01", "hit_01", "die_01", "skill_02", "skill_03", "skill_04"):
    dur, res = R.CD[clip]
    print(clip, round(dur, 2), {b: (round(float(res[b][:, 0].min() - ref[b][0, 0])), round(float(res[b][:, 0].max() - ref[b][0, 0])))
                               for b in ("bone3", "bone4", "bone5", "bone6", "bone7", "bone34", "bone33")})
print([(b["name"], R.NB[b["parent"]]) for b in R.I["bones"] if b["name"] in ("bone5", "bone6", "bone7", "bone33", "bone34", "bone35", "bone36", "bone37")])
