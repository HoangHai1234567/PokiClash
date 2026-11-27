// Dựng và chụp popup chọn một gói bản 4 (2026-11-27, OfferPopup.ShowGroup; GD_Claude/26 mục 17). Cờ (Unity đang không Play, biên dịch xong):
// - Temp/pop_group_build.flag: dựng lại Items/PopCot + Dialogs/PopUuDai (OfferPopupMenu.Build);
// - Temp/pop_group_tour.flag: tự Play từ Boot, mở nhóm Gói Khởi Hành 3 bậc (còn 47 giờ, rồi còn 40 phút), rồi popup theo ngày (Quà Nhập
//   Môn), gói lẻ (Ưu Đãi Nóng), Hết bi 3 gói, Lọ Bi, Hết bi lần đầu, quà trở lại; bản lưu sao lưu đầu tour, trả lại cuối tour; xong Stop.
// Menu "PokiClash/Thử/Cửa hàng/popup chọn gói: dựng + chụp". Ảnh: Temp/PokiShots/pop_chon_goi/; log "[Popup chọn gói]".
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
    public static class OfferGroupTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "pop_chon_goi");
        static string TempFile(string n) => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/" + n));
        static string LibFlag => TempFile("pop_group_build.flag");
        static string TourFlag => TempFile("pop_group_tour.flag");
        static string DataFlag => TempFile("pop_group_data.flag"); // nhập lại balance.json (như menu "PokiClash/Nhập dữ liệu")
        const string Key = "OfferGroupTour";
        static double nextPoll, tourStart;

        static void Log(string s)
        {
            Debug.Log("[Popup chọn gói] " + s);
            Directory.CreateDirectory(Dir);
            File.AppendAllText(Path.Combine(Dir, "nhat_ky.txt"), s + System.Environment.NewLine);
        }

        [MenuItem("PokiClash/Thử/Cửa hàng/popup chọn gói: dựng + chụp", priority = 164)]
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
                if (File.Exists(DataFlag))
                {
                    File.Delete(DataFlag);
                    bool ok = DataImporter.Run(true);
                    AssetDatabase.SaveAssets();
                    Log("nhập dữ liệu: " + (ok ? "xong" : "LỖI"));
                    return;
                }
                if (File.Exists(LibFlag))
                {
                    File.Delete(LibFlag);
                    OfferPopupMenu.Build();
                    Log("đã dựng PopCot + PopUuDai");
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
                Debug.LogWarning("[Popup chọn gói] Tour quá 150 giây: dừng Play.");
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
                var c = D.Cfg.shop;
                var b = Shop.Of(S).offers;
                double now = SaveService.Now();

                IEnumerator Show(Popup p, string name)
                {
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.3f);
                    ShopSheet.OpenPopup(p, null);
                    yield return Shot(name + "_vao", 0.35f);
                    yield return Shot(name, 1.8f);
                }

                // nhóm Khởi Hành 3 bậc
                b.active.RemoveAll(o => o.pack != null && c.Pack(o.pack)?.group == "launch");
                foreach (var pk in c.packs.Where(q => q.group == "launch").OrderBy(q => q.price))
                    b.active.Add(new ActiveOffer { uid = pk.id + "_" + (++b.seq), tpl = pk.id, pack = pk.id, price = pk.price, created = now, until = now + 47 * 3600000.0, popped = true });
                var lead = b.active.Find(o => o.pack == "launch");
                Log("nhóm khởi hành: " + b.active.Count(o => o.pack != null && c.Pack(o.pack)?.group == "launch") + " gói");
                if (lead != null)
                {
                    yield return Show(new Popup { kind = "offer", id = lead.uid, key = "launch", free = true }, "nhom");
                    foreach (var o in b.active.Where(o => o.pack != null && c.Pack(o.pack)?.group == "launch")) o.until = now + 40 * 60000.0;
                    yield return Show(new Popup { kind = "offer", id = lead.uid, key = "launch" }, "nhom_gap");
                    yield return Shot("nhom_gap_2", 0.4f);
                    foreach (var o in b.active.Where(o => o.pack != null && c.Pack(o.pack)?.group == "launch")) o.until = now - 1;
                }

                // khung bản 3 không vỡ: theo ngày, gói lẻ, Hết bi
                Offers.EnsureStarter(S, D, now);
                var starter = b.active.Find(o => o.pack == "starter3");
                if (starter != null)
                {
                    starter.until = now + 71 * 3600000.0;
                    yield return Show(new Popup { kind = "offer", id = starter.uid, key = "starter3", free = true }, "ngay");
                    starter.until = now - 1;
                }
                var hot = Offers.Build(S, D, "hot", null, now, new Rng(3));
                if (hot != null) yield return Show(new Popup { kind = "offer", id = hot.uid, key = "hot", free = true }, "le");
                yield return Show(new Popup { kind = "piggy", free = true }, "lo_bi");
                yield return Show(new Popup { kind = "refill", first = true, free = true }, "het_bi_dau");
                var back = Offers.Build(S, D, "comeback", null, now, new Rng(5));
                if (back != null) yield return Show(new Popup { kind = "comeback", id = back.uid, key = "comeback", free = true }, "tro_lai");
                yield return Show(new Popup { kind = "refill", free = true }, "het_bi");
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
