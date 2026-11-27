// Chụp icon riêng từng loại ưu đãi (2026-11-27, uu2_<mã mẫu>.png, ShopUi.TplArt; GD_Claude/26 mục 17). Cờ (Unity đang không Play, biên dịch xong):
// - Temp/shop_uu2_lib.flag: dựng lại danh mục ảnh (ArtImporter.BuildLibrary) để danh mục có uu2_*;
// - Temp/shop_uu2_tour.flag: tự Play từ Boot (chạy cả khi Unity nằm nền), cột ưu đãi ở sảnh theo nhóm ba (Bất Ngờ / Nóng / Tiếp Sức,
//   Đồng Hành / Sắp Lên Sao / Vượt Mốc, Đảo Mới / Trở Lại / mẫu chưa có icon riêng), Chuỗi Quà; mục Ưu đãi của cửa hàng có đủ chín loại;
//   popup bán của Ưu Đãi Nóng, Đảo Mới, Bất Ngờ. Bản lưu sao lưu đầu tour, trả lại cuối tour; xong Stop.
// Menu "PokiClash/Thử/Cửa hàng/icon ưu đãi: chụp". Ảnh: Temp/PokiShots/uu_dai_icon/; log "[Icon ưu đãi]".
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class ShopOfferIconTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "uu_dai_icon");
        static string TempFile(string n) => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/" + n));
        static string LibFlag => TempFile("shop_uu2_lib.flag");
        static string TourFlag => TempFile("shop_uu2_tour.flag");
        const string Key = "ShopOfferIconTour";
        static double nextPoll, tourStart;

        static void Log(string s)
        {
            Debug.Log("[Icon ưu đãi] " + s);
            Directory.CreateDirectory(Dir);
            File.AppendAllText(Path.Combine(Dir, "nhat_ky.txt"), s + System.Environment.NewLine);
        }

        [MenuItem("PokiClash/Thử/Cửa hàng/icon ưu đãi: chụp", priority = 163)]
        static void Try()
        {
            if (EditorApplication.isPlaying)
            {
                if (App.I != null) App.I.StartCoroutine(Run(false));
                return;
            }
            File.WriteAllText(TourFlag, "1");
        }

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating) return;
            if (!EditorApplication.isPlayingOrWillChangePlaymode)
            {
                if (File.Exists(LibFlag))
                {
                    File.Delete(LibFlag);
                    var lib = ArtImporter.BuildLibrary();
                    int n = lib ? lib.art.Count(e => e.name != null && e.name.StartsWith("uu2_")) : 0;
                    Log($"đã dựng danh mục ảnh: {n} icon uu2_");
                    return;
                }
                if (!File.Exists(TourFlag)) return;
                File.Delete(TourFlag);
                SessionState.SetBool(Key, true);
                tourStart = EditorApplication.timeSinceStartup;
                NuocFxMenu.PlayTuBoot();
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false)) Application.runInBackground = true;
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 150)
            {
                Debug.LogWarning("[Icon ưu đãi] Tour quá 150 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null)
            {
                SessionState.SetBool(Key, false);
                BootTitle.Dismiss();
                App.I.StartCoroutine(Run(true));
            }
        }

        static IEnumerator Shot(string name, float wait = 0.7f)
        {
            yield return new WaitForSecondsRealtime(wait);
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, name + ".jpg"), tex.EncodeToJPG(90));
            Object.Destroy(tex);
            Log(name);
        }

        static IEnumerator Run(bool stop)
        {
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            yield return new WaitForSecondsRealtime(2f);
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            try
            {
                var S = App.Save.Data;
                var D = App.Data;
                var st = Shop.Of(S);
                double now = SaveService.Now();
                var rng = new Rng(7);
                string hero = S.heroes.FirstOrDefault(kv => kv.Value.owned).Key;
                string isle = "e:" + Keys.Of(Elements.All.First());
                Log("uu2_ trong danh mục: " + string.Join(", ", new[] { "flash", "hot", "relief", "companion", "nearstar", "jump", "newisle", "comeback", "chain", "offer" }
                    .Where(t => !App.Art.HasArt("uu2_" + t))) + " (thiếu)");

                ActiveOffer Make(string tpl)
                {
                    string ctx = tpl == "companion" || tpl == "nearstar" || tpl == "jump" ? hero : tpl == "newisle" ? isle : null;
                    var o = Offers.Build(S, D, tpl, ctx, now, rng);
                    if (o != null) o.popped = true;
                    Log(tpl + (o != null ? $": {o.items.Count} món" : ": không dựng được"));
                    return o;
                }

                var groups = new[] { new[] { "flash", "hot", "relief" }, new[] { "companion", "nearstar", "jump" }, new[] { "newisle", "comeback", "refill" } };
                for (int g = 0; g < groups.Length; g++)
                {
                    App.Modals.CloseAll();
                    st.offers.active.Clear();
                    st.chainUntil = 0;
                    foreach (var t in groups[g]) Make(t);
                    yield return Shot($"sanh_{g + 1}", 1.6f);
                }
                // Chuỗi Quà đứng sau các ưu đãi hẹn giờ
                App.Modals.CloseAll();
                st.offers.active.Clear();
                Make("hot");
                Shop.ChainStart(S, D.Cfg.shop, now);
                yield return Shot("sanh_chuoi", 1.6f);

                // mục Ưu đãi của cửa hàng: đủ chín loại
                st.offers.active.Clear();
                var all = new Dictionary<string, ActiveOffer>();
                foreach (var t in new[] { "hot", "flash", "relief", "companion", "nearstar", "jump", "newisle", "comeback" })
                {
                    var o = Make(t);
                    if (o != null) all[t] = o;
                }
                App.Modals.CloseAll();
                var page = ShopPage.Open();
                yield return Shot("cua_hang_1", 1.4f);
                var scroll = page.GetComponentInChildren<ScrollRect>();
                for (int i = 1; i <= 3; i++)
                {
                    scroll.velocity = Vector2.zero;
                    scroll.verticalNormalizedPosition = 1 - i * 0.12f;
                    yield return Shot($"cua_hang_{i + 1}");
                }

                // popup bán
                foreach (var t in new[] { "hot", "newisle", "flash" })
                {
                    if (!all.TryGetValue(t, out var o)) continue;
                    App.Modals.CloseAll();
                    ShopSheet.OpenPopup(new Popup { kind = "offer", id = o.uid, free = true }, null);
                    yield return Shot("popup_" + t, 1.0f);
                }
                Log("xong");
            }
            finally
            {
                App.Modals.CloseAll();
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                    Log(File.ReadAllText(path) == backup ? "đã trả bản lưu cũ (đọc lại khớp)" : "CẢNH BÁO: bản lưu đọc lại không khớp bản sao lưu");
                }
            }
            yield return new WaitForSecondsRealtime(0.5f);
            if (stop) EditorApplication.isPlaying = false;
        }
    }
}
