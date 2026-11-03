// Vòng thử popup gọn (đang Play từ Boot): màn Tướng (đội hình 1 ô rồi 3 ô, xoay), chạm chấm ải và bệ ải trên đảo Thủy (ải mở, ải khoá),
// hộp mở rương, rương mốc đảo, kết quả trận với ô thưởng. Ảnh "p_<tên>.png" vào Temp/PokiShots (không xoá ảnh khác). Giữ bản lưu như cũ.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;
using Progress = PokiClash.Core.Progress;

namespace PokiClash.EditorTools
{
    public static class PopupTour
    {
        [MenuItem("PokiClash/Thử/Popup gọn: đội hình, chạm ải, ô thưởng (đang Play)", priority = 114)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Popup] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            var s = App.Save.Data;
            var d = App.Data;
            App.Modals.CloseAll();

            // đội 1 ô: chưa xong đảo nào, đang ở ải 5 đảo Thủy
            foreach (var h in new[] { "tieu_y", "giot_suong", "vo_su", "ky_lan" }) Progress.UnlockHero(s, h);
            // sổ tướng: tướng chưa mở có mảnh thì hiện bóng sẫm, chưa có mảnh thì ẩn
            foreach (var h in d.Heroes.Where(h => !s.Hero(h.id).owned)) s.Hero(h.id).shards = 0;
            s.Hero("huyen_vu").shards = 7;
            s.Hero("mi_nhi").shards = 2;
            for (int i = 0; i < s.zones.Length; i++) s.zones[i] = 0;
            s.zones[(int)Elem.Thuy] = 4;
            s.team = new List<string> { "tieu_y", "giot_suong", "vo_su" };
            App.Save.Save();
            yield return Go(SceneIds.Heroes);
            yield return Shot("tuong_doi_1o");
            int expect = d.Heroes.Count(h => s.Hero(h.id).owned) + 2, tiles = Object.FindObjectsByType<HeroTile>(FindObjectsSortMode.None).Length;
            if (tiles == expect) Debug.Log($"[Popup] Sổ tướng: {tiles} thẻ (đã có + 2 tướng có mảnh), đúng.");
            else Debug.LogError($"[Popup] Sổ tướng: {tiles} thẻ, cần {expect}.");
            var scroll = Object.FindAnyObjectByType<HeroesScene>()?.GetComponentInChildren<UnityEngine.UI.ScrollRect>();
            if (scroll)
            {
                scroll.verticalNormalizedPosition = 0;
                yield return new WaitForSecondsRealtime(0.3f);
                yield return Shot("tuong_luoi_cuoi");
                scroll.verticalNormalizedPosition = 1;
            }

            // đội 3 ô: xong 3 đảo
            s.zones[(int)Elem.Kim] = Islands.Size(Elem.Kim);
            s.zones[(int)Elem.Moc] = Islands.Size(Elem.Moc);
            s.zones[(int)Elem.Hoa] = Islands.Size(Elem.Hoa);
            App.Save.Save();
            yield return Go(SceneIds.Hub);
            yield return Go(SceneIds.Heroes);
            yield return Shot("tuong_doi_3");
            var lineup = Object.FindAnyObjectByType<TeamLineup>();
            var side = lineup ? lineup.GetComponentsInChildren<ClickCatcher>().FirstOrDefault(c => c.name == "o_1") : null;
            side?.OnClick?.Invoke();
            yield return new WaitForSecondsRealtime(0.7f);
            yield return Shot("tuong_doi_xoay");
            // vuốt sang trái 3 khung (con bên phải vào giữa)
            if (lineup)
            {
                var e = new UnityEngine.EventSystems.PointerEventData(UnityEngine.EventSystems.EventSystem.current)
                    { position = new Vector2(Screen.width * 0.7f, Screen.height * 0.75f), delta = new Vector2(-Screen.width * 0.06f, 0) };
                lineup.OnBeginDrag(e);
                for (int i = 0; i < 3; i++)
                {
                    e.position += e.delta;
                    lineup.OnDrag(e);
                    yield return null;
                }
                lineup.OnEndDrag(e);
                yield return new WaitForSecondsRealtime(0.7f);
                yield return Shot("tuong_doi_vuot");
            }

