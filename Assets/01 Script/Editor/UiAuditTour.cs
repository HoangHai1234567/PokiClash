// Chụp mọi màn và hộp thoại chính để soi giao diện (đang Play từ Boot): sảnh, AFK, đảo, hộp chuẩn bị, trận, tướng và chi tiết tướng,
// sổ thẻ, máy bi, sổ tay, đền huy hiệu, hang tiềm năng, trang trại, hộp lên cấp. Ảnh ra Temp/PokiShots/ui/<tên>.png, không xoá ảnh
// của vòng thử khác trong Temp/PokiShots.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class UiAuditTour
    {
        static string Dir => Path.Combine(PlayTour.ShotDir, "ui");

        [MenuItem("PokiClash/Thử/Chụp mọi màn để soi giao diện (đang Play)", priority = 121)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Soi giao diện] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Run()
        {
            BootTitle.Dismiss();
            App.Modals.CloseAll();
            Directory.CreateDirectory(Dir);
            var d = App.Data;
            string starter = App.Save.Data.starter ?? (d.Starters.Count > 0 ? d.Starters[0] : null);

            yield return Go(SceneIds.Hub);
            yield return Shot("01_sanh");
            App.OpenAfk();
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("02_afk");
            App.Modals.CloseAll();

            yield return Go(SceneIds.Zone, Elem.Thuy);
            yield return Shot("03_dao_thuy");
            StagePrep.Open(1);
            yield return new WaitForSecondsRealtime(0.7f);
            yield return Shot("04_chuan_bi");
            App.Modals.CloseAll();
            // bể tướng (hộp chọn đội): lọc theo hệ Hỏa, rồi đổi cách xếp
            var picker = App.Modals.Open(AssetDatabase.LoadAssetAtPath<TeamPickerDialog>("Assets/04 Prefabs/Dialogs/ChonDoi.prefab"));
            var stage = d.Stage(1);
            picker.Show(new List<string>(App.Save.Data.team), PokiClash.Core.Progress.TeamSlots(App.Save.Data), stage != null && stage.enemies.Count > 0 ? d.Hero(stage.enemies[0].hero) : null, null);
            yield return new WaitForSecondsRealtime(0.8f);
            yield return Shot("04b_be_tuong");
            Tap(picker, "loc_e_hoa");
            yield return new WaitForSecondsRealtime(0.7f);
            yield return Shot("04c_be_tuong_hoa");
            Tap(picker, "loc_tat_ca");
            Tap(picker, "nut_xep");
            Tap(picker, "nut_xep");
            yield return new WaitForSecondsRealtime(0.7f);
            yield return Shot("04d_be_tuong_xep_he");
            Tap(picker, "nut_xep");
            App.Modals.CloseAll();

            yield return Go(SceneIds.Battle, 1);
            yield return new WaitForSecondsRealtime(2.5f);
            yield return Shot("05_tran");
            yield return new WaitForSecondsRealtime(3f);
            yield return Shot("06_tran_2");

            yield return Go(SceneIds.Heroes);
            yield return Shot("07_tuong");
            if (starter != null)
            {
                HeroDetail.Open(starter);
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Shot("08_tuong_chi_tiet");
                App.Modals.CloseAll();
            }

            yield return Go(SceneIds.Cards);
            yield return Shot("09_so_the");
            yield return Go(SceneIds.Machine);
            yield return Shot("10_may_bi");
            yield return Go(SceneIds.Notebook);
            yield return Shot("11_so_tay");
            yield return Go(SceneIds.Badges);
            yield return Shot("12_den_huy_hieu");
            yield return Go(SceneIds.Cave);
            yield return Shot("13_hang");
            yield return Go(SceneIds.Farm);
            yield return Shot("14_trang_trai");

            yield return Go(SceneIds.Hub);
            Dialogs.LevelUp(App.Save.Data.level, App.Save.Data.level + 1);
            yield return new WaitForSecondsRealtime(0.8f);
            yield return Shot("15_len_cap");
            App.Modals.CloseAll();
            Debug.Log($"[Soi giao diện] Chụp xong: {Dir}");
        }

        // bấm hộ nút có tên trong hộp (như người chơi chạm)
        static void Tap(Component root, string name)
        {
            foreach (var b in root.GetComponentsInChildren<PokiClash.UI.SketchButton>(true))
                if (b.name == name)
                {
                    b.SimulateClick();
                    return;
                }
            Debug.LogWarning("[Soi giao diện] Không thấy nút " + name);
        }

        static IEnumerator Go(string scene, object args = null)
        {
            App.Router.Go(scene, args);
            float t0 = Time.realtimeSinceStartup;
            yield return null;
            while ((App.Router.Busy || App.Router.Current != scene) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(0.8f);
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, name + ".png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }
    }
}
