// Âm thanh: các tiếng tổng hợp (SfxSynth) nướng sẵn thành WAV (Assets/03 Art/Baked/Audio), phát qua một nhóm AudioSource.
// Tiếng chạm đinh của máy bi bị giới hạn nhịp (35 ms) và đổi cao độ ngẫu nhiên như bản web.
using System.Collections.Generic;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public sealed class AudioService : MonoBehaviour
    {
        public const int Voices = 10;

        [SerializeField] AudioSource[] sources; // gắn sẵn trên prefab App ("Am thanh")
        readonly Dictionary<string, AudioClip> clips = new Dictionary<string, AudioClip>();
        int next;
        float lastPeg = -1;

        public bool Enabled { get; set; } = true;

        // Dùng khi nướng prefab (Editor).
        public void Setup(AudioSource[] voices) => sources = voices;

        // Gọi sau Theme.Init (App.Awake): nạp tiếng đã nướng.
        public void Init()
        {
            clips.Clear();
            if (BakedArt.Current)
                foreach (var c in BakedArt.Current.sfx)
                    if (c.clip) clips[c.name] = c.clip;
        }

        public void Play(string name, float volume = 1, float pitch = 1)
        {
            if (!Enabled || !clips.TryGetValue(name, out var clip)) return;
            var s = sources[next];
            next = (next + 1) % sources.Length;
            s.pitch = pitch;
            s.volume = volume;
            s.PlayOneShot(clip);
        }

        public void Hit(bool crit) => Play(crit ? "hitCrit" : "hit");

        // speed: tốc độ bi lúc chạm (px/giây của khung web), to dần theo tốc độ, tối đa như bản web; tối đa ~25 tiếng mỗi giây
        public void Peg(float speed)
        {
            float now = Time.unscaledTime;
            if (now - lastPeg < 0.04f) return;
            lastPeg = now;
            float vol = Mathf.Min(1f, speed / 540f);
            Play("peg", vol, (1100f + Random.value * 500f) / 1100f);
        }
    }
}
