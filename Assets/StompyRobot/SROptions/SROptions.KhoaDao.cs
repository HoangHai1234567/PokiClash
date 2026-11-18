// Khoá / mở lại đảo trong tab Options của SRDebugger, mục "Khoá đảo" (chạm 3 lần góc trái dưới màn hình để mở bảng). Người dùng dặn
// 2026-11-18: "thêm option lock lại các đảo trong srdebugger". Đảo không có khoá riêng: tiến độ mỗi đảo là số ải đã qua
// (SaveData.zones), ải mở khi ải trước đã qua (Progress.StageOpen). "Khoá lại hết đảo" đưa cả 5 đảo về 0 ải đã qua (chỉ ải 1 mở,
// ngược với "Mở hết ải"); ô số của từng đảo đặt số ải đã qua (0 = khoá lại đảo đó). Hạ tiến độ thì rương mốc chưa tới coi như chưa
// nhận, xoá số lần qua của các ải bị khoá, đội AFK đang treo ở ải bị khoá về tự chọn. Đảo vùng đất: số vùng boss đã diễn cảnh mở
// (LandShown) đặt lại để vào đảo diễn lại (khoá hết: diễn mở vùng đầu như lần đầu vào đảo; đặt n ải: diễn mở vùng mới nhất). Lưu ngay,
// màn đang mở tự làm mới.
using System;
using System.ComponentModel;
using System.Linq;
using PokiClash;
using PokiClash.Core;

public partial class SROptions
{
    const string IslandCategory = "Khoá đảo";

    [Category(IslandCategory), DisplayName("Khoá lại hết đảo"), Sort(0)]
    public void PokiLockAllIslands()
    {
        PokiCheat("Khoá lại hết đảo", (s, d) =>
        {
            foreach (var e in Elements.All) PokiSetIsland(s, d, e, 0);
        });
        PokiIslandsChanged();
    }

    [Category(IslandCategory), DisplayName("Đảo Thủy: ải đã qua"), NumberRange(0, 70), Increment(1), Sort(1)]
    public int PokiIslandThuy { get => PokiIsland(Elem.Thuy); set => PokiSetIsland(Elem.Thuy, value); }

    [Category(IslandCategory), DisplayName("Đảo Hỏa: ải đã qua"), NumberRange(0, 70), Increment(1), Sort(2)]
    public int PokiIslandHoa { get => PokiIsland(Elem.Hoa); set => PokiSetIsland(Elem.Hoa, value); }

    [Category(IslandCategory), DisplayName("Đảo Mộc: ải đã qua"), NumberRange(0, 70), Increment(1), Sort(3)]
    public int PokiIslandMoc { get => PokiIsland(Elem.Moc); set => PokiSetIsland(Elem.Moc, value); }

    [Category(IslandCategory), DisplayName("Đảo Kim: ải đã qua"), NumberRange(0, 70), Increment(1), Sort(4)]
    public int PokiIslandKim { get => PokiIsland(Elem.Kim); set => PokiSetIsland(Elem.Kim, value); }

    [Category(IslandCategory), DisplayName("Đảo Thổ: ải đã qua"), NumberRange(0, 70), Increment(1), Sort(5)]
    public int PokiIslandTho { get => PokiIsland(Elem.Tho); set => PokiSetIsland(Elem.Tho, value); }

    static int PokiIsland(Elem e) => App.Save?.Data != null ? App.Save.Data.zones[(int)e] : 0;

    void PokiSetIsland(Elem e, int n)
    {
        n = Math.Max(0, Math.Min(n, Islands.Size(e)));
        if (App.Save?.Data == null || App.Save.Data.zones[(int)e] == n) return;
        PokiCheat($"Đảo {Elements.Name(e)}: {n} ải đã qua", (s, d) => PokiSetIsland(s, d, e, n));
        PokiIslandsChanged();
    }

    // đặt tiến độ một đảo; hạ xuống thì dọn những thứ gắn với ải bị khoá
    static void PokiSetIsland(SaveData s, GameData d, Elem e, int n)
    {
        s.zones[(int)e] = n;
        s.zoneChests[(int)e] = Math.Min(s.zoneChests[(int)e], Islands.Chests(e).Count(at => at <= n));
        if (d == null) return;
        var land = d.Zone(e)?.land;
        if (land != null && land.Has && land.secs.Count > 0) LandShown.Set(s, e, n == 0 ? 0 : Math.Max(0, land.OpenSections(n) - 1));
        foreach (var st in d.ZoneStages(e))
        {
            if (st.idx <= n) continue;
            s.clears.Remove(st.id);
            if (s.afk.stage == st.id) s.afk.stage = 0;
        }
    }

    void PokiIslandsChanged()
    {
        OnPropertyChanged(nameof(PokiIslandThuy));
        OnPropertyChanged(nameof(PokiIslandHoa));
        OnPropertyChanged(nameof(PokiIslandMoc));
        OnPropertyChanged(nameof(PokiIslandKim));
        OnPropertyChanged(nameof(PokiIslandTho));
    }
}
