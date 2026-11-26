// Lời dẫn của Lão Mực trên đảo Casino (GD_Claude/31_LaoMuc_Dealer.md mục 4.5 và 5; mốc D6 + D7, 2026-11-27):
// - lần đầu ra đảo: ông đón ở bến (4 câu, khoanh Tháp Máy Bi và Bến câu) thay hộp chữ "Bến Lữ Khách";
// - lần đầu vào mỗi trò: 2–3 câu (ba lều: thay hộp Cách chơi tự mở; luật đầy đủ vẫn ở nút Cách chơi);
// - câu bình phẩm lúc chơi (Bến câu, Chợ đen, Quán trọ: những chỗ không có Lão Mực đứng sẵn).
// Hiện qua lớp phủ hướng dẫn (Guide.SayMuc, Guide.Quip): màn có Lão Mực đứng sẵn (ba lều, Hầm đấu, Trường đua) đặt Guide.MucActor để chính
// ông nói; màn khác ông trồi lên góc dưới màn. Cờ "đã xem" là "howto:<trò>" trong bản lưu đảo (như hộp Cách chơi của ba lều trước đây),
// không theo cờ FTUE, nên bản lưu cũ cũng được dẫn khi lần đầu ra đảo. Công tắc "Gợi ý" tắt thì không dẫn: màn lùi về cách cũ.
// Chỉ diễn và nói, không gạ chơi thêm hay gạ nạp bi (31 mục 1.2).
using System;
using System.Collections.Generic;
using PokiClash.Core;

namespace PokiClash
{
    public static class CasinoGuide
    {
        static SaveData S => App.Save?.Data;

        static readonly string[] Games =
            { Casino.Fishing, Casino.Inn, Casino.Race, Casino.Market, Casino.Underground, Casino.Blackjack, Casino.Roulette, Casino.Slot };

        public static bool Seen(string game) => S == null || Casino.Of(S).seen.Contains("howto:" + game);

        // tour Editor (chạy trên bản lưu thật): coi như đã nghe hết, vì lời dẫn chặn chạm
        public static void SkipAll(SaveData s)
        {
            if (s == null) return;
            foreach (var g in Games) Casino.MarkSeen(s, "howto:" + g);
        }

        struct Line
        {
            public string text, clip, key;
            public Line(string text, string clip = null, string key = null)
            {
                this.text = text;
                this.clip = clip;
                this.key = key;
            }
        }

        // xếp chuỗi câu vào lớp phủ; câu đầu không hiện được (Gợi ý tắt, tour tắt hướng dẫn, chưa có lớp phủ) thì trả false để màn lùi về
        // cách cũ. Đánh dấu đã xem ngay khi xếp được (khách rời màn giữa chừng thì thôi, không dẫn lại).
        static bool Run(string tag, IList<Line> lines, Action done)
        {
            for (int i = 0; i < lines.Count; i++)
            {
                var l = lines[i];
                string id = "muc_" + tag + "_" + i;
                Action after = i == lines.Count - 1 ? done : null;
                bool ok = string.IsNullOrEmpty(l.key)
                    ? Guide.SayMuc(id, l.text, l.clip, after, true)
                    : Guide.SayMucAt(id, l.key, l.text, l.clip, after, true);
                if (!ok && i == 0) return false;
            }
            return true;
        }

        static bool First(string game, IList<Line> lines, Action done = null)
        {
            if (Seen(game)) return false;
            if (!Run(game, lines, done)) return false;
            Casino.MarkSeen(S, "howto:" + game);
            App.Save.Save();
            return true;
        }

        // ---------- lần đầu ra đảo ----------

        // khoá chỗ khoanh trên bản đồ đảo: "casino_" + mã điểm chạm (tower, fishing...), CasinoScene đăng ký khi dựng
        public static string SpotKey(string spotId) => "casino_" + spotId;

        public static bool Port(Action done) =>
            Run("port", new[]
            {
                new Line(Loc.T("Ồ, khách lạ! Chào mừng tới Bến Lữ Khách, chỗ nghỉ chân của mọi thám hiểm gia. Ta là Lão Mực, ở đây ai cũng biết ta."), "greet"),
                new Line(Loc.T("Giữa đảo là Tháp Máy Bi. Bi của khách vẫn thả ở đó như thường, ta không đụng tới đâu."), null, SpotKey("tower")),
                new Line(Loc.T("Bến câu với quán trọ mở trước. Ngồi câu vài con đi, cá hiếm bán được khá bi đấy."), null, SpotKey("fishing")),
                new Line(Loc.T("Trường đua, chợ đen, hầm đấu mở dần theo cấp. Thỉnh thoảng có đoàn lữ khách ghé dựng lều chơi vài ngày. Đi dạo đi, khách!"), "react_win_small"),
            }, done);

        // ---------- lần đầu vào mỗi trò ----------

        public static bool Fishing() => First(Casino.Fishing, new[]
        {
            new Line(Loc.T("Bến câu đây! Chạm CÂU là quăng. Phao rơi chỗ nào thì câu chỗ đó: gần bờ, xa bờ hay rạn đá."), "greet"),
            new Line(Loc.T("Cá cắn thì kim chạy qua lại trên thanh. Chạm đúng lúc kim nằm trong vùng vàng; cá càng hiếm càng phải trúng nhiều nhịp.")),
            new Line(Loc.T("Cá vào giỏ thì bán luôn ở đây. Mỗi ngày ta cho mười mồi, hết thì mua thêm.")),
        });

