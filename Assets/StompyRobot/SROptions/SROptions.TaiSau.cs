// Gói tải sau (GD_Claude/27_TaiNoiDungSau.md) trong tab Options của SRDebugger, mục "Tải sau": giả lập gói chưa tải (chỉ Editor: chờ
// vài giây có tiến độ như đang tải lần đầu) và giả lập mất mạng (gói chưa có thì báo cần mạng), xem trạng thái 5 gói. Giả lập chỉ ảnh
// hưởng lần nạp sau: gói đã nạp thì vẫn dùng.
using System.ComponentModel;
using System.Linq;
using PokiClash.Game;

public partial class SROptions
{
    const string PackCategory = "Tải sau";

    [Category(PackCategory), DisplayName("Giả lập: gói chưa tải (Editor)"), Sort(0)]
    public bool PokiPackSimMissing
    {
        get => ContentPacks.SimulateMissing;
        set => ContentPacks.SimulateMissing = value;
    }

    [Category(PackCategory), DisplayName("Giả lập: mất mạng"), Sort(1)]
    public bool PokiPackSimOffline
    {
        get => ContentPacks.SimulateOffline;
        set => ContentPacks.SimulateOffline = value;
    }

    [Category(PackCategory), DisplayName("Trạng thái 5 gói"), Sort(2)]
    public string PokiPackState => string.Join(", ", ContentPacks.Elems.Select(e => $"{e}: {ContentPacks.StateOf(e)}"));
}
