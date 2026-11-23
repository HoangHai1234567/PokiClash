// Tour thử cửa hàng trong game thật (GD_Claude/26 mục 7): các chỗ cửa hàng gắn vào trận và máy bi, chạy qua đúng đường người chơi đi.
// 1. trận thắng: hộp kết quả có nút "Nhận ×2" (quảng cáo giả lập 3 giây) rồi hộp Thưởng ×2;
// 2. thua 2 lần liền cùng ải: dòng "Thua N lần liền" + nút "Tiếp sức +15%", bấm thì vào lại trận có tiếp sức (toast), thua tiếp lần 3;
// 3. máy bi: còn bi mà thiếu cho mức cược thì tự hạ cược; hết hẳn bi thì popup Hết bi;
// 4. máy bi: rương gỗ trong khay thì hỏi "Nâng rương?", xem quảng cáo thành rương bạc.
// Ảnh vào Temp/PokiShots/cua_hang_tran/. Sao lưu file bản lưu đầu tour, trả lại trong finally rồi đọc lại file kiểm.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using Progress = PokiClash.Core.Progress;

namespace PokiClash.EditorTools
{
    public static class ShopPlayTour
    {
        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();
        static string Dir => Path.Combine(PlayTour.ShotDir, "cua_hang_tran");
        static int shot;
        static readonly List<string> log = new List<string>();

