// Menu thử (đang Play): đo độ mượt khi chạm ở màn Tướng (người dùng dặn 2026-11-07: tiến hóa, lên cấp, bỏ / thêm tướng vào đội
// phải phản hồi ngay). Đo bằng Stopwatch phần việc chạy trong khung bấm, so với cách cũ (phá đi dựng lại cả lưới tướng và 3 sticker
// đội hình mỗi lần làm mới, đọc animation dạng mới trên luồng chính); đếm camera sticker chụp mỗi khung; chụp màn vào
// Temp/PokiShots/muot_*.jpg. Kết quả in Console dòng "[Mượt]". Xong trả lại bản lưu như trước.
// Số đo ở Editor nhanh hơn điện thoại tầm 3–5 lần: so tương đối cũ / mới, mốc là dưới 16 ms (một khung 60 hình/giây).
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;
using Debug = UnityEngine.Debug;
using Progress = PokiClash.Core.Progress;

namespace PokiClash.EditorTools
{
    public static class ResponsivenessTour
    {
        const BindingFlags Any = BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic;
        static string Dir => Path.Combine(PlayTour.ShotDir, "muot");
        static readonly List<string> lines = new List<string>();

        [MenuItem("PokiClash/Thử/Đo độ mượt màn Tướng: tiến hóa, lên cấp, đổi đội (đang Play)", priority = 117)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Mượt] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        static object F(object o, string name) => (o is System.Type t ? t : o.GetType()).GetField(name, Any)?.GetValue(o is System.Type ? null : o);

        static void Log(string s)
        {
            lines.Add(s);
            Debug.Log("[Mượt] " + s);
        }

        static double Ms(System.Action a)
        {
            var sw = Stopwatch.StartNew();
            a();
            return sw.Elapsed.TotalMilliseconds;
        }

