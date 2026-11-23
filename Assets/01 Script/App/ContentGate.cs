// Chặn chuyển màn tới khi đủ gói tải sau (GD_Claude/27_TaiNoiDungSau.md): SceneRouter hỏi PacksFor trước khi rời màn cũ, chờ các gói
// đó nạp xong; gói lỗi (mất mạng, chưa tải) thì ở lại màn cũ và báo. Vào đảo: gói của đảo. Vào trận: gói đảo của ải (địch cùng hệ đảo)
// và gói của tướng trong đội (trừ dòng tướng khởi đầu, nằm trong bản cài).
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.Game;

namespace PokiClash
{
    public static class ContentGate
    {
        public static List<string> PacksFor(string scene, object args)
        {
            var r = new List<string>();
            var d = App.Data;
            if (d == null) return r;
            if (scene == SceneIds.Zone && args is Elem z) Add(r, Keys.Of(z));
            else if (scene == SceneIds.Battle && args is BattleArgs b)
            {
                var st = d.Stage(b.stageId);
                if (st != null) Add(r, Keys.Of(st.zone));
                if (b.cave != null) Add(r, Keys.Of(b.cave.zone));
                if (b.badge != null) Add(r, Keys.Of(b.badge.zone));
                var team = b.team ?? App.Save?.Data?.team;
                if (team != null)
                    foreach (var id in team)
                        AddHero(r, d, id);
            }
            return r;
        }

        // gói chứa hình tướng id (null: bản cài)
        public static string HeroPack(GameData d, string id)
        {
            if (d == null || string.IsNullOrEmpty(id) || d.Starters.Contains(id)) return null;
            var h = d.Hero(id);
            return h != null ? Keys.Of(h.elem) : null;
        }

        static void AddHero(List<string> r, GameData d, string id) => Add(r, HeroPack(d, id));

        static void Add(List<string> r, string e)
        {
            if (ContentPacks.IsPack(e) && !r.Contains(e)) r.Add(e);
        }

        // tên đảo của gói (để báo)
        public static string Name(string elem) =>
            Keys.TryElem(elem, out var e) ? (App.Data?.Zone(e)?.name ?? Elements.Name(e)) : elem;

        public static string WaitText(List<string> packs) => Loc.F("Đang tải {0} lần đầu…", Name(packs[0]));

        public static string FailText(string elem) => Loc.F("Cần mạng để tải {0} lần đầu. Kết nối mạng rồi thử lại.", Name(elem));
    }
}
