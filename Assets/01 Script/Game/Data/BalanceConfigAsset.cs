// Cấu hình cân bằng (CFG và hằng số tiến trình của bản web), dựng từ balance.json.
// Bảo mật số (Lớp 3): bản phát hành mang blob mã hoá (enc = balance.json đã AES, nhãn "balance"); lúc chạy giải ra dùng, nên
// AssetStudio không đọc được số. cfg thô chỉ để trong Editor cho tiện xem/kiểm; bước build strip cfg khỏi bản ship (PokiBuild,
// chỉ strip khi enc giải ra khớp cfg — không bao giờ ship config hỏng).
using PokiClash.Core;
using PokiClash.Security;
using UnityEngine;

namespace PokiClash.Game
{
    [CreateAssetMenu(menuName = "PokiClash/BalanceConfig", fileName = "BalanceConfig")]
    public sealed class BalanceConfigAsset : ScriptableObject
    {
        public BalanceConfig cfg = new BalanceConfig(); // bản thử/Editor; bản ship để rỗng, số nằm trong enc
        public byte[] enc;                               // balance.json đã mã hoá (nhãn "balance"); có thì lúc chạy dùng cái này

        [System.NonSerialized] BalanceConfig resolved;

        // Số cân bằng thật dùng lúc chạy: ưu tiên bản mã hoá (enc); chưa có enc (bản thử chưa re-import) thì dùng cfg như cũ.
        public BalanceConfig Resolve()
        {
            if (enc == null || enc.Length == 0) return cfg;
            if (resolved != null) return resolved;
            string json = PokiCrypt.DecryptString(enc, "balance");
            if (json == null)
            {
                Debug.LogError("[Bảo mật] Giải mã balance thất bại — dùng cfg dự phòng.");
                return cfg;
            }
            resolved = BalanceConfig.FromJson(J.Obj(MiniJson.Parse(json)));
            return resolved;
        }
    }
}
