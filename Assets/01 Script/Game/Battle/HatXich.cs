// Bộ QUỶ XÍCH (2026-11-16, quỷ béo mặc giáp, móc nối xích sắt, suất khien_bac ải 20 đảo Kim; rig ArtGen/Spine/quy_xich_rig.py (rig gốc
// monster_3408): dạng 1 non quy_xich_1 (QX_DANG=non), dạng 2 quy_xich_2; ghi chú ArtGen/Spine/inbox/quy_xich_ghichu.md).
// Người dùng: đánh thường "bay tới dùng móc gõ vào đầu đối thủ" (tướng lao tới); chiêu mana "quay xích ném đối thủ" (móc + xích là mảnh của
// rig trên xương fly_*, game lái tới đối thủ); chiêu cuối "xích sắt bốc lửa, xoay xích tạo ra trail lửa và khói, ném trói đối thủ sau đó thiêu
// đốt; thêm 1 cột lửa rất to thiêu cháy đối thủ". Đi đường "n_" (StageView.PreFx / AtkFx → PlayNuoc), phát lúc clip BẮT ĐẦU; mốc là giây clip
// của rig, co theo `lead` (giờ trúng của clip):
// - n_xich_go (đòn thường): móc gõ đỉnh đầu đối thủ: chớp sắt, tia toé, dăm thép; móc đập xuống: bụi dưới chân đối thủ.
// - n_xich_nem1 / n_xich_nem (chiêu mana): vệt gió kim loại theo đúng đường móc quay, tia + bụi lúc ném, móc găm: chớp, vòng sóng, dăm, rung;
//   móc giật ra: tia, dăm; móc về tay: chớp nhỏ.
// - n_xich_lua1 / n_xich_lua (chiêu cuối): `lua_xich` móc bốc lửa; lúc quay: vệt lửa + khói theo đúng đường móc quay, lửa liếm dọc xích; ném:
//   lửa chạy dọc xích từ tay tới đối thủ; `troi`: VÒNG XÍCH quấn quanh thân đối thủ (ảnh mắt xích của rig: Resources/quy_xich_2/
//   quy_xich_2_tt_xich_<1|2>.png), nóng đỏ dần, lửa liếm vòng xích, xích căng cháy; `cot_lua`: CỘT LỬA rất to bốc từ chân đối thủ (cao tới gần
//   mép trên màn, tối đa 2,4 lần thân), vòng lửa + khe nứt dưới đất, khói đen ở đỉnh, than; bốn nhịp `chay`: nổ lửa trên thân; `tha`: vòng
//   xích rơi, lửa dọc xích tắt dần theo xích rút về, khói.
// Điểm trên rig (đầu móc khi quay, ba điểm giữa xích dài, chỗ xích nối tay) là bảng số đo theo khung 30 / giây (phần của chiều cao KHAI cho
// game, x về phía trước, y lên): đổi clip hay tỉ lệ rig thì đo lại và sinh lại file này (ArtGen/Spine/quy_xich_hat_cs.py). FILE SINH TỰ ĐỘNG.
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed partial class HatLua
    {
        // mốc clip (giây) của rig: attack / cast / skill
        const float XqDt = 1f / 30f;
        const float XqALead = 0.775f;
        const float XqCLead = 0.895f, XqCQuay = 0.20f, XqCNem = 0.733f, XqCRut = 1.07f, XqCVe = 1.267f;
        const float XqSLead = 1.732f, XqSLua = 0.10f, XqSNem = 1.022f, XqSTroi = 1.182f, XqSCot = 1.582f, XqSTha = 2.682f, XqSRut = 2.882f;
        static readonly Color XqThep = C(170, 174, 184), XqNong = C(255, 150, 70), XqGio = C(236, 238, 244);

        // quy_xich_non: chiều cao khai 662.7; skill 3.232 s, trúng 1.732; cast 1.500 s, trúng 0.895
        static readonly float[] Xq1SMocX = { -0.094f, -0.044f, 0.020f, 0.095f, 0.178f, 0.260f, 0.439f, 0.508f, 0.422f, 0.192f, -0.124f, -0.670f, -0.953f, -0.467f, 0.422f, 0.118f, -0.365f, -0.955f, -0.467f, 0.365f, -0.078f, -0.872f, -0.495f, 0.071f, -0.490f, -1.106f, -0.793f, -0.295f, -0.535f, 0.934f, 0.020f, 0.087f, 0.251f, 0.369f, 0.562f, 0.867f, 0.907f, 0.970f, 1.054f, 1.154f, 1.228f, 1.266f, 1.268f, 1.255f, 1.246f, 1.239f, 1.221f, 1.205f, 1.207f, 1.212f, 1.221f, 1.237f, 1.250f, 1.257f, 1.271f, 1.250f, 1.196f, 1.117f, 1.017f, 0.930f, 0.884f, 0.869f, 0.869f, 0.896f, 0.970f, 1.067f, 1.154f, 1.223f, 1.266f, 1.261f, 1.253f, 1.249f, 1.240f, 1.229f, 1.223f, 1.222f, 1.226f, 1.234f, 1.241f, 1.251f, 1.262f, 0.739f, 0.706f, 0.704f, 0.600f, 0.437f, 0.273f, -0.078f, -0.439f, 0.004f, 1.021f, 1.328f, 0.716f, 0.601f, 1.573f, 1.573f, 1.573f, 1.573f };
        static readonly float[] Xq1SMocY = { 0.216f, 0.172f, 0.139f, 0.124f, 0.131f, 0.161f, 0.330f, 0.601f, 0.895f, 1.123f, 1.217f, 1.383f, 0.819f, 0.304f, 0.895f, 1.161f, 1.396f, 1.000f, 0.304f, 0.977f, 1.213f, 1.217f, 0.311f, 0.832f, 1.327f, 0.991f, 0.320f, 0.222f, 0.584f, 1.510f, 0.647f, 0.460f, 0.336f, 0.182f, -0.152f, -0.223f, -0.215f, -0.206f, -0.170f, -0.053f, 0.072f, 0.169f, 0.296f, 0.315f, 0.289f, 0.214f, 0.080f, 0.026f, 0.062f, 0.063f, 0.059f, 0.123f, 0.236f, 0.313f, 0.217f, 0.078f, -0.001f, -0.083f, -0.180f, -0.233f, -0.221f, -0.201f, -0.218f, -0.240f, -0.206f, -0.125f, -0.053f, 0.018f, 0.157f, 0.349f, 0.337f, 0.242f, 0.182f, 0.190f, 0.198f, 0.161f, 0.139f, 0.188f, 0.264f, 0.292f, 0.304f, -0.260f, -0.355f, -0.432f, -0.376f, -0.182f, 0.024f, -0.500f, -0.241f, 0.417f, 0.340f, -0.521f, -0.730f, 0.128f, 0.687f, 0.687f, 0.687f, 0.687f };
        static readonly byte[] Xq1SMocHien = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
        static readonly float[] Xq1SXich0X = { 0.484f, 0.522f, 0.547f, 0.555f, 0.547f, 0.522f, 0.403f, 0.204f, -0.037f, -0.275f, -0.467f, -0.476f, -0.482f, -0.484f, -0.037f, -0.328f, -0.472f, -0.481f, -0.484f, -0.113f, -0.444f, -0.479f, -0.484f, -0.482f, -0.477f, -0.469f, -0.458f, -0.380f, -0.049f, 0.581f, 0.716f, 0.751f, 0.788f, 0.810f, 0.797f, 0.786f, 0.785f, 0.785f, 0.784f, 0.771f, 0.764f, 0.768f, 0.767f, 0.755f, 0.746f, 0.751f, 0.762f, 0.761f, 0.755f, 0.758f, 0.765f, 0.764f, 0.757f, 0.758f, 0.769f, 0.775f, 0.770f, 0.770f, 0.782f, 0.790f, 0.786f, 0.779f, 0.785f, 0.791f, 0.785f, 0.773f, 0.771f, 0.776f, 0.771f, 0.756f, 0.750f, 0.756f, 0.758f, 0.748f, 0.741f, 0.748f, 0.755f, 0.751f, 0.745f, 0.752f, 0.764f, 0.708f, 0.649f, 0.468f, 0.219f, -0.038f, -0.224f, -0.101f, 0.106f, 0.370f, 0.571f, 0.792f, 1.026f, 1.268f, 1.506f, 1.506f, 1.506f, 1.506f };
        static readonly float[] Xq1SXich0Y = { 0.239f, 0.313f, 0.396f, 0.484f, 0.573f, 0.661f, 0.877f, 1.031f, 1.095f, 1.061f, 0.945f, 0.916f, 0.886f, 0.855f, 1.095f, 1.039f, 0.931f, 0.893f, 0.855f, 1.094f, 0.965f, 0.904f, 0.856f, 0.814f, 0.784f, 0.754f, 0.725f, 0.799f, 1.011f, 0.936f, 0.503f, 0.477f, 0.450f, 0.433f, 0.434f, 0.435f, 0.436f, 0.427f, 0.421f, 0.448f, 0.454f, 0.427f, 0.415f, 0.437f, 0.451f, 0.428f, 0.361f, 0.336f, 0.361f, 0.356f, 0.340f, 0.361f, 0.405f, 0.422f, 0.407f, 0.411f, 0.444f, 0.456f, 0.431f, 0.414f, 0.435f, 0.457f, 0.440f, 0.415f, 0.427f, 0.454f, 0.448f, 0.420f, 0.420f, 0.448f, 0.451f, 0.422f, 0.408f, 0.430f, 0.445f, 0.425f, 0.404f, 0.422f, 0.448f, 0.440f, 0.416f, 0.387f, 0.286f, 0.134f, 0.063f, 0.091f, 0.179f, 0.047f, -0.048f, -0.070f, -0.113f, -0.130f, -0.120f, -0.081f, -0.017f, -0.017f, -0.017f, -0.017f };
        static readonly float[] Xq1SXich1X = { 0.381f, 0.432f, 0.478f, 0.517f, 0.543f, 0.553f, 0.494f, 0.319f, 0.054f, -0.244f, -0.511f, -0.584f, -0.516f, -0.399f, 0.054f, -0.316f, -0.564f, -0.544f, -0.399f, -0.038f, -0.478f, -0.572f, -0.402f, -0.413f, -0.538f, -0.592f, -0.495f, -0.366f, -0.164f, 0.697f, 0.587f, 0.631f, 0.720f, 0.787f, 0.769f, 0.755f, 0.753f, 0.752f, 0.749f, 0.738f, 0.731f, 0.731f, 0.727f, 0.715f, 0.705f, 0.705f, 0.707f, 0.702f, 0.698f, 0.701f, 0.708f, 0.711f, 0.712f, 0.718f, 0.729f, 0.736f, 0.736f, 0.739f, 0.749f, 0.756f, 0.754f, 0.751f, 0.754f, 0.757f, 0.752f, 0.742f, 0.738f, 0.738f, 0.732f, 0.720f, 0.712f, 0.712f, 0.709f, 0.700f, 0.694f, 0.699f, 0.704f, 0.704f, 0.702f, 0.711f, 0.723f, 0.622f, 0.563f, 0.389f, 0.148f, -0.102f, -0.288f, -0.215f, 0.048f, 0.431f, 0.696f, 0.819f, 0.916f, 1.162f, 1.536f, 1.536f, 1.536f, 1.536f };
        static readonly float[] Xq1SXich1Y = { 0.216f, 0.258f, 0.313f, 0.382f, 0.463f, 0.554f, 0.810f, 1.033f, 1.166f, 1.174f, 1.055f, 0.918f, 0.777f, 0.767f, 1.166f, 1.155f, 0.998f, 0.803f, 0.767f, 1.183f, 1.078f, 0.850f, 0.764f, 0.886f, 0.887f, 0.763f, 0.638f, 0.691f, 0.978f, 1.000f, 0.532f, 0.428f, 0.347f, 0.319f, 0.325f, 0.330f, 0.332f, 0.324f, 0.319f, 0.347f, 0.354f, 0.331f, 0.322f, 0.343f, 0.355f, 0.333f, 0.270f, 0.248f, 0.271f, 0.266f, 0.251f, 0.270f, 0.312f, 0.328f, 0.313f, 0.315f, 0.344f, 0.354f, 0.328f, 0.310f, 0.330f, 0.351f, 0.334f, 0.311f, 0.323f, 0.351f, 0.347f, 0.322f, 0.324f, 0.353f, 0.356f, 0.327f, 0.314f, 0.335f, 0.349f, 0.330f, 0.311f, 0.328f, 0.353f, 0.345f, 0.323f, 0.302f, 0.202f, 0.047f, -0.027f, 0.000f, 0.092f, 0.051f, 0.055f, 0.037f, -0.132f, -0.256f, -0.191f, -0.004f, 0.112f, 0.112f, 0.112f, 0.112f };
        static readonly float[] Xq1SXich2X = { 0.267f, 0.324f, 0.383f, 0.441f, 0.493f, 0.534f, 0.545f, 0.423f, 0.176f, -0.149f, -0.476f, -0.679f, -0.603f, -0.353f, 0.176f, -0.234f, -0.602f, -0.650f, -0.353f, 0.080f, -0.433f, -0.685f, -0.362f, -0.309f, -0.566f, -0.723f, -0.554f, -0.356f, -0.279f, 0.799f, 0.449f, 0.515f, 0.676f, 0.807f, 0.819f, 0.828f, 0.829f, 0.831f, 0.834f, 0.834f, 0.834f, 0.837f, 0.837f, 0.824f, 0.811f, 0.804f, 0.794f, 0.784f, 0.783f, 0.787f, 0.794f, 0.804f, 0.815f, 0.828f, 0.836f, 0.837f, 0.835f, 0.832f, 0.832f, 0.831f, 0.829f, 0.827f, 0.828f, 0.830f, 0.831f, 0.831f, 0.834f, 0.837f, 0.838f, 0.834f, 0.823f, 0.815f, 0.806f, 0.797f, 0.790f, 0.792f, 0.796f, 0.800f, 0.806f, 0.818f, 0.832f, 0.626f, 0.575f, 0.440f, 0.232f, 0.009f, -0.166f, -0.225f, -0.085f, 0.355f, 0.799f, 0.927f, 0.846f, 1.032f, 1.562f, 1.562f, 1.562f, 1.562f };
        static readonly float[] Xq1SXich2Y = { 0.209f, 0.221f, 0.248f, 0.293f, 0.356f, 0.437f, 0.702f, 0.972f, 1.175f, 1.251f, 1.173f, 0.994f, 0.708f, 0.646f, 1.175f, 1.246f, 1.117f, 0.769f, 0.646f, 1.215f, 1.193f, 0.869f, 0.642f, 0.922f, 1.001f, 0.798f, 0.555f, 0.579f, 0.919f, 1.095f, 0.553f, 0.360f, 0.231f, 0.201f, 0.204f, 0.214f, 0.217f, 0.211f, 0.209f, 0.245f, 0.261f, 0.242f, 0.240f, 0.260f, 0.268f, 0.238f, 0.165f, 0.137f, 0.163f, 0.159f, 0.144f, 0.169f, 0.222f, 0.247f, 0.226f, 0.220f, 0.245f, 0.250f, 0.217f, 0.195f, 0.215f, 0.236f, 0.219f, 0.194f, 0.210f, 0.244f, 0.245f, 0.224f, 0.234f, 0.276f, 0.275f, 0.236f, 0.217f, 0.237f, 0.251f, 0.229f, 0.209f, 0.230f, 0.262f, 0.259f, 0.240f, 0.164f, 0.064f, -0.081f, -0.135f, -0.080f, 0.031f, -0.086f, 0.020f, 0.152f, -0.039f, -0.344f, -0.311f, 0.048f, 0.249f, 0.249f, 0.249f, 0.249f };
        static readonly float[] Xq1STayX = { 0.205f, 0.237f, 0.268f, 0.297f, 0.321f, 0.340f, 0.371f, 0.335f, 0.216f, 0.021f, -0.222f, -0.254f, -0.286f, -0.318f, 0.216f, -0.037f, -0.238f, -0.278f, -0.318f, 0.162f, -0.187f, -0.267f, -0.316f, -0.359f, -0.388f, -0.416f, -0.442f, -0.302f, 0.228f, 0.657f, 0.506f, 0.554f, 0.606f, 0.636f, 0.618f, 0.604f, 0.602f, 0.600f, 0.597f, 0.586f, 0.579f, 0.579f, 0.575f, 0.564f, 0.555f, 0.557f, 0.561f, 0.558f, 0.553f, 0.556f, 0.562f, 0.564f, 0.562f, 0.566f, 0.577f, 0.584f, 0.584f, 0.587f, 0.597f, 0.604f, 0.603f, 0.600f, 0.603f, 0.606f, 0.601f, 0.591f, 0.586f, 0.586f, 0.580f, 0.567f, 0.561f, 0.562f, 0.561f, 0.553f, 0.547f, 0.552f, 0.558f, 0.556f, 0.553f, 0.560f, 0.571f, 0.500f, 0.439f, 0.257f, 0.008f, -0.249f, -0.426f, -0.241f, -0.147f, -0.034f, 0.049f, 0.133f, 0.216f, 0.298f, 0.375f, 0.375f, 0.375f, 0.375f };
        static readonly float[] Xq1STayY = { 0.291f, 0.305f, 0.326f, 0.355f, 0.391f, 0.434f, 0.586f, 0.768f, 0.943f, 1.069f, 1.112f, 1.112f, 1.108f, 1.101f, 0.943f, 1.089f, 1.112f, 1.110f, 1.101f, 0.989f, 1.112f, 1.111f, 1.101f, 1.084f, 1.067f, 1.046f, 1.022f, 1.086f, 1.129f, 0.700f, 0.441f, 0.391f, 0.342f, 0.313f, 0.323f, 0.330f, 0.331f, 0.326f, 0.323f, 0.346f, 0.353f, 0.336f, 0.330f, 0.349f, 0.362f, 0.346f, 0.298f, 0.280f, 0.299f, 0.295f, 0.281f, 0.295f, 0.326f, 0.336f, 0.322f, 0.322f, 0.344f, 0.351f, 0.330f, 0.315f, 0.330f, 0.346f, 0.333f, 0.315f, 0.325f, 0.349f, 0.346f, 0.327f, 0.330f, 0.354f, 0.359f, 0.340f, 0.331f, 0.350f, 0.362f, 0.347f, 0.331f, 0.343f, 0.361f, 0.352f, 0.332f, 0.349f, 0.261f, 0.123f, 0.066f, 0.109f, 0.213f, 0.143f, 0.097f, 0.064f, 0.058f, 0.060f, 0.068f, 0.083f, 0.105f, 0.105f, 0.105f, 0.105f };
        static readonly float[] Xq1CMocX = { -0.094f, -0.044f, 0.020f, 0.095f, 0.178f, 0.260f, 0.439f, 0.508f, 0.422f, 0.192f, -0.124f, -0.670f, -0.953f, -0.467f, 0.066f, -0.237f, -0.977f, -1.007f, -0.203f, -0.493f, -0.394f, 0.025f, 0.052f, 0.190f, 0.380f, 0.465f, 0.817f, 1.172f, 1.259f, 1.228f, 1.145f, 1.014f, 0.846f, 0.656f, 0.719f, 0.641f, 0.471f, 0.278f, -0.063f, -0.437f, -0.021f, 0.995f, 1.337f, 0.735f, 0.586f, 1.573f };
        static readonly float[] Xq1CMocY = { 0.216f, 0.172f, 0.139f, 0.124f, 0.131f, 0.161f, 0.330f, 0.601f, 0.895f, 1.123f, 1.217f, 1.383f, 0.819f, 0.304f, 0.605f, 1.238f, 1.190f, 0.506f, 0.221f, 0.407f, 1.005f, 0.708f, 0.518f, 0.366f, 0.312f, -0.064f, -0.227f, -0.045f, 0.354f, 0.178f, 0.013f, -0.127f, -0.226f, -0.275f, -0.414f, -0.408f, -0.230f, 0.086f, -0.495f, -0.258f, 0.402f, 0.358f, -0.498f, -0.743f, 0.099f, 0.687f };
        static readonly byte[] Xq1CMocHien = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
        static readonly float[] Xq1CXich0X = { 0.484f, 0.522f, 0.547f, 0.555f, 0.547f, 0.522f, 0.403f, 0.204f, -0.037f, -0.275f, -0.467f, -0.476f, -0.482f, -0.484f, -0.483f, -0.479f, -0.472f, -0.462f, -0.449f, -0.176f, 0.249f, 0.705f, 0.739f, 0.776f, 0.814f, 0.801f, 0.788f, 0.774f, 0.760f, 0.749f, 0.738f, 0.726f, 0.715f, 0.702f, 0.555f, 0.299f, 0.010f, -0.231f, -0.106f, 0.099f, 0.365f, 0.565f, 0.785f, 1.019f, 1.261f, 1.506f };
        static readonly float[] Xq1CXich0Y = { 0.239f, 0.313f, 0.396f, 0.484f, 0.573f, 0.661f, 0.877f, 1.031f, 1.095f, 1.061f, 0.945f, 0.916f, 0.886f, 0.855f, 0.824f, 0.793f, 0.764f, 0.735f, 0.707f, 0.958f, 1.043f, 0.511f, 0.486f, 0.459f, 0.432f, 0.434f, 0.435f, 0.436f, 0.436f, 0.426f, 0.415f, 0.404f, 0.393f, 0.382f, 0.190f, 0.074f, 0.078f, 0.191f, 0.050f, -0.046f, -0.068f, -0.112f, -0.130f, -0.120f, -0.083f, -0.017f };
        static readonly float[] Xq1CXich1X = { 0.381f, 0.432f, 0.478f, 0.517f, 0.543f, 0.553f, 0.494f, 0.319f, 0.054f, -0.244f, -0.511f, -0.584f, -0.516f, -0.399f, -0.385f, -0.496f, -0.591f, -0.541f, -0.389f, -0.261f, 0.143f, 0.583f, 0.611f, 0.687f, 0.792f, 0.775f, 0.757f, 0.740f, 0.722f, 0.701f, 0.679f, 0.657f, 0.635f, 0.613f, 0.473f, 0.226f, -0.055f, -0.287f, -0.220f, 0.038f, 0.422f, 0.691f, 0.817f, 0.912f, 1.152f, 1.536f };
        static readonly float[] Xq1CXich1Y = { 0.216f, 0.258f, 0.313f, 0.382f, 0.463f, 0.554f, 0.810f, 1.033f, 1.166f, 1.174f, 1.055f, 0.918f, 0.777f, 0.767f, 0.859f, 0.903f, 0.812f, 0.670f, 0.620f, 0.880f, 1.122f, 0.565f, 0.461f, 0.369f, 0.317f, 0.323f, 0.329f, 0.335f, 0.341f, 0.331f, 0.322f, 0.313f, 0.306f, 0.300f, 0.104f, -0.015f, -0.013f, 0.099f, 0.051f, 0.055f, 0.041f, -0.127f, -0.255f, -0.196f, -0.009f, 0.112f };
        static readonly float[] Xq1CXich2X = { 0.267f, 0.324f, 0.383f, 0.441f, 0.493f, 0.534f, 0.545f, 0.423f, 0.176f, -0.149f, -0.476f, -0.679f, -0.603f, -0.353f, -0.267f, -0.473f, -0.704f, -0.642f, -0.339f, -0.341f, 0.010f, 0.454f, 0.480f, 0.616f, 0.804f, 0.815f, 0.827f, 0.835f, 0.835f, 0.796f, 0.752f, 0.705f, 0.655f, 0.604f, 0.508f, 0.300f, 0.051f, -0.160f, -0.224f, -0.093f, 0.341f, 0.789f, 0.928f, 0.846f, 1.021f, 1.562f };
        static readonly float[] Xq1CXich2Y = { 0.209f, 0.221f, 0.248f, 0.293f, 0.356f, 0.437f, 0.702f, 0.972f, 1.175f, 1.251f, 1.173f, 0.994f, 0.708f, 0.646f, 0.847f, 1.008f, 0.887f, 0.617f, 0.524f, 0.786f, 1.165f, 0.616f, 0.420f, 0.262f, 0.203f, 0.202f, 0.212f, 0.234f, 0.264f, 0.232f, 0.205f, 0.184f, 0.169f, 0.162f, -0.029f, -0.130f, -0.099f, 0.050f, -0.086f, 0.015f, 0.152f, -0.030f, -0.338f, -0.318f, 0.037f, 0.249f };
        static readonly float[] Xq1CTayX = { 0.205f, 0.237f, 0.268f, 0.297f, 0.321f, 0.340f, 0.371f, 0.335f, 0.216f, 0.021f, -0.222f, -0.254f, -0.286f, -0.318f, -0.349f, -0.379f, -0.407f, -0.434f, -0.458f, 0.053f, 0.541f, 0.490f, 0.538f, 0.589f, 0.642f, 0.624f, 0.606f, 0.588f, 0.569f, 0.554f, 0.538f, 0.523f, 0.508f, 0.494f, 0.344f, 0.088f, -0.201f, -0.440f, -0.244f, -0.150f, -0.037f, 0.047f, 0.131f, 0.214f, 0.296f, 0.375f };
        static readonly float[] Xq1CTayY = { 0.291f, 0.305f, 0.326f, 0.355f, 0.391f, 0.434f, 0.586f, 0.768f, 0.943f, 1.069f, 1.112f, 1.112f, 1.108f, 1.101f, 1.089f, 1.073f, 1.054f, 1.030f, 1.003f, 1.151f, 0.981f, 0.458f, 0.407f, 0.358f, 0.310f, 0.320f, 0.329f, 0.337f, 0.345f, 0.347f, 0.348f, 0.348f, 0.349f, 0.349f, 0.173f, 0.073f, 0.093f, 0.221f, 0.145f, 0.099f, 0.065f, 0.059f, 0.059f, 0.068f, 0.083f, 0.105f };
        // quy_xich: chiều cao khai 664.6; skill 3.232 s, trúng 1.732; cast 1.500 s, trúng 0.895
        static readonly float[] Xq2SMocX = { -0.106f, -0.058f, 0.005f, 0.080f, 0.162f, 0.245f, 0.426f, 0.499f, 0.420f, 0.197f, -0.113f, -0.658f, -0.958f, -0.478f, 0.420f, 0.124f, -0.350f, -0.956f, -0.478f, 0.365f, -0.068f, -0.866f, -0.506f, 0.081f, -0.477f, -1.111f, -0.805f, -0.302f, -0.548f, 0.944f, 0.009f, 0.076f, 0.240f, 0.355f, 0.545f, 0.856f, 0.897f, 0.963f, 1.050f, 1.155f, 1.233f, 1.275f, 1.279f, 1.266f, 1.256f, 1.248f, 1.230f, 1.213f, 1.215f, 1.219f, 1.229f, 1.246f, 1.260f, 1.268f, 1.281f, 1.256f, 1.199f, 1.115f, 1.012f, 0.921f, 0.874f, 0.859f, 0.858f, 0.887f, 0.962f, 1.064f, 1.155f, 1.227f, 1.275f, 1.273f, 1.264f, 1.260f, 1.249f, 1.239f, 1.232f, 1.231f, 1.234f, 1.243f, 1.251f, 1.262f, 1.273f, 0.731f, 0.698f, 0.703f, 0.604f, 0.446f, 0.286f, -0.083f, -0.454f, -0.001f, 1.033f, 1.333f, 0.702f, 0.588f, 1.578f, 1.578f, 1.578f, 1.578f };
        static readonly float[] Xq2SMocY = { 0.225f, 0.179f, 0.144f, 0.127f, 0.131f, 0.159f, 0.321f, 0.587f, 0.879f, 1.107f, 1.204f, 1.389f, 0.829f, 0.299f, 0.879f, 1.145f, 1.392f, 1.011f, 0.299f, 0.960f, 1.200f, 1.227f, 0.306f, 0.819f, 1.329f, 1.001f, 0.318f, 0.212f, 0.577f, 1.516f, 0.657f, 0.471f, 0.348f, 0.191f, -0.157f, -0.237f, -0.229f, -0.221f, -0.186f, -0.068f, 0.058f, 0.157f, 0.289f, 0.307f, 0.281f, 0.203f, 0.068f, 0.014f, 0.050f, 0.051f, 0.047f, 0.112f, 0.228f, 0.306f, 0.207f, 0.065f, -0.016f, -0.099f, -0.196f, -0.247f, -0.234f, -0.214f, -0.232f, -0.253f, -0.221f, -0.141f, -0.068f, 0.004f, 0.146f, 0.342f, 0.329f, 0.233f, 0.171f, 0.179f, 0.187f, 0.150f, 0.127f, 0.178f, 0.254f, 0.284f, 0.296f, -0.275f, -0.370f, -0.447f, -0.390f, -0.194f, 0.015f, -0.514f, -0.240f, 0.431f, 0.345f, -0.533f, -0.738f, 0.139f, 0.698f, 0.698f, 0.698f, 0.698f };
        static readonly byte[] Xq2SMocHien = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
        static readonly float[] Xq2SXich0X = { 0.482f, 0.521f, 0.545f, 0.553f, 0.545f, 0.521f, 0.402f, 0.203f, -0.037f, -0.274f, -0.466f, -0.475f, -0.481f, -0.483f, -0.037f, -0.327f, -0.471f, -0.480f, -0.483f, -0.113f, -0.443f, -0.478f, -0.483f, -0.481f, -0.476f, -0.468f, -0.457f, -0.379f, -0.048f, 0.579f, 0.714f, 0.749f, 0.786f, 0.807f, 0.795f, 0.784f, 0.782f, 0.783f, 0.782f, 0.769f, 0.762f, 0.766f, 0.765f, 0.753f, 0.744f, 0.749f, 0.760f, 0.759f, 0.753f, 0.755f, 0.762f, 0.762f, 0.755f, 0.756f, 0.767f, 0.772f, 0.768f, 0.768f, 0.780f, 0.788f, 0.783f, 0.777f, 0.783f, 0.789f, 0.783f, 0.771f, 0.769f, 0.773f, 0.768f, 0.754f, 0.748f, 0.754f, 0.755f, 0.745f, 0.739f, 0.746f, 0.753f, 0.749f, 0.743f, 0.750f, 0.762f, 0.706f, 0.647f, 0.467f, 0.219f, -0.038f, -0.224f, -0.101f, 0.106f, 0.369f, 0.570f, 0.790f, 1.023f, 1.265f, 1.501f, 1.501f, 1.501f, 1.501f };
        static readonly float[] Xq2SXich0Y = { 0.238f, 0.313f, 0.395f, 0.483f, 0.572f, 0.659f, 0.875f, 1.028f, 1.092f, 1.058f, 0.943f, 0.913f, 0.883f, 0.852f, 1.092f, 1.036f, 0.928f, 0.891f, 0.852f, 1.091f, 0.963f, 0.901f, 0.854f, 0.812f, 0.781f, 0.752f, 0.723f, 0.796f, 1.008f, 0.934f, 0.502f, 0.476f, 0.448f, 0.431f, 0.433f, 0.434f, 0.435f, 0.426f, 0.419f, 0.447f, 0.453f, 0.426f, 0.414f, 0.436f, 0.449f, 0.426f, 0.360f, 0.335f, 0.360f, 0.355f, 0.339f, 0.360f, 0.404f, 0.421f, 0.406f, 0.410f, 0.442f, 0.455f, 0.430f, 0.413f, 0.434f, 0.455f, 0.438f, 0.413f, 0.425f, 0.453f, 0.447f, 0.419f, 0.419f, 0.447f, 0.450f, 0.420f, 0.407f, 0.429f, 0.444f, 0.423f, 0.403f, 0.421f, 0.447f, 0.439f, 0.415f, 0.385f, 0.285f, 0.134f, 0.063f, 0.091f, 0.179f, 0.047f, -0.048f, -0.070f, -0.113f, -0.130f, -0.119f, -0.081f, -0.017f, -0.017f, -0.017f, -0.017f };
        static readonly float[] Xq2SXich1X = { 0.379f, 0.430f, 0.477f, 0.515f, 0.541f, 0.552f, 0.493f, 0.318f, 0.054f, -0.244f, -0.509f, -0.583f, -0.514f, -0.397f, 0.054f, -0.315f, -0.562f, -0.542f, -0.397f, -0.038f, -0.476f, -0.570f, -0.401f, -0.412f, -0.536f, -0.591f, -0.493f, -0.365f, -0.164f, 0.694f, 0.585f, 0.629f, 0.718f, 0.784f, 0.767f, 0.753f, 0.751f, 0.750f, 0.747f, 0.736f, 0.729f, 0.729f, 0.725f, 0.713f, 0.703f, 0.703f, 0.705f, 0.700f, 0.696f, 0.699f, 0.705f, 0.709f, 0.710f, 0.716f, 0.727f, 0.734f, 0.734f, 0.737f, 0.747f, 0.754f, 0.752f, 0.749f, 0.752f, 0.755f, 0.750f, 0.740f, 0.736f, 0.736f, 0.730f, 0.718f, 0.710f, 0.710f, 0.707f, 0.698f, 0.692f, 0.697f, 0.702f, 0.702f, 0.700f, 0.709f, 0.721f, 0.620f, 0.561f, 0.388f, 0.148f, -0.101f, -0.287f, -0.214f, 0.048f, 0.430f, 0.694f, 0.817f, 0.914f, 1.158f, 1.531f, 1.531f, 1.531f, 1.531f };
        static readonly float[] Xq2SXich1Y = { 0.216f, 0.257f, 0.312f, 0.381f, 0.462f, 0.552f, 0.808f, 1.030f, 1.163f, 1.170f, 1.052f, 0.915f, 0.775f, 0.765f, 1.163f, 1.152f, 0.995f, 0.801f, 0.765f, 1.179f, 1.075f, 0.848f, 0.762f, 0.884f, 0.885f, 0.761f, 0.636f, 0.689f, 0.975f, 0.998f, 0.530f, 0.427f, 0.346f, 0.318f, 0.324f, 0.329f, 0.331f, 0.323f, 0.318f, 0.346f, 0.353f, 0.330f, 0.321f, 0.342f, 0.354f, 0.332f, 0.270f, 0.247f, 0.270f, 0.265f, 0.250f, 0.269f, 0.311f, 0.327f, 0.312f, 0.314f, 0.343f, 0.353f, 0.327f, 0.310f, 0.329f, 0.350f, 0.333f, 0.310f, 0.322f, 0.350f, 0.346f, 0.321f, 0.323f, 0.352f, 0.355f, 0.326f, 0.313f, 0.334f, 0.348f, 0.329f, 0.310f, 0.327f, 0.352f, 0.344f, 0.322f, 0.302f, 0.201f, 0.047f, -0.027f, 0.000f, 0.091f, 0.050f, 0.055f, 0.037f, -0.132f, -0.255f, -0.191f, -0.004f, 0.111f, 0.111f, 0.111f, 0.111f };
        static readonly float[] Xq2SXich2X = { 0.267f, 0.323f, 0.382f, 0.440f, 0.492f, 0.532f, 0.543f, 0.422f, 0.175f, -0.149f, -0.475f, -0.677f, -0.602f, -0.352f, 0.175f, -0.233f, -0.600f, -0.648f, -0.352f, 0.080f, -0.432f, -0.683f, -0.361f, -0.308f, -0.564f, -0.721f, -0.552f, -0.355f, -0.278f, 0.797f, 0.448f, 0.513f, 0.675f, 0.805f, 0.817f, 0.826f, 0.827f, 0.829f, 0.831f, 0.831f, 0.832f, 0.835f, 0.835f, 0.822f, 0.809f, 0.802f, 0.792f, 0.782f, 0.781f, 0.784f, 0.791f, 0.802f, 0.813f, 0.825f, 0.834f, 0.835f, 0.832f, 0.830f, 0.830f, 0.829f, 0.826f, 0.824f, 0.826f, 0.828f, 0.829f, 0.829f, 0.831f, 0.835f, 0.835f, 0.831f, 0.820f, 0.812f, 0.804f, 0.794f, 0.788f, 0.790f, 0.794f, 0.798f, 0.804f, 0.815f, 0.830f, 0.624f, 0.573f, 0.438f, 0.232f, 0.009f, -0.165f, -0.224f, -0.085f, 0.354f, 0.797f, 0.924f, 0.843f, 1.030f, 1.557f, 1.557f, 1.557f, 1.557f };
        static readonly float[] Xq2SXich2Y = { 0.208f, 0.220f, 0.247f, 0.292f, 0.355f, 0.435f, 0.700f, 0.969f, 1.172f, 1.247f, 1.170f, 0.991f, 0.706f, 0.644f, 1.172f, 1.242f, 1.114f, 0.767f, 0.644f, 1.211f, 1.190f, 0.866f, 0.641f, 0.920f, 0.998f, 0.796f, 0.553f, 0.578f, 0.917f, 1.091f, 0.551f, 0.359f, 0.230f, 0.201f, 0.203f, 0.214f, 0.216f, 0.210f, 0.208f, 0.245f, 0.260f, 0.241f, 0.240f, 0.259f, 0.267f, 0.237f, 0.164f, 0.137f, 0.163f, 0.158f, 0.144f, 0.169f, 0.221f, 0.246f, 0.226f, 0.219f, 0.244f, 0.249f, 0.217f, 0.194f, 0.214f, 0.236f, 0.218f, 0.194f, 0.210f, 0.244f, 0.245f, 0.223f, 0.233f, 0.275f, 0.274f, 0.236f, 0.216f, 0.237f, 0.251f, 0.228f, 0.208f, 0.230f, 0.262f, 0.258f, 0.240f, 0.163f, 0.064f, -0.081f, -0.135f, -0.080f, 0.031f, -0.086f, 0.020f, 0.152f, -0.039f, -0.343f, -0.310f, 0.048f, 0.248f, 0.248f, 0.248f, 0.248f };
        static readonly float[] Xq2STayX = { 0.157f, 0.192f, 0.228f, 0.263f, 0.295f, 0.323f, 0.382f, 0.369f, 0.263f, 0.066f, -0.191f, -0.228f, -0.265f, -0.302f, 0.263f, 0.006f, -0.210f, -0.256f, -0.302f, 0.211f, -0.153f, -0.243f, -0.300f, -0.350f, -0.385f, -0.419f, -0.451f, -0.301f, 0.264f, 0.688f, 0.457f, 0.509f, 0.564f, 0.597f, 0.578f, 0.563f, 0.561f, 0.559f, 0.555f, 0.545f, 0.537f, 0.536f, 0.531f, 0.521f, 0.512f, 0.513f, 0.515f, 0.511f, 0.507f, 0.510f, 0.516f, 0.518f, 0.518f, 0.522f, 0.533f, 0.541f, 0.542f, 0.546f, 0.556f, 0.563f, 0.562f, 0.560f, 0.562f, 0.564f, 0.559f, 0.550f, 0.545f, 0.544f, 0.537f, 0.525f, 0.518f, 0.518f, 0.517f, 0.509f, 0.503f, 0.508f, 0.513f, 0.512f, 0.510f, 0.517f, 0.527f, 0.452f, 0.391f, 0.208f, -0.040f, -0.297f, -0.473f, -0.275f, -0.182f, -0.066f, 0.021f, 0.109f, 0.196f, 0.282f, 0.364f, 0.364f, 0.364f, 0.364f };
        static readonly float[] Xq2STayY = { 0.280f, 0.284f, 0.297f, 0.318f, 0.348f, 0.386f, 0.537f, 0.732f, 0.930f, 1.083f, 1.147f, 1.151f, 1.150f, 1.144f, 0.930f, 1.109f, 1.150f, 1.150f, 1.144f, 0.985f, 1.145f, 1.151f, 1.144f, 1.129f, 1.113f, 1.092f, 1.067f, 1.132f, 1.158f, 0.661f, 0.426f, 0.368f, 0.312f, 0.280f, 0.291f, 0.299f, 0.301f, 0.296f, 0.294f, 0.317f, 0.324f, 0.308f, 0.303f, 0.322f, 0.334f, 0.321f, 0.276f, 0.260f, 0.278f, 0.274f, 0.261f, 0.273f, 0.301f, 0.310f, 0.296f, 0.295f, 0.315f, 0.321f, 0.300f, 0.286f, 0.300f, 0.315f, 0.303f, 0.285f, 0.296f, 0.318f, 0.317f, 0.299f, 0.303f, 0.326f, 0.332f, 0.314f, 0.307f, 0.324f, 0.336f, 0.322f, 0.307f, 0.318f, 0.334f, 0.326f, 0.306f, 0.332f, 0.247f, 0.113f, 0.059f, 0.105f, 0.211f, 0.132f, 0.074f, 0.027f, 0.018f, 0.017f, 0.023f, 0.036f, 0.056f, 0.056f, 0.056f, 0.056f };
        static readonly float[] Xq2CMocX = { -0.106f, -0.058f, 0.005f, 0.080f, 0.162f, 0.245f, 0.426f, 0.499f, 0.420f, 0.197f, -0.113f, -0.658f, -0.958f, -0.478f, 0.071f, -0.222f, -0.975f, -1.020f, -0.208f, -0.503f, -0.409f, 0.014f, 0.041f, 0.179f, 0.370f, 0.447f, 0.805f, 1.173f, 1.271f, 1.237f, 1.149f, 1.014f, 0.841f, 0.647f, 0.715f, 0.643f, 0.479f, 0.291f, -0.067f, -0.452f, -0.026f, 1.007f, 1.342f, 0.720f, 0.573f, 1.578f };
        static readonly float[] Xq2CMocY = { 0.225f, 0.179f, 0.144f, 0.127f, 0.131f, 0.159f, 0.321f, 0.587f, 0.879f, 1.107f, 1.204f, 1.389f, 0.829f, 0.299f, 0.589f, 1.234f, 1.199f, 0.508f, 0.210f, 0.399f, 1.005f, 0.718f, 0.529f, 0.377f, 0.324f, -0.064f, -0.239f, -0.061f, 0.348f, 0.168f, -0.001f, -0.142f, -0.241f, -0.288f, -0.429f, -0.423f, -0.242f, 0.077f, -0.509f, -0.258f, 0.416f, 0.364f, -0.510f, -0.751f, 0.110f, 0.698f };
        static readonly byte[] Xq2CMocHien = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
        static readonly float[] Xq2CXich0X = { 0.482f, 0.521f, 0.545f, 0.553f, 0.545f, 0.521f, 0.402f, 0.203f, -0.037f, -0.274f, -0.466f, -0.475f, -0.481f, -0.483f, -0.482f, -0.478f, -0.471f, -0.461f, -0.448f, -0.176f, 0.248f, 0.703f, 0.737f, 0.773f, 0.811f, 0.799f, 0.786f, 0.772f, 0.757f, 0.747f, 0.736f, 0.724f, 0.713f, 0.700f, 0.553f, 0.298f, 0.010f, -0.230f, -0.106f, 0.099f, 0.364f, 0.564f, 0.783f, 1.016f, 1.258f, 1.501f };
        static readonly float[] Xq2CXich0Y = { 0.238f, 0.313f, 0.395f, 0.483f, 0.572f, 0.659f, 0.875f, 1.028f, 1.092f, 1.058f, 0.943f, 0.913f, 0.883f, 0.852f, 0.822f, 0.791f, 0.761f, 0.732f, 0.705f, 0.955f, 1.040f, 0.510f, 0.484f, 0.457f, 0.431f, 0.433f, 0.434f, 0.434f, 0.434f, 0.424f, 0.414f, 0.403f, 0.392f, 0.381f, 0.189f, 0.074f, 0.078f, 0.190f, 0.050f, -0.046f, -0.068f, -0.112f, -0.129f, -0.120f, -0.083f, -0.017f };
        static readonly float[] Xq2CXich1X = { 0.379f, 0.430f, 0.477f, 0.515f, 0.541f, 0.552f, 0.493f, 0.318f, 0.054f, -0.244f, -0.509f, -0.583f, -0.514f, -0.397f, -0.384f, -0.495f, -0.589f, -0.539f, -0.388f, -0.260f, 0.142f, 0.582f, 0.609f, 0.685f, 0.790f, 0.773f, 0.755f, 0.737f, 0.719f, 0.699f, 0.677f, 0.655f, 0.633f, 0.611f, 0.472f, 0.225f, -0.055f, -0.286f, -0.219f, 0.038f, 0.420f, 0.689f, 0.814f, 0.909f, 1.149f, 1.531f };
        static readonly float[] Xq2CXich1Y = { 0.216f, 0.257f, 0.312f, 0.381f, 0.462f, 0.552f, 0.808f, 1.030f, 1.163f, 1.170f, 1.052f, 0.915f, 0.775f, 0.765f, 0.857f, 0.900f, 0.810f, 0.668f, 0.618f, 0.877f, 1.119f, 0.563f, 0.460f, 0.368f, 0.316f, 0.322f, 0.328f, 0.334f, 0.340f, 0.330f, 0.321f, 0.312f, 0.305f, 0.299f, 0.104f, -0.015f, -0.013f, 0.099f, 0.051f, 0.055f, 0.040f, -0.126f, -0.254f, -0.195f, -0.009f, 0.111f };
        static readonly float[] Xq2CXich2X = { 0.267f, 0.323f, 0.382f, 0.440f, 0.492f, 0.532f, 0.543f, 0.422f, 0.175f, -0.149f, -0.475f, -0.677f, -0.602f, -0.352f, -0.266f, -0.471f, -0.702f, -0.640f, -0.338f, -0.340f, 0.010f, 0.453f, 0.479f, 0.615f, 0.802f, 0.813f, 0.825f, 0.833f, 0.832f, 0.794f, 0.750f, 0.703f, 0.653f, 0.602f, 0.506f, 0.300f, 0.051f, -0.160f, -0.224f, -0.093f, 0.340f, 0.787f, 0.925f, 0.844f, 1.018f, 1.557f };
        static readonly float[] Xq2CXich2Y = { 0.208f, 0.220f, 0.247f, 0.292f, 0.355f, 0.435f, 0.700f, 0.969f, 1.172f, 1.247f, 1.170f, 0.991f, 0.706f, 0.644f, 0.845f, 1.005f, 0.884f, 0.615f, 0.523f, 0.784f, 1.161f, 0.614f, 0.419f, 0.262f, 0.203f, 0.201f, 0.212f, 0.233f, 0.263f, 0.231f, 0.204f, 0.183f, 0.169f, 0.161f, -0.029f, -0.130f, -0.099f, 0.050f, -0.086f, 0.015f, 0.152f, -0.030f, -0.337f, -0.317f, 0.037f, 0.248f };
        static readonly float[] Xq2CTayX = { 0.157f, 0.192f, 0.228f, 0.263f, 0.295f, 0.323f, 0.382f, 0.369f, 0.263f, 0.066f, -0.191f, -0.228f, -0.265f, -0.302f, -0.338f, -0.374f, -0.408f, -0.440f, -0.470f, 0.080f, 0.588f, 0.441f, 0.492f, 0.546f, 0.603f, 0.584f, 0.565f, 0.546f, 0.526f, 0.509f, 0.493f, 0.477f, 0.461f, 0.446f, 0.296f, 0.040f, -0.249f, -0.487f, -0.277f, -0.185f, -0.069f, 0.018f, 0.106f, 0.194f, 0.280f, 0.364f };
        static readonly float[] Xq2CTayY = { 0.280f, 0.284f, 0.297f, 0.318f, 0.348f, 0.386f, 0.537f, 0.732f, 0.930f, 1.083f, 1.147f, 1.151f, 1.150f, 1.144f, 1.134f, 1.119f, 1.099f, 1.076f, 1.047f, 1.189f, 0.985f, 0.445f, 0.387f, 0.330f, 0.277f, 0.287f, 0.298f, 0.308f, 0.318f, 0.321f, 0.325f, 0.328f, 0.331f, 0.334f, 0.162f, 0.065f, 0.088f, 0.220f, 0.134f, 0.075f, 0.028f, 0.018f, 0.017f, 0.023f, 0.036f, 0.056f };

        sealed class XqBang
        {
            public float[] mx, my, ax, ay, bx, by, cx, cy, tx, ty;
            public byte[] mh;
        }

        static XqBang XqLay(int dang, bool chieu) =>
            dang == 1 ? (chieu ? new XqBang { mx = Xq1SMocX, my = Xq1SMocY, mh = Xq1SMocHien, ax = Xq1SXich0X, ay = Xq1SXich0Y, bx = Xq1SXich1X, by = Xq1SXich1Y, cx = Xq1SXich2X, cy = Xq1SXich2Y, tx = Xq1STayX, ty = Xq1STayY }
                              : new XqBang { mx = Xq1CMocX, my = Xq1CMocY, mh = Xq1CMocHien, ax = Xq1CXich0X, ay = Xq1CXich0Y, bx = Xq1CXich1X, by = Xq1CXich1Y, cx = Xq1CXich2X, cy = Xq1CXich2Y, tx = Xq1CTayX, ty = Xq1CTayY })
                      : (chieu ? new XqBang { mx = Xq2SMocX, my = Xq2SMocY, mh = Xq2SMocHien, ax = Xq2SXich0X, ay = Xq2SXich0Y, bx = Xq2SXich1X, by = Xq2SXich1Y, cx = Xq2SXich2X, cy = Xq2SXich2Y, tx = Xq2STayX, ty = Xq2STayY }
                              : new XqBang { mx = Xq2CMocX, my = Xq2CMocY, mh = Xq2CMocHien, ax = Xq2CXich0X, ay = Xq2CXich0Y, bx = Xq2CXich1X, by = Xq2CXich1Y, cx = Xq2CXich2X, cy = Xq2CXich2Y, tx = Xq2CTayX, ty = Xq2CTayY });

        static Vector2 XqMau(float[] xs, float[] ys, float t)
        {
            float f = Mathf.Max(0, t) / XqDt;
            int i = Mathf.Clamp((int)f, 0, xs.Length - 1), j = Mathf.Min(i + 1, xs.Length - 1);
            float w = Mathf.Clamp01(f - i);
            return new Vector2(Mathf.Lerp(xs[i], xs[j], w), Mathf.Lerp(ys[i], ys[j], w));
        }

        static bool XqHien(byte[] h, float t) => h[Mathf.Clamp(Mathf.RoundToInt(Mathf.Max(0, t) / XqDt), 0, h.Length - 1)] != 0;

        // ảnh mắt xích của rig (AolaImport nhập tên có "_tt_" thành sprite: Resources/quy_xich_2/quy_xich_2_tt_xich_<i>.png), nạp một lần
        static readonly Dictionary<string, Sprite> xqAnh = new Dictionary<string, Sprite>();

        static Sprite XqXich(int i)
        {
            string key = "quy_xich_2_tt_xich_" + i;
            if (xqAnh.TryGetValue(key, out var s) && s) return s;
            s = PokiClash.Game.ContentPacks.Get<Sprite>(key); // tướng trong gói tải sau (GD_Claude/27)
            if (!s) s = Resources.Load<Sprite>("quy_xich_2/" + key);
            xqAnh[key] = s;
            return s;
        }

        // một lưỡi lửa của vệt móc quay: bay chậm theo móc rồi tụt lại, ngọn ngả ngược hướng bay
        void XqVet(Vector2 p, Vector2 v, float manh, int g)
        {
            var q = Flame(p + U2(-4, 4), v * 0.12f + new Vector2(U(-30, 30), -U(40, 120)), U(0.22f, 0.34f), U(8, 11) * manh, U(18, 26) * manh, "tron",
                Th.pal, g, 3f, -260, 1.7f, 0.04f, 0.05f);   // khói của vệt nay là cụm liền riêng (NXichLua), lưỡi lửa ít nhả khói lẻ
            Tongue(q, -1, 0.45f);
            q.smokeGroup = Back;
        }

        // lưỡi lửa nhỏ liếm lên (dọc xích, quanh vòng trói)
        void XqLiem(Vector2 p, float manh, int g, float r = 1)
        {
            var q = Flame(p + U2(-3, 3), new Vector2(U(-25, 25), -U(70, 150)), U(0.18f, 0.28f), 5 * manh * r, U(10, 15) * manh * r, "tron", Th.pal, g, 3f,
                -300, 1.6f, 0.06f, 0.06f);
            Tongue(q, 1, 0.6f);
            q.smokeGroup = Back;
        }

        // ĐÒN THƯỜNG: tướng bay tới, móc gõ đỉnh đầu đối thủ rồi đập xuống. lead: giây từ đầu clip attack tới lúc móc chạm đầu.
        public float NXichGo(Vector2 casterFeet, Vector2 foeFeet, Vector2 foeBody, float tH, float lead)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.02f, lead), k = t0 / XqALead;
            var dau = foeBody + new Vector2(-dir * 0.06f * tH, -0.34f * tH);
            At(t0, () =>
            {
                Shake?.Invoke(0.3f);
                SatChop(dau, 0.42f * tH, Front, 0.14f);
                for (int i = 0; i < 8; i++)
                    Spark(dau, new Vector2(dir * U(-0.3f, 0.9f), U(-0.9f, 0.6f)), U(240, 440), U(0.16f, 0.28f), U(6, 9), 500);
                for (int i = 0; i < 4; i++)
                    GiaoDam(dau + U2(-5, 5), new Vector2(dir * U(-0.2f, 0.9f), -U(0.2f, 1f)) * U(160, 320), U(10, 15));
            });
            At(t0 + 0.05f * k, () =>
            {
                for (int i = 0; i < 4; i++)
                {
                    float sd = (i & 1) == 0 ? 1 : -1;
                    Bui(foeFeet + new Vector2(sd * U(6, 0.3f * tH), U(-5, 2)), new Vector2(sd * U(100, 240), -U(10, 50)), 0, 4, 11, Back);
                }
            });
            return t0;
        }

        // CHIÊU MANA: quay xích qua đầu rồi ném móc (móc + xích là mảnh của rig, game lái). dang: 1 / 2; manh: 0,85 dạng 1, 1 dạng 2.
        public float NXichNem(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang, float manh)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.3f, lead), k = t0 / XqCLead, T0 = T;
            var B = XqLay(dang, false);
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            float Tc() => (T - T0) / k;
            Vector2 Moc(float tc) => San(XqMau(B.mx, B.my, tc));
            // vệt gió kim loại theo đúng đường móc quay
            Every(XqCQuay * k, XqCNem * k, 34, x =>
            {
                float tc = Tc();
                if (!XqHien(B.mh, tc)) return;
                var v = (Moc(tc + XqDt) - Moc(tc - XqDt)) / (2 * XqDt * k);
                if (v.sqrMagnitude < 100) return;
                var p = Spark(Moc(tc), -v, U(60, 140), U(0.1f, 0.16f), U(6, 9) * manh, 0, Back, 6);
                p.col = XqGio;
            });
            At(XqCNem * k, () =>
            {
                var a = San(XqMau(B.tx, B.ty, XqCNem));
                for (int i = 0; i < 6; i++) Spark(a, new Vector2(dir * U(0.4f, 1f), U(-0.5f, 0.3f)), U(220, 420), U(0.12f, 0.22f), U(5, 8), 100);
                Bui(casterFeet + new Vector2(-dir * U(4, 0.12f * casterH), U(-4, 2)), new Vector2(-dir * U(80, 180), -U(10, 40)), 0, 4, 10, Back);
            });
            var c = foeBody + new Vector2(-dir * 0.05f * tH, 0);
            At(t0, () =>
            {
                Shake?.Invoke(0.3f * manh);
                GiaoTrung(c, new Vector2(dir, 0), tH, 1.1f * manh, 9, 6);
                Ring(c, 0.34f, 0.06f * tH, 0.55f * tH * manh, XqThep, 0.5f, Front, 32);
                for (int i = 0; i < 3; i++) Bui(foeFeet + new Vector2(U(-0.3f, 0.3f) * tH, U(-4, 2)), new Vector2(U(-120, 120), -U(10, 60)), 0, 4, 11, Back);
            });
            At(XqCRut * k, () =>
            {
                for (int i = 0; i < 6; i++) Spark(c, new Vector2(-dir * U(0.3f, 1f), U(-0.6f, 0.3f)), U(200, 380), U(0.12f, 0.22f), U(5, 8), 300);
                for (int i = 0; i < 3; i++) GiaoDam(c + U2(-5, 5), new Vector2(-dir * U(0.2f, 0.8f), -U(0.3f, 1f)) * U(140, 280), U(9, 13));
            });
            At(XqCVe * k, () =>
            {
                var a = San(XqMau(B.tx, B.ty, XqCVe));
                SatChop(a, 0.16f * casterH * manh, Front, 0.12f);
            });
            return t0;
        }

        // CHIÊU CUỐI: xích lửa quay, ném, trói, cột lửa thiêu. dang: 1 / 2; manh: 0,8 dạng 1, 1 dạng 2. Trả giây tới nhịp đốt đầu (= lead).
        public float NXichLua(Vector2 casterFeet, float casterH, Vector2 foeFeet, Vector2 foeBody, float tH, float lead, int dang, float manh)
        {
            float dir = foeFeet.x >= casterFeet.x ? 1 : -1;
            float t0 = Mathf.Max(0.3f, lead), k = t0 / XqSLead, T0 = T;
            var B = XqLay(dang, true);
            Vector2 San(Vector2 v) => casterFeet + new Vector2(dir * v.x * casterH, -v.y * casterH);
            float Tc() => (T - T0) / k;
            Vector2 Moc(float tc) => San(XqMau(B.mx, B.my, tc));
            Vector2 Tay(float tc) => San(XqMau(B.tx, B.ty, tc));
            Vector2 VMoc(float tc) => (Moc(tc + XqDt) - Moc(tc - XqDt)) / (2 * XqDt * k);
            var dich = foeBody;

            // 1. móc bốc lửa: chớp nhỏ, lưỡi lửa bùng
            At(XqSLua * k, () =>
            {
                var m = Moc(XqSLua);
                KmChop(m, 0.16f * casterH * manh, 0.06f, KmLua, Back);
                for (int i = 0; i < 6; i++) XqLiem(m, manh, Back, 1.4f);
            });
            // 2. quay (2026-11-18: người dùng chê khói, lửa rải rác, chưa thành cụm): vệt lửa + KHÓI CỤM LIỀN chia theo QUÃNG đường móc quay (KR5),
            // không theo giờ nữa nên vệt liền dù móc quay nhanh; khói than đáy còn ánh lửa, bay lên, ngả xám rồi mờ
            float dQuay = (XqSNem - XqSLua) * k;
            int demQ = 0;
            // khung vẽ sẵn (2026-11-19, người dùng: "các fireball ... nên thêm trail smoke vào"): có khung "khoi" thì vệt khói đuôi theo móc lửa
            // (KmDuoiKhoi, HatFbKim.cs; cụm 0,24 thân, 22 cụm/giây, sau tướng dưới lưỡi lửa) thay chuỗi khói một múi, không để cả hai
            bool fbKhoi = HasFb("khoi");
            if (fbKhoi) At(XqSLua * k, () => KmDuoiKhoi(t => Moc((t - T0) / k), dQuay, 0.24f * casterH * manh, 0.04f * casterH, 22, Back));
            At(XqSLua * k, () => KmDuoi(t => Moc((t - T0) / k), dQuay, 0.12f * casterH, (pt, ud) =>
            {
                float tc = Tc();
                if (!XqHien(B.mh, tc)) return;
                float x = Mathf.Clamp01((tc - XqSLua) / (XqSNem - XqSLua));
                XqVet(pt, VMoc(tc), manh * (0.85f + 0.3f * x), Back);
                if (!fbKhoi && demQ++ % 2 == 0)
                    KmKhoi(pt + U2(-3, 3), new Vector2(U(-15, 15), -U(40, 80)), U(0.1f, 0.12f) * casterH * manh, U(0.55f, 0.8f), Back, 0.8f, 0, null, 0.2f,
                        demQ % 8 != 1);
            }));
            Every(XqSLua * k, XqSNem * k, 40 * manh, x =>
            {
                float tc = Tc();
                if (!XqHien(B.mh, tc)) return;
                int j = rng.Next(3);
                var v = j == 0 ? XqMau(B.ax, B.ay, tc) : j == 1 ? XqMau(B.bx, B.by, tc) : XqMau(B.cx, B.cy, tc);
                XqLiem(San(v), manh, Back);
            });
            // 3. ném: lửa chạy dọc xích từ tay tới đối thủ, đầu xích (móc) cháy to
            Every(XqSNem * k, XqSTroi * k, 90 * manh, x =>
            {
                float tc = Tc();
                float q = EaseOut(Mathf.Clamp01((tc - XqSNem) / (XqSTroi - XqSNem)));
                var a = Tay(tc);
                var dau = Vector2.Lerp(a, dich, q);
                if (U(0, 1) < 0.4f) XqVet(dau, (dich - a) * 4f, manh, Front);
                else XqLiem(Vector2.Lerp(a, dau, U(0.05f, 1f)), manh, Front);
            });
            // 4. trói: vòng xích quấn thân đối thủ, lửa liếm vòng, xích căng cháy
            At(XqSTroi * k, () =>
            {
                Shake?.Invoke(0.4f * manh);
                KmNhip(0.8f);   // trói: nhịp trúng phụ trước cú đốt chính
                KmNo(dich, foeFeet, tH, 0.45f * manh, "luat", dir);
                XqVongXich(dich, foeFeet.y, tH, manh, (XqSTha - XqSTroi) * k, (XqSCot - XqSTroi) * k);
            });
            float rx = 0.44f * tH * Mathf.Sqrt(manh), ry = 0.12f * tH;
            // lửa liếm vòng xích: lưỡi chữ S liền khối có giọt tách (KmLuaS; ảnh chưa nhập thì lưỡi cũ)
            Every(XqSTroi * k, XqSTha * k, 24 * manh, x =>
            {
                float th = U(0, 6.2832f);
                float cy = dich.y + (rng.Next(2) == 0 ? -0.1f : 0.12f) * tH;
                var p = new Vector2(dich.x + rx * Mathf.Cos(th), cy + ry * Mathf.Sin(th));
                int g = Mathf.Sin(th) > 0 ? Front : Back;
                if (KmLuaS(p, U(0.12f, 0.17f) * tH * manh, U(0.3f, 0.42f), KmLua, Th.pal, g, new Vector2(U(-10, 10), -U(20, 50)), 0.35f) == null)
                    XqLiem(p, manh, g, 1.1f);
            });
            Every(XqSTroi * k, XqSTha * k, 26 * manh, x => XqLiem(Vector2.Lerp(Tay(Tc()), dich, U(0.05f, 0.92f)), manh, Front, 0.85f));
            // 5. CỘT LỬA rất to + bốn nhịp đốt (nổ KR5 nhỏ, lõi sau lưng đối thủ)
            At(XqSCot * k, () =>
            {
                KmNhip(0.6f);
                XqCotLua(foeFeet, tH, manh, (XqSTha - XqSCot) * k);
            });
            for (int i = 0; i < 4; i++)
            {
                int ii = i;
                At((XqSCot + 0.15f + 0.25f * i) * k, () =>
                {
                    Shake?.Invoke(0.18f * manh);
                    if (ii > 0) KmNhip(0.4f);   // nhịp đốt đầu là cú trúng chính (StageView)
                    KmNo(dich + new Vector2(U(-0.15f, 0.15f) * tH, U(-0.2f, 0.1f) * tH), foeFeet, tH, 0.4f * manh, "luat", dir);
                });
            }
            // 6. thả: khói cụm bay lên tách dần, lửa dọc xích tắt dần theo xích rút về
            At(XqSTha * k, () =>
            {
                for (int i = 0; i < 3; i++)
                    KmKhoi(dich + new Vector2(U(-0.25f, 0.25f) * tH, -U(0.2f, 0.5f) * tH), new Vector2(U(-20, 20), -U(40, 80)), U(0.14f, 0.18f) * tH,
                        U(1.0f, 1.3f), Back, 0.5f, 2, null, 0.4f);
            });
            Every(XqSTha * k, XqSRut * k, x => 70 * manh * (1 - x), x =>
            {
                float tc = Tc();
                float q = 1 - EaseOut(Mathf.Clamp01((tc - XqSTha) / (XqSRut - XqSTha)));
                var a = Tay(tc);
                XqLiem(Vector2.Lerp(a, Vector2.Lerp(a, dich, q), U(0.05f, 1f)), manh, Front, 0.8f);
            });
            return t0;
        }

        // VÒNG XÍCH quấn thân đối thủ: hai vòng elip mắt xích của rig (nửa sau vẽ sau tướng, nửa trước vẽ trước), quấn dần từng mắt, nóng đỏ
        // dần khi cột lửa bốc (tCot giây sau lúc trói), giữ tới tTha rồi rơi xuống mặt đất dưới chân đối thủ (dat), nảy nhẹ, nằm yên, mờ
        void XqVongXich(Vector2 body, float dat, float tH, float manh, float tTha, float tCot)
        {
            var s1 = XqXich(1);
            var s2 = XqXich(2);
            if (s1 == null || s2 == null) return;
            float rx = 0.44f * tH * Mathf.Sqrt(manh), ry = 0.12f * tH, L = 0.15f * tH;
            const int n = 14;
            for (int vong = 0; vong < 2; vong++)
            {
                float cy = body.y + (vong == 0 ? -0.1f : 0.12f) * tH;
                for (int i = 0; i < n; i++)
                {
                    float th = 6.2832f * i / n + vong * 0.22f;
                    var sp = (i & 1) == 0 ? s2 : s1;
                    var p = new P
                    {
                        pos = new Vector2(body.x + rx * Mathf.Cos(th), cy + ry * Mathf.Sin(th)), life = tTha + 0.7f,
                        group = Mathf.Sin(th) > 0 ? Front : Back, ph = 0.012f * (i + vong * n), sz = L,
                        ground = dat + ry * Mathf.Sin(th) * 0.6f, bounce = 0.25f
                    };
                    p.onGround = (q, s3) => q.spin = 0;
                    var d = new Vector2(-rx * Mathf.Sin(th), ry * Mathf.Cos(th));
                    float goc = VelAng(d) - 90;
                    float asp = sp.rect.width / Mathf.Max(1f, sp.rect.height);
                    float quay = U(-6, 6);
                    p.upd = (q, dt, s3) =>
                    {
                        if (q.age > tTha && q.acc.y == 0 && q.vel.y >= 0 && q.pos.y < q.ground - 0.5f)
                        {
                            q.acc = new Vector2(0, 1400);                      // bắt đầu rơi (một lần)
                            q.vel = new Vector2(U(-40, 40), -U(40, 120));
                            q.spin = quay;
                        }
                    };
                    p.draw = (q, k, buf) =>
                    {
                        float t = q.age;
                        if (t < q.ph) return;
                        float hien = EaseOut(Mathf.Clamp01((t - q.ph) / 0.08f));
                        float nong = SmoothStep(tCot, tCot + 0.45f, t) * (1 - SmoothStep(tTha, tTha + 0.4f, t));
                        float a = 1 - SmoothStep(tTha + 0.35f, tTha + 0.7f, t);
                        var col = Color.Lerp(Color.white, XqNong, 0.75f * nong);
                        Put(buf, q.group, 38, sp, col, q.pos, q.sz * hien, asp, goc + q.ang * Mathf.Rad2Deg, a);
                    };
                    Add(p);
                }
            }
        }

        // CỘT LỬA rất to dưới chân đối thủ: vòng lửa + khe nứt dưới đất, nổ ở chân, cột lưỡi lửa bốc thẳng lên (lõi sau lưng đối thủ, hai mép
        // trước nhỏ hơn để không che mặt), lõi nóng giữa cột, khói đen ở đỉnh, than bay. Cao tới gần mép trên màn, tối đa 2,4 lần thân.
        void XqCotLua(Vector2 feet, float tH, float manh, float dur)
        {
            float rx = 0.36f * tH;
            float cao = Mathf.Clamp(feet.y - 24, 1.2f * tH, 2.4f * tH) * Mathf.Sqrt(manh);
            float v0 = Mathf.Max(380, (cao - 60) / 0.425f);
            Shake?.Invoke(0.7f * manh);
            // hai vòng cung dẹt KHÔNG viền nở trên đất (KR5; vòng có viền mực dày nhìn nặng, soi tờ khung 2026-11-18)
            KmCung(feet + new Vector2(0, 2), 0.15f * tH, 1.1f * tH * manh, 0.45f, Th.ring2, 0.3f, Floor, 30.6f, 0.9f);
            KmCung(feet + new Vector2(0, 2), 0.1f * tH, 0.75f * tH * manh, 0.6f, Th.ember, 0.3f, Floor, 31, 0.75f);
            var cr = new P { pos = feet + new Vector2(0, 2), life = dur + 0.5f, group = Floor, seed = rng.Next(4), sz = tH };
            cr.draw = (q, k, buf) => Put(buf, Floor, 1, S("crack_" + q.seed), Color.white, q.pos, 1.4f * q.sz * 0.42f * Mathf.Min(1, q.age / 0.15f),
                1 / 0.42f, 0, Mathf.Min(1, (1 - k) / 0.3f));
            Add(cr);
            KmChay(feet + new Vector2(0, 3), 0.5f * tH, dur, 0.8f, 0.42f);
            KmNo(feet + new Vector2(0, -0.15f * tH), feet, tH, 0.9f * manh, "luat", 0);
            // 2026-11-18 (người dùng: lửa rải rác, chưa liền, chưa mềm): thân cột là các lưỡi lửa TO chồng sát nhau sau lưng đối thủ (một khối, một
            // viền mực), ít hơn mà to hơn; mép trước chỉ vài lưỡi chữ S nhỏ ở chân (không che mặt); giọt lửa tách khỏi ngọn; đỉnh cột là khói CỤM
            // than đáy ánh lửa (tách cụm rồi mới mờ); cụm đốm nhỏ thay đốm lẻ to
            // khung vẽ sẵn (2026-11-19): thân cột là ba khung lửa lặp "lua_lap" chồng nhau sau lưng (KmCotLuaFb, HatFbKim.cs) thay ~90 lưỡi rời;
            // mép trước (KmLuaS), nổ chân (KmNo), khói đỉnh (KmKhoi) cũng ra khung; chưa nhập ảnh thì lưỡi lửa dưới
            if (!KmCotLuaFb(feet, cao, dur))
            {
                Every(0, dur, x => 64 * manh * (1 - 0.3f * x), x =>
                {
                    float th = U(0, 6.2832f);
                    float c = Mathf.Cos(th), s = Mathf.Sin(th);
                    var q = Flame(feet + new Vector2(rx * c * U(0.5f, 0.95f), 10 * s - 6), new Vector2(-c * U(10, 50), -U(0.85f, 1.15f) * v0), U(0.5f, 0.72f),
                        U(13, 17) * manh, U(38, 50) * manh, "tron", Th.pal, Back, 1.3f, -380, 1.75f, 0.03f, 0.04f);
                    Tongue(q, 1, 0.65f);
                    q.smokeGroup = Back;
                });
                Every(0, dur * 0.85f, 24 * manh, x =>
                {
                    var q = Flame(feet + new Vector2(U(-0.12f, 0.12f) * tH, -4), new Vector2(U(-20, 20), -U(1.05f, 1.3f) * v0), U(0.4f, 0.55f), 10 * manh,
                        U(26, 34) * manh, "tron", Th.pal, Back, 1.2f, -420, 2.1f, 0, 0.04f);
                    Tongue(q, 1, 0.75f);
                });
            }
            Every(0.04f, dur, 9 * manh, x =>
            {
                float sd = rng.Next(2) == 0 ? -1 : 1;
                var chan = feet + new Vector2(sd * rx * U(0.55f, 0.95f), U(2, 8));
                if (KmLuaS(chan, U(0.2f, 0.28f) * tH * manh, U(0.34f, 0.48f), KmLua, Th.pal, Front, new Vector2(-sd * U(0, 20), -U(10, 40)), 0.6f) == null)
                {
                    var q = Flame(chan + new Vector2(0, -6), new Vector2(-sd * U(0, 30), -U(0.5f, 0.7f) * v0), U(0.3f, 0.42f), 8 * manh, U(16, 22) * manh, "tron",
                        Th.pal, Front, 1.6f, -380, 1.7f, 0, 0);
                    Tongue(q, 1, 0.7f);
                }
            });
            Every(0.1f, dur, 10 * manh, x => KmGiot(feet + new Vector2(U(-0.25f, 0.25f) * tH, -cao * U(0.55f, 0.95f)), new Vector2(U(-40, 40), -U(160, 260)),
                U(6, 9) * manh, KmLua, Back));
            Every(0.15f, dur + 0.3f, 6 * manh, x => KmKhoi(feet + new Vector2(U(-0.25f, 0.25f) * tH, -cao * U(0.85f, 1.05f)),
                new Vector2(U(-30, 30), -U(60, 110)), U(0.16f, 0.21f) * tH * manh, U(1.0f, 1.3f), Back, 0.8f, 2, null, 0.45f));
            Every(0, dur, 2 * manh, x => KmDomCum(feet + new Vector2(U(-0.4f, 0.4f) * tH, -U(0.2f, 0.9f) * cao), new Vector2(U(-50, 50), -U(140, 240)),
                Th.ember, U(0, 1) < 0.5f ? Front : Back));
        }
    }
}