        public static bool Race() => First(Casino.Race, new[]
        {
            new Line(Loc.T("Trường đua của ta đây! Chạm một con trên đường đua để chọn, chọn chip rồi bấm Đặt cược."), "greet"),
            new Line(Loc.T("Về nhất ăn gấp ba, nhì gấp đôi, ba thì hoà vốn. Cược càng to càng khó thắng, ta nói trước rồi nhé. Mỗi ngày năm lượt.")),
        });

        public static bool Market() => First(Casino.Market, new[]
        {
            new Line(Loc.T("Chợ đen đây, hàng lạ đổi bằng bi. Hàng bày theo buổi, tối có thêm vài món hiếm."), "greet"),
            new Line(Loc.T("Cá trong giỏ bán được ở đây. Thẻ thừa thì đổi lấy đá tiềm năng, mỗi ngày có hạn thôi.")),
        });

        public static bool Underground() => First(Casino.Underground, new[]
        {
            new Line(Loc.T("Xuống Hầm đấu rồi đấy! Mỗi ngày mười đội ngầm, đội sau mạnh hơn đội trước. Vuốt để xem, chạm biển gỗ để xem chi tiết."), "greet"),
            new Line(Loc.T("Đóng lệ phí rồi đánh. Thắng thì ta trả lại lệ phí kèm quà, thua thì lệ phí ta giữ. Mỗi ngày đánh được năm trận.")),
        });

        // Quán trọ là hộp thoại: câu gắn chỗ khoanh trong hộp (key), lớp phủ hiện trên hộp
        public static bool Inn(string key) => First(Casino.Inn, new[]
        {
            new Line(Loc.T("Bảng việc của quán trọ: mỗi ngày ba việc nhỏ quanh đảo. Xong việc nào thì về đây lĩnh thưởng việc đó, xong cả ba còn có quà thêm."), "greet", key),
        });

        // ba lều: free = còn ván đầu miễn phí
        public static bool Table(string game, bool free)
        {
            var lines = new List<Line>();
            string freeLine;
            switch (game)
            {
                case Casino.Blackjack:
                    lines.Add(new Line(Loc.T("Đêm Bài! Rút bài cho gần 21 mà đừng quá. Quá là ta ăn hết đấy, khè khè."), "greet"));
                    freeLine = Loc.T("Ván đầu ta khao, thua không mất gì.");
                    break;
                case Casino.Roulette:
                    lines.Add(new Line(Loc.T("Vòng Xoay! Đặt chip vào hệ, vào số, hay liều một ô. Bi dừng đâu, ta trả đó."), "greet"));
                    freeLine = Loc.T("Vòng đầu ta khao, trượt không mất gì.");
                    break;
                case Casino.Slot:
                    lines.Add(new Line(Loc.T("Hội Máy Quả! Ba hình giống nhau trên một đường là trúng. Đừng hỏi ta máy có bịp không, nó thật thà hơn ta."), "greet"));
                    freeLine = Loc.T("Lượt đầu ta khao, trượt không mất gì.");
                    break;
                default:
                    return false;
            }
            if (free) lines.Add(new Line(freeLine));
            lines.Add(new Line(Loc.T("Luật đầy đủ ở nút Cách chơi, trong bảng gập góc dưới bên trái.")));
            return First(game, lines);
        }

        // ---------- câu bình phẩm ----------

        static readonly System.Random rnd = new System.Random();

        static string Pick(params string[] xs) => xs[rnd.Next(xs.Length)];

        // tiếng lầm bầm vô nghĩa của Lão Mực khi bong bóng hiện (3 bản, gen Magnific 2026-11-27, ArtGen/Sfx/casino; không lồng tiếng thật)
        public static void Mumble(float volume = 0.75f) => App.Audio?.PlayGap("mucTalk" + rnd.Next(1, 4), 0.6f, volume);

        public static void Caught(bool king, bool first, bool record, Rarity rar)
        {
            if (king) Guide.Quip(Loc.T("Cá Vua! Ta ngồi bến này ba chục năm chưa thấy con nào to thế."), "react_win_big", null, 3.2f);
            else if (first && rar >= Rarity.Rare) Guide.Quip(Loc.T("Loài mới! Ghi vào Sổ Cá đi, khách."), "react_win_small");
            else if (record && rar >= Rarity.Epic) Guide.Quip(Loc.T("Kỷ lục mới! Con này đem khoe được đấy."), "react_win_small");
        }

        public static void Escaped(bool king, Rarity rar)
        {
            if (!king && rar < Rarity.Epic) return;
            Guide.Quip(king ? Loc.T("Cá Vua chạy mất rồi... Tuần này nó còn quanh đây, thử lại đi.")
                : Pick(Loc.T("Hừ, sổng mất rồi. Trượt nhịp nhiều quá là cá chạy đấy."), Loc.T("Tiếc ghê! Con đó bán được khối bi.")), "react_lose");
        }

        public static void Bought()
        {
            if (rnd.NextDouble() > 0.4) return;
            Guide.Quip(Pick(Loc.T("Hàng tốt đấy, khách sành ghê."), Loc.T("Mua rồi thì không trả lại đâu nhé, khè khè.")), "react_win_small");
        }

        public static void InnClaimed(string key, bool all)
        {
            if (all) Guide.Quip(Loc.T("Xong cả ngày rồi à? Chăm thế, mai ghé nữa nhé."), "react_win_big", key);
            else if (rnd.NextDouble() < 0.5) Guide.Quip(Loc.T("Việc gọn ghẽ. Thưởng của khách đây."), "react_win_small", key);
        }
    }
}
