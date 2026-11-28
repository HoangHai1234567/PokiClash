// TIẾNG CHIÊU trên sân (2026-11-24, làm lại 2026-11-28; bảng tiếng ở SkillSfx.cs). Một chỗ điều phối: StageView gọi SkillSound ở PreFx / AtkFx
// / UltFx / FireBeam với mã chiêu và giờ tới lúc trúng; các mốc của bảng hẹn theo giờ SÂN (HatLua.At: dừng / tua cùng trận), cao độ ±4 %
// cho đỡ nhàm. Chiêu nhiều phát nghe từng cú: mỗi cú rung màn (HatLua.Shake) hay nhịp trúng (NuocPulse / DanhTrung / HoaTrung) của chiêu
// đang diễn gọi ImpactSound — trước lúc trúng là tiếng "cast" (dậm, bắn pháo), sau lúc trúng là "rep" (đạn, thiên thạch, nhát chém tới
// nơi) hay "big" (cú rung mạnh nhất, nổ kết), cách nhau ≥ 0,1 s, tối đa 16 cú. Chiêu mới (clip đánh / chiêu / tuyệt kỹ bắt đầu) xoá chiêu
// cũ nên cú rung của đòn sau không phát nhầm tiếng chiêu trước.
using UnityEngine;

namespace PokiClash
{
    public sealed partial class StageView
    {
        const float RepGap = 0.1f, CastGap = 0.15f, PulseMin = 0.35f;
        const int RepMax = 16;

        SkillSfx.Cue tieng;          // chiêu đang diễn (null = không có)
        float tiengTrung, tiengHet;  // giờ sân lúc trúng, hết cửa sổ nghe cú trúng phụ
        float tiengRep, tiengCast;   // giờ sân của tiếng cú trúng / tiếng cast vừa phát
        int tiengSoRep;
        bool tiengBig;

        void TiengMoi() => tieng = null;

        void SkillSound(Actor a, string kind, float tHit)
        {
            if (a?.hero == null || App.Audio == null) return;
            var cue = SkillSfx.Get(kind, a.hero.elem, a.hero.id);
            if (cue == null) return;
            tHit = Mathf.Max(0, tHit);
            tieng = cue;
            tiengTrung = Clock + tHit;
            tiengHet = tiengTrung + cue.win;
            tiengRep = tiengTrung; // cú rung đúng lúc trúng đã có tiếng trúng của bảng
            tiengCast = -9;
            tiengSoRep = 0;
            tiengBig = false;
            var h = Hat;
            foreach (var m in cue.marks)
            {
                float at = SkillSfx.When(m, tHit);
                string s = m.snd;
                float vol = at <= 0.02f ? 0.85f : 0.9f;
                if (at <= 0.02f || h == null) Tieng(s, vol);
                else h.At(at, () => Tieng(s, vol));
            }
        }

        static void Tieng(string s, float vol) => App.Audio?.Play(s, vol, Random.Range(0.96f, 1.04f));

        // mag: độ rung (Shake) hoặc độ mạnh nhịp trúng 0..1 (pulse)
        void ImpactSound(float mag, bool pulse)
        {
            var c = tieng;
            if (c == null || Clock > tiengHet) return;
            if (pulse ? mag < PulseMin : mag < c.min) return;
            float now = Clock;
            if (now < tiengTrung - 0.05f)
            {
                if (c.cast == null || now - tiengCast < CastGap) return;
                tiengCast = now;
                Tieng(c.cast, 0.8f);
                return;
            }
            if (now - tiengRep < RepGap) return;
            if (c.big != null && !tiengBig && !pulse && mag >= c.bigMin)
            {
                tiengBig = true;
                tiengRep = now;
                Tieng(c.big, 1f);
                return;
            }
            if (c.rep == null || tiengSoRep >= RepMax) return;
            tiengSoRep++;
            tiengRep = now;
            Tieng(c.rep, 0.75f);
        }
    }
}
