// Thử cửa sổ xem .atomik của gói AtomSpine (Window > AtomSpine > Viewer, 2026-11-20): mở Viewer trên vài file .atomik của game,
// đặt clip / thời điểm / tab, rồi chụp đúng cửa sổ (GUIView.GrabPixels, không phụ thuộc cửa sổ có bị che hay không) vào
// Temp/PokiShots/viewer_*.png. Kèm ảnh Inspector của file .atomik (xem nút "Open in AtomSpine Viewer" ở đầu). Gọi gói qua
// reflection để asmdef của PokiClash không phải tham chiếu AtomSpine.Editor. Chạy ở Edit mode.
using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class AtomSpineViewerShot
    {
        const string Res = "Assets/03 Art/Heroes/Resources/";

        // (file, clip, giây, tab) — tab: 0 Info, 1 Bones, 2 Slots, 3 Atlas, 4 Events
        static readonly (string file, string clip, float t, int tab)[] Steps =
        {
            ("thach_giai_1", "walk", 0.38f, 0),
            ("thach_giai_1", "attack", 0.45f, 1),
            ("hai_long_2", "idle", 1.0f, 3),
            ("uyen_xa_1", "skill", 1.2f, 4),
        };

        static Queue<Action> queue;
        static int wait;

        [MenuItem("PokiClash/Thử/AtomSpine Viewer: mở và chụp", priority = 112)]
        static void Run()
        {
            var type = FindType("AtomSpine.Editor.AtomikViewerWindow");
            if (type == null)
            {
                Debug.LogError("[Viewer] Không thấy AtomSpine.Editor.AtomikViewerWindow (gói AtomSpine chưa có Viewer?).");
                return;
            }
            Directory.CreateDirectory(PlayTour.ShotDir);
            queue = new Queue<Action>();
            EditorWindow win = null;
            foreach (var s in Steps)
            {
                var step = s;
                queue.Enqueue(() =>
                {
                    var asset = AssetDatabase.LoadMainAssetAtPath($"{Res}{step.file}/{step.file}.atomik");
                    if (!asset)
                    {
                        Debug.LogError($"[Viewer] Không nạp được {step.file}.atomik");
                        return;
                    }
                    Selection.activeObject = asset;
                    win = (EditorWindow)type.GetMethod("Open", BindingFlags.Public | BindingFlags.Static).Invoke(null, new object[] { asset });
                    win.position = new Rect(80, 80, 1280, 760);
                    type.GetField("tab", BindingFlags.Instance | BindingFlags.NonPublic)?.SetValue(win, step.tab);
                    wait = 20;
                });
                queue.Enqueue(() =>
                {
                    // model có sau lần vẽ đầu: chọn clip, dừng, tua tới giây cần
                    var model = type.GetProperty("Model")?.GetValue(win);
                    var a = type.GetProperty("Asset")?.GetValue(win);
                    if (model == null || a == null)
                    {
                        Debug.LogWarning($"[Viewer] {step.file}: chưa có model / asset");
                        return;
                    }
                    var mt = model.GetType();
                    mt.GetMethod("SelectClip", new[] { a.GetType(), typeof(string), typeof(bool) })?.Invoke(model, new object[] { a, step.clip, false });
                    mt.GetMethod("Scrub")?.Invoke(model, new object[] { a, step.t });
                    mt.GetField("playing")?.SetValue(model, false);
                    win.Repaint();
                    wait = 20;
                });
                queue.Enqueue(() =>
                {
                    Grab(win, $"viewer_{step.file}_{step.clip}_tab{step.tab}");
                    wait = 2;
                });
            }
            queue.Enqueue(() =>
            {
                // Inspector của file .atomik cuối (đầu Inspector phải có nút mở Viewer)
                var insp = FindType("UnityEditor.InspectorWindow");
                var all = insp != null ? Resources.FindObjectsOfTypeAll(insp) : new Object[0];
                if (all.Length > 0) Grab((EditorWindow)all[0], "viewer_inspector");
                Debug.Log("[Viewer] Xong: " + PlayTour.ShotDir);
            });
            wait = 0;
            EditorApplication.update -= Tick;
            EditorApplication.update += Tick;
        }

        // Nhấp đúp: đóng mọi Viewer đang mở, gọi AssetDatabase.OpenAsset như khi nhấp đúp trong Project, chụp Viewer (phải là tab
        // cạnh Scene) và cửa sổ Project đang mở thư mục tướng (mỗi dòng .atomik có nút ▶).
        [MenuItem("PokiClash/Thử/AtomSpine Viewer: thử nhấp đúp + nút trên dòng", priority = 113)]
        static void RunOpen()
        {
            var type = FindType("AtomSpine.Editor.AtomikViewerWindow");
            if (type == null)
            {
                Debug.LogError("[Viewer] Không thấy AtomSpine.Editor.AtomikViewerWindow.");
                return;
            }
            foreach (var w in Resources.FindObjectsOfTypeAll(type)) ((EditorWindow)w).Close();
            Directory.CreateDirectory(PlayTour.ShotDir);
            queue = new Queue<Action>();
            queue.Enqueue(() =>
            {
                var asset = AssetDatabase.LoadMainAssetAtPath(Res + "ca_den_1/ca_den_1.atomik");
                bool handled = AssetDatabase.OpenAsset(asset);
                var open = Resources.FindObjectsOfTypeAll(type);
                bool docked = open.Length > 0 && (bool)(typeof(EditorWindow).GetProperty("docked", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)?.GetValue(open[0]) ?? false);
                Debug.Log($"[Viewer] nhấp đúp ca_den_1: handled={handled}, cửa sổ Viewer={open.Length}, docked={docked}");
                // ping đúng file: Project mở thư mục chứa nó, thấy nút ▶ trên ô .atomik
                Selection.activeObject = asset;
                EditorGUIUtility.PingObject(asset);
                wait = 30;
            });
            queue.Enqueue(() =>
            {
                var open = Resources.FindObjectsOfTypeAll(type);
                if (open.Length > 0) Grab((EditorWindow)open[0], "viewer_nhapdup");
                wait = 40; // chụp lần hai sau ~0,5 s: clip phải đang chạy (thời gian trên thanh khác lần đầu)
            });
            queue.Enqueue(() =>
            {
                var open = Resources.FindObjectsOfTypeAll(type);
                if (open.Length > 0) Grab((EditorWindow)open[0], "viewer_nhapdup_2");
                var pb = FindType("UnityEditor.ProjectBrowser");
                var all = pb != null ? Resources.FindObjectsOfTypeAll(pb) : new Object[0];
                if (all.Length > 0) Grab((EditorWindow)all[0], "viewer_project");
                Debug.Log("[Viewer] Xong nhấp đúp: " + PlayTour.ShotDir);
            });
            wait = 0;
            EditorApplication.update -= Tick;
            EditorApplication.update += Tick;
        }

        static void Tick()
        {
            if (wait-- > 0)
            {
                InternalEditorUtility_RepaintAll();
                return;
            }
            if (queue == null || queue.Count == 0)
            {
                EditorApplication.update -= Tick;
                return;
            }
            try
            {
                queue.Dequeue()();
            }
            catch (Exception e)
            {
                Debug.LogException(e);
                queue.Clear();
            }
        }

        static void InternalEditorUtility_RepaintAll() => UnityEditorInternal.InternalEditorUtility.RepaintAllViews();

        // chụp cả khung chứa cửa sổ: GUIView.GrabPixels (nội bộ) vẽ view vào RenderTexture
        static void Grab(EditorWindow w, string name)
        {
            if (!w) return;
            var parent = typeof(EditorWindow).GetField("m_Parent", BindingFlags.Instance | BindingFlags.NonPublic)?.GetValue(w);
            var grab = parent?.GetType().GetMethod("GrabPixels", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public);
            if (grab == null)
            {
                Debug.LogWarning("[Viewer] Unity này không có GUIView.GrabPixels");
                return;
            }
            float ppp = EditorGUIUtility.pixelsPerPoint;
            var pos = (Rect)parent.GetType().GetProperty("position", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic).GetValue(parent);
            int pw = Mathf.RoundToInt(pos.width * ppp), ph = Mathf.RoundToInt(pos.height * ppp);
            var rt = new RenderTexture(pw, ph, 0, RenderTextureFormat.ARGB32);
            grab.Invoke(parent, new object[] { rt, new Rect(0, 0, pw, ph) });
            var prev = RenderTexture.active;
            RenderTexture.active = rt;
            var tex = new Texture2D(pw, ph, TextureFormat.RGB24, false);
            tex.ReadPixels(new Rect(0, 0, pw, ph), 0, 0);
            RenderTexture.active = prev;
            // GrabPixels để hàng trên cùng ở đáy ảnh: lật dọc
            var px = tex.GetPixels32();
            var flip = new Color32[px.Length];
            for (int y = 0; y < ph; y++) Array.Copy(px, y * pw, flip, (ph - 1 - y) * pw, pw);
            tex.SetPixels32(flip);
            tex.Apply();
            File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, name + ".png"), tex.EncodeToPNG());
            Object.DestroyImmediate(tex);
            Object.DestroyImmediate(rt);
            Debug.Log($"[Viewer] chụp {name} ({pw}x{ph})");
        }

        static Type FindType(string fullName)
        {
            foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
            {
                var t = asm.GetType(fullName);
                if (t != null) return t;
            }
            return null;
        }
    }
}