            // đảo Thủy: chạm chấm ải đang đánh, chấm ải khoá, bệ ải tướng
            yield return Go(SceneIds.Zone, Elem.Thuy);
            yield return Shot("dao_thuy");
            foreach (var (pip, tag) in new[] { ("cham_6", "cham_mo"), ("cham_9", "cham_khoa") })
            {
                var c = Object.FindObjectsByType<ZonePip>(FindObjectsSortMode.None).FirstOrDefault(x => x.name == pip);
                if (!c)
                {
                    Debug.LogWarning("[Popup] Không thấy " + pip);
                    continue;
                }
                c.GetComponent<ClickCatcher>().OnClick();
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Shot(tag);
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.3f);
            }
            var hero = d.ZoneStages(Elem.Thuy).First(st => st.tag == StageTag.Hero && st.idx > 1);
            StagePrep.Open(hero.id);
            yield return new WaitForSecondsRealtime(0.8f);
            yield return Shot("be_ai_tuong");
            App.Modals.CloseAll();

            // hộp mở rương: XP, bi, đá, thẻ, mảnh (mở khoá, đổi thẻ)
            var rng = new Rng(7);
            var rewards = new List<Reward>
            {
                new Reward { k = RewardKind.Exp, n = 15 },
                new Reward { k = RewardKind.Balls, n = 3 },
                new Reward { k = RewardKind.Stones, n = 2 },
                new Reward { k = RewardKind.Shards, res = new ShardResult { hero = "ky_lan", n = 4, converted = 1 } },
                new Reward { k = RewardKind.Shards, res = new ShardResult { hero = "huyen_vu", n = 10, unlocked = true } },
            };
            for (int i = 0; i < 3; i++)
            {
                var drop = Progress.RollCardDrop(s, d, (Rarity)(i + 1), rng);
                if (drop != null) rewards.Add(new Reward { k = RewardKind.Card, drop = drop });
            }
            App.I.StartCoroutine(ChestBox.Show("Rương Vàng", SlotKind.ChestGold, null, rewards, "Nhận"));
            yield return new WaitForSecondsRealtime(2.6f);
            yield return Shot("mo_ruong");
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.3f);

            // rương mốc đảo
            var zc = new Progress.ZoneChest { zone = Elem.Thuy, n = 0, balls = 10 };
            for (int i = 0; i < 2; i++)
            {
                var drop = Progress.RollCardDrop(s, d, (Rarity)(i + 2), rng);
                if (drop != null) zc.cards.Add(drop);
            }
            var zcPrefab = AssetDatabase.LoadAssetAtPath<ZoneChestDialog>("Assets/04 Prefabs/Dialogs/RuongDao.prefab");
            App.Modals.Open(zcPrefab).Show(zc, s, d);
            yield return new WaitForSecondsRealtime(0.8f);
            yield return Shot("ruong_dao");
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.3f);

            // kết quả trận: bi lần đầu, mảnh tướng mới mở khoá, mảnh thường
            var resPrefab = AssetDatabase.LoadAssetAtPath<BattleResultDialog>("Assets/04 Prefabs/Dialogs/TranKetQua.prefab");
            var m = App.Modals.Open(resPrefab, mandatory: true);
            m.Show(true, "Đảo Thủy · Ải 5 · Vũng San Hô", 40, "4 hiệp · gây 1320 sát thương");
            m.Reward().Item(App.Art.Icon("ball"), "×12", "Bi").Tag("Lần đầu", Theme.Yellow);
            m.Reward().Hero(d.Hero("ky_lan"), "×3").Tag("7/20", Theme.Paper2);
            m.Reward().Hero(d.Hero("huyen_vu"), "×10").Tag("MỞ KHÓA!", Theme.Red);
            m.Button("Ải tiếp »", BtnColor.Green, 210, null);
            m.Button("Đánh lại", BtnColor.Paper, 200, null);
            yield return new WaitForSecondsRealtime(0.8f);
            yield return Shot("ket_qua");
            App.Modals.CloseAll();

            // trả bản lưu như trước; trước đó chưa có file thì xoá file vòng thử vừa ghi (người chơi mới)
            if (backup != null) File.WriteAllText(path, backup);
            else if (File.Exists(path)) File.Delete(path);
            App.Save.Load();
            App.Bars.Refresh();
            yield return Go(SceneIds.Hub);
            Debug.Log($"[Popup] Xong vòng thử popup: {PlayTour.ShotDir}");
        }

        static IEnumerator Go(string scene, object args = null)
        {
            App.Router.Go(scene, args);
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != scene) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(0.5f);
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(PlayTour.ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"p_{name}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }
    }
}
