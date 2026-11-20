// Hộp chi tiết tướng (Dialogs/ChiTietTuong): thêm nút 6, 7 "RA SÂN", "CHẾT" xem clip appear, die của rig .atomik (lô quái Thủy
// 2026-11-11) và nút 8 "ĐI" xem clip walk (2026-11-20). Chép nút Mana (p.clips[4], menu "Hộp chi tiết tướng: hạt lửa + nút Mana"
// phải chạy trước), gán HeroDetailDialog.p.clips[5..7] (ClipIds[5..7] = appear, die, walk). RA SÂN, CHẾT ở cuối hàng; ĐI đứng ngay
// sau ĐỨNG. Nút ẩn sẵn trong prefab: HeroDetailDialog bật khi dạng đang xem có clip đó. Chạy lại không tạo trùng, chỉ sửa nhãn,
// thứ tự và cách xếp hàng.
// Xếp hàng (2026-11-20, người dùng: nút cuối tràn mép thẻ): hàng căng ngang theo ô nền trừ lề, HorizontalLayoutGroup điều khiển
// bề rộng con, mọi nút flexibleWidth 1 nên các nút đang hiện chia đều; nút ẩn không chiếm chỗ. Bản cũ để ChildControlWidth = 0 nên
// nút giữ bề rộng 100 của prefab Nut_Ti, preferredWidth thu nhỏ không có tác dụng. Nhãn Nut_Ti tự co chữ (26 → 15,6).
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HeroDetailClipMenu
    {
        const string DetailPath = "Assets/04 Prefabs/Dialogs/ChiTietTuong.prefab";
        static readonly string[] Labels = { "RA SÂN", "CHẾT", "ĐI" };
        static readonly string[] Names = { "nut_RaSan", "nut_Chet", "nut_Di" };
        const int First = 5, WalkSlot = 2; // Labels[WalkSlot] = nút Đi: đứng sau nút Đứng thay vì cuối hàng
        const float Margin = 12, Spacing = 6; // lề hai bên hàng trong ô nền, khoảng giữa hai nút

        [MenuItem("PokiClash/Prefab/Hộp chi tiết tướng: nút Đi, Ra sân, Chết + xếp hàng nút clip", priority = 64)]
        public static void Build()
        {
            var root = PrefabUtility.LoadPrefabContents(DetailPath);
            try
            {
                var dlg = root.GetComponentInChildren<HeroDetailDialog>(true);
                if (!dlg)
                {
                    Debug.LogError("[Hộp chi tiết] ChiTietTuong thiếu HeroDetailDialog.");
                    return;
                }
                var so = new SerializedObject(dlg);
                var clips = so.FindProperty("p.clips");
                var src = clips.arraySize > 4 ? clips.GetArrayElementAtIndex(4).objectReferenceValue as UI.SketchButton : null;
                if (!src)
                {
                    Debug.LogError("[Hộp chi tiết] Chưa có nút Mana (p.clips[4]): chạy menu \"Hộp chi tiết tướng: hạt lửa + nút Mana\" trước.");
                    return;
                }
                // tăng cỡ mảng thì Unity chép phần tử cuối (nút Mana) vào ô mới: dọn về rỗng, và coi ô trỏ vào nút Mana là rỗng
                int old = clips.arraySize;
                if (old < First + Labels.Length)
                {
                    clips.arraySize = First + Labels.Length;
                    for (int i = old; i < clips.arraySize; i++) clips.GetArrayElementAtIndex(i).objectReferenceValue = null;
                }
                // trả nút Mana về đúng (lần chạy lỗi trước đã đổi tên, nhãn, ẩn nó): tên, nhãn, hiện, đứng ngay sau nút Chiêu
                var row = src.transform.parent;
                src.gameObject.name = "nut_Mana";
                var srcLabel = src.GetComponentInChildren<TMPro.TextMeshProUGUI>(true);
                if (srcLabel) srcLabel.text = "Mana";
                src.gameObject.SetActive(true);
                var skill = clips.GetArrayElementAtIndex(2).objectReferenceValue as UI.SketchButton;
                if (skill && skill.transform.parent == row) src.transform.SetSiblingIndex(skill.transform.GetSiblingIndex() + 1);
                for (int i = 0; i < Labels.Length; i++)
                {
                    var cur = clips.GetArrayElementAtIndex(First + i).objectReferenceValue as UI.SketchButton;
                    if (cur == src) cur = null;
                    if (!cur)
                    {
                        var go = Object.Instantiate(src.gameObject, row);
                        cur = go.GetComponent<UI.SketchButton>();
                        clips.GetArrayElementAtIndex(First + i).objectReferenceValue = cur;
                    }
                    cur.gameObject.name = Names[i];
                    var idleBtn = clips.GetArrayElementAtIndex(0).objectReferenceValue as UI.SketchButton;
                    if (i == WalkSlot && idleBtn && idleBtn.transform.parent == row)
                    {
                        cur.transform.SetAsLastSibling(); // gỡ khỏi chỗ cũ rồi chèn sau nút Đứng
                        cur.transform.SetSiblingIndex(idleBtn.transform.GetSiblingIndex() + 1);
                    }
                    else cur.transform.SetAsLastSibling();
                    var label = cur.GetComponentInChildren<TMPro.TextMeshProUGUI>(true);
                    if (label) label.text = Labels[i];
                    cur.gameObject.SetActive(false);
                }
                so.ApplyModifiedPropertiesWithoutUndo();

                // xếp hàng: căng ngang theo ô nền trừ lề, nhóm điều khiển bề rộng con, các nút đang hiện chia đều
                var rt = (RectTransform)row;
                rt.anchorMin = new Vector2(0, rt.anchorMin.y);
                rt.anchorMax = new Vector2(1, rt.anchorMax.y);
                rt.pivot = new Vector2(0.5f, rt.pivot.y);
                rt.anchoredPosition = new Vector2(0, rt.anchoredPosition.y);
                rt.sizeDelta = new Vector2(-2 * Margin, rt.sizeDelta.y);
                var hl = rt.GetComponent<HorizontalLayoutGroup>();
                if (hl)
                {
                    hl.childControlWidth = true;
                    hl.childForceExpandWidth = true;
                    hl.childAlignment = TextAnchor.MiddleCenter;
                    hl.spacing = Spacing;
                    hl.padding = new RectOffset(0, 0, hl.padding.top, hl.padding.bottom);
                }
                foreach (Transform c in rt)
                {
                    // preferredWidth 0 (không -1): LayoutElement thắng Image (Image báo bề rộng theo ảnh), cả hàng chia theo flexible
                    var le = c.GetComponent<LayoutElement>() ?? c.gameObject.AddComponent<LayoutElement>();
                    le.minWidth = 0;
                    le.preferredWidth = 0;
                    le.flexibleWidth = 1;
                }
                PrefabUtility.SaveAsPrefabAsset(root, DetailPath);
                Debug.Log($"[Hộp chi tiết] {DetailPath}: {rt.childCount} nút clip (ĐI sau ĐỨNG; RA SÂN, CHẾT cuối hàng; ẩn khi dạng " +
                          $"không có clip), hàng rộng {((RectTransform)rt.parent).rect.width - 2 * Margin:0} chia đều.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // Thử nút ĐI (đang Play): mở hộp chi tiết từng tướng trong Temp/PokiShots/di_ids.txt, bấm nút nut_Di như người chơi, chụp 6 khung trong 3 giây (walk phải lặp, không về
        // đứng) vào Temp/PokiShots/di_<tướng>_s<sao>_<i>.png. Tướng không có walk thì ghi nút đang ẩn. Chỉ sửa bản lưu tạm, cuối đọc lại.
        [MenuItem("PokiClash/Thử/Hộp chi tiết tướng: bấm nút Đi và chụp (đang Play)", priority = 111)]
        static void TryWalk()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Nút Đi] Cần đang Play và game đã khởi động xong.");
                return;
            }
            // danh sách tướng: Temp/PokiShots/di_ids.txt (mỗi dòng "id" hoặc "id sao"), không có thì ba tướng mẫu
            var list = System.IO.Path.Combine(PlayTour.ShotDir, "di_ids.txt");
            var ids = System.IO.File.Exists(list)
                ? System.Array.FindAll(System.IO.File.ReadAllLines(list), l => l.Trim().Length > 0)
                : new[] { "tho_hoang", "mam_u", "han_ngac" };
            App.I.StartCoroutine(RunWalk(ids));
        }

        static System.Collections.IEnumerator RunWalk(string[] ids)
        {
            BootTitle.Dismiss();
            try
            {
                App.Router.Go(SceneIds.Heroes);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Heroes) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(0.5f);
                foreach (var line in ids)
                {
                    var parts = line.Trim().Split(' ');
                    string id = parts[0];
                    int star = parts.Length > 1 && int.TryParse(parts[1], out int st) ? st : 3;
                    var hp = App.Save.Data.Hero(id);
                    hp.owned = true;
                    hp.star = star;
                    HeroDetail.Open(id);
                    yield return new WaitForSecondsRealtime(0.8f);
                    var dlg = Object.FindAnyObjectByType<HeroDetailDialog>();
                    UI.SketchButton walk = null;
                    if (dlg)
                        foreach (var b in dlg.GetComponentsInChildren<UI.SketchButton>(true))
                            if (b.name == Names[WalkSlot]) walk = b;
                    if (!walk || !walk.gameObject.activeInHierarchy)
                    {
                        Debug.Log($"[Nút Đi] {id}: nút {(walk ? "đang ẩn (dạng không có walk)" : "không tìm thấy")}.");
                        yield return Shot($"di_{id}_s{star}_an");
                    }
                    else
                    {
                        walk.SimulateClick();
                        for (int i = 0; i < 6; i++)
                        {
                            yield return Shot($"di_{id}_s{star}_{i}");
                            yield return new WaitForSecondsRealtime(0.5f);
                        }
                        Debug.Log($"[Nút Đi] {id}: đã bấm và chụp 6 khung.");
                    }
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.3f);
                }
                Debug.Log("[Nút Đi] Xong: " + PlayTour.ShotDir);
            }
            finally
            {
                App.Save.Load();
                App.Bars.Refresh();
            }
        }

        // như EvolutionStripMenu.Shot: tự vẽ mọi camera vào ảnh tạm (Game view không cần đang hiện)
        static System.Collections.IEnumerator Shot(string name)
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
            System.IO.Directory.CreateDirectory(PlayTour.ShotDir);
            System.IO.File.WriteAllBytes(System.IO.Path.Combine(PlayTour.ShotDir, name + ".png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }
    }
}
