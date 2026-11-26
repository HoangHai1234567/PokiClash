// Hướng dẫn người mới (FTUE, GD_Claude/25_FTUE.md), phần gọi từ các màn: đăng ký chỗ cần khoanh theo khoá chuỗi (Mark), xin hiện
// một bước (Force: ép chạm đúng chỗ; Hint: khoanh, không chặn; Note: ghi chú tự tắt; Say: lời tướng đồng hành giữa màn). Bước đã
// xong (Core/Tutorial, cờ trong bản lưu) thì bỏ qua; bước ngoài chuỗi bắt buộc theo công tắc "Gợi ý" của Sổ tay. Lớp phủ: GuideOverlay.
// Mỗi bước ghi một dòng vào Logs/ftue.csv (chỉ Editor và bản Development) để biết người chơi dừng ở đâu.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using UnityEngine;

namespace PokiClash
{
    public static class Guide
    {
        public enum Mode { Force, Hint, Note, Say }

        static readonly Dictionary<string, RectTransform> targets = new Dictionary<string, RectTransform>();

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void ResetStatics()
        {
            targets.Clear();
            Tutorial.Off = false;
            MucActor = null;
        }

        static SaveData S => App.Save?.Data;

        // chỗ cần khoanh của một màn (nút, ô, hàng thẻ); gọi lại mỗi lần màn dựng lại
        public static void Mark(string key, Component c)
        {
            if (string.IsNullOrEmpty(key)) return;
            if (c) targets[key] = c.transform as RectTransform;
            else targets.Remove(key);
        }

        public static RectTransform Target(string key) =>
            key != null && targets.TryGetValue(key, out var r) && r ? r : null;

        public static bool Done(string id) => S == null || Tutorial.Done(S, id);

        // có hiện được bước này không (chưa xong, lớp phủ có, công tắc gợi ý)
        public static bool Can(string id, bool repeat = false)
        {
            var s = S;
            if (s == null || Tutorial.Off || !GuideOverlay.I) return false;
            if (!repeat && Tutorial.Done(s, id)) return false;
            return Tutorial.IsCore(id) || s.settings.hints;
        }

        public static bool Show(string id, Mode mode, string key, string text, Action done = null, bool repeat = false, string hero = null,
            float secs = 0, string clip = null)
        {
            if (!Can(id, repeat)) return false;
            return GuideOverlay.I.Enqueue(new GuideOverlay.Req
                { id = id, mode = mode, key = key, text = text, done = done, repeat = repeat, hero = hero, secs = secs, clip = clip });
        }

        public static bool Force(string id, string key, string text, Action done = null, bool repeat = false) =>
            Show(id, Mode.Force, key, text, done, repeat);

        public static bool Hint(string id, string key, string text, float secs = 7, Action done = null) =>
            Show(id, Mode.Hint, key, text, done, false, null, secs);

        public static bool Note(string id, string key, string text, float secs = 3.4f) => Show(id, Mode.Note, key, text, null, false, null, secs);

        // lời tướng đồng hành có khoanh sáng một chỗ (nền tối quanh, vòng mực): chạm đâu cũng qua; chạm trúng chỗ khoanh không bấm
        // xuống vật bên dưới (vòng khoanh chặn chạm ở chế độ Say). Dùng để giới thiệu một thứ mà chưa bắt bấm (Nhà, Cửa hàng 2026-11-24)
        public static bool SayAt(string id, string key, string text, Action done = null) => Show(id, Mode.Say, key, text, done, false, S?.starter);

        // lời tướng đồng hành (chân dung ló ra cạnh ghi chú), chạm để tiếp
        public static bool Say(string id, string text, Action done = null, bool repeat = false)
        {
            var s = S;
            return Show(id, Mode.Say, null, text, done, repeat, s?.starter);
        }

        // người nói là nhân vật chính (cậu bé thuần thú sư của cốt truyện mở đầu, App/StoryIntro): chân dung bên trái ghi chú, tướng
        // đồng hành (nếu đã chọn) ló bên phải. Chưa có ảnh chân dung (Assets/03 Art/Story/nhan_vat.png) thì như Say.
        public const string Me = "@nhan_vat";

