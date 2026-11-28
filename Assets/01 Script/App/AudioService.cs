// Âm thanh: tiếng ngắn (BakedArt.sfx: tiếng tổng hợp nướng sẵn ở Assets/03 Art/Baked/Audio, tiếng chọn 2026-11-22 ở Assets/03 Art/Audio/Sfx)
// phát qua một nhóm AudioSource; nhạc nền (BakedArt.music, Assets/03 Art/Audio/Music) phát qua hai AudioSource nối mờ; một AudioSource
// riêng cho tiếng lặp (bi lăn của máy bi). Nhạc và tiếng chọn nạp bằng menu "PokiClash/Âm thanh/Nạp nhạc và tiếng".
// Tiếng chạm đinh của máy bi là tiếng lặp nhiều nhất nên bị hãm: cách nhau ít nhất 0,1 giây, ba biến thể cao độ không lặp
// liền nhau, cao độ ±5% và độ to ±7% ngẫu nhiên quanh biến thể, nhỏ hơn các tiếng thưởng.
// Nhạc: mỗi scene một bài (MusicFor, App gán SceneMusic khi vào scene; sảnh đổi bài theo mùa, Season.HubMusic); màn tải tàu lúc mở game
// phát chủ đề chính. Đổi bài thì nối
// mờ; bài gen không lặp liền nên gần hết bài thì nối mờ về đầu bài trên kênh kia. Tắt "Âm thanh" (Sổ tay) thì nhạc và tiếng lặp
// nhỏ dần rồi dừng.
using System.Collections.Generic;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public sealed class AudioService : MonoBehaviour
    {
        public const int Voices = 10;
        public const float MusicVolume = 0.5f, MusicFade = 1.2f, LoopFade = 2.5f, LoopVolumeSpeed = 2f;

        [SerializeField] AudioSource[] sources; // gắn sẵn trên prefab App ("Am thanh")
        [SerializeField] AudioSource[] musicSources; // 2 kênh nhạc nối mờ ("Am thanh/Nhac")
        [SerializeField] AudioSource loopSource; // tiếng lặp ("Am thanh/Tieng lap")
        readonly Dictionary<string, AudioClip> clips = new Dictionary<string, AudioClip>();
        readonly Dictionary<string, AudioClip> music = new Dictionary<string, AudioClip>();
        readonly Dictionary<string, float> lastPlay = new Dictionary<string, float>();
        int next;
        float lastPeg = -1;
        int lastPegVariant = -1;
        string curKey; // bài đang dẫn (null = im)
        int cur; // musicSources[cur] là kênh dẫn
        float curStart; // lúc kênh dẫn bắt đầu (unscaled)
        float loopTarget;

        public const float PegGap = 0.1f, PegMaxVolume = 0.6f;
        static readonly float[] PegPitch = { 0.92f, 1f, 1.1f };

        public bool Enabled { get; set; } = true;

        // khoá bài của scene đang mở (MusicFor); null = im
        public string SceneMusic { get; set; }

        public string CurrentMusic => curKey;

        // Dùng khi nướng prefab (Editor).
        public void Setup(AudioSource[] voices) => sources = voices;

        public void SetupMusic(AudioSource[] musicVoices, AudioSource loop)
        {
            musicSources = musicVoices;
            loopSource = loop;
        }

        // Gọi sau Theme.Init (App.Awake): nạp tiếng và nhạc đã nướng.
        public void Init()
        {
            clips.Clear();
            music.Clear();
            if (!BakedArt.Current) return;
            foreach (var c in BakedArt.Current.sfx)
                if (c.clip) clips[c.name] = c.clip;
            foreach (var c in BakedArt.Current.music)
                if (c.clip) music[c.name] = c.clip;
        }

#if UNITY_EDITOR
        // nhật ký tiếng (chỉ Editor, 2026-11-28): menu "PokiClash/Âm thanh/Thử: in tiếng vừa phát" (AudioDebugMenu) để soát tiếng chiêu khi
        // không nghe được: giờ thật, tên, độ to; "(THIẾU)" = tên chưa nạp vào BakedArt
        public static readonly List<string> DebugLog = new List<string>();
#endif

        public void Play(string name, float volume = 1, float pitch = 1)
        {
#if UNITY_EDITOR
            DebugLog.Add($"{Time.unscaledTime:0.00} {name} {volume:0.00}{(clips.ContainsKey(name) ? "" : " (THIẾU)")}");
            if (DebugLog.Count > 400) DebugLog.RemoveAt(0);
#endif
            // tiếng lỗi luôn đi kèm rung lỗi (mọi chỗ báo "không được"), kể cả khi tắt âm thanh; tắt rung riêng ở Sổ tay
            if (name == "error" || name == "machineDeny") Haptics.Play(Haptic.UiError);
            if (!Enabled || !clips.TryGetValue(name, out var clip)) return;
            var s = sources[next];
            next = (next + 1) % sources.Length;
            s.pitch = pitch;
            s.volume = volume;
            s.PlayOneShot(clip);
        }

        // như Play nhưng cùng tên cách nhau ít nhất gap giây (tiếng dài bị gọi dồn, vd. phóng bi khi giữ nút thả). Trả false nếu bị hãm.
        public bool PlayGap(string name, float gap, float volume = 1, float pitch = 1)
        {
            float now = Time.unscaledTime;
            if (lastPlay.TryGetValue(name, out var t) && now - t < gap) return false;
            lastPlay[name] = now;
            Play(name, volume, pitch);
            return true;
        }

        // tiếng lặp nền, một kênh: gọi mỗi khung với độ to mong muốn; 0 thì nhỏ dần rồi dừng
        public void Loop(string name, float volume)
        {
            if (!loopSource) return;
            loopTarget = Enabled ? volume : 0;
            if (loopTarget <= 0 || !clips.TryGetValue(name, out var clip)) return;
            if (loopSource.clip == clip && loopSource.isPlaying) return;
            loopSource.clip = clip;
            loopSource.loop = true;
            loopSource.volume = 0;
            loopSource.Play();
        }

        // tiếng trúng: cao độ ±4% ngẫu nhiên cho đỡ nhàm (GameFeel mục 8.4); power 0..1 (độ mạnh cú, StageView.Power) hạ cao độ cho
        // nặng hơn, cú lớn ở trận khó lót thêm tiếng "stamp" trầm
        public void Hit(bool crit, float power = 0)
        {
            Play(crit ? "hitCrit" : "hit", 1, (1 - 0.12f * power) * Random.Range(0.96f, 1.04f));
            if (crit && power >= 0.4f) Play("stamp", 0.35f + 0.4f * power, 0.9f);
        }

        // speed: tốc độ bi lúc chạm (đơn vị máy/giây), to dần theo tốc độ tới PegMaxVolume; tối đa 10 tiếng mỗi giây.
        // Trả về false nếu bị hãm (để rung chạm đinh đi cùng nhịp với tiếng).
        // combo: lần chạm thứ mấy của chính bi đó: cao dần 2,5 % mỗi lần, tối đa 30 % (bi càng nảy nhiều càng réo rắt, GD_Claude/23)
        public bool Peg(float speed, int combo = 0)
        {
            float now = Time.unscaledTime;
            if (lastPeg >= 0 && now - lastPeg < PegGap) return false;
            lastPeg = now;
            int v = lastPegVariant < 0 ? Random.Range(0, PegPitch.Length) : Random.Range(0, PegPitch.Length - 1);
            if (lastPegVariant >= 0 && v >= lastPegVariant) v++;
            lastPegVariant = v;
            float vol = Mathf.Min(1f, speed / 540f) * PegMaxVolume * (1 + (Random.value - 0.5f) * 0.14f);
            float rise = 1 + Mathf.Min(0.3f, Mathf.Max(0, combo - 1) * 0.025f);
            Play("peg", vol, PegPitch[v] * rise * (1 + (Random.value - 0.5f) * 0.1f));
            return true;
        }

        // Bài của scene: scene tự chọn (SceneRoot.Music) trước, không thì theo bảng. Màn phụ (Sổ tay, Tướng, Thẻ, Đền, Hang...) giữ bài
        // đang phát, trừ khi đó là nhạc trận, máy bi hay chủ đề thì về nhạc sảnh.
        public static string MusicFor(string scene, SceneRoot root, string playing)
        {
            var own = root ? root.Music : null;
            if (own != null) return own;
            switch (scene)
            {
                case SceneIds.Hub:
                    return Season.HubMusic; // theo mùa (Noel: "sanh_noel", người dùng 2026-11-27)
                case SceneIds.Home:
                case SceneIds.Farm:
                    return "sanh";
                case SceneIds.Machine:
                    return "maybi";
                case SceneIds.Battle:
                    return "tran";
            }
            return playing == null || playing == "tran" || playing == "boss" || playing == "maybi" || playing == "chude" ? Season.HubMusic : playing;
        }

        void Update()
        {
            float dt = Time.unscaledDeltaTime;
            UpdateLoop(dt);
            UpdateMusic(dt);
        }

        void UpdateLoop(float dt)
        {
            if (!loopSource || !loopSource.isPlaying) return;
            float target = Enabled ? loopTarget : 0;
            loopSource.volume = Mathf.MoveTowards(loopSource.volume, target, dt * LoopVolumeSpeed);
            if (target <= 0 && loopSource.volume <= 0) loopSource.Stop();
        }

        void UpdateMusic(float dt)
        {
            if (musicSources == null || musicSources.Length < 2) return;
            // màn tải: nhạc chủ đề, trong mùa là bài sảnh của mùa (Season.LoadMusic); cốt truyện: nhạc chủ đề
            string want = Enabled ? (ShipVoyage.Booting ? Season.LoadMusic : StoryIntro.Current ? "chude" : SceneMusic) : null;
            // bài chưa nạp: bài theo mùa lùi về bài gốc ("sanh_noel" → "sanh"), không thì giữ bài cũ
            if (want != null && !music.ContainsKey(want)) want = music.ContainsKey(Season.BaseMusic(want)) ? Season.BaseMusic(want) : curKey;
            if (want != curKey)
            {
                curKey = want;
                if (want != null) StartTrack(music[want]);
            }
            else if (curKey != null)
            {
                var a = musicSources[cur];
                float played = Time.unscaledTime - curStart;
                if (a.clip && played > 1f && (!a.isPlaying || a.clip.length - a.time < LoopFade)) StartTrack(a.clip);
            }
            float step = dt / MusicFade * MusicVolume;
            for (int i = 0; i < musicSources.Length; i++)
            {
                var s = musicSources[i];
                if (!s || !s.isPlaying) continue;
                float target = i == cur && curKey != null ? MusicVolume : 0;
                s.volume = Mathf.MoveTowards(s.volume, target, step);
                if (target <= 0 && s.volume <= 0)
                {
                    s.Stop();
                    s.clip = null;
                }
            }
        }

        // bài mới (hoặc vòng mới của bài cũ) lên ở kênh kia, kênh cũ nhỏ dần
        void StartTrack(AudioClip clip)
        {
            cur = 1 - cur;
            var s = musicSources[cur];
            s.Stop();
            s.clip = clip;
            s.loop = false;
            s.time = 0;
            s.volume = 0;
            s.Play();
            curStart = Time.unscaledTime;
        }
    }
}
