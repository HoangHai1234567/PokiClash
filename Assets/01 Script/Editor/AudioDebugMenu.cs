// Menu "PokiClash/Âm thanh/Thử: ..." (2026-11-22): lúc Play ghi trạng thái nhạc ra console (bài theo scene, bài đang dẫn, từng kênh nhạc
// và kênh tiếng lặp) và đi nhanh tới các scene có nhạc riêng để kiểm (máy bi, đảo Hỏa, ải 20 có boss, sảnh).
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class AudioDebugMenu
    {
        [MenuItem("PokiClash/Âm thanh/Thử: báo trạng thái nhạc")]
        public static void Report()
        {
            var a = App.Audio;
            if (!Application.isPlaying || !a)
            {
                Debug.LogWarning("[Nhạc] Cần Play trước");
                return;
            }
            var so = new SerializedObject(a);
            var mus = so.FindProperty("musicSources");
            var sb = new System.Text.StringBuilder();
            sb.Append($"[Nhạc] scene={App.Router.Current} sceneMusic={a.SceneMusic} đang={a.CurrentMusic} booting={ShipVoyage.Booting} bật={a.Enabled}");
            for (int i = 0; i < mus.arraySize; i++)
            {
                var s = mus.GetArrayElementAtIndex(i).objectReferenceValue as AudioSource;
                if (s) sb.Append($" | kênh{i}: {(s.clip ? $"{s.clip.name} t={s.time:0.0}/{s.clip.length:0.0}" : "-")} chơi={s.isPlaying} vol={s.volume:0.00}");
            }
            var loop = so.FindProperty("loopSource").objectReferenceValue as AudioSource;
            if (loop) sb.Append($" | lặp: {(loop.clip ? loop.clip.name : "-")} chơi={loop.isPlaying} vol={loop.volume:0.00}");
            Debug.Log(sb.ToString());
        }

        [MenuItem("PokiClash/Âm thanh/Thử: tới máy bi")]
        static void GoMachine() => Go(SceneIds.Machine, null);

        [MenuItem("PokiClash/Âm thanh/Thử: tới đảo Hỏa")]
        static void GoFire() => Go(SceneIds.Zone, Elem.Hoa);

        [MenuItem("PokiClash/Âm thanh/Thử: tới ải 20 (boss)")]
        static void GoBoss() => Go(SceneIds.Battle, 20);

        [MenuItem("PokiClash/Âm thanh/Thử: tới sảnh")]
        static void GoHub() => Go(SceneIds.Hub, null);

        static void Go(string scene, object args)
        {
            if (!Application.isPlaying || App.Router == null)
            {
                Debug.LogWarning("[Nhạc] Cần Play trước");
                return;
            }
            App.Router.Go(scene, args);
        }
    }
}
