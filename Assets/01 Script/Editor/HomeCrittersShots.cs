// Thử giao diện kiểu Clash of Critters của màn Nhà (đang Play, 2026-11-22). Menu "PokiClash/Thử/Nhà: vòng nút + chế độ xây kiểu Critters
// (đang Play)": sang Nhà, 12h; chụp màn thường (hàng nút icon, bong bóng có vòng tiến độ), chọn một công trình sản xuất (vòng nút + nhãn
// tên), bấm Xây chụp tấm xây và tab Sản xuất, chọn thẻ đầu xây được chụp bóng ma có ✓ ✗ (không thẻ nào xây được thì dời Nhà chính), rồi
// Thôi, Xong. Ảnh vào Temp/PokiShots/nha_critters/. Không đổi bản lưu (không bấm Đặt).
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using PokiClash.Core;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HomeCrittersShots
    {
        static string Dir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "nha_critters");
        const BindingFlags Inst = BindingFlags.Instance | BindingFlags.NonPublic;

        [MenuItem("PokiClash/Thử/Nhà và side meta/Nhà: vòng nút + chế độ xây kiểu Critters (đang Play)", priority = 145)]
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

        static T Field<T>(object o, string n) where T : class => typeof(HomeScene).GetField(n, Inst)?.GetValue(o) as T;
        static void Call(object o, string n, params object[] a) => typeof(HomeScene).GetMethod(n, Inst)?.Invoke(o, a);

        // kéo máy cho target ra giữa khung nhìn
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
            if (!home)
            {
                Debug.LogWarning("[Thử] Không vào được màn Nhà");
                yield break;
            }
            // giao diện cố định ẩn trong chuyến tàu, hiện lại sau khi cập bến: chờ hiện hẳn
            var chrome = Field<CanvasGroup>(home, "chrome");
            for (float t = 0; t < 8 && chrome && chrome.alpha < 0.99f; t += 0.25f) yield return new WaitForSecondsRealtime(0.25f);
            yield return new WaitForSecondsRealtime(0.8f);
            DayCycle.Override = 12f;
            var s = App.Save.Data;
            var cfg = App.Data.Cfg;
            var view = Object.FindAnyObjectByType<LandView>();
            var objs = Field<Dictionary<int, HomeObject>>(home, "objs");
            yield return Shot("1_thuong");

            // chọn công trình sản xuất (ưu tiên cái có đồ chờ thu: thấy bong bóng có vòng)
            var prod = s.home.buildings.Where(b => Home.Def(cfg, b.def)?.kind == "prod" && objs != null && objs.ContainsKey(b.id))
                .OrderByDescending(Home.Stock).FirstOrDefault();
            if (prod != null)
            {
                var o = objs[prod.id];
                Center(view, o.Rt);
                yield return new WaitForSecondsRealtime(1.2f);
                // bong bóng có vòng tiến độ: cho tạm đồ chờ thu 55% rồi đầy kho (chụp), trả lại như cũ
                var df = Home.Def(cfg, prod.def);
                var keep = prod.slots.Select(sl => sl.stock).ToList();
                double capH = Home.CapHours(cfg, df, prod.level);
                foreach (var k in new[] { 0.55, 1.0 })
                {
                    foreach (var sl in prod.slots)
                        if (sl.hero != null) sl.stock = Home.Rate(s, App.Data, sl.hero, prod) * capH * k;
                    Call(home, "Labels");
                    yield return new WaitForSecondsRealtime(0.7f);
                    yield return Shot($"2_bong_bong_{(int)(k * 100)}_{prod.def}");
                }
                for (int i = 0; i < prod.slots.Count; i++) prod.slots[i].stock = keep[i];
                Call(home, "Labels");
                yield return new WaitForSecondsRealtime(0.4f);
                var a = o.Rt.anchoredPosition;
                int n = Home.Def(cfg, prod.def).size;
                Call(home, "OnTap", new Vector2(a.x, -a.y - n * 24f));
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Shot("3_chon_" + prod.def);
                Call(home, "HideSel");
            }
            else Debug.LogWarning("[Thử] Nhà chưa có công trình sản xuất");

            var hud = Field<HomeRingButton>(home, "hudBuild");
            if (!hud)
            {
                Debug.LogWarning("[Thử] Prefab chưa có hàng nút icon: chạy menu \"PokiClash/Prefab/Nhà và side meta/Nhà: giao diện kiểu Critters\"");
                DayCycle.Override = null;
                yield break;
            }
            hud.Button.SimulateClick();
            yield return new WaitForSecondsRealtime(0.8f);
            yield return Shot("4_tam_xay");
            var tabs = Field<SketchButton[]>(home, "tabs");
            if (tabs != null && tabs.Length > 1 && tabs[1])
            {
                tabs[1].SimulateClick();
                yield return new WaitForSecondsRealtime(0.5f);
                yield return Shot("5_tab_san_xuat");
                tabs[0].SimulateClick();
                yield return null;
            }
            var tray = Field<RectTransform>(home, "tray");
            var card = tray ? tray.GetComponentsInChildren<SketchButton>().FirstOrDefault(b => b.Interactable) : null;
            if (card)
            {
                card.SimulateClick();
                yield return new WaitForSecondsRealtime(0.9f);
                yield return Shot("6_bong_ma_xay");
            }
            else
            {
                var main = Home.Main(s.home);
                if (main != null) Call(home, "StartMove", main, true);
                yield return new WaitForSecondsRealtime(0.9f);
                yield return Shot("6_bong_ma_doi");
            }
            Call(home, "CancelGhost");
            yield return null;
            hud.Button.SimulateClick(); // Xong
            yield return new WaitForSecondsRealtime(0.4f);
            DayCycle.Override = null;
            Debug.Log("[Thử] Nhà kiểu Critters: ảnh ở " + Path.GetFullPath(Dir));
        }
    }
}
