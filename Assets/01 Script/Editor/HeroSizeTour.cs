// Menu thử (đang Play): đo cỡ thật của tướng trên sân. Mỗi đảo lấy 10 tướng theo thứ tự ải ra mắt (ải tag Hero), mỗi dạng nạp prefab
// aola ở chiều cao = size của dạng x 1,18 nếu ải ra mắt là boss (như StageView: Height x size x boss), đo khung bao các lưới ở khung đầu
// dáng đứng (bỏ lớp hạt không viền đặt cao FxLift), xếp thành hàng (mỗi dạng một hàng, mỗi tướng một cột) rồi render một camera ra
// Temp/PokiShots/co_tuong/<đảo>.png; số đo ghi vào Temp/PokiShots/co_tuong/co_tuong.csv (đơn vị = chiều cao chuẩn 1, nhân 150 ra
// điểm sân phía địch). Sau 10 tướng là lính của đảo (theo ải gặp đầu, không nhân boss).
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HeroSizeTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "co_tuong");
        const float Gap = 0.25f, RowGap = 0.35f, Ppu = 180f;

        [MenuItem("PokiClash/Thử/Khác/Tướng∕Cỡ tướng: đo và chụp hàng tướng từng đảo (đang Play)", priority = 140)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.Data == null) return;
            Directory.CreateDirectory(Dir);
            var csv = new StringBuilder("zone,stage,kind,boss,hero,name,form,formName,size,mul,normW,normH,normBot,stageW,stageH,col,row,cx,top\n");
            var root = new GameObject("co_tuong_root");
            root.transform.position = new Vector3(-20000, -20000, 0);
            try
            {
                foreach (Elem z in new[] { Elem.Thuy, Elem.Hoa, Elem.Kim, Elem.Moc, Elem.Tho })
                    Zone(z, root.transform, csv);
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
            File.WriteAllText(Path.Combine(Dir, "co_tuong.csv"), csv.ToString(), new UTF8Encoding(true));
            Debug.Log("[Thử] Xong cỡ tướng: " + Dir);
        }

        struct Item
        {
            public AolaActor a;
            public Bounds b;
            public int col, row;
        }

        static void Zone(Elem z, Transform root, StringBuilder csv)
        {
            var d = App.Data;
            var zs = d.ZoneStages(z).OrderBy(s => s.idx).ToList();
            // cột: 10 tướng theo ải ra mắt, rồi lính của đảo theo ải gặp đầu (kind "minion", không nhân boss)
            var cols = zs.Where(s => s.tag == StageTag.Hero && s.enemies.Count > 0).Select(s => (st: s, e: s.enemies[0], minion: false)).ToList();
            var seen = new HashSet<string>();
            foreach (var s in zs)
                foreach (var e in s.enemies)
                    if (d.Minions.Any(m => m.id == e.hero) && seen.Add(e.hero)) cols.Add((s, new StageEnemy { hero = e.hero, level = e.level }, true));
            var items = new List<Item>();
            var colW = new List<float>();
            int rows = 1;
            for (int c = 0; c < cols.Count; c++)
            {
                var st = cols[c].st;
                var e = cols[c].e;
                var h = cols[c].minion ? d.Minions.FirstOrDefault(m => m.id == e.hero) : d.Hero(e.hero);
                float w = 0.6f;
                if (h == null) { colW.Add(w); continue; }
                float mul = e.boss ? 1.18f : 1f;
                rows = Mathf.Max(rows, h.forms.Length);
                for (int f = 0; f < h.forms.Length; f++)
                {
                    var form = h.forms[f];
                    float H = (float)form.size * mul;
                    if (!AolaActor.Find(form.aola, out var prefab, out int fi)) continue;
                    var a = Object.Instantiate(prefab, root);
                    a.transform.localPosition = new Vector3(0, -10 * (f + 1) - 100 * c, 0);
                    a.Manual = true;
                    a.SplitFx = true;
                    if (!a.LoadForm(fi, H, false, 0)) { Object.DestroyImmediate(a.gameObject); continue; }
                    a.ShowFrame(AolaActor.Idle, 0);
                    var o = a.transform.position;
                    var b = new Bounds();
                    bool any = false;
                    foreach (var r in a.GetComponentsInChildren<Renderer>())
                    {
                        if (!r.enabled || r.bounds.size.sqrMagnitude <= 1e-8f || Mathf.Abs(r.bounds.center.y - o.y) > 50) continue;
                        if (!any) b = r.bounds; else b.Encapsulate(r.bounds);
                        any = true;
                    }
                    if (!any) { Object.DestroyImmediate(a.gameObject); continue; }
                    b.center -= o; // so với chân
                    w = Mathf.Max(w, b.size.x);
                    items.Add(new Item { a = a, b = b, col = c, row = f });
                    csv.Append($"{z},{st.idx},{(cols[c].minion ? "minion" : st.kind.ToString())},{e.boss},{h.id},{h.name},{f},{form.name},{form.size:0.00},{mul:0.00}," +
                               $"{b.size.x / H:0.000},{b.max.y / H:0.000},{b.min.y / H:0.000},{b.size.x * 150:0},{b.max.y * 150:0},{c},{f},");
                    csv.Append("CX" + items.Count + ",TOP" + items.Count + "\n");
                }
                colW.Add(w);
            }
            // xếp: cột theo bề rộng lớn nhất của tướng, hàng theo dạng; hàng cao 1,6 (dạng to nhất ~1,4)
            float rowH = 1.75f;
            var colX = new float[colW.Count];
            float x = 0;
            for (int c = 0; c < colW.Count; c++) { colX[c] = x + colW[c] / 2; x += colW[c] + Gap; }
            float totalW = Mathf.Max(1, x - Gap) + 2 * Gap, totalH = rows * rowH + (rows - 1) * RowGap + 2 * Gap;
            var csvText = csv.ToString();
            for (int i = 0; i < items.Count; i++)
            {
                var it = items[i];
                float footY = -(Gap + it.row * (rowH + RowGap) + rowH * 0.92f); // chân gần đáy hàng
                float cx = Gap + colX[it.col];
                // đặt sao cho tâm khung bao nằm giữa cột
                it.a.transform.localPosition = new Vector3(cx - it.b.center.x, footY, 0);
                it.a.ShowFrame(AolaActor.Idle, 0);
                csvText = csvText.Replace("CX" + (i + 1) + ",", $"{cx / totalW:0.0000},").Replace("TOP" + (i + 1) + "\n", $"{(-footY - it.b.max.y) / totalH:0.0000}\n");
            }
            csv.Clear().Append(csvText);
            // camera: góc trên trái của vùng xếp là root
            var camGo = new GameObject("cam_co");
            camGo.transform.SetParent(root, false);
            camGo.transform.localPosition = new Vector3(totalW / 2, -totalH / 2, -20);
            var cam = camGo.AddComponent<Camera>();
            cam.orthographic = true;
            cam.orthographicSize = totalH / 2;
            cam.aspect = totalW / totalH;
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0.93f, 0.91f, 0.86f, 1);
            cam.nearClipPlane = 0.1f;
            cam.farClipPlane = 60;
            int pw = Mathf.CeilToInt(totalW * Ppu), ph = Mathf.CeilToInt(totalH * Ppu);
            var rt = RenderTexture.GetTemporary(pw, ph, 24, RenderTextureFormat.ARGB32);
            cam.targetTexture = rt;
            cam.aspect = (float)pw / ph;
            cam.Render();
            var prev = RenderTexture.active;
            RenderTexture.active = rt;
            var tex = new Texture2D(pw, ph, TextureFormat.RGB24, false);
            tex.ReadPixels(new Rect(0, 0, pw, ph), 0, 0);
            tex.Apply();
            RenderTexture.active = prev;
            cam.targetTexture = null;
            RenderTexture.ReleaseTemporary(rt);
            File.WriteAllBytes(Path.Combine(Dir, z.ToString().ToLower() + ".png"), tex.EncodeToPNG());
            Object.DestroyImmediate(tex);
            Object.DestroyImmediate(camGo);
            foreach (var it in items) Object.DestroyImmediate(it.a.gameObject);
        }
    }
}
