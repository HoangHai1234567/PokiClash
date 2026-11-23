// Thử màn Nhà (đang Play, 2026-11-22): vật vừa chọn nhún + sáng nhẹ (shader PokiClash/UIHomeSelect), bong bóng số bi trên đầu Cây bi,
// chạm một cây là hái hết, bi bay lên chip bi. Menu "PokiClash/Thử/Nhà và side meta/Nhà và side meta∕Nhà: chọn vật + hái Cây bi (đang Play)": sang Nhà, 12h, cho cây
// chín 6 giờ, kéo máy tới cây chụp bong bóng, chạm cây (qua OnTap như ngón thật) chụp các khung bi bay; chạm Nhà chính chụp trước /
// loé / nhún / thở; chạm một ô rừng. Ảnh vào Temp/PokiShots/nha_chon/. Xong thì trả bi, cây về như trước (không đổi bản lưu).
using System.Collections;
using System.IO;
using System.Linq;
using System.Reflection;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HomeSelectShots
    {
        static string Dir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "nha_chon");

        [MenuItem("PokiClash/Thử/Nhà và side meta/Nhà và side meta∕Nhà: chọn vật + hái Cây bi (đang Play)", priority = 144)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, name + ".png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }

        static void Tap(HomeScene home, Vector2 map) =>
            typeof(HomeScene).GetMethod("OnTap", BindingFlags.Instance | BindingFlags.NonPublic)?.Invoke(home, new object[] { map });

        // điểm bản đồ (px, y xuống) giữa chân thoi của vật: neo góc dưới chân thoi, lên nửa chân (cells ô cao 48 px)
        static Vector2 FootCenter(HomeObject o, int cells)
        {
            var a = o.Rt.anchoredPosition;
            return new Vector2(a.x, -a.y - cells * 24f);
        }

        static void Center(LandView view, RectTransform target)
        {
            if (!view || !target) return;
            var vr = (RectTransform)view.transform;
            var cam = vr.GetComponentInParent<Canvas>()?.rootCanvas.worldCamera;
            var c = RectTransformUtility.WorldToScreenPoint(cam, vr.TransformPoint(vr.rect.center));
            RectTransformUtility.ScreenPointToWorldPointInRectangle(vr, c, cam, out var w);
            var corners = new Vector3[4];
            target.GetWorldCorners(corners);
            view.ShiftWorld(w - (corners[0] + corners[2]) * 0.5f);
        }

        static IEnumerator Run()
        {
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, "*.png")) File.Delete(f);
            if (App.Router.Current != SceneIds.Home) App.Router.Go(SceneIds.Home);
            HomeScene home = null;
            for (float t = 0; t < 25 && !(home && App.Router.CurrentRoot == home); t += 0.25f)
            {
                yield return new WaitForSecondsRealtime(0.25f);
                home = Object.FindFirstObjectByType<HomeScene>();
            }
            for (float t = 0; t < 10 && PierShip.Active && PierShip.Active.Busy; t += 0.25f) yield return new WaitForSecondsRealtime(0.25f);
            yield return new WaitForSecondsRealtime(2.5f);
            if (!home)
            {
                Debug.LogWarning("[Thử] Không vào được màn Nhà");
                yield break;
            }
            DayCycle.Override = 12f;
            var s = App.Save.Data;
            var cfg = App.Data.Cfg;
            double now = SaveService.Now();
            Trees.Tick(s, cfg, now);
            // giữ để trả lại sau khi thử
            int balls0 = s.balls;
            var tree0 = Trees.Of(s, now).stock.ToList();
            double tick0 = Trees.Of(s, now).lastTick;
            var view = Object.FindAnyObjectByType<LandView>();
            var objs = Object.FindObjectsByType<HomeObject>(FindObjectsSortMode.None).Where(o => o.Id >= 0 && o.gameObject.activeInHierarchy).ToList();
            var trees = s.home.buildings.Where(b => Home.Def(cfg, b.def)?.kind == "tree").ToList();
            Debug.Log($"[Thử] Nhà: {trees.Count} Cây bi trong nhà, bi {balls0}, cây đang có {string.Join("/", tree0.Select(x => x.ToString("0.0")))}");
            var tb = trees.FirstOrDefault();
            var to = tb != null ? objs.FirstOrDefault(o => o.Id == tb.id) : null;
            if (to)
            {
                Trees.Travel(s, 6 * 3600000.0);
                Center(view, to.Rt);
                yield return new WaitForSecondsRealtime(1.4f); // Labels mỗi giây
                Debug.Log($"[Thử] Cây sau 6 giờ: {Trees.Stock(s, cfg, SaveService.Now())} bi");
                yield return Shot("1_cay_bong_bong");
                Tap(home, FootCenter(to, Home.Def(cfg, tb.def).size));
                float[] at = { 0.05f, 0.22f, 0.4f, 0.6f, 0.85f, 1.4f };
                float tt = 0;
                for (int i = 0; i < at.Length; i++)
                {
                    yield return new WaitForSecondsRealtime(at[i] - tt);
                    tt = at[i];
                    yield return Shot($"2_hai_{i}_{(int)(at[i] * 1000)}ms");
                }
                Debug.Log($"[Thử] Sau khi hái: bi {s.balls} (+{s.balls - balls0}), cây còn {Trees.Stock(s, cfg, SaveService.Now())}");
            }
            else Debug.LogWarning("[Thử] Nhà chưa có Cây bi: bỏ phần hái");
            // chọn Nhà chính: trước / loé / nhún / thở
            var mainB = Home.Main(s.home);
            var mo = mainB != null ? objs.FirstOrDefault(o => o.Id == mainB.id) : null;
            if (mo)
            {
                Center(view, mo.Rt);
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Shot("3_nha_truoc");
                Tap(home, FootCenter(mo, Home.Def(cfg, mainB.def).size));
                float[] at = { 0.06f, 0.12f, 0.3f, 1.2f };
                float tt = 0;
                for (int i = 0; i < at.Length; i++)
                {
                    yield return new WaitForSecondsRealtime(at[i] - tt);
                    tt = at[i];
                    Debug.Log($"[Thử] chọn nhà {at[i]:0.00}s: _HomeSel {Shader.GetGlobalFloat("_HomeSel"):0.00}, scale {mo.transform.localScale.x:0.000}/{mo.transform.localScale.y:0.000}");
                    yield return Shot($"4_nha_chon_{i}_{(int)(at[i] * 1000)}ms");
                }
                Tap(home, new Vector2(-5000, -5000)); // chạm ra ngoài: đóng bảng
                yield return new WaitForSecondsRealtime(0.3f);
                Debug.Log($"[Thử] bỏ chọn: _HomeSel {Shader.GetGlobalFloat("_HomeSel"):0.00}, vật liệu {mo.Img.material?.name}");
            }
            // ô rừng gần Nhà chính (mốc nhãn vô hình, Id = -2 - ô)
            var lots = Object.FindObjectsByType<HomeObject>(FindObjectsSortMode.None).Where(o => o.Id <= -2).ToList();
            if (mo && lots.Count > 0)
            {
                var near = lots.OrderBy(o => (o.Rt.anchoredPosition - mo.Rt.anchoredPosition).sqrMagnitude).First();
                Center(view, near.Rt);
                yield return new WaitForSecondsRealtime(0.6f);
                Tap(home, FootCenter(near, 0));
                yield return new WaitForSecondsRealtime(0.15f);
                yield return Shot("5_rung_chon_150ms");
                yield return new WaitForSecondsRealtime(0.85f);
                yield return Shot("5_rung_chon_1000ms");
                Tap(home, new Vector2(-5000, -5000));
            }
            // trả bản lưu như trước
            yield return new WaitForSecondsRealtime(0.5f);
            var ts = Trees.Of(s, SaveService.Now());
            ts.stock = tree0;
            ts.lastTick = tick0;
            s.balls = balls0;
            App.Save.Save();
            App.Bars.Refresh();
            DayCycle.Override = null;
            Debug.Log("[Thử] Xong chọn vật + hái Cây bi (đã trả bi, cây như trước): " + Path.GetFullPath(Dir));
        }
    }
}
