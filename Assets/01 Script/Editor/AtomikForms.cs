// Gắn dạng tướng vẽ mới rig xương riêng (.atomik, xuất từ ArtGen/Spine, 2026-11-08) vào prefab tướng, không đụng các dạng aola:
// - dạng trong heroes.json (khoá aola) có file Assets/03 Art/Heroes/Resources/<dạng>/<dạng>.atomik thì dựng hoặc cập nhật
//   AolaAnim <dạng>.asset cùng thư mục: atomik = rig trong file, res = "<dạng>/<dạng>" cho chân dung <dạng>_portrait.png;
// - prefab Assets/04 Prefabs/Heroes/<id>.prefab của tướng có dạng đó: danh sách dạng dựng lại theo heroes.json (dạng aola
//   giữ asset đang có), rồi làm mới danh mục HeroModels.
// Không gọi menu nhập aola (menu đó nhập lại dạng aola từ AolaRipper máy này, đè bản viết lại của máy kia). Menu nhập aola bỏ
// qua dạng có atomik (AolaImport.ImportAll).
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class AtomikForms
    {
        const string HeroesJson = "Assets/02 Data/Json/heroes.json";

        [MenuItem("PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng", priority = 57)]
        public static string Attach()
        {
            var heroes = (List<object>)((Dictionary<string, object>)MiniJson.Parse(File.ReadAllText(HeroesJson)))["heroes"];
            var log = new List<string>();
            var lib = AssetDatabase.LoadAssetAtPath<HeroModels>(AolaImport.LibraryPath);
            foreach (Dictionary<string, object> h in heroes)
            {
                var forms = new List<string>();
                if (h.TryGetValue("forms", out var fs) && fs is List<object> fl)
                    foreach (Dictionary<string, object> f in fl)
                        if (f.TryGetValue("aola", out var a) && a is string s && s.Length > 0) forms.Add(s);
                if (forms.Count == 0 && h.TryGetValue("aola", out var a0) && a0 is string s0 && s0.Length > 0) forms.Add(s0);
                bool any = false;
                foreach (var form in forms)
                    if (AttachForm(form, log)) any = true;
                if (!any) continue;
                string id = (string)h["id"];
                var anims = new AolaAnim[forms.Count];
                for (int i = 0; i < forms.Count; i++)
                    anims[i] = AssetDatabase.LoadAssetAtPath<AolaAnim>($"{AolaImport.ResDir}/{forms[i]}/{forms[i]}.asset");
                var path = $"{AolaImport.PrefabDir}/{id}.prefab";
                if (!File.Exists(path))
                {
                    log.Add($"{id}: chưa có prefab tướng ({path}), chạy menu nhập aola một lần trước");
                    continue;
                }
                var root = PrefabUtility.LoadPrefabContents(path);
                try
                {
                    var actor = root.GetComponent<AolaActor>();
                    if (!actor)
                    {
                        log.Add($"{id}: prefab không có AolaActor");
                        continue;
                    }
                    actor.Setup(anims);
                    PrefabUtility.SaveAsPrefabAsset(root, path);
                    log.Add($"{id}: prefab giữ {anims.Length} dạng ({string.Join(", ", forms)})");
                }
                finally
                {
                    PrefabUtility.UnloadPrefabContents(root);
                }
            }
            if (lib)
            {
                lib.Setup(lib.heroes); // bỏ bảng tra cũ
                EditorUtility.SetDirty(lib);
            }
            AssetDatabase.SaveAssets();
            var msg = "[Atomik] " + (log.Count == 0 ? "không có dạng .atomik nào trong heroes.json" : string.Join("\n", log));
            Debug.Log(msg);
            return msg;
        }

        // Chụp dạng .atomik qua AolaActor (đường game chạy thật): mỗi clip một hàng 8 khung, ô như AolaSticker (3,4 lần chiều cao,
        // chân ở 20%); ghi Library/PokiHeroShots/<id>_atomik.png và in khung trúng, đỉnh lao, chỗ bắn tia.
        [MenuItem("PokiClash/Tướng/Chụp thử dạng .atomik (mọi clip)", priority = 58)]
        public static string Shot()
        {
            const float Span = 3.4f, FootV = 0.2f;
            const int Cell = 256, N = 8;
            string[] clips = { AolaActor.Idle, AolaActor.Hit, AolaActor.Attack, AolaActor.Cast, AolaActor.Skill, AolaActor.Evolve };
            var lib = AssetDatabase.LoadAssetAtPath<HeroModels>(AolaImport.LibraryPath);
            var outDir = Path.GetFullPath(Path.Combine(Application.dataPath, "../Library/PokiHeroShots"));
            Directory.CreateDirectory(outDir);
            var rt = new RenderTexture(Cell, Cell, 16, RenderTextureFormat.ARGB32);
            var camGo = new GameObject("cam_chup_atomik") { hideFlags = HideFlags.HideAndDontSave };
            var cam = camGo.AddComponent<Camera>();
            cam.orthographic = true;
            cam.orthographicSize = Span / 2;
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0.93f, 0.89f, 0.80f, 1);
            cam.targetTexture = rt;
            cam.nearClipPlane = 0.1f;
            cam.farClipPlane = 50;
            cam.enabled = false;
            var log = new List<string>();
            try
            {
                foreach (var prefab in lib.heroes)
                {
                    if (!prefab) continue;
                    var forms = prefab.Forms;
                    for (int f = 0; f < forms.Length; f++)
                    {
                        if (!forms[f] || !forms[f].atomik) continue;
                        var actor = (AolaActor)PrefabUtility.InstantiatePrefab(prefab);
                        actor.gameObject.hideFlags = HideFlags.HideAndDontSave;
                        actor.transform.position = new Vector3(6000, 0, 0);
                        actor.Manual = true;
                        var sheet = new Texture2D(Cell * N, Cell * clips.Length, TextureFormat.RGBA32, false);
                        try
                        {
                            if (!actor.LoadForm(f, 1f, false, 0))
                            {
                                log.Add($"{prefab.name} dạng {f + 1}: không nạp được");
                                continue;
                            }
                            actor.Beam(out var muzzle, out float beam);
                            log.Add($"{prefab.name} dạng {f + 1} ({forms[f].name}): cao {actor.IdleHeightPx:0} px, tia ở ({muzzle.x:0},{muzzle.y:0}) cỡ {beam}");
                            for (int c = 0; c < clips.Length; c++)
                            {
                                int n = actor.FrameCount(clips[c]);
                                int row = clips.Length - 1 - c;
                                if (n > 0)
                                    log.Add($"  {clips[c]}: {n} khung ({actor.Duration(clips[c]):0.00} s), trúng {actor.HitFrame(clips[c])}, " +
                                            $"đỉnh lao {actor.PeakFrame(clips[c])}, dời đỉnh {actor.Disp(clips[c], actor.PeakFrame(clips[c]))}, lao {actor.Lunges(clips[c])}");
                                for (int i = 0; i < N; i++)
                                {
                                    // đòn lao: camera theo thân để thấy cú chém ở xa
                                    int fi = n <= 1 ? 0 : Mathf.RoundToInt(i * (n - 1) / (float)(N - 1));
                                    var d = n > 0 ? actor.Disp(clips[c], fi) * (1f / Mathf.Max(1, actor.IdleHeightPx)) : Vector2.zero;
                                    camGo.transform.position = new Vector3(6000 + d.x * 0.6f, Span * (0.5f - FootV), -10);
                                    actor.ShowFrame(clips[c], fi);
                                    cam.Render();
                                    RenderTexture.active = rt;
                                    var t = new Texture2D(Cell, Cell, TextureFormat.RGBA32, false);
                                    t.ReadPixels(new Rect(0, 0, Cell, Cell), 0, 0);
                                    t.Apply();
                                    RenderTexture.active = null;
                                    sheet.SetPixels32(i * Cell, row * Cell, Cell, Cell, t.GetPixels32());
                                    Object.DestroyImmediate(t);
                                }
                            }
                            sheet.Apply();
                            File.WriteAllBytes(Path.Combine(outDir, $"{prefab.name}_atomik_{f + 1}.png"), sheet.EncodeToPNG());
                        }
                        finally
                        {
                            Object.DestroyImmediate(sheet);
                            Object.DestroyImmediate(actor.gameObject);
                        }
                    }
                }
            }
            finally
            {
                Object.DestroyImmediate(camGo);
                rt.Release();
                Object.DestroyImmediate(rt);
            }
            var msg = $"[Atomik] chụp vào {outDir}\n" + string.Join("\n", log);
            Debug.Log(msg);
            return msg;
        }

        static bool AttachForm(string form, List<string> log)
        {
            string dir = $"{AolaImport.ResDir}/{form}";
            string file = $"{dir}/{form}.atomik";
            if (!File.Exists(file)) return false;
            AssetDatabase.ImportAsset(file, ImportAssetOptions.ForceSynchronousImport);
            var rig = AssetDatabase.LoadAssetAtPath<AtomikAsset>(file);
            if (!rig)
            {
                log.Add($"{form}: không đọc được {file}");
                return false;
            }
            string path = $"{dir}/{form}.asset";
            var a = AssetDatabase.LoadAssetAtPath<AolaAnim>(path);
            bool fresh = !a;
            if (fresh) a = ScriptableObject.CreateInstance<AolaAnim>();
            a.Setup($"{form}/{form}", null, new Vector2[0], new Rect[0], -1,
                "atomik:" + File.GetLastWriteTimeUtc(file).Ticks);
            a.atomik = rig;
            if (fresh) AssetDatabase.CreateAsset(a, path);
            else EditorUtility.SetDirty(a);
            bool portrait = File.Exists($"{dir}/{form}_portrait.png");
            log.Add($"{form}: rig {rig.bones.Length} xương, {rig.anims.Length} clip ({string.Join(", ", System.Array.ConvertAll(rig.anims, c => c.name))})" +
                    (portrait ? "" : $"; THIẾU chân dung {form}_portrait.png"));
            return true;
        }
    }
}
