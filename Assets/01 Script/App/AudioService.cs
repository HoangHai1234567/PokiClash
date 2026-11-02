// Âm thanh: các tiếng tổng hợp (SfxSynth) nướng sẵn thành WAV (Assets/03 Art/Baked/Audio), phát qua một nhóm AudioSource.
// Tiếng chạm đinh của máy bi là tiếng lặp nhiều nhất nên bị hãm: cách nhau ít nhất 0,1 giây, ba biến thể cao độ không lặp
// liền nhau, cao độ ±5% và độ to ±7% ngẫu nhiên quanh biến thể, nhỏ hơn các tiếng thưởng.
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
        int lastPegVariant = -1;

        public const float PegGap = 0.1f, PegMaxVolume = 0.6f;
        static readonly float[] PegPitch = { 0.92f, 1f, 1.1f };

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

        // speed: tốc độ bi lúc chạm (đơn vị máy/giây), to dần theo tốc độ tới PegMaxVolume; tối đa 10 tiếng mỗi giây.
        // Trả về false nếu bị hãm (để rung chạm đinh đi cùng nhịp với tiếng).
        public bool Peg(float speed)
        {
            float now = Time.unscaledTime;
            if (lastPeg >= 0 && now - lastPeg < PegGap) return false;
            lastPeg = now;
            int v = lastPegVariant < 0 ? Random.Range(0, PegPitch.Length) : Random.Range(0, PegPitch.Length - 1);
            if (lastPegVariant >= 0 && v >= lastPegVariant) v++;
            lastPegVariant = v;
            float vol = Mathf.Min(1f, speed / 540f) * PegMaxVolume * (1 + (Random.value - 0.5f) * 0.14f);
            Play("peg", vol, PegPitch[v] * (1 + (Random.value - 0.5f) * 0.1f));
            return true;
        }
    }
}