        static IEnumerator Run()
        {
            lines.Clear();
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            try
            {
                // bản lưu thử: mọi tướng có hình aola đã nhận (lưới dài như người chơi lâu), đội 3 con, mở đủ 3 ô
                var d = App.Data;
                var s = App.Save.Data;
                var withArt = d.Heroes.Where(h => AolaActor.Find(HeroArt.FormOf(h, 1).aola, out _, out _)).ToList();
                foreach (var h in withArt)
                {
                    var hp = s.Hero(h.id);
                    if (!hp.owned) Progress.UnlockHero(s, h.id);
                    if (hp.star < 1) hp.star = 1;
                }
                if (s.level < 200) s.level = 200; // mở đủ 3 ô đội
                var team = withArt.Take(3).Select(h => h.id).ToList();
                s.team = new List<string>(team);
                Log($"{withArt.Count} tướng có hình aola, đội {string.Join(", ", team)}, ô đội mở {Progress.TeamSlots(s)}");

                App.Router.Go(SceneIds.Heroes);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Heroes) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(1.2f);
                var scene = Object.FindAnyObjectByType<HeroesScene>();
                var lineup = (TeamLineup)F(scene, "lineup");
                var tiles = (List<HeroTile>)F(scene, "tiles");
                Log($"lưới {tiles.Count} ô");

                // 1. làm mới: mới (dùng lại ô, sticker) và cũ (phá hết rồi dựng lại)
                double warm = 0;
                for (int i = 0; i < 5; i++) warm += Ms(scene.Refresh);
                warm /= 5;
                double cold = 0;
                for (int i = 0; i < 3; i++)
                {
                    foreach (var tile in tiles) Object.Destroy(tile.gameObject);
                    tiles.Clear();
                    var anim = (AolaSticker[])F(lineup, "anim");
                    var keys = (string[])F(lineup, "animKey");
                    for (int k = 0; k < anim.Length; k++)
                    {
                        anim[k]?.Destroy();
                        anim[k] = null;
                        keys[k] = null;
                    }
                    yield return null;
                    cold += Ms(scene.Refresh);
                    yield return null;
                }
                cold /= 3;
                Log($"Làm mới màn Tướng: mới {warm:0.0} ms; dựng lại cả lưới {cold:0.0} ms");

                // 1b. tách phần: ghi bản lưu, dựng một sticker (dạng đã đọc), thông báo, tiếng, mở hộp chi tiết
                {
                    string json = null;
                    double enc = 0, io = 0, mk = 0, toast1, toast2, snd1, snd2, open1, open2;
                    var tmp = App.Save.FilePath + ".do";
                    for (int i = 0; i < 3; i++)
                    {
                        enc += Ms(() => json = SaveCodec.Write(App.Save.Data));
                        io += Ms(() => File.WriteAllText(tmp, json));
                    }
                    File.Delete(tmp);
                    var host = (RectTransform)lineup.transform;
                    var h0 = d.Hero(team[0]);
                    for (int i = 0; i < 3; i++)
                    {
                        AolaSticker st = null;
                        mk += Ms(() => st = AolaSticker.TryCreate(host, h0, HeroArt.FormOf(h0).aola, TeamLineup.HeroH, false));
                        st?.Destroy();
                        yield return null;
                    }
                    toast1 = Ms(() => App.Toasts.Show("đo 1", null));
                    toast2 = Ms(() => App.Toasts.Show("đo 2", null));
                    snd1 = Ms(() => App.Audio.Play("level"));
                    snd2 = Ms(() => App.Audio.Play("level"));
                    open1 = Ms(() => HeroDetail.Open(team[1], null));
                    yield return new WaitForSecondsRealtime(0.5f);
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.5f);
                    open2 = Ms(() => HeroDetail.Open(team[1], null));
                    yield return new WaitForSecondsRealtime(0.5f);
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.5f);
                    Log($"Tách phần: mã hoá bản lưu {enc / 3:0.0} ms ({json.Length / 1024} KB), ghi file {io / 3:0.0} ms, dựng sticker {mk / 3:0.0} ms, " +
                        $"thông báo {toast1:0.0}/{toast2:0.0} ms, tiếng {snd1:0.0}/{snd2:0.0} ms, mở hộp chi tiết {open1:0.0}/{open2:0.0} ms (lần đầu/lần sau)");
                    double oldOne = cold + mk; // cũ: dựng lại lưới + 3 sticker đội hình mỗi lần làm mới
                    Log($"Làm mới màn Tướng kiểu cũ ≈ {oldOne:0} ms một lần, mỗi lần bấm 2–3 lần: {oldOne * 2:0}–{oldOne * 3:0} ms; kiểu mới {warm:0.0} ms");
                }

                // 2. đọc animation dạng chưa đọc: trên luồng chính (cũ) và đọc trước ở luồng phụ (mới)
                var cache = (IDictionary)F(typeof(AolaActor), "Cache");
                var parse = typeof(AolaActor).GetMethod("Parse", Any);
                var fresh = d.Heroes.SelectMany(h => h.forms).Select(f => f.aola).Distinct()
                    .Select(f => (f, a: AolaActor.Find(f, out var pf, out int fi) ? pf.Forms[fi] : null))
                    .Where(x => x.a && x.a.anim && !cache.Contains(x.a))
                    .OrderByDescending(x => x.a.anim.bytes.Length).Take(2).ToList();
                if (fresh.Count == 2)
                {
                    double sync = Ms(() => parse.Invoke(null, new object[] { fresh[0].a }));
                    AolaActor.Prewarm(fresh[1].f);
                    t0 = Time.realtimeSinceStartup;
                    while (!AolaActor.Ready(fresh[1].f) && Time.realtimeSinceStartup - t0 < 10) yield return null;
                    float wait = Time.realtimeSinceStartup - t0;
                    double after = Ms(() => parse.Invoke(null, new object[] { fresh[1].a }));
                    Log($"Đọc animation dạng mới ({fresh[0].a.anim.bytes.Length / 1024} KB gzip): luồng chính {sync:0.0} ms; " +
                        $"đọc trước ở luồng phụ xong sau {wait * 1000:0} ms, lúc dùng còn {after:0.0} ms");
                }

