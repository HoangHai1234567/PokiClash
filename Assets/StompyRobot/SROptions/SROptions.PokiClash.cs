// Cheat của PokiClash trong tab Options của SRDebugger (chạm 3 lần góc trái dưới màn hình để mở bảng).
// Bật ở mọi bản build như ClashMaster (người dùng chốt 2026-11-05). Mở hết ải, mở hết tướng làm giống nút cùng tên trong Sổ tay dev
// (01 Script/App/Dev/NotebookDev.cs).
using System;
using System.ComponentModel;
using PokiClash;
using PokiClash.Core;

public partial class SROptions
{
    const string PokiCategory = "PokiClash";

    // mọi ải của 5 đảo coi như đã qua (ải mở khi ải trước đã qua, Progress.StageOpen)
    [Category(PokiCategory), DisplayName("Mở hết ải"), Sort(0)]
    public void PokiUnlockAllStages() => PokiCheat("Mở hết ải", (s, d) =>
    {
        foreach (var e in Elements.All) s.zones[(int)e] = Islands.Size(e);
    });

    [Category(PokiCategory), DisplayName("Mở hết tướng"), Sort(1)]
    public void PokiUnlockAllHeroes() => PokiCheat("Mở hết tướng", (s, d) =>
    {
        foreach (var h in d.Heroes) s.Hero(h.id).owned = true;
    });

    [Category(PokiCategory), DisplayName("+100 bi"), Sort(2)]
    public void PokiAddBalls100() => PokiCheat("+100 bi", (s, d) => s.balls += 100);

    [Category(PokiCategory), DisplayName("+1000 bi"), Sort(3)]
    public void PokiAddBalls1000() => PokiCheat("+1000 bi", (s, d) => s.balls += 1000);

    // cấp người chơi (cũng là cấp tướng mình trong trận, mở ô đội, trang trại, cây bi, hang): đổi là lưu ngay, EXP về 0.
    // Hạ cấp không cần sửa đội: chỗ nào dùng đội cũng chỉ lấy đủ số ô đã mở (Progress.TeamSlots).
    // Khung ô số 1..200 theo maxLevel của balance.json; số thật vẫn kẹp theo App.Data.Cfg.maxLevel.
    [Category(PokiCategory), DisplayName("Cấp"), NumberRange(1, 200), Increment(1), Sort(4)]
    public int PokiLevel
    {
        get => App.Save?.Data?.level ?? 1;
        set => PokiSetLevel(value);
    }

    [Category(PokiCategory), DisplayName("Cấp tối đa"), Sort(5)]
    public void PokiMaxLevel() => PokiSetLevel(App.Data != null ? App.Data.Cfg.maxLevel : 200);

    void PokiSetLevel(int lv)
    {
        if (App.Data != null) lv = Math.Min(lv, App.Data.Cfg.maxLevel);
        lv = Math.Max(1, lv);
        if (App.Save?.Data != null && App.Save.Data.level == lv) return;
        PokiCheat("Đặt cấp " + lv, (s, d) =>
        {
            s.level = lv;
            s.exp = 0;
        });
        OnPropertyChanged(nameof(PokiLevel));
    }

    // sửa bản lưu rồi lưu: SaveService.Changed làm mới thanh trên và scene đang mở (App.OnSaveChanged)
    static void PokiCheat(string name, Action<SaveData, GameData> fn)
    {
        if (App.Save == null || App.Save.Data == null)
        {
            UnityEngine.Debug.LogWarning("[SRDebugger] " + name + ": chưa nạp bản lưu");
            return;
        }
        fn(App.Save.Data, App.Data);
        App.Save.Save();
        if (App.Audio != null) App.Audio.Play("coin");
        UnityEngine.Debug.Log("[SRDebugger] " + name);
    }
}
