// Hộp AFK "Đội tự đi ải" bản mới (người dùng 2026-11-27: hộp cũ "nhìn không rõ ràng, khó hiểu và xấu", chọn hướng "cảnh + thanh mốc";
// rương vẽ tạm "cũng xấu" → rương gỗ thật có rig). Menu "PokiClash/Prefab/Hộp thoại và màn/AFK: hộp Đội tự đi ải" dựng (chạy lại thì
// dựng lại, giữ đường dẫn nên GUID và chỗ trỏ trong UiKit.dialogs giữ nguyên):
// - Items/RuongAfk (AfkSlot): nút giấy, rương Kit/Ruong (ảnh pk_ruong_go + rig) trong khung có CanvasGroup, chữ, thanh đếm giờ nhỏ;
// - Dialogs/Afk (AfkPanel) = bản sao tờ giấy gốc Dialogs/HopThoai rộng 1000, cỡ cố định: tiêu đề, nút (i) + tờ luật, thẻ cảnh (khung
//   cắt ảnh sàn đấu, chỗ tướng đứng, chip trạng thái, dải tên ải / mặt tướng / tỉ lệ mảnh / nút Đổi ải "afk_doi_ai"), hàng giờ (đồng
//   hồ, "x / 12 giờ", lượt rơi mảnh), thanh giờ Kit/bar kèm 23 vạch giờ và 4 hình rương mốc, khay 5 ô dựng sẵn, nút TV Mở ngay, hàng
//   nút TV Tăng tốc ×2 + Nhận mảnh; nhóm "khoa" (chưa qua ải nào: câu nhắc + OK). Chữ đổi theo số liệu để trống (lúc chạy điền).
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class AfkDialogMenu
    {
        const string SheetBase = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string DialogPath = "Assets/04 Prefabs/Dialogs/Afk.prefab";
        const string SlotPath = "Assets/04 Prefabs/Items/RuongAfk.prefab";
        const string ChestArt = "Assets/03 Art/Pachinko/pk_ruong_go.png";

        const float SheetW = 1000, SheetH = 1290, CardW = 940, CardH = 400, CardTop = -116, BandH = 104;
        const float HoursY = -540, BarY = -626, BarW = 880, BarH = 50, TrayHeadY = -710, TrayY = -770, SlotW = 168, SlotH = 210;
        const int Slots = 5, Ticks = 23, Marks = 4, Faces = 3;

        static readonly Color Dark = new Color(0.36f, 0.27f, 0.2f, 0.32f);

        static T Load<T>() where T : Object =>
            AssetDatabase.FindAssets("t:" + typeof(T).Name).Select(g => AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(g))).FirstOrDefault(a => a);

        static TextMeshProUGUI T(Transform p, string n, float size, Color c, Vector2 anchor, Vector2 pos, Vector2 box, Vector2 pivot,
            TextAlignmentOptions align = TextAlignmentOptions.MidlineLeft)
        {
            var t = HomeSceneMenu.Text(p, n, size, c, align);
            HomeSceneMenu.At(t.rectTransform, anchor, pos, box, pivot);
            t.enableAutoSizing = true;
            t.fontSizeMin = size * 0.6f;
            t.fontSizeMax = size;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            return t;
        }

        static SketchButton Btn(SketchButton prefab, Transform parent, string name, string label, BtnColor color, Vector2 anchor, Vector2 pos,
            Vector2 size, Vector2 pivot)
        {
            var b = ((GameObject)PrefabUtility.InstantiatePrefab(prefab.gameObject, parent)).GetComponent<SketchButton>();
            b.name = name;
            b.SetRole(color);
            b.SetText(label);
            HomeSceneMenu.At(b.Rect, anchor, pos, size, pivot);
            if (b.Label)
            {
                b.Label.enableAutoSizing = true;
                b.Label.fontSizeMax = b.Label.fontSize;
                b.Label.fontSizeMin = b.Label.fontSize * 0.55f;
                b.Label.textWrappingMode = TextWrappingModes.NoWrap;
            }
            return b;
        }

        // hình TV bên trái chữ của nút quảng cáo (Ads.Bind bật / tắt con tên "tv")
        static void Tv(SketchButton b, Sprite tv, float size)
        {
            var img = HomeSceneMenu.Img(b.transform, "tv", tv, Color.white);
            img.preserveAspect = true;
            HomeSceneMenu.At(img.rectTransform, new Vector2(0, 0.5f), new Vector2(18, 3), new Vector2(size, size), new Vector2(0, 0.5f));
            var lr = b.Label.rectTransform;
            lr.offsetMin = new Vector2(lr.offsetMin.x + size + 8, lr.offsetMin.y);
        }

        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/AFK: hộp Đội tự đi ải", priority = 66)]
        public static void Build()
        {
            var assets = Load<UiAssets>();
            var art = Load<ArtLibrary>();
            if (!assets || !art) return;
            Theme.Init(assets);
            var kit = assets.prefabs;
            if (!kit.bar || !kit.chest || !kit.buttonBig || !kit.buttonSmall || !kit.buttonNormal || !kit.buttonRound)
            {
                Debug.LogError("[AFK] UiKit thiếu bar / chest / nút");
                return;
            }
            var chestSp = AssetDatabase.LoadAssetAtPath<Sprite>(ChestArt);
            var slotPrefab = BuildSlot(kit);
            var white = Theme.Outlined(Theme.Bold, 0.25f);

            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetBase));
            try
            {
                root.name = "Afk";
                var view = root.GetComponent<ModalSheet>();
                view.Configure(SheetW, false, false);
                var sheet = view.Sheet;
                foreach (var f in sheet.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(f);
                foreach (var l in sheet.GetComponents<LayoutGroup>()) Object.DestroyImmediate(l);
                sheet.anchorMin = sheet.anchorMax = new Vector2(0.5f, 0.5f);
                sheet.pivot = new Vector2(0.5f, 0.5f);
                sheet.anchoredPosition = new Vector2(0, -10);
                sheet.sizeDelta = new Vector2(SheetW, SheetH);
                var page = HomeSceneMenu.Fill(HomeSceneMenu.Node(sheet, "noi_dung"));
                page.SetAsLastSibling();
                var close = view.Close ? (RectTransform)view.Close.transform : null;
                var top = new Vector2(0.5f, 1);

                var title = T(page, "tieu_de", 58, Theme.Ink, top, new Vector2(0, -26), new Vector2(640, 78), top, TextAlignmentOptions.Center);
                title.text = "Đội tự đi ải";
                var info = Btn(kit.buttonRound, page, "nut_luat", "", BtnColor.Paper, new Vector2(0, 1), new Vector2(40, -24), new Vector2(84, 84),
                    new Vector2(0, 1));
                var infoIcon = HomeSceneMenu.Img(info.transform, "icon", art.Icon("info"), Color.white);
                infoIcon.preserveAspect = true;
                HomeSceneMenu.At(infoIcon.rectTransform, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(52, 52), new Vector2(0.5f, 0.5f));

                // ---------- chưa qua ải nào ----------
                var lockG = HomeSceneMenu.Fill(HomeSceneMenu.Node(page, "khoa"));
                var lockText = T(lockG, "chu", 40, Theme.Ink, top, new Vector2(0, -380), new Vector2(860, 140), top, TextAlignmentOptions.Center);
                lockText.textWrappingMode = TextWrappingModes.Normal;
                lockText.text = "Qua ải 1 để đội tự đi ải khi bạn vắng mặt";
                var ok = Btn(kit.buttonBig, lockG, "nut_ok", "OK", BtnColor.Green, top, new Vector2(0, -600), new Vector2(360, 130), top);
                lockG.gameObject.SetActive(false);

                // ---------- nội dung ----------
                var open = HomeSceneMenu.Fill(HomeSceneMenu.Node(page, "mo"));

                // thẻ cảnh: khung giấy, khung cắt (ảnh sàn đấu, chỗ tướng, dải dưới), chip trạng thái
                var card = HomeSceneMenu.Img(open, "the_canh", Sketch.PanelThin, Theme.Paper, false, true);
                HomeSceneMenu.At(card.rectTransform, top, new Vector2(0, CardTop), new Vector2(CardW, CardH), top);
                var mask = HomeSceneMenu.Node(card.transform, "khung", typeof(RectMask2D));
                HomeSceneMenu.Fill(mask);
                mask.offsetMin = new Vector2(10, 10);
                mask.offsetMax = new Vector2(-10, -10);
                var sky = HomeSceneMenu.Img(mask, "troi", null, Theme.Hex("#bfe3f2"));
                HomeSceneMenu.Fill(sky.rectTransform);
                var scene = HomeSceneMenu.Img(mask, "san", null, Color.white);
                HomeSceneMenu.At(scene.rectTransform, new Vector2(0.5f, 0), Vector2.zero, new Vector2(CardW - 20, CardH), new Vector2(0.5f, 0));
                var heroes = HomeSceneMenu.Fill(HomeSceneMenu.Node(mask, "tuong"));
                heroes.offsetMin = new Vector2(0, BandH - 10); // chân tướng (trên bệ sàn đấu) đứng sát mép trên dải
                var band = HomeSceneMenu.Img(mask, "dai", Sketch.PanelFlat, new Color(Theme.Paper.r, Theme.Paper.g, Theme.Paper.b, 0.95f), false, true);
                HomeSceneMenu.At(band.rectTransform, new Vector2(0.5f, 0), Vector2.zero, new Vector2(CardW - 20, BandH), new Vector2(0.5f, 0));
                band.rectTransform.anchorMin = new Vector2(0, 0);
                band.rectTransform.anchorMax = new Vector2(1, 0);
                band.rectTransform.sizeDelta = new Vector2(0, BandH);
                var stage = T(band.transform, "ten_ai", 38, Theme.Ink, new Vector2(0, 1), new Vector2(22, -8), new Vector2(640, 48), new Vector2(0, 1));
                var row = HomeSceneMenu.Node(band.transform, "hang_manh", typeof(HorizontalLayoutGroup));
                HomeSceneMenu.At(row, new Vector2(0, 1), new Vector2(22, -56), new Vector2(660, 40), new Vector2(0, 1));
                var hl = row.GetComponent<HorizontalLayoutGroup>();
                hl.spacing = 6;
                hl.childAlignment = TextAnchor.MiddleLeft;
                hl.childControlWidth = hl.childControlHeight = true;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var shardIcon = HomeSceneMenu.Img(row, "icon_manh", art.Icon("shard"), Color.white);
                shardIcon.preserveAspect = true;
                var sle = shardIcon.gameObject.AddComponent<LayoutElement>();
                sle.preferredWidth = sle.preferredHeight = 34;
                var faces = new Image[Faces];
                for (int i = 0; i < Faces; i++)
                {
                    faces[i] = HomeSceneMenu.Img(row, "mat_" + i, null, Color.white);
                    faces[i].preserveAspect = true;
                    var le = faces[i].gameObject.AddComponent<LayoutElement>();
                    le.preferredWidth = le.preferredHeight = 40;
                }
                var shard = HomeSceneMenu.Text(row, "manh", 26, Theme.Ink2, TextAlignmentOptions.MidlineLeft);
                shard.enableAutoSizing = true;
                shard.fontSizeMax = 26;
                shard.fontSizeMin = 16;
                shard.textWrappingMode = TextWrappingModes.NoWrap;
                var tle = shard.gameObject.AddComponent<LayoutElement>();
                tle.flexibleWidth = 1;
                tle.preferredHeight = 40;
                var change = Btn(kit.buttonSmall, band.transform, "afk_doi_ai", "Đổi ải", BtnColor.Blue, new Vector2(1, 0.5f), new Vector2(-16, 0),
                    new Vector2(200, 80), new Vector2(1, 0.5f));
                var chip = HomeSceneMenu.Img(mask, "chip_trang_thai", Sketch.Pill, AfkPanel.GoColor, false, true);
                HomeSceneMenu.At(chip.rectTransform, new Vector2(1, 1), new Vector2(-14, -14), new Vector2(250, 58), new Vector2(1, 1)); // góc phải: tướng đứng bên trái
                var chipIcon = HomeSceneMenu.Img(chip.transform, "dong_ho", art.Icon("clock"), Color.white);
                chipIcon.preserveAspect = true;
                HomeSceneMenu.At(chipIcon.rectTransform, new Vector2(0, 0.5f), new Vector2(12, 0), new Vector2(42, 42), new Vector2(0, 0.5f));
                var status = T(chip.transform, "chu", 28, Color.white, new Vector2(0, 0.5f), new Vector2(60, 2), new Vector2(180, 50), new Vector2(0, 0.5f));
                if (white) status.fontSharedMaterial = white;

                // hàng giờ
                var clock = HomeSceneMenu.Img(open, "dong_ho", art.Icon("clock"), Color.white);
                clock.preserveAspect = true;
                HomeSceneMenu.At(clock.rectTransform, new Vector2(0, 1), new Vector2(54, HoursY), new Vector2(60, 60), new Vector2(0, 1));
                var hours = T(open, "gio", 46, Theme.Ink, new Vector2(0, 1), new Vector2(124, HoursY + 2), new Vector2(440, 64), new Vector2(0, 1));
                var rolls = T(open, "luot_manh", 28, Theme.Ink2, new Vector2(1, 1), new Vector2(-60, HoursY), new Vector2(380, 64), new Vector2(1, 1),
                    TextAlignmentOptions.MidlineRight);

                // thanh giờ: vạch từng giờ, hình rương ở giờ ra rương kế
                var bar = ((GameObject)PrefabUtility.InstantiatePrefab(kit.bar.gameObject, open)).GetComponent<UiBar>();
                bar.name = "thanh_gio";
                bar.SetKind(UiBar.Kind.Shard);
                HomeSceneMenu.At((RectTransform)bar.transform, top, new Vector2(0, BarY), new Vector2(BarW, BarH), top);
                var ticks = new RectTransform[Ticks];
                for (int i = 0; i < Ticks; i++)
                {
                    var tk = HomeSceneMenu.Img(bar.transform, "vach_" + i, null, Dark);
                    HomeSceneMenu.At(tk.rectTransform, new Vector2((i + 1f) / 12, 0.5f), Vector2.zero, new Vector2(3, BarH * 0.56f), new Vector2(0.5f, 0.5f));
                    ticks[i] = tk.rectTransform;
                    if (i >= 11) tk.gameObject.SetActive(false);
                }
                var marks = new RectTransform[Marks];
                float mw = 66, mh = chestSp ? mw * chestSp.rect.height / chestSp.rect.width : mw;
                for (int i = 0; i < Marks; i++)
                {
                    var m = HomeSceneMenu.Img(bar.transform, "moc_ruong_" + i, chestSp, Color.white);
                    m.preserveAspect = true;
                    HomeSceneMenu.At(m.rectTransform, new Vector2((i + 1) * 0.25f, 1), new Vector2(0, -BarH * 0.35f), new Vector2(mw, mh), new Vector2(0.5f, 0));
                    marks[i] = m.rectTransform;
                }

                // khay rương
                var trayHead = T(open, "khay_tieu_de", 34, Theme.Ink, new Vector2(0, 1), new Vector2(40, TrayHeadY), new Vector2(400, 50), new Vector2(0, 1));
                trayHead.text = "Rương đường đi";
                var trayNote = T(open, "khay_ghi", 26, Theme.Ink2, new Vector2(1, 1), new Vector2(-40, TrayHeadY), new Vector2(520, 50), new Vector2(1, 1),
                    TextAlignmentOptions.MidlineRight);
                var tray = HomeSceneMenu.Node(open, "khay");
                HomeSceneMenu.At(tray, top, new Vector2(0, TrayY), new Vector2(CardW, SlotH), top);
                var slots = new AfkSlot[Slots];
                for (int i = 0; i < Slots; i++)
                {
                    var s = ((GameObject)PrefabUtility.InstantiatePrefab(slotPrefab.gameObject, tray)).GetComponent<AfkSlot>();
                    s.name = "afk_ruong_" + i;
                    HomeSceneMenu.At(s.Rect, top, new Vector2((i - 1.5f) * (SlotW + 28), 0), new Vector2(SlotW, SlotH), top);
                    if (i >= 4) s.gameObject.SetActive(false);
                    slots[i] = s;
                }
                var openNow = Btn(kit.buttonSmall, open, "nut_mo_ngay", "Mở ngay", BtnColor.Orange, top,
                    new Vector2(slots[0].Rect.anchoredPosition.x, TrayY - SlotH - 14), new Vector2(270, 84), top);
                Tv(openNow, art.Icon("tv"), 50);

                // hàng nút cuối: TV Tăng tốc ×2 (phụ), Nhận mảnh (chính)
                var bottom = new Vector2(0.5f, 0);
                var boost = Btn(kit.buttonSmall, open, "nut_tang_toc", "Tăng tốc ×2", BtnColor.Orange, bottom, new Vector2(-230, 52),
                    new Vector2(400, 116), bottom);
                Tv(boost, art.Icon("tv"), 62);
                var claim = Btn(kit.buttonBig, open, "nut_nhan", "Nhận mảnh", BtnColor.Green, bottom, new Vector2(220, 46), new Vector2(440, 132), bottom);

                // tờ luật: phủ nội dung dưới tiêu đề, chạm để tắt
                var rulesImg = HomeSceneMenu.Img(page, "to_luat", Sketch.PanelThin, Theme.Paper, true, true);
                HomeSceneMenu.Fill(rulesImg.rectTransform);
                rulesImg.rectTransform.offsetMin = new Vector2(30, 30);
                rulesImg.rectTransform.offsetMax = new Vector2(-30, -118);
                var rules = rulesImg.gameObject.AddComponent<Button>();
                rules.transition = Selectable.Transition.None;
                var rulesHead = T(rulesImg.transform, "tieu_de", 42, Theme.Ink, top, new Vector2(0, -30), new Vector2(800, 60), top, TextAlignmentOptions.Center);
                rulesHead.text = "Cách chơi";
                var rulesText = HomeSceneMenu.Text(rulesImg.transform, "luat", 32, Theme.Ink, TextAlignmentOptions.TopLeft);
                HomeSceneMenu.Fill(rulesText.rectTransform);
                rulesText.rectTransform.offsetMin = new Vector2(44, 90);
                rulesText.rectTransform.offsetMax = new Vector2(-44, -112);
                rulesText.lineSpacing = 18;
                rulesText.paragraphSpacing = 18;
                var rulesTap = T(rulesImg.transform, "cham_dong", 26, Theme.Ink2, new Vector2(0.5f, 0), new Vector2(0, 30), new Vector2(800, 44),
                    new Vector2(0.5f, 0), TextAlignmentOptions.Center);
                rulesTap.text = "Chạm để đóng";
                rulesImg.gameObject.SetActive(false);
                if (close) close.SetAsLastSibling();

                var dlgComp = root.GetComponent<AfkPanel>();
                if (!dlgComp) dlgComp = root.AddComponent<AfkPanel>();
                dlgComp.Setup(new AfkPanel.Parts
                {
                    locked = new[] { lockG.gameObject }, unlocked = new[] { open.gameObject }, ok = ok, info = info, rules = rules, rulesText = rulesText,
                    sceneMask = mask, scene = scene, heroes = heroes, statusChip = chip, status = status, stage = stage, shard = shard, faces = faces,
                    change = change, hours = hours, rolls = rolls, bar = bar, ticks = ticks, marks = marks, trayNote = trayNote, slots = slots,
                    openNow = openNow, boost = boost, claim = claim,
                });
                var dlg = PrefabUtility.SaveAsPrefabAsset(root, DialogPath).GetComponent<AfkPanel>();
                kit.dialogs.RemoveAll(x => !x || (x is AfkPanel && x != dlg));
                if (!kit.dialogs.Contains(dlg)) kit.dialogs.Add(dlg);
                EditorUtility.SetDirty(kit);
                AssetDatabase.SaveAssets();
                Debug.Log($"[AFK] Đã dựng {DialogPath} (bố cục cảnh + thanh mốc) và {SlotPath} (rương gỗ có rig)");
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // ---------- thử ----------

        const double H = 3600000;
        static string ShotDir => System.IO.Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "afk");

        // Hộp AFK bản mới (đang Play): đảo Thủy qua 30 ải, đảo Hỏa 70 (ảnh người dùng gửi); chụp 1. rương mở được + đang đếm + chờ,
        // 2. đầy giờ, 3. đang tăng tốc, khay trống (rương mốc trên thanh), 4. tờ luật, 5. mở rương (rig) mỗi 0,3 s; ảnh vào
        // Temp/PokiShots/afk/; xong trả bản lưu.
        [MenuItem("PokiClash/Thử/Đảo và sảnh/Hộp AFK bản mới: các trạng thái, mở rương (đang Play)", priority = 116)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[AFK] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(RunTour());
        }

        static System.Collections.IEnumerator RunTour()
        {
            var path = App.Save.FilePath;
            string backup = System.IO.File.Exists(path) ? System.IO.File.ReadAllText(path) : null;
            System.IO.Directory.CreateDirectory(ShotDir);
            foreach (var f in System.IO.Directory.GetFiles(ShotDir, "*.jpg")) System.IO.File.Delete(f);
            bool tutOff = Tutorial.Off;
            Tutorial.Off = true;
            try
            {
                var s = App.Save.Data;
                App.Modals.CloseAll();
                s.zones[(int)Elem.Thuy] = 30;
                s.zones[(int)Elem.Hoa] = 70;
                s.afk.stage = 0;
                App.Router.Go(SceneIds.Hub);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Hub) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(1f);

                double now = Game.SaveService.Now();
                // 1. rương đầu mở được, rương 2 đang đếm (còn 1,5 giờ), rương 3 chờ; 3,4 giờ, rương kế sau 1,8 giờ
                s.afk = new AfkState { hours = 3.4, chestAcc = 1.2, lastTick = now, chests = { now - 2.5 * H, now - 0.5 * H, now - 0.2 * H } };
                yield return Open("1_khay");
                // 2. đầy giờ
                s.afk = new AfkState { hours = 12, chestAcc = 0, lastTick = now, chests = { now - 0.4 * H } };
                yield return Open("2_day_gio");
                // 3. đang tăng tốc, khay trống: rương mốc trên thanh ở 5,5 / 8,5 / 11,5 giờ
                s.afk = new AfkState { hours = 5, chestAcc = 2.5, lastTick = now, boostUntil = now + 1.3 * H };
                yield return Open("3_tang_toc");
                // 4. tờ luật
                var panel = Object.FindAnyObjectByType<AfkPanel>();
                var info = panel ? panel.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(b => b.name == "nut_luat") : null;
                if (info) info.SimulateClick();
                yield return new WaitForSecondsRealtime(0.4f);
                yield return Shot("4_luat");
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.4f);
                // 5. mở rương: chạm rương đầu khay (mở được)
                s.afk = new AfkState { hours = 2, chestAcc = 0.5, lastTick = Game.SaveService.Now(), chests = { Game.SaveService.Now() - 2.2 * H } };
                yield return Open("5_truoc_mo");
                panel = Object.FindAnyObjectByType<AfkPanel>();
                var slot = panel ? panel.GetComponentsInChildren<AfkSlot>(true).FirstOrDefault(x => x.name == "afk_ruong_0") : null;
                if (slot) slot.Button.SimulateClick();
                for (int k = 0; k < 10; k++)
                {
                    yield return new WaitForSecondsRealtime(k == 0 ? 0.15f : 0.3f);
                    yield return Shot($"6_mo_{k:00}");
                }
                App.Modals.CloseAll();
                Debug.Log("[AFK] Xong thử hộp AFK bản mới: " + System.IO.Path.GetFullPath(ShotDir));
            }
            finally
            {
                Tutorial.Off = tutOff;
                if (backup != null)
                {
                    System.IO.File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
        }

        static System.Collections.IEnumerator Open(string shot)
        {
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.4f);
            AfkPanel.Open();
            yield return new WaitForSecondsRealtime(1.2f);
            yield return Shot(shot);
        }

        static System.Collections.IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            if (!tex) yield break;
            System.IO.File.WriteAllBytes(System.IO.Path.Combine(ShotDir, name + ".jpg"), tex.EncodeToJPG(85));
            Object.DestroyImmediate(tex);
        }

        // ô khay: nút giấy (chữ của nút tắt), khung rương có CanvasGroup chứa Kit/Ruong (gốc ở mép đáy), chữ, thanh đếm giờ
        static AfkSlot BuildSlot(UiKit kit)
        {
            var root = (GameObject)PrefabUtility.InstantiatePrefab(kit.buttonNormal.gameObject);
            try
            {
                root.name = "RuongAfk";
                var btn = root.GetComponent<SketchButton>();
                btn.SetRole(BtnColor.Paper);
                btn.SetText("");
                if (btn.Label) btn.Label.gameObject.SetActive(false);
                HomeSceneMenu.At(btn.Rect, new Vector2(0.5f, 1), Vector2.zero, new Vector2(SlotW, SlotH), new Vector2(0.5f, 1));
                if (!root.GetComponent<AfkSlot>()) root.AddComponent<AfkSlot>();
                var holder = HomeSceneMenu.Node(root.transform, "cho_ruong", typeof(CanvasGroup));
                HomeSceneMenu.At(holder, new Vector2(0.5f, 1), new Vector2(0, -18), new Vector2(SlotW - 20, 124), new Vector2(0.5f, 1));
                var fade = holder.GetComponent<CanvasGroup>();
                fade.blocksRaycasts = false;
                fade.interactable = false;
                var chest = ((GameObject)PrefabUtility.InstantiatePrefab(kit.chest.gameObject, holder)).GetComponent<ChestIcon>();
                chest.name = "ruong";
                HomeSceneMenu.At(chest.Rect, new Vector2(0.5f, 0), Vector2.zero, new Vector2(SlotW * 0.72f, SlotW * 0.66f), new Vector2(0.5f, 0));
                foreach (var g in chest.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
                var label = T(root.transform, "chu", 30, Theme.Ink, new Vector2(0.5f, 0), new Vector2(0, 50), new Vector2(SlotW - 12, 42),
                    new Vector2(0.5f, 0.5f), TextAlignmentOptions.Center);
                var back = HomeSceneMenu.Img(root.transform, "thanh_nen", Sketch.Pill, Dark, false, true);
                HomeSceneMenu.At(back.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 20), new Vector2(SlotW - 40, 16), new Vector2(0.5f, 0.5f));
                var fill = HomeSceneMenu.Img(back.transform, "thanh", Sketch.Pill, AfkPanel.GoColor, false, true);
                HomeSceneMenu.At(fill.rectTransform, new Vector2(0, 0.5f), Vector2.zero, new Vector2(16, 16), new Vector2(0, 0.5f));
                back.gameObject.SetActive(false);
                root.GetComponent<AfkSlot>().Setup(btn, chest, fade, label, back.rectTransform, fill.rectTransform);
                return PrefabUtility.SaveAsPrefabAsset(root, SlotPath).GetComponent<AfkSlot>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }
    }
}
