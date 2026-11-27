// Dựng và chụp màn cửa hàng bản 3 (2026-11-27, GD_Claude/26 mục 17). Cờ (Unity đang không Play, biên dịch xong):
// - Temp/shop_v3_build.flag: dựng prefab màn cửa hàng (ShopPageMenu.BuildShopOnly);
// - Temp/shop_v3_sheet_build.flag: dựng tờ popup + ô gói + cụm ưu đãi ở sảnh (ShopMenu.BuildSheetAndHub);
// - Temp/shop_v3_tour.flag: tự Play (chạy cả khi Unity nằm nền), mở cửa hàng có đủ loại thẻ (ưu đãi hẹn giờ, Quà Nhập Môn, Chuỗi Quà, Lọ Bi,
//   trứng trong túi, vé), chụp đầu trang, cuộn 8 nấc, bấm mục Trứng / Đặc quyền ở cột trái; rồi tờ popup (Lọ Bi, Chuỗi Quà, giới thiệu
//   Quỹ / thẻ, quà hôm nay), trang con (Quỹ, Chuỗi, vé), cụm ưu đãi ở sảnh; bản lưu sao lưu đầu tour, trả lại cuối tour; xong Stop.
// Menu "PokiClash/Thử/Cửa hàng/bản 3: chụp màn cửa hàng". Ảnh: Temp/PokiShots/cua_hang_v3/; log "[Cửa hàng v3]".
using System.Collections;
using System.IO;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class ShopV3Tour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "cua_hang_v3");
        static string TempFile(string n) => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/" + n));
        static string BuildFlag => TempFile("shop_v3_build.flag");
        static string SheetFlag => TempFile("shop_v3_sheet_build.flag");
        static string TourFlag => TempFile("shop_v3_tour.flag");
        const string Key = "ShopV3Tour";
        static double nextPoll, tourStart;

        static void Log(string s)
        {
            Debug.Log("[Cửa hàng v3] " + s);
            Directory.CreateDirectory(Dir);
            File.AppendAllText(Path.Combine(Dir, "nhat_ky.txt"), s + System.Environment.NewLine);
        }

        [MenuItem("PokiClash/Thử/Cửa hàng/bản 3: chụp màn cửa hàng", priority = 162)]
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
                if (File.Exists(BuildFlag))
                {
                    File.Delete(BuildFlag);
                    ShopPageMenu.BuildShopOnly();
                    Log("đã dựng prefab");
                    return;
                }
                if (File.Exists(SheetFlag))
                {
                    File.Delete(SheetFlag);
                    ShopMenu.BuildSheetAndHub();
                    Log("đã dựng tờ popup và cụm sảnh");
                    return;
                }
                if (!File.Exists(TourFlag)) return;
                File.Delete(TourFlag);
                SessionState.SetBool(Key, true);
                tourStart = EditorApplication.timeSinceStartup;
                NuocFxMenu.PlayTuBoot(); // Play từ cảnh Boot, giữ cảnh đang mở (trình soạn có thể đang mở Hub.unity: Play thẳng không có App)
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false)) Application.runInBackground = true;
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 180)
            {
                Debug.LogWarning("[Cửa hàng v3] Tour quá 180 giây: dừng Play.");
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
                double now = SaveService.Now();
                App.Modals.CloseAll();
                Shop.Of(S).AddItem(Eggs.Key(2), 3);
                Shop.Of(S).piggy = 900;
                Offers.EnsureStarter(S, D, now);
                Offers.Build(S, D, "flash", null, now, new Rng(2));
                Shop.ChainStart(S, D.Cfg.shop, now);
                Shop.Grant(S, D, new System.Collections.Generic.List<ShopItem> { new ShopItem { k = Shop.Ticket, n = 1, r = 2 } }, now, new Rng(1));
                App.Modals.CloseAll();
                var page = ShopPage.Open();
                yield return Shot("00_dau", 1.4f);
                var scroll = page.GetComponentInChildren<ScrollRect>();
                for (int i = 1; i <= 8; i++)
                {
                    scroll.velocity = Vector2.zero;
                    scroll.verticalNormalizedPosition = 1 - i / 8f;
                    yield return Shot($"{i:00}_cuon");
                }
                // bấm mục ở cột trái: nhảy tới mục, ô chọn đổi theo
                foreach (var id in new[] { "eggs", "perks" })
                {
                    var b = page.GetComponentsInChildren<UI.SketchButton>(true).FirstOrDefaultByName("muc_" + id);
                    if (b) b.SimulateClick();
                    else Log("không thấy nút muc_" + id);
                    yield return Shot("muc_" + id, 0.9f);
                }
                // tờ popup (trừ popup bán: OfferPopup) và trang con
                string card = null;
                foreach (var pk in D.Cfg.shop.packs)
                    if (pk.kind == "card")
                    {
                        card = pk.id;
                        break;
                    }
                var pops = new System.Collections.Generic.List<Popup>
                {
                    new Popup { kind = "piggy", free = true }, new Popup { kind = "chain", free = true }, new Popup { kind = "intro", id = "fund", key = "intro_fund" },
                    new Popup { kind = "claims", free = true },
                };
                if (card != null) pops.Insert(3, new Popup { kind = "intro", id = card, key = "intro_card" });
                foreach (var pop in pops)
                {
                    App.Modals.CloseAll();
                    ShopSheet.OpenPopup(pop, null);
                    yield return Shot("to_" + pop.kind + (pop.id != null ? "_" + pop.id : ""), 0.9f);
                }
                App.Modals.CloseAll();
                ShopSheet.OpenFund();
                yield return Shot("trang_quy", 0.9f);
                App.Modals.CloseAll();
                ShopSheet.OpenChain();
                yield return Shot("trang_chuoi", 0.9f);
                App.Modals.CloseAll();
                if (Shop.Of(S).tickets.Count > 0)
                {
                    ShopSheet.OpenTicket(false, 0);
                    yield return Shot("trang_ve", 0.9f);
                }
                // cụm ưu đãi ở sảnh (thở: chụp hai nhịp)
                App.Modals.CloseAll();
                yield return Shot("sanh_1", 1.6f);
                yield return Shot("sanh_2", 0.9f);
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

        static T FirstOrDefaultByName<T>(this T[] arr, string name) where T : Component
        {
            foreach (var x in arr)
                if (x.name == name)
                    return x;
            return null;
        }
    }
}
