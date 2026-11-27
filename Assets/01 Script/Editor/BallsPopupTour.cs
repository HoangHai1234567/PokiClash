// Tour thử popup bi ở máy bi (người dùng 2026-11-27: "hết hoặc gần hết bi thì bắn popup gạ mua gói bi"):
// 1. thả một đợt ×1, cuối đợt còn 7 bi (dưới một đợt đầy) → popup "Sắp hết bi!" tự bật khi máy rảnh; đóng (không mua);
// 2. thả một đợt nữa, cuối đợt 0 bi → popup "Hết bi!" tự bật, không cần bấm thả;
// 3. thả một đợt nữa còn 7 bi → KHÔNG có popup (vừa đóng "Sắp hết bi!": 24 giờ mới bật lại).
// Cờ Temp/balls_popup_tour.flag (Unity không Play: tự vào Play, chạy, Stop) hoặc menu khi đang Play. Ảnh Temp/PokiShots/popup_bi/, log "[Popup bi]".
// Sao lưu file bản lưu đầu tour, trả lại trong finally.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using PokiClash.Core;
using PokiClash.Game;
using TMPro;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class BallsPopupTour
    {
        const BindingFlags F = BindingFlags.NonPublic | BindingFlags.Public | BindingFlags.Instance;
        const string Key = "BallsPopupTour";
        static double nextPoll, tourStart;
        static bool fromFlag;
        static int shot;
        static readonly List<string> log = new List<string>();
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/balls_popup_tour.flag"));
        static string Dir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots/popup_bi"));
        static SaveData S => App.Save.Data;
        static GameData D => App.Data;

        [MenuItem("PokiClash/Thử/Cửa hàng/máy bi: thả hết đợt → popup Sắp hết bi, Hết bi (chụp)", priority = 162)]
        static void Run()
        {
            if (EditorApplication.isPlaying)
            {
                if (App.I != null) App.I.StartCoroutine(Tour());
                return;
            }
            File.WriteAllText(Flag, "menu");
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
                if (!File.Exists(Flag)) return;
                File.Delete(Flag);
                SessionState.SetBool(Key, true);
                tourStart = EditorApplication.timeSinceStartup;
                EditorApplication.isPlaying = true;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false)) Application.runInBackground = true; // Unity nằm nền thì vòng game đứng
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 300)
            {
                Debug.LogWarning("[Popup bi] Tour quá 300 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null && !App.Booting)
            {
                SessionState.SetBool(Key, false);
                fromFlag = true;
                if (BootTitle.Current) BootTitle.Dismiss();
                App.I.StartCoroutine(Tour());
            }
        }

        static object Get(object o, string f) => o.GetType().GetField(f, F)?.GetValue(o);
        static void Set(object o, string f, object v) => o.GetType().GetField(f, F)?.SetValue(o, v);
        static void Call(object o, string m, params object[] a) => o.GetType().GetMethod(m, F)?.Invoke(o, a);

        static void Note(string s)
        {
            log.Add(s);
            Debug.Log("[Popup bi] " + s);
        }

        static IEnumerator Until(System.Func<bool> ok, float seconds)
        {
            float t0 = Time.realtimeSinceStartup;
            while (!ok() && Time.realtimeSinceStartup - t0 < seconds) yield return null;
        }

        static IEnumerator Shot(string name, float wait = 0.8f)
        {
            yield return new WaitForSecondsRealtime(wait);
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, $"{shot++:00}_{name}.jpg"), tex.EncodeToJPG(85));
            Object.Destroy(tex);
        }

        // tiêu đề popup bi đang mở (tờ cửa hàng cũ hay popup kiểu mới), null nếu chưa có
        static string PopupText()
        {
            Object dlg = Object.FindAnyObjectByType<ShopSheet>();
            if (!dlg) dlg = Object.FindAnyObjectByType<OfferPopup>();
            if (!dlg) return null;
            var p = Get(dlg, "p");
            if (p == null) return dlg.GetType().Name;
            string T(string f) => (p.GetType().GetField(f)?.GetValue(p) as TextMeshProUGUI)?.text ?? "";
            return $"{dlg.GetType().Name}: \"{T("title")}\" / \"{T("sub")}\"";
        }

        static void ClearOfferQueue()
        {
            var f = typeof(OfferHost).GetField("queue", BindingFlags.Static | BindingFlags.NonPublic);
            (f?.GetValue(null) as IList)?.Clear();
        }

        // thả một đợt ×1 (nút Liên); lúc bi rơi hết (SessionEnd bắt đầu) đặt số bi cuối đợt, bỏ rương cho khỏi màn mở rương;
        // rồi chờ popup bi (bảng lên cấp thì đóng cho popup tới lượt). Trả tiêu đề popup qua out[0]
        static IEnumerator Session(MachineScene mc, int ballsAtEnd, float waitPopup, string[] outText)
        {
            outText[0] = null;
            S.balls = Mathf.Max(S.balls, 40);
            Call(mc, "RefreshUi");
            yield return Until(() => mc.Idle, 10);
            Call(mc, "Auto");
            yield return Until(() => (bool)Get(mc, "ending"), 120);
            if (!(bool)Get(mc, "ending"))
            {
                Note("đợt thả không kết thúc trong 120 giây");
                yield break;
            }
            S.balls = ballsAtEnd;
            S.chests.Clear();
            Call(mc, "RebuildTray");
            Call(mc, "RefreshUi");
            yield return Until(() => mc.Idle, 30);
            float t0 = Time.realtimeSinceStartup;
            while (Time.realtimeSinceStartup - t0 < waitPopup)
            {
                var t = PopupText();
                if (t != null)
                {
                    outText[0] = t;
                    yield break;
                }
                if (App.Modals.Count > 0) App.Modals.CloseAll(); // bảng lên cấp
                yield return null;
            }
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
                yield return Until(() => !BootTitle.Current && !App.Booting && !App.Router.Busy, 20);
                App.Modals.CloseAll();
                ClearOfferQueue();
                var s = S;
                Tutorial.Skip(s);
                var st = Shop.Of(s);
                st.sessions = Mathf.Max(st.sessions, 3);
                var b = st.offers;
                b.lastAuto = b.lastBuy = b.lastAd = b.lastRefill = 0;
                b.autoCount = 0;
                b.muteDay = -1;
                b.refillSeen = true; // đã gặp Hết bi lần đầu (lần đầu chưa bán gói)
                b.dismiss.Remove("refill_low");
                b.dismissAt.Remove("refill_low");
                if (s.level < 20) s.level = 20;
                s.balls = 40;
                s.chests.Clear();
                App.Save.Save();

                App.Router.Go(SceneIds.Machine);
                yield return new WaitForSecondsRealtime(0.3f);
                yield return Until(() => !App.Router.Busy && App.Router.Current == SceneIds.Machine, 30);
                yield return new WaitForSecondsRealtime(1.2f);
                var mc = Object.FindAnyObjectByType<MachineScene>();
                if (!mc)
                {
                    Note("không thấy MachineScene");
                    yield break;
                }
                App.Modals.CloseAll();
                ClearOfferQueue();
                Call(mc, "PickX", 1, 1);
                Set(mc, "upgradeAsked", true); // khỏi hộp "Nâng rương?" giữa đợt
                Note($"vào máy bi: cấp {s.level}, cược ×{Get(mc, "x")}, một đợt tối đa {D.Cfg.MaxPerDrop(s.level)} bi");
                var txt = new string[1];

                // 1. Sắp hết bi
                yield return Session(mc, 7, 12, txt);
                Note("1. cuối đợt còn 7 bi: " + (txt[0] ?? "KHÔNG có popup") + $"; hàng popup {OfferHost.Pending}");
                yield return Shot("1_sap_het_bi");
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.6f);
                Note($"   đóng: refill_low bị đóng {(b.dismiss.TryGetValue("refill_low", out var n1) ? n1 : 0)} lần, lastRefill {(b.lastRefill > 0 ? "đã ghi" : "chưa ghi")}");

                // 2. Hết bi (nhịp 20 phút chung với Sắp hết bi: xoá để thử ngay)
                b.lastRefill = 0;
                yield return Session(mc, 0, 12, txt);
                Note("2. cuối đợt 0 bi: " + (txt[0] ?? "KHÔNG có popup") + $"; hàng popup {OfferHost.Pending}");
                yield return Shot("2_het_bi");
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.6f);

                // 3. vừa đóng Sắp hết bi: 24 giờ chưa bật lại
                b.lastRefill = 0;
                yield return Session(mc, 7, 5, txt);
                Note("3. còn 7 bi, vừa đóng Sắp hết bi: " + (txt[0] == null ? "không có popup (đúng)" : "CÓ popup (sai): " + txt[0]) + $"; hàng popup {OfferHost.Pending}");
                yield return Shot("3_khong_popup");
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
                    Note(File.ReadAllText(path) == backup ? "đã trả bản lưu cũ (đọc lại khớp)" : "CẢNH BÁO: bản lưu đọc lại không khớp bản sao lưu");
                }
                File.WriteAllLines(Path.Combine(Dir, "log.txt"), log);
                Debug.Log("[Popup bi] KẾT THÚC TOUR");
                if (fromFlag)
                {
                    fromFlag = false;
                    tourStart = 0;
                    EditorApplication.isPlaying = false;
                }
            }
        }
    }
}
