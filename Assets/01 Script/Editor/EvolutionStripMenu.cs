// Dựng thanh mốc tiến hóa (EvolutionStrip) vào prefab Dialogs/ChiTietTuong: một hàng mới ngay dưới hàng ô xem tướng, gồm thanh
// kit (Thanh, loại Exp), 4 chỗ mốc bậc (kit ChanDung, kit Sao, chữ chép từ nhãn dòng tiến hóa của hộp; lúc chạy chỉ hiện đúng số bậc
// của tướng, bậc theo dạng 2026-11-19) và nút Tiến hóa kit Tiny màu xanh lá trên thanh (giữa hai mốc, có nhịp phồng) với dòng giá
// dưới nút. Chạy lại thì dựng lại hàng đó.
// Menu "Hộp chi tiết tướng: nhãn bậc sao + thanh mảnh, đá" (2026-11-17): nhãn "Bạc 3 sao" cạnh hàng sao và một hàng thanh (icon mảnh / đá
// tiến hóa + thanh kit) ngay trên dòng điều kiện tiến hóa. Chạy lại thì dựng lại hai phần đó.
// Sau khi dựng, chỉnh vị trí và cỡ trong Editor như mọi prefab khác.
// Menu thử (đang Play): đặt tạm sao của vài tướng trong bộ nhớ (không ghi bản lưu), mở hộp chi tiết, chụp vào Temp/PokiShots/evo_*.png,
// rồi nạp lại bản lưu từ đĩa.
using System.Collections;
using System.IO;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class EvolutionStripMenu
    {
        const string DialogPath = "Assets/04 Prefabs/Dialogs/ChiTietTuong.prefab";
        const int Nodes = 4; // tối đa 4 bậc (Core.StarTier.Count); tướng hiện có 1–3 bậc theo số hình
        const float Pad = 100, BarH = 32, PortraitH = 128, Top = 8;
        const float TrackY = Top + PortraitH * (1 - HeroArt.FootY) + 4 + BarH / 2; // tâm thanh, tính từ mép trên
        const float StarsY = TrackY + BarH / 2 + 6 + 13, NameY = StarsY + 13 + 4 + 17, Height = NameY + 17 + 10;

        [MenuItem("PokiClash/Prefab/Thêm thanh tiến hóa vào ChiTietTuong", priority = 60)]
        static void Build()
        {
            var kitGuids = AssetDatabase.FindAssets("t:UiKit");
            if (kitGuids.Length == 0)
            {
                Debug.LogError("[Tiến hóa] Không thấy asset UiKit.");
                return;
            }
            var kit = AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(kitGuids[0]));
            var contents = PrefabUtility.LoadPrefabContents(DialogPath);
            try
            {
                var dlg = contents.GetComponentInChildren<HeroDetailDialog>(true);
                var so = new SerializedObject(dlg);
                var viewer = (HeroViewer)so.FindProperty("p.viewer").objectReferenceValue;
                var lineLabel = (TextMeshProUGUI)so.FindProperty("p.line").objectReferenceValue;
                var evo = so.FindProperty("p.evolution");
                if (!viewer || !lineLabel)
                {
                    Debug.LogError("[Tiến hóa] ChiTietTuong thiếu ô xem hoặc nhãn dòng tiến hóa.");
                    return;
                }

                // hàng chứa ô xem: tổ tiên đầu tiên có cha là cột VerticalLayoutGroup
                var row = viewer.transform;
                while (row.parent && !row.parent.GetComponent<VerticalLayoutGroup>()) row = row.parent;
                if (!row.parent)
                {
                    Debug.LogError("[Tiến hóa] Không thấy cột chứa hàng ô xem.");
                    return;
                }
                if (evo.objectReferenceValue) Object.DestroyImmediate(((Component)evo.objectReferenceValue).gameObject);

                var root = new GameObject("thanh_tien_hoa", typeof(RectTransform), typeof(LayoutElement), typeof(EvolutionStrip));
                root.transform.SetParent(row.parent, false);
                root.transform.SetSiblingIndex(row.GetSiblingIndex() + 1);
                root.GetComponent<LayoutElement>().preferredHeight = Height;
                var rootRt = (RectTransform)root.transform;
                rootRt.sizeDelta = new Vector2(rootRt.sizeDelta.x, Height);

                var bar = ((GameObject)PrefabUtility.InstantiatePrefab(kit.bar.gameObject, root.transform)).GetComponent<UiBar>();
                bar.name = "thanh";
                TopStretch((RectTransform)bar.transform, TrackY, BarH);
                bar.SetKind(UiBar.Kind.Exp);

                var rail = new GameObject("moc", typeof(RectTransform)).GetComponent<RectTransform>();
                rail.SetParent(root.transform, false);
                TopStretch(rail, TrackY, 0);

                var nodes = new EvolutionStrip.Node[Nodes];
                for (int i = 0; i < Nodes; i++)
                {
                    var node = new GameObject($"dang_{i + 1}", typeof(RectTransform)).GetComponent<RectTransform>();
                    node.SetParent(rail, false);
                    float x = i / (Nodes - 1f);
                    node.anchorMin = node.anchorMax = new Vector2(x, 0.5f);
                    node.pivot = new Vector2(0.5f, 0.5f);
                    node.sizeDelta = new Vector2(1.6f * Pad, BarH); // mốc gần nhau (sao 1, 6, 11, 16 trên thanh 1..20)
                    node.anchoredPosition = Vector2.zero;

                    var portrait = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, node)).GetComponent<HeroPortrait>();
                    var prt = portrait.Rect;
                    prt.anchorMin = prt.anchorMax = new Vector2(0.5f, 0.5f);
                    prt.sizeDelta = new Vector2(PortraitH * HeroArt.W / HeroArt.H, PortraitH);
                    prt.anchoredPosition = new Vector2(0, BarH / 2 + 4); // chân (pivot của ChanDung) đứng trên thanh

                    var stars = ((GameObject)PrefabUtility.InstantiatePrefab(kit.stars.gameObject, node)).GetComponent<UiStars>();
                    stars.SetSize(28); // to hơn cho rõ (người dùng dặn 2026-11-19)
                    stars.SetTier(i, Core.StarTier.PerTier);
                    var srt = stars.Rect;
                    srt.anchorMin = srt.anchorMax = new Vector2(0.5f, 0.5f);
                    srt.pivot = new Vector2(0.5f, 0.5f);
                    srt.anchoredPosition = new Vector2(0, TrackY - StarsY);

                    var name = Label(lineLabel, node, "ten");
                    name.rectTransform.sizeDelta = new Vector2(1.6f * Pad + 20, 34);
                    name.rectTransform.anchoredPosition = new Vector2(0, TrackY - NameY);
                    nodes[i] = new EvolutionStrip.Node { root = node, portrait = portrait, stars = stars, name = name };
                }

                var note = Label(lineLabel, root.transform, "ghi_chu");
                var nrt = note.rectTransform;
                nrt.anchorMin = nrt.anchorMax = new Vector2(0.6f, 1);
                nrt.sizeDelta = new Vector2(520, 60);
                nrt.anchoredPosition = new Vector2(0, -(StarsY + NameY) / 2);
                note.text = "Dòng 1 dạng: lên sao không đổi hình";
                note.gameObject.SetActive(false);

                // nút Tiến hóa: trên thanh (tâm nút trùng tâm thanh), Bind đặt ngang giữa mốc đang ở và mốc kế; dòng giá ở hàng tên bậc
                var evoBtn = ((GameObject)PrefabUtility.InstantiatePrefab(kit.Button(BtnSize.Tiny).gameObject, rail)).GetComponent<SketchButton>();
                evoBtn.name = "nut_tien_hoa";
                evoBtn.SetRole(BtnColor.Green);
                evoBtn.SetText("Tiến hóa");
                evoBtn.FitWidth();
                var ert = evoBtn.Rect;
                ert.anchorMin = ert.anchorMax = new Vector2(0.5f, 0.5f);
                ert.pivot = new Vector2(0.5f, 0.5f);
                ert.anchoredPosition = Vector2.zero;
                var pulse = evoBtn.GetComponent<Pulse>();
                if (!pulse) pulse = evoBtn.gameObject.AddComponent<Pulse>();
                pulse.enabled = false;
                evoBtn.gameObject.SetActive(false);
                var cost = Label(lineLabel, rail, "gia_tien_hoa");
                cost.rectTransform.sizeDelta = new Vector2(1.6f * Pad + 60, 34);
                cost.rectTransform.anchoredPosition = new Vector2(0, TrackY - NameY);
                cost.fontStyle = FontStyles.Bold;
                cost.text = "20/20 đá · cấp 30";
                cost.gameObject.SetActive(false);

                var strip = root.GetComponent<EvolutionStrip>();
                strip.Setup(bar, rail, nodes, note, evoBtn, cost, pulse);
                evo.objectReferenceValue = strip;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, DialogPath);
                Debug.Log($"[Tiến hóa] Đã dựng thanh mốc tiến hóa vào {DialogPath} (cao {Height}, dưới hàng \"{row.name}\").");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // Nút hack tiến hóa (HeroDetailDialog.HackStar): nút kit Tiny màu tím ở góc trái sân khấu (nền ô xem), ngay trên hàng nút
        // clip, chỉ hiện trong Editor. Chạy lại thì dựng lại nút.
        [MenuItem("PokiClash/Prefab/Thêm nút hack tiến hóa vào ChiTietTuong", priority = 61)]
        static void BuildHack()
        {
            var kitGuids = AssetDatabase.FindAssets("t:UiKit");
            if (kitGuids.Length == 0)
            {
                Debug.LogError("[Tiến hóa] Không thấy asset UiKit.");
                return;
            }
            var kit = AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(kitGuids[0]));
            var contents = PrefabUtility.LoadPrefabContents(DialogPath);
            try
            {
                var dlg = contents.GetComponentInChildren<HeroDetailDialog>(true);
                var so = new SerializedObject(dlg);
                var stage = (Image)so.FindProperty("p.viewBg").objectReferenceValue;
                var hack = so.FindProperty("p.hackStar");
                if (!stage)
                {
                    Debug.LogError("[Tiến hóa] ChiTietTuong thiếu nền ô xem (p.viewBg).");
                    return;
                }
                if (hack.objectReferenceValue) Object.DestroyImmediate(((Component)hack.objectReferenceValue).gameObject);
                var btn = ((GameObject)PrefabUtility.InstantiatePrefab(kit.Button(BtnSize.Tiny).gameObject, stage.transform)).GetComponent<SketchButton>();
                btn.name = "nut_hack_tien_hoa";
                btn.SetRole(BtnColor.Purple);
                btn.SetText("Hack: 2 sao");
                btn.FitWidth();
                var rt = btn.Rect;
                rt.anchorMin = rt.anchorMax = rt.pivot = Vector2.zero;
                rt.anchoredPosition = new Vector2(18, 64); // trên hàng 4 nút clip (cao khoảng 47 tính từ đáy sân khấu), không che nút nào
                btn.gameObject.SetActive(false); // Render bật trong Editor
                hack.objectReferenceValue = btn;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, DialogPath);
                Debug.Log($"[Tiến hóa] Đã thêm nút hack tiến hóa vào {DialogPath} (góc trái \"{stage.name}\", trên hàng nút clip).");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // Nhãn bậc sao + thanh mảnh / đá (HeroDetailDialog.Parts.tierLabel, evolveBar, evolveIcon): nhãn chép từ nhãn độ hiếm, đặt ngay
        // sau hàng sao (cùng hàng ngang); một hàng mới (LayoutElement cao 46) ngay trên khối chứa dòng điều kiện tiến hóa trong cột dọc của
        // hộp: icon 40×40 bên trái, thanh kit (loại Exp) giãn ngang. Chạy lại thì dựng lại.
        [MenuItem("PokiClash/Prefab/Hộp chi tiết tướng: nhãn bậc sao + thanh mảnh, đá", priority = 62)]
        static void BuildStarStep()
        {
            var kitGuids = AssetDatabase.FindAssets("t:UiKit");
            if (kitGuids.Length == 0)
            {
                Debug.LogError("[Tiến hóa] Không thấy asset UiKit.");
                return;
            }
            var kit = AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(kitGuids[0]));
            var contents = PrefabUtility.LoadPrefabContents(DialogPath);
            try
            {
                var dlg = contents.GetComponentInChildren<HeroDetailDialog>(true);
                var so = new SerializedObject(dlg);
                var stars = (UiStars)so.FindProperty("p.stars").objectReferenceValue;
                var rarity = (TextMeshProUGUI)so.FindProperty("p.rarity").objectReferenceValue;
                var need = (TextMeshProUGUI)so.FindProperty("p.evolveNeed").objectReferenceValue;
                var tierProp = so.FindProperty("p.tierLabel");
                var barProp = so.FindProperty("p.evolveBar");
                var iconProp = so.FindProperty("p.evolveIcon");
                if (!stars || !rarity || !need)
                {
                    Debug.LogError("[Tiến hóa] ChiTietTuong thiếu hàng sao, nhãn độ hiếm hoặc dòng điều kiện tiến hóa.");
                    return;
                }
                if (tierProp.objectReferenceValue) Object.DestroyImmediate(((Component)tierProp.objectReferenceValue).gameObject);
                if (barProp.objectReferenceValue) Object.DestroyImmediate(((Component)barProp.objectReferenceValue).transform.parent.gameObject);

                // nhãn bậc: cùng cha với hàng sao, ngay sau nó
                var tier = Object.Instantiate(rarity.gameObject, stars.transform.parent, false).GetComponent<TextMeshProUGUI>();
                tier.name = "bac_sao";
                tier.transform.SetSiblingIndex(stars.transform.GetSiblingIndex() + 1);
                tier.text = "Bạc 3 sao";
                tier.textWrappingMode = TextWrappingModes.NoWrap;
                if (!tier.GetComponent<ContentSizeFitter>())
                    tier.gameObject.AddComponent<ContentSizeFitter>().horizontalFit = ContentSizeFitter.FitMode.PreferredSize;
                tierProp.objectReferenceValue = tier;

                // hàng thanh: tổ tiên đầu tiên của dòng điều kiện có cha là cột dọc; hàng mới đứng ngay trước nó
                var row = need.transform;
                while (row.parent && !row.parent.GetComponent<VerticalLayoutGroup>()) row = row.parent;
                if (!row.parent)
                {
                    Debug.LogError("[Tiến hóa] Không thấy cột dọc chứa dòng điều kiện tiến hóa.");
                    return;
                }
                const float RowH = 46, IconS = 40, Side = 120;
                var host = new GameObject("thanh_buoc_sao", typeof(RectTransform), typeof(LayoutElement));
                host.transform.SetParent(row.parent, false);
                host.transform.SetSiblingIndex(row.GetSiblingIndex());
                host.GetComponent<LayoutElement>().preferredHeight = RowH;
                var hrt = (RectTransform)host.transform;
                hrt.sizeDelta = new Vector2(hrt.sizeDelta.x, RowH);

                var icon = new GameObject("icon", typeof(RectTransform), typeof(Image)).GetComponent<Image>();
                icon.transform.SetParent(host.transform, false);
                icon.preserveAspect = true;
                icon.raycastTarget = false;
                var irt = icon.rectTransform;
                irt.anchorMin = irt.anchorMax = new Vector2(0, 0.5f);
                irt.pivot = new Vector2(0, 0.5f);
                irt.sizeDelta = new Vector2(IconS, IconS);
                irt.anchoredPosition = new Vector2(Side - IconS - 10, 0);

                var bar = ((GameObject)PrefabUtility.InstantiatePrefab(kit.bar.gameObject, host.transform)).GetComponent<UiBar>();
                bar.name = "thanh";
                bar.SetKind(UiBar.Kind.Shard);
                var brt = (RectTransform)bar.transform;
                brt.anchorMin = new Vector2(0, 0.5f);
                brt.anchorMax = new Vector2(1, 0.5f);
                brt.pivot = new Vector2(0.5f, 0.5f);
                brt.offsetMin = new Vector2(Side, -BarH / 2);
                brt.offsetMax = new Vector2(-Side, BarH / 2);

                barProp.objectReferenceValue = bar;
                iconProp.objectReferenceValue = icon;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, DialogPath);
                Debug.Log($"[Tiến hóa] Đã thêm nhãn bậc sao (cạnh \"{stars.name}\") và thanh mảnh / đá (trên \"{row.name}\") vào {DialogPath}.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        [MenuItem("PokiClash/Thử/Thanh tiến hóa: chụp hộp chi tiết ở các mốc (đang Play)", priority = 109)]
        static void TryStrip()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunStrip());
        }

        static IEnumerator RunStrip()
        {
            var s = App.Save.Data;
            BootTitle.Dismiss(); // màn mở game che mọi thứ
            Debug.Log("[Tiến hóa] Bắt đầu chụp hộp chi tiết");
            try
            {
                App.Router.Go(SceneIds.Heroes);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Heroes) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(0.5f);
                yield return Shot("luoi");
                // (tướng, có chưa, sao tổng, đủ đá + cấp): bậc theo dạng 2026-11-19. Dòng 3 dạng (Mầm Ú) ở Đồng 1★, Bạc 1★, Vàng 1★, Vàng 5★;
                // dòng 2 dạng (Voọc Tướng) ở Đồng 3★, Đồng 5★ chờ tiến hóa (thiếu đá, rồi đủ), Bạc 3★; dòng 1 dạng (Bùn Ngoạm, Thiết Cưa hai
                // dạng cùng hình); tướng chưa có
                var cases = new (string id, bool owned, int star, bool rich)[]
                {
                    ("mam_u", true, 1, false), ("mam_u", true, 6, false), ("mam_u", true, 11, false), ("mam_u", true, 20, false),
                    ("tho_hoang", true, 3, false), ("tho_hoang", true, 5, false), ("tho_hoang", true, 5, true), ("tho_hoang", true, 13, false),
                    ("ho_kim_cuong", true, 11, false), ("phi_thuong", true, 6, false), ("han_ngac", false, 1, false),
                };
                foreach (var (id, owned, star, rich) in cases)
                {
                    var hp = s.Hero(id);
                    hp.owned = owned;
                    hp.star = star;
                    hp.shards = rich ? 999 : 7;
                    s.evoStones = rich ? 500 : 3;
                    s.level = rich ? 200 : 15;
                    HeroDetail.Open(id);
                    yield return new WaitForSecondsRealtime(0.8f);
                    yield return Shot($"{id}_{(owned ? "sao" + star : "chua_co")}{(rich ? "_du" : "")}");
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.3f);
                }
                Debug.Log("[Tiến hóa] Đã chụp " + PlayTour.ShotDir);
            }
            finally
            {
                App.Save.Load(); // bỏ mọi thay đổi tạm
                App.Bars.Refresh();
            }
        }

        // Menu thử nút hack (đang Play): mở hộp chi tiết Mầm Ú (dòng 3 dạng), chụp, bấm nút hack, lặp 20 lần (đủ một vòng sao) vào
        // Temp/PokiShots/hack_*.png. Nút hack ghi bản lưu: chép bản lưu ra trước khi thử nếu cần giữ.
        [MenuItem("PokiClash/Thử/Nút hack tiến hóa: bấm thử và chụp (đang Play)", priority = 110)]
        static void TryHack()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunHack("mam_u"));
        }

        static IEnumerator RunHack(string id)
        {
            App.Router.Go(SceneIds.Heroes);
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != SceneIds.Heroes) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(0.5f);
            HeroDetail.Open(id);
            yield return new WaitForSecondsRealtime(0.8f);
            for (int i = 0; i <= Core.StarTier.MaxStar; i++)
            {
                var hp = App.Save.Data.Hero(id);
                yield return Shot($"hack_{i}_{(hp.owned ? hp.star + "sao" : "chua_co")}");
                if (i == Core.StarTier.MaxStar) break;
                var go = GameObject.Find("nut_hack_tien_hoa");
                if (!go)
                {
                    Debug.LogError("[Tiến hóa] Không thấy nút hack (menu PokiClash/Prefab/Thêm nút hack tiến hóa vào ChiTietTuong).");
                    yield break;
                }
                go.GetComponent<SketchButton>().SimulateClick();
                yield return new WaitForSecondsRealtime(1.2f);
            }
            App.Modals.CloseAll();
            Debug.Log("[Tiến hóa] Đã thử nút hack: " + PlayTour.ShotDir);
        }

        // Menu thử clip đánh (đang Play): mở hộp chi tiết Mầm Ú ở sao 1, 6, 11 (3 dạng; đặt tạm trong bộ nhớ, không ghi bản lưu), cho ô
        // xem chạy clip đánh, chụp 6 thời điểm vào Temp/PokiShots/danh_sao<n>_<i>.png, rồi nạp lại bản lưu từ đĩa.
        [MenuItem("PokiClash/Thử/Clip đánh Mầm Ú: chụp các dạng (đang Play)", priority = 111)]
        static void TryAttack()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunAttack("mam_u"));
        }

        static IEnumerator RunAttack(string id)
        {
            try
            {
                App.Router.Go(SceneIds.Heroes);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Heroes) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(0.5f);
                foreach (int star in new[] { 1, 6, 11 })
                {
                    var hp = App.Save.Data.Hero(id);
                    hp.owned = true;
                    hp.star = star;
                    HeroDetail.Open(id);
                    yield return new WaitForSecondsRealtime(0.8f);
                    var viewer = Object.FindFirstObjectByType<HeroViewer>();
                    if (!viewer) break;
                    viewer.Play(HeroViewer.Attack);
                    float start = Time.realtimeSinceStartup;
                    for (int i = 0; i < 6; i++)
                    {
                        float at = i * 0.3f; // 0, 0.3 ... 1.5 giây
                        while (Time.realtimeSinceStartup - start < at) yield return null;
                        yield return Shot($"danh_sao{star}_{i}");
                    }
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.3f);
                }
                Debug.Log("[Tiến hóa] Đã chụp clip đánh: " + PlayTour.ShotDir);
            }
            finally
            {
                App.Save.Load(); // bỏ mọi thay đổi tạm
            }
        }

        // Tự render camera (camera sticker aola vẽ vào RenderTexture của nó trước, rồi camera UI) thay vì chụp màn hình: khi Editor
        // không được focus, Game view không vẽ lại nên WaitForEndOfFrame không bao giờ tới.
        static IEnumerator Shot(string name)
        {
            yield return null;
            int w = Screen.width, h = Screen.height;
            var cams = Camera.allCameras;
            System.Array.Sort(cams, (x, y) => x.depth.CompareTo(y.depth));
            foreach (var c in cams)
                if (c.targetTexture) c.Render();
            var rt = RenderTexture.GetTemporary(w, h, 24, RenderTextureFormat.ARGB32);
            var prev = RenderTexture.active;
            foreach (var c in cams)
            {
                if (c.targetTexture) continue;
                c.targetTexture = rt;
                c.Render();
                c.targetTexture = null;
            }
            RenderTexture.active = rt;
            var tex = new Texture2D(w, h, TextureFormat.RGB24, false);
            tex.ReadPixels(new Rect(0, 0, w, h), 0, 0);
            tex.Apply();
            RenderTexture.active = prev;
            RenderTexture.ReleaseTemporary(rt);
            Directory.CreateDirectory(PlayTour.ShotDir);
            File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"evo_{name}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }

        // neo trên, giãn ngang chừa lề Pad hai bên; y: tâm cách mép trên
        static void TopStretch(RectTransform rt, float y, float h)
        {
            rt.anchorMin = new Vector2(0, 1);
            rt.anchorMax = new Vector2(1, 1);
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(-2 * Pad, h);
            rt.anchoredPosition = new Vector2(0, -y);
        }

        // chữ chép từ nhãn có sẵn của hộp (cùng phông, viền, cỡ), canh giữa, một dòng
        static TextMeshProUGUI Label(TextMeshProUGUI from, Transform parent, string name)
        {
            var t = Object.Instantiate(from.gameObject, parent, false).GetComponent<TextMeshProUGUI>();
            t.name = name;
            foreach (var c in t.GetComponents<LayoutElement>()) Object.DestroyImmediate(c);
            foreach (var c in t.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
            var rt = t.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.pivot = new Vector2(0.5f, 0.5f);
            t.alignment = TextAlignmentOptions.Center;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Truncate; // phông Pangolin không có dấu "…"
            t.text = "";
            return t;
        }
    }
}
