// Thanh hải trình đầu màn đảo (ZoneHeader, người dùng 2026-11-27: "thanh này trong các đảo nhìn ổn nhưng chưa có sự ấn tượng và độc
// đáo, thử thiết kế sáng tạo hơn"). Menu "PokiClash/Prefab/Sảnh và đảo/Đảo: thanh hải trình" dựng nút "hai_trinh" trong Screens/Zone,
// cùng neo và mép trên với khung thông tin mỏng cũ (cha của ZoneProgressBar), rồi ẩn khung cũ và gán ZoneScene.header. Chạy lại được.
// Chỉ dùng sprite vẽ tay sẵn có (bộ Sketch nướng sẵn, ô vuông sảnh Shop/v3 o_san_*, icon hệ, ảnh rương của khung cũ, chân dung kit):
// - tấm giấy (PanelThin) cao 190;
// - bản 2 (người dùng 2026-11-27: "2 ô đầu cuối nhìn viền đậm và không rõ ràng, phải giấu finalboss đi cho bí ẩn"): hai đầu là ô vuông
//   150 viền trắng giấy như cột ô sảnh (ShopMenu.HubTileSprites: lòng ô tô màu, viền trắng, lớp đen mờ đáy), thay đĩa + vòng mực đậm;
// - ô hệ trái: lòng màu hệ nhạt (tô lúc chạy), icon hệ thở, "1/70" chữ trắng viền mực ở đáy; lòng ô nhận chạm;
// - đường mòn giữa: chấm mẫu (Dot), 7 rương (ảnh rương cũ, ClickCatcher, Wobble), ghim ải kế (viên màu hệ + mũi nhọn, chữ trắng viền);
// - ô boss phải: lòng đỏ, chân dung kit thở (bóng đen lúc chạy), dấu "?" chữ trắng viền mực, "BOSS" ở đáy, vương miện (tắt); nhận chạm;
// - dấu độ khó ở nửa trên tấm, sát bên trái ô boss, nghiêng.
using System.Linq;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using M = PokiClash.EditorTools.HomeSceneMenu;

namespace PokiClash.EditorTools
{
    public static class ZoneHeaderMenu
    {
        const string ZonePath = "Assets/04 Prefabs/Screens/Zone.prefab";
        const string NodeName = "hai_trinh";
        // cao tấm, cạnh hai ô vuông đầu cuối, lề từ mép tấm tới ô
        const float H = 190, T = 150, Pad = 18;

