// Hộp Chuẩn bị trận: mỗi đối thủ một hàng, tướng bên trái, thông tin bên phải (người dùng dặn 2026-11-04: phóng to hết thông tin, tên,
// hệ…; cấp của tướng, địch rõ; trước đó: chỉ số địch rõ, không so với tướng người chơi).
// Menu "PokiClash/Prefab/Hộp chuẩn bị: ô đối thủ trái phải" dựng lại từ đầu (chạy lại thì dựng lại):
// - Items/DoiThu (PrepFoe, hàng to cho ải một địch, cao Big.H): ô chân dung trái; phải là tên, [nhãn hệ][viên lực chiến], dòng ghi
//   chú, 3 hàng [icon][Máu/Công/Thủ][số];
// - Items/DoiThuGon (hàng gọn cho ải 2–3 địch, cao Row.H, nền giấy nhạt): tên, [nhãn hệ][lực chiến][ghi chú], Máu Công Thủ xếp ngang;
// - cả hai: chip cấp (Kit/Chip, icon exp như chip cấp trên thanh trên) ở góc trên trái ô chân dung;
// - Dialogs/ChuanBiTran: gán foePrefab, foeRowPrefab; khung "doi_thu" cao mặc định bằng một hàng to (StagePrepDialog đặt lại theo số
//   địch); chip cấp góc trên trái 3 ô đội (Slot.level); chữ đầu mục "Đối thủ" gán foeTitle (ghi luật tiến hóa).
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class PrepStatsMenu
    {
        const string FoePath = "Assets/04 Prefabs/Items/DoiThu.prefab";
        const string RowPath = "Assets/04 Prefabs/Items/DoiThuGon.prefab";
        const string PrepPath = "Assets/04 Prefabs/Dialogs/ChuanBiTran.prefab";
        const float FramePad = 12; // như StagePrepDialog.FoePad
        static readonly string[] Icons = { "heart", "sword", "shield" };
        static readonly string[] Labels = { "Máu", "Công", "Thủ" };
        static readonly string[] Keys = { "mau", "cong", "thu" };

        // số đo một kiểu hàng (toạ độ tính từ góc trên trái hàng, điểm khung 1080). Ô chữ Baloo cao ~1,8 lần cỡ chữ (dòng của Baloo
        // cao 1,6 lần): ô thấp hơn dòng thì chế độ cắt "…" ẩn cả dòng, chữ tự co thì co nhỏ hơn ý muốn
        sealed class Spec
        {
            public float H; // cao hàng
            public Vector2 boxPos, box; // ô chân dung
            public Vector2 chipPos, chip; // chip cấp (cao, rộng)
            public float x0; // mép trái cột thông tin
            public float nameTop, nameH, nameSize, nameMin;
            public float line2Top, tagH, powerSize, powerIcon;
            public bool noteInLine; // ghi chú chung hàng với nhãn hệ (hàng gọn)
            public float noteTop, noteSize;
            public bool statsDown; // Máu, Công, Thủ xếp dọc có chữ (hàng to) hay xếp ngang (hàng gọn)
            public float statsTop, statRow, statIcon, statSize, labelSize, labelW, groupW;
            public bool bg;
        }

        static readonly Spec Big = new Spec
        {
            H = 340, boxPos = new Vector2(14, 12), box = new Vector2(250, 316), chipPos = new Vector2(6, 6), chip = new Vector2(64, 196),
            x0 = 284, nameTop = -6, nameH = 98, nameSize = 54, nameMin = 34,
            line2Top = 84, tagH = 50, powerSize = 40, powerIcon = 40,
            noteTop = 130, noteSize = 32,
            statsDown = true, statsTop = 190, statRow = 48, statIcon = 42, statSize = 48, labelSize = 32, labelW = 96,
        };

        static readonly Spec Row = new Spec
        {
            H = 180, boxPos = new Vector2(10, 6), box = new Vector2(150, 168), chipPos = new Vector2(4, 4), chip = new Vector2(52, 160),
            x0 = 172, nameTop = -8, nameH = 84, nameSize = 46, nameMin = 30,
            line2Top = 66, tagH = 44, powerSize = 36, powerIcon = 36, noteInLine = true, noteSize = 28,
            statsTop = 122, statRow = 50, statIcon = 40, statSize = 42, groupW = 180, bg = true,
        };

        static ArtLibrary art;
        static UiKit kit;

        [MenuItem("PokiClash/Prefab/Hộp chuẩn bị: ô đối thủ trái phải", priority = 67)]
        static void Build()
        {
            var assets = Load<UiAssets>();
            Theme.Init(assets); // phông, sprite giấy, viền chữ nướng sẵn
            art = Load<ArtLibrary>();
            kit = assets.prefabs;
            var big = BuildFoe(FoePath, "DoiThu", Big);
            var row = BuildFoe(RowPath, "DoiThuGon", Row);
            Edit(PrepPath, root => PatchPrep(root, big, row));
            AssetDatabase.SaveAssets();
            Debug.Log($"[Chuẩn bị] Đã dựng {FoePath} (cao {Big.H}), {RowPath} (cao {Row.H}); gán vào {PrepPath}, chip cấp ở ô đội.");
        }

        static PrepFoe BuildFoe(string path, string name, Spec s)
        {
            var root = new GameObject(name, typeof(RectTransform), typeof(PrepFoe));
            try
            {
                // neo mép trên khung đối thủ, giãn ngang
                var rt = (RectTransform)root.transform;
                rt.anchorMin = new Vector2(0, 1);
                rt.anchorMax = new Vector2(1, 1);
                rt.pivot = new Vector2(0.5f, 1);
                rt.sizeDelta = new Vector2(-2 * FramePad, s.H);
                rt.anchoredPosition = new Vector2(0, -FramePad);
                if (s.bg) Img(rt, "nen", Sketch.PanelThin, new Color(1, 1, 1, 0.5f), true).rectTransform.Stretch();

                var box = Node(rt, "o_chan_dung");
                TopLeft(box, s.boxPos, s.box);
                var portrait = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, box)).GetComponent<HeroPortrait>();
                portrait.name = "chan_dung";
                portrait.Rect.anchorMin = portrait.Rect.anchorMax = new Vector2(0.5f, 0.5f);
                portrait.Rect.anchoredPosition = Vector2.zero;
                portrait.Rect.sizeDelta = new Vector2(s.box.y * HeroArt.W / HeroArt.H, s.box.y);

                var chip = ((GameObject)PrefabUtility.InstantiatePrefab(kit.chip.gameObject, rt)).GetComponent<UiChip>();
                chip.name = "cap";
                chip.Set(Icon("exp"), Color.white, "Cấp 1");
                chip.SetHeight(s.chip.x, s.chip.y);
                TopLeft(chip.Rect, s.chipPos + new Vector2(6, 0), chip.Rect.sizeDelta); // icon tròn lấn ra mép trái 6

                var heroName = Text(rt, "ten", Theme.Title, s.nameSize, Theme.Ink, TextAlignmentOptions.MidlineLeft);
                TopStretch(heroName.rectTransform, s.x0, s.nameTop, s.nameH);
                heroName.enableAutoSizing = true;
                heroName.fontSizeMin = s.nameMin;
                heroName.fontSizeMax = s.nameSize;
                heroName.overflowMode = TextOverflowModes.Ellipsis;
                heroName.text = "Tên tướng";

                // hàng 2: nhãn hệ, viên lực chiến (và ghi chú ở hàng gọn), xếp ngang theo cỡ
                var line = Node(rt, "hang_2", typeof(HorizontalLayoutGroup));
                TopStretch(line, s.x0, s.line2Top, s.tagH + 8);
                var hl = line.GetComponent<HorizontalLayoutGroup>();
                hl.childAlignment = TextAnchor.MiddleLeft;
                hl.spacing = 12;
                hl.childControlWidth = hl.childControlHeight = true;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var elem = ((GameObject)PrefabUtility.InstantiatePrefab(kit.elemTag.gameObject, line)).GetComponent<UiElemTag>();
                elem.SetHeight(s.tagH);
                var ele = elem.gameObject.AddComponent<LayoutElement>();
                ele.minWidth = ele.preferredWidth = s.tagH * 2.4f;
                ele.minHeight = ele.preferredHeight = s.tagH;
                var power = PowerPill(line, s);

                TextMeshProUGUI note;
                if (s.noteInLine)
                {
                    // ghi chú lấy phần còn lại của hàng (không chen nhãn hệ, lực chiến)
                    note = Text(line, "ghi_chu", Theme.Bold, s.noteSize, Theme.Red, TextAlignmentOptions.MidlineLeft);
                    var nle = note.gameObject.AddComponent<LayoutElement>();
                    nle.minWidth = nle.preferredWidth = 0;
                    nle.flexibleWidth = 1;
                    nle.preferredHeight = s.noteSize * 1.9f;
                }
                else
                {
                    note = Text(rt, "ghi_chu", Theme.Bold, s.noteSize, Theme.Red, TextAlignmentOptions.MidlineLeft);
                    TopStretch(note.rectTransform, s.x0, s.noteTop, s.noteSize * 1.9f);
                }
                note.enableAutoSizing = true; // ghi chú dài (Boss · Cường hóa +15%) co lại cho vừa phần còn lại của hàng
                note.fontSizeMin = 20;
                note.fontSizeMax = s.noteSize;
                note.text = "Boss";

                var stats = new TextMeshProUGUI[3];
                var block = Node(rt, "chi_so");
                if (s.statsDown) TopLeft(block, new Vector2(s.x0, s.statsTop), new Vector2(s.labelW + 330, s.statRow * 3));
                else TopStretch(block, s.x0, s.statsTop, s.statRow);
                for (int i = 0; i < 3; i++)
                {
                    var r = Node(block, "hang_" + Keys[i]);
                    float rowW = s.statsDown ? s.labelW + 330 : s.groupW;
                    TopLeft(r, s.statsDown ? new Vector2(0, i * s.statRow) : new Vector2(i * s.groupW, 0), new Vector2(rowW, s.statRow));
                    Img(r, "icon", Icon(Icons[i]), Color.white).rectTransform
                        .Place(new Vector2(0, 0.5f), Vector2.zero, new Vector2(s.statIcon, s.statIcon), new Vector2(0, 0.5f));
                    float x = s.statIcon + 10;
                    if (s.statsDown)
                    {
                        var label = Text(r, "chu", Theme.Body, s.labelSize, Theme.Ink3, TextAlignmentOptions.MidlineLeft);
                        label.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(x, 0), new Vector2(s.labelW, s.statRow), new Vector2(0, 0.5f));
                        label.text = Labels[i];
                        x += s.labelW;
                    }
                    var value = Text(r, "so", Theme.Title, s.statSize, Theme.Ink2, TextAlignmentOptions.MidlineLeft);
                    value.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(x, 2), new Vector2(rowW - x, s.statRow), new Vector2(0, 0.5f));
                    value.text = "0";
                    stats[i] = value;
                }

                root.GetComponent<PrepFoe>().Setup(portrait, box, heroName, chip, elem, note.gameObject, power, stats);
                return PrefabUtility.SaveAsPrefabAsset(root, path).GetComponent<PrepFoe>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // viên lực chiến: [kiếm][số đỏ] trên nền viên giấy, rộng theo số (hàng cha xếp theo cỡ ưa thích); trả chữ số
        static TextMeshProUGUI PowerPill(Transform parent, Spec s)
        {
            var row = Node(parent, "luc_chien", typeof(Image), typeof(HorizontalLayoutGroup));
            var img = row.GetComponent<Image>();
            Theme.SetSprite(img, Sketch.Pill);
            img.type = Image.Type.Sliced;
            img.color = Theme.CardFill;
            img.raycastTarget = false;
            var hl = row.GetComponent<HorizontalLayoutGroup>();
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.spacing = 6;
            hl.padding = new RectOffset(10, 18, 2, 2);
            hl.childControlWidth = hl.childControlHeight = true;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            var le = row.gameObject.AddComponent<LayoutElement>();
            le.minHeight = le.preferredHeight = s.tagH;
            var ic = Img(row, "icon", Icon("sword"), Color.white);
            var ile = ic.gameObject.AddComponent<LayoutElement>();
            ile.minWidth = ile.preferredWidth = ile.minHeight = ile.preferredHeight = s.powerIcon;
            var t = Text(row, "so", Theme.Title, s.powerSize, Theme.RedD, TextAlignmentOptions.MidlineLeft);
            t.text = "0";
            return t;
        }

        static void PatchPrep(GameObject root, PrepFoe big, PrepFoe row)
        {
            var dlg = root.GetComponent<StagePrepDialog>();
            var so = new SerializedObject(dlg);
            so.FindProperty("foePrefab").objectReferenceValue = big;
            so.FindProperty("foeRowPrefab").objectReferenceValue = row;

            var foes = Find(root.transform, "doi_thu");
            for (int i = foes.childCount - 1; i >= 0; i--) Object.DestroyImmediate(foes.GetChild(i).gameObject); // hàng mẫu cũ (nếu có)
            foes.GetComponent<LayoutElement>().preferredHeight = Big.H + 2 * FramePad;
            // chữ đầu mục ngay trước khung đối thủ
            var title = foes.parent.GetChild(foes.GetSiblingIndex() - 1).GetComponent<TextMeshProUGUI>();
            if (title && title.text.StartsWith("Đối thủ")) so.FindProperty("foeTitle").objectReferenceValue = title;
            else Debug.LogError("[Chuẩn bị] Không thấy chữ \"Đối thủ\" ngay trước khung doi_thu");

            // chip cấp góc trên trái ô đội (cấp tướng của người chơi)
            var slots = so.FindProperty("p.slots");
            for (int i = 0; i < slots.arraySize; i++)
            {
                var slot = slots.GetArrayElementAtIndex(i);
                var bg = (Image)slot.FindPropertyRelative("bg").objectReferenceValue;
                if (!bg) continue;
                Remove(bg.transform, "cap");
                var chip = ((GameObject)PrefabUtility.InstantiatePrefab(kit.chip.gameObject, bg.transform)).GetComponent<UiChip>();
                chip.name = "cap";
                chip.Set(Icon("exp"), Color.white, "Cấp 1");
                chip.SetHeight(46, 140);
                TopLeft(chip.Rect, new Vector2(12, 6), chip.Rect.sizeDelta);
                slot.FindPropertyRelative("level").objectReferenceValue = chip;
            }
            so.ApplyModifiedPropertiesWithoutUndo();
        }

        // ---------- công cụ ----------

        static Sprite Icon(string n) => art ? art.Icon(n) : null;

        // neo góc trên trái của cha, pos tính xuống dưới
        static void TopLeft(RectTransform rt, Vector2 pos, Vector2 size)
        {
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0, 1);
            rt.anchoredPosition = new Vector2(pos.x, -pos.y);
            rt.sizeDelta = size;
        }

        // giãn ngang từ left tới cách mép phải 16, cách mép trên top, cao h
        static void TopStretch(RectTransform rt, float left, float top, float h)
        {
            rt.anchorMin = new Vector2(0, 1);
            rt.anchorMax = new Vector2(1, 1);
            rt.pivot = new Vector2(0, 1);
            rt.offsetMin = new Vector2(left, -top - h);
            rt.offsetMax = new Vector2(-16, -top);
        }

        static T Load<T>() where T : Object =>
            AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:" + typeof(T).Name)[0]));

        static void Edit(string path, System.Action<GameObject> patch)
        {
            var root = PrefabUtility.LoadPrefabContents(path);
            try
            {
                patch(root);
                PrefabUtility.SaveAsPrefabAsset(root, path);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        static Transform Find(Transform t, string name)
        {
            foreach (var c in t.GetComponentsInChildren<Transform>(true))
                if (c.name == name) return c;
            return null;
        }

        static void Remove(Transform parent, string name)
        {
            for (int i = parent.childCount - 1; i >= 0; i--)
                if (parent.GetChild(i).name == name) Object.DestroyImmediate(parent.GetChild(i).gameObject);
        }

        static RectTransform Node(Transform parent, string name, params System.Type[] comps)
        {
            var go = new GameObject(name, typeof(RectTransform));
            foreach (var c in comps) go.AddComponent(c);
            go.transform.SetParent(parent, false);
            return (RectTransform)go.transform;
        }

        static Image Img(Transform parent, string name, Sprite sprite, Color color, bool sliced = false)
        {
            var img = Node(parent, name, typeof(Image)).GetComponent<Image>();
            Theme.SetSprite(img, sprite);
            img.type = sliced ? Image.Type.Sliced : Image.Type.Simple;
            img.preserveAspect = !sliced;
            img.color = color;
            img.raycastTarget = false;
            return img;
        }

        static TextMeshProUGUI Text(Transform parent, string name, TMP_FontAsset font, float size, Color color, TextAlignmentOptions align)
        {
            var t = Node(parent, name, typeof(TextMeshProUGUI)).GetComponent<TextMeshProUGUI>();
            t.font = font;
            t.fontSize = size;
            t.color = color;
            t.alignment = align;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Overflow;
            t.raycastTarget = false;
            t.text = "";
            return t;
        }
    }
}
