// Thổ Tinh (suất giap_nham, ải 70 đảo Thổ, final boss; hiệu ứng HatThoTinh.cs): phần sân làm đối thủ đổi cỡ / giật theo đòn của nó.
// Phần riêng của StageView (partial) để file chính chỉ thêm một dòng trong Place (sau dòng bị nhổ của Bùn Ngoạm, StageViewNuot.cs).
// - Chiêu cuối "Hằng Tinh Diệt": từ sự kiện ep (2,15 s) tới hết ép (2,83 s) đối thủ CO còn ~0,4 quanh giữa thân để nằm gọn trong vỏ đá, run theo
//   vỏ, bật về 1 đúng lúc nổ (3,48 s) (HatLua.TinhCoDoiThu, cùng hàm với vỏ đá của lớp hạt). Ảnh aola xoay quanh chân nên dời xuống cho giữa
//   thân đứng yên; bóng dưới chân co theo.
// - Đòn thường "Thiên Chuỳ": lúc hai nắm đấm nện, đối thủ BẸP theo chân rồi nảy (HatLua.TinhBep).
// - Chiêu mana "Nguyệt Nhận": mỗi lưỡi trăng (dạng 1: mảnh vỏ) cắm vào, đối thủ giật nhẹ ra xa kẻ đánh và nháy (mảnh cuối mạnh hơn; dạng 1
//   nhẹ hơn) (HatLua.TinhLuoiCam).
// Hai dạng (mã dạng 1 thêm đuôi "1", HatLua.TinhDang) dùng chung phần này.
// Trạng thái suy thẳng từ giờ clip của kẻ đánh, không lưu cờ (clip bị cắt thì đối thủ về cỡ cũ ngay khung sau); chỉ nhớ phía nào đang bị đổi
// cỡ để trả lại cỡ ảnh, cỡ bóng khi xong. Đối thủ không phải ảnh aola / rig (ô trống) thì bỏ qua.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class StageView
    {
        readonly bool[] tinhDoi = new bool[2]; // phía đang bị Thổ Tinh đổi cỡ ảnh

        // v đang bị Thổ Tinh đánh: cỡ ảnh (sx, sy quanh chân), cỡ bóng, dời ảnh (đơn vị sân, y xuống); false: không bị gì
        bool TinhCo(Actor v, out float sx, out float sy, out float bong, out Vector2 off, out float hien)
        {
            sx = sy = bong = hien = 1;
            off = Vector2.zero;
            if (v == null || v.aola == null || !v.body || v.exit > 0 || Entering(v)) return false;
            var k = actors[1 - v.side];
            if (k == null || k.aola == null || k.loop || k.dead > 0) return false;
            if (k.clip == Skill && HatLua.TinhDang(FireUlt(k.hero, k.form), "n_tinh_hang") > 0)
            {
                float c = HatLua.TinhCoDoiThu(k.t);
                hien = HatLua.TinhHienDoiThu(k.t); // nổ: ẩn trong cầu lửa, rồi hiện mờ dần sau khói đen
                if (c > 0.999f && hien > 0.999f) return false;
                if (c < 0.999f) c = Mathf.LerpUnclamped(1, c, 1.15f); // co thêm một nấc: đối thủ bè ngang (cua) không lòi mai hai bên vỏ đá (~0,32)
                sx = sy = c;
                bong = Mathf.Max(0.3f, c) * hien;
                // ảnh co quanh CHÂN (pivot AolaSticker.FootV) nên giữa thân tụt xuống 0,45·H·(1−c): dời LÊN chừng ấy (y sân hướng xuống,
                // P(x, y) = (x, −y)) cho giữa thân đứng yên trong vỏ đá (tour 2026-11-18: bản dời xuống làm đối thủ lòi ra dưới quả cầu)
                off = new Vector2(0, -0.45f * v.H * (1 - c));
                return true;
            }
            if (k.clip == Attack && HatLua.TinhDang(FireAtk(k.hero, k.form), "n_tinh_nen") > 0)
                return HatLua.TinhBep(k.t - k.aola.HitTime(Attack), out sx, out sy);
            int dm = k.clip == Cast ? HatLua.TinhDang(FireMana(k.hero, k.form), "n_tinh_gai") : 0;
            if (dm > 0)
            {
                if (!HatLua.TinhLuoiCam(dm == 1, k.t, k.aola.HitTime(Cast), out float since, out bool cuoi)) return false;
                float muc = (cuoi ? 1.6f : 0.8f) * (dm == 1 ? 0.8f : 1f);
                float f = since < 0.02f ? since / 0.02f : Mathf.Max(0, 1 - (since - 0.02f) / 0.08f);
                var away = (Pos[v.side] - Pos[k.side]).normalized;
                off = away * (0.028f * muc * f * v.H) + new Vector2(0, -0.012f * muc * f * v.H);
                if (since < 0.05f) v.flash = Mathf.Max(v.flash, 0.08f * muc);
                return true;
            }
            return false;
        }

        // gọi trong Place sau phần bật lùi / bị nhổ: đặt cỡ ảnh, cỡ bóng, cộng dời ảnh; hết bị thì trả cỡ cũ
        void TinhDat(Actor a, ref float ox, ref float oy, ref float alpha)
        {
            if (!TinhCo(a, out float sx, out float sy, out float bong, out var off, out float hien))
            {
                if (!tinhDoi[a.side]) return;
                tinhDoi[a.side] = false;
                if (a.body) a.body.localScale = Vector3.one;
                if (a.shadow) a.shadow.localScale = Vector3.one;
                return;
            }
            tinhDoi[a.side] = true;
            a.body.localScale = new Vector3(sx, sy, 1);
            if (a.shadow) a.shadow.localScale = new Vector3(bong, bong, 1);
            ox += off.x;
            oy += off.y;
            alpha *= hien;
        }
    }
}
