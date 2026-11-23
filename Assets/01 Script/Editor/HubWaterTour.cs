// Tour chụp nước chảy và easter egg bản đồ sảnh (đang Play): "PokiClash/Thử/Đảo và sảnh/Sảnh: nước chảy, easter egg (chụp, đang Play)".
// Vào sảnh, chụp toàn cảnh; rồi phóng lớp kéo (keo) lên từng chỗ (thác Mộc trên, hẻm núi, thác Mộc dưới, thác Thủy, mặt biển) và chụp
// chuỗi khung liền (ghép GIF soi chuyển động: ArtGen/Islands/sanh_moi/nuoc_dong/ghep_gif.py). Ảnh vào Temp/PokiShots/nuoc/; xong trả
// lớp kéo về như cũ. Chạm bí mật có ghi bản lưu (bi, cờ hubEgg): tour sao lưu trước, xong trả lại.
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HubWaterTour
    {
        static string Dir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "nuoc");

        // chỗ soi: tên, toạ độ tỉ lệ trên ảnh bản đồ (u, v từ trên), độ phóng
        static readonly (string name, Vector2 uv, float zoom)[] Spots =
        {
            ("moc_tren", new Vector2(0.27f, 0.305f), 3.2f),
            ("hem_nui", new Vector2(0.47f, 0.42f), 3.2f),
            ("moc_duoi", new Vector2(0.19f, 0.575f), 3.2f),
            ("thuy", new Vector2(0.65f, 0.75f), 3.2f),
        };

        public static int Frames = 10, Super = 1; // superSize > 1 làm canvas đổi cỡ, ảnh hỏng (2026-11-23): phóng lớp kéo thay vào
        public static bool Water = true, Eggs = true;

        [MenuItem("PokiClash/Thử/Đảo và sảnh/Sảnh: nước chảy, easter egg (chụp, đang Play)", priority = 141)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator WaitRouter(string id)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != id) && Time.realtimeSinceStartup - t0 < 30) yield return null;
        }

        static IEnumerator Run()
        {
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, "*.jpg")) File.Delete(f);
            if (App.Router.Current != SceneIds.Hub)
            {
                App.Modals.CloseAll();
                App.Router.Go(SceneIds.Hub);
                yield return WaitRouter(SceneIds.Hub);
            }
            yield return new WaitForSecondsRealtime(1.5f);
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.4f);
            yield return Shot("0_toan_canh");
            var pan = Object.FindAnyObjectByType<HubPan>();
            var keo = pan ? FindRt(pan.transform.root, "keo") : null;
            var dao = keo ? FindRt(keo, "dao") : null;
            if (!pan || !keo || !dao)
            {
                Debug.LogError("[Thử] Không thấy HubPan / keo / dao");
                yield break;
            }
            pan.enabled = false;
            var pos0 = keo.anchoredPosition;
            var savePath = App.Save.FilePath;
            string backup = File.Exists(savePath) ? File.ReadAllText(savePath) : null;
            var anim = dao.GetComponentInChildren<IslandAnim>(true);
            try
            {
                if (Water)
                    foreach (var (name, uv, zoom) in Spots)
                    {
                        Look(keo, dao, uv, zoom);
                        yield return new WaitForSecondsRealtime(0.5f);
                        for (int k = 0; k < Frames; k++)
                        {
                            yield return Shot($"{name}_{k:00}");
                            yield return new WaitForSecondsRealtime(0.07f);
                        }
                    }
                if (Eggs && anim)
                {
                    // chạm từng bí mật (IslandAnim.TestTap), chụp chuỗi khung
                    foreach (var (name, hot, uv, zoom, n, gap) in new[]
                             {
                                 ("e_nui", "cham_nui_lua", new Vector2(375 / 1024f, 230 / 1796f), 2.6f, 8, 0.2f),
                                 ("e_den", "cham_hai_dang", new Vector2(302 / 1024f, 1290 / 1796f), 2.6f, 6, 0.35f),
                                 ("e_tau", "cham_xac_tau", new Vector2(405 / 1024f, 1435 / 1796f), 3.0f, 8, 0.4f),
                                 ("e_xoay", "cham_xoay_nuoc", new Vector2(745 / 1024f, 1245 / 1796f), 2.4f, 5, 0.25f),
                                 ("e_sanho", "cham_san_ho", new Vector2(150 / 1024f, 1380 / 1796f), 3.0f, 6, 0.12f),
                             })
                    {
                        Look(keo, dao, uv, zoom);
                        yield return new WaitForSecondsRealtime(0.4f);
                        if (name == "e_nui" || name == "e_den") RealTap(anim, hot); // chạm như ngón tay: điểm chạm phải nằm trên ảnh đảo
                        else Tap(anim, hot);
                        for (int k = 0; k < n; k++)
                        {
                            yield return new WaitForSecondsRealtime(gap);
                            yield return Shot($"{name}_{k:00}");
                        }
                        if (name == "e_xoay")
                        {
                            yield return new WaitForSecondsRealtime(0.5f);
                            Tap(anim, "cham_chai_thu");
                            yield return new WaitForSecondsRealtime(0.6f);
                            yield return Shot("e_xoay_thu");
                            App.Modals.CloseAll();
                        }
                    }
                    // rùa: chạm theo chỗ hiện tại
                    Look(keo, dao, new Vector2(860 / 1024f, 1225 / 1796f), 2.6f);
                    yield return new WaitForSecondsRealtime(0.4f);
                    yield return Shot("e_rua_00");
                    Tap(anim, "cham_rua");
                    for (int k = 1; k < 5; k++)
                    {
                        yield return new WaitForSecondsRealtime(0.25f);
                        yield return Shot($"e_rua_{k:00}");
                    }
                    // cá voi: gọi nổi ngay, chụp cả chu kỳ, chạm lúc đang nổi
                    Look(keo, dao, new Vector2(780 / 1024f, 1505 / 1796f), 2.8f);
                    yield return new WaitForSecondsRealtime(0.3f);
                    anim.TestEgg("voi");
                    for (int k = 0; k < 16; k++)
                    {
                        yield return new WaitForSecondsRealtime(0.35f);
                        if (k == 4) Tap(anim, "cham_ca_voi");
                        yield return Shot($"e_voi_{k:00}");
                    }
                    // cá vàng: gọi nhảy ngay, nhìn theo điểm chạm của nó, chạm giữa cú nhảy
                    anim.TestEgg("ca_vang");
                    yield return null;
                    yield return null;
                    var gold = FindRt(anim.transform, "cham_ca_vang");
                    if (gold)
                    {
                        Vector2 g = anim.transform.InverseTransformPoint(gold.position);
                        var ar = ((RectTransform)anim.transform).rect;
                        Look(keo, dao, new Vector2((g.x - ar.xMin) / ar.width, (ar.yMax - g.y) / ar.height), 2.0f);
                    }
                    for (int k = 0; k < 6; k++)
                    {
                        yield return new WaitForSecondsRealtime(0.18f);
                        if (k == 3) Tap(anim, "cham_ca_vang");
                        yield return Shot($"e_ca_vang_{k:00}");
                    }
                    Debug.Log("[Thử] Bí mật bản đồ đã tìm: " + System.Convert.ToString(App.Save.Data.extra.TryGetValue("hubEgg", out var bits) ? bits : 0));
                }
            }
            finally
            {
                keo.localScale = Vector3.one;
                keo.anchoredPosition = pos0;
                pan.enabled = true;
                if (backup != null)
                {
                    File.WriteAllText(savePath, backup);
                    App.Save.Load();
                }
            }
            Debug.Log("[Thử] Xong nước chảy sảnh: " + Path.GetFullPath(Dir));
        }

        // phóng lớp kéo lên điểm uv (tỉ lệ ảnh bản đồ) ở giữa màn
        static void Look(RectTransform keo, RectTransform dao, Vector2 uv, float zoom)
        {
            keo.localScale = new Vector3(zoom, zoom, 1);
            var r = dao.rect;
            var world = dao.TransformPoint(new Vector3(r.xMin + uv.x * r.width, r.yMax - uv.y * r.height, 0));
            var parent = (RectTransform)keo.parent;
            var want = parent.TransformPoint(parent.rect.center);
            keo.anchoredPosition += (Vector2)parent.InverseTransformVector(want - world);
        }

        // raycast của EventSystem tại tâm điểm chạm, gửi cú chạm vào vật trên cùng (như ngón tay); ghi log vật trúng
        static void RealTap(IslandAnim anim, string hot)
        {
            var rt = FindRt(anim.transform, hot);
            var es = UnityEngine.EventSystems.EventSystem.current;
            if (!rt || !es)
            {
                Debug.LogWarning("[Thử] Không chạm thật được " + hot);
                return;
            }
            var canvas = rt.GetComponentInParent<Canvas>().rootCanvas;
            var cam = canvas.renderMode == RenderMode.ScreenSpaceOverlay ? null : canvas.worldCamera;
            var ped = new UnityEngine.EventSystems.PointerEventData(es) { position = RectTransformUtility.WorldToScreenPoint(cam, rt.position) };
            var hits = new System.Collections.Generic.List<UnityEngine.EventSystems.RaycastResult>();
            es.RaycastAll(ped, hits);
            if (hits.Count == 0)
            {
                Debug.LogWarning("[Thử] Chạm thật " + hot + ": không trúng gì");
                return;
            }
            var top = hits[0].gameObject;
            ped.pointerCurrentRaycast = hits[0];
            ped.rawPointerPress = top;
            Debug.Log($"[Thử] Chạm thật {hot}: trúng {top.name} (dưới nó: {(hits.Count > 1 ? hits[1].gameObject.name : "-")})");
            UnityEngine.EventSystems.ExecuteEvents.ExecuteHierarchy(top, ped, UnityEngine.EventSystems.ExecuteEvents.pointerClickHandler);
        }

        static void Tap(IslandAnim anim, string hot)
        {
            if (!anim.TestTap(hot)) Debug.LogWarning("[Thử] Không thấy điểm chạm " + hot);
        }

        static RectTransform FindRt(Transform root, string n) =>
            root.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == n);

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture(Super); // vẽ lại ở cỡ lớn hơn màn Game: soi được nét
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(Dir, name + ".jpg"), tex.EncodeToJPG(88));
            Object.DestroyImmediate(tex);
        }
    }
}
