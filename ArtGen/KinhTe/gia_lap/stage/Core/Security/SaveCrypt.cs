// Bọc/mở bản lưu ở ranh giới file (SaveService gọi): mã hoá AES + ký HMAC (PokiCrypt nhãn "save") rồi Base64 để vẫn là chuỗi văn
// bản ghi ra file. Sửa tay một byte là hỏng HMAC -> Unprotect trả null -> SaveService coi như hỏng (giữ .bak, báo người chơi).
// SaveCodec vẫn sinh/đọc JSON thô (test không đụng tới, IV ngẫu nhiên không phá assert "ghi lại y nguyên").
// Tương thích ngược: bản lưu cũ (JSON thô, mở đầu '{') chỉ đọc thẳng khi chỗ gọi cho phép (Editor, development build); lần Save
// sau tự chuyển sang bản mã hoá. Bản phát hành coi JSON thô là bản lưu hỏng.
// Ràng buộc theo máy (Context) để trống mặc định: khoá app đã đủ chặn sửa; buộc theo id máy dễ khoá nhầm người chơi khi cài lại/đổi
// máy nên chỉ bật khi có hệ tài khoản (App.cs tiêm vào lúc khởi động nếu cần, giữ Core thuần không đụng UnityEngine).
using System;
using System.Text;
using PokiClash.Security;

namespace PokiClash.Core
{
    public static class SaveCrypt
    {
        const string Tag = "PKS1:"; // dấu nhận biết bản lưu đã mã hoá

        // id máy (hoặc tài khoản) để buộc bản lưu vào máy; null = không buộc. App tiêm nếu muốn.
        public static byte[] Context;

        // Có đang là bản lưu mã hoá không.
        public static bool IsProtected(string s) => s != null && s.StartsWith(Tag, StringComparison.Ordinal);

        // JSON thô -> chuỗi mã hoá để ghi file.
        public static string Protect(string json)
        {
            if (json == null) return null;
            byte[] blob = PokiCrypt.Encrypt(Encoding.UTF8.GetBytes(json), "save", Context);
            return Tag + Convert.ToBase64String(blob);
        }

        // Nội dung file -> JSON thô. Bản mã hoá hỏng/bị sửa/sai máy trả null. Bản chưa mã hoá (JSON thô) chỉ nhận khi allowPlain:
        // nhận mãi thì ai cũng ghi đè file bằng JSON thô sửa coin/gem mà khỏi phá mã hoá (cửa hậu, vá 2026-11-25). SaveService cho phép
        // ở Editor + development build (test, tour, máy thử), bản phát hành thì không (chưa có người chơi thật giữ bản lưu thô).
        public static string Unprotect(string stored, bool allowPlain = true)
        {
            if (stored == null) return null;
            if (!IsProtected(stored)) return allowPlain ? stored : null; // bản lưu thô (cũ, hoặc bị ghi đè tay)
            try
            {
                byte[] blob = Convert.FromBase64String(stored.Substring(Tag.Length));
                byte[] plain = PokiCrypt.TryDecrypt(blob, "save", Context);
                return plain == null ? null : Encoding.UTF8.GetString(plain);
            }
            catch
            {
                return null; // Base64 hỏng = bị sửa
            }
        }
    }
}
