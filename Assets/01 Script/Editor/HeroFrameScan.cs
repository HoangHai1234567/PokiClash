// Quét khung hình tướng (2026-11-20, người dùng: "quét lại các animation các tướng xem con nào lỗi, cắt outline lỗi thì sửa").
// Mọi prefab × dạng × clip × thời điểm, dựng đúng đường game: AolaActor (rig .atomik hoặc hình aola) + khung camera của
// AolaSticker (SpanFor theo AtomikAsset.fit, bám xương move, dời theo đích ở xa của trận). Đo đỉnh lưới thật so với khung chụp ra
// RenderTexture: hình + viền giấy (5,5 điểm ảnh ở ảnh 512 = 0,0365 chiều cao dáng đứng) lọt ra ngoài khung là bị mép ảnh cắt.
// Kèm: tam giác mất vì mặt nạ cắt hết chỗ chừa (AtomikPose.Dropped), đỉnh NaN.
// Chỉ tính bằng CPU (không vẽ GPU: máy từng sập khi vẽ hàng loạt khung). Tiến độ ở Library/PokiHeroScan/status.txt, kết quả
// frame_scan.csv + frame_scan.md cùng thư mục.
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.Game;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class HeroFrameScan
    {
        // như AolaSticker
        const float DefSpan = 3.4f, FootV = 0.2f, FitMargin = 0.06f, MaxSpan = 8f;
        const float Outline = 5.5f * DefSpan / 512f; // viền trắng 3 + mực 2,5 điểm ảnh của ảnh 512 ở khung DefSpan
        const float Fps = 40;                        // mẫu mỗi giây (rig .atomik chạy liên tục)
        const int AuraPhases = 8;                    // số pha clip aura thử cho mỗi thời điểm

        // nơi tướng hiện: lật, chiều cao dáng đứng trên sân, đích ở xa (đơn vị sân, y xuống), có dời khung theo đích
        sealed class Ctx
        {
            public string name;
            public bool flip, shift;
            public float h;
            public Vector2 to;
        }

        // StageView.Pos/Height: phe ta (392,418) cao 176 quay trái; địch (158,236) cao 150; đích = Body(đối thủ) − chỗ mình.
        // Ô xem tướng (HeroViewer, màn boot, ô trứng): FarAhead(1,3), không dời khung.
        static readonly Ctx[] FarCtxs =
        {
            new Ctx { name = "tran_ta", flip = true, shift = true, h = 176, to = new Vector2(158 - 392, 236 - 150 * 0.45f - 418) },
            new Ctx { name = "tran_dich", flip = false, shift = true, h = 150, to = new Vector2(392 - 158, 418 - 176 * 0.45f - 236) },
            new Ctx { name = "o_xem", flip = false, shift = false, h = 100, to = new Vector2(130, -40) },
        };

        static readonly string[] Clips =
        {
            AolaActor.Idle, AolaActor.Hit, AolaActor.Attack, AolaActor.Cast, AolaActor.Skill, AolaActor.SkillLand,
            AolaActor.Evolve, AolaActor.Appear, AolaActor.Die, AolaSticker.Walk,
        };

        // clip sân gọi Far (StageView: đòn bắn từ xa); skill_land chạy tiếp sau skill, giữ đích + khung dời của skill
        static bool FarCaller(string c) => c == AolaActor.Attack || c == AolaActor.Skill || c == AolaActor.Cast || c == AolaActor.SkillLand;

        static string OutDir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Library/PokiHeroScan"));

        sealed class Row
        {
            public string prefab, formName, kind, ctx, clip, hint;
            public int form, samples, cutSamples, dropped, nan;
            public float dur, span, need;
            public bool capped;
            public float ovL = float.NegativeInfinity, ovR = float.NegativeInfinity, ovB = float.NegativeInfinity, ovT = float.NegativeInfinity;
            public float artL = float.NegativeInfinity, artR = float.NegativeInfinity, artB = float.NegativeInfinity, artT = float.NegativeInfinity;
            public float tL, tR, tB, tT;
            public float Worst => Mathf.Max(Mathf.Max(ovL, ovR), Mathf.Max(ovB, ovT));
            public float WorstArt => Mathf.Max(Mathf.Max(artL, artR), Mathf.Max(artB, artT));
        }

        sealed class FormInfo
        {
            public string prefab, formName;
            public int form, maxVerts, safeExtra, curExtra, peakVerts, dropped;
        }

        [MenuItem("PokiClash/Tướng/Quét khung hình tướng (cắt viền, mất mảnh)", priority = 59)]
        public static void ScanMenu() => Scan();

        public static string Scan()
        {
            var lib = AssetDatabase.LoadAssetAtPath<HeroModels>(AolaImport.LibraryPath);
            Directory.CreateDirectory(OutDir);
            var status = Path.Combine(OutDir, "status.txt");
            var rows = new List<Row>();
            var infos = new List<FormInfo>();
            var vl = new List<Vector3>();
            var cl = new List<Color32>();
            var tl = new List<int>();
            int forms = 0;
            var watch = System.Diagnostics.Stopwatch.StartNew();
            try
            {
                var prefabs = lib.heroes.Where(p => p).ToArray();
                for (int pi = 0; pi < prefabs.Length; pi++)
                {
                    var prefab = prefabs[pi];
                    var fl = prefab.Forms;
                    for (int f = 0; f < fl.Length; f++)
                    {
                        if (!fl[f]) continue;
                        forms++;
                        File.WriteAllText(status, $"RUN {pi + 1}/{prefabs.Length} {prefab.name} dạng {f + 1} ({fl[f].name}) {watch.Elapsed.TotalSeconds:0}s\n");
                        if (EditorUtility.DisplayCancelableProgressBar("Quét khung hình tướng", $"{prefab.name} dạng {f + 1}", (pi + f / (float)fl.Length) / prefabs.Length))
                            throw new System.OperationCanceledException();
                        ScanForm(prefab, f, fl[f], rows, infos, vl, cl, tl);
                    }
                }
            }
            catch (System.OperationCanceledException)
            {
                File.WriteAllText(status, "CANCELLED\n");
                return "huỷ";
            }
            finally
            {
                AolaActor.AuraClock = null;
                EditorUtility.ClearProgressBar();
            }
            WriteCsv(rows);
            var md = Summary(rows, infos, forms, watch.Elapsed.TotalSeconds);
            File.WriteAllText(Path.Combine(OutDir, "frame_scan.md"), md);
            File.WriteAllText(status, $"DONE {forms} dạng, {rows.Count} clip, {watch.Elapsed.TotalSeconds:0}s\n");
            Debug.Log("[HeroFrameScan] " + md.Split('\n').Take(12).Aggregate((a, b) => a + "\n" + b));
            return md;
        }

        static void ScanForm(AolaActor prefab, int f, AolaAnim anim, List<Row> rows, List<FormInfo> infos,
                             List<Vector3> vl, List<Color32> cl, List<int> tl)
        {
            var rig = anim.atomik;
            string kind = rig ? "atomik" : "aola";
            float auraDur = 0;
            if (rig)
            {
                int ai = rig.FindClip("aura");
                if (ai >= 0) auraDur = rig.anims[ai].dur;
            }
            var info = new FormInfo { prefab = prefab.name, form = f + 1, formName = anim.name };
            if (rig)
            {
                info.maxVerts = new AtomikPose(rig).maxVerts;
                Capacity(rig, out info.curExtra, out info.safeExtra);
            }
            infos.Add(info);

            // lật ngang chỉ đổi phía khi khung đối xứng (không dời): clip thường đo một lần không lật; clip có đích ở xa đo từng nơi hiện
            foreach (bool flip in new[] { false, true })
            {
                var actor = (AolaActor)PrefabUtility.InstantiatePrefab(prefab);
                actor.gameObject.hideFlags = HideFlags.HideAndDontSave;
                actor.transform.position = new Vector3(7000, 0, 0);
                actor.Manual = true;
                actor.SplitFx = true;
                try
                {
                    if (!actor.LoadForm(f, 1f, flip, 0))
                    {
                        if (!flip) rows.Add(new Row { prefab = prefab.name, form = f + 1, formName = anim.name, kind = kind, ctx = "-", clip = "-", hint = "không nạp được" });
                        continue;
                    }
                    foreach (var clip in Clips)
                    {
                        if (!actor.HasClip(clip)) continue;
                        string farName = clip == AolaActor.SkillLand ? AolaActor.Skill : clip;
                        bool far = FarCaller(clip) && actor.HasFar(farName);
                        if (!far)
                        {
                            if (flip) continue;
                            rows.Add(ScanClip(actor, prefab.name, f, anim.name, kind, clip, null, auraDur, info, vl, cl, tl));
                            continue;
                        }
                        foreach (var ctx in FarCtxs)
                            if (ctx.flip == flip)
                                rows.Add(ScanClip(actor, prefab.name, f, anim.name, kind, clip, ctx, auraDur, info, vl, cl, tl));
                    }
                }
                finally
                {
                    AolaActor.AuraClock = null;
                    Object.DestroyImmediate(actor.gameObject);
                }
            }
        }

        static Row ScanClip(AolaActor actor, string prefab, int f, string formName, string kind, string clip, Ctx ctx, float auraDur,
                            FormInfo info, List<Vector3> vl, List<Color32> cl, List<int> tl)
        {
            var row = new Row { prefab = prefab, form = f + 1, formName = formName, kind = kind, clip = clip, ctx = ctx != null ? ctx.name : "chung" };
            // đích ở xa + khung dời như AolaSticker.Far
            var shift = Vector2.zero;
            string farName = clip == AolaActor.SkillLand ? AolaActor.Skill : clip;
            if (ctx == null) actor.SetFarTarget(null);
            else
            {
                float h = Mathf.Max(1, ctx.h);
                var d = ctx.to;
                actor.SetFarTarget(new Vector2((ctx.flip ? -d.x : d.x) / h, -d.y / h));
                if (ctx.shift)
                {
                    float up = -d.y / h;
                    shift = new Vector2(Mathf.Clamp(d.x / h * 0.5f, -1.1f, 1.1f), up > 0 ? Mathf.Clamp(up - 1.9f, 0, 0.8f) : Mathf.Max(up * 0.5f, -0.8f));
                }
            }
            row.span = SpanFor(actor, clip, out row.need);
            row.capped = row.need > MaxSpan + 1e-3f && row.need > Mathf.Max(DefSpan, actor.Span);
            row.dur = actor.Duration(clip);
            bool atomik = kind == "atomik";
            int dropped0 = AtomikPose.Dropped;
            var origin = actor.transform.position;
            int steps = atomik ? Mathf.Max(1, Mathf.CeilToInt(row.dur * Fps)) : Mathf.Max(1, actor.FrameCount(clip));
            int phases = auraDur > 0 ? AuraPhases : 1;
            for (int i = 0; i <= steps; i++)
            {
                if (!atomik && i == steps) break;
                float t = atomik ? Mathf.Min(row.dur, i / Fps) : 0;
                for (int k = 0; k < phases; k++)
                {
                    if (auraDur > 0) AolaActor.AuraClock = auraDur * k / AuraPhases;
                    if (atomik) actor.ShowTime(clip, t, false);
                    else actor.ShowFrame(clip, i);
                    var follow = actor.Follow;
                    float s = row.span;
                    float cx = follow.x + shift.x, cy = follow.y + shift.y;
                    float L = cx - s / 2, R = cx + s / 2, B = cy - FootV * s, T = cy + (1 - FootV) * s;
                    float tt = atomik ? t : (i + 0.5f) / Mathf.Max(1, actor.FrameCount(clip)) * row.dur;
                    bool cut = Measure(actor, origin, L, R, B, T, tt, row, info, vl, cl, tl);
                    row.samples++;
                    if (cut) row.cutSamples++;
                }
            }
            row.dropped = AtomikPose.Dropped - dropped0;
            info.dropped += row.dropped;
            row.hint = Hint(row, actor, auraDur, ctx);
            return row;
        }

        // đo mọi lưới đang hiện của tướng; true nếu hình hay viền lọt khỏi khung
        static bool Measure(AolaActor actor, Vector3 origin, float L, float R, float B, float T, float t, Row row, FormInfo info,
                            List<Vector3> vl, List<Color32> cl, List<int> tl)
        {
            bool cut = false;
            foreach (var mf in actor.GetComponentsInChildren<MeshFilter>(true))
            {
                var r = mf.GetComponent<MeshRenderer>();
                var mesh = mf.sharedMesh;
                if (!r || !r.enabled || !mesh || mesh.vertexCount == 0) continue;
                bool plain = mf.gameObject.name == "atomik_fx"; // hạt không viền giấy, camera thứ hai cùng khung, đặt cao FxLift
                float lift = plain ? AolaActor.FxLift : 0, m = plain ? 0 : Outline;
                if (!plain) info.peakVerts = Mathf.Max(info.peakVerts, mesh.vertexCount);
                mesh.GetVertices(vl);
                mesh.GetColors(cl);
                mesh.GetTriangles(tl, 0);
                var tr = mf.transform;
                for (int q = 0; q + 2 < tl.Count; q += 3)
                {
                    if (tl[q] == tl[q + 1] && tl[q] == tl[q + 2]) continue; // tam giác rỗng (chỗ dư của mặt nạ cắt)
                    for (int e = 0; e < 3; e++)
                    {
                        int vi = tl[q + e];
                        if (vi >= vl.Count) continue;
                        if (cl.Count == vl.Count && cl[vi].a < 8) continue;
                        var w = tr.TransformPoint(vl[vi]) - origin;
                        w.y -= lift;
                        if (float.IsNaN(w.x) || float.IsNaN(w.y) || float.IsInfinity(w.x) || float.IsInfinity(w.y)) { row.nan++; continue; }
                        cut |= Upd(ref row.ovL, ref row.tL, L - w.x + m, t);
                        cut |= Upd(ref row.ovR, ref row.tR, w.x + m - R, t);
                        cut |= Upd(ref row.ovB, ref row.tB, B - w.y + m, t);
                        cut |= Upd(ref row.ovT, ref row.tT, w.y + m - T, t);
                        row.artL = Mathf.Max(row.artL, L - w.x);
                        row.artR = Mathf.Max(row.artR, w.x - R);
                        row.artB = Mathf.Max(row.artB, B - w.y);
                        row.artT = Mathf.Max(row.artT, w.y - T);
                    }
                }
            }
            return cut;
        }

        static bool Upd(ref float best, ref float at, float v, float t)
        {
            if (v > best) { best = v; at = t; }
            return v > 0;
        }

        // như AolaSticker.SpanFor; need: khung clip cần trước khi kẹp
        static float SpanFor(AolaActor a, string clip, out float need)
        {
            float span = Mathf.Max(DefSpan, a.Span);
            string c = a.HasClip(clip) ? clip : AolaActor.Idle;
            if (!a.Extent(c, out float mx, out float top, out float bot)) { need = 0; return span; }
            need = Mathf.Max(2 * (mx + FitMargin), (top + FitMargin) / (1 - FootV), (FitMargin - bot) / FootV);
            return Mathf.Clamp(need, span, Mathf.Max(span, MaxSpan));
        }

        // chỗ chừa đỉnh mới của mặt nạ cắt: hiện có (AtomikPose: 3 đỉnh mỗi tam giác trong vùng cắt, trần 12000) và đủ chắc
        // (mỗi tam giác bị xén thành tối đa 3 + số đỉnh mặt nạ đỉnh, mỗi slot chỉ hiện một hình)
        static void Capacity(AtomikAsset a, out int cur, out int safe)
        {
            cur = safe = 0;
            if (a.masks == null || a.masks.Length == 0 || a.slots == null) return;
            int ns = a.slots.Length;
            var slotMask = new int[ns];
            for (int s = 0; s < ns; s++) slotMask[s] = -1;
            for (int m = 0; m < a.masks.Length; m++)
            {
                if (a.masks[m].verts == null || a.masks[m].verts.Length < 6) continue;
                for (int s = Mathf.Max(0, a.masks[m].slot); s <= a.masks[m].end && s < ns; s++) slotMask[s] = m;
            }
            var maxT = new int[ns];
            int clipTris = 0;
            foreach (var att in a.atts)
            {
                if (att.slot < 0 || att.slot >= ns || slotMask[att.slot] < 0) continue;
                clipTris += att.tris.Length / 3;
                maxT[att.slot] = Mathf.Max(maxT[att.slot], att.tris.Length / 3);
            }
            for (int s = 0; s < ns; s++)
                if (maxT[s] > 0) safe += maxT[s] * (3 + a.masks[slotMask[s]].verts.Length / 2);
            cur = Mathf.Min(Mathf.Max(clipTris * 3, Mathf.Min(safe, 4096)), 12000); // như AtomikPose (bản 2026-11-20)
        }

        static string Hint(Row r, AolaActor a, float auraDur, Ctx ctx)
        {
            if (r.Worst <= 0) return "";
            var h = new List<string>();
            if (r.kind == "aola") h.Add("aola: không có fit, khung cố định");
            if (r.capped) h.Add($"cần khung {r.need:0.0} > trần {MaxSpan}");
            if (auraDur > 0 && r.clip != "aura") h.Add("aura phủ lên không nằm trong fit");
            if (ctx != null && ctx.shift) h.Add("khung dời theo đích (farShift) chưa tính vào SpanFor");
            if (ctx != null && !ctx.shift) h.Add("đích ở xa, ô xem không dời khung");
            if (h.Count == 0) h.Add("khác (fit lấy mẫu thiếu?)");
            return string.Join("; ", h);
        }

        // ---------- quét xác minh qua AolaSticker thật ----------
        // Dựng sticker như sân đấu (Theme.Init, TryCreate) rồi gọi Far / FarAhead / Show như StageView, HeroViewer; đọc khung camera từ
        // ảnh của sticker (cỡ = sizeDelta / uiHeight, chỗ = anchoredPosition / uiHeight) và đo đỉnh lưới thật so với khung đó. Kiểm đúng
        // code game (AolaSticker.Fit), không phải bản mô phỏng. Ghi verify.csv + verify.md.
        const float VerifyFps = 60;
        static readonly StringBuilder verifyLog = new();

        [MenuItem("PokiClash/Tướng/Quét khung qua AolaSticker thật (xác minh)", priority = 61)]
        public static void VerifyMenu() => Verify();

        static readonly string[] StageClips =
        {
            StageView.Idle, StageView.Hit, StageView.Attack, StageView.Cast, StageView.Skill,
            AolaActor.Evolve, AolaActor.Appear, AolaActor.Die, AolaSticker.Walk,
        };

        public static string Verify()
        {
            var lib = AssetDatabase.LoadAssetAtPath<HeroModels>(AolaImport.LibraryPath);
            var guid = AssetDatabase.FindAssets("t:UiAssets").FirstOrDefault();
            var ui = guid != null ? AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(guid)) : null;
            if (!ui) return "không thấy UiAssets";
            Theme.Init(ui);
            Directory.CreateDirectory(OutDir);
            var status = Path.Combine(OutDir, "status.txt");
            var fActor = typeof(AolaSticker).GetField("actor", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
            var root = new GameObject("quet_xac_minh", typeof(RectTransform)) { hideFlags = HideFlags.HideAndDontSave };
            var rows = new List<Row>();
            var infos = new List<FormInfo>();
            var vl = new List<Vector3>();
            var cl = new List<Color32>();
            var tl = new List<int>();
            var hero = new PokiClash.Core.HeroDef { id = "quet" };
            int forms = 0;
            var watch = System.Diagnostics.Stopwatch.StartNew();
            try
            {
                // verify_only.txt (mỗi dòng một tên prefab): chỉ quét các prefab đó
                var onlyFile = Path.Combine(OutDir, "verify_only.txt");
                var only = File.Exists(onlyFile) ? new HashSet<string>(File.ReadAllLines(onlyFile).Select(x => x.Trim()).Where(x => x.Length > 0)) : null;
                verifyLog.Clear();
                var prefabs = lib.heroes.Where(p => p && (only == null || only.Contains(p.name))).ToArray();
                for (int pi = 0; pi < prefabs.Length; pi++)
                {
                    var fl = prefabs[pi].Forms;
                    for (int f = 0; f < fl.Length; f++)
                    {
                        if (!fl[f] || !fl[f].atomik) continue; // chỉ rig .atomik (người dùng 2026-11-20: hình aola không làm)
                        forms++;
                        File.WriteAllText(status, $"VERIFY {pi + 1}/{prefabs.Length} {prefabs[pi].name} dạng {f + 1} {watch.Elapsed.TotalSeconds:0}s\n");
                        if (EditorUtility.DisplayCancelableProgressBar("Quét xác minh khung", $"{prefabs[pi].name} dạng {f + 1}", (pi + f / (float)fl.Length) / prefabs.Length))
                            throw new System.OperationCanceledException();
                        var anim = fl[f];
                        float auraDur = 0;
                        if (anim.atomik)
                        {
                            int ai = anim.atomik.FindClip("aura");
                            if (ai >= 0) auraDur = anim.atomik.anims[ai].dur;
                        }
                        var info = new FormInfo { prefab = prefabs[pi].name, form = f + 1, formName = anim.name };
                        if (anim.atomik)
                        {
                            info.maxVerts = new AtomikPose(anim.atomik).maxVerts;
                            Capacity(anim.atomik, out info.curExtra, out info.safeExtra);
                        }
                        infos.Add(info);
                        // sticker phe địch (không lật, cao 150): clip thường, đích của trận, ô xem; sticker phe ta (lật, cao 176)
                        foreach (var (flip, h) in new[] { (false, 150f), (true, 176f) })
                        {
                            var st = AolaSticker.TryCreate((RectTransform)root.transform, hero, anim.name, h * StageView.K, flip);
                            if (st == null) { rows.Add(new Row { prefab = prefabs[pi].name, form = f + 1, formName = anim.name, kind = "?", ctx = "-", clip = "-", hint = "không nạp được" }); break; }
                            try
                            {
                                var actor = (AolaActor)fActor.GetValue(st);
                                var img = st.Rect.GetComponentInChildren<RawImage>(true);
                                float uiH = h * StageView.K;
                                foreach (var clip in StageClips)
                                {
                                    if (!st.HasClip(clip)) continue;
                                    bool farClip = clip == StageView.Attack || clip == StageView.Skill || clip == StageView.Cast;
                                    var ctxs = flip ? (farClip ? new[] { "tran_ta" } : new string[0])
                                                    : farClip ? new[] { "chung", "tran_dich", "o_xem" } : new[] { "chung" };
                                    foreach (var ctx in ctxs)
                                        rows.Add(VerifyClip(st, actor, img, uiH, prefabs[pi].name, f, anim, clip, ctx, auraDur, info, vl, cl, tl));
                                }
                            }
                            finally
                            {
                                AolaActor.AuraClock = null;
                                DestroySticker(st);
                            }
                        }
                    }
                }
            }
            catch (System.OperationCanceledException)
            {
                File.WriteAllText(status, "CANCELLED\n");
                return "huỷ";
            }
            finally
            {
                AolaActor.AuraClock = null;
                Object.DestroyImmediate(root);
                EditorUtility.ClearProgressBar();
            }
            WriteCsv(rows, "verify.csv");
            var md = Summary(rows, infos, forms, watch.Elapsed.TotalSeconds, "Quét xác minh qua AolaSticker thật");
            // khung nới cỡ (độ nét đổi): clip nào cần khung lớn hơn khung nền
            var grown = rows.Where(r => r.need > r.span + 1e-3f).OrderByDescending(r => r.need / Mathf.Max(1e-3f, r.span)).ToList();
            md += $"\n## Khung phải nới cỡ (độ nét giảm trong clip đó): {grown.Count} clip\n";
            foreach (var r in grown.Take(60))
                md += $"- {r.prefab} dạng {r.form} ({r.formName}) {r.clip} [{r.ctx}]: khung nền {r.span:0.00} → {r.need:0.00} (×{r.need / r.span:0.00})\n";
            File.WriteAllText(Path.Combine(OutDir, "verify.md"), md);
            File.WriteAllText(Path.Combine(OutDir, "verify_cuts.txt"), verifyLog.ToString());
            File.WriteAllText(status, $"DONE VERIFY {forms} dạng, {rows.Count} clip, {watch.Elapsed.TotalSeconds:0}s\n");
            Debug.Log("[HeroFrameScan] " + md.Split('\n').Take(8).Aggregate((a, b) => a + "\n" + b));
            return md;
        }

        // Row.span: khung nền lúc bắt đầu clip; Row.need: khung lớn nhất sticker dùng trong clip
        static Row VerifyClip(AolaSticker st, AolaActor actor, RawImage img, float uiH, string prefab, int f, AolaAnim anim, string clip,
                              string ctx, float auraDur, FormInfo info, List<Vector3> vl, List<Color32> cl, List<int> tl)
        {
            var row = new Row { prefab = prefab, form = f + 1, formName = anim.name, kind = anim.atomik ? "atomik" : "aola", clip = clip, ctx = ctx };
            var c = FarCtxs.FirstOrDefault(x => x.name == ctx);
            if (ctx == "o_xem") st.FarAhead(clip, 1.3f);
            else st.Far(clip, c != null ? c.to : (Vector2?)null);
            row.dur = st.Duration(clip);
            int dropped0 = AtomikPose.Dropped;
            var origin = actor.transform.position;
            int steps = Mathf.Max(1, Mathf.CeilToInt(row.dur * VerifyFps));
            int phases = auraDur > 0 ? AuraPhases : 1;
            row.span = -1;
            for (int i = 0; i <= steps; i++)
            {
                float t = Mathf.Min(row.dur, i / VerifyFps);
                for (int k = 0; k < phases; k++)
                {
                    if (auraDur > 0) AolaActor.AuraClock = auraDur * k / AuraPhases;
                    st.Show(clip, t, false, 1, false, 0);
                    var r = img.rectTransform;
                    float s = r.sizeDelta.x / uiH;
                    var w = r.anchoredPosition / uiH;
                    if (row.span < 0) row.span = s;
                    row.need = Mathf.Max(row.need, s);
                    float L = w.x - s / 2, R = w.x + s / 2, B = w.y - FootV * s, T = w.y + (1 - FootV) * s;
                    bool cut = Measure(actor, origin, L, R, B, T, t, row, info, vl, cl, tl);
                    row.samples++;
                    if (cut)
                    {
                        row.cutSamples++;
                        if (row.cutSamples <= 4)
                        {
                            actor.Drawn(out var lo, out var hi);
                            verifyLog.AppendLine(string.Format(CultureInfo.InvariantCulture,
                                "{0} d{1} {2} [{3}] t={4:0.000} pha={5}: khung x[{6:0.000},{7:0.000}] y[{8:0.000},{9:0.000}] s={10:0.000}; " +
                                "drawn x[{11:0.000},{12:0.000}] y[{13:0.000},{14:0.000}]; follow ({15:0.000},{16:0.000}); lọt L{17:0.000} R{18:0.000} B{19:0.000} T{20:0.000}",
                                prefab, f + 1, clip, ctx, t, k, L, R, B, T, s, lo.x, hi.x, lo.y, hi.y, actor.Follow.x, actor.Follow.y,
                                row.ovL, row.ovR, row.ovB, row.ovT));
                        }
                    }
                }
            }
            row.capped = row.need >= MaxSpan - 1e-3f;
            row.dropped = AtomikPose.Dropped - dropped0;
            info.dropped += row.dropped;
            row.hint = row.Worst > 0 ? (row.capped ? $"chạm trần khung {MaxSpan}" : "lọt khung dù đã nới (kiểm lại)") : "";
            return row;
        }

        // AolaSticker.Destroy dùng Object.Destroy (chỉ chạy lúc Play): dọn tay
        static void DestroySticker(AolaSticker st)
        {
            const System.Reflection.BindingFlags NP = System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance;
            foreach (var name in new[] { "rt", "fxRt" })
                if (typeof(AolaSticker).GetField(name, NP)?.GetValue(st) is RenderTexture t && t) { t.Release(); Object.DestroyImmediate(t); }
            foreach (var name in new[] { "mat", "fxMat" })
                if (typeof(AolaSticker).GetField(name, NP)?.GetValue(st) is Material m && m) Object.DestroyImmediate(m);
            if (typeof(AolaSticker).GetField("world", NP)?.GetValue(st) is GameObject go && go) Object.DestroyImmediate(go);
            if (st.Rect) Object.DestroyImmediate(st.Rect.gameObject);
        }

        // ---------- chụp chẩn đoán ----------
        // Library/PokiHeroScan/diag_list.txt, mỗi dòng: prefab,dạng(1..),clip,nơi hiện(chung|tran_ta|tran_dich|o_xem),t1;t2;...
        // Mỗi dòng một tờ: mỗi thời điểm một ô vẽ rộng quanh tướng, khung ảnh của game kẻ đỏ, mép viền giấy cam, chân chấm xanh.
        // Vẽ GPU từng ô một (vài chục ô), nền be như AtomikForms.Shot. "cũ": khung theo cách tính trước 2026-11-20 (SpanFor + dời nửa
        // quãng); "mới": khung lấy từ AolaSticker thật (Fit). Tờ ghi diag/<...>_cu.png hoặc _moi.png.
        [MenuItem("PokiClash/Tướng/Chụp chẩn đoán khung (diag_list.txt)", priority = 60)]
        public static void DiagMenu() => Diag(false);

        [MenuItem("PokiClash/Tướng/Chụp chẩn đoán khung qua AolaSticker thật (diag_list.txt)", priority = 60)]
        public static void DiagNewMenu() => Diag(true);

        public static string Diag(bool real)
        {
            var lib = AssetDatabase.LoadAssetAtPath<HeroModels>(AolaImport.LibraryPath);
            if (real)
            {
                var guid = AssetDatabase.FindAssets("t:UiAssets").FirstOrDefault();
                var ui = guid != null ? AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(guid)) : null;
                if (!ui) return "không thấy UiAssets";
                Theme.Init(ui);
            }
            var fActor = typeof(AolaSticker).GetField("actor", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
            var stRoot = new GameObject("chan_doan_root", typeof(RectTransform)) { hideFlags = HideFlags.HideAndDontSave };
            var listFile = Path.Combine(OutDir, "diag_list.txt");
            if (!File.Exists(listFile)) return "không có " + listFile;
            var outDir = Path.Combine(OutDir, "diag");
            Directory.CreateDirectory(outDir);
            const int Cell = 320;
            var rt = new RenderTexture(Cell, Cell, 16, RenderTextureFormat.ARGB32);
            var camGo = new GameObject("cam_chan_doan") { hideFlags = HideFlags.HideAndDontSave };
            var cam = camGo.AddComponent<Camera>();
            cam.orthographic = true;
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0.93f, 0.89f, 0.80f, 1);
            cam.targetTexture = rt;
            cam.nearClipPlane = 0.1f;
            cam.farClipPlane = 50;
            cam.enabled = false;
            var log = new List<string>();
            var vl = new List<Vector3>();
            var cl = new List<Color32>();
            var tl = new List<int>();
            try
            {
                foreach (var raw in File.ReadAllLines(listFile))
                {
                    var line = raw.Trim();
                    if (line.Length == 0 || line.StartsWith("#")) continue;
                    var p = line.Split(',');
                    var prefab = lib.heroes.FirstOrDefault(h => h && h.name == p[0]);
                    int f = int.Parse(p[1]) - 1;
                    string clip = p[2];
                    var ctx = FarCtxs.FirstOrDefault(c => c.name == p[3]);
                    var times = p[4].Split(';').Select(s => float.Parse(s, CultureInfo.InvariantCulture)).ToArray();
                    if (!prefab || f < 0 || f >= prefab.Forms.Length) { log.Add("bỏ: " + line); continue; }
                    AolaSticker st = null;
                    AolaActor actor;
                    RawImage stImg = null;
                    float uiH = 0;
                    if (real)
                    {
                        bool fl = ctx != null && ctx.flip;
                        uiH = (fl ? 176f : 150f) * StageView.K;
                        st = AolaSticker.TryCreate((RectTransform)stRoot.transform, new PokiClash.Core.HeroDef { id = "chan_doan" }, prefab.Forms[f].name, uiH, fl);
                        if (st == null) { log.Add("không nạp: " + line); continue; }
                        actor = (AolaActor)fActor.GetValue(st);
                        stImg = st.Rect.GetComponentInChildren<RawImage>(true);
                    }
                    else
                    {
                        actor = (AolaActor)PrefabUtility.InstantiatePrefab(prefab);
                        actor.gameObject.hideFlags = HideFlags.HideAndDontSave;
                        actor.transform.position = new Vector3(7000, 0, 0);
                        actor.Manual = true;
                    }
                    actor.SplitFx = false; // một lưới: hạt không viền vẽ chung cho dễ nhìn
                    var sheet = new Texture2D(Cell * times.Length, Cell, TextureFormat.RGBA32, false);
                    try
                    {
                        if (!real && !actor.LoadForm(f, 1f, ctx != null && ctx.flip, 0)) { log.Add("không nạp: " + line); continue; }
                        var shift = Vector2.zero;
                        string sc = StageName(clip);
                        if (real)
                        {
                            if (p[3] == "o_xem") st.FarAhead(sc, 1.3f);
                            else st.Far(sc, ctx != null && ctx.shift ? ctx.to : (Vector2?)null);
                        }
                        else if (ctx == null) actor.SetFarTarget(null);
                        else
                        {
                            float h = Mathf.Max(1, ctx.h);
                            var d = ctx.to;
                            actor.SetFarTarget(new Vector2((ctx.flip ? -d.x : d.x) / h, -d.y / h));
                            if (ctx.shift)
                            {
                                float up = -d.y / h;
                                shift = new Vector2(Mathf.Clamp(d.x / h * 0.5f, -1.1f, 1.1f), up > 0 ? Mathf.Clamp(up - 1.9f, 0, 0.8f) : Mathf.Max(up * 0.5f, -0.8f));
                            }
                        }
                        float s = real ? 0 : SpanFor(actor, clip, out _);
                        bool atomik = prefab.Forms[f].atomik;
                        var origin = actor.transform.position;
                        for (int i = 0; i < times.Length; i++)
                        {
                            Rect win;
                            if (real)
                            {
                                st.Show(sc, times[i], false, 1, false, 0);
                                var ir = stImg.rectTransform;
                                s = ir.sizeDelta.x / uiH;
                                var w = ir.anchoredPosition / uiH;
                                win = new Rect(w.x - s / 2, w.y - FootV * s, s, s);
                            }
                            else
                            {
                                if (atomik) actor.ShowTime(clip, times[i], false);
                                else actor.ShowFrame(clip, Mathf.FloorToInt(times[i] * actor.FrameCount(clip) / Mathf.Max(1e-3f, actor.Duration(clip))));
                                var fo = actor.Follow;
                                float cx = fo.x + shift.x, cy = fo.y + shift.y;
                                win = new Rect(cx - s / 2, cy - FootV * s, s, s);
                            }
                            // khung vẽ rộng: ôm khung game + mọi đỉnh đang hiện; cột 6 = "can": chỉ ôm hình (soi cận)
                            bool close = p.Length > 5 && p[5].Trim() == "can";
                            float x0 = close ? float.MaxValue : win.xMin, x1 = close ? float.MinValue : win.xMax;
                            float y0 = close ? float.MaxValue : win.yMin, y1 = close ? float.MinValue : win.yMax;
                            foreach (var mf in actor.GetComponentsInChildren<MeshFilter>(true))
                            {
                                var r = mf.GetComponent<MeshRenderer>();
                                if (!r || !r.enabled || !mf.sharedMesh) continue;
                                mf.sharedMesh.GetVertices(vl);
                                foreach (var v in vl)
                                {
                                    var w = mf.transform.TransformPoint(v) - origin;
                                    x0 = Mathf.Min(x0, w.x); x1 = Mathf.Max(x1, w.x);
                                    y0 = Mathf.Min(y0, w.y); y1 = Mathf.Max(y1, w.y);
                                }
                            }
                            float view = Mathf.Max(x1 - x0, y1 - y0) * 1.08f;
                            var c = new Vector2((x0 + x1) / 2, (y0 + y1) / 2);
                            cam.orthographicSize = view / 2;
                            camGo.transform.position = origin + new Vector3(c.x, c.y, -10);
                            cam.Render();
                            RenderTexture.active = rt;
                            var t = new Texture2D(Cell, Cell, TextureFormat.RGBA32, false);
                            t.ReadPixels(new Rect(0, 0, Cell, Cell), 0, 0);
                            RenderTexture.active = null;
                            var px = t.GetPixels32();
                            Object.DestroyImmediate(t);
                            System.Func<float, float, Vector2Int> P = (wx, wy) => new Vector2Int(
                                Mathf.RoundToInt((wx - (c.x - view / 2)) / view * Cell), Mathf.RoundToInt((wy - (c.y - view / 2)) / view * Cell));
                            DrawRect(px, Cell, P(win.xMin - Outline, win.yMin - Outline), P(win.xMax + Outline, win.yMax + Outline), new Color32(230, 140, 20, 255));
                            DrawRect(px, Cell, P(win.xMin, win.yMin), P(win.xMax, win.yMax), new Color32(220, 20, 20, 255));
                            DrawRect(px, Cell, P(win.xMin + 0.002f, win.yMin + 0.002f), P(win.xMax - 0.002f, win.yMax - 0.002f), new Color32(220, 20, 20, 255));
                            var o = P(0, 0);
                            for (int dy = -2; dy <= 2; dy++)
                                for (int dx = -2; dx <= 2; dx++)
                                    Put(px, Cell, o.x + dx, o.y + dy, new Color32(20, 120, 220, 255));
                            sheet.SetPixels32(i * Cell, 0, Cell, Cell, px);
                        }
                        sheet.Apply();
                        string name = $"{p[0]}_{f + 1}_{clip}_{p[3]}_{(real ? "moi" : "cu")}.png";
                        File.WriteAllBytes(Path.Combine(outDir, name), sheet.EncodeToPNG());
                        log.Add($"{name}: khung {s:0.00}, t={p[4]}");
                    }
                    finally
                    {
                        Object.DestroyImmediate(sheet);
                        if (real) DestroySticker(st);
                        else Object.DestroyImmediate(actor.gameObject);
                    }
                }
            }
            finally
            {
                Object.DestroyImmediate(stRoot);
                Object.DestroyImmediate(camGo);
                rt.Release();
                Object.DestroyImmediate(rt);
            }
            var msg = "[HeroFrameScan] chụp chẩn đoán vào " + outDir + "\n" + string.Join("\n", log);
            File.WriteAllText(Path.Combine(OutDir, "diag_log.txt"), msg + "\nDONE\n");
            Debug.Log(msg);
            return msg;
        }

        // tên clip của AolaActor (1_4...) sang tên StageView mà AolaSticker.Show nhận; clip khác (appear, die...) giữ nguyên
        static string StageName(string c) =>
            c == AolaActor.Idle ? StageView.Idle : c == AolaActor.Hit ? StageView.Hit : c == AolaActor.Attack ? StageView.Attack :
            c == AolaActor.Cast ? StageView.Cast : c == AolaActor.Skill ? StageView.Skill : c;

        static void Put(Color32[] px, int n, int x, int y, Color32 c)
        {
            if (x >= 0 && y >= 0 && x < n && y < n) px[y * n + x] = c;
        }

        static void DrawRect(Color32[] px, int n, Vector2Int a, Vector2Int b, Color32 c)
        {
            for (int x = a.x; x <= b.x; x++) { Put(px, n, x, a.y, c); Put(px, n, x, b.y, c); }
            for (int y = a.y; y <= b.y; y++) { Put(px, n, a.x, y, c); Put(px, n, b.x, y, c); }
        }

        static string F(float v) => float.IsNegativeInfinity(v) ? "" : v.ToString("0.000", CultureInfo.InvariantCulture);

        static void WriteCsv(List<Row> rows, string file = "frame_scan.csv")
        {
            var sb = new StringBuilder();
            sb.AppendLine("prefab,form,formName,kind,ctx,clip,dur,span,need,capped,worst,worstArt,ovL,ovR,ovB,ovT,artL,artR,artB,artT,tL,tR,tB,tT,samples,cutSamples,dropped,nan,hint");
            foreach (var r in rows)
                sb.AppendLine(string.Join(",", r.prefab, r.form, r.formName, r.kind, r.ctx, r.clip, F(r.dur), F(r.span), F(r.need), r.capped ? 1 : 0,
                    F(r.Worst), F(r.WorstArt), F(r.ovL), F(r.ovR), F(r.ovB), F(r.ovT), F(r.artL), F(r.artR), F(r.artB), F(r.artT),
                    F(r.tL), F(r.tR), F(r.tB), F(r.tT), r.samples, r.cutSamples, r.dropped, r.nan, "\"" + r.hint + "\""));
            File.WriteAllText(Path.Combine(OutDir, file), sb.ToString());
        }

        static string Side(Row r)
        {
            float w = r.Worst;
            return w == r.ovL ? $"trái t={r.tL:0.00}" : w == r.ovR ? $"phải t={r.tR:0.00}" : w == r.ovB ? $"đáy t={r.tB:0.00}" : $"đỉnh t={r.tT:0.00}";
        }

        static string Summary(List<Row> rows, List<FormInfo> infos, int forms, double secs, string title = "Quét khung hình tướng")
        {
            var sb = new StringBuilder();
            var cut = rows.Where(r => r.Worst > 0).OrderByDescending(r => r.Worst).ToList();
            var drop = infos.Where(i => i.dropped > 0).ToList();
            var nan = rows.Where(r => r.nan > 0).ToList();
            var fail = rows.Where(r => r.hint == "không nạp được").ToList();
            sb.AppendLine($"# {title} — {forms} dạng, {rows.Count} clip, {rows.Sum(r => r.samples)} mẫu, {secs:0}s");
            sb.AppendLine($"- Cắt viền/hình: {cut.Count} clip ở {cut.Select(r => r.prefab + r.form).Distinct().Count()} dạng (hình bị cắt thật: {cut.Count(r => r.WorstArt > 0)} clip)");
            sb.AppendLine($"- Mất tam giác (mặt nạ cắt hết chỗ): {drop.Count} dạng");
            sb.AppendLine($"- Đỉnh NaN: {nan.Count} clip; không nạp được: {fail.Count} dạng");
            sb.AppendLine();
            sb.AppendLine("## Cắt viền / hình (đơn vị: chiều cao dáng đứng; viền giấy dày 0,037)");
            foreach (var r in cut)
                sb.AppendLine($"- {r.prefab} dạng {r.form} ({r.formName}, {r.kind}) {r.clip} [{r.ctx}]: lọt {r.Worst:0.000} phía {Side(r)}" +
                              $"{(r.WorstArt > 0 ? $", hình cắt {r.WorstArt:0.000}" : ", chỉ viền")}; khung {r.span:0.00} (cần {r.need:0.00}); " +
                              $"{r.cutSamples}/{r.samples} mẫu — {r.hint}");
            sb.AppendLine();
            sb.AppendLine("## Mất tam giác (AtomikPose.Dropped)");
            foreach (var i in drop)
                sb.AppendLine($"- {i.prefab} dạng {i.form} ({i.formName}): {i.dropped} tam giác bỏ; chừa {i.curExtra} đỉnh, cần chắc {i.safeExtra}, đỉnh lớn nhất {i.peakVerts}/{i.maxVerts}");
            sb.AppendLine();
            sb.AppendLine("## Rig có mặt nạ cắt (chỗ chừa)");
            foreach (var i in infos.Where(x => x.safeExtra > 0))
                sb.AppendLine($"- {i.prefab} dạng {i.form} ({i.formName}): chừa {i.curExtra}, cần chắc {i.safeExtra}, đỉnh lớn nhất {i.peakVerts}/{i.maxVerts}, bỏ {i.dropped}");
            if (nan.Count > 0)
            {
                sb.AppendLine();
                sb.AppendLine("## Đỉnh NaN");
                foreach (var r in nan) sb.AppendLine($"- {r.prefab} dạng {r.form} {r.clip} [{r.ctx}]: {r.nan}");
            }
            if (fail.Count > 0)
            {
                sb.AppendLine();
                sb.AppendLine("## Không nạp được");
                foreach (var r in fail) sb.AppendLine($"- {r.prefab} dạng {r.form} ({r.formName})");
            }
            return sb.ToString();
        }
    }
}
