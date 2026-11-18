// Thử sáng tối (DayCycle, lớp DayNight trên các đảo và sảnh) trong tab Options của SRDebugger (chạm 3 lần góc trái dưới màn hình để
// mở bảng). Người dùng dặn 2026-11-18: "thêm sáng tối trong debugger để test". Ép giờ chỉ trong phiên chạy, không lưu; "Theo giờ máy"
// bỏ ép.
using System.ComponentModel;
using PokiClash;

public partial class SROptions
{
    const string DayCategory = "Sáng tối";

    // bấm lần lượt: sáng 10h → chiều 18h20 → tối 22h → theo giờ máy
    [Category(DayCategory), DisplayName("Đổi sáng / chiều / tối"), Sort(0)]
    public void PokiDayCycleNext()
    {
        var h = DayCycle.Override;
        PokiSetHour(h == null ? 10f : h < 12f ? 18.33f : h < 20f ? 22f : (float?)null);
    }

    [Category(DayCategory), DisplayName("Sáng (10h)"), Sort(1)]
    public void PokiDayMorning() => PokiSetHour(10f);

    [Category(DayCategory), DisplayName("Chiều (18h20)"), Sort(2)]
    public void PokiDayDusk() => PokiSetHour(18.33f);

    [Category(DayCategory), DisplayName("Tối (22h)"), Sort(3)]
    public void PokiDayNight() => PokiSetHour(22f);

    [Category(DayCategory), DisplayName("Theo giờ máy"), Sort(4)]
    public void PokiDayReal() => PokiSetHour(null);

    // giờ đang ép (-1 = theo giờ máy); kéo để xem chuyển dần
    [Category(DayCategory), DisplayName("Giờ (-1 = theo máy)"), NumberRange(-1, 24), Increment(0.5), Sort(5)]
    public float PokiHour
    {
        get => DayCycle.Override ?? -1f;
        set => PokiSetHour(value < 0 ? (float?)null : value);
    }

    void PokiSetHour(float? h)
    {
        DayCycle.Override = h;
        UnityEngine.Debug.Log("[SRDebugger] Giờ trong game: " + (h.HasValue ? h.Value.ToString("0.##") + "h" : "theo giờ máy"));
        OnPropertyChanged(nameof(PokiHour));
    }
}