                // 3. bấm thật trong hộp chi tiết (con đầu đội): bỏ khỏi đội, cho vào lại, tiến hóa (nút hack), mỗi lần đo phần việc
                // trong khung bấm và khung dài nhất 5 khung sau
                string id = team[0];
                var cam = CountCams();
                HeroDetail.Open(id, null);
                yield return new WaitForSecondsRealtime(1f);
                var dlg = Object.FindAnyObjectByType<HeroDetailDialog>();
                object parts = F(dlg, "p");
                var teamBtn = (UI.SketchButton)F(parts, "team");
                var hack = (UI.SketchButton)F(parts, "hackStar");
                yield return Tap("Bỏ khỏi đội", teamBtn);
                yield return Shot("1_bo_khoi_doi");
                yield return Tap("Cho vào đội", teamBtn);
                yield return Tap("Bỏ khỏi đội (lần 2)", teamBtn);
                yield return Tap("Cho vào đội (lần 2)", teamBtn);
                // lên cấp thẻ: cho đủ bản sao thẻ đầu rồi bấm nút "Lên cấp"
                var hpId = s.Hero(id);
                var slot0 = Progress.Slots[0];
                hpId.Card(slot0).copies += 50;
                hpId.Card(Progress.Slots[1]).copies += 50;
                App.Modals.CloseAll(); // mở lại hộp để vẽ nút lên cấp
                yield return new WaitForSecondsRealtime(0.5f);
                HeroDetail.Open(id, null);
                yield return new WaitForSecondsRealtime(0.8f);
                dlg = Object.FindAnyObjectByType<HeroDetailDialog>();
                parts = F(dlg, "p");
                teamBtn = (UI.SketchButton)F(parts, "team");
                hack = (UI.SketchButton)F(parts, "hackStar");
                var cards = (System.Array)F(parts, "cards");
                for (int round = 0; round < 2; round++)
                {
                    UI.SketchButton up = null;
                    foreach (var c in cards)
                    {
                        var b = (UI.SketchButton)F(c, "up");
                        if (b && b.gameObject.activeInHierarchy)
                        {
                            up = b;
                            break;
                        }
                    }
                    yield return Tap($"Lên cấp thẻ (lần {round + 1})", up);
                }
                yield return Tap("Tiến hóa (hack sao)", hack);
                yield return new WaitForSecondsRealtime(0.3f);
                yield return Shot("2_tien_hoa_a");
                yield return new WaitForSecondsRealtime(0.25f);
                yield return Shot("2_tien_hoa_b");
                yield return Tap("Tiến hóa lần nữa", hack);
                yield return new WaitForSecondsRealtime(0.4f);
                yield return Shot("3_tien_hoa_2");
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.5f);

                // 4. mở hộp chi tiết tướng chưa đọc animation: hộp hiện ngay với chân dung, tướng động thay vào khi đọc xong
                var cold2 = withArt.Select(h => h.id).FirstOrDefault(h =>
                {
                    var a = AolaActor.Find(HeroArt.FormOf(d.Hero(h)).aola, out var pf, out int fi) ? pf.Forms[fi] : null;
                    return a && !cache.Contains(a);
                });
                if (cold2 != null)
                {
                    double open = Ms(() => HeroDetail.Open(cold2, null));
                    var viewer = Object.FindAnyObjectByType<HeroViewer>();
                    t0 = Time.realtimeSinceStartup;
                    yield return Shot("4_mo_hop_lan_dau");
                    while (F(viewer, "waitHero") != null && Time.realtimeSinceStartup - t0 < 10) yield return null;
                    Log($"Mở hộp tướng chưa đọc animation ({cold2}): {open:0.0} ms trong khung chạm, tướng động sau {(Time.realtimeSinceStartup - t0) * 1000:0} ms");
                    yield return new WaitForSecondsRealtime(0.3f);
                    yield return Shot("5_mo_hop_dong");
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.4f);
                }

                // 5. camera sticker: tỉ lệ khung có chụp (trước đây mọi camera chụp mỗi khung)
                int frames = 0, shots = 0, total = 0;
                t0 = Time.realtimeSinceStartup;
                while (Time.realtimeSinceStartup - t0 < 1.5f)
                {
                    var (on, all) = CountCams();
                    shots += on;
                    total += all;
                    frames++;
                    yield return null;
                }
                Log($"Camera sticker ở màn Tướng: {shots}/{total} lượt chụp trong {frames} khung ({100f * shots / Mathf.Max(1, total):0}% so với chụp mọi khung)");
                yield return Shot("6_man_tuong");

                // 6. đổi đội qua hộp Chọn đội: bỏ hết, chọn 3 con khác (đọc trước animation khi chọn), bấm Xong
                ((UI.SketchButton)F(F(lineup, "p"), "edit")).SimulateClick();
                yield return new WaitForSecondsRealtime(0.8f);
                var picker = Object.FindAnyObjectByType<TeamPickerDialog>();
                if (picker)
                {
                    var pickCells = picker.GetComponentsInChildren<PrepRosterCell>();
                    foreach (var c in pickCells.Take(3)) c.GetComponent<ClickCatcher>().OnClick?.Invoke(); // bỏ 3 con đang trong đội
                    yield return null;
                    foreach (var c in pickCells.Skip(10).Take(3))
                    {
                        c.GetComponent<ClickCatcher>().OnClick?.Invoke();
                        yield return new WaitForSecondsRealtime(0.25f);
                    }
                    yield return new WaitForSecondsRealtime(0.3f);
                    yield return Tap("Đổi đội: bấm Xong", (UI.SketchButton)F(picker, "done"));
                    yield return new WaitForSecondsRealtime(0.4f);
                    yield return Shot("7_doi_doi");
                }

                // 7. màn Đảo: làm mới vì lưu (nhận rương, đổi ải AFK) khi tiến độ không đổi, so với dựng lại cả bản đồ như cũ
                App.Router.Go(SceneIds.Zone, Elem.Tho);
                t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.Zone) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(1f);
                var zs = Object.FindAnyObjectByType<ZoneScene>();
                var built = zs.GetType().GetField("builtProg", Any);
                double zWarm = 0, zCold = 0;
                for (int i = 0; i < 3; i++)
                {
                    zWarm += Ms(zs.Refresh);
                    yield return null;
                    built.SetValue(zs, -1);
                    zCold += Ms(zs.Refresh);
                    yield return null;
                }
                Log($"Làm mới màn Đảo (tiến độ không đổi): mới {zWarm / 3:0.0} ms, cũ {zCold / 3:0.0} ms (nhận rương cũ làm mới 2 lần)");
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
                File.WriteAllText(Path.Combine(Dir, "ket_qua.txt"), string.Join("\n", lines));
            }
            App.Router.Go(SceneIds.Hub);
            Debug.Log("[Mượt] Xong, ảnh và kết quả ở " + Dir);
        }

        // camera của sticker aola (đặt ở x ≥ 10000): đang bật / tổng
        static (int on, int all) CountCams()
        {
            int on = 0, all = 0;
            foreach (var c in Object.FindObjectsByType<Camera>(FindObjectsInactive.Include, FindObjectsSortMode.None))
            {
                if (!c.targetTexture || c.transform.position.x < 9000) continue;
                all++;
                if (c.enabled) on++;
            }
            return (on, all);
        }

        static IEnumerator Tap(string what, UI.SketchButton b)
        {
            if (!b || !b.gameObject.activeInHierarchy)
            {
                Log($"{what}: không thấy nút");
                yield break;
            }
            yield return null;
            double ms = Ms(b.SimulateClick);
            float worst = 0;
            for (int i = 0; i < 5; i++)
            {
                yield return null;
                worst = Mathf.Max(worst, Time.unscaledDeltaTime * 1000);
            }
            Log($"{what}: {ms:0.0} ms trong khung bấm, khung dài nhất sau đó {worst:0} ms");
            yield return new WaitForSecondsRealtime(0.4f);
        }

        // chụp nhỏ bằng cách tự render camera (Editor không có tiêu điểm thì Game view không vẽ); camera sticker đang tắt giữ ảnh cũ
        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            int w = Screen.width / 2, h = Screen.height / 2;
            var cams = Camera.allCameras;
            System.Array.Sort(cams, (x, y) => x.depth.CompareTo(y.depth));
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
            File.WriteAllBytes(Path.Combine(Dir, name + ".jpg"), tex.EncodeToJPG(85));
            Object.DestroyImmediate(tex);
        }
    }
}
