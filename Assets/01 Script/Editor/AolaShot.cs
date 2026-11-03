// Chụp thử prefab tướng (AolaActor nạp từ asset đã nhập) ra ảnh để soi: mỗi tướng một ảnh, mỗi dạng một hàng gồm chân dung,
// khung đầu dáng đứng, khung lao xa nhất của đòn đánh, khung trúng đòn của chiêu; ô vẽ như AolaSticker (khung 3,4 lần chiều cao
// dáng đứng, chân ở 20%). Ảnh ghi vào Library/PokiHeroShots (Temp bị xoá khi đóng Unity).
// Batchmode: Unity -batchmode -projectPath <dự án> -executeMethod PokiClash.EditorTools.AolaShot.Batch [-heroes id,id] [-out thư mục]
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class AolaShot
    {
        const float Span = 3.4f, FootV = 0.2f;
        const int Cell = 384;

        static string DefaultOut => Path.GetFullPath(Path.Combine(Application.dataPath, "../Library/PokiHeroShots"));

        [MenuItem("PokiClash/Tướng/Chụp thử prefab tướng", priority = 52)]
        static void Menu()
        {
            var n = Shot(null, DefaultOut);
            Debug.Log($"[Tướng aola] Chụp {n} tướng vào {DefaultOut}");
            EditorUtility.RevealInFinder(DefaultOut);
        }

        public static void Batch()
        {
            string[] ids = null;
            var outDir = DefaultOut;
            var args = Environment.GetCommandLineArgs();
            for (int i = 0; i < args.Length - 1; i++)
            {
                if (args[i] == "-heroes") ids = args[i + 1].Split(',');
                if (args[i] == "-out") outDir = args[i + 1];
            }
            int code = 0;
            try
            {
                var n = Shot(ids, outDir);
                Debug.Log($"[Tướng aola] Chụp {n} tướng vào {outDir}");
            }
            catch (Exception e)
            {
                Debug.LogException(e);
                code = 1;
            }
            EditorApplication.Exit(code);
        }

        public static int Shot(string[] ids, string outDir)
        {
            var lib = AssetDatabase.LoadAssetAtPath<HeroModels>(AolaImport.LibraryPath);
            if (!lib) throw new Exception("Chưa có " + AolaImport.LibraryPath + " (menu PokiClash/Tướng/Nhập hình tướng aola)");
            Directory.CreateDirectory(outDir);
            var rt = new RenderTexture(Cell, Cell, 16, RenderTextureFormat.ARGB32);
            var camGo = new GameObject("cam_chup") { hideFlags = HideFlags.HideAndDontSave };
            var cam = camGo.AddComponent<Camera>();
            cam.orthographic = true;
            cam.orthographicSize = Span / 2;
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0.93f, 0.89f, 0.80f, 1); // nền giấy để thấy mép trong suốt
            cam.targetTexture = rt;
            cam.nearClipPlane = 0.1f;
            cam.farClipPlane = 50;
            cam.enabled = false;
            int count = 0;
            try
            {
                foreach (var prefab in lib.heroes)
                {
                    if (!prefab || ids != null && !ids.Contains(prefab.name)) continue;
                    var forms = prefab.Forms;
                    var sheet = new Texture2D(Cell * 4, Cell * Math.Max(1, forms.Length), TextureFormat.RGBA32, false);
                    sheet.SetPixels32(Enumerable.Repeat(new Color32(255, 255, 255, 255), sheet.width * sheet.height).ToArray());
                    for (int f = 0; f < forms.Length; f++)
                    {
                        int row = forms.Length - 1 - f; // dạng 1 ở trên
                        var portrait = forms[f] ? forms[f].LoadPortrait() : null;
                        if (portrait) Blit(portrait.texture, sheet, 0, row);
                        var actor = (AolaActor)PrefabUtility.InstantiatePrefab(prefab);
                        actor.gameObject.hideFlags = HideFlags.HideAndDontSave;
                        actor.transform.position = new Vector3(5000, 0, 0);
                        camGo.transform.position = new Vector3(5000, Span * (0.5f - FootV), -10);
                        actor.Manual = true;
                        if (actor.LoadForm(f, 1f, false, 0))
                        {
                            var shots = new[]
                            {
                                (AolaActor.Idle, 0),
                                (AolaActor.Attack, actor.PeakFrame(AolaActor.Attack)),
                                (AolaActor.Skill, actor.HitFrame(AolaActor.Skill)),
                            };
                            for (int s = 0; s < shots.Length; s++)
                            {
                                actor.ShowFrame(shots[s].Item1, shots[s].Item2);
                                cam.Render();
                                RenderTexture.active = rt;
                                var t = new Texture2D(Cell, Cell, TextureFormat.RGBA32, false);
                                t.ReadPixels(new Rect(0, 0, Cell, Cell), 0, 0);
                                t.Apply();
                                RenderTexture.active = null;
                                sheet.SetPixels32((s + 1) * Cell, row * Cell, Cell, Cell, t.GetPixels32());
                                Object.DestroyImmediate(t);
                            }
                        }
                        else Debug.LogWarning($"[Tướng aola] {prefab.name} dạng {f + 1}: không nạp được");
                        Object.DestroyImmediate(actor.gameObject);
                    }
                    sheet.Apply();
                    File.WriteAllBytes(Path.Combine(outDir, prefab.name + ".png"), sheet.EncodeToPNG());
                    Object.DestroyImmediate(sheet);
                    count++;
                }
            }
            finally
            {
                Object.DestroyImmediate(camGo);
                rt.Release();
                Object.DestroyImmediate(rt);
            }
            return count;
        }

        // chân dung (nén, không đọc được điểm ảnh) vẽ qua RenderTexture vào ô (col, row), giữ tỉ lệ
        static void Blit(Texture src, Texture2D sheet, int col, int row)
        {
            var tmp = RenderTexture.GetTemporary(Cell, Cell, 0, RenderTextureFormat.ARGB32);
            RenderTexture.active = tmp;
            GL.Clear(true, true, new Color(1, 1, 1, 1));
            float k = (float)src.width / src.height; // < 1: dọc
            Graphics.Blit(src, tmp, new Vector2(1 / k, 1), new Vector2(-(1 - k) / 2 / k, 0));
            var t = new Texture2D(Cell, Cell, TextureFormat.RGBA32, false);
            t.ReadPixels(new Rect(0, 0, Cell, Cell), 0, 0);
            t.Apply();
            RenderTexture.active = null;
            RenderTexture.ReleaseTemporary(tmp);
            // Blit chép cả màu của điểm trong suốt (Unity loang màu ra vùng trong suốt khi nhập): trộn lên nền trắng
            var px = t.GetPixels32();
            for (int i = 0; i < px.Length; i++)
            {
                var c = px[i];
                int a = c.a;
                px[i] = new Color32((byte)((c.r * a + 255 * (255 - a)) / 255), (byte)((c.g * a + 255 * (255 - a)) / 255),
                    (byte)((c.b * a + 255 * (255 - a)) / 255), 255);
            }
            sheet.SetPixels32(col * Cell, row * Cell, Cell, Cell, px);
            Object.DestroyImmediate(t);
        }
    }
}