        public static bool SayMe(string id, string text, Action done = null, bool repeat = false) =>
            Show(id, Mode.Say, null, text, done, repeat, Me);

        // người nói là Lão Mực, dealer của đảo Casino (GD_Claude/31_LaoMuc_Dealer.md mục 4.5, 5; CasinoGuide): màn có Lão Mực đứng sẵn trên
        // sân khấu (ba lều, Hầm đấu, Trường đua) đặt MucActor khi vào và trả null khi ra: lớp phủ cho chính ông nói, không tối màn. Màn khác:
        // ông trồi lên góc dưới màn (từ ngực trở lên, rig trong Kit/HuongDan). clip: dáng mở câu (greet, react_*...), sau đó "talk" lặp.
        public const string Muc = "@lao_muc";
        public static DealerRig MucActor;

        public static bool SayMuc(string id, string text, string clip = null, Action done = null, bool repeat = false) =>
            Show(id, Mode.Say, null, text, done, repeat, Muc, 0, clip);

        // như SayMuc, khoanh sáng một chỗ (key) mà chưa bắt bấm; chỗ nằm trong hộp thoại đang mở thì lớp phủ hiện trên hộp
        public static bool SayMucAt(string id, string key, string text, string clip = null, Action done = null, bool repeat = false) =>
            Show(id, Mode.Say, key, text, done, repeat, Muc, 0, clip);

        // câu bình phẩm của Lão Mực: ghi chú tự tắt, không chặn chạm, không theo cờ hướng dẫn hay công tắc Gợi ý; một câu một lúc.
        // key: hiện cạnh chỗ đó (bắt buộc khi đang mở hộp thoại, không thì chờ hộp đóng)
        public static bool Quip(string text, string clip = null, string key = null, float secs = 2.8f)
        {
            const string id = "muc_quip";
            if (S == null || Tutorial.Off || !GuideOverlay.I || GuideOverlay.I.Has(id)) return false;
            return GuideOverlay.I.Enqueue(new GuideOverlay.Req
                { id = id, mode = Mode.Note, key = key, text = text, repeat = true, hero = Muc, secs = secs, clip = clip });
        }

        // đang hiện hoặc đang chờ hiện bước id
        public static bool Pending(string id) => GuideOverlay.I && GuideOverlay.I.Has(id);

        // lớp phủ đang chặn chạm (bước ép, lời tướng)
        public static bool Blocking => GuideOverlay.I && GuideOverlay.I.Blocking;

        public static bool Idle => !GuideOverlay.I || GuideOverlay.I.Idle;

        // đánh dấu xong mà không hiện (bước bị bỏ qua vì người chơi đã tự làm), và gỡ khỏi hàng chờ
        public static void Skip(params string[] ids)
        {
            var s = S;
            if (s == null) return;
            foreach (var id in ids)
            {
                Tutorial.Mark(s, id);
                if (GuideOverlay.I) GuideOverlay.I.Cancel(id);
            }
            App.Save.Save();
        }

        public static void Cancel(string id)
        {
            if (GuideOverlay.I) GuideOverlay.I.Cancel(id);
        }

        internal static void Log(string id, string what)
        {
#if UNITY_EDITOR || DEVELOPMENT_BUILD
            try
            {
                string dir = Application.isEditor ? System.IO.Path.Combine(Application.dataPath, "..", "Logs")
                    : System.IO.Path.Combine(Application.persistentDataPath, "Logs");
                System.IO.Directory.CreateDirectory(dir);
                string path = System.IO.Path.Combine(dir, "ftue.csv");
                bool head = !System.IO.File.Exists(path);
                using (var w = new System.IO.StreamWriter(path, true))
                {
                    if (head) w.WriteLine("luc,buoc,su_kien,giay_tu_luc_mo,cap,bi");
                    var s = S;
                    w.WriteLine($"{DateTime.Now:yyyy-MM-dd HH:mm:ss},{id},{what},{Time.realtimeSinceStartup:0.0},{s?.level ?? 0},{s?.balls ?? 0}");
                }
            }
            catch (Exception)
            {
                // ghi log hỏng thì thôi, không ảnh hưởng trò chơi
            }
#endif
        }
    }
}
