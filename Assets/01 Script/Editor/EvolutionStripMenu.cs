// Dựng thanh mốc tiến hóa (EvolutionStrip) vào prefab Dialogs/ChiTietTuong: một hàng mới ngay dưới hàng ô xem tướng, gồm thanh
// kit (Thanh, loại Exp) và 3 mốc (kit ChanDung, kit Sao, chữ chép từ nhãn dòng tiến hóa của hộp). Chạy lại thì dựng lại hàng đó.
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
        const int Nodes = 3; // dòng dài nhất 3 dạng
        const float Pad = 110, BarH = 32, PortraitH = 140, Top = 8;
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
                    node.sizeDelta = new Vector2(2 * Pad, BarH);
                    node.anchoredPosition = Vector2.zero;

                    var portrait = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, node)).GetComponent<HeroPortrait>();
                    var prt = portrait.Rect;
                    prt.anchorMin = prt.anchorMax = new Vector2(0.5f, 0.5f);
                    prt.sizeDelta = new Vector2(PortraitH * HeroArt.W / HeroArt.H, PortraitH);
                    prt.anchoredPosition = new Vector2(0, BarH / 2 + 4); // chân (pivot của ChanDung) đứng trên thanh

                    var stars = ((GameObject)PrefabUtility.InstantiatePrefab(kit.stars.gameObject, node)).GetComponent<UiStars>();
                    stars.SetSize(26);
                    stars.Set(i == 0 ? 1 : 2 * i + 1, i == 0 ? 1 : 2 * i + 1);
                    var srt = stars.Rect;
                    srt.anchorMin = srt.anchorMax = new Vector2(0.5f, 0.5f);
                    srt.pivot = new Vector2(0.5f, 0.5f);
                    srt.anchoredPosition = new Vector2(0, TrackY - StarsY);

                    var name = Label(lineLabel, node, "ten");
                    name.rectTransform.sizeDelta = new Vector2(2 * Pad + 20, 34);
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

                var strip = root.GetComponent<EvolutionStrip>();
                strip.Setup(bar, rail, nodes, note);
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

        [MenuItem("PokiClash/Thử/Thanh tiến hóa: chụp hộp chi tiết ở các mốc (đang Play)", priority = 109)]
        static void TryStrip()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunStrip());
        }

        static IEnumerator RunStrip()
        {
            var s = App.Save.Data;
            Debug.Log("[Tiến hóa] Bắt đầu chụp hộp chi tiết");
            try
            {
                App.Router.Go(SceneIds.Heroes);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Heroes) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(0.5f);
                yield return Shot("luoi");
                // (tướng, có chưa, sao): dòng 3 dạng ở sao 1, 3, 5; dòng 2 dạng ở sao 2, 4 và chưa có; dòng 1 dạng; tướng chưa có
                var cases = new (string id, bool owned, int star)[]
                {
                    ("giot_suong", true, 1), ("giot_suong", true, 3), ("giot_suong", true, 5),
                    ("tieu_y", true, 2), ("tieu_y", true, 4), ("meo_quyen", false, 1), ("kiem_linh", true, 2), ("huyen_vu", false, 1),
                };
                foreach (var (id, owned, star) in cases)
                {
                    var hp = s.Hero(id);
                    hp.owned = owned;
                    hp.star = star;
                    HeroDetail.Open(id);
                    yield return new WaitForSecondsRealtime(0.8f);
                    yield return Shot($"{id}_{(owned ? "sao" + star : "chua_co")}");
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

        // Menu thử nút hack (đang Play): mở hộp chi tiết Giọt Sương, chụp, bấm nút hack, lặp 6 lần (đủ một vòng sao) vào
        // Temp/PokiShots/hack_*.png. Nút hack ghi bản lưu: chép bản lưu ra trước khi thử nếu cần giữ.
        [MenuItem("PokiClash/Thử/Nút hack tiến hóa: bấm thử và chụp (đang Play)", priority = 110)]
        static void TryHack()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunHack("giot_suong"));
        }

        static IEnumerator RunHack(string id)
        {
            App.Router.Go(SceneIds.Heroes);
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != SceneIds.Heroes) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(0.5f);
            HeroDetail.Open(id);
            yield return new WaitForSecondsRealtime(0.8f);
            for (int i = 0; i < 7; i++)
            {
                var hp = App.Save.Data.Hero(id);
                yield return Shot($"hack_{i}_{(hp.owned ? hp.star + "sao" : "chua_co")}");
                if (i == 6) break;
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

        // Menu thử clip đánh (đang Play): mở hộp chi tiết Giọt Sương ở sao 1, 3, 5 (đặt tạm trong bộ nhớ, không ghi bản lưu), cho ô
        // xem chạy clip đánh, chụp 6 thời điểm vào Temp/PokiShots/danh_sao<n>_<i>.png, rồi nạp lại bản lưu từ đĩa.
        [MenuItem("PokiClash/Thử/Clip đánh Giọt Sương: chụp các dạng (đang Play)", priority = 111)]
        static void TryAttack()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunAttack("giot_suong"));
        }

        static IEnumerator RunAttack(string id)
        {
            try
            {
                App.Router.Go(SceneIds.Heroes);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Heroes) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(0.5f);
                foreach (int star in new[] { 1, 3, 5 })
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
