// Xem màn mở khoá tướng mới (App/Shop/HeroUnlockView, người dùng 2026-11-23: "tạo thêm menu cho tôi xem đoạn mở khóa tướng"):
// menu "PokiClash/Thử/Màn mở khoá tướng: …" theo bậc hoặc ngẫu nhiên. Chưa Play thì mở Boot.unity, vào Play, tắt màn mở game, chờ màn
// tải xong rồi diễn (như menu xem lại cốt truyện). Chọn ngẫu nhiên một tướng đúng bậc, ưu tiên tướng có rig (bút chì vẽ theo viền của
// rig, bật ra diễn chiêu); không ghi gì vào bản lưu.
using System.Linq;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HeroUnlockMenu
    {
        const string Flag = "HeroUnlockReplay"; // bậc cần xem (-1: ngẫu nhiên), -2: không có lệnh chờ
        const int None = -2;

        [MenuItem("PokiClash/Thử/Cửa hàng/Màn mở khoá tướng: xem (ngẫu nhiên)", priority = 147)]
        static void Any() => Show(-1);

        [MenuItem("PokiClash/Thử/Cửa hàng/Màn mở khoá tướng: Thường", priority = 148)]
        static void Common() => Show((int)Rarity.Common);

        [MenuItem("PokiClash/Thử/Cửa hàng/Màn mở khoá tướng: Khá", priority = 148)]
        static void Uncommon() => Show((int)Rarity.Uncommon);

        [MenuItem("PokiClash/Thử/Cửa hàng/Màn mở khoá tướng: Hiếm", priority = 148)]
        static void Rare() => Show((int)Rarity.Rare);

        [MenuItem("PokiClash/Thử/Cửa hàng/Màn mở khoá tướng: Sử thi", priority = 148)]
        static void Epic() => Show((int)Rarity.Epic);

        [MenuItem("PokiClash/Thử/Cửa hàng/Màn mở khoá tướng: Huyền thoại", priority = 148)]
        static void Legend() => Show((int)Rarity.Legend);

        static void Show(int rarity)
        {
            if (Application.isPlaying)
            {
                if (App.I) App.I.StartCoroutine(PlayWhenReady(rarity));
                return;
            }
            if (!UnityEditor.SceneManagement.EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo()) return;
            const string boot = "Assets/00 Scenes/Boot.unity";
            if (UnityEngine.SceneManagement.SceneManager.GetActiveScene().path != boot)
                UnityEditor.SceneManagement.EditorSceneManager.OpenScene(boot);
            SessionState.SetInt(Flag, rarity);
            EditorApplication.isPlaying = true;
        }

        [InitializeOnLoadMethod]
        static void Hook()
        {
            EditorApplication.update += Poll;
            // thoát Play trước khi kịp diễn thì bỏ lệnh
            EditorApplication.playModeStateChanged += s =>
            {
                if (s == PlayModeStateChange.EnteredEditMode) SessionState.SetInt(Flag, None);
            };
        }

        static void Poll()
        {
            int r = SessionState.GetInt(Flag, None);
            if (r == None) return;
            if (!EditorApplication.isPlaying || App.I == null || App.Router == null || App.Router.CurrentRoot == null) return;
            SessionState.SetInt(Flag, None);
            BootTitle.Dismiss(); // màn mở game chỉ tắt khi chạm
            App.I.StartCoroutine(PlayWhenReady(r));
        }

        static System.Collections.IEnumerator PlayWhenReady(int rarity)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Booting || BootTitle.Current || StoryIntro.Current) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            var hero = Pick(rarity);
            if (hero == null)
            {
                Debug.LogWarning("[Mở khoá tướng] Không có tướng bậc này.");
                yield break;
            }
            // hình tướng ngoài 5 dòng khởi đầu nằm trong gói tải sau: chờ gói / rig sẵn (tối đa 10 giây) để xem đúng rig, không chân dung
            var form = HeroArt.FormOf(hero).aola;
            t0 = Time.realtimeSinceStartup;
            while (!string.IsNullOrEmpty(form) && !Game.AolaActor.Ready(form) && Time.realtimeSinceStartup - t0 < 10) yield return null;
            Debug.Log($"[Mở khoá tướng] Xem: {hero.name} ({Elements.RarityName(hero.rarity)}), rig {(string.IsNullOrEmpty(form) || Game.AolaActor.Ready(form) ? "sẵn" : "chưa về: chân dung")}");
            HeroUnlockView.Play(new[] { hero.id });
        }

        static HeroDef Pick(int rarity)
        {
            var pool = App.Data.Heroes.Where(h => rarity < 0 || (int)h.rarity == rarity).ToList();
            if (pool.Count == 0) return null;
            // ưu tiên tướng có rig (dạng 1 tìm được prefab tướng)
            var rigged = pool.Where(h =>
            {
                var aola = HeroArt.FormOf(h, 1).aola;
                return !string.IsNullOrEmpty(aola) && Game.AolaActor.Find(aola, out _, out _);
            }).ToList();
            var from = rigged.Count > 0 ? rigged : pool;
            return from[Random.Range(0, from.Count)];
        }
    }
}
