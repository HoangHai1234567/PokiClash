// Tour soi bảng tổng kết cuộn của màn mở rương nhóm (2026-11-26): 5 rương (mặc định vàng ×3, hoặc theo nội dung cờ) vào khay, mở tất cả, chụp dày lúc ô bật và lưới
// cuộn theo hàng, rồi thử kéo lưới xuống (xem lại hàng đầu) và bấm "Nhận". Menu "PokiClash/Thử/Máy bi/soi bảng tổng kết cuộn (chụp)"
// hoặc cờ Temp/chest_scroll_tour.flag (Unity đang không Play: tự vào Play, chụp xong tự Stop). Bản lưu sao lại đầu tour, trả lại ở finally.
// Ảnh và log: Temp/PokiShots/chest_scroll/.
using System.Collections;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using PokiClash.Core;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class MachineChestScrollTour
    {
        const BindingFlags F = BindingFlags.NonPublic | BindingFlags.Instance;
        const string Key = "MachineChestScrollTour";
        static double nextPoll, tourStart;
        static bool stopAfter;
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/chest_scroll_tour.flag"));
        static string Dir => Path.Combine(PlayTour.ShotDir, "chest_scroll");

        [MenuItem("PokiClash/Thử/Máy bi/soi bảng tổng kết cuộn (chụp)", priority = 119)]
        static void Run()
        {
            if (EditorApplication.isPlaying)
            {
                if (App.I != null) App.I.StartCoroutine(Tour());
                return;
            }
            File.WriteAllText(Flag, "1");
        }

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating) return;
            if (!EditorApplication.isPlayingOrWillChangePlaymode)
            {
                if (!File.Exists(Flag)) return;
                SessionState.SetString(Key + "Spec", File.ReadAllText(Flag).Trim());
                File.Delete(Flag);
                SessionState.SetBool(Key, true);
                tourStart = EditorApplication.timeSinceStartup;
                EditorApplication.isPlaying = true;
                return;
            }
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 150)
            {
                Debug.LogWarning("[Rương cuộn] Tour quá 150 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false)) Application.runInBackground = true; // Unity nằm nền thì vòng game đứng
            if (EditorApplication.isPlaying && SessionState.GetBool(Key, false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null)
            {
                SessionState.SetBool(Key, false);
                stopAfter = true;
                BootTitle.Dismiss();
                App.I.StartCoroutine(Tour());
            }
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, name + ".png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }

        static IEnumerator Wait(float s)
        {
            for (float t = 0; t < s; t += Time.unscaledDeltaTime) yield return null;
        }

        static float Num(object o, string field) => (float)(o.GetType().GetField(field, F)?.GetValue(o) ?? 0f);

        static IEnumerator Tour()
        {
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            var log = new StringBuilder();
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            try
            {
                yield return Wait(1.5f);
                var s = App.Save.Data;
                s.balls = Mathf.Max(s.balls, 50);
                s.chests.Clear();
                // nội dung cờ: danh sách "loại*x" cách nhau dấu phẩy (vd "chest_gold*10,chest_silver*10"); trống thì 5 rương vàng ×3
                var spec = SessionState.GetString(Key + "Spec", "");
                if (!spec.Contains("chest_")) spec = "chest_gold*3,chest_gold*3,chest_gold*3,chest_gold*3,chest_gold*3";
                foreach (var part in spec.Split(','))
                {
                    var kv = part.Trim().Split('*');
                    s.chests.Add(new PendingChest { kind = kv[0], x = kv.Length > 1 && int.TryParse(kv[1], out int cx) ? cx : 1 });
                }
                log.AppendLine("ruong: " + spec);
                App.Save.Save();
                App.Router.Go(SceneIds.Machine);
                float t0 = Time.realtimeSinceStartup;
                MachineScene m = null;
                while ((!(m = Object.FindAnyObjectByType<MachineScene>()) || App.Router.Busy) && Time.realtimeSinceStartup - t0 < 25) yield return null;
                yield return Wait(1.5f);
                if (!m)
                {
                    log.AppendLine("KHONG vao duoc man may bi");
                    yield break;
                }
                while (App.Modals.Count > 0)
                {
                    App.Modals.Back();
                    yield return Wait(0.4f);
                }
                typeof(MachineScene).GetMethod("OpenFromTray", F)?.Invoke(m, null);
                MachineChestOpen open = null;
                for (float t = 0; t < 6 && !(open = Object.FindAnyObjectByType<MachineChestOpen>()); t += Time.unscaledDeltaTime) yield return null;
                if (!open)
                {
                    log.AppendLine("KHONG thay man mo ruong nhom");
                    yield break;
                }
                yield return Wait(1.4f);
                yield return Shot("00_cho");
                var title = open.transform.Find("tieu_de");
                log.AppendLine($"ruy bang luc cho: {(title && title.gameObject.activeInHierarchy ? "hien" : "an")}");
                var all = open.GetComponentsInChildren<SketchButton>().FirstOrDefault(b => b.name == "nut_Mở tất cả");
                if (all) all.SimulateClick();
                else log.AppendLine("KHONG thay nut Mo tat ca");
                // chờ bảng tổng kết dựng xong
                Transform grid = null;
                for (float t = 0; t < 12 && !grid; t += Time.unscaledDeltaTime)
                {
                    grid = open.GetComponentsInChildren<Transform>(true).FirstOrDefault(x => x.name == "tong_ket");
                    yield return null;
                }
                if (!grid)
                {
                    log.AppendLine("KHONG thay bang tong ket");
                    yield break;
                }
                var view = (RectTransform)grid.parent;
                int tiles = grid.GetComponentsInChildren<RewardTile>(true).Length;
                log.AppendLine($"so o: {tiles}; khung: {view.name} mask={(bool)view.GetComponent<RectMask2D>()} cao {view.rect.height:0} rong {view.rect.width:0}; " +
                               $"luoi scale {grid.localScale.x:0.00}; sumMax {Num(open, "sumMax"):0}; man {Screen.width}x{Screen.height}");
                // chụp mỗi 0,25 giây tới khi nút "Nhận" hiện (tối đa 14 giây)
                SketchButton ok = null;
                int n = 1;
                for (float t = 0; t < 14 && !ok; t += 0.25f)
                {
                    yield return Shot($"{n:00}_bat_o");
                    log.AppendLine($"  anh {n:00}: sumY {Num(open, "sumY"):0} / dich {Num(open, "sumTarget"):0}; ruy bang {(title && title.gameObject.activeInHierarchy ? "hien" : "an")}; " +
                                   $"o da bat {grid.GetComponentsInChildren<RewardTile>(true).Count(x => x.transform.localScale.y > 0.5f)}");
                    n++;
                    yield return Wait(0.25f);
                    ok = open.GetComponentsInChildren<SketchButton>().FirstOrDefault(b => b.name.StartsWith("nut_Nhận") || b.name.StartsWith("nut_Mở tiếp"));
                }
                yield return Wait(0.5f);
                yield return Shot($"{n++:00}_het");
                log.AppendLine($"het: sumY {Num(open, "sumY"):0} / sumMax {Num(open, "sumMax"):0}; nut {(ok ? ok.name : "KHONG")}");
                // ô nào ló ra ngoài khung cắt mà vẫn vẽ? (đo góc ô so với khung, chỉ ghi số ô nằm hẳn ngoài khung: phải bị cắt hết)
                // kéo lưới xuống 45 % chiều cao màn (xem lại hàng đầu): sự kiện kéo gửi thẳng vào màn mở rương
                var ray = open.GetComponent<GraphicRaycaster>();
                var cam = ray ? ray.eventCamera : null;
                Vector2 from = RectTransformUtility.WorldToScreenPoint(cam, view.TransformPoint(view.rect.center));
                var ev = new PointerEventData(EventSystem.current)
                {
                    position = from, pressPosition = from, button = PointerEventData.InputButton.Left,
                    pointerPressRaycast = new RaycastResult { module = ray, gameObject = open.gameObject },
                    pointerDrag = open.gameObject,
                };
                ExecuteEvents.Execute(open.gameObject, ev, ExecuteEvents.initializePotentialDrag);
                log.AppendLine($"keo: quyen keo sau initializePotentialDrag = {(ev.pointerDrag ? "giu" : "tra lai (LOI neu luoi cao hon khung)")}");
                if (ev.pointerDrag)
                {
                    ExecuteEvents.Execute(open.gameObject, ev, ExecuteEvents.beginDragHandler);
                    for (int i = 1; i <= 12; i++)
                    {
                        ev.position = from + new Vector2(0, -Screen.height * 0.45f * i / 12f);
                        ExecuteEvents.Execute(open.gameObject, ev, ExecuteEvents.dragHandler);
                        yield return null;
                    }
                    yield return Shot($"{n++:00}_dang_keo");
                    log.AppendLine($"dang keo: sumY {Num(open, "sumY"):0}");
                    ExecuteEvents.Execute(open.gameObject, ev, ExecuteEvents.endDragHandler);
                    yield return Wait(1.0f);
                    yield return Shot($"{n++:00}_tha_tay");
                    log.AppendLine($"tha tay 1 giay: sumY {Num(open, "sumY"):0}");
                }
                // chạm ngoài khung (chỗ nút): phải trả quyền kéo
                var out2 = new PointerEventData(EventSystem.current)
                {
                    position = new Vector2(Screen.width * 0.5f, Screen.height * 0.04f),
                    pointerPressRaycast = new RaycastResult { module = ray, gameObject = open.gameObject }, pointerDrag = open.gameObject,
                };
                ExecuteEvents.Execute(open.gameObject, out2, ExecuteEvents.initializePotentialDrag);
                log.AppendLine($"cham ngoai khung: quyen keo = {(out2.pointerDrag ? "giu (LOI)" : "tra lai")}");
                if (ok) ok.SimulateClick();
                yield return Wait(1.2f);
                yield return Shot($"{n++:00}_xong");
                log.AppendLine($"sau Nhan: man mo ruong {(Object.FindAnyObjectByType<MachineChestOpen>() ? "con" : "da dong")}");
                while (App.Modals.Count > 0)
                {
                    App.Modals.Back();
                    yield return Wait(0.4f);
                }
            }
            finally
            {
                if (backup != null) File.WriteAllText(path, backup);
                App.Save.Load();
                log.AppendLine($"ban luu tra lai: {(backup != null && File.ReadAllText(path) == backup ? "khop" : "KHONG khop / khong co ban sao")}");
                File.WriteAllText(Path.Combine(Dir, "log.txt"), log.ToString(), Encoding.UTF8);
                Debug.Log("[Rương cuộn] xong: " + Dir);
                tourStart = 0;
                if (stopAfter)
                {
                    stopAfter = false;
                    EditorApplication.isPlaying = false;
                }
            }
        }
    }
}
