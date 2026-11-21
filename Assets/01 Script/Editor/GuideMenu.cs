// Hướng dẫn người mới (GD_Claude/25_FTUE.md):
// - "PokiClash/Prefab/Hướng dẫn người mới (lớp phủ)": dựng Kit/HuongDan (GuideOverlay: canvas thứ tự 30, 4 dải chắn, vòng khoanh InkPath,
//   bút chì, ghi chú Kit/GoiY, chân dung tướng, chữ "Chạm để tiếp tục") và gắn vào App.prefab. Chạy lại thì dựng lại.
// - "PokiClash/Prefab/Hướng dẫn: hộp Cách chơi, dòng Sổ tay": hộp Dialogs/CachChoi (HowToDialog, biến thể HopThoai, chữ cuộn dọc), thêm
//   vào UiKit; thêm dòng "Cách chơi" vào Screens/Notebook (nhân bản dòng Ngôn ngữ như NotebookLanguageMenu), gán NotebookScene.p.howTo.
// - Menu thử (đang Play): chơi lại hướng dẫn từ đầu (xoá bản lưu!), bỏ qua hết, và tour người chơi mới: xoá bản lưu, đi hết chuỗi bắt
//   buộc bằng chạm giả, chụp từng bước vào Temp/PokiShots/huong_dan/, xong trả lại bản lưu cũ.
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class GuideMenu
    {
        const string OverlayPath = "Assets/04 Prefabs/Kit/HuongDan.prefab";
        const string AppPath = "Assets/04 Prefabs/App/App.prefab";
        const string SheetPath = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string PrepPath = "Assets/04 Prefabs/Dialogs/ChuanBiTran.prefab";
        const string HowToPath = "Assets/04 Prefabs/Dialogs/CachChoi.prefab";
        const string NotebookPath = "Assets/04 Prefabs/Screens/Notebook.prefab";
        const string PencilPath = "Assets/03 Art/Boot/boot_but_chi.png";

        static UiKit Kit => AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiKit")[0]));

        // ---------- lớp phủ ----------

        [MenuItem("PokiClash/Prefab/Hướng dẫn người mới (lớp phủ)", priority = 66)]
        public static void BuildOverlay()
        {
            var kit = Kit;
            var root = new GameObject("HuongDan");
            try
            {
                var view = Ui.Spawn(kit.canvas, root.transform);
                view.name = "Canvas";
                view.Canvas.sortingOrder = 30; // trên thanh trên (10), màn tải (15), hộp thoại và mây (20)
                var area = view.Bg;
                var cg = area.gameObject.AddComponent<CanvasGroup>();

                var dim = new Color(0.09f, 0.06f, 0.04f, 0.74f); // hoà màu linear: alpha trông nhạt hơn số đặt
                var blockers = new[] { "chan_tren", "chan_duoi", "chan_trai", "chan_phai" }.Select(n => Img(area, n, null, dim, true)).ToArray();

                InkPath Ink(string name, Color c, float w)
                {
                    var go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(InkPath));
                    go.layer = LayerMask.NameToLayer("UI");
                    go.transform.SetParent(area, false);
                    var ink = go.GetComponent<InkPath>();
                    ink.color = c;
                    ink.raycastTarget = false;
                    ink.Setup(new Vector2[0], w, 0, 0, true);
                    return ink;
                }
                var ringUnder = Ink("vong_lot", new Color(Theme.Paper.r, Theme.Paper.g, Theme.Paper.b, 0.95f), 16); // lót màu giấy dưới nét đỏ
                var ring = Ink("vong_khoanh", Theme.RedD, 8);

                var pencilSprite = AssetDatabase.LoadAllAssetsAtPath(PencilPath).OfType<Sprite>().FirstOrDefault();
                var pencil = Img(area, "but_chi", pencilSprite, Color.white);
                // cạnh dài 230 (ảnh bút chì nằm ngang)
                float aspect = pencilSprite ? pencilSprite.rect.width / Mathf.Max(1, pencilSprite.rect.height) : 0.3f;
                float pw = aspect >= 1 ? 230 : 230 * aspect, ph = aspect >= 1 ? 230 / aspect : 230;
                pencil.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(pw, ph));
                if (!pencilSprite) Debug.LogWarning("[Hướng dẫn] Không thấy ảnh bút chì " + PencilPath + ": bút chì để trống");

                var note = ((GameObject)PrefabUtility.InstantiatePrefab(kit.hint.gameObject, area)).GetComponent<UiHint>();
                note.name = "ghi_chu";
                note.Set("Chọn 1 trong 3 thẻ.", 660);

                var face = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, area)).GetComponent<HeroPortrait>();
                face.name = "ban_dong_hanh";
                face.Rect.sizeDelta = new Vector2(220, 220);

                var tap = Object.Instantiate(note.Label.gameObject, area, false).GetComponent<TextMeshProUGUI>();
                tap.name = "cham_tiep";
                foreach (var c in tap.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
                foreach (var c in tap.GetComponents<LayoutElement>()) Object.DestroyImmediate(c);
                tap.text = "Chạm để tiếp tục";
                tap.color = Theme.Paper;
                tap.fontSize = 36;
                tap.alignment = TextAlignmentOptions.Center;
                tap.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -200), new Vector2(720, 64));

                // chỉ 4 dải chắn nhận chạm
                foreach (var gr in area.GetComponentsInChildren<Graphic>(true))
                    gr.raycastTarget = blockers.Contains(gr as Image);

                var ov = root.AddComponent<GuideOverlay>();
                ov.Setup(area, cg, blockers, ring, ringUnder, pencil.rectTransform, note, face, tap);
                PrefabUtility.SaveAsPrefabAsset(root, OverlayPath);
            }
            finally
            {
                Object.DestroyImmediate(root);
            }

            var prefab = AssetDatabase.LoadAssetAtPath<GameObject>(OverlayPath);
            var appRoot = PrefabUtility.LoadPrefabContents(AppPath);
            try
            {
                var app = appRoot.GetComponentInChildren<App>(true);
                var old = app.transform.Find("HuongDan");
                if (old) Object.DestroyImmediate(old.gameObject);
                var inst = (GameObject)PrefabUtility.InstantiatePrefab(prefab, app.transform);
                inst.name = "HuongDan";
                PrefabUtility.SaveAsPrefabAsset(appRoot, AppPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(appRoot);
            }
            AssetDatabase.SaveAssets();
            Debug.Log($"[Hướng dẫn] Đã dựng {OverlayPath} và gắn vào App.prefab.");
        }

        static Image Img(Transform parent, string name, Sprite s, Color c, bool raycast = false)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
            go.layer = LayerMask.NameToLayer("UI");
            go.transform.SetParent(parent, false);
            var img = go.GetComponent<Image>();
            Theme.SetSprite(img, s);
            img.color = c;
            img.raycastTarget = raycast;
            ((RectTransform)go.transform).Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(100, 100));
            return img;
        }

        // ---------- hộp Cách chơi, dòng Sổ tay ----------

        [MenuItem("PokiClash/Prefab/Hướng dẫn: hộp Cách chơi, dòng Sổ tay", priority = 67)]
        public static void BuildHowTo()
        {
            var kit = Kit;
            var prep = AssetDatabase.LoadAssetAtPath<GameObject>(PrepPath).GetComponent<StagePrepDialog>();
            var pso = new SerializedObject(prep);
            var titleTpl = (TextMeshProUGUI)pso.FindProperty("p.title").objectReferenceValue;
            var hintTpl = (TextMeshProUGUI)pso.FindProperty("p.hint").objectReferenceValue;

            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetPath));
            try
            {
                root.name = "CachChoi";
                root.GetComponent<ModalSheet>().Configure(980, false, false);
                var sheet = root.GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "to_giay");
                if (!sheet)
                {
                    Debug.LogError("[Hướng dẫn] HopThoai không có to_giay.");
                    return;
                }
                var content = new GameObject("noi_dung", typeof(RectTransform), typeof(VerticalLayoutGroup)).transform;
                content.SetParent(sheet, false);
                var vl = content.GetComponent<VerticalLayoutGroup>();
                vl.spacing = 14;
                vl.childControlWidth = vl.childControlHeight = true;
                vl.childForceExpandWidth = true;
                vl.childForceExpandHeight = false;

                var title = Text(titleTpl, content, "tieu_de", 72);
                title.alignment = TextAlignmentOptions.Center;
                title.text = "Cách chơi";

                // vùng cuộn: khung (RectMask2D) và nội dung giãn theo chữ
                var scrollGo = new GameObject("cuon", typeof(RectTransform), typeof(Image), typeof(ScrollRect), typeof(LayoutElement));
                scrollGo.transform.SetParent(content, false);
                scrollGo.GetComponent<LayoutElement>().preferredHeight = 1180;
                var scrollImg = scrollGo.GetComponent<Image>();
                scrollImg.color = new Color(1, 1, 1, 0);
                var scroll = scrollGo.GetComponent<ScrollRect>();
                scroll.horizontal = false;
                scroll.vertical = true;
                scroll.movementType = ScrollRect.MovementType.Clamped;
                var viewport = new GameObject("khung", typeof(RectTransform), typeof(RectMask2D)).GetComponent<RectTransform>();
                viewport.SetParent(scrollGo.transform, false);
                viewport.Stretch();
                var inner = new GameObject("chu_cuon", typeof(RectTransform), typeof(VerticalLayoutGroup), typeof(ContentSizeFitter)).GetComponent<RectTransform>();
                inner.SetParent(viewport, false);
                inner.anchorMin = new Vector2(0, 1);
                inner.anchorMax = new Vector2(1, 1);
                inner.pivot = new Vector2(0.5f, 1);
                inner.anchoredPosition = Vector2.zero;
                inner.sizeDelta = Vector2.zero;
                var ivl = inner.GetComponent<VerticalLayoutGroup>();
                ivl.childControlWidth = ivl.childControlHeight = true;
                ivl.childForceExpandWidth = true;
                ivl.childForceExpandHeight = false;
                ivl.padding = new RectOffset(8, 8, 4, 20);
                inner.GetComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;
                scroll.viewport = viewport;
                scroll.content = inner;

                var body = Object.Instantiate(hintTpl.gameObject, inner, false).GetComponent<TextMeshProUGUI>();
                body.name = "trang";
                foreach (var c in body.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
                foreach (var c in body.GetComponents<LayoutElement>()) Object.DestroyImmediate(c);
                body.gameObject.SetActive(true);
                body.alignment = TextAlignmentOptions.TopLeft;
                body.textWrappingMode = TextWrappingModes.Normal;
                body.richText = true;
                body.enableAutoSizing = false;
                body.fontSize = 34;
                body.lineSpacing = 6;
                body.text = "Vòng chơi";

                root.AddComponent<HowToDialog>().Setup(body, scroll);
                var dlg = PrefabUtility.SaveAsPrefabAsset(root, HowToPath).GetComponent<HowToDialog>();
                if (!kit.dialogs.Any(x => x is HowToDialog))
                {
                    kit.dialogs.Add(dlg);
                    EditorUtility.SetDirty(kit);
                }
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
            AddNotebookRow();
            AssetDatabase.SaveAssets();
            Debug.Log($"[Hướng dẫn] Đã dựng {HowToPath} (thêm vào UiKit) và dòng Cách chơi ở Sổ tay.");
        }

        static TextMeshProUGUI Text(TextMeshProUGUI from, Transform parent, string name, float h)
        {
            var t = Object.Instantiate(from.gameObject, parent, false).GetComponent<TextMeshProUGUI>();
            t.name = name;
            foreach (var c in t.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
            var le = t.GetComponent<LayoutElement>();
            if (!le) le = t.gameObject.AddComponent<LayoutElement>();
            le.preferredHeight = h;
            t.gameObject.SetActive(true);
            return t;
        }

        // dòng "Cách chơi" ở Sổ tay: nhân bản dòng Ngôn ngữ (hoặc Giảm nhấp nháy / Rung / Âm thanh), nút ghi "Xem"
        static void AddNotebookRow()
        {
            var contents = PrefabUtility.LoadPrefabContents(NotebookPath);
            try
            {
                var scene = contents.GetComponentInChildren<NotebookScene>(true);
                var so = new SerializedObject(scene);
                var prop = so.FindProperty("p.howTo");
                if (prop.objectReferenceValue)
                {
                    Debug.Log("[Sổ tay] Đã có dòng Cách chơi");
                    return;
                }
                var src = (SketchButton)so.FindProperty("p.language").objectReferenceValue
                          ?? (SketchButton)so.FindProperty("p.lowFlash").objectReferenceValue
                          ?? (SketchButton)so.FindProperty("p.haptics").objectReferenceValue
                          ?? (SketchButton)so.FindProperty("p.sound").objectReferenceValue;
                if (!src)
                {
                    Debug.LogError("[Sổ tay] Không thấy dòng nào để nhân bản cho dòng Cách chơi.");
                    return;
                }
                var row = src.transform.parent;
                var copy = Object.Instantiate(row.gameObject, row.parent, false);
                copy.name = "hang_CachChoi";
                copy.transform.SetSiblingIndex(row.GetSiblingIndex() + 1);
                for (int i = 0; i < row.childCount; i++)
                {
                    var orig = row.GetChild(i).gameObject;
                    if (!PrefabUtility.IsAnyPrefabInstanceRoot(orig)) continue;
                    var source = PrefabUtility.GetCorrespondingObjectFromSource(orig);
                    var cloned = copy.transform.GetChild(i).gameObject;
                    var fresh = (GameObject)PrefabUtility.InstantiatePrefab(source, copy.transform);
                    PrefabUtility.SetPropertyModifications(fresh, PrefabUtility.GetPropertyModifications(orig));
                    fresh.transform.SetSiblingIndex(i);
                    fresh.name = cloned.name;
                    Object.DestroyImmediate(cloned);
                }
                foreach (var t in copy.GetComponentsInChildren<TextMeshProUGUI>(true))
                    if (!t.GetComponentInParent<SketchButton>()) t.text = "Cách chơi";
                var btn = copy.GetComponentInChildren<SketchButton>(true);
                btn.SetText("Xem");
                prop.objectReferenceValue = btn;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, NotebookPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // ---------- menu thử (đang Play) ----------

        static bool Playing()
        {
            if (EditorApplication.isPlaying && App.I != null) return true;
            Debug.LogWarning("[Hướng dẫn] Mở Boot.unity và bấm Play trước.");
            return false;
        }

        [MenuItem("PokiClash/Thử/Hướng dẫn: chơi lại từ đầu, xoá bản lưu (đang Play)", priority = 140)]
        static void Restart()
        {
            var path = App.Save != null ? App.Save.FilePath : null;
            if (!Playing() || !EditorUtility.DisplayDialog("Chơi lại hướng dẫn",
                    $"Chép bản lưu hiện tại ra {Path.GetFileName(path)}.bak_ftue rồi chơi như người mới?", "Chép, chơi lại", "Thôi"))
                return;
            if (File.Exists(path)) File.Copy(path, path + ".bak_ftue", true);
            Tutorial.Off = false;
            App.Modals.CloseAll();
            App.Save.Reset();
            App.Router.Go(SceneIds.Hub);
            Debug.Log($"[Hướng dẫn] Đã chép bản lưu cũ ra {path}.bak_ftue; muốn lấy lại thì đổi tên về {Path.GetFileName(path)} khi không Play.");
        }

        [MenuItem("PokiClash/Thử/Hướng dẫn: bỏ qua hết (đang Play)", priority = 141)]
        static void SkipAll()
        {
            if (!Playing()) return;
            Tutorial.Skip(App.Save.Data);
            App.Save.Save();
            App.Router.Go(SceneIds.Hub);
        }

        // ---------- tour người chơi mới ----------

        static string Dir => Path.Combine(PlayTour.ShotDir, "huong_dan");
        static int shot;

        [MenuItem("PokiClash/Thử/Hướng dẫn: người chơi mới, đi hết chuỗi và chụp (đang Play)", priority = 142)]
        static void Tour()
        {
            if (!Playing()) return;
            App.I.StartCoroutine(RunTour());
        }

        static IEnumerator Until(System.Func<bool> cond, float timeout)
        {
            float t0 = Time.realtimeSinceStartup;
            while (!cond() && Time.realtimeSinceStartup - t0 < timeout) yield return null;
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(Dir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, $"{shot++:00}_{name}.jpg"), tex.EncodeToJPG(85));
            Object.Destroy(tex);
        }

        static IEnumerator RunTour()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            shot = 0;
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            Tutorial.Off = false;
            var log = new System.Text.StringBuilder();
            try
            {
                App.Modals.CloseAll();
                App.Save.Reset();
                App.Router.Go(SceneIds.Hub);
                yield return Until(() => !App.Router.Busy && App.Router.Current == SceneIds.Hub, 20);
                float t0 = Time.realtimeSinceStartup;
                string lastId = null;
                int idle = 0, chestTick = 0;
                while (Time.realtimeSinceStartup - t0 < 600 && !Tutorial.CoreDone(App.Save.Data))
                {
                    yield return new WaitForSecondsRealtime(0.25f);
                    var ov = GuideOverlay.I;
                    // hộp chọn tướng: chọn tướng đầu
                    var starter = Object.FindAnyObjectByType<StarterDialog>();
                    if (starter && App.Save.Data.starter == null)
                    {
                        yield return new WaitForSecondsRealtime(0.6f);
                        yield return Shot("chon_tuong");
                        App.Save.Data.ChooseStarter(App.Data.Starters[0]);
                        App.Save.Save();
                        App.Modals.CloseAll();
                        App.Router.CurrentRoot?.Refresh();
                        log.AppendLine("chọn tướng " + App.Data.Starters[0]);
                        continue;
                    }
                    if (ov && ov.ShownId != null)
                    {
                        idle = 0;
                        string id = ov.ShownId;
                        if (id != lastId)
                        {
                            yield return new WaitForSecondsRealtime(0.5f);
                            if (ov.ShownId != id) continue;
                            yield return Shot($"{id}_{App.Router.Current}");
                            log.AppendLine($"{id} ({ov.ShownMode}) ở {App.Router.Current}");
                            lastId = id;
                        }
                        ov.DebugTap();
                        continue;
                    }
                    // trong trận không có bước ép: chọn thẻ đầu; hộp kết quả, lên cấp: không có bước thì đóng bằng nút đầu
                    var ctl = Object.FindAnyObjectByType<BattleController>();
                    if (ctl) ctl.FastForward(3);
                    if (ctl && ctl.WaitingPlayer && Guide.Idle)
                    {
                        ctl.TestPick(0);
                        continue;
                    }
                    // hộp lên cấp: đóng như người chơi (bước hướng dẫn kế có thể đang chờ hộp đóng, nên không đợi lớp phủ rảnh)
                    var lvUp = Object.FindAnyObjectByType<LevelUpDialog>();
                    if (lvUp)
                    {
                        yield return Shot("len_cap");
                        lvUp.Close();
                        continue;
                    }
                    var machine = App.Router.CurrentRoot as MachineScene;
                    if (machine && Guide.Idle && App.Save.Data.balls > 0 && !Tutorial.Done(App.Save.Data, Tutorial.NoBalls))
                    {
                        // giữ nút thả: thả từng bi qua đúng nút
                        var drop = Guide.Target("machine.drop");
                        var hold = drop ? drop.GetComponentInChildren<UnityEngine.EventSystems.IPointerDownHandler>() as Component : null;
                        if (hold)
                        {
                            var ev = new UnityEngine.EventSystems.PointerEventData(UnityEngine.EventSystems.EventSystem.current);
                            UnityEngine.EventSystems.ExecuteEvents.Execute(hold.gameObject, ev, UnityEngine.EventSystems.ExecuteEvents.pointerDownHandler);
                            UnityEngine.EventSystems.ExecuteEvents.Execute(hold.gameObject, ev, UnityEngine.EventSystems.ExecuteEvents.pointerUpHandler);
                        }
                        yield return new WaitForSecondsRealtime(0.4f);
                        continue;
                    }
                    // màn mở rương của máy bi: mở rương còn đóng, rồi bấm Nhận / Mở tiếp
                    var open = Object.FindAnyObjectByType<MachineChestOpen>();
                    if (open && Guide.Idle && ++chestTick % 3 == 0)
                    {
                        // nút của màn mở rương nằm dưới khung máy, không nằm trong cây con của MachineChestOpen: "Mở tất cả" (nhiều rương),
                        // không thì chạm rương; xong thì "Nhận" / "Mở tiếp"
                        var buttons = Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None).Where(b => b.isActiveAndEnabled).ToList();
                        var all = buttons.FirstOrDefault(b => b.name.StartsWith("nut_Mở tất cả"));
                        if (all) all.SimulateClick();
                        else
                        {
                            var chest = Object.FindObjectsByType<Button>(FindObjectsSortMode.None).FirstOrDefault(b => b.name == "than_ruong" && b.isActiveAndEnabled && b.interactable);
                            if (chest) chest.onClick.Invoke();
                        }
                        var ok = buttons.FirstOrDefault(b => b.name.StartsWith("nut_Nhận") || b.name.StartsWith("nut_Mở tiếp"));
                        if (ok)
                        {
                            yield return Shot("ruong_mo");
                            ok.SimulateClick();
                        }
                        continue;
                    }
                    // không có bước nào chờ mà chưa xong chuỗi: làm như người chơi tự đi tiếp. Hộp kết quả trận (bắt buộc) bấm nút cuối
                    // (về đảo); hộp khác (chi tiết tướng sau khi nâng Chiêu) đóng; không hộp thì quay lại (về sảnh, nơi có bước kế)
                    var result = Object.FindAnyObjectByType<BattleResultDialog>();
                    bool nothingShown = !ov || ov.ShownId == null;
                    bool calm = !App.Router.Busy && !App.Booting && !App.Covered;
                    if (nothingShown && calm && idle > 0 && idle % 12 == 0)
                    {
                        var s = App.Save.Data;
                        var btn = result ? result.GetComponentsInChildren<SketchButton>().LastOrDefault(b => b.isActiveAndEnabled && b.name.StartsWith("nut_")) : null;
                        string did = null;
                        if (btn)
                        {
                            // hộp kết quả không còn bước nào: bấm nút cuối (về đảo)
                            yield return Shot($"ket_qua_{App.Router.Current}");
                            btn.SimulateClick();
                            did = btn.name;
                        }
                        else if (!result && App.Modals.Count > 0 && !Guide.Idle && App.Modals.Back()) did = "đóng hộp che bước kế";
                        else if (App.Router.Current == SceneIds.Zone && Guide.Idle && s.zones[(int)Tutorial.CounterIsland(s, App.Data)] > 0)
                        {
                            App.Back(); // trận 2 xong: về sảnh nghe lời chào cuối
                            did = "về sảnh";
                        }
                        if (did != null) log.AppendLine($"tự đi tiếp ở {App.Router.Current} ({did})");
                    }
                    if (++idle > 160)
                    {
                        log.AppendLine($"kẹt ở {App.Router.Current}, hộp {App.Modals.Count}, lớp phủ: {(ov ? ov.DebugState : "không có")}");
                        yield return Shot("ket");
                        break;
                    }
                }
                yield return new WaitForSecondsRealtime(1f);
                yield return Shot("xong");
                log.AppendLine(Tutorial.CoreDone(App.Save.Data) ? "XONG chuỗi bắt buộc" : "CHƯA XONG chuỗi bắt buộc");
                File.WriteAllText(Path.Combine(Dir, "nhat_ky.txt"), log.ToString());
                Debug.Log("[Hướng dẫn] Tour người mới:\n" + log + $"Ảnh: {Dir}");
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
    }
}
