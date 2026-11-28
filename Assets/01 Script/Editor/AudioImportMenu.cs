// Menu "PokiClash/Âm thanh/Nạp nhạc và tiếng" (2026-11-22). Nhạc nền (Google Lyria qua Magnific) ở Assets/03 Art/Audio/Music, tiếng chọn
// (máy bi: ElevenLabs qua Magnific; UI: Kenney, CC0) ở Assets/03 Art/Audio/Sfx; bản gốc và trang chọn ở ArtGen/Music, ArtGen/Sfx.
// Menu: đặt cách nhập (nhạc: mono, Vorbis 40 %, đọc dần; tiếng: mono, Vorbis 70 %, giải nén lúc nạp), ghi vào BakedArt (sfx thay hoặc
// thêm theo tên, music theo khoá), thêm 2 kênh nhạc + 1 kênh tiếng lặp cho AudioService trên prefab App. Chạy lại được (ghi đè cùng tên,
// kênh đã có thì giữ).
using System.Collections.Generic;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class AudioImportMenu
    {
        const string Root = "Assets/03 Art/Audio";
        const string BakedPath = "Assets/03 Art/Baked/BakedArt.asset";
        const string AppPrefab = "Assets/04 Prefabs/App/App.prefab";

        // tên tiếng trong game → file trong Assets/03 Art/Audio/Sfx (tên cũ click, pick, buff, error, card, peg đổi sang tiếng mới)
        static readonly (string name, string file)[] Sfx =
        {
            ("click", "ui_click.ogg"), ("pick", "ui_pick.ogg"), ("buff", "ui_buff.ogg"), ("error", "ui_error.ogg"),
            ("card", "ui_card.ogg"), ("open", "ui_open.ogg"), ("close", "ui_close.ogg"), ("toggle", "ui_toggle.ogg"),
            ("drop", "ui_drop.ogg"),
            ("peg", "maybi_dinh.mp3"), ("launch", "maybi_phong_bi.mp3"), ("xp", "maybi_xp.mp3"), ("balls", "maybi_them_bi.mp3"),
            ("giftPeg", "maybi_dinh_qua.mp3"), ("prize", "maybi_trung_ruong.mp3"), ("jackpot", "maybi_jackpot.mp3"),
            ("bet", "maybi_doi_cuoc.mp3"), ("counter", "maybi_dem_so.mp3"), ("machineLevel", "maybi_len_cap.mp3"),
            ("machineDeny", "maybi_bi_chan.mp3"), ("chestOpen", "maybi_mo_ruong.mp3"), ("roll", "maybi_bi_lan_loop.mp3"),
            // tiếng đánh nhau (2026-11-24, ArtGen/Sfx/xuat_tieng_tran.py; dùng ở AudioService.Hit, BattlePlayer "ult", SkillSfx.cs): "hit",
            // "hitCrit", "ult" thay tiếng tổng hợp cũ cùng tên
            ("hit", "tran_hit.ogg"), ("hitCrit", "tran_hitCrit.ogg"), ("ult", "tran_ult.ogg"),
            ("fx_tu", "tran_fx_tu.ogg"), ("fx_nha_tia", "tran_fx_nha_tia.ogg"), ("fx_no", "tran_fx_no.ogg"), ("fx_no_nho", "tran_fx_no_nho.ogg"),
            ("fx_no_lon", "tran_fx_no_lon.ogg"), ("fx_chem", "tran_fx_chem.ogg"), ("fx_chem2", "tran_fx_chem2.ogg"), ("fx_kim", "tran_fx_kim.ogg"),
            ("fx_huc", "tran_fx_huc.ogg"), ("fx_lua_bay", "tran_fx_lua_bay.ogg"), ("fx_phun_lua", "tran_fx_phun_lua.ogg"),
            ("fx_nuoc", "tran_fx_nuoc.ogg"), ("fx_nuoc_lon", "tran_fx_nuoc_lon.ogg"), ("fx_bong", "tran_fx_bong.ogg"),
            ("fx_tia_nuoc", "tran_fx_tia_nuoc.ogg"), ("fx_song", "tran_fx_song.ogg"), ("fx_loc", "tran_fx_loc.ogg"), ("fx_gam", "tran_fx_gam.ogg"),
            ("fx_da", "tran_fx_da.ogg"), ("fx_phep", "tran_fx_phep.ogg"),
            // tiếng chiêu riêng từng tướng (2026-11-28, ArtGen/Sfx/xuat_tieng_chieu.py; bảng ở SkillSfx.cs): sét, mưa, động đất, đá, thiên thạch,
            // tia Mặt Trời giáng, nổ nấm, cưa máy, máy nổ, tên lửa, pháo, xích, hồn, đớp, pha lê, lá, roi, điện, dung nham, sóng xung kích, gió,
            // tan biến, gầm thú, hét, bùn, nuốt, búa
            ("fx_set", "tran_fx_set.ogg"), ("fx_mua", "tran_fx_mua.ogg"), ("fx_dong_dat", "tran_fx_dong_dat.ogg"),
            ("fx_da_vo", "tran_fx_da_vo.ogg"), ("fx_da_lon", "tran_fx_da_lon.ogg"), ("fx_thien_thach_roi", "tran_fx_thien_thach_roi.ogg"),
            ("fx_thien_thach", "tran_fx_thien_thach.ogg"), ("fx_tia_troi", "tran_fx_tia_troi.ogg"), ("fx_no_nam", "tran_fx_no_nam.ogg"),
            ("fx_cua", "tran_fx_cua.ogg"), ("fx_may_no", "tran_fx_may_no.ogg"), ("fx_ten_lua", "tran_fx_ten_lua.ogg"),
            ("fx_phao", "tran_fx_phao.ogg"), ("fx_xich", "tran_fx_xich.ogg"), ("fx_hon", "tran_fx_hon.ogg"), ("fx_dop", "tran_fx_dop.ogg"),
            ("fx_pha_le", "tran_fx_pha_le.ogg"), ("fx_la", "tran_fx_la.ogg"), ("fx_roi", "tran_fx_roi.ogg"), ("fx_dien", "tran_fx_dien.ogg"),
            ("fx_nham", "tran_fx_nham.ogg"), ("fx_song_am", "tran_fx_song_am.ogg"), ("fx_gio", "tran_fx_gio.ogg"),
            ("fx_bien_mat", "tran_fx_bien_mat.ogg"), ("fx_gam_thu", "tran_fx_gam_thu.ogg"), ("fx_het", "tran_fx_het.ogg"),
            ("fx_bun", "tran_fx_bun.ogg"), ("fx_nuot", "tran_fx_nuot.ogg"), ("fx_bua", "tran_fx_bua.ogg"),
            // bút chì sột soạt lặp liền 4 s (gen Magnific, ArtGen/Sfx/but_chi): màn mở khoá tướng, App.Audio.Loop("pencil", …) ở HeroUnlockView
            ("pencil", "ui_but_chi.ogg"),
            // khán giả Hầm đấu (gen Magnific, ArtGen/Sfx/ham_dau): hai tiếng reo xen kẽ, ồn ào nền lặp liền 8 s (App.Audio.Loop ở UndergroundScene)
            ("pitCheer1", "ham_reo_1.mp3"), ("pitCheer2", "ham_reo_2.mp3"), ("pitCrowd", "ham_on_loop.mp3"),
            // đảo Casino (gen Magnific 2026-11-27, ArtGen/Sfx/casino/dua_vao_unity.py): bi Vòng Xoay gõ phím / rơi ô, cần gạt và ba tiếng dừng
            // cuộn Máy Quả, húc (2 bản xen kẽ) và vọt lên ở Trường đua, guồng câu, Lão Mực lầm bầm (3 bản) và "boing" giật mình
            ("rlTick", "casino_rl_tick.mp3"), ("rlDrop", "casino_rl_roi.mp3"),
            ("slLever", "casino_sl_can.mp3"), ("slStop1", "casino_sl_dung_1.mp3"), ("slStop2", "casino_sl_dung_2.mp3"),
            ("slStop3", "casino_sl_dung_3.mp3"),
            ("raceBonk1", "casino_dua_huc_1.mp3"), ("raceBonk2", "casino_dua_huc_2.mp3"), ("raceDash", "casino_dua_vot.mp3"),
            ("reelCrank", "casino_cau_guong.mp3"),
            ("mucTalk1", "casino_muc_noi_1.mp3"), ("mucTalk2", "casino_muc_noi_2.mp3"), ("mucTalk3", "casino_muc_noi_3.mp3"),
            ("mucBoing", "casino_muc_boing.mp3"),
            // mùa Noel (gen Magnific 2026-11-27, ArtGen/Sfx/noel): chuông xe tuần lộc lúc ông già Noel bay ngang sảnh (SantaFlyby)
            ("noelBells", "noel_chuong_xe.mp3"),
        };

        // khoá nhạc (AudioService.MusicFor, SceneRoot.Music) → Assets/03 Art/Audio/Music/bgm_<khoá>.mp3
        // "sanh_noel": nhạc sảnh mùa Noel (2026-11-27, Lyria qua Magnific, bản gốc ở ArtGen/Music/noel; Season.HubMusic)
        static readonly string[] Music = { "chude", "sanh", "sanh_noel", "dao_thuy", "dao_hoa", "dao_moc", "dao_kim", "dao_tho", "tran", "boss", "maybi" };

        [MenuItem("PokiClash/Âm thanh/Nạp nhạc và tiếng")]
        public static void Run()
        {
            int missing = 0;
            foreach (var (_, file) in Sfx) missing += SetImport($"{Root}/Sfx/{file}", false) ? 0 : 1;
            foreach (var k in Music) missing += SetImport($"{Root}/Music/bgm_{k}.mp3", true) ? 0 : 1;

            var baked = AssetDatabase.LoadAssetAtPath<BakedArt>(BakedPath);
            if (!baked)
            {
                Debug.LogError("[Âm thanh] Không thấy " + BakedPath);
                return;
            }
            foreach (var (name, file) in Sfx) Put(baked.sfx, name, $"{Root}/Sfx/{file}");
            foreach (var k in Music) Put(baked.music, k, $"{Root}/Music/bgm_{k}.mp3");
            EditorUtility.SetDirty(baked);
            AssetDatabase.SaveAssets();

            bool added = AddChannels();
            Debug.Log($"[Âm thanh] Đã nạp {Sfx.Length} tiếng, {Music.Length} bài nhạc vào BakedArt" +
                      (added ? "; thêm kênh nhạc vào prefab App" : "; prefab App đã có kênh nhạc") +
                      (missing > 0 ? $"; THIẾU {missing} file (xem lỗi)" : ""));
        }

        static bool SetImport(string path, bool music)
        {
            var imp = AssetImporter.GetAtPath(path) as AudioImporter;
            if (!imp)
            {
                Debug.LogError("[Âm thanh] Thiếu file " + path);
                return false;
            }
            imp.forceToMono = true;
            imp.loadInBackground = music;
            var s = imp.defaultSampleSettings;
            s.loadType = music ? AudioClipLoadType.Streaming : AudioClipLoadType.DecompressOnLoad;
            s.compressionFormat = AudioCompressionFormat.Vorbis;
            s.quality = music ? 0.4f : 0.7f;
            s.preloadAudioData = !music;
            s.sampleRateSetting = AudioSampleRateSetting.PreserveSampleRate;
            imp.defaultSampleSettings = s;
            imp.ClearSampleSettingOverride("Android");
            imp.ClearSampleSettingOverride("iOS");
            imp.SaveAndReimport();
            return true;
        }

        static void Put(List<BakedArt.ClipItem> list, string name, string path)
        {
            var clip = AssetDatabase.LoadAssetAtPath<AudioClip>(path);
            if (!clip) return; // đã báo ở SetImport
            var item = new BakedArt.ClipItem { name = name, clip = clip };
            int i = list.FindIndex(c => c.name == name);
            if (i >= 0) list[i] = item;
            else list.Add(item);
        }

        // "Am thanh/Nhac" (2 AudioSource) và "Am thanh/Tieng lap" (1 AudioSource), gán vào AudioService
        static bool AddChannels()
        {
            var root = PrefabUtility.LoadPrefabContents(AppPrefab);
            try
            {
                var svc = root.GetComponentInChildren<AudioService>(true);
                if (!svc)
                {
                    Debug.LogError("[Âm thanh] Prefab App không có AudioService");
                    return false;
                }
                var so = new SerializedObject(svc);
                if (so.FindProperty("musicSources").arraySize >= 2 && so.FindProperty("loopSource").objectReferenceValue) return false;

                var musicGo = Child(svc.transform, "Nhac");
                var loopGo = Child(svc.transform, "Tieng lap");
                var a = Source(musicGo, 0);
                var b = Source(musicGo, 0);
                var loop = Source(loopGo, 64);
                svc.SetupMusic(new[] { a, b }, loop);
                EditorUtility.SetDirty(svc);
                PrefabUtility.SaveAsPrefabAsset(root, AppPrefab);
                return true;
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        static GameObject Child(Transform parent, string name)
        {
            var t = parent.Find(name);
            if (t) return t.gameObject;
            var go = new GameObject(name);
            go.transform.SetParent(parent, false);
            return go;
        }

        static AudioSource Source(GameObject go, int priority)
        {
            var s = go.AddComponent<AudioSource>();
            s.playOnAwake = false;
            s.loop = false;
            s.spatialBlend = 0;
            s.priority = priority;
            s.volume = 0;
            return s;
        }
    }
}
