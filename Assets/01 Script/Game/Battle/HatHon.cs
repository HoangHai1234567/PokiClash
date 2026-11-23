// Bộ VONG KỴ (2026-11-16, kỵ sĩ cổ đại bị nguyền, giáp sắt đen rỉ giữ hồn bằng lửa linh hồn xanh, suất tam_kiem ải 50 đảo Kim; rig
// ArtGen/Spine/ky_nguyen_rig.py (rig gốc monster_3642): dạng 2 ky_nguyen_2; ghi chú ArtGen/Spine/inbox/ky_nguyen_ghichu.md).
// Người dùng: đánh thường "lao tới dùng kiếm chém"; chiêu mana "giơ kiếm lên trời, gọi những linh hồn đồng đội từ thời xưa dạng linh hồn xanh
// lao tới đánh kẻ thù"; chiêu cuối "tay kia vuốt lên, thanh kiếm cùn hút những khí xanh xung quanh, được khôi phục bằng vật chất linh hồn xanh
// lá thành kiếm hoàn chỉnh, tỏa aura linh hồn xanh; chém một phát thật mạnh xuống đối thủ, epic, impact". Đi đường "n_" (StageView.PreFx /
// AtkFx → PlayNuoc), phát lúc clip BẮT ĐẦU; mốc là giây clip của rig, co theo `lead` (giờ trúng của clip):
// - n_hon_chem (đòn thường): vệt chém lửa hồn quét chéo qua đối thủ ngay trước khung trúng; trúng: chớp hồn, lưỡi lửa hồn toé, tia, mảnh giáp.
// - n_hon_goi1 / n_hon_goi (chiêu mana): `goi` mũi kiếm giơ trên trời bùng lửa hồn, lửa liếm quanh mũi kiếm; HỒN ĐỒNG ĐỘI (hình mũ vương miện
//   xanh hồn: Resources/ky_nguyen_2/ky_nguyen_2_tt_hon.png) bay ra từ mũi kiếm, xếp quạt trên đầu, lần lượt lao theo cung xuống đối thủ để lại
//   đuôi lửa hồn; mỗi hồn trúng: chớp, lưỡi lửa toé; hồn cuối nổ to (3 / 5 hồn).
// - n_hon_kiem1 / n_hon_kiem (chiêu cuối): `hut` → `hoi_phuc` khí hồn xanh từ quanh người bị hút vào MÉP ĐANG HIỆN của phần vá (đúng mép mặt nạ
//   cắt của rig, bảng số đo), tia lấp lánh ở mép; `hat` lửa hồn chạy dọc lưỡi tới mũi; `hoi_phuc` lưỡi bùng sáng dọc kiếm; `gong` aura hồn bùng
//   quanh người (vòng sàn, lưỡi lửa bốc); nhát bổ: vệt lửa hồn theo đúng đường mũi kiếm; trúng: chớp lớn, hai vòng sóng, cột lưỡi lửa hồn toé
//   lên, khói hồn, mảnh giáp, đá văng, rung mạnh; `tat` phần vá tan thành khí hồn bay lên.
// FILE SINH TỰ ĐỘNG từ ArtGen/Spine/ky_nguyen_hat_cs.py (bảng số đo của rig): đổi clip hay tỉ lệ rig thì chạy lại script, đừng sửa tay.
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        const float KnDt = 1f / 30f;
        const float KnALead = 0.467f;
        const float KnCLead = 1.050f, KnCGoi = 0.700f;
        const float KnSLead = 2.670f, KnSHut = 0.500f, KnSHat = 1.550f, KnSHoi = 1.720f, KnSGong = 2.300f, KnSChem = 2.550f, KnSTat = 2.910f;
        static readonly Color KnXanh = C(132, 205, 57), KnNhat = C(214, 250, 170), KnDam = C(56, 132, 54);
        static readonly Color[] KnChopC = { Ink, C(56, 132, 54), C(132, 205, 57), C(196, 244, 140), C(246, 255, 226) };

        // dạng 1: chiều cao khai 1178.6; skill 3.750 s, trúng 2.670; cast 1.850 s, trúng 1.050
        static readonly float[] Kn1CastTipX = { 0.023f, 0.038f, 0.075f, 0.141f, 0.314f, 0.584f, 0.445f, 0.232f, 0.056f, -0.011f, -0.016f, -0.019f, -0.020f, -0.021f, -0.022f, -0.023f, -0.024f, -0.025f, -0.025f, -0.025f, -0.026f, -0.031f, -0.022f, -0.022f, -0.031f, -0.025f, -0.019f, -0.028f, -0.028f, -0.018f, -0.023f, -0.028f, -0.019f, -0.018f, -0.027f, -0.021f, -0.015f, -0.024f, -0.024f, -0.015f, -0.020f, -0.021f, -0.020f, -0.021f, 0.016f, 0.114f, 0.208f, 0.242f, 0.247f, 0.273f, 0.292f, 0.278f, 0.229f, 0.158f, 0.087f, 0.040f, 0.026f };
        static readonly float[] Kn1CastTipY = { 0.111f, 0.117f, 0.139f, 0.223f, 0.341f, 0.732f, 1.109f, 1.240f, 1.270f, 1.258f, 1.258f, 1.258f, 1.257f, 1.257f, 1.257f, 1.258f, 1.261f, 1.265f, 1.269f, 1.273f, 1.276f, 1.278f, 1.281f, 1.284f, 1.287f, 1.290f, 1.293f, 1.296f, 1.298f, 1.301f, 1.304f, 1.306f, 1.309f, 1.311f, 1.314f, 1.316f, 1.318f, 1.320f, 1.322f, 1.324f, 1.325f, 1.327f, 1.328f, 1.331f, 1.326f, 1.269f, 1.121f, 0.929f, 0.776f, 0.659f, 0.536f, 0.407f, 0.289f, 0.200f, 0.144f, 0.119f, 0.112f };
        static readonly float[] Kn1SkillTipX = { 0.023f, 0.080f, 0.175f, 0.271f, 0.338f, 0.368f, 0.370f, 0.362f, 0.346f, 0.325f, 0.301f, 0.278f, 0.256f, 0.236f, 0.221f, 0.209f, 0.203f, 0.195f, 0.189f, 0.186f, 0.183f, 0.180f, 0.177f, 0.175f, 0.175f, 0.179f, 0.178f, 0.174f, 0.177f, 0.180f, 0.181f, 0.176f, 0.172f, 0.172f, 0.174f, 0.177f, 0.179f, 0.179f, 0.177f, 0.174f, 0.170f, 0.167f, 0.164f, 0.163f, 0.162f, 0.162f, 0.161f, 0.161f, 0.160f, 0.160f, 0.160f, 0.160f, 0.160f, 0.160f, 0.160f, 0.160f, 0.160f, 0.160f, 0.160f, 0.160f, 0.159f, 0.181f, 0.235f, 0.290f, 0.311f, 0.275f, 0.188f, 0.086f, 0.007f, -0.024f, -0.024f, -0.024f, -0.024f, -0.024f, -0.024f, -0.024f, -0.024f, -0.052f, -0.157f, 0.080f, 0.373f, 0.331f, 0.322f, 0.330f, 0.324f, 0.329f, 0.325f, 0.328f, 0.326f, 0.327f, 0.326f, 0.327f, 0.327f, 0.327f, 0.327f, -0.136f, -0.440f, -0.483f, -0.493f, -0.514f, -0.539f, -0.559f, -0.570f, -0.568f, -0.554f, -0.527f, -0.489f, -0.439f, -0.377f, -0.303f, -0.219f, -0.126f, -0.027f };
        static readonly float[] Kn1SkillTipY = { 0.111f, 0.143f, 0.205f, 0.300f, 0.411f, 0.509f, 0.575f, 0.637f, 0.691f, 0.738f, 0.777f, 0.806f, 0.827f, 0.841f, 0.850f, 0.855f, 0.856f, 0.858f, 0.856f, 0.850f, 0.846f, 0.847f, 0.847f, 0.846f, 0.846f, 0.837f, 0.835f, 0.839f, 0.831f, 0.823f, 0.819f, 0.822f, 0.824f, 0.821f, 0.814f, 0.805f, 0.798f, 0.794f, 0.791f, 0.790f, 0.789f, 0.788f, 0.785f, 0.780f, 0.773f, 0.764f, 0.755f, 0.746f, 0.740f, 0.734f, 0.730f, 0.727f, 0.727f, 0.727f, 0.727f, 0.727f, 0.727f, 0.727f, 0.727f, 0.727f, 0.713f, 0.725f, 0.768f, 0.853f, 0.973f, 1.101f, 1.199f, 1.249f, 1.261f, 1.260f, 1.260f, 1.260f, 1.260f, 1.260f, 1.260f, 1.260f, 1.260f, 1.252f, 0.901f, 0.891f, 0.164f, 0.108f, 0.108f, 0.108f, 0.108f, 0.108f, 0.108f, 0.108f, 0.108f, 0.108f, 0.108f, 0.108f, 0.108f, 0.108f, 0.108f, -0.035f, 0.178f, 0.316f, 0.353f, 0.356f, 0.338f, 0.305f, 0.263f, 0.220f, 0.185f, 0.156f, 0.129f, 0.104f, 0.084f, 0.070f, 0.066f, 0.074f, 0.095f };
        static readonly float[] Kn1SkillGocX = { 0.029f, 0.085f, 0.177f, 0.269f, 0.334f, 0.361f, 0.362f, 0.353f, 0.336f, 0.315f, 0.290f, 0.266f, 0.244f, 0.225f, 0.209f, 0.197f, 0.192f, 0.183f, 0.177f, 0.174f, 0.171f, 0.168f, 0.165f, 0.164f, 0.163f, 0.167f, 0.167f, 0.162f, 0.165f, 0.169f, 0.169f, 0.165f, 0.160f, 0.160f, 0.162f, 0.166f, 0.168f, 0.167f, 0.165f, 0.162f, 0.158f, 0.155f, 0.153f, 0.152f, 0.151f, 0.150f, 0.149f, 0.149f, 0.149f, 0.148f, 0.148f, 0.148f, 0.148f, 0.148f, 0.148f, 0.148f, 0.148f, 0.148f, 0.148f, 0.148f, 0.148f, 0.170f, 0.223f, 0.279f, 0.299f, 0.263f, 0.177f, 0.075f, -0.005f, -0.035f, -0.035f, -0.035f, -0.035f, -0.035f, -0.035f, -0.035f, -0.035f, -0.063f, -0.161f, 0.071f, 0.373f, 0.333f, 0.324f, 0.332f, 0.326f, 0.331f, 0.327f, 0.330f, 0.328f, 0.329f, 0.328f, 0.329f, 0.329f, 0.329f, 0.329f, -0.126f, -0.429f, -0.471f, -0.481f, -0.503f, -0.528f, -0.548f, -0.558f, -0.557f, -0.543f, -0.516f, -0.477f, -0.427f, -0.365f, -0.292f, -0.209f, -0.118f, -0.020f };
        static readonly float[] Kn1SkillGocY = { 0.122f, 0.154f, 0.217f, 0.311f, 0.422f, 0.519f, 0.584f, 0.644f, 0.697f, 0.743f, 0.780f, 0.809f, 0.829f, 0.842f, 0.850f, 0.855f, 0.856f, 0.857f, 0.855f, 0.849f, 0.846f, 0.846f, 0.846f, 0.846f, 0.845f, 0.836f, 0.834f, 0.838f, 0.830f, 0.822f, 0.819f, 0.821f, 0.823f, 0.820f, 0.813f, 0.804f, 0.798f, 0.793f, 0.791f, 0.790f, 0.789f, 0.787f, 0.784f, 0.779f, 0.772f, 0.764f, 0.755f, 0.746f, 0.740f, 0.734f, 0.731f, 0.729f, 0.728f, 0.728f, 0.728f, 0.728f, 0.728f, 0.728f, 0.728f, 0.728f, 0.715f, 0.727f, 0.770f, 0.854f, 0.974f, 1.101f, 1.199f, 1.248f, 1.260f, 1.260f, 1.260f, 1.260f, 1.260f, 1.260f, 1.260f, 1.260f, 1.260f, 1.248f, 0.890f, 0.885f, 0.175f, 0.119f, 0.119f, 0.119f, 0.119f, 0.119f, 0.119f, 0.119f, 0.119f, 0.119f, 0.119f, 0.119f, 0.119f, 0.119f, 0.119f, -0.030f, 0.177f, 0.315f, 0.352f, 0.354f, 0.336f, 0.302f, 0.260f, 0.217f, 0.182f, 0.154f, 0.128f, 0.105f, 0.086f, 0.075f, 0.073f, 0.082f, 0.104f };
        static readonly float[] Kn1SkillDauX = { -0.013f, 0.040f, 0.130f, 0.222f, 0.290f, 0.322f, 0.327f, 0.323f, 0.311f, 0.295f, 0.275f, 0.255f, 0.237f, 0.220f, 0.207f, 0.196f, 0.192f, 0.185f, 0.179f, 0.177f, 0.174f, 0.171f, 0.168f, 0.164f, 0.163f, 0.165f, 0.162f, 0.157f, 0.159f, 0.162f, 0.162f, 0.157f, 0.151f, 0.150f, 0.152f, 0.155f, 0.157f, 0.156f, 0.155f, 0.152f, 0.149f, 0.147f, 0.145f, 0.144f, 0.145f, 0.147f, 0.151f, 0.158f, 0.164f, 0.177f, 0.186f, 0.191f, 0.194f, 0.194f, 0.194f, 0.194f, 0.194f, 0.194f, 0.194f, 0.194f, 0.224f, 0.243f, 0.288f, 0.330f, 0.335f, 0.283f, 0.181f, 0.066f, -0.022f, -0.056f, -0.056f, -0.056f, -0.056f, -0.056f, -0.056f, -0.056f, -0.056f, -0.187f, -0.553f, -0.160f, 0.818f, 0.772f, 0.763f, 0.771f, 0.764f, 0.770f, 0.766f, 0.768f, 0.766f, 0.768f, 0.767f, 0.767f, 0.767f, 0.767f, 0.767f, 0.071f, -0.443f, -0.504f, -0.526f, -0.574f, -0.624f, -0.659f, -0.676f, -0.670f, -0.640f, -0.584f, -0.502f, -0.396f, -0.269f, -0.124f, 0.033f, 0.196f, 0.354f };
        static readonly float[] Kn1SkillDauY = { 0.143f, 0.170f, 0.223f, 0.306f, 0.404f, 0.492f, 0.552f, 0.607f, 0.657f, 0.700f, 0.735f, 0.762f, 0.782f, 0.795f, 0.803f, 0.808f, 0.809f, 0.810f, 0.808f, 0.802f, 0.798f, 0.799f, 0.803f, 0.833f, 0.855f, 0.873f, 0.894f, 0.915f, 0.920f, 0.925f, 0.933f, 0.948f, 0.961f, 0.969f, 0.972f, 0.973f, 0.976f, 0.981f, 0.988f, 0.995f, 1.002f, 1.006f, 1.009f, 1.010f, 1.010f, 1.009f, 1.007f, 1.038f, 1.090f, 1.125f, 1.147f, 1.156f, 1.176f, 1.176f, 1.176f, 1.176f, 1.176f, 1.176f, 1.176f, 1.176f, 1.159f, 1.171f, 1.216f, 1.302f, 1.423f, 1.552f, 1.649f, 1.699f, 1.711f, 1.710f, 1.710f, 1.710f, 1.710f, 1.710f, 1.710f, 1.710f, 1.710f, 1.675f, 1.039f, 1.241f, 0.162f, 0.040f, 0.040f, 0.040f, 0.040f, 0.040f, 0.040f, 0.040f, 0.040f, 0.040f, 0.040f, 0.040f, 0.040f, 0.040f, 0.040f, -0.435f, -0.273f, -0.134f, -0.096f, -0.091f, -0.105f, -0.135f, -0.175f, -0.219f, -0.258f, -0.291f, -0.322f, -0.345f, -0.354f, -0.343f, -0.307f, -0.242f, -0.146f };
        static readonly float[] Kn1SkillMuiX = { 0.394f, 0.471f, 0.585f, 0.679f, 0.717f, 0.702f, 0.664f, 0.613f, 0.552f, 0.487f, 0.421f, 0.360f, 0.306f, 0.262f, 0.226f, 0.200f, 0.190f, 0.172f, 0.159f, 0.152f, 0.147f, 0.142f, 0.138f, 0.136f, 0.135f, 0.139f, 0.139f, 0.134f, 0.138f, 0.142f, 0.142f, 0.138f, 0.134f, 0.133f, 0.136f, 0.140f, 0.143f, 0.144f, 0.143f, 0.142f, 0.141f, 0.139f, 0.138f, 0.138f, 0.141f, 0.145f, 0.152f, 0.161f, 0.167f, 0.178f, 0.186f, 0.189f, 0.190f, 0.190f, 0.190f, 0.190f, 0.190f, 0.190f, 0.190f, 0.190f, 0.218f, 0.237f, 0.283f, 0.326f, 0.332f, 0.281f, 0.181f, 0.067f, -0.021f, -0.054f, -0.054f, -0.054f, -0.054f, -0.054f, -0.054f, -0.054f, -0.054f, -0.177f, -0.519f, -0.140f, 0.780f, 0.734f, 0.726f, 0.734f, 0.727f, 0.732f, 0.729f, 0.731f, 0.729f, 0.731f, 0.730f, 0.730f, 0.730f, 0.730f, 0.730f, 0.054f, -0.442f, -0.501f, -0.522f, -0.568f, -0.616f, -0.650f, -0.666f, -0.660f, -0.632f, -0.578f, -0.499f, -0.399f, -0.277f, -0.138f, 0.013f, 0.169f, 0.323f };
        static readonly float[] Kn1SkillMuiY = { -0.070f, 0.009f, 0.158f, 0.360f, 0.576f, 0.752f, 0.865f, 0.964f, 1.049f, 1.118f, 1.172f, 1.210f, 1.237f, 1.253f, 1.263f, 1.267f, 1.269f, 1.270f, 1.267f, 1.261f, 1.257f, 1.257f, 1.258f, 1.257f, 1.257f, 1.247f, 1.245f, 1.250f, 1.242f, 1.234f, 1.230f, 1.233f, 1.235f, 1.231f, 1.225f, 1.216f, 1.209f, 1.205f, 1.203f, 1.202f, 1.201f, 1.199f, 1.197f, 1.192f, 1.185f, 1.177f, 1.167f, 1.158f, 1.152f, 1.146f, 1.141f, 1.139f, 1.139f, 1.139f, 1.139f, 1.139f, 1.139f, 1.139f, 1.139f, 1.139f, 1.121f, 1.134f, 1.178f, 1.264f, 1.385f, 1.513f, 1.611f, 1.661f, 1.673f, 1.672f, 1.672f, 1.672f, 1.672f, 1.672f, 1.672f, 1.672f, 1.672f, 1.639f, 1.026f, 1.211f, 0.163f, 0.047f, 0.047f, 0.047f, 0.047f, 0.047f, 0.047f, 0.047f, 0.047f, 0.047f, 0.047f, 0.047f, 0.047f, 0.047f, 0.047f, -0.401f, -0.235f, -0.096f, -0.059f, -0.053f, -0.068f, -0.098f, -0.138f, -0.182f, -0.221f, -0.253f, -0.284f, -0.307f, -0.317f, -0.308f, -0.275f, -0.215f, -0.125f };
        static readonly float[] Kn1SkillHon = { 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 0.973f, 0.859f, 0.684f, 0.479f, 0.278f, 0.112f, 0.014f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f };
        // dạng 2: chiều cao khai 1105.9; skill 3.750 s, trúng 2.670; cast 1.850 s, trúng 1.050
        static readonly float[] Kn2CastTipX = { 0.101f, 0.121f, 0.173f, 0.258f, 0.472f, 0.799f, 0.603f, 0.316f, 0.080f, -0.009f, -0.015f, -0.019f, -0.019f, -0.019f, -0.019f, -0.020f, -0.021f, -0.022f, -0.023f, -0.023f, -0.024f, -0.031f, -0.020f, -0.020f, -0.032f, -0.024f, -0.017f, -0.028f, -0.028f, -0.015f, -0.022f, -0.029f, -0.016f, -0.016f, -0.027f, -0.019f, -0.011f, -0.023f, -0.023f, -0.011f, -0.018f, -0.019f, -0.016f, -0.018f, 0.029f, 0.153f, 0.273f, 0.320f, 0.338f, 0.387f, 0.428f, 0.424f, 0.369f, 0.279f, 0.186f, 0.123f, 0.105f };
        static readonly float[] Kn2CastTipY = { -0.012f, -0.001f, 0.039f, 0.156f, 0.321f, 0.842f, 1.337f, 1.513f, 1.557f, 1.545f, 1.545f, 1.545f, 1.544f, 1.544f, 1.544f, 1.546f, 1.548f, 1.552f, 1.557f, 1.561f, 1.564f, 1.567f, 1.570f, 1.573f, 1.576f, 1.579f, 1.582f, 1.585f, 1.588f, 1.591f, 1.594f, 1.597f, 1.600f, 1.602f, 1.605f, 1.607f, 1.609f, 1.612f, 1.614f, 1.616f, 1.617f, 1.619f, 1.621f, 1.623f, 1.616f, 1.543f, 1.356f, 1.114f, 0.922f, 0.770f, 0.605f, 0.426f, 0.258f, 0.125f, 0.041f, 0.000f, -0.010f };
        static readonly float[] Kn2SkillTipX = { 0.101f, 0.175f, 0.296f, 0.414f, 0.495f, 0.525f, 0.523f, 0.507f, 0.482f, 0.451f, 0.416f, 0.381f, 0.350f, 0.323f, 0.301f, 0.284f, 0.277f, 0.266f, 0.258f, 0.254f, 0.250f, 0.246f, 0.243f, 0.241f, 0.241f, 0.245f, 0.244f, 0.240f, 0.244f, 0.247f, 0.248f, 0.243f, 0.238f, 0.238f, 0.241f, 0.244f, 0.246f, 0.246f, 0.244f, 0.241f, 0.238f, 0.235f, 0.232f, 0.231f, 0.231f, 0.231f, 0.231f, 0.232f, 0.232f, 0.234f, 0.235f, 0.236f, 0.236f, 0.236f, 0.236f, 0.236f, 0.236f, 0.236f, 0.236f, 0.236f, 0.240f, 0.267f, 0.333f, 0.398f, 0.420f, 0.369f, 0.256f, 0.122f, 0.019f, -0.021f, -0.021f, -0.021f, -0.021f, -0.021f, -0.021f, -0.021f, -0.021f, -0.067f, -0.224f, 0.092f, 0.535f, 0.480f, 0.471f, 0.479f, 0.472f, 0.478f, 0.474f, 0.477f, 0.475f, 0.476f, 0.475f, 0.476f, 0.475f, 0.475f, 0.475f, -0.142f, -0.552f, -0.607f, -0.622f, -0.652f, -0.685f, -0.710f, -0.721f, -0.716f, -0.695f, -0.657f, -0.602f, -0.531f, -0.443f, -0.341f, -0.225f, -0.098f, 0.035f };
        static readonly float[] Kn2SkillTipY = { -0.012f, 0.033f, 0.123f, 0.256f, 0.410f, 0.544f, 0.633f, 0.715f, 0.788f, 0.849f, 0.900f, 0.938f, 0.966f, 0.984f, 0.996f, 1.002f, 1.004f, 1.006f, 1.004f, 0.998f, 0.994f, 0.994f, 0.995f, 0.994f, 0.994f, 0.983f, 0.981f, 0.986f, 0.978f, 0.969f, 0.965f, 0.967f, 0.969f, 0.965f, 0.958f, 0.948f, 0.941f, 0.936f, 0.933f, 0.931f, 0.930f, 0.928f, 0.924f, 0.918f, 0.911f, 0.901f, 0.890f, 0.879f, 0.871f, 0.864f, 0.859f, 0.856f, 0.855f, 0.855f, 0.855f, 0.855f, 0.855f, 0.855f, 0.855f, 0.855f, 0.837f, 0.853f, 0.910f, 1.019f, 1.175f, 1.339f, 1.465f, 1.530f, 1.548f, 1.548f, 1.548f, 1.548f, 1.548f, 1.548f, 1.548f, 1.548f, 1.548f, 1.531f, 1.050f, 1.062f, 0.094f, 0.014f, 0.014f, 0.014f, 0.014f, 0.014f, 0.014f, 0.014f, 0.014f, 0.014f, 0.014f, 0.014f, 0.014f, 0.014f, 0.014f, -0.212f, 0.039f, 0.203f, 0.248f, 0.252f, 0.232f, 0.192f, 0.142f, 0.091f, 0.046f, 0.011f, -0.024f, -0.055f, -0.079f, -0.092f, -0.092f, -0.075f, -0.038f };
        static readonly float[] Kn2SkillGocX = { 0.109f, 0.181f, 0.298f, 0.412f, 0.488f, 0.516f, 0.511f, 0.494f, 0.468f, 0.435f, 0.400f, 0.365f, 0.333f, 0.306f, 0.284f, 0.268f, 0.261f, 0.249f, 0.241f, 0.237f, 0.233f, 0.229f, 0.226f, 0.224f, 0.224f, 0.228f, 0.228f, 0.223f, 0.227f, 0.231f, 0.231f, 0.227f, 0.222f, 0.221f, 0.224f, 0.228f, 0.230f, 0.230f, 0.228f, 0.225f, 0.221f, 0.218f, 0.216f, 0.215f, 0.214f, 0.214f, 0.214f, 0.215f, 0.216f, 0.217f, 0.218f, 0.219f, 0.219f, 0.219f, 0.219f, 0.219f, 0.219f, 0.219f, 0.219f, 0.219f, 0.223f, 0.251f, 0.316f, 0.382f, 0.403f, 0.352f, 0.239f, 0.106f, 0.002f, -0.037f, -0.037f, -0.037f, -0.037f, -0.037f, -0.037f, -0.037f, -0.037f, -0.083f, -0.230f, 0.078f, 0.536f, 0.483f, 0.474f, 0.482f, 0.475f, 0.481f, 0.477f, 0.479f, 0.477f, 0.479f, 0.478f, 0.478f, 0.478f, 0.478f, 0.478f, -0.127f, -0.535f, -0.591f, -0.605f, -0.635f, -0.669f, -0.693f, -0.705f, -0.700f, -0.679f, -0.641f, -0.586f, -0.514f, -0.427f, -0.325f, -0.211f, -0.086f, 0.044f };
        static readonly float[] Kn2SkillGocY = { 0.003f, 0.049f, 0.139f, 0.273f, 0.425f, 0.558f, 0.645f, 0.726f, 0.797f, 0.856f, 0.906f, 0.942f, 0.968f, 0.986f, 0.996f, 1.002f, 1.004f, 1.006f, 1.003f, 0.997f, 0.993f, 0.993f, 0.993f, 0.993f, 0.992f, 0.982f, 0.980f, 0.985f, 0.976f, 0.968f, 0.964f, 0.966f, 0.968f, 0.964f, 0.957f, 0.947f, 0.940f, 0.935f, 0.932f, 0.930f, 0.929f, 0.927f, 0.924f, 0.918f, 0.910f, 0.901f, 0.890f, 0.879f, 0.872f, 0.865f, 0.860f, 0.858f, 0.857f, 0.857f, 0.857f, 0.857f, 0.857f, 0.857f, 0.857f, 0.857f, 0.840f, 0.856f, 0.912f, 1.021f, 1.176f, 1.340f, 1.465f, 1.530f, 1.547f, 1.547f, 1.547f, 1.547f, 1.547f, 1.547f, 1.547f, 1.547f, 1.547f, 1.526f, 1.035f, 1.054f, 0.110f, 0.031f, 0.031f, 0.031f, 0.031f, 0.031f, 0.031f, 0.031f, 0.031f, 0.031f, 0.031f, 0.031f, 0.031f, 0.031f, 0.031f, -0.204f, 0.038f, 0.202f, 0.246f, 0.250f, 0.228f, 0.188f, 0.138f, 0.086f, 0.043f, 0.008f, -0.025f, -0.054f, -0.075f, -0.086f, -0.083f, -0.063f, -0.025f };
        static readonly float[] Kn2SkillDauX = { 0.049f, 0.118f, 0.231f, 0.345f, 0.426f, 0.460f, 0.462f, 0.452f, 0.433f, 0.407f, 0.378f, 0.350f, 0.323f, 0.300f, 0.281f, 0.267f, 0.261f, 0.251f, 0.244f, 0.241f, 0.237f, 0.233f, 0.230f, 0.229f, 0.227f, 0.229f, 0.226f, 0.220f, 0.223f, 0.226f, 0.225f, 0.220f, 0.214f, 0.213f, 0.215f, 0.218f, 0.220f, 0.220f, 0.218f, 0.215f, 0.213f, 0.210f, 0.208f, 0.207f, 0.209f, 0.211f, 0.216f, 0.225f, 0.236f, 0.256f, 0.271f, 0.280f, 0.284f, 0.284f, 0.284f, 0.284f, 0.284f, 0.284f, 0.284f, 0.284f, 0.333f, 0.355f, 0.408f, 0.455f, 0.455f, 0.381f, 0.245f, 0.094f, -0.023f, -0.067f, -0.067f, -0.067f, -0.067f, -0.067f, -0.067f, -0.067f, -0.067f, -0.260f, -0.788f, -0.250f, 1.169f, 1.107f, 1.099f, 1.107f, 1.100f, 1.105f, 1.101f, 1.104f, 1.102f, 1.104f, 1.103f, 1.103f, 1.103f, 1.103f, 1.103f, 0.153f, -0.555f, -0.637f, -0.669f, -0.737f, -0.806f, -0.853f, -0.873f, -0.861f, -0.817f, -0.737f, -0.620f, -0.470f, -0.289f, -0.085f, 0.135f, 0.360f, 0.577f };
        static readonly float[] Kn2SkillDauY = { 0.034f, 0.073f, 0.149f, 0.265f, 0.400f, 0.519f, 0.600f, 0.674f, 0.739f, 0.795f, 0.842f, 0.876f, 0.902f, 0.919f, 0.929f, 0.935f, 0.936f, 0.938f, 0.936f, 0.929f, 0.925f, 0.926f, 0.926f, 0.925f, 0.949f, 0.973f, 0.999f, 1.024f, 1.031f, 1.038f, 1.049f, 1.066f, 1.082f, 1.091f, 1.096f, 1.099f, 1.103f, 1.110f, 1.117f, 1.126f, 1.133f, 1.139f, 1.143f, 1.144f, 1.143f, 1.142f, 1.140f, 1.208f, 1.320f, 1.397f, 1.445f, 1.466f, 1.496f, 1.496f, 1.496f, 1.496f, 1.496f, 1.496f, 1.496f, 1.496f, 1.472f, 1.489f, 1.547f, 1.659f, 1.816f, 1.981f, 2.107f, 2.172f, 2.188f, 2.188f, 2.188f, 2.188f, 2.188f, 2.188f, 2.188f, 2.188f, 2.188f, 2.134f, 1.247f, 1.561f, 0.091f, -0.082f, -0.082f, -0.082f, -0.082f, -0.082f, -0.082f, -0.082f, -0.082f, -0.082f, -0.082f, -0.082f, -0.082f, -0.082f, -0.082f, -0.782f, -0.604f, -0.438f, -0.393f, -0.384f, -0.399f, -0.434f, -0.482f, -0.535f, -0.584f, -0.627f, -0.666f, -0.694f, -0.702f, -0.681f, -0.624f, -0.525f, -0.382f };
        static readonly float[] Kn2SkillMuiX = { 0.629f, 0.731f, 0.880f, 0.996f, 1.034f, 1.001f, 0.942f, 0.865f, 0.776f, 0.681f, 0.585f, 0.498f, 0.422f, 0.359f, 0.309f, 0.273f, 0.258f, 0.234f, 0.215f, 0.206f, 0.198f, 0.192f, 0.187f, 0.185f, 0.185f, 0.188f, 0.188f, 0.184f, 0.188f, 0.192f, 0.193f, 0.188f, 0.184f, 0.184f, 0.187f, 0.191f, 0.195f, 0.196f, 0.197f, 0.197f, 0.196f, 0.195f, 0.194f, 0.196f, 0.200f, 0.207f, 0.218f, 0.233f, 0.242f, 0.260f, 0.272f, 0.278f, 0.279f, 0.279f, 0.279f, 0.279f, 0.279f, 0.279f, 0.279f, 0.279f, 0.324f, 0.347f, 0.400f, 0.449f, 0.451f, 0.378f, 0.245f, 0.095f, -0.021f, -0.065f, -0.065f, -0.065f, -0.065f, -0.065f, -0.065f, -0.065f, -0.065f, -0.245f, -0.741f, -0.222f, 1.115f, 1.055f, 1.046f, 1.054f, 1.047f, 1.053f, 1.049f, 1.052f, 1.050f, 1.051f, 1.050f, 1.051f, 1.050f, 1.050f, 1.050f, 0.130f, -0.554f, -0.633f, -0.664f, -0.728f, -0.794f, -0.839f, -0.858f, -0.847f, -0.806f, -0.729f, -0.617f, -0.473f, -0.301f, -0.106f, 0.106f, 0.322f, 0.532f };
        static readonly float[] Kn2SkillMuiY = { -0.269f, -0.157f, 0.056f, 0.342f, 0.644f, 0.889f, 1.045f, 1.182f, 1.297f, 1.391f, 1.463f, 1.514f, 1.549f, 1.571f, 1.584f, 1.590f, 1.592f, 1.593f, 1.591f, 1.584f, 1.579f, 1.580f, 1.580f, 1.579f, 1.579f, 1.569f, 1.566f, 1.571f, 1.563f, 1.554f, 1.550f, 1.553f, 1.555f, 1.551f, 1.543f, 1.534f, 1.526f, 1.521f, 1.519f, 1.517f, 1.516f, 1.514f, 1.511f, 1.505f, 1.498f, 1.488f, 1.477f, 1.466f, 1.459f, 1.451f, 1.445f, 1.442f, 1.442f, 1.442f, 1.442f, 1.442f, 1.442f, 1.442f, 1.442f, 1.442f, 1.419f, 1.436f, 1.494f, 1.605f, 1.762f, 1.927f, 2.053f, 2.118f, 2.134f, 2.134f, 2.134f, 2.134f, 2.134f, 2.134f, 2.134f, 2.134f, 2.134f, 2.082f, 1.229f, 1.518f, 0.093f, -0.072f, -0.072f, -0.072f, -0.072f, -0.072f, -0.072f, -0.072f, -0.072f, -0.072f, -0.072f, -0.072f, -0.072f, -0.072f, -0.072f, -0.733f, -0.549f, -0.384f, -0.339f, -0.331f, -0.346f, -0.381f, -0.429f, -0.483f, -0.531f, -0.573f, -0.612f, -0.640f, -0.649f, -0.631f, -0.578f, -0.486f, -0.352f };
        static readonly float[] Kn2SkillHon = { 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 1.000f, 0.973f, 0.859f, 0.684f, 0.479f, 0.278f, 0.112f, 0.014f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f, 0.000f };

        static Vector2 KnMau(float[] xs, float[] ys, float t)
        {
            float f = Mathf.Max(0, t) / KnDt;
            int i = Mathf.Clamp((int)f, 0, xs.Length - 1), j = Mathf.Min(i + 1, xs.Length - 1);
            float w = Mathf.Clamp01(f - i);
            return new Vector2(Mathf.Lerp(xs[i], xs[j], w), Mathf.Lerp(ys[i], ys[j], w));
        }

        static float KnMau1(float[] xs, float t)
        {
            float f = Mathf.Max(0, t) / KnDt;
            int i = Mathf.Clamp((int)f, 0, xs.Length - 1), j = Mathf.Min(i + 1, xs.Length - 1);
            return Mathf.Lerp(xs[i], xs[j], Mathf.Clamp01(f - i));
        }

        // điểm bảng (phần chiều cao, x tới trước, y lên) → sân (y xuống)
        static Vector2 KnO(Vector2 feet, float H, float dir, Vector2 n) => feet + new Vector2(dir * n.x * H, -n.y * H);

        // ảnh hồn đồng đội (AolaImport nhập tên có "_tt_" thành sprite), nạp một lần
        static readonly Dictionary<string, Sprite> knAnh = new Dictionary<string, Sprite>();

        static Sprite KnHonAnh()
        {
            const string key = "ky_nguyen_2_tt_hon";
            if (knAnh.TryGetValue(key, out var s) && s) return s;
            s = PokiClash.Game.ContentPacks.Get<Sprite>(key); // tướng trong gói tải sau (GD_Claude/27)
            if (!s) s = Resources.Load<Sprite>("ky_nguyen_2/" + key);
            knAnh[key] = s;
            return s;
        }

        // chớp hồn: vương miện toé xanh (khuôn SatChop)
        void HonChop(Vector2 c, float size, int group = Front, float life = 0.16f)
        {
            var p = new P { pos = c, life = life, group = group, ang = U(0, 360), seed = 2 + rng.Next(2), sz = size };
            p.draw = (q, k, buf) =>
            {
                for (int i = 0; i < 5; i++)
                    Put(buf, q.group, 33 + i * 0.1f, S((i == 0 ? "crowns_" : "crown_") + q.seed), KnChopC[i], q.pos,
                        q.sz * (0.6f + 0.5f * EaseOut(k / 0.6f)) * BurstF[i] + (i == 0 ? 5 : 0), 1, q.ang);
            };
            Add(p);
        }

        // lưỡi lửa hồn: tip +1 ngọn theo hướng bay (toé), −1 ngả ngược (đuôi, vệt)
        P HonLuoi(Vector2 p, Vector2 v, float r0, float r1, float life, int g, float tip = 1, float up = 0.5f)
        {
            var q = Flame(p, v, life, r0, r1, "tron", "hon", g, 2.6f, -280, 1.6f, 0.12f, 0.08f);
            Tongue(q, tip, up);
            q.smokeGroup = Back;
            return q;
        }

        // một cú trúng của hồn: chớp, lưỡi lửa hồn toé theo hướng d, tia, mảnh giáp rỉ
        void HonTrung(Vector2 c, Vector2 d, float tH, float manh, int nLua, int nTia)
        {
            KmBong(c - d * 0.04f * tH, -d, 0.3f * tH * manh, 0.12f, KmHon);   // bông va chạm toé ngược hướng đánh (2026-11-18)
            HonChop(c, 0.4f * tH * manh);
            for (int i = 0; i < Mathf.RoundToInt(nLua * manh); i++)
            {
                var dd = (d * U(0.2f, 1f) + new Vector2(U(-0.8f, 0.8f), U(-1f, 0.3f))).normalized;
                HonLuoi(c + U2(-6, 6), dd * U(160, 360) * manh, U(6, 9) * manh, U(16, 26) * manh, U(0.22f, 0.36f), Front, 1, 0.3f);
            }
            for (int i = 0; i < Mathf.RoundToInt(nTia * manh); i++)   // tia bắn nhanh rồi khựng
                KmTiaLua(c, (d * U(0.3f, 1f) + new Vector2(U(-0.7f, 0.7f), U(-0.9f, 0.4f))).normalized, U(380, 680), U(6, 9), KmHon[3 + (i & 1)]);
            Extra(c, Mathf.RoundToInt(3 * manh), 260 * manh);
        }

        // ĐÒN THƯỜNG: lao tới, vung kiếm qua đầu, bổ. lead: giây từ đầu clip attack tới khung trúng.
        public float NHonChem(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.08f, lead);
            var c = foeBody + new Vector2(-dir * 0.1f * tH, -0.02f * tH);
            float R = 0.46f * tH;
            // vệt chém: cung lưỡi lửa hồn quét từ trên sau qua đỉnh xuống dưới trước đối thủ trong 0,07 s trước khung trúng
            for (int i = 0; i < 10; i++)
            {
                float f = i / 9f;
                float ph = Mathf.Lerp(140f, -35f, f) * Mathf.Deg2Rad;
                var pt = c + new Vector2(dir * Mathf.Cos(ph), -Mathf.Sin(ph)) * R;
                var tg = new Vector2(dir * Mathf.Sin(ph), Mathf.Cos(ph));                 // tiếp tuyến theo chiều quét
                At(t0 - 0.075f + 0.075f * f, () => HonLuoi(pt, tg * U(120, 220), U(7, 9), U(17, 24), U(0.16f, 0.24f), Front, -1, 0.15f));
            }
            At(t0, () =>
            {
                Shake?.Invoke(0.26f);
                HonTrung(c, new Vector2(dir, 0.4f).normalized, tH, 1f, 8, 8);
                KmVong(_ => c, 0.3f, 0.05f * tH, 0.5f * tH, KnNhat, 0.5f, 0.85f);   // vòng mảnh không viền (2026-11-18)
            });
            return t0;
        }

        // MỘT HỒN ĐỒNG ĐỘI: bay ra từ mũi kiếm tới chỗ lơ lửng (quạt trên đầu) trong 0,18 s, lơ lửng nhấp nhô, tới tBay lao theo cung xuống tgt
        // (tới nơi đúng hết đời hạt) để lại đuôi lửa hồn; trúng: chớp + lưỡi lửa toé. H: chiều cao hình hồn (sân).
        // nhip: sức nhịp trúng phụ khi hồn chạm (0: hồn đầu, cú trúng chính do StageView lo)
        void HonDongDoi(Vector2 tip, Vector2 home, Vector2 tgt, float H, float tBay, float life, float dir, float tHFoe, float manh, bool cuoi, float nhip = 0.4f)
        {
            float ph = U(0, 6.28f);
            var ctrl = (home + tgt) * 0.5f + new Vector2(0, -0.6f * H);
            var p = new P { pos = tip, life = life, group = Front, sz = H, home = home, aim = tgt, off = ctrl };
            p.upd = (q, dt, s3) =>
            {
                float t = q.age;
                Vector2 np;
                if (t < 0.24f) np = Vector2.Lerp(tip, q.home, EaseOut(t / 0.24f));
                else if (t < tBay) np = q.home + new Vector2(0, Mathf.Sin((t - 0.24f) * 6.3f + ph) * 0.06f * H);
                else
                {
                    float u = Mathf.Pow(Mathf.Clamp01((t - tBay) / Mathf.Max(0.05f, q.life - tBay)), 1.35f);
                    np = (1 - u) * (1 - u) * q.home + 2 * u * (1 - u) * q.off + u * u * q.aim;
                }
                q.vel = dt > 1e-5f ? (np - q.pos) / dt : Vector2.zero;
                if (t > 0.05f && (float)q.rng.NextDouble() < (t < tBay ? 0.25f : 0.9f))
                    HonLuoi(q.pos + new Vector2(0, 0.25f * H) + U2(-0.12f, 0.12f) * H, -q.vel * 0.08f + new Vector2(U(-20, 20), -U(30, 80)),
                        U(4, 6) * manh, U(10, 16) * manh, U(0.18f, 0.28f), Back, -1, 0.5f);
            };
            var anh = KnHonAnh();
            float st = anh ? anh.rect.width / Mathf.Max(1f, anh.rect.height) : 0.8f;
            p.draw = (q, k, buf) =>
            {
                float t = k * q.life;
                float s = EaseOut(Mathf.Clamp01(t / 0.16f));
                float lean = Mathf.Clamp(q.vel.x * dir / 900f, -1, 1) * 22f;
                if (anh) Put(buf, q.group, 46, anh, Color.white, q.pos, q.sz * s, st, -dir * lean, 0.95f, 0, dir < 0);
                else Put(buf, q.group, 46, S("blob_0"), KnXanh, q.pos, q.sz * 0.6f * s, 1, 0, 0.9f);
            };
            p.onDeath = (q, s3) =>
            {
                s3.KmNhip(nhip);   // đối thủ chớp + giật theo từng hồn
                HonTrung(tgt, new Vector2(dir, 0.3f).normalized, tHFoe, (cuoi ? 1.2f : 0.8f) * manh, cuoi ? 8 : 5, cuoi ? 8 : 4);
                if (cuoi)
                {
                    // hồn cuối NỔ HỒN kiểu KR5: chớp 2 khung, lưỡi liềm lửa hồn trong khối khói hồn hai tông sau lưng đối thủ, tách cụm bay lên
                    Shake?.Invoke(0.4f * manh);
                    KmNo(tgt, new Vector2(tgt.x, tgt.y + 0.45f * tHFoe), tHFoe, 0.9f * manh, "hon", dir, KmKhoiHon);
                }
                else Shake?.Invoke(0.16f);
            };
            Add(p);
        }

        // CHIÊU MANA: n hồn (3 dạng 1, 5 dạng 2). lead: giây từ đầu clip cast tới trúng (hồn đầu chạm). Trả giây tới lúc hồn đầu trúng.
        public float NHonGoi(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int n, float manh)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float k = Mathf.Max(0.3f, lead) / KnCLead;
            float tGoi = KnCGoi * k, tTrung = Mathf.Max(0.3f, lead);
            bool non = manh < 0.95f;                                                      // bản nhẹ = dạng 1 (rig riêng: tay ngắn, kiếm nhỏ)
            var tip = KnO(casterFeet, casterH, dir, KnMau(non ? Kn1CastTipX : Kn2CastTipX, non ? Kn1CastTipY : Kn2CastTipY, KnCGoi));
            At(tGoi, () =>
            {
                HonChop(tip, 0.32f * casterH * manh, Front, 0.2f);
                KmVong(_ => tip, 0.4f, 0.04f * casterH, 0.42f * casterH * manh, KnNhat, 1, 0.85f);
                for (int i = 0; i < 7; i++) HonLuoi(tip + U2(-8, 8), new Vector2(U(-160, 160), -U(140, 320)), 6, U(14, 22) * manh, U(0.24f, 0.36f), Front, 1, 0.5f);
                for (int i = 0; i < 6; i++) Spark(tip, new Vector2(U(-1f, 1f), U(-1f, 0.1f)), U(160, 320), U(0.16f, 0.26f), U(5, 8), 120);
            });
            Every(tGoi, tGoi + 0.72f * k, 26, _ => HonLuoi(tip + U2(-0.05f, 0.05f) * casterH, new Vector2(U(-40, 40), -U(60, 140)), 4, U(10, 16) * manh,
                U(0.2f, 0.3f), Front, 1, 0.6f));
            float H = 0.46f * casterH * Mathf.Sqrt(manh);
            for (int i = 0; i < n; i++)
            {
                float f = n == 1 ? 0.5f : i / (n - 1f);
                float tHien = tGoi + 0.05f * i;
                float tToi = tTrung + 0.075f * i;
                // chỗ lơ lửng: VÒNG CUNG quanh vai, từ sau lưng sang phía đối thủ (mũi kiếm giơ sát mép trên màn: xếp quạt trên mũi kiếm thì hồn
                // lọt khỏi màn, nấp sau bảng máu đối thủ — soi trong trận 2026-11-16)
                float cao = Mathf.Lerp(1.05f, 1.3f, 1f - Mathf.Abs(f - 0.5f) * 2f);
                var home = casterFeet + new Vector2(dir * Mathf.Lerp(-0.3f, 0.62f, f) * casterH, -cao * casterH);
                var tgt = foeBody + new Vector2(-dir * U(0f, 0.08f) * tH, (f - 0.5f) * 0.32f * tH);
                bool cuoi = i == n - 1;
                float life = tToi - tHien, tBay = Mathf.Max(0.22f, life - 0.34f);
                float nhip = i == 0 ? 0 : cuoi ? 0.8f : 0.4f;
                At(tHien, () => HonDongDoi(tip, home, tgt, H, tBay, life, dir, tH, manh, cuoi, nhip));
            }
            return tTrung;
        }

        // CHIÊU CUỐI: lead: giây từ đầu clip skill tới nhát bổ trúng. manh: 0,8 dạng 1, 1 dạng 2. Trả giây tới lúc trúng.
        public float NHonKiem(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, float manh)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float k = Mathf.Max(0.3f, lead) / KnSLead, T0 = T;
            float tTrung = Mathf.Max(0.3f, lead);
            bool non = manh < 0.95f;                                                      // bản nhẹ = dạng 1 (rig riêng: tay ngắn, kiếm nhỏ)
            float[] dX = non ? Kn1SkillDauX : Kn2SkillDauX, dY = non ? Kn1SkillDauY : Kn2SkillDauY;
            float[] gX = non ? Kn1SkillGocX : Kn2SkillGocX, gY = non ? Kn1SkillGocY : Kn2SkillGocY;
            float[] mX = non ? Kn1SkillMuiX : Kn2SkillMuiX, mY = non ? Kn1SkillMuiY : Kn2SkillMuiY;
            float[] honA = non ? Kn1SkillHon : Kn2SkillHon;
            Vector2 Dau(float tc) => KnO(casterFeet, casterH, dir, KnMau(dX, dY, tc));
            Vector2 Goc(float tc) => KnO(casterFeet, casterH, dir, KnMau(gX, gY, tc));
            Vector2 Mui(float tc) => KnO(casterFeet, casterH, dir, KnMau(mX, mY, tc));
            float r = 0.012f * casterH;                                                   // cỡ hạt nhỏ theo thân
            // khí hồn bị hút vào mép đang hiện của phần vá (2026-11-18, người dùng chê pha hút xấu): VỆT hồn xanh thuôn kéo theo vận tốc, bay XOẮN
            // ỐC vào mép vá, nhanh dần, hiện dần lúc sinh, chạm mép thì nhập; dày dần tới lúc kiếm lành; thêm vài lưỡi lửa hồn bay vào; tia lấp
            // lánh ở mép
            System.Func<float, Vector2> mep = t => Dau(Mathf.Clamp((t - T0) / k, KnSHut, KnSHoi));
            float rMep = 0.025f * casterH;
            Every(KnSHut * k, KnSHoi * k, x => 26 + 30 * x, x =>
            {
                float tc = Mathf.Lerp(KnSHut, KnSHoi, x);
                if (KnMau1(honA, tc) < 0.5f && tc > KnSHut + 0.12f) return;
                KmHut(mep, _ => rMep, U(0.5f, 0.9f) * casterH, U(0.3f, 0.42f), U(6, 8) * manh, KmHon[3 + rng.Next(2)], -dir, rng.Next(2) == 0 ? Back : Front, 0.7f);
            });
            Every(KnSHut * k, KnSHoi * k, 10, x =>
            {
                float tc = Mathf.Lerp(KnSHut, KnSHoi, x);
                if (KnMau1(honA, tc) < 0.5f && tc > KnSHut + 0.12f) return;
                var dau = Dau(tc);
                float a = U(0, 6.28f), d = U(0.5f, 0.85f) * casterH;
                var from = dau + new Vector2(Mathf.Cos(a) * d, Mathf.Sin(a) * d * 0.7f + 0.15f * casterH);
                var q = HonLuoi(from, (dau - from) / 0.32f, U(4, 6) * manh, U(9, 14) * manh, 0.32f, (rng.Next(2) == 0) ? Back : Front, -1, 0.1f);
                q.drag = 0;
                q.acc = Vector2.zero;
            });
            At((KnSHut + 0.5f * (KnSHoi - KnSHut)) * k, () => KmVong(mep, 0.26f, 0.7f * casterH, rMep, KmHon[4], 0.8f, 0.7f));
            Every(KnSHut * k + 0.1f, KnSHoi * k, 30, x =>
            {
                float tc = Mathf.Lerp(KnSHut + 0.1f / k, KnSHoi, x);
                if (KnMau1(honA, tc) < 0.5f) return;
                Spark(Dau(tc), new Vector2(U(-1f, 1f), U(-1f, 0.2f)), U(80, 200), U(0.12f, 0.22f), U(5, 8) * manh, 60);
            });
            // tay hất: lửa hồn chạy dọc lưỡi tới mũi
            Every(KnSHat * k, KnSHoi * k, 50, x =>
            {
                float tc = Mathf.Lerp(KnSHat, KnSHoi, x);
                HonLuoi(Dau(tc) + U2(-0.02f, 0.02f) * casterH, new Vector2(U(-50, 50), -U(80, 180)), 5, U(12, 18) * manh, U(0.2f, 0.3f), Front, 1, 0.6f);
            });
            // kiếm lành: bùng sáng dọc lưỡi
            At(KnSHoi * k, () =>
            {
                var g = Goc(KnSHoi);
                var m = Mui(KnSHoi);
                HonChop(m, 0.3f * casterH * manh, Front, 0.18f);
                for (int i = 0; i < 10; i++)
                {
                    var pt = Vector2.Lerp(g, m, i / 9f);
                    HonLuoi(pt + U2(-6, 6), new Vector2(U(-120, 120), -U(60, 200)), 6, U(14, 22) * manh, U(0.24f, 0.34f), Front, 1, 0.5f);
                }
                var giua = Vector2.Lerp(g, m, 0.5f);
                KmVong(_ => giua, 0.36f, 0.05f * casterH, 0.5f * casterH * manh, KnNhat, 0.9f, 0.85f);
            });
            // giơ qua đầu: aura hồn bùng quanh người
            At(KnSGong * k, () =>
            {
                Shake?.Invoke(0.22f * manh);
                KmCung(casterFeet + new Vector2(0, 2), 0.1f * casterH, 1.0f * casterH * manh, 0.45f, KnXanh, 0.3f, Floor, 30.6f, 0.85f);   // vòng cung dẹt không viền (KR5)
                KmCung(casterFeet + new Vector2(0, 2), 0.06f * casterH, 0.75f * casterH * manh, 0.5f, KnNhat, 0.3f, Floor, 31);
                // aura lửa hồn: lưỡi chữ S liền khối có giọt tách (KmLuaS; ảnh chưa nhập thì lưỡi cũ)
                for (int i = 0; i < Mathf.RoundToInt(12 * manh); i++)
                {
                    var pt = casterFeet + new Vector2(U(-0.42f, 0.42f) * casterH, -U(0.05f, 0.9f) * casterH);
                    int g = (i & 1) == 0 ? Back : Front;
                    if (KmLuaS(pt + new Vector2(0, 0.1f * casterH), U(0.16f, 0.24f) * casterH * manh, U(0.34f, 0.48f), KmHon, "hon", g,
                            new Vector2(U(-40, 40), -U(120, 240)), 0.5f) == null)
                        HonLuoi(pt, new Vector2(U(-60, 60), -U(160, 320)), 6, U(16, 26) * manh, U(0.3f, 0.45f), g, 1, 0.8f);
                }
                var m = Mui(KnSGong);
                for (int i = 0; i < 6; i++) Spark(m, new Vector2(U(-1f, 1f), U(-1f, 0.3f)), U(160, 300), U(0.16f, 0.26f), U(5, 8), 120);
            });
            // lửa hồn liếm dọc lưỡi trong lúc giơ qua đầu
            Every(KnSHoi * k, KnSChem * k, 22, x =>
            {
                float tc = Mathf.Lerp(KnSHoi, KnSChem, x);
                var pt = Vector2.Lerp(Goc(tc), Mui(tc), U(0.05f, 0.95f));
                HonLuoi(pt, new Vector2(U(-30, 30), -U(60, 140)), 4, U(9, 14) * manh, U(0.18f, 0.26f), Front, 1, 0.6f);
            });
            // nhát bổ: vệt lửa hồn theo đúng đường mũi kiếm
            Every(KnSChem * k, tTrung + 0.02f, 160, x =>
            {
                float tc = Mathf.Lerp(KnSChem, KnSLead + 0.02f / k, x);
                var a0 = Mui(tc);
                var a1 = Mui(tc - 0.02f);
                HonLuoi(a0 + U2(-6, 6), (a0 - a1) / 0.02f * 0.08f, U(8, 11) * manh, U(20, 30) * manh, U(0.16f, 0.24f), Front, -1, 0.1f);
                if ((rng.Next(3)) == 0) HonLuoi(Vector2.Lerp(Goc(tc), a0, U(0.4f, 0.9f)), (a0 - a1) / 0.02f * 0.05f, 6, U(14, 20) * manh, 0.18f, Front, -1, 0.1f);
            });
            // TRÚNG: chớp lớn, hai vòng sóng, cột lưỡi lửa hồn toé lên, khói hồn, mảnh giáp, đá
            // TRÚNG (2026-11-18): NỔ HỒN KIỂU KR5 thay chớp hồn 0,9 thân trùm kín đối thủ: chớp 2 khung, lưỡi liềm lửa hồn cắm trong khối khói hồn hai
            // tông sau lưng đối thủ, khói tách cụm bay lên rồi mờ, vòng cung dẹt hai đợt, vệt cháy, cột lưỡi lửa hồn (phần lớn sau lưng), mảnh giáp
            At(tTrung, () =>
            {
                Shake?.Invoke(0.7f * manh);
                var c = foeBody + new Vector2(-dir * 0.06f * tH, 0.06f * tH);
                HonTrung(c, new Vector2(dir, 0.5f).normalized, tH, 1.3f * manh, 8, 10);
                KmNo(c + new Vector2(0, -0.08f * tH), foeFeet, tH, 1.5f * manh, "hon", dir, KmKhoiHon);
                KmCung(foeFeet + new Vector2(0, 2), 0.1f * tH, 1.35f * tH * manh, 0.45f, KnXanh, 0.3f, Floor, 30.6f, 0.85f);
                KmCung(foeFeet + new Vector2(0, 2), 0.06f * tH, 1.0f * tH * manh, 0.6f, KnNhat, 0.3f, Floor, 31);
                for (int i = 0; i < Mathf.RoundToInt(10 * manh); i++)
                {
                    var pt = foeFeet + new Vector2(U(-0.45f, 0.45f) * tH, -U(0f, 0.25f) * tH);
                    HonLuoi(pt, new Vector2(U(-120, 120), -U(260, 620) * manh), 8, U(20, 34) * manh, U(0.34f, 0.5f), i % 3 == 0 ? Front : Back, 1, 0.85f);
                }
                for (int i = 0; i < Mathf.RoundToInt(3 * manh); i++)
                    Rock(foeFeet + new Vector2(U(-0.25f, 0.25f) * tH, -6), new Vector2(U(-260, 260), -U(260, 480)), foeFeet.y + U(-4, 6), U(11, 16));
            });
            At(tTrung + 0.3f, () =>
            {
                for (int i = 0; i < Mathf.RoundToInt(3 * manh); i++)
                    KmKhoi(foeFeet + new Vector2(U(-0.35f, 0.35f) * tH, -U(0.35f, 0.6f) * tH), new Vector2(U(-30, 30), -U(50, 90)), U(0.14f, 0.18f) * tH,
                        U(1.0f, 1.3f), Back, 0, 2, KmKhoiHon, 0.4f);
            });
            // phần vá tan: khí hồn bay lên dọc lưỡi
            Every(KnSTat * k, KnSTat * k + 0.24f * k, 60, x =>
            {
                float tc = KnSTat + 0.24f * x;
                var pt = Vector2.Lerp(Goc(tc), Mui(tc), U(0f, 1f));
                HonLuoi(pt, new Vector2(U(-40, 40), -U(80, 200)), 4, U(10, 16) * manh, U(0.24f, 0.36f), Front, 1, 0.7f);
            });
            return tTrung;
        }
    }
}
