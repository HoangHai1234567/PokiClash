// SINH TỰ ĐỘNG bởi ArtGen/Spine/nuoc_goi/dong_goi.py — đừng sửa tay (chạy lại script).
// Bảng UV các flipbook nước trong atlas Assets/03 Art/Fx/Nuoc/nuoc_fb.png (2048², cặp 0 = RG (giá trị, alpha), cặp 1 = BA).
// Nguồn từng flipbook: ArtGen/Spine/nuoc_goi/NGUON.md (gói SrRubfish Water VFX 02, người dùng 2026-11-25 cho dùng, có biến đổi).
namespace PokiClash
{
    public enum NFb { Xoan, NuocNgang, VongNuoc, Toe, ToeNgangA, ToeNgangB, TruotDat, ChamDat, MuaA, MuaB, MuaC, MuaD, Giot, BongNho, GaiTrung, ChopHuong, ChopTron, ToeGiua, ToeDon, ToeTrung, ToeVa, CotDung, ToeDat, CauVong, BongVo, BongDon, Chem, SongTruot, Roi, GonMua, XoayO, BotKhoi, ChemVong, ToeNgangC, ToeNho, ToeGiuaNho, NuocRoi, ToeDatLon, BotRieng, VetSang }

    public readonly struct NFbDef
    {
        public readonly float u0, vTop, cu, cv, aspect;
        public readonly int cols, frames, pair;

        public NFbDef(float u0, float vTop, float cu, float cv, int cols, int frames, int pair, float aspect)
        {
            this.u0 = u0;
            this.vTop = vTop;
            this.cu = cu;
            this.cv = cv;
            this.cols = cols;
            this.frames = frames;
            this.pair = pair;
            this.aspect = aspect;
        }

        // góc dưới trái (uv) của khung i (ô hàng r tính từ trên xuống)
        public UnityEngine.Vector2 Min(int i)
        {
            int c = i % cols, r = i / cols;
            return new UnityEngine.Vector2(u0 + c * cu, vTop - (r + 1) * cv);
        }
    }

