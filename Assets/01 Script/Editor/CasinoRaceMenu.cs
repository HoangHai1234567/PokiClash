// Scene Trường đua của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.3, mốc C5; mỗi trò một scene). Menu
// "PokiClash/Prefab/Đảo Casino/Trường đua: dựng scene" (chạy lại được): Screens/CasinoRace (lần đầu chép từ Screens/Cave, thay bằng
// RaceScene), scene CasinoRace + Build Settings.
// Bản sân vận động (người dùng 2026-11-26): khung nhìn `san` có RaceStadium, thế giới cuộn ngang, PHỦ KÍN MÀN (nằm dưới Canvas/Nen).
// Hình ở Assets/03 Art/Baked/Casino (race_san.png, race_hinh.png, race_buc.png, race_art.json do
// ArtGen/Casino/truong_dua/dong_goi.py đóng; menu này đặt cách nhập nhiều sprite).
// Lớp trong `san` từ xa tới gần: khán đài hai tầng lát 3 ô, cờ mái, 6 hàng khán giả, tường trước, mặt đường 3 ô (giãn theo chiều cao
// màn), vạch làn, trang trí xa, cổng chặng phía xa (vạch, cột, cờ, biển tên hệ), bụi, 5 tướng (chân dung UiKit.portrait trong khung
// nhún, sao choáng, vụt nổ, chữ nổi, số hạng), trang trí gần, hàng rào dây, cột cổng phía gần, hai hàng cổ động viên quay lưng, thẻ
// mép, lễ trao giải (màn tối, bục 3 bậc, 3 tướng, số hạng, thẻ tên), hoa giấy, chớp trắng.
// Giao diện trong vùng an toàn: `hud` (thanh đường hôm nay kiêm bản đồ nhỏ, bảng treo có mặt tướng dẫn đầu + tường thuật), chữ lớn,
// `sanh` ở đáy màn là QUẦY CƯỢC (tấm quầy gỗ mái sọc cắt 9 mảnh: vé lượt hôm nay, điểm cúp tuần, bảng trả thưởng, 4 đồng chip mức cược,
// nút Đặt cược / dải băng nhắc chạm chọn; ẩn khi đua), nút Cổ vũ, `ket_qua` (huy hiệu, hạng, thưởng, bảng xếp hạng, Đua tiếp / Xong).
// Mỗi con ở vạch có vùng chạm `cham` (RaceTap) để chọn con đặt cược.
// Cờ Temp/casino_race_build.flag (dựng), Temp/casino_race_tour.flag (vào Play, đua một lượt tự cổ vũ, chụp Temp/PokiShots/casino_dua/).
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class CasinoRaceMenu
    {
        const string ScreenPath = "Assets/04 Prefabs/Screens/CasinoRace.prefab";
        const string BaseScreenPath = "Assets/04 Prefabs/Screens/Cave.prefab";
        const string ScenePath = "Assets/00 Scenes/CasinoRace.unity";
        const string PickerPath = "Assets/04 Prefabs/Dialogs/ChonDoi.prefab";
        const int Lanes = 5;
        // khung nhìn sân phủ kín màn (người dùng 2026-11-26): khán đài neo mép trên, hàng rào và cổ động viên neo mép dưới, mặt đường giãn ở giữa
        const float StandW = 1360, StandTop = 170; // khán đài: bề ngang một ô lát, mép trên mái (dưới thanh trên)
        const float TierSrc = 216; // tầng ghế dưới thấp hơn tầng trên bấy nhiêu px hình khán đài (đúng phần ba bậc ghế)
        const float WallW = 1140; // tường trước khán đài
        const float NearH = 520; // mép gần của mặt đường cách mép dưới khung
        const float BoardW = 640; // bảng treo
        const float PodW = 900, PodY = -120; // bục nhận thưởng: bề ngang, đáy bục so với giữa khung
        const string DealerRigPath = "Assets/03 Art/Casino/Dealer/lao_muc.bytes"; // rig Lão Mực (ArtGen/Casino/dealer, lều Đêm Bài dùng chung)
        const float DealerScale = 0.5f, DealerX = 340; // chủ quầy cược: cỡ rig, lệch phải so với giữa quầy
        const float BoothH = 526; // quầy cược: cao bấy nhiêu tính từ đáy vùng an toàn (xấp xỉ mép gần của mặt đường)

        static T Load<T>() where T : Object =>
            AssetDatabase.FindAssets("t:" + typeof(T).Name).Select(g => AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(g))).FirstOrDefault(a => a);

        static RectTransform N(Transform p, string n, params System.Type[] t) => HomeSceneMenu.Node(p, n, t);
        static RectTransform At(RectTransform rt, Vector2 a, Vector2 pos, Vector2 size, Vector2 pivot) => HomeSceneMenu.At(rt, a, pos, size, pivot);
        static Image Img(Transform p, string n, Sprite s, Color c, bool ray = false, bool sliced = false) => HomeSceneMenu.Img(p, n, s, c, ray, sliced);
        static TextMeshProUGUI Txt(Transform p, string n, float size, Color c) => HomeSceneMenu.Text(p, n, size, c);
        static UiKit Kit => AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiKit")[0]));

        // ---------- hình sân vận động ----------

        const string ArtDir = "Assets/03 Art/Baked/Casino/";
        const string ArtJson = ArtDir + "race_art.json";

        sealed class Art
        {
            public Dictionary<string, Sprite> sprites = new Dictionary<string, Sprite>();
            public Rect boardInner; // ô bảng đen trong hình "bang" (px hình, gốc trên trái)
            public Vector2[] podStand = new Vector2[3], podPlaque = new Vector2[3]; // chỗ đứng, tâm biển tròn hạng 1, 2, 3 trong hình "buc"
            public Sprite this[string n] => sprites.TryGetValue(n, out var s) ? s : null;
        }

        // hai tấm atlas: nhiều sprite theo race_art.json, không mipmap, điện thoại ASTC 6x6 (thư mục Baked: ArtImporter không đặt hộ)
        static Art ImportArt()
        {
            if (!File.Exists(ArtJson)) { Debug.LogError("[Đảo Casino] Thiếu " + ArtJson + " (chạy ArtGen/Casino/truong_dua/dong_goi.py)"); return null; }
            var meta = J.Obj(MiniJson.Parse(File.ReadAllText(ArtJson)));
            var art = new Art();
            foreach (var a in J.Arr(meta, "atlases").Select(J.Obj))
            {
                string png = ArtDir + J.Str(a, "png");
                int h = J.Int(a, "h");
                AssetDatabase.ImportAsset(png);
                var ti = (TextureImporter)AssetImporter.GetAtPath(png);
                if (!ti) { Debug.LogError("[Đảo Casino] Thiếu " + png); return null; }
                ti.textureType = TextureImporterType.Sprite;
                ti.spriteImportMode = SpriteImportMode.Multiple;
                ti.mipmapEnabled = false;
                ti.alphaIsTransparency = true;
                ti.wrapMode = TextureWrapMode.Clamp;
                ti.filterMode = FilterMode.Bilinear;
                ti.npotScale = TextureImporterNPOTScale.None;
                ti.maxTextureSize = 2048;
                var st = new TextureImporterSettings();
                ti.ReadTextureSettings(st);
                st.spriteMeshType = SpriteMeshType.FullRect;
                ti.SetTextureSettings(st);
                foreach (var pf in new[] { "Android", "iPhone" })
                {
                    var ps = ti.GetPlatformTextureSettings(pf);
                    ps.overridden = true;
                    ps.maxTextureSize = 2048;
                    ps.format = TextureImporterFormat.ASTC_6x6;
                    ti.SetPlatformTextureSettings(ps);
                }
#pragma warning disable 618
                ti.spritesheet = J.Arr(a, "items").Select(J.Obj).Select(m =>
                {
                    var piv = J.Arr(m, "pivot");
                    return new SpriteMetaData
                    {
                        name = J.Str(m, "name"), alignment = (int)SpriteAlignment.Custom,
                        rect = new Rect(J.Int(m, "x"), h - J.Int(m, "y") - J.Int(m, "h"), J.Int(m, "w"), J.Int(m, "h")),
                        pivot = new Vector2((float)(double)piv[0], (float)(double)piv[1]),
                        border = J.Arr(m, "border") is var bd && bd.Count == 4
                            ? new Vector4((float)(double)bd[0], (float)(double)bd[1], (float)(double)bd[2], (float)(double)bd[3]) : Vector4.zero,
                    };
                }).ToArray();
#pragma warning restore 618
                ti.SaveAndReimport();
                foreach (var sp in AssetDatabase.LoadAllAssetsAtPath(png).OfType<Sprite>()) art.sprites[sp.name] = sp;
            }
            var bi = J.Arr(meta, "bang_trong");
            if (bi.Count == 4) art.boardInner = Rect.MinMaxRect((float)(double)bi[0], (float)(double)bi[1], (float)(double)bi[2], (float)(double)bi[3]);
            var stand = J.Arr(meta, "buc_cho");
            var plaque = J.Arr(meta, "buc_bien");
            for (int i = 0; i < 3 && i < stand.Count && i < plaque.Count; i++)
            {
                var a0 = J.Arr(stand[i]);
                var a1 = J.Arr(plaque[i]);
                art.podStand[i] = new Vector2((float)(double)a0[0], (float)(double)a0[1]);
                art.podPlaque[i] = new Vector2((float)(double)a1[0], (float)(double)a1[1]);
            }
            return art;
        }

        // đặt theo góc trên trái của khung nhìn: x từ trái, y từ mép trên xuống
        static RectTransform TL(RectTransform rt, float x, float y, Vector2 size, Vector2 pivot) => At(rt, new Vector2(0, 1), new Vector2(x, -y), size, pivot);

        static RectTransform Layer(Transform parent, string name) => HomeSceneMenu.Fill(N(parent, name));

        static readonly Vector2 Foot = new Vector2(0.5f, 0), TopMid = new Vector2(0.5f, 1), Mid = new Vector2(0.5f, 0.5f);

        // neo góc dưới trái của khung: x từ trái, y từ mép dưới lên
        static RectTransform BL(RectTransform rt, float x, float y, Vector2 size, Vector2 pivot) => At(rt, Vector2.zero, new Vector2(x, y), size, pivot);

        // một hàng ô lát lật gương; y: mép trên của ô tính từ mép trên khung, hoặc (fromBottom) đáy ô tính từ mép dưới khung
        static RaceStadium.Tiles TileRow(Transform view, string name, Sprite sp, float width, float y, int count, float parallax, bool fromBottom = false)
        {
            var layer = Layer(view, name);
            float h = sp.rect.height * width / sp.rect.width;
            var items = new RectTransform[count];
            for (int i = 0; i < count; i++)
            {
                var img = Img(layer, "o_" + i, sp, Color.white);
                items[i] = fromBottom
                    ? BL(img.rectTransform, i * width + width / 2, y, new Vector2(width + 1, h), Foot)
                    : TL(img.rectTransform, i * width + width / 2, y, new Vector2(width + 1, h), TopMid);
            }
            return new RaceStadium.Tiles { items = items, width = width, parallax = parallax, mirror = true };
        }

        static HeroPortrait Portrait(UiKit kit, Transform parent, string name, float h)
        {
            var p = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, parent)).GetComponent<HeroPortrait>();
            p.name = name;
            At(p.Rect, Foot, new Vector2(0, -h * HeroArt.FootY), new Vector2(h * HeroArt.W / HeroArt.H, h), Foot);
            foreach (var g in p.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
            return p;
        }

        [MenuItem("PokiClash/Prefab/Đảo Casino/Trường đua: dựng scene", priority = 74)]
        public static void Build()
        {
            var assets = Load<UiAssets>();
            if (!assets) return;
            Theme.Init(assets);
            var art = ImportArt();
            if (art == null) return;
            if (!File.Exists(ScreenPath))
            {
                if (!AssetDatabase.CopyAsset(BaseScreenPath, ScreenPath)) { Debug.LogError("[Đảo Casino] Không chép được " + BaseScreenPath); return; }
                AssetDatabase.ImportAsset(ScreenPath);
            }
            var root = PrefabUtility.LoadPrefabContents(ScreenPath);
            try
            {
                root.name = "CasinoRace";
                var scene = root.GetComponent<RaceScene>();
                RectTransform content;
                if (!scene)
                {
                    var old = root.GetComponent<SceneRoot>();
                    PokiCanvas view = null;
                    content = null;
                    if (old)
                    {
                        var so = new SerializedObject(old);
                        view = so.FindProperty("view").objectReferenceValue as PokiCanvas;
                        content = so.FindProperty("content").objectReferenceValue as RectTransform;
                        Object.DestroyImmediate(old);
                    }
                    scene = root.AddComponent<RaceScene>();
                    scene.SetupView(view ? view : root.GetComponentInChildren<PokiCanvas>(true), content);
                }
                else content = scene.Content;
                var nen = root.transform.Find("Canvas/Nen") as RectTransform;
                var safe = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!nen || !safe) { Debug.LogError("[Đảo Casino] Screens/CasinoRace thiếu Canvas/Nen hoặc Canvas/An toan/Khung."); return; }
                foreach (Transform c in nen.Cast<Transform>().ToList())
                {
                    if (c.name == "san") Object.DestroyImmediate(c.gameObject);
                    else c.gameObject.SetActive(c.name == "nen_hai_ben");
                }
                if (nen.Find("nen_hai_ben")?.GetComponent<Image>() is Image si) { si.sprite = null; si.color = Theme.Sky; }
                foreach (Transform c in safe.Cast<Transform>().ToList()) if (c != content) Object.DestroyImmediate(c.gameObject);
                if (content) foreach (Transform c in content.Cast<Transform>().ToList()) Object.DestroyImmediate(c.gameObject);

                var kit = Kit;
                var outline = Theme.Outlined(Theme.Bold, 0.3f);
                var paper = new Color(1f, 0.98f, 0.92f, 0.95f);

                // ---------- sân vận động phủ kín màn (dưới Canvas/Nen; nới 16 px mỗi bên để rung khung không lộ mép) ----------
                var viewImg = Img(nen, "san", null, Theme.Sky);
                var field = HomeSceneMenu.Fill(viewImg.rectTransform);
                field.offsetMin = new Vector2(-16, -16);
                field.offsetMax = new Vector2(16, 16);
                var stadium = field.gameObject.AddComponent<RaceStadium>();
                var sp = new RaceStadium.Parts { view = field };

                // khán đài hai tầng (tầng dưới vẽ trước, mái của nó bị tầng trên che), cờ mái, 6 hàng khán giả ngồi
                var standSp = art["khan_dai"];
                float standK = StandW / standSp.rect.width, standH = standSp.rect.height * standK;
                sp.standsLow = TileRow(field, "khan_dai_duoi", standSp, StandW, StandTop + TierSrc * standK, 3, 0.85f);
                sp.stands = TileRow(field, "khan_dai", standSp, StandW, StandTop, 3, 0.85f);
                var roofL = Layer(field, "co_mai");
                var roofSp = art["co_mai"];
                sp.roofFlags = new RectTransform[10];
                for (int i = 0; i < sp.roofFlags.Length; i++)
                {
                    var f = Img(roofL, "co_" + i, roofSp, Color.white);
                    sp.roofFlags[i] = TL(f.rectTransform, i * 204, StandTop + 6, roofSp.rect.size * 0.9f, new Vector2(0.14f, 0));
                }
                sp.roofFlagStep = 204;
                sp.roofFlagY = StandTop + 6;
                sp.fanSprites = Enumerable.Range(0, 8).Select(i => art["fan_f" + i]).ToArray();
                sp.fanCols = 20; sp.fanStep = 84; sp.fanScale = 0.66f;
                // đáy hình khán giả theo bậc ghế (px hình khán đài 282 / 353 / 425), hai tầng
                sp.fanRowY = new[] { 0f, TierSrc }.SelectMany(t => new[] { 282f, 353f, 425f }.Select(y => StandTop + (y + t) * standK)).ToArray();
                var fanL = Layer(field, "khan_gia");
                sp.fans = new Image[sp.fanRowY.Length * sp.fanCols];
                for (int r = 0; r < sp.fanRowY.Length; r++)
                    for (int c = 0; c < sp.fanCols; c++)
                    {
                        var fs = sp.fanSprites[(r * 3 + c) % sp.fanSprites.Length];
                        var f = Img(fanL, "kg_" + r + "_" + c, fs, Color.white);
                        TL(f.rectTransform, c * sp.fanStep + (r & 1) * 42, sp.fanRowY[r], fs.rect.size * sp.fanScale, Foot);
                        sp.fans[r * sp.fanCols + c] = f;
                    }
                float wallTop = StandTop + (408 + TierSrc) * standK;
                var wallSp = art["tuong"];
                sp.walls = TileRow(field, "tuong", wallSp, WallW, wallTop, 3, 1f);
                float trackTop = Mathf.Round(wallTop + wallSp.rect.height * WallW / wallSp.rect.width - 6);

                // mặt đường: 3 ô lát giãn theo chiều cao màn, mỗi ô dải đường (nhuộm màu chặng) + lề cỏ phía gần
                var groundL = Layer(field, "mat_duong");
                sp.grounds = new RectTransform[3];
                sp.groundFill = new Image[3];
                for (int i = 0; i < 3; i++)
                {
                    var g = N(groundL, "o_" + i);
                    g.anchorMin = new Vector2(0, 0); g.anchorMax = new Vector2(0, 1); g.pivot = new Vector2(0, 1);
                    g.anchoredPosition = new Vector2(i * 1080, -trackTop);
                    g.sizeDelta = new Vector2(1081, -trackTop);
                    sp.grounds[i] = g;
                    var road = Img(g, "duong", art["dat"], Color.white);
                    HomeSceneMenu.Fill(road.rectTransform).offsetMin = new Vector2(0, NearH);
                    sp.groundFill[i] = road;
                    var verge = Img(g, "le", art["dat"], Theme.Hex("#9bd070"));
                    verge.rectTransform.anchorMin = new Vector2(0, 0); verge.rectTransform.anchorMax = new Vector2(1, 0);
                    verge.rectTransform.pivot = Foot; verge.rectTransform.anchoredPosition = Vector2.zero;
                    verge.rectTransform.sizeDelta = new Vector2(0, NearH);
                }
                // vạch phấn: hai mép đường + vạch giữa các làn (RaceScene dời theo số tướng)
                var lineL = Layer(field, "vach_lan");
                RectTransform Chalk(string n, float y, float a, bool fromBottom = false)
                {
                    var l = Img(lineL, n, null, new Color(1, 1, 1, a));
                    float ay = fromBottom ? 0 : 1;
                    l.rectTransform.anchorMin = new Vector2(0, ay); l.rectTransform.anchorMax = new Vector2(1, ay);
                    l.rectTransform.pivot = Mid; l.rectTransform.anchoredPosition = new Vector2(0, fromBottom ? y : -y);
                    l.rectTransform.sizeDelta = new Vector2(0, 6);
                    return l.rectTransform;
                }
                Chalk("mep_xa", trackTop + 9, 0.7f);
                Chalk("mep_gan", NearH + 7, 0.7f, true);
                var lanes = new RaceScene.Lane[Lanes];
                float feetTop = trackTop + 80;
                for (int i = 1; i < Lanes; i++) lanes[i].line = Chalk("ke_" + i, feetTop + i * 110, 0.5f);

                // trang trí theo hệ, mép xa
                sp.decalSprites = new[] { "kim", "moc", "thuy", "hoa", "tho" }.SelectMany(e => Enumerable.Range(0, 3).Select(k => art["decal_" + e + "_" + k])).ToArray();
                sp.decalStep = 300; sp.decalScale = 0.55f; sp.decalFarY = trackTop + 38; sp.decalNearY = NearH - 30;
                Image[] DecalPool(string name, bool fromBottom)
                {
                    var l = Layer(field, name);
                    var pool = new Image[7];
                    for (int i = 0; i < pool.Length; i++)
                    {
                        pool[i] = Img(l, "tt_" + i, sp.decalSprites[i], Color.white);
                        var size = sp.decalSprites[i].rect.size * sp.decalScale;
                        if (fromBottom) BL(pool[i].rectTransform, i * 300, sp.decalNearY, size, Foot);
                        else TL(pool[i].rectTransform, i * 300, sp.decalFarY, size, Foot);
                        pool[i].enabled = false;
                    }
                    return pool;
                }
                sp.decalsFar = DecalPool("trang_tri_xa", false);

                // cổng chặng, cụm phía xa (cao hết khung): vạch trên đường, cột + cờ, biển tên hệ (cổng cuối: vạch đích và cờ ca rô)
                var gateFarL = Layer(field, "cong_xa");
                sp.gates = new RaceStadium.Gate[4];
                var pole = art["cot"];
                for (int i = 0; i < sp.gates.Length; i++)
                {
                    bool fin = i == sp.gates.Length - 1;
                    var g = new RaceStadium.Gate();
                    g.far = N(gateFarL, "cong_" + i);
                    g.far.anchorMin = new Vector2(0, 0); g.far.anchorMax = new Vector2(0, 1); g.far.pivot = TopMid;
                    g.far.sizeDelta = Vector2.zero; g.far.anchoredPosition = new Vector2(i * 400, 0);
                    var line = Img(g.far, fin ? "vach_dich" : "vach", fin ? art["vach_dich"] : null, fin ? Color.white : new Color(1, 1, 1, 0.8f));
                    float lw = fin ? 84 : 10;
                    line.rectTransform.anchorMin = new Vector2(0.5f, 0); line.rectTransform.anchorMax = new Vector2(0.5f, 1);
                    line.rectTransform.pivot = Mid;
                    line.rectTransform.offsetMin = new Vector2(-lw / 2, NearH + 7);
                    line.rectTransform.offsetMax = new Vector2(lw / 2, -(trackTop + 7));
                    if (fin)
                    {
                        // dải ca rô lát lặp theo chiều dọc (màn dài không bị kéo giãn ô)
                        line.type = Image.Type.Tiled;
                        line.pixelsPerUnitMultiplier = art["vach_dich"].rect.width / lw;
                    }
                    else
                    {
                        var sign = Img(g.far, "bien", art["bien_tron"], Color.white);
                        var ss = art["bien_tron"].rect.size * 0.7f;
                        At(sign.rectTransform, TopMid, new Vector2(-84, -(trackTop + 16)), ss, Foot);
                        // mặt biển là hình tròn ở nửa trên, đường kính gần bằng bề ngang biển
                        var face = Img(sign.transform, "mat", Sketch.Dot, Color.white);
                        At(face.rectTransform, TopMid, new Vector2(0, -ss.x * 0.5f), new Vector2(ss.x * 0.68f, ss.x * 0.68f), Mid);
                        g.signFill = face;
                        g.sign = Txt(sign.transform, "ten", 30, Theme.Ink);
                        At(g.sign.rectTransform, TopMid, new Vector2(0, -ss.x * 0.5f), new Vector2(ss.x * 0.9f, 44), Mid);
                        g.sign.textWrappingMode = TextWrappingModes.NoWrap;
                        g.sign.enableAutoSizing = true; g.sign.fontSizeMin = 14; g.sign.fontSizeMax = 30;
                    }
                    var pf = Img(g.far, "cot", pole, Color.white);
                    var ps = pole.rect.size * 0.8f;
                    At(pf.rectTransform, TopMid, new Vector2(0, -(trackTop + 14)), ps, Foot);
                    var cloth = art[fin ? "co_caro" : "co_trang"];
                    var ff = Img(g.far, "co", cloth, Color.white);
                    g.flagFar = At(ff.rectTransform, TopMid, new Vector2(9, -(trackTop + 14 - ps.y + 58)), cloth.rect.size * 0.62f, new Vector2(0, 0.5f));
                    if (!fin) g.clothFar = ff;
                    sp.gates[i] = g;
                }

                // bụi dưới chân
                var dustL = Layer(field, "bui");
                for (int i = 0; i < Lanes; i++)
                {
                    lanes[i].dust = new Image[2];
                    for (int k = 0; k < 2; k++)
                    {
                        var d = Img(dustL, "bui_" + i + "_" + k, Sketch.CloudPuff, Color.white);
                        TL(d.rectTransform, 0, 0, new Vector2(62, 44), Mid);
                        d.enabled = false;
                        lanes[i].dust[k] = d;
                    }
                }

                // 5 tướng dựng sẵn (RaceScene chia làn và đặt cỡ theo số tướng 3–5, theo chiều cao màn)
                var runL = Layer(field, "tuong_dua");
                for (int i = 0; i < Lanes; i++)
                {
                    var ln = lanes[i];
                    // token: chân tướng; body: khung nhún / lắc / lao (con của token)
                    ln.token = TL(N(runL, "tuong_" + i), 300, feetTop + (i + 0.5f) * 110, new Vector2(10, 10), Foot);
                    // vòng vàng dưới chân tướng của mình (sau lưng tướng): khung dẹt thành elip, vòng nét đứt xoay bên trong
                    ln.mark = N(ln.token, "cua_minh");
                    At(ln.mark, Foot, new Vector2(0, 2), new Vector2(140, 140), Mid);
                    ln.mark.localScale = new Vector3(1, 0.34f, 1);
                    var markImg = Img(ln.mark, "vong", Sketch.DashRing, Theme.Yellow);
                    ln.markSpin = HomeSceneMenu.Fill(markImg.rectTransform);
                    ln.mark.gameObject.SetActive(false);
                    ln.body = N(ln.token, "than");
                    At(ln.body, Foot, Vector2.zero, new Vector2(10, 10), Foot);
                    ln.portrait = Portrait(kit, ln.body, "chan_dung", 170);
                    ln.face = new SerializedObject(ln.portrait).FindProperty("body").objectReferenceValue as Image;
                    // chỗ gắn rig tướng (AolaSticker dựng lúc đua), gốc ở chân, vẽ trên chân dung
                    ln.rig = N(ln.body, "rig");
                    At(ln.rig, Foot, Vector2.zero, Vector2.zero, Foot);
                    // sao choáng: vòng 3 sao xoay, dẹt thành elip
                    ln.stars = N(ln.body, "sao_choang");
                    At(ln.stars, Foot, new Vector2(0, 160), new Vector2(10, 10), Mid);
                    ln.spin = N(ln.stars, "xoay");
                    At(ln.spin, Mid, Vector2.zero, new Vector2(10, 10), Mid);
                    for (int k = 0; k < 3; k++)
                    {
                        float ang = k * Mathf.PI * 2 / 3;
                        var st = Img(ln.spin, "sao_" + k, Sketch.Star, Theme.Yellow);
                        At(st.rectTransform, Mid, new Vector2(Mathf.Cos(ang) * 54, Mathf.Sin(ang) * 18), new Vector2(52, 52), Mid);
                    }
                    ln.stars.gameObject.SetActive(false);
                    // vụt nổ chỗ trúng (trước tướng)
                    ln.burst = Img(ln.body, "vut_no", Sketch.Burst, new Color(1f, 0.85f, 0.25f));
                    At(ln.burst.rectTransform, Foot, new Vector2(42, 85), new Vector2(150, 150), Mid);
                    ln.burst.gameObject.SetActive(false);
                    // chữ nổi (Choáng! Vấp! Né! Gió thuận!)
                    ln.pop = Txt(ln.token, "chu_noi", 40, Theme.RedD);
                    At(ln.pop.rectTransform, Foot, new Vector2(76, 90), new Vector2(280, 50), new Vector2(0, 0.5f));
                    ln.pop.alignment = TextAlignmentOptions.MidlineLeft;
                    ln.pop.textWrappingMode = TextWrappingModes.NoWrap;
                    if (outline) ln.pop.fontSharedMaterial = outline;
                    ln.pop.gameObject.SetActive(false);
                    // số hạng đang giữ
                    ln.badge = Img(ln.token, "hang", Sketch.Dot, Theme.Yellow);
                    At(ln.badge.rectTransform, Foot, new Vector2(-78, 130), new Vector2(54, 54), Mid);
                    var bo = Img(ln.badge.transform, "vien", Sketch.Ring, Theme.Ink);
                    HomeSceneMenu.Fill(bo.rectTransform);
                    ln.badgeText = Txt(ln.badge.transform, "so", 32, Theme.Ink);
                    HomeSceneMenu.Fill(ln.badgeText.rectTransform);
                    ln.badge.gameObject.SetActive(false);
                    lanes[i] = ln;
                }
                // vùng chạm chung trên đường đua (trong suốt, ngay trên lớp tướng): RaceScene chọn con gần chỗ chạm nhất, chỉ bật lúc chưa đua
                var tapImg = Img(field, "cham_chon", null, new Color(1, 1, 1, 0), true);
                HomeSceneMenu.Fill(tapImg.rectTransform).offsetMin = new Vector2(0, NearH - 80);
                tapImg.rectTransform.offsetMax = new Vector2(0, -(trackTop - 150));
                var trackTap = tapImg.gameObject.AddComponent<RaceTap>();

                sp.decalsNear = DecalPool("trang_tri_gan", true);
                sp.fences = TileRow(field, "rao", art["rao"], 1100, NearH - 68, 3, 1f, true);

                // cổng chặng, cụm phía gần (neo mép dưới): cột + cờ đứng ngoài hàng rào
                var gateNearL = Layer(field, "cong_gan");
                for (int i = 0; i < sp.gates.Length; i++)
                {
                    bool fin = i == sp.gates.Length - 1;
                    var g = sp.gates[i];
                    g.near = BL(N(gateNearL, "cong_" + i), i * 400, 0, Vector2.zero, Foot);
                    var pn = Img(g.near, "cot", pole, Color.white);
                    var ps = pole.rect.size * 0.72f;
                    At(pn.rectTransform, Mid, new Vector2(0, NearH - 105), ps, Foot);
                    var cloth = art[fin ? "co_caro" : "co_trang"];
                    var fn = Img(g.near, "co", cloth, Color.white);
                    g.flagNear = At(fn.rectTransform, Mid, new Vector2(8, NearH - 105 + ps.y - 52), cloth.rect.size * 0.56f, new Vector2(0, 0.5f));
                    if (!fin) g.clothNear = fn;
                    sp.gates[i] = g;
                }

                // hai hàng cổ động viên quay lưng, sát máy quay (bỏ con giơ biển trống: che mất làn gần)
                sp.nearSprites = Enumerable.Range(0, 6).Where(i => i != 1).Select(i => art["fan_b" + i]).ToArray();
                sp.nearCols = 13;
                sp.nearRowY = new[] { 85f, -115f };
                sp.nearRowScale = new[] { 0.8f, 1.15f };
                sp.nearRowStep = new[] { 140f, 185f };
                sp.nearRowParallax = new[] { 1.1f, 1.22f };
                var nearL = Layer(field, "co_dong_vien");
                sp.nearFans = new Image[sp.nearRowY.Length * sp.nearCols];
                for (int r = 0; r < sp.nearRowY.Length; r++)
                    for (int c = 0; c < sp.nearCols; c++)
                    {
                        var fs = sp.nearSprites[(r + c) % sp.nearSprites.Length];
                        var f = Img(nearL, "cdv_" + r + "_" + c, fs, r == 0 ? new Color(0.9f, 0.88f, 0.88f) : Color.white);
                        BL(f.rectTransform, c * sp.nearRowStep[r], sp.nearRowY[r], fs.rect.size * sp.nearRowScale[r], Foot);
                        sp.nearFans[r * sp.nearCols + c] = f;
                    }

                // thẻ ở mép khung: tướng ra khỏi tầm nhìn
                var edgeL = Layer(field, "the_mep");
                for (int i = 0; i < Lanes; i++)
                {
                    var ln = lanes[i];
                    var e = Img(edgeL, "mep_" + i, Sketch.Pill, new Color(1f, 0.98f, 0.92f, 0.96f), false, true);
                    ln.edge = TL(e.rectTransform, 78, 1000, new Vector2(118, 62), Mid);
                    ln.edgeFace = Portrait(kit, ln.edge, "mat", 54);
                    At(ln.edgeFace.Rect, Mid, new Vector2(-28, -30), new Vector2(54f * HeroArt.W / HeroArt.H, 54), Foot);
                    ln.edgeText = Txt(ln.edge, "met", 26, Theme.Ink);
                    At(ln.edgeText.rectTransform, Mid, new Vector2(26, 0), new Vector2(62, 42), Mid);
                    ln.edgeText.textWrappingMode = TextWrappingModes.NoWrap;
                    ln.edgeText.enableAutoSizing = true; ln.edgeText.fontSizeMin = 14; ln.edgeText.fontSizeMax = 26;
                    ln.edge.gameObject.SetActive(false);
                    lanes[i] = ln;
                }

                // lễ trao giải (dưới lớp hoa giấy): màn tối, bục 3 bậc trồi lên, ba tướng về đầu đứng trên bục
                var cer = Layer(field, "le_trao");
                var podDim = Img(cer, "toi", null, new Color(0.1f, 0.08f, 0.06f, 0.6f));
                HomeSceneMenu.Fill(podDim.rectTransform);
                var rise = N(cer, "buc_len");
                At(rise, Mid, new Vector2(0, PodY), Vector2.zero, Mid);
                var podSp = art["buc"];
                float pk = PodW / podSp.rect.width;
                var podImg = Img(rise, "buc", podSp, Color.white);
                At(podImg.rectTransform, Mid, Vector2.zero, podSp.rect.size * pk, Foot);
                Vector2 OnPod(Vector2 px) => new Vector2((px.x - podSp.rect.width / 2) * pk, (podSp.rect.height - px.y) * pk);
                var podSlots = new RaceScene.PodSlot[3];
                float[] podH = { 250, 215, 205 };
                for (int k = 0; k < 3; k++)
                {
                    var num = Txt(rise, "so_" + (k + 1), k == 0 ? 88 : 70, Theme.Ink2);
                    At(num.rectTransform, Mid, OnPod(art.podPlaque[k]), new Vector2(130, 110), Mid);
                    num.text = (k + 1).ToString();
                }
                for (int k = 0; k < 3; k++)
                {
                    var st = OnPod(art.podStand[k]);
                    var sl = new RaceScene.PodSlot();
                    sl.tag = Img(rise, "ten_" + (k + 1), Sketch.Pill, Theme.Paper, false, true);
                    At(sl.tag.rectTransform, Mid, new Vector2(st.x, -36), new Vector2(276, 52), Mid);
                    sl.name = Txt(sl.tag.transform, "chu", 26, Theme.Ink);
                    HomeSceneMenu.Fill(sl.name.rectTransform);
                    sl.name.textWrappingMode = TextWrappingModes.NoWrap;
                    sl.name.enableAutoSizing = true; sl.name.fontSizeMin = 14; sl.name.fontSizeMax = 26;
                    sl.root = At(N(rise, "hang_" + (k + 1)), Mid, st, new Vector2(10, 10), Foot);
                    sl.body = N(sl.root, "than");
                    At(sl.body, Foot, Vector2.zero, new Vector2(10, 10), Foot);
                    sl.portrait = Portrait(kit, sl.body, "chan_dung", podH[k]);
                    podSlots[k] = sl;
                }
                cer.gameObject.SetActive(false);

                // hoa giấy, chớp trắng
                var confL = Layer(field, "hoa_giay");
                sp.confetti = new Image[40];
                for (int i = 0; i < sp.confetti.Length; i++)
                {
                    sp.confetti[i] = Img(confL, "giay_" + i, null, Theme.Yellow);
                    TL(sp.confetti[i].rectTransform, 0, 0, new Vector2(i % 3 == 0 ? 24 : 16, i % 3 == 0 ? 14 : 26), Mid);
                    sp.confetti[i].enabled = false;
                }
                sp.flash = Img(field, "chop", null, new Color(1, 1, 1, 0));
                HomeSceneMenu.Fill(sp.flash.rectTransform);
                sp.flash.enabled = false;
                sp.feetTop = feetTop;
                sp.feetBottomInset = NearH + 22;
                stadium.Setup(sp);

                // ---------- giao diện trong vùng an toàn ----------
                var page = HomeSceneMenu.Fill(N(safe, "duong_dua"));

                // trên (ẩn lúc trao giải): thanh đường hôm nay kiêm bản đồ nhỏ, bảng treo ngay dưới
                var hud = HomeSceneMenu.Fill(N(page, "hud"));
                var boardSp = art["bang"];
                float bk = BoardW / boardSp.rect.width;
                var board = Img(hud, "bang_treo", boardSp, Color.white);
                At(board.rectTransform, TopMid, new Vector2(0, -(SceneRoot.BarHeight + 44)), boardSp.rect.size * bk, TopMid);
                var inner = new Rect(art.boardInner.x * bk, art.boardInner.y * bk, art.boardInner.width * bk, art.boardInner.height * bk);
                var boardFace = Portrait(kit, board.transform, "dan_dau", 96);
                TL(boardFace.Rect, inner.x + 56, inner.yMax + 2, new Vector2(96f * HeroArt.W / HeroArt.H, 96), Foot);
                var talk = Txt(board.transform, "tuong_thuat", 28, Theme.Hex("#f6f1e1"));
                TL(talk.rectTransform, inner.x + 112, inner.y + 4, new Vector2(inner.width - 124, inner.height - 8), new Vector2(0, 1));
                talk.alignment = TextAlignmentOptions.MidlineLeft;
                talk.enableAutoSizing = true; talk.fontSizeMin = 16; talk.fontSizeMax = 28;
                var strip = Img(hud, "duong_hom_nay", Sketch.PanelThin, paper, false, true);
                At(strip.rectTransform, TopMid, new Vector2(0, -(SceneRoot.BarHeight + 2)), new Vector2(1048, 54), TopMid);
                var track = Txt(strip.transform, "duong", 24, Theme.BlueD);
                At(track.rectTransform, new Vector2(0, 0.5f), new Vector2(20, 0), new Vector2(190, 40), new Vector2(0, 0.5f));
                track.alignment = TextAlignmentOptions.MidlineLeft;
                track.enableAutoSizing = true; track.fontSizeMin = 14; track.fontSizeMax = 24;
                track.textWrappingMode = TextWrappingModes.NoWrap;
                var map = N(strip.transform, "ban_do");
                At(map, new Vector2(0, 0.5f), new Vector2(218, 2), new Vector2(756, 30), new Vector2(0, 0.5f));
                var segs = new Image[3];
                var segNames = new TextMeshProUGUI[3];
                for (int i = 0; i < 3; i++)
                {
                    var sg = Img(map, "chang_" + i, null, Color.white);
                    sg.rectTransform.anchorMin = new Vector2(i / 3f, 0);
                    sg.rectTransform.anchorMax = new Vector2((i + 1) / 3f, 1);
                    sg.rectTransform.offsetMin = new Vector2(2, 0);
                    sg.rectTransform.offsetMax = new Vector2(-2, 0);
                    segs[i] = sg;
                    segNames[i] = Txt(sg.transform, "ten", 20, Theme.Ink);
                    HomeSceneMenu.Fill(segNames[i].rectTransform);
                }
                var mapFlag = Img(strip.transform, "co_dich", art["co_caro"], Color.white);
                At(mapFlag.rectTransform, new Vector2(1, 0.5f), new Vector2(-16, 0), new Vector2(46, 31), new Vector2(1, 0.5f));
                for (int i = 0; i < Lanes; i++)
                {
                    var ln = lanes[i];
                    ln.chip = N(map, "cham_" + i);
                    At(ln.chip, Vector2.zero, new Vector2(0, 2), new Vector2(26, 26), Mid);
                    ln.chipFill = Img(ln.chip, "to", Sketch.Dot, Theme.Yellow);
                    HomeSceneMenu.Fill(ln.chipFill.rectTransform);
                    var ring = Img(ln.chip, "vien", Sketch.Ring, Theme.Ink);
                    HomeSceneMenu.Fill(ring.rectTransform);
                    ln.chip.gameObject.SetActive(false);
                    lanes[i] = ln;
                }

                // chữ lớn giữa màn: đếm ngược, Nước rút!, Sát nút!
                var big = Txt(page, "chu_lon", 170, Theme.Yellow);
                At(big.rectTransform, Mid, new Vector2(0, -90), new Vector2(1040, 220), Mid);
                big.textWrappingMode = TextWrappingModes.NoWrap;
                big.enableAutoSizing = true; big.fontSizeMin = 60; big.fontSizeMax = 170;
                if (outline) big.fontSharedMaterial = outline;
                big.gameObject.SetActive(false);

                // quầy cược ở đáy màn (ẩn khi đua): tấm quầy gỗ mái sọc, từ trên xuống: vé lượt hôm nay + điểm cúp tuần, bảng trả thưởng,
                // 4 đồng chip mức cược, nút Đặt cược (chưa chọn con nào thì chỗ đó là dải băng nhắc chạm chọn)
                var lobby = HomeSceneMenu.Fill(N(page, "sanh"));
                var bottom = new Vector2(0.5f, 0);
                // Lão Mực đứng sau quầy (rig dùng chung với lều Đêm Bài): lớp thân vẽ SAU tấm quầy, lớp tay vẽ TRÊN tấm quầy (hai tay tì mép
                // quầy như tì mép bàn); mép bàn của rig (DealerRig.TableY) trùng mép trên quầy
                var dealerPos = new Vector2(DealerX, BoothH - 16 - DealerRig.TableY * DealerScale);
                DealerLayer DealerPart(string n)
                {
                    var rt = N(lobby, n, typeof(DealerLayer));
                    At(rt, bottom, dealerPos, new Vector2(1000, 1400), bottom);
                    return rt.GetComponent<DealerLayer>();
                }
                var dealerBack = DealerPart("lao_muc_sau");
                var boothSp = art["quay"];
                var booth = Img(lobby, "quay", boothSp, Color.white, true, true);
                booth.pixelsPerUnitMultiplier = boothSp.rect.width / 1080f; // viền (mái, khung) thu theo bề ngang, ván giữa giãn dọc
                At(booth.rectTransform, bottom, new Vector2(0, -36), new Vector2(1080, BoothH + 36), bottom);
                var dealerFront = DealerPart("lao_muc_truoc");
                var dealer = N(lobby, "lao_muc").gameObject.AddComponent<DealerRig>();
                var dealerFile = AssetDatabase.LoadAssetAtPath<TextAsset>(DealerRigPath);
                if (!dealerFile) Debug.LogWarning("[Đảo Casino] Thiếu rig Lão Mực " + DealerRigPath + ": quầy cược không có chủ quầy.");
                dealer.Setup(dealerFile, dealerBack, dealerFront, DealerScale);
                RectTransform InBooth(RectTransform rt, float x, float y, Vector2 size, Vector2 pivot) => TL(rt, x, y, size, pivot);
                // hàng 1: vé lượt hôm nay (trái), điểm cúp tuần (phải)
                var playsLabel = Txt(booth.transform, "luot", 26, Theme.Ink);
                InBooth(playsLabel.rectTransform, 74, 162, new Vector2(190, 44), new Vector2(0, 0.5f));
                playsLabel.alignment = TextAlignmentOptions.MidlineLeft;
                playsLabel.textWrappingMode = TextWrappingModes.NoWrap;
                playsLabel.enableAutoSizing = true; playsLabel.fontSizeMin = 16; playsLabel.fontSizeMax = 26;
                playsLabel.text = Loc.T("Lượt hôm nay");
                var tickets = new Image[5];
                var ticketSp = art["ve"];
                for (int i = 0; i < tickets.Length; i++)
                {
                    tickets[i] = Img(booth.transform, "ve_" + i, ticketSp, Color.white);
                    InBooth(tickets[i].rectTransform, 306 + i * 78, 162, ticketSp.rect.size * 0.5f, Mid);
                }
                var info = Txt(booth.transform, "tin", 26, Theme.Ink);
                InBooth(info.rectTransform, 1006, 162, new Vector2(320, 44), new Vector2(1, 0.5f));
                info.alignment = TextAlignmentOptions.MidlineRight;
                info.textWrappingMode = TextWrappingModes.NoWrap;
                info.enableAutoSizing = true; info.fontSizeMin = 16; info.fontSizeMax = 26;
                // hàng 2: bảng trả thưởng nhất / nhì / ba
                var legend = new TextMeshProUGUI[3];
                var legendIcons = new[] { art["cup"], art["no_bac"], art["no_dong"] };
                for (int i = 0; i < 3; i++)
                {
                    float cx = 200 + i * 340;
                    var icon = Img(booth.transform, "thuong_" + i, legendIcons[i], Color.white);
                    icon.preserveAspect = true;
                    InBooth(icon.rectTransform, cx - 92, 226, new Vector2(56, 56), Mid);
                    legend[i] = Txt(booth.transform, "tra_" + i, 30, Theme.Ink);
                    InBooth(legend[i].rectTransform, cx - 56, 226, new Vector2(230, 48), new Vector2(0, 0.5f));
                    legend[i].alignment = TextAlignmentOptions.MidlineLeft;
                    legend[i].textWrappingMode = TextWrappingModes.NoWrap;
                    legend[i].enableAutoSizing = true; legend[i].fontSizeMin = 16; legend[i].fontSizeMax = 30;
                }
                // hàng 3: 4 đồng chip mức cược; vòng sáng quanh chip đang chọn (RaceScene dời sang chip được chọn)
                var chips = new RaceTap[4];
                var chipTexts = new TextMeshProUGUI[4];
                for (int i = 0; i < chips.Length; i++)
                {
                    var csp = art["chip_" + i];
                    var chip = Img(booth.transform, "chip_" + i, csp, Color.white, true);
                    InBooth(chip.rectTransform, 150 + i * 260, 318, new Vector2(112, 112), Mid);
                    chips[i] = chip.gameObject.AddComponent<RaceTap>();
                    chipTexts[i] = Txt(chip.transform, "so", 30, Theme.Ink);
                    HomeSceneMenu.Fill(chipTexts[i].rectTransform);
                    chipTexts[i].textWrappingMode = TextWrappingModes.NoWrap;
                    chipTexts[i].enableAutoSizing = true; chipTexts[i].fontSizeMin = 16; chipTexts[i].fontSizeMax = 30;
                }
                var chipRing = Img(chips[0].transform, "dang_chon", Sketch.Ring, Theme.Yellow);
                At(chipRing.rectTransform, Mid, Vector2.zero, new Vector2(140, 140), Mid);
                chipRing.transform.SetAsFirstSibling();
                // hàng 4: nút Đặt cược; chưa chạm chọn con nào thì hiện dải băng nhắc
                var ribbonSp = art["bang_ron"];
                var ribbon = Img(lobby, "nhac", ribbonSp, Color.white, false, true);
                ribbon.pixelsPerUnitMultiplier = ribbonSp.rect.height / 84f;
                At(ribbon.rectTransform, bottom, new Vector2(0, 58), new Vector2(760, 84), bottom);
                var hero = Txt(ribbon.transform, "chu", 28, Theme.Paper);
                HomeSceneMenu.Fill(hero.rectTransform).offsetMin = new Vector2(70, 0);
                hero.rectTransform.offsetMax = new Vector2(-70, 0);
                hero.textWrappingMode = TextWrappingModes.NoWrap;
                hero.enableAutoSizing = true; hero.fontSizeMin = 16; hero.fontSizeMax = 28;
                var go = HomeSceneMenu.Button(assets, lobby, "dua", Loc.T("Đặt cược"), BtnColor.Green, new Vector2(640, 112));
                At((RectTransform)go.transform, bottom, new Vector2(0, 44), new Vector2(640, 112), bottom);
                // Nhận quà tuần: nổi ngay trên mép phải quầy khi đủ điểm
                var claim = HomeSceneMenu.Button(assets, lobby, "nhan_tuan", Loc.T("Nhận quà tuần"), BtnColor.Yellow, new Vector2(340, 80));
                At((RectTransform)claim.transform, Vector2.zero, new Vector2(24, BoothH + 10), new Vector2(340, 80), Vector2.zero); // mép trái: mép phải là chỗ Lão Mực

                // lúc đua: chỉ còn nút Cổ vũ (khán đài hò reo) và dòng chữ cổ vũ
                var cheer = HomeSceneMenu.Button(assets, page, "co_vu", Loc.T("Cổ vũ!"), BtnColor.Yellow, new Vector2(190, 190));
                At((RectTransform)cheer.transform, bottom, new Vector2(0, 140), new Vector2(190, 190), Mid);
                var cheerText = Txt(page, "co_vu_chu", 40, Color.white);
                At(cheerText.rectTransform, bottom, new Vector2(0, 262), new Vector2(1000, 60), bottom);
                if (outline) cheerText.fontSharedMaterial = outline;

                // kết quả trên lễ trao giải: huy hiệu (cúp / nơ), hạng, thưởng, bảng xếp hạng cả đoàn, Đua lại / Xong
                var res = HomeSceneMenu.Fill(N(page, "ket_qua"));
                var resIcon = Img(res, "huy_hieu", art["cup"], Color.white);
                resIcon.preserveAspect = true;
                At(resIcon.rectTransform, Mid, new Vector2(0, 682), new Vector2(150, 150), Mid);
                var rTitle = Txt(res, "hang", 88, Theme.Yellow);
                At(rTitle.rectTransform, Mid, new Vector2(0, 560), new Vector2(1000, 110), Mid);
                rTitle.textWrappingMode = TextWrappingModes.NoWrap;
                rTitle.enableAutoSizing = true; rTitle.fontSizeMin = 48; rTitle.fontSizeMax = 88;
                if (outline) rTitle.fontSharedMaterial = outline;
                var rewardBg = Img(res, "thuong", Sketch.PanelThin, Theme.Paper, false, true);
                At(rewardBg.rectTransform, Mid, new Vector2(0, PodY - 130), new Vector2(900, 104), Mid);
                var rInfo = Txt(rewardBg.transform, "chu", 32, Theme.Ink);
                HomeSceneMenu.Fill(rInfo.rectTransform);
                rInfo.enableAutoSizing = true; rInfo.fontSizeMin = 20; rInfo.fontSizeMax = 32;
                var rowsBg = Img(res, "bang", Sketch.PanelThin, Theme.Paper2, false, true);
                At(rowsBg.rectTransform, Mid, new Vector2(0, PodY - 194), new Vector2(900, 244), TopMid);
                var rRows = new TextMeshProUGUI[Lanes];
                for (int i = 0; i < Lanes; i++)
                {
                    rRows[i] = Txt(rowsBg.transform, "dong_" + i, 26, Theme.Ink);
                    At(rRows[i].rectTransform, TopMid, new Vector2(0, -12 - i * 44), new Vector2(860, 42), TopMid);
                    rRows[i].enableAutoSizing = true; rRows[i].fontSizeMin = 16; rRows[i].fontSizeMax = 26;
                    rRows[i].alignment = TextAlignmentOptions.MidlineLeft;
                }
                var again = HomeSceneMenu.Button(assets, res, "dua_lai", Loc.T("Đua tiếp"), BtnColor.Green, new Vector2(300, 110));
                At((RectTransform)again.transform, bottom, new Vector2(-170, 44), new Vector2(300, 110), bottom);
                var done = HomeSceneMenu.Button(assets, res, "xong", Loc.T("Xong"), BtnColor.Paper, new Vector2(300, 110));
                At((RectTransform)done.transform, bottom, new Vector2(170, 44), new Vector2(300, 110), bottom);
                res.gameObject.SetActive(false);

                scene.Setup(info, track, talk, claim, field, stadium, map, segs, segNames, lanes, boardFace, big, hero, go, cheer,
                    cheerText, res.gameObject, rTitle, rInfo, rRows, again, done, lobby.gameObject, hud.gameObject, cer.gameObject,
                    rise, podDim, podSlots, resIcon, new[] { art["cup"], art["no_bac"], art["no_dong"] }, chips, chipTexts, chipRing.rectTransform,
                    legend, tickets, art["ve"], art["ve_het"], trackTap, dealer);
                PrefabUtility.SaveAsPrefabAsset(root, ScreenPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            MakeScene();
            AssetDatabase.SaveAssets();
            Debug.Log("[Đảo Casino] Đã dựng " + ScreenPath + ", " + ScenePath);
        }

        static void MakeScene()
        {
            if (!File.Exists(ScenePath))
            {
                var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
                var prev = SceneManager.GetActiveScene();
                SceneManager.SetActiveScene(scene);
                ((GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(ScreenPath))).name = SceneIds.CasinoRace;
                SceneManager.SetActiveScene(prev);
                EditorSceneManager.SaveScene(scene, ScenePath);
                EditorSceneManager.CloseScene(scene, true);
            }
            else
            {
                var scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Additive);
                foreach (var go in scene.GetRootGameObjects())
                    if (PrefabUtility.IsPartOfPrefabInstance(go))
                        PrefabUtility.RevertPrefabInstance(PrefabUtility.GetOutermostPrefabInstanceRoot(go), InteractionMode.AutomatedAction);
                EditorSceneManager.SaveScene(scene);
                EditorSceneManager.CloseScene(scene, true);
            }
            var list = EditorBuildSettings.scenes.ToList();
            if (list.All(x => x.path != ScenePath))
            {
                list.Add(new EditorBuildSettingsScene(ScenePath, true));
                EditorBuildSettings.scenes = list.ToArray();
            }
        }

        // ---------- chụp thử ----------

        static string ShotDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "casino_dua");

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(ShotDir);
            foreach (var f in Directory.GetFiles(ShotDir, "*.jpg")) File.Delete(f);
            try
            {
                var s = App.Save.Data;
                s.level = Mathf.Max(s.level, 75);
                s.balls = Mathf.Max(s.balls, 3000);
                foreach (var h in App.Data.Heroes.Where(h => !h.minion).Take(8)) s.Hero(h.id).owned = true;
                Casino.Of(s).intro = true;
                App.Router.Go(SceneIds.CasinoRace, Casino.Race);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.CasinoRace) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(1.2f);
                App.Modals.CloseAll();
                yield return Shot("1_truoc_dua");
                var sc = Object.FindAnyObjectByType<RaceScene>();
                var taps = sc.GetComponentsInChildren<RaceTap>(true);
                sc.PickRunner(2);
                yield return new WaitForSecondsRealtime(0.6f);
                yield return Shot("1a_chon_con");
                taps.First(t => t.name == "chip_2").SimulateClick();
                yield return new WaitForSecondsRealtime(0.3f);
                yield return Shot("1a_chon_chip");
                sc.GetComponentsInChildren<SketchButton>(true).First(b => b.name == "dua").SimulateClick();
                yield return new WaitForSecondsRealtime(0.5f);
                yield return Shot("1b_dem_nguoc");
                float cheerAt = 4;
                float t1 = Time.realtimeSinceStartup;
                bool mid = false, stunShot = false, sprint = false, fin = false;
                while (sc.Game != null && !sc.Game.done && Time.realtimeSinceStartup - t1 < 70)
                {
                    if (Time.realtimeSinceStartup - t1 > cheerAt)
                    {
                        cheerAt += 5;
                        var cv = sc.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(b => b.name == "co_vu" && b.gameObject.activeInHierarchy);
                        if (cv) cv.SimulateClick();
                    }
                    if (!mid && Time.realtimeSinceStartup - t1 > 7)
                    {
                        mid = true;
                        File.WriteAllText(Path.Combine(ShotDir, "rig.txt"), sc.RigReport());
                        yield return Shot("2_dang_dua");
                    }
                    if (!stunShot && sc.Game.events.Any(e => e.kind == RaceEv.Hit))
                    {
                        stunShot = true;
                        yield return Shot("2b_danh_0");
                        yield return new WaitForSecondsRealtime(0.12f);
                        yield return Shot("2b_danh_1");
                        yield return new WaitForSecondsRealtime(0.2f);
                        yield return Shot("2b_danh_2");
                        yield return new WaitForSecondsRealtime(0.4f);
                        yield return Shot("2b_danh_3");
                    }
                    if (!sprint && sc.Game.runners.Any(r => r.pos >= sc.Game.Length(App.Data.Cfg.casino.race) * 0.84))
                    {
                        sprint = true;
                        yield return Shot("2c_nuoc_rut");
                    }
                    if (!fin && sc.Game.events.Any(e => e.kind == RaceEv.Finish))
                    {
                        fin = true;
                        yield return new WaitForSecondsRealtime(0.15f);
                        yield return Shot("2d_ve_dich_0");
                        yield return new WaitForSecondsRealtime(0.5f);
                        yield return Shot("2d_ve_dich_1");
                    }
                    yield return null;
                }
                yield return new WaitForSecondsRealtime(2.0f);
                yield return Shot("3_len_buc");
                yield return new WaitForSecondsRealtime(1.7f);
                yield return Shot("3b_trao_giai");
                var g = sc.Game;
                if (g != null)
                    Debug.Log($"[Thử] Đua: {g.runners.Count} tướng, {g.events.Count(e => e.kind == RaceEv.Hit)} cú trúng, " +
                              $"{g.events.Count(e => e.kind == RaceEv.Trip || e.kind == RaceEv.Dodge)} hụt / né, hạng mình {Race.PlaceOf(g) + 1}, {g.t:F1} giây");
                Debug.Log("[Thử] Xong Trường đua: " + Path.GetFullPath(ShotDir));
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(ShotDir, name + ".jpg"), tex.EncodeToJPG(82));
            Object.DestroyImmediate(tex);
        }

        static double nextPoll, tourStart;
        static bool tourRunning;
        static string Flag(string n) => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/" + n));

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating) return;
            var build = Flag("casino_race_build.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(build))
            {
                File.Delete(build);
                Build();
                return;
            }
            var tour = Flag("casino_race_tour.flag");
            if (File.Exists(tour) && !tourRunning)
            {
                if (!EditorApplication.isPlaying)
                {
                    if (!EditorApplication.isPlayingOrWillChangePlaymode) EditorApplication.isPlaying = true;
                    return;
                }
                Application.runInBackground = true; // Unity nằm nền thì vòng game đứng
                if (App.I == null || App.Router == null || App.Router.Busy || App.Router.Current == null) return;
                File.Delete(tour);
                tourRunning = true;
                tourStart = EditorApplication.timeSinceStartup;
                App.I.StartCoroutine(TourThenStop());
                return;
            }
            if (tourRunning && EditorApplication.timeSinceStartup - tourStart > 150)
            {
                tourRunning = false;
                EditorApplication.isPlaying = false;
            }
        }

        static IEnumerator TourThenStop()
        {
            yield return new WaitForSecondsRealtime(3f);
            yield return Run();
            yield return new WaitForSecondsRealtime(1f);
            tourRunning = false;
            EditorApplication.isPlaying = false;
        }
    }
}
