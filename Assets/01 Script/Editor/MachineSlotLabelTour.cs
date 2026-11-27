// Tour soi nhãn mặt máy bi (2026-11-27: thẻ ô số tối, số ô to sáng, hình quà trong nấm to hơn, "+5" bỏ đậm): vào máy bi, chụp cả màn,
// phóng lớp máy (localScale, chỉ lúc chạy) để chụp nét vùng hai nấm và hàng ô đáy, đổi tạm số theo cược ×2 / ×10 (chỉ hình, không
// đổi cược thật) rồi trả lại. Cờ Temp/machine_slot_label_tour.flag (Unity không Play: tự vào Play, xong tự Stop) hoặc menu
// "PokiClash/Thử/Máy bi/nhãn ô và quà nấm (chụp)". Không ghi bản lưu. Ảnh: Temp/PokiShots/nhan_o/*.png; log "[Nhãn ô]".
using System.Collections;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class MachineSlotLabelTour
    {
        static double nextPoll, tourStart;
        static bool stopAfter;
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/machine_slot_label_tour.flag"));
        static string Dir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots/nhan_o"));

        [MenuItem("PokiClash/Thử/Máy bi/nhãn ô và quà nấm (chụp)", priority = 121)]
        static void Run()
        {
            if (EditorApplication.isPlaying)
            {
                if (App.I != null) App.I.StartCoroutine(Tour());
                return;
            }
            File.WriteAllText(Flag, "menu");
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
                File.Delete(Flag);
                SessionState.SetBool("MachineSlotLabelTour", true);
                tourStart = EditorApplication.timeSinceStartup;
                EditorApplication.isPlaying = true;
                return;
            }
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 150)
            {
                Debug.LogWarning("[Nhãn ô] Tour quá 150 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool("MachineSlotLabelTour", false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null)
            {
                SessionState.SetBool("MachineSlotLabelTour", false);
                Application.runInBackground = true; // Unity nằm nền vẫn chạy vòng game
                stopAfter = true;
                BootTitle.Dismiss();
                App.I.StartCoroutine(Tour());
            }
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(Dir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, name + ".png"), tex.EncodeToPNG());
            Object.Destroy(tex);
            Debug.Log("[Nhãn ô] chụp " + name);
        }

        // phóng lớp máy s lần, đưa điểm (x, y) toạ độ máy về giữa khung canvas
        static IEnumerator Zoom(MachineBoard board, float s, double x, double y, string name)
        {
            var root = board.Root;
            var keepScale = root.localScale;
            var keepPos = root.position;
            var canvas = board.GetComponentInParent<Canvas>().rootCanvas;
            var corners = new Vector3[4];
            ((RectTransform)canvas.transform).GetWorldCorners(corners);
            var center = (corners[0] + corners[2]) / 2;
            root.localScale = keepScale * s;
            yield return null;
            var target = board.World(x, y);
            root.position += new Vector3(center.x - target.x, center.y - target.y, 0);
            yield return null;
            yield return Shot(name);
            root.localScale = keepScale;
            root.position = keepPos;
            yield return null;
        }

        static IEnumerator Tour()
        {
            App.Router.Go(SceneIds.Machine);
            float t0 = Time.realtimeSinceStartup;
            MachineBoard board = null;
            while ((!(board = Object.FindAnyObjectByType<MachineBoard>()) || App.Router.Busy) && Time.realtimeSinceStartup - t0 < 25) yield return null;
            yield return new WaitForSecondsRealtime(2.5f);
            if (!board || board.Board == null)
            {
                Debug.LogWarning("[Nhãn ô] không vào được máy bi");
            }
            else
            {
                yield return Shot("1_ca_man");
                yield return Zoom(board, 3.2f, 89.6, 258, "2_nam_trai");
                yield return Zoom(board, 3.2f, 347, 258, "2_nam_phai");
                yield return Zoom(board, 1.4f, 218, 600, "3_o_day_ca_hang");
                yield return Zoom(board, 2.4f, 218, 620, "3_o_day");
                // số theo cược (chỉ hình): ×2 hiện nhãn "×2" trên ô rương, ×10 thử số 3 chữ số
                board.SetMult(2, false);
                yield return Zoom(board, 2.4f, 218, 620, "4_o_day_x2");
                board.SetMult(10, false);
                yield return Zoom(board, 2.4f, 218, 620, "5_o_day_x10");
                board.SetMult(1, false);
                yield return null;
            }
            Debug.Log("[Nhãn ô] Xong tour: " + Dir);
            if (stopAfter)
            {
                stopAfter = false;
                tourStart = 0;
                EditorApplication.isPlaying = false;
            }
        }
    }
}
