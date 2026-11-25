// Bảo mật số (Lớp 3) ở bước build: strip cfg thô khỏi BalanceConfig.asset của bản ship khi đã có enc giải mã được, để AssetStudio
// không đọc được số. An toàn: enc là nguồn thật lúc chạy (BalanceConfigAsset.Resolve), nên dù strip/restore có trục trặc thì game vẫn
// chạy đúng bằng enc; cfg thô chỉ là tiện ích trong Editor, nhập lại dữ liệu là có lại. Verify enc giải được TRƯỚC khi strip —
// không bao giờ ship config hỏng. Trả về token để trả lại cfg sau build (PokiBuild gọi trong finally).
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.Security;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class SecureBuild
    {
        const string BalancePath = "Assets/02 Data/BalanceConfig.asset";

        public sealed class Token
        {
            public BalanceConfigAsset asset;
            public BalanceConfig saved;
        }

        public static Token StripBalance()
        {
            var bal = AssetDatabase.LoadAssetAtPath<BalanceConfigAsset>(BalancePath);
            if (!bal)
            {
                Debug.LogWarning($"[Bảo mật] Không thấy {BalancePath}, bỏ qua strip số.");
                return null;
            }
            if (bal.enc == null || bal.enc.Length == 0)
            {
                Debug.LogWarning("[Bảo mật] BalanceConfig chưa có enc (chạy 'PokiClash/Nhập dữ liệu' trước). Bản build vẫn mang số thô — số CHƯA được giấu.");
                return null;
            }
            if (PokiCrypt.DecryptString(bal.enc, "balance") == null)
            {
                Debug.LogError("[Bảo mật] enc của BalanceConfig giải mã lỗi — KHÔNG strip cfg (giữ số thô để game chạy đúng). Hãy 'Nhập dữ liệu' lại.");
                return null;
            }
            var tok = new Token { asset = bal, saved = bal.cfg };
            bal.cfg = new BalanceConfig(); // bản ship: cfg rỗng, số thật nằm trong enc
            EditorUtility.SetDirty(bal);
            AssetDatabase.SaveAssets();
            Debug.Log("[Bảo mật] Đã strip số thô khỏi BalanceConfig (bản ship chỉ còn enc mã hoá).");
            return tok;
        }

        public static void Restore(Token tok)
        {
            if (tok?.asset == null) return;
            tok.asset.cfg = tok.saved;
            EditorUtility.SetDirty(tok.asset);
            AssetDatabase.SaveAssets();
        }
    }
}
