// Soát giao diện toàn bộ (đang Play, 2026-11-23): mọi màn (sảnh, 5 đảo, Tướng, Sổ thẻ, Máy bi, Sổ tay, Đền, Hang, Trang trại, Nhà: thường,
// chọn công trình, tấm xây, lát ô; trận) và mọi hộp thoại mở được bằng dữ liệu thật (AFK, chuẩn bị trận thường / Đền / Hang, chọn đội, chi
// tiết tướng có / chưa có / 3 dạng, tiềm năng, so sánh tiềm năng, chi tiết thẻ, tỉ lệ máy bi, mốc huyền thoại, lên cấp, xác nhận, báo, Cây
// bi, chọn bạn đồng hành, giới thiệu, cách chơi, kết quả thắng / thua, tạm dừng, danh sách trận Đền, thắng Đền, quảng cáo giả, chọn tướng
// trang trại, rương đảo, mở rương). Mỗi ảnh chụp xong chạy UiLint.Scan (Temp/PokiShots/lint/<tên>.txt). Ảnh vào Temp/PokiShots/soat/.
// Menu "PokiClash/Thử/Giao diện/Soát UI: chụp + quét mọi màn, mọi hộp (đang Play)". Không lưu bản lưu (không bấm nút làm đổi dữ liệu).
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using PokiClash.Core;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class UiFullAudit
    {
        static string Dir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "soat");
        static readonly List<string> summary = new List<string>();

        [MenuItem("PokiClash/Thử/Giao diện/Soát UI: chụp + quét mọi màn, mọi hộp (đang Play)", priority = 148)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Soát UI] Bấm Play trước");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static IEnumerator Run()
        {
            BootTitle.Dismiss();
            App.Modals.CloseAll();
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, "*.png")) File.Delete(f);
            if (Directory.Exists(UiLint.Dir))
                foreach (var f in Directory.GetFiles(UiLint.Dir, "*.txt")) File.Delete(f);
            summary.Clear();
            var d = App.Data;
            var s = App.Save.Data;
            string starter = s.starter ?? (d.Starters.Count > 0 ? d.Starters[0] : d.Heroes[0].id);
            string unowned = d.Heroes.FirstOrDefault(h => s.Hero(h.id)?.owned != true)?.id;
            string threeForms = d.Heroes.FirstOrDefault(h => StarTier.Tiers(h) >= 3)?.id;

            // ---------- màn ----------
            yield return Go(SceneIds.Hub);
            yield return Cap("m01_sanh");
            foreach (Elem e in Enum.GetValues(typeof(Elem)))
            {
                yield return Go(SceneIds.Zone, e);
                yield return Cap("m02_dao_" + Keys.Of(e));
            }
            yield return Go(SceneIds.Heroes);
            yield return new WaitForSecondsRealtime(1.2f);
            yield return Cap("m03_tuong");
            yield return Go(SceneIds.Cards);
            yield return Cap("m04_so_the");
            yield return Go(SceneIds.Machine);
            yield return Cap("m05_may_bi");
            yield return Go(SceneIds.Notebook);
            yield return Cap("m06_so_tay");
            yield return Go(SceneIds.Badges);
            yield return Cap("m07_den");
            yield return Go(SceneIds.Cave);
            yield return Cap("m08_hang");
            yield return Go(SceneIds.Farm);
            yield return Cap("m09_trang_trai");
            yield return HomeShots();
            yield return Go(SceneIds.Battle, 1);
            yield return new WaitForSecondsRealtime(2.5f);
            yield return Cap("m11_tran");
            yield return new WaitForSecondsRealtime(3f);
            yield return Cap("m11b_tran_chon_the");

            // ---------- hộp thoại ----------
            yield return Go(SceneIds.Hub);
            var rewards = new List<Reward>
            {
                new Reward { k = RewardKind.Balls, n = 120 },
                new Reward { k = RewardKind.Exp, n = 30 },
                new Reward { k = RewardKind.Stones, n = 3 },
            };
            var boxes = new List<(string, Action)>
            {
                ("h01_afk", App.OpenAfk),
                ("h02_chuan_bi", () => { StagePrep.Open(1); }),
                ("h03_chuan_bi_den", () => { StagePrep.OpenBadge(Elem.Thuy, 1, 1); }), // trận đếm từ 1
                ("h04_chuan_bi_hang", () => { StagePrep.OpenCave(Elem.Kim, 0, 0); }),
                ("h05_chon_doi", () => Open<TeamPickerDialog>("ChonDoi").Show(new List<string>(s.team), PokiClash.Core.Progress.TeamSlots(s), d.Hero(d.Stage(1).enemies[0].hero), null)),
                ("h06_chi_tiet_tuong", () => { HeroDetail.Open(starter); }),
                ("h06b_chi_tiet_chua_co", () => { HeroDetail.Open(unowned ?? starter); }),
                ("h06c_chi_tiet_3_dang", () => { HeroDetail.Open(threeForms ?? starter); }),
                ("h07_tiem_nang", () => Open<PotentialDialog>("TiemNang").Show(starter)),
                ("h08_tiem_nang_so_sanh", () => Open<PotentialCompareDialog>("TiemNangSoSanh").Show(starter, null)),
                ("h09_chi_tiet_the", () => Open<CardDetailDialog>("ChiTietThe").Show(d.Pool[0], 1)),
                ("h10_ti_le_may_bi", () => Open<MachineRatesDialog>("TiLeMayBi").Show(d.Cfg)),
                ("h11_huyen_thoai", () => Open<LegendMilestoneDialog>("HuyenThoai").Show(d.Hero(d.LegendMilestoneHero ?? starter), d.Cfg.legendMilestone)),
                ("h12_len_cap", () => { Dialogs.LevelUp(s.level, s.level + 1); }),
                ("h13_xac_nhan", () => { App.Modals.Confirm("Thoát trận?", "Thoát giữa trận sẽ mất lượt đánh này. Bạn chắc chứ?", "Thoát", null); }),
                ("h14_thong_bao", () => { App.Modals.Alert("Hết chỗ", "Đội đã đủ 4 tướng. Bỏ bớt một tướng để thêm tướng mới.", "Đã hiểu", null, false); }),
                ("h15_cay_bi", TreePanel.Open),
                ("h16_khoi_dau", () => { Dialogs.Starter(); }),
                ("h17_gioi_thieu", () => { Dialogs.Intro(); }),
                ("h18_cach_choi", () => Open<HowToDialog>("CachChoi").Show()),
                // kết quả trận: dựng như BattleController.Finish (tiêu đề cỡ 40, một dòng số liệu, ô thưởng / lời khuyên, hàng nút)
                ("h19_ket_qua_thang", () =>
                {
                    var m = Open<BattleResultDialog>("TranKetQua");
                    m.Show(true, Loc.F("{0} · Ải {1} · {2}", d.Zone(Elem.Thuy).name, 12, d.ZoneStages(Elem.Thuy).ElementAt(11).name), 40, Loc.F("{0} hiệp · gây {1} sát thương", 5, 1240));
                    m.Reward().Item(App.Art.Icon("ball"), "×120", Loc.T("Bi")).Tag(Loc.T("Lần đầu"), Theme.Yellow);
                    m.Reward().Hero(d.Hero(starter), "×3").Tag("3/10", Theme.Paper2);
                    m.Button(Loc.F("Máy bi ({0})", s.balls), BtnColor.Orange, 250, null);
                    m.Button(Loc.T("Ải tiếp »"), BtnColor.Green, 210, null);
                    m.Button(Loc.T("Đánh lại"), BtnColor.Paper, 200, null);
                    m.Button(d.Zone(Elem.Thuy).name, BtnColor.Paper, 200, null);
                }),
                ("h20_ket_qua_thua", () =>
                {
                    var m = Open<BattleResultDialog>("TranKetQua");
                    m.Show(false, Loc.F("{0} · Ải {1} · {2}", d.Zone(Elem.Thuy).name, 12, d.ZoneStages(Elem.Thuy).ElementAt(11).name), 40, Loc.F("{0} hiệp · gây {1} sát thương", 7, 860));
                    m.Tips(Loc.T("Thua không mất gì! Mạnh hơn bằng:\n") + Loc.T("• Thả bi ở Máy bi để lên cấp: mọi tướng mạnh lên.\n• Nâng thẻ và tiến hóa ở mục Tướng.\n") +
                           Loc.F("• Chọn tướng khắc hệ địch ({0} bị {1} khắc), hoặc đánh ải dễ hơn ở đảo khác.", "Thủy", "Thổ"));
                    m.Button(Loc.F("Máy bi ({0})", s.balls), BtnColor.Orange, 250, null);
                    m.Button(Loc.T("Tướng"), BtnColor.Green, 200, null);
                    m.Button(Loc.T("Đánh lại"), BtnColor.Paper, 200, null);
                    m.Button(d.Zone(Elem.Thuy).name, BtnColor.Paper, 200, null);
                }),
                ("h21_tam_dung", () => Open<BattlePauseDialog>("TranTamDung").Show("Đảo Thủy · Ải 1", null)),
                ("h22_danh_sach_den", () => Open<BadgeListDialog>("DanhSachTranHuyHieu").Show(Elem.Thuy, 1, null)),
                ("h23_thang_den", () => Open<BadgeWinDialog>("TranHuyHieu").Show(Elem.Thuy, 1, "Huy hiệu Thủy!", "Hệ Thủy +5% Máu, Công, Thủ", "Nhận")),
                ("h24_quang_cao", () => Open<FakeAdDialog>("QuangCaoGia").Show(5, null)),
                ("h25_chon_tuong_trai", () => Open<FarmPickerDialog>("ChonTuongTrangTrai").Show(0, null)),
                ("h26_ruong_dao", () => Open<ZoneChestDialog>("RuongDao").Show(new PokiClash.Core.Progress.ZoneChest { zone = Elem.Thuy, n = 0, balls = 120, evoStones = 1 }, s, d)),
                ("h27_mo_ruong", () => { App.I.StartCoroutine(ChestBox.Show("Rương Bạc", SlotKind.ChestSilver, null, rewards, "Nhận")); }),
            };
            foreach (var (name, open) in boxes)
            {
                bool ok;
                try
                {
                    open();
                    ok = true;
                }
                catch (Exception e)
                {
                    summary.Add($"{name}: LỖI MỞ {e.GetType().Name}: {e.Message}");
                    Debug.LogWarning($"[Soát UI] {name}: {e}");
                    App.Modals.CloseAll();
                    ok = false;
                }
                if (!ok) continue;
                yield return new WaitForSecondsRealtime(name == "h27_mo_ruong" ? 2.6f : 0.9f);
                yield return Cap(name);
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.35f);
            }
            File.WriteAllText(Path.Combine(UiLint.Dir, "_tong.txt"), string.Join("\n", summary), System.Text.Encoding.UTF8);
            Debug.Log($"[Soát UI] Xong: ảnh {Path.GetFullPath(Dir)}, báo cáo {Path.GetFullPath(UiLint.Dir)}/_tong.txt");
        }

        // màn Nhà: thường, chọn Nhà chính (vòng nút), tấm xây, lát ô
        static IEnumerator HomeShots()
        {
            yield return Go(SceneIds.Home);
            var home = Object.FindFirstObjectByType<HomeScene>();
            var chrome = home ? typeof(HomeScene).GetField("chrome", BindingFlags.Instance | BindingFlags.NonPublic)?.GetValue(home) as CanvasGroup : null;
            for (float t = 0; t < 10 && (PierShip.Active && PierShip.Active.Busy || chrome && chrome.alpha < 0.99f); t += 0.25f)
                yield return new WaitForSecondsRealtime(0.25f);
            yield return new WaitForSecondsRealtime(1f);
            yield return Cap("m10_nha");
            if (!home) yield break;
            var main = Home.Main(App.Save.Data.home);
            var objs = typeof(HomeScene).GetField("objs", BindingFlags.Instance | BindingFlags.NonPublic)?.GetValue(home) as Dictionary<int, HomeObject>;
            if (main != null && objs != null && objs.TryGetValue(main.id, out var mo))
            {
                var a = mo.Rt.anchoredPosition;
                int n = Home.Def(App.Data.Cfg, main.def).size;
                typeof(HomeScene).GetMethod("OnTap", BindingFlags.Instance | BindingFlags.NonPublic)?.Invoke(home, new object[] { new Vector2(a.x, -a.y - n * 24f) });
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Cap("m10b_nha_chon");
                typeof(HomeScene).GetMethod("HideSel", BindingFlags.Instance | BindingFlags.NonPublic)?.Invoke(home, null);
            }
            foreach (var (field, shot) in new[] { ("hudBuild", "m10c_nha_xay"), ("hudPaint", "m10d_nha_lat") })
            {
                var hb = typeof(HomeScene).GetField(field, BindingFlags.Instance | BindingFlags.NonPublic)?.GetValue(home) as HomeRingButton;
                if (!hb) continue;
                hb.Button.SimulateClick();
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Cap(shot);
                hb.Button.SimulateClick();
                yield return new WaitForSecondsRealtime(0.4f);
            }
        }

        static T Open<T>(string prefab) where T : Dialog
        {
            var p = AssetDatabase.LoadAssetAtPath<T>($"Assets/04 Prefabs/Dialogs/{prefab}.prefab");
            return p ? App.Modals.Open(p) : App.Modals.Open<T>();
        }

        static IEnumerator Go(string scene, object args = null)
        {
            App.Modals.CloseAll();
            App.Router.Go(scene, args);
            float t0 = Time.realtimeSinceStartup;
            yield return null;
            while ((App.Router.Busy || App.Router.Current != scene) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(1f);
        }

        static IEnumerator Cap(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, name + ".png"), tex.EncodeToPNG());
            Object.Destroy(tex);
            var issues = UiLint.Scan(name);
            summary.Add($"{name}: {issues.Count}");
        }
    }
}