        // Temp/zone_header.flag: biên dịch xong và không Play thì dựng một lần rồi xoá cờ (Unity dùng chung nhiều phiên)
        static double nextPoll;

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || EditorApplication.isPlayingOrWillChangePlaymode) return;
            var f = System.IO.Path.GetFullPath(System.IO.Path.Combine(Application.dataPath, "../Temp/zone_header.flag"));
            if (!System.IO.File.Exists(f)) return;
            System.IO.File.Delete(f);
            Build();
        }

        [MenuItem("PokiClash/Prefab/Sảnh và đảo/Đảo: thanh hải trình", priority = 66)]
        public static void Build()
        {
            var assets = M.Load<UiAssets>();
            Theme.Init(assets);
            var kit = M.Load<UiKit>();
            var contents = PrefabUtility.LoadPrefabContents(ZonePath);
            try
            {
                var zone = contents.GetComponent<ZoneScene>();
                var so = new SerializedObject(zone);
                var bar = so.FindProperty("p.bar").objectReferenceValue as ZoneProgressBar;
                var old = bar ? bar.transform.parent as RectTransform : null;
                if (!old)
                {
                    Debug.LogError("[Đảo] Không thấy khung thông tin cũ (cha của ZoneProgressBar) trong " + ZonePath);
                    return;
                }
                var chestSprite = (so.FindProperty("p.chests").GetArrayElementAtIndex(0).FindPropertyRelative("image").objectReferenceValue as Image)?.sprite;
                var parent = old.parent;
                var prev = parent.Find(NodeName);
                if (prev) Object.DestroyImmediate(prev.gameObject);

                // cùng neo, cùng mép trên với khung cũ, cao H
                var root = M.Node(parent, NodeName);
                root.anchorMin = old.anchorMin;
                root.anchorMax = old.anchorMax;
                root.pivot = old.pivot;
                root.sizeDelta = new Vector2(old.sizeDelta.x, H);
                float oldTop = old.anchoredPosition.y + (1 - old.pivot.y) * old.sizeDelta.y;
                root.anchoredPosition = new Vector2(old.anchoredPosition.x, oldTop - (1 - old.pivot.y) * H);
                root.SetSiblingIndex(old.GetSiblingIndex() + 1);
                old.gameObject.SetActive(false);

                var paper = M.Img(root, "giay", Sketch.PanelThin, Theme.Paper, true, true);
                M.Fill(paper.rectTransform);
                paper.rectTransform.localEulerAngles = new Vector3(0, 0, -0.5f);

                var p = new ZoneHeader.Parts();
                var (nenS, vienS, dayS) = ShopMenu.HubTileSprites();

                // ---------- ô hệ (trái) ----------
                p.crest = M.At(M.Node(root, "o_he"), new Vector2(0, 0.5f), new Vector2(Pad + T / 2, 0), new Vector2(T, T), new Vector2(0.5f, 0.5f));
                p.crestFill = M.Img(p.crest, "nen_o", nenS, Color.Lerp(Theme.Green, Color.white, 0.5f), true);
                M.Fill(p.crestFill.rectTransform);
                p.crestClick = p.crestFill.gameObject.AddComponent<ClickCatcher>();
                M.Fill(M.Img(p.crest, "vien_o", vienS, Color.white).rectTransform);
                p.icon = M.Img(p.crest, "icon", null, Color.white);
                p.icon.preserveAspect = true;
                M.At(p.icon.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -T * 0.42f), new Vector2(T * 0.74f, T * 0.74f), new Vector2(0.5f, 0.5f));
                Breathe(p.icon.gameObject, 0.05f, 1.8f, 0);
                M.Fill(M.Img(p.crest, "day_o", dayS, Color.white).rectTransform);
                p.count = Label(p.crest, "so_ai", "1/70");

                // ---------- ô boss (phải): bóng đen + dấu "?" tới khi mở ải cuối ----------
                p.boss = M.At(M.Node(root, "o_boss"), new Vector2(1, 0.5f), new Vector2(-(Pad + T / 2), 0), new Vector2(T, T), new Vector2(0.5f, 0.5f));
                var bnen = M.Img(p.boss, "nen_o", nenS, Theme.Red, true);
                M.Fill(bnen.rectTransform);
                p.bossClick = bnen.gameObject.AddComponent<ClickCatcher>();
                M.Fill(M.Img(p.boss, "vien_o", vienS, Color.white).rectTransform);
                var hold = M.Node(p.boss, "khung");
                M.Fill(hold).offsetMin = new Vector2(16, 34);
                hold.offsetMax = new Vector2(-16, -14);
                Breathe(hold.gameObject, 0.03f, 2.4f, 0.4f);
                p.portrait = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, hold)).GetComponent<HeroPortrait>();
                p.portrait.name = "chan_dung";
                foreach (var g in p.portrait.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
                M.Fill(M.Img(p.boss, "day_o", dayS, Color.white).rectTransform);
                var q = M.Text(p.boss, "dau_hoi", 84, Color.white);
                M.At(q.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, 14), new Vector2(96, 110), new Vector2(0.5f, 0.5f));
                Outline(q, 0.3f);
                q.text = "?";
                p.mystery = q.rectTransform;
                p.bossLabel = Label(p.boss, "chu", "BOSS");
                var art = M.Load<ArtLibrary>();
                var crown = M.Img(p.boss, "vuong_mien", art ? art.Icon("crown") : null, Color.white);
                crown.preserveAspect = true;
                M.At(crown.rectTransform, new Vector2(0.5f, 1), new Vector2(0, 6), new Vector2(70, 70), new Vector2(0.5f, 0.5f));
                crown.rectTransform.localEulerAngles = new Vector3(0, 0, 8);
                p.crown = crown.gameObject;
                p.crown.SetActive(false);

                // ---------- dấu độ khó: nửa trên tấm, sát bên trái ô boss (không che bóng boss) ----------
                p.stamp = M.Img(root, "dau_do_kho", Sketch.Pill, Theme.Green, false, true);
                M.At(p.stamp.rectTransform, new Vector2(1, 0.5f), new Vector2(-(Pad + T + 32), 62), new Vector2(150, 48), new Vector2(0.5f, 0.5f));
                p.stamp.rectTransform.localEulerAngles = new Vector3(0, 0, -9);
                p.stampText = M.Text(p.stamp.transform, "chu", 28, Color.white);
                M.Fill(p.stampText.rectTransform).offsetMin = new Vector2(10, 2);
                p.stampText.rectTransform.offsetMax = new Vector2(-10, -2);
                Single(p.stampText, 14, 28);
                Outline(p.stampText, 0.22f);
                p.stampText.text = "Dễ";

                // ---------- đường mòn ----------
                float x0 = Pad + T + 26, x1 = x0; // lề hai đầu (từ mép trái / phải tấm)
                p.trail = M.Node(root, "duong_mon");
                p.trail.anchorMin = new Vector2(0, 0.5f);
                p.trail.anchorMax = new Vector2(1, 0.5f);
                p.trail.pivot = new Vector2(0.5f, 0.5f);
                p.trail.offsetMin = new Vector2(x0, -34 - 40);
                p.trail.offsetMax = new Vector2(-x1, -34 + 40);
                p.dash = M.Img(p.trail, "cham_mau", Sketch.Dot, Color.white);
                M.At(p.dash.rectTransform, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(16, 8), new Vector2(0.5f, 0.5f));
                p.dash.gameObject.SetActive(false);
                p.chests = new ZoneHeader.Chest[7];
                for (int i = 0; i < p.chests.Length; i++)
                {
                    var c = M.Img(p.trail, "ruong_" + i, chestSprite ? chestSprite : Sketch.Chest, Color.white, true);
                    c.preserveAspect = true;
                    M.At(c.rectTransform, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(60, 60), new Vector2(0.5f, 0.5f));
                    var w = c.gameObject.AddComponent<Wobble>();
                    w.enabled = false;
                    p.chests[i] = new ZoneHeader.Chest { image = c, click = c.gameObject.AddComponent<ClickCatcher>(), wobble = w };
                }
                // ghim ải kế: gốc ở mũi nhọn (chạm đường mòn), viên màu hệ phía trên
                p.pin = M.At(M.Node(p.trail, "ghim"), new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(104, 86), new Vector2(0.5f, 0));
                p.pinBg = M.Img(p.pin, "vien_mau", Sketch.Pill, Theme.Green, false, true);
                M.At(p.pinBg.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 26), new Vector2(104, 54), new Vector2(0.5f, 0));
                var tip = M.Img(p.pinBg.transform, "mui", Sketch.White, Theme.Green);
                M.At(tip.rectTransform, new Vector2(0.5f, 0), new Vector2(0, -6), new Vector2(26, 26), new Vector2(0.5f, 0.5f));
                tip.rectTransform.localEulerAngles = new Vector3(0, 0, 45);
                tip.transform.SetAsFirstSibling();
                p.pinText = M.Text(p.pinBg.transform, "chu", 30, Color.white);
                M.Fill(p.pinText.rectTransform).offsetMin = new Vector2(8, 2);
                p.pinText.rectTransform.offsetMax = new Vector2(-8, -2);
                Single(p.pinText, 16, 30);
                Outline(p.pinText, 0.24f);
                p.pinText.text = "Lv6";

                var header = root.gameObject.AddComponent<ZoneHeader>();
                header.Setup(p);
                zone.SetupHeader(header);
                EditorUtility.SetDirty(zone);
                PrefabUtility.SaveAsPrefabAsset(contents, ZonePath);
                Debug.Log($"[Đảo] Đã dựng thanh hải trình {NodeName} trong {ZonePath} (khung cũ {old.name} {old.sizeDelta} đã ẩn).");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // chữ trắng viền mực ở đáy ô (như chữ ô vuông sảnh), trên lớp đen mờ
        static TextMeshProUGUI Label(RectTransform tile, string name, string text)
        {
            var t = M.Text(tile, name, 32, Color.white);
            t.rectTransform.anchorMin = new Vector2(0, 0);
            t.rectTransform.anchorMax = new Vector2(1, 0);
            t.rectTransform.pivot = new Vector2(0.5f, 0);
            t.rectTransform.offsetMin = new Vector2(10, 10);
            t.rectTransform.offsetMax = new Vector2(-10, 54);
            Single(t, 18, 32);
            Outline(t, 0.28f);
            t.text = text;
            return t;
        }

        static void Breathe(GameObject go, float amount, float period, float phase)
        {
            var b = go.AddComponent<PokiClash.Breathe>();
            b.amount = amount;
            b.period = period;
            b.phase = phase;
        }

        static void Single(TextMeshProUGUI t, float min, float max)
        {
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.enableAutoSizing = true;
            t.fontSizeMin = min;
            t.fontSizeMax = max;
        }

        static void Outline(TextMeshProUGUI t, float w)
        {
            var m = Theme.Outlined(t.font, w);
            if (m) t.fontSharedMaterial = m;
        }
    }
}