    public static class NuocFbBang
    {
        public static readonly NFbDef[] Defs =
        {
            new NFbDef(0.460938f, 1.000000f, 0.125000f, 0.031250f, 2, 16, 0, 4.0000f), // 0 Xoan: vệt xoắn cuộn quanh thân tia / mũ đầu tia (Water Laser LaserNoise03/05)
            new NFbDef(0.710938f, 1.000000f, 0.062500f, 0.062500f, 3, 12, 0, 1.0000f), // 1 NuocNgang: lá nước xoay ở đầu tia (Laser LaserNoise06)
            new NFbDef(0.000000f, 1.000000f, 0.125000f, 0.062500f, 3, 12, 1, 2.0000f), // 2 VongNuoc: vòng nước nở quanh thân tia / gốc (Laser WaterAOE)
            new NFbDef(0.375000f, 1.000000f, 0.062500f, 0.062500f, 4, 16, 1, 1.0000f), // 3 Toe: toé thường (Laser Splashes)
            new NFbDef(0.273438f, 1.000000f, 0.093750f, 0.052734f, 2, 10, 0, 1.7803f), // 4 ToeNgangA: toé ngang có hướng (Laser Impact WaterDirectionalImpact)
            new NFbDef(0.156250f, 0.726562f, 0.093750f, 0.049805f, 2, 10, 0, 1.8746f), // 5 ToeNgangB: toé ngang có hướng 2
            new NFbDef(0.312500f, 0.476562f, 0.078125f, 0.042480f, 4, 16, 0, 1.8436f), // 6 TruotDat: vệt nước loang trượt trên đất (Laser LateralWater_Lingering)
            new NFbDef(0.625000f, 1.000000f, 0.062500f, 0.062500f, 4, 16, 1, 1.0000f), // 7 ChamDat: vòng gợn chấm trên đất (GroundDots)
            new NFbDef(0.531250f, 0.281250f, 0.062500f, 0.031250f, 4, 16, 1, 2.0000f), // 8 MuaA: toé hạt mưa trên đất (WaterGround_01)
            new NFbDef(0.500000f, 0.125000f, 0.062500f, 0.031250f, 3, 9, 0, 2.0000f), // 9 MuaB: toé hạt mưa 2 (WaterGround_03)
            new NFbDef(0.156250f, 0.281250f, 0.046875f, 0.046875f, 4, 12, 1, 1.0000f), // 10 MuaC: toé hạt mưa 3 (WaterGround_04)
            new NFbDef(0.343750f, 0.281250f, 0.046875f, 0.046875f, 4, 12, 1, 1.0000f), // 11 MuaD: toé hạt mưa 4 (WaterGround_02)
            new NFbDef(0.906250f, 0.281250f, 0.031250f, 0.031250f, 2, 4, 1, 1.0000f), // 12 Giot: giọt bắn kéo dài (Dots / DotsDirectional)
            new NFbDef(0.875000f, 0.125000f, 0.031250f, 0.031250f, 2, 4, 0, 1.0000f), // 13 BongNho: bong bóng trong lòng tia (DotsDirectionalInside)
            new NFbDef(0.781250f, 0.281250f, 0.062500f, 0.062500f, 2, 4, 1, 1.0000f), // 14 GaiTrung: gai sắc chỗ trúng (Impact LightImpact / ImpactSpikes)
            new NFbDef(0.937500f, 0.125000f, 0.062500f, 0.062500f, 1, 1, 0, 1.0000f), // 15 ChopHuong: chớp trúng có hướng (Impact Impact)
            new NFbDef(0.000000f, 0.125000f, 0.062500f, 0.062500f, 1, 1, 1, 1.0000f), // 16 ChopTron: chớp trúng tròn (Impact CenterImpact)
            new NFbDef(0.000000f, 0.750000f, 0.062500f, 0.062500f, 4, 16, 1, 1.0000f), // 17 ToeGiua: toé bung giữa (SimpleSplash)
            new NFbDef(0.250000f, 0.750000f, 0.062500f, 0.062500f, 4, 16, 1, 1.0000f), // 18 ToeDon: toé đơn (SimpleWaterImpact)
            new NFbDef(0.500000f, 0.750000f, 0.062500f, 0.062500f, 4, 16, 1, 1.0000f), // 19 ToeTrung: toé trúng đạn (Water_Impact_01)
            new NFbDef(0.750000f, 0.750000f, 0.062500f, 0.062500f, 4, 16, 1, 1.0000f), // 20 ToeVa: toé va (ImpactGround)
            new NFbDef(0.000000f, 0.726562f, 0.039062f, 0.062500f, 4, 16, 0, 0.6341f), // 21 CotDung: cột nước dựng (mạch phun / ImpactGround)
            new NFbDef(0.437500f, 0.289062f, 0.078125f, 0.039062f, 4, 16, 0, 2.0157f), // 22 ToeDat: toé trên đất (Water_ImpactGround)
            new NFbDef(0.000000f, 1.000000f, 0.054688f, 0.054688f, 5, 25, 0, 1.0000f), // 23 CauVong: khối nước cuộn vòng (Orb / StrongProjectile)
            new NFbDef(0.750000f, 0.476562f, 0.054688f, 0.054688f, 3, 9, 0, 1.0000f), // 24 BongVo: bong bóng vỡ (Bubble)
            new NFbDef(0.750000f, 0.289062f, 0.039062f, 0.039062f, 4, 16, 0, 0.9961f), // 25 BongDon: bong bóng đơn
            new NFbDef(0.000000f, 0.125000f, 0.125000f, 0.031250f, 4, 16, 0, 4.0000f), // 26 Chem: lưỡi chém nước (WaveAttack / Slash)
            new NFbDef(0.218750f, 0.500000f, 0.062500f, 0.036133f, 4, 24, 1, 1.7143f), // 27 SongTruot: sóng trượt ngang (WaveAttack Projectile)
            new NFbDef(0.656250f, 0.726562f, 0.054688f, 0.054688f, 4, 16, 0, 1.0000f), // 28 Roi: roi nước (Whip)
            new NFbDef(0.000000f, 0.289062f, 0.054688f, 0.054688f, 4, 12, 0, 1.0000f), // 29 GonMua: vòng gợn mưa (RainExample)
            new NFbDef(0.343750f, 0.726562f, 0.078125f, 0.046875f, 4, 20, 0, 1.6667f), // 30 XoayO: lốc xoáy ô lặp (Buff / whirl)
            new NFbDef(0.000000f, 0.476562f, 0.046875f, 0.046875f, 4, 16, 0, 1.0250f), // 31 BotKhoi: khói bọt (FoamImpact)
            new NFbDef(0.000000f, 0.500000f, 0.054688f, 0.054688f, 4, 16, 1, 1.0000f), // 32 ChemVong: chém vòng tròn (SlashBasic / whirl)
            new NFbDef(0.218750f, 0.289062f, 0.054688f, 0.054688f, 4, 12, 0, 1.0000f), // 33 ToeNgangC: toé ngang 3 (StrongProjectile Impact)
            new NFbDef(0.625000f, 0.476562f, 0.062500f, 0.027832f, 2, 12, 0, 2.2582f), // 34 ToeNho: toé nhỏ
            new NFbDef(0.468750f, 0.500000f, 0.039062f, 0.029297f, 6, 41, 1, 1.3229f), // 35 ToeGiuaNho: toé nhỏ bung giữa (Projectile)
            new NFbDef(0.187500f, 0.476562f, 0.031250f, 0.062500f, 4, 12, 0, 0.5000f), // 36 NuocRoi: nước rơi (FallingWater)
            new NFbDef(0.703125f, 0.500000f, 0.054688f, 0.040527f, 5, 25, 1, 1.3486f), // 37 ToeDatLon: toé đất lớn (Grenade Explosion)
            new NFbDef(0.000000f, 0.281250f, 0.039062f, 0.039062f, 4, 16, 1, 1.0000f), // 38 BotRieng: bọt rời (Waterfall foam)
            new NFbDef(0.687500f, 0.125000f, 0.093750f, 0.014160f, 2, 10, 0, 6.7368f), // 39 VetSang: vệt sáng lưỡi chém (Slash highlight)
        };

        public static NFbDef Get(NFb f) => Defs[(int)f];
    }
}
