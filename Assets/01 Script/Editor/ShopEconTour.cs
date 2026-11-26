// Tour chụp các popup cửa hàng thêm ở đợt cân bằng kinh tế 2026-11-27 (GD_Claude/33 mục 0): Gói Vượt Mốc (tướng đi trước 3 mốc, trọn
// bộ), nạp đầu 3 bậc chọn một (ba Gói Khởi Hành), Lọ Bi vừa đập (đồng hồ chờ), và trang cửa hàng mục Ưu đãi có cả ba thứ.
// Menu "PokiClash/Thử/Cửa hàng/tour kinh tế: Vượt Mốc, Khởi Hành 3 bậc, Lọ Bi (đang Play)". Ảnh và log.txt vào
// Temp/PokiShots/cua_hang_kinh_te/. Sao lưu file bản lưu đầu tour, trả lại trong finally rồi đọc lại file kiểm.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class ShopEconTour
    {
        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();
        static string Dir => Path.Combine(PlayTour.ShotDir, "cua_hang_kinh_te");
        static int shot;
        static readonly List<string> log = new List<string>();

        [MenuItem("PokiClash/Thử/Cửa hàng/tour kinh tế: Vượt Mốc, Khởi Hành 3 bậc, Lọ Bi (đang Play)", priority = 162)]
        static void Run()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Cửa hàng] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Tour());
        }

        static IEnumerator Shot(string name, float wait = 0.8f)
        {
            yield return new WaitForSecondsRealtime(wait);
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, $"{shot++:00}_{name}.jpg"), tex.EncodeToJPG(85));
            Object.Destroy(tex);
        }

        static void Note(string s)
        {
            log.Add(s);
            Debug.Log("[Cửa hàng kinh tế] " + s);
        }

        static IEnumerator Tour()
        {
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            shot = 0;
            log.Clear();
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            try
            {
                var c = D.Cfg.shop;
                App.Modals.CloseAll();
                Tutorial.Skip(S);
                S.shop = null;
                var st = Shop.Of(S);
                st.installAt = Now - 5 * 86400000.0;
                st.sessions = 5;
                var b = st.offers;

                // 1. Gói Vượt Mốc ở hai cỡ: người mới (cấp 20, tướng mốc 6) và giữa game (cấp 100, tướng mốc 10)
                var ms = Offers.MilestoneStages(D, Elem.Thuy);
                foreach (var (lv, moc) in new[] { (20, 6), (100, 10) })
                {
                    S.level = lv;
                    string hero = Teams.StageLead(ms[moc - 1], D).hero;
                    S.Hero(hero).owned = false;
                    var o = Offers.Build(S, D, "jump", hero, Now, new Rng(1));
                    Note($"Vượt Mốc cấp {lv}, mốc {moc} ({D.Hero(hero).name}): {o.price} USD, ×{Shop.OfferMult(S, D, o):F1}, " +
                         string.Join(", ", o.items.Select(it => it.k + " " + it.n)));
                    ShopSheet.OpenPopup(new Popup { kind = "offer", id = o.uid, key = "jump", free = true }, null);
                    yield return Shot($"vuot_moc_cap{lv}_moc{moc}");
                    App.Modals.CloseAll();
                    o.until = Now; // đóng gói thử này để không chồng lên gói sau
                }

                // 2. nạp đầu 3 bậc: ba gói cùng nhóm, cùng đồng hồ; popup của gói đứng đầu vẽ cả ba
                S.level = 12;
                double until = Now + 48 * 3600000.0;
                foreach (var pk in c.packs.Where(q => q.group == "launch").OrderBy(q => q.price))
                    b.active.Add(new ActiveOffer { uid = pk.id + "_" + (++b.seq), tpl = pk.id, pack = pk.id, price = pk.price, created = Now, until = until });
                var lead = b.active.Find(o => o.pack == "launch" && !o.bought && o.until > Now);
                ShopSheet.OpenPopup(new Popup { kind = "offer", id = lead.uid, key = "launch", free = true }, null);
                yield return Shot("khoi_hanh_3_bac");
                App.Modals.CloseAll();
                Note("Khởi Hành 3 bậc: " + string.Join(" | ", c.packs.Where(q => q.group == "launch").OrderBy(q => q.price)
                    .Select(q => $"{q.Name} {q.price} USD ×{Shop.PackMult(S, D, q):F1}")));

                // 3. Lọ Bi vừa đập: ô Lọ Bi ghi đồng hồ chờ
                st.piggy = Shop.PiggyCap(S, c);
                st.piggyAt = Now - 3600000.0;
                Note($"Lọ Bi: đập được {Shop.PiggyCanBreak(S, c, Now)}, còn chờ {Shop.PiggyWait(S, c, Now) / 3600000.0:F0} giờ");

                // 4. trang cửa hàng, mục Ưu đãi: bong bóng và thẻ của các gói trên
                ShopSheet.OpenShop("offers");
                yield return Shot("trang_uu_dai", 1.2f);
                App.Modals.CloseAll();
                App.Router.Go(SceneIds.Hub); // vào lại sảnh cho hàng bong bóng vẽ lại theo ưu đãi vừa thêm
                yield return new WaitForSecondsRealtime(0.3f);
                for (float t = 0; (App.Router.Busy || App.Router.Current != SceneIds.Hub) && t < 20; t += Time.unscaledDeltaTime) yield return null;
                yield return Shot("sanh_bong_bong", 1.5f);
                Note($"Xong: {shot} ảnh ở {Dir}");
            }
            finally
            {
                App.Modals.CloseAll();
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                    Note(File.ReadAllText(path) == backup ? "đã trả bản lưu cũ (đọc lại khớp)" : "CẢNH BÁO: bản lưu đọc lại không khớp bản sao lưu");
                }
                File.WriteAllLines(Path.Combine(Dir, "log.txt"), log);
            }
        }
    }
}