        [MenuItem("PokiClash/Thử/Khác/Cửa hàng∕trận (Nhận ×2, Tiếp sức), máy bi (hạ cược, Hết bi, nâng rương) (đang Play)", priority = 161)]
        static void Run()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Cửa hàng] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Tour());
        }

        static void Note(string s)
        {
            log.Add(s);
            Debug.Log("[Cửa hàng/tour] " + s);
        }

        static IEnumerator Shot(string name, float wait = 0.7f)
        {
            yield return new WaitForSecondsRealtime(wait);
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, $"{shot++:00}_{name}.jpg"), tex.EncodeToJPG(85));
            Object.Destroy(tex);
        }

        static SketchButton Button(string label)
        {
            string want = Loc.T(label).ToUpperInvariant();
            return Object.FindObjectsByType<SketchButton>(FindObjectsInactive.Exclude, FindObjectsSortMode.None)
                .FirstOrDefault(b => b.isActiveAndEnabled && b.Label && b.Label.text.StartsWith(want));
        }

        static SketchButton Named(string name) =>
            Object.FindObjectsByType<SketchButton>(FindObjectsInactive.Exclude, FindObjectsSortMode.None).FirstOrDefault(b => b.isActiveAndEnabled && b.name == name);

        static IEnumerator Until(System.Func<bool> ok, float seconds)
        {
            float t0 = Time.realtimeSinceStartup;
            while (!ok() && Time.realtimeSinceStartup - t0 < seconds) yield return null;
        }

        static IEnumerator Go(string scene, object args = null)
        {
            App.Modals.CloseAll();
            App.Router.Go(scene, args);
            yield return new WaitForSecondsRealtime(0.2f);
            yield return Until(() => !App.Router.Busy && App.Router.Current == scene, 30);
            yield return new WaitForSecondsRealtime(0.5f);
        }

        // vào trận, bật tự đánh nhanh ×4, chờ hộp kết quả
        static IEnumerator Fight(BattleArgs args, string tag)
        {
            yield return Go(SceneIds.Battle, args);
            yield return PlayFight(tag);
        }

        static IEnumerator PlayFight(string tag)
        {
            var ctl = Object.FindAnyObjectByType<BattleController>();
            if (!ctl)
            {
                Note("không thấy BattleController (" + tag + ")");
                yield break;
            }
            var me = ctl.Battle.ActiveOf(0);
            Note($"{tag}: tướng ta {me.Name} máu {me.maxHp:0}, công {me.atk:0}");
            yield return Until(() => ctl.WaitingPlayer, 25);
            ctl.SetAuto(true);
            ctl.FastForward(4);
            yield return Until(() => App.Modals.Count > 0, 180);
            yield return new WaitForSecondsRealtime(1.2f);
            Note($"{tag}: {(ctl.Battle.winner == 0 ? "thắng" : "thua")} sau {ctl.Battle.round} hiệp; chuỗi thua {S.shop?.offers.lossStreak} ở ải {S.shop?.offers.lossStage}; hàng popup {OfferHost.Pending}");
        }

        static void Call(object o, string method, params object[] a)
        {
            var m = o.GetType().GetMethod(method, BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public);
            m.Invoke(o, a);
        }

        static T Field<T>(object o, string name) =>
            (T)o.GetType().GetField(name, BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public).GetValue(o);

        static void SetField(object o, string name, object v) =>
            o.GetType().GetField(name, BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public).SetValue(o, v);

        static void ClearOfferQueue()
        {
            var f = typeof(OfferHost).GetField("queue", BindingFlags.Static | BindingFlags.NonPublic);
            (f?.GetValue(null) as System.Collections.IList)?.Clear();
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
                if (BootTitle.Current) BootTitle.Dismiss();
                yield return Until(() => !BootTitle.Current && !App.Booting, 10);
                App.Modals.CloseAll();
                ClearOfferQueue();
                var s = S;
                Tutorial.Skip(s);
                Offers.EnsureStarter(s, D, Now);
                var st = Shop.Of(s);
                st.sessions = Mathf.Max(st.sessions, 3); // không còn là người mới (Gói Tiếp Sức không mời người mới)
                st.offers.lastAuto = st.offers.lastBuy = st.offers.lastAd = 0;

                // ---------- 1. trận thắng: Nhận ×2 ----------
                const string strong = "nham_than";
                var hp = s.Hero(strong);
                hp.owned = true;
                hp.star = D.Cfg.maxStar;
                if (s.level < 55) s.level = 55;
                var easy = D.Stages.Where(x => x.idx == 1).OrderBy(x => x.id).First();
                Progress.WinStage(s, D, easy.id, new Rng(1)); // ải đã thắng một lần (thưởng thường, không phải lần đầu)
                App.Save.Save();
                yield return Fight(new BattleArgs { stageId = easy.id, team = new List<string> { strong } }, "trận thắng ải " + easy.id);
                yield return Shot("thang_co_nut_nhan_x2");
                var x2 = Named("nut_qc_" + Ads.WinDouble);
                Note(x2 ? "có nút Nhận ×2: " + x2.Label.text : "KHÔNG có nút Nhận ×2");
                if (x2)
                {
                    int balls0 = s.balls;
                    x2.SimulateClick();
                    yield return Shot("quang_cao_gia", 1.0f);
                    yield return Until(() => !x2.isActiveAndEnabled, 8); // quảng cáo giả 3 giây xong thì nút ẩn, hộp Thưởng ×2 mở
                    yield return Shot("thuong_x2", 1.5f);
                    Note($"Nhận ×2: bi {balls0} → {s.balls}, nút còn hiện: {x2.isActiveAndEnabled}");
                }

                // ---------- 2. thua liền: Tiếp sức ----------
                var hard = D.Stages.OrderByDescending(x => x.id).First(x => x.enemies.Count > 0);
                string weak = s.starter ?? s.team.FirstOrDefault();
                s.Hero(weak).owned = true;
                s.level = 1;
                s.balls = 0; // khỏi lọt "thả bi" vào cách làm ngay
                st.offers.lossStage = hard.id;
                st.offers.lossStreak = 1; // lần thua này là lần 2 liền
                App.Save.Save();
                yield return Fight(new BattleArgs { stageId = hard.id, team = new List<string> { weak } }, "trận thua 1 ải " + hard.id);
                yield return Shot("thua_2_lan_tiep_suc");
                var boost = Named("nut_qc_" + Ads.BattleRetry);
                Note(boost ? "có nút Tiếp sức: " + boost.Label.text : "KHÔNG có nút Tiếp sức (FreeFix: " + Offers.FreeFix(s, D, new[] { weak }) + ")");
                if (boost)
                {
                    boost.SimulateClick();
                    yield return Shot("quang_cao_gia_tiep_suc", 1.0f);
                    yield return Until(() => App.Router.Current == SceneIds.Battle && !App.Router.Busy && App.Modals.Count == 0, 15);
                    yield return Shot("tran_co_tiep_suc", 0.5f);
                    yield return PlayFight("trận thua 2 (có tiếp sức)");
                    yield return Shot("thua_3_lan");
                }
                // Gói Tiếp Sức (thua 3 lần, không còn cách miễn phí) hiện khi về sảnh
                yield return Go(SceneIds.Hub);
                yield return Until(() => App.Modals.Count > 0, 6);
                yield return Shot("sanh_sau_3_tran_thua");
                Note("về sảnh sau 3 trận thua: hộp đang mở " + App.Modals.Count + ", hàng popup " + OfferHost.Pending);
                App.Modals.CloseAll();
                ClearOfferQueue();

                // ---------- 3. máy bi: hạ cược, Hết bi ----------
                s.level = 55;
                s.balls = 500;
                App.Save.Save();
                yield return Go(SceneIds.Machine);
                var mc = Object.FindAnyObjectByType<MachineScene>();
                if (!mc)
                {
                    Note("không thấy MachineScene");
                    yield break;
                }
                var steps = D.Cfg.xSteps.Where(q => Progress.XAllowed(s, D.Cfg).Contains(q.x)).OrderBy(q => q.x).ToList();
                if (steps.Count > 1)
                {
                    var top = steps.Last();
                    Call(mc, "PickX", top.x, top.balls);
                    s.balls = Mathf.Max(1, top.x - 1);
                    Call(mc, "RefreshUi");
                    yield return new WaitForSecondsRealtime(0.4f);
                    Call(mc, "DenyDrop");
                    yield return Shot("may_bi_ha_cuoc", 0.4f);
                    Note($"hạ cược: bi {s.balls}, cược ×{top.x} → ×{Field<int>(mc, "x")}");
                }
                else Note("chỉ có một mức cược, bỏ qua thử hạ cược");
                s.balls = 0;
                st.offers.lastRefill = 0;
                Call(mc, "RefreshUi");
                yield return new WaitForSecondsRealtime(0.3f);
                Call(mc, "DenyDrop");
                yield return Until(() => App.Modals.Count > 0, 6);
                yield return Shot("may_bi_het_bi");
                Note("hết bi: hộp đang mở " + App.Modals.Count);
                App.Modals.CloseAll();

                // ---------- 4. máy bi: nâng rương ----------
                yield return new WaitForSecondsRealtime(0.6f);
                SetField(mc, "upgradeAsked", false);
                s.chests.Add(new PendingChest { kind = "chest_wood", x = 1 });
                Call(mc, "RebuildTray");
                Call(mc, "OpenFromTray");
                yield return Until(() => App.Modals.Count > 0, 6);
                yield return Shot("hoi_nang_ruong");
                var up = Button("Nâng");
                Note(up ? "có hộp Nâng rương?" : "KHÔNG có hộp Nâng rương?");
                if (up)
                {
                    up.SimulateClick();
                    yield return Shot("quang_cao_gia_nang_ruong", 1.0f);
                    MachineChestOpen open = null;
                    yield return Until(() => (open = Object.FindAnyObjectByType<MachineChestOpen>()) != null, 10);
                    yield return Shot("ruong_bac_bay_vao", 1.2f);
                    if (open)
                    {
                        for (int i = 0; i < 20 && open && Field<IList>(open, "slots").Cast<object>().Any(q => !Field<bool>(q, "opened")); i++)
                        {
                            Call(open, "TapEmpty");
                            yield return new WaitForSecondsRealtime(0.5f);
                        }
                        yield return Shot("ruong_bac_mo", 2.0f);
                        if (open) SetField(open, "done", true);
                    }
                    yield return Until(() => Object.FindAnyObjectByType<MachineChestOpen>() == null, 6);
                }
                yield return new WaitForSecondsRealtime(0.8f);
                Note($"Xong: {shot} ảnh ở {Dir}");
            }
            finally
            {
                App.Modals.CloseAll();
                ClearOfferQueue();
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                    bool same = File.ReadAllText(path) == backup;
                    Note(same ? "đã trả bản lưu cũ (đọc lại khớp)" : "CẢNH BÁO: bản lưu đọc lại không khớp bản sao lưu");
                }
                File.WriteAllLines(Path.Combine(Dir, "log.txt"), log);
                App.Router.Go(SceneIds.Hub);
            }
        }
    }
}
