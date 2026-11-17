// Phát lại sự kiện trận kèm hoạt cảnh (chép playEv của Web/src/view/battle/battleScreen.ts).
// Mỗi loại sự kiện một handler; chờ tính theo giây sân (StageView.Wait: lúc ra đòn sân chậm thì chờ chậm cùng); đòn đánh, tuyệt kỹ,
// chiêu chờ tới khung trúng đòn rồi mới chạy tiếp,
// phần còn lại của clip chạy song song; trước sự kiện card/turn/ult/attack/round/swap và chiêu (innate "skill") thì chờ clip trước xong.
// Thanh số chỉ vẽ theo ảnh chụp của sự kiện (không đọc trạng thái trận, vì trạng thái đã đi trước hoạt cảnh).
// Trình diễn (2026-11-17): cú hạ gục cho tướng ngã ngay (clip chết, StageView.KnockDown); Death chờ clip chết chạy trọn; Swap chờ tướng cũ
// nằm hẳn / lùi khỏi sân rồi tướng mới diễn clip ra sân; tướng chỉ ra đòn khi clip ra sân của nó xong (WaitEntered); Evolve là chuỗi
// chết → biến hình → ra sân (StageView.Evolve), thanh máu dâng có nhịp (BattleView.FillHp); Revive: nằm xuống rồi được nâng dậy.
// Ảnh chụp của bị động Tiến Hóa boss và bị động hồi sinh đã là trạng thái sau (máu đầy): giữ lại tới sự kiện Evolve / Revive.
using System;
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public sealed class BattlePlayer
    {
        readonly Battle b;
        readonly BattleView view;
        readonly StageView st;
        readonly MonoBehaviour host;
        ClipHandle pending;
        public int ExecIdx = -1;
        public Snap LastSnap;
        public Func<bool> Alive = () => true;
        public Func<int, IEnumerator> OnRound; // băng rôn "Hiệp N"
        public Func<string, string, bool, IEnumerator> Banner;
        public Func<int, CardDef, IEnumerator> UltCut; // dải tuyệt kỹ: chờ chạy xong rồi mới phát clip (không có thì băng rôn)
        public Action<int> OnTurnFoe; // vẽ lá úp của địch

        public BattlePlayer(MonoBehaviour host, Battle b, BattleView view)
        {
            this.host = host;
            this.b = b;
            this.view = view;
            st = view.Stage;
        }

        // màu chữ, số theo loại (độc: xanh độc; phản đòn: tím gai)
        const string PoisonHex = "#8fd14f", ThornsHex = "#d79cff";

        // màu chữ nổi khi dính trạng thái
        static string StatusHex(StatusId id) =>
            id == StatusId.Burn ? "#ffb070" : id == StatusId.Stun ? "#ffe14a" : id == StatusId.Poison ? PoisonHex : "#bfe8a0";

        // số lớp của trạng thái id trên tướng đang ra sân bên side (độc; 0 nếu không có)
        static int Stacks(Snap s, int side, StatusId id)
        {
            if (s == null) return 0;
            var f = s.f[side][s.active[side]];
            for (int i = 0; i < f.st.Count; i++)
                if (f.st[i].id == id)
                    return i < f.stk.Count ? f.stk[i] : 0;
            return 0;
        }

        object W(float ms) => st.Wait(ms / 1000f);

        // thang ngũ cung trưởng (bán cung) cho chuỗi leo cao độ; quá 1 quãng tám thì giữ ở đỉnh
        static readonly int[] PentSteps = { 0, 2, 4, 7, 9, 12 };
        public static int Pent(int i) => PentSteps[Mathf.Clamp(i, 0, PentSteps.Length - 1)];
        public static float Semitone(int n) => Mathf.Pow(2, n / 12f);

        // rung tay mạnh dần theo độ mạnh cú (0..1 → ×0,75..×1,35)
        static float HapticGain(float pw) => 0.75f + 0.6f * pw;

        public IEnumerator WaitPending()
        {
            while (pending != null && !pending.done) yield return null;
        }

        public IEnumerator PlayAll(List<BattleEvent> evs)
        {
            foreach (var e in evs)
            {
                if (!Alive()) yield break;
                yield return Play(e);
            }
            yield return WaitPending();
        }

        IEnumerator PlayClip(int side, string clip)
        {
            yield return st.WaitEntered(side); // còn đang diễn clip ra sân: ra đòn sau
            var h = st.Play(side, clip, () => { });
            pending = h;
            while (!h.hit) yield return null;
        }

        // clip bắn, tới khung trúng thì phóng tia; chờ tia tới thân đối thủ rồi mới hiện sát thương
        IEnumerator PlayBeam(int side)
        {
            float travel = 0;
            yield return st.WaitEntered(side);
            var h = st.Play(side, StageView.Cast, () => travel = st.Beam(side));
            pending = h;
            while (!h.hit) yield return null;
            yield return st.Wait(travel);
        }

        // clip CHIÊU; tướng hệ Hỏa có hiệu ứng hạt (StageView.UltFx: thiên thạch, dung nham phun, lốc xoáy, nổ lớn) phát lúc trúng,
        // chờ tới lúc hiệu ứng chạm đối thủ rồi mới hiện sát thương
        IEnumerator PlayUlt(int side)
        {
            float travel = 0;
            yield return st.WaitEntered(side);
            var h = st.Play(side, StageView.Skill, () => travel = st.UltFx(side));
            pending = h;
            while (!h.hit) yield return null;
            if (travel > 0) yield return st.Wait(travel);
        }

        public IEnumerator Play(BattleEvent e)
        {
            var sfx = App.Audio;
            bool keep = false; // giữ ảnh chụp cũ (bị động Tiến Hóa, hồi sinh: ảnh chụp đã là máu sau khi lên dạng / sống lại)
            if (e.t == EvType.Card || e.t == EvType.Turn || e.t == EvType.Ult || e.t == EvType.Attack || e.t == EvType.Round || e.t == EvType.Swap)
                yield return WaitPending();
            switch (e.t)
            {
                case EvType.Start:
                    break;
                case EvType.Round:
                    // băng rôn hiệp mới chạy ngang giữa sân: chờ tướng vừa ra thay diễn xong clip ra sân (tối đa 1,6 giây), không che nhau
                    yield return st.WaitEntered(0, 1.6f);
                    yield return st.WaitEntered(1, 1.6f);
                    view.SetRound(e.round);
                    if (OnRound != null) yield return OnRound(e.round);
                    break;
                case EvType.Turn:
                    ExecIdx = -1;
                    view.SetTurn(e.side);
                    view.RenderQueue(ExecIdx, b.phase == Phase.Picking);
                    if (e.side == 1) OnTurnFoe?.Invoke(e.side);
                    break;
                case EvType.Card:
                {
                    if (e.rep == 0) ExecIdx++;
                    view.RenderQueue(ExecIdx, false);
                    view.PopNow();
                    var c = b.Data.Card(e.card);
                    // chuỗi thẻ trong lượt leo cao độ theo thang ngũ cung (GameFeel mục 6.8, 8.5): dồn lên cú đánh cuối lượt
                    sfx.Play("card", 1, Semitone(Pent(Mathf.Max(0, ExecIdx))));
                    host.StartCoroutine(FlyTile(e.side));
                    st.Text(e.side, c.name, "#fff6c8", 22);
                    yield return W(420);
                    break;
                }
                case EvType.Innate:
                {
                    // bật tuyệt kỹ chỉ đổi đòn cuối lượt; chiêu ra đòn ngay lúc bấm, hiệu ứng của nó là các sự kiện theo sau
                    if (e.kind != "skill") break;
                    yield return WaitPending();
                    var c = b.Data.Card(e.card);
                    sfx.Play("card");
                    st.Text(e.side, c.name, "#8ec5ff", 22);
                    // chiêu dùng mana: tướng có tia (Giọt Sương) bắn tia nước tới đối thủ; clip CHIÊU để dành cho tuyệt kỹ
                    if (st.CanBeam(e.side)) yield return PlayBeam(e.side);
                    else yield return PlayClip(e.side, StageView.Skill);
                    break;
                }
                case EvType.Buff:
                {
                    bool up = CardText.StatUp(e.stat, e.v);
                    string pct = $"{(e.v > 0 ? "+" : "−")}{CardText.Pct(Math.Abs(e.v))}";
                    // chặn hồi máu: nhãn riêng cho rõ ("Chặn hồi máu" khi mất hết, không thì "Hồi máu nhận −50%"); sát thương nhận, hồi máu
                    // nhận, phản đòn ghi tên trước số; còn lại số trước tên
                    string v = e.stat == Stat.HealTaken && e.v <= -1 ? "Chặn hồi máu"
                        : e.stat == Stat.DmgTaken || e.stat == Stat.HealTaken || e.stat == Stat.Thorns ? $"{CardText.StatLabel(e.stat)} {pct}"
                        : $"{pct} {CardText.StatLabel(e.stat)}";
                    string hex = e.stat == Stat.Thorns && up ? ThornsHex : e.stat == Stat.HealTaken && !up ? "#c79bff" : up ? "#9be36a" : "#ff8a7a";
                    st.Text(e.side, $"{(up ? "▲" : "▼")} {v}", hex, e.stat == Stat.HealTaken && !up ? 23 : 21);
                    sfx.Play(up ? "buff" : "debuff");
                    yield return W(e.stat == Stat.HealTaken && !up ? 320 : 230);
                    break;
                }
                case EvType.Heal:
                    st.Number(e.side, e.amount, Theme.Hex("#7be36a"));
                    st.Ring(e.side, "#6cbf4f");
                    sfx.Play("heal");
                    yield return W(260);
                    break;
                case EvType.MaxHp:
                    st.Text(e.side, $"+{NumFmt.Short(e.amount)} máu tối đa", "#7be36a", 21);
                    st.Ring(e.side, "#f7c948");
                    sfx.Play("heal");
                    yield return W(260);
                    break;
                case EvType.Shield:
                    st.Text(e.side, $"+{NumFmt.Short(e.amount)} khiên", "#8ec5ff", 22);
                    st.Ring(e.side, "#4a90d9");
                    sfx.Play("shield");
                    yield return W(260);
                    break;
                case EvType.Mana:
                    st.Text(e.side, $"{(e.v > 0 ? "+" : "")}{e.v} mana", "#8ec5ff", 19);
                    yield return W(160);
                    break;
                case EvType.Rage:
                    st.Text(e.side, $"{(e.v > 0 ? "+" : "")}{e.v} nộ", "#ffb070", 19);
                    yield return W(160);
                    break;
                case EvType.Status:
                {
                    // độc lan sang tướng vừa ra thay (Status ngay sau Swap): chờ clip ra sân xong rồi mới báo, không đè chuỗi ra sân
                    if (st.IsEntering(e.side)) yield return st.WaitEntered(e.side, 2.4f);
                    string name = CardText.StatusFloat(e.status);
                    int stk = e.status == StatusId.Poison ? Stacks(e.snap, e.side, StatusId.Poison) : 0;
                    if (stk > 1) name += $" ×{stk}";
                    st.Text(e.side, name, StatusHex(e.status), 26);
                    sfx.Play(CardText.StatusBad(e.status) ? "debuff" : "buff");
                    yield return W(300);
                    break;
                }
                case EvType.Resist:
                    st.Text(e.side, "Trượt hiệu ứng", "#dddddd", 20);
                    yield return W(200);
                    break;
                case EvType.Cleanse:
                    st.Text(e.side, "Sạch hiệu ứng xấu", "#bfe8ff", 21);
                    st.Ring(e.side, "#bfe8ff");
                    yield return W(240);
                    break;
                case EvType.Double:
                    st.Text(e.side, "Thẻ sau ×2!", "#ffe14a", 24);
                    yield return W(240);
                    break;
                case EvType.Stunned:
                    st.Text(e.side, "Choáng: mất lượt", "#ffe14a", 20);
                    sfx.Play("debuff");
                    yield return W(700);
                    break;
                case EvType.Passive:
                {
                    // Tiến Hóa của boss: chuỗi Evolve tự báo (không chữ), thanh máu dâng ở đó. Luật mới (C, 2026-11-17): sự kiện này phát TRƯỚC
                    // khi đổi dạng, ảnh chụp còn dạng cũ máu 0 nên vẽ bình thường; luật cũ phát sau (ảnh chụp đã đầy máu) thì giữ tới Evolve.
                    if (e.card == Battle.BossEvoCard)
                    {
                        var nf = e.snap != null && e.idx < e.snap.f[e.side].Count ? e.snap.f[e.side][e.idx] : null;
                        var of = LastSnap != null && e.idx < LastSnap.f[e.side].Count ? LastSnap.f[e.side][e.idx] : null;
                        keep = nf != null && of != null && nf.hp > of.hp;
                        break;
                    }
                    if (LastSnap != null && LastSnap.active[e.side] != e.idx) break;
                    var pc = b.Data.Card(e.card);
                    if (pc.trigger == PassiveTrigger.Death) keep = true; // hồi sinh: máu dâng lúc Revive
                    st.Text(e.side, $"◆ {pc.name}", "#e3c4ff", 20);
                    yield return W(260);
                    break;
                }
                case EvType.Attack:
                    ExecIdx = b.turn.queue.Count;
                    view.RenderQueue(ExecIdx, false);
                    sfx.Play("whoosh");
                    yield return PlayClip(e.side, StageView.Attack);
                    break;
                case EvType.Ult:
                {
                    ExecIdx = b.turn.queue.Count;
                    view.RenderQueue(ExecIdx, false);
                    var c = b.Data.Card(e.card);
                    sfx.Play("ult");
                    st.Flash("#fff3c4");
                    if (UltCut != null) yield return UltCut(e.side, c);
                    else if (Banner != null) host.StartCoroutine(Banner(c.name, $"Tuyệt kỹ của {b.ActiveOf(e.side).Name}", true));
                    yield return PlayUlt(e.side);
                    break;
                }
                case EvType.Dmg:
                {
                    // cú hạ gục (máu về 0 trong ảnh chụp): tướng ngã ngay ở cú này (clip chết); Death / Evolve / Revive sau đó diễn tiếp
                    var tf = e.snap != null && e.snap.f[e.to].Count > e.snap.active[e.to] ? e.snap.f[e.to][e.snap.active[e.to]] : null;
                    bool ko = tf != null && (tf.dead || tf.hp <= 0);
                    bool last = ko && e.snap.f[e.to].TrueForAll(x => x.dead || x.hp <= 0);
                    // boss còn dạng sau: cú này không phải cú cuối trận (không đứng hình 0,2 giây kiểu hết trận), chuỗi tiến hóa theo sau
                    if (last && EvolvesNext(e.to, e.snap)) last = false;
                    if (e.dmgKind == DmgKind.Self)
                    {
                        st.Number(e.to, e.amount, Theme.Hex("#ff8a7a"));
                        sfx.Play("debuff");
                        if (ko) st.KnockDown(e.to);
                        yield return W(240);
                        break;
                    }
                    if (e.dodged)
                    {
                        st.Dodge(e.to);
                        st.Text(e.to, "Né!", "#e3c4ff", 30);
                        sfx.Play("miss");
                        yield return W(260);
                        break;
                    }
                    if (e.dmgKind == DmgKind.Poison) // độc mỗi lượt / kích nổ: như bỏng, số xanh độc, kèm số lớp
                    {
                        st.Number(e.to, e.amount, Theme.Hex(PoisonHex));
                        int stk = Stacks(e.snap, e.to, StatusId.Poison);
                        st.Text(e.to, stk > 0 ? $"Độc ×{stk}" : "Độc", PoisonHex, 18);
                        st.Hurt(e.to, false, true);
                        sfx.Hit(false);
                        if (ko)
                        {
                            st.KoHit(e.to, last);
                            st.KnockDown(e.to);
                            Haptics.Play(Haptic.Ko);
                        }
                        yield return W(360);
                        break;
                    }
                    if (e.dmgKind == DmgKind.Thorns) // phản đòn: số hiện trên KẺ ĐÁNH (e.to), tím gai, chữ "Phản đòn", tia gai văng
                    {
                        st.Number(e.to, e.amount, Theme.Hex(ThornsHex));
                        st.Text(e.to, "Phản đòn!", ThornsHex, 20);
                        st.Spark(e.to, Theme.Hex(ThornsHex), 7, 0.9f);
                        if (e.blocked > 0) st.Text(e.to, $"Khiên đỡ {NumFmt.Short(e.blocked)}", "#8ec5ff", 18);
                        st.Hurt(e.to, false);
                        sfx.Hit(false);
                        if (ko)
                        {
                            st.KoHit(e.to, last);
                            st.KnockDown(e.to);
                            Haptics.Play(Haptic.Ko);
                        }
                        else Haptics.Play(Haptic.Hit);
                        yield return W(300);
                        break;
                    }
                    if (e.dmgKind == DmgKind.Burn)
                    {
                        st.Number(e.to, e.amount, Theme.Hex("#ffb070"));
                        st.Hurt(e.to, false, true);
                        sfx.Hit(false);
                        if (ko)
                        {
                            st.KoHit(e.to, last);
                            st.KnockDown(e.to);
                            Haptics.Play(Haptic.Ko);
                        }
                        yield return W(360);
                        break;
                    }
                    bool big = e.crit || e.dmgKind == DmgKind.Ult;
                    float pw = st.Power(1 - e.to);
                    st.Hurt(e.to, big);
                    st.Burst(e.to, big);
                    st.Number(e.to, e.amount, e.crit ? Theme.Hex("#ffe14a") : Theme.Hex("#ff6a5a"), big);
                    if (e.crit)
                    {
                        st.Text(e.to, "CHÍ MẠNG!", "#ffe14a", 28 * (1 + 0.15f * pw));
                        st.Flash(new Color(1, 0.96f, 0.78f, Mathf.Lerp(0.12f, 0.22f, pw))); // chớp kem nhạt (≤ 0,15 alpha sau nhân)
                    }
                    if (e.elem > 1) st.Text(e.to, "Khắc hệ ×1,5", "#9be36a", 18);
                    if (e.elem < 1) st.Text(e.to, "Bị khắc ×0,75", "#c9c0b0", 18);
                    if (e.blocked > 0) st.Text(e.to, $"Khiên đỡ {e.blocked}", "#8ec5ff", 18);
                    sfx.Hit(big, pw);
                    // cú hạ gục: thêm nhịp khựng, rung; con cuối của phe đó (hết trận) mạnh nhất; tướng ngã ngay (clip chết)
                    if (ko)
                    {
                        st.KoHit(e.to, last);
                        st.KnockDown(e.to);
                        Haptics.Play(Haptic.Ko, HapticGain(pw));
                    }
                    else
                        Haptics.Play(e.dmgKind == DmgKind.Ult ? Haptic.UltHit : big ? Haptic.HitBig : Haptic.Hit, HapticGain(pw));
                    yield return W(big ? 330 : 240);
                    break;
                }
                case EvType.Revive:
                    // tướng đang nằm (clip chết từ cú hạ gục) được ánh sáng vàng nâng dậy, diễn clip ra sân; máu dâng lúc chớp. Không chờ clip
                    // của kẻ đánh xong (chiêu cuối dài thì clip chết đã hết): hai bên diễn song song
                    yield return st.Revive(e.side, () =>
                    {
                        st.Text(e.side, "Hồi sinh!", "#ffe08a", 30);
                        sfx.Play("level");
                        Haptics.Play(Haptic.HitBig);
                        view.FillHp(e.side, e.snap, 0.6f);
                    });
                    break;
                case EvType.Evolve:
                {
                    // boss lên dạng sau: chết → biến hình → ra sân (StageView.Evolve). Boss tiến hóa lúc máu về 0 thì cú hạ gục đã cho nó
                    // ngã, chuỗi chạy tiếp từ giữa clip chết; tiến hóa dưới ngưỡng máu thì nó ngã từ đây. Không chờ clip của kẻ đánh xong
                    // (chiêu cuối dài thì clip chết đã hết trước khi kịp sáng lên): kẻ đánh về chỗ trong lúc boss biến hình.
                    var f = b.sides[e.side].fighters[e.idx];
                    string formName = f.hero.forms[e.form].name;
                    if (!st.IsDown(e.side)) sfx.Play("stamp", 0.9f, 0.8f);
                    float pw = st.Power(e.side);
                    yield return st.Evolve(e.side, f.hero, f.boss, Teams.FormStar(b.Data.Cfg, e.form), formName,
                        () => sfx.Play("ult", 0.85f, 0.85f),
                        () =>
                        {
                            sfx.Play("level");
                            Haptics.Play(Haptic.UltHit, HapticGain(pw));
                            if (e.side == 1) st.SetPhase(e.form + 1); // sàn đấu boss đổi theo dạng (trong lúc chớp kem)
                            if (e.side == 1) view.SetFoeForm(e.idx, e.form); // mặt boss ở góc trên trái đổi theo dạng
                            view.SetPlateName(e.side, formName);
                            view.FillHp(e.side, e.snap, 0.9f); // thanh máu dâng đầy theo nhịp
                        });
                    break;
                }
                case EvType.Death:
                    yield return WaitPending();
                    st.KnockDown(e.side); // thường đã ngã từ cú hạ gục; gục vì nguyên nhân khác thì ngã từ đây
                    st.HoldPace(2); // chữ, hạt theo nhịp ×1 cùng clip chết
                    st.Text(e.side, "Gục!", "#c9c0b0", 34);
                    // địch gục là tin vui: tiếng nện "stamp" chắc tay; tướng mình gục mới dùng thang đi xuống
                    if (e.side == 1) sfx.Play("stamp", 1, 0.85f);
                    else sfx.Play("lose");
                    // clip chết chạy trọn rồi mới tới tướng kế / hộp chọn tướng thay / kết trận (trước 2026-11-17: chờ cứng 0,3 giây, clip
                    // chết bị tướng kế ra sân cắt ngang)
                    yield return st.WaitDown(e.side);
                    st.ReleasePace();
                    yield return W(120);
                    break;
                case EvType.Swap:
                {
                    // tướng cũ: đang gục thì nằm hết clip chết, còn đứng thì lùi khỏi sân; tướng mới diễn clip ra sân (đòn đầu của nó chờ
                    // clip xong, PlayClip); thanh máu dâng từ 0 (BattleView.ApplySnap thấy đổi tướng)
                    yield return st.WaitDown(e.side);
                    yield return st.WaitEntered(e.side);
                    sfx.Play("swap");
                    if (st.Retreat(e.side) > 0) yield return st.WaitRetreat(e.side);
                    var f = b.sides[e.side].fighters[e.to];
                    st.SetActor(e.side, f.hero, f.boss, true, Teams.LookStar(b.Data.Cfg, f));
                    view.FillPlate(e.side);
                    st.Text(e.side, e.side == 0 ? $"{f.hero.name}, ra sân!" : $"{f.hero.name} ra sân", "#fff6c8", 22);
                    yield return W(300);
                    break;
                }
                case EvType.End:
                    break;
            }
            if (keep) yield break;
            LastSnap = e.snap;
            view.ApplySnap(e.snap);
        }

        // cú hạ gục tướng đang ra sân bên side sẽ thành tiến hóa (boss evo, sân còn đang hiện dạng chưa cuối)
        bool EvolvesNext(int side, Snap s)
        {
            if (s == null) return false;
            var f = b.sides[side].fighters[s.active[side]];
            return f.evo && st.FormShown(side) < f.hero.forms.Length - 1;
        }

        // ô thẻ đang chạy bay từ hàng thẻ lên đầu tướng rồi tan
        IEnumerator FlyTile(int side)
        {
            var tile = view.NowTile;
            if (!tile) yield break;
            // ô bay: ô hàng thẻ dùng lại trong lớp phủ, chép hình của ô đang chạy
            var fly = view.TakeFlyTile(tile.GetComponent<QueueTile>());
            var clone = fly.Rect;
            clone.anchorMin = clone.anchorMax = new Vector2(0.5f, 0.5f);
            clone.sizeDelta = tile.rect.size;
            clone.position = tile.position;
            var cg = fly.Group;
            cg.blocksRaycasts = false;
            var head = st.Head(side);
            var target = st.transform.TransformPoint(new Vector3(head.x * StageView.K, -head.y * StageView.K + 40, 0) +
                                                     new Vector3(-((RectTransform)st.transform).rect.width / 2, ((RectTransform)st.transform).rect.height, 0));
            var from = clone.position;
            float dur = 0.32f / Mathf.Max(0.1f, st.speed * st.fast);
            for (float t = 0; t < dur * 1.6f; t += Time.unscaledDeltaTime)
            {
                if (!clone) yield break;
                float k = Mathf.Min(1, t / dur);
                float e = 1 - Mathf.Pow(1 - k, 3);
                clone.position = Vector3.Lerp(from, target, e);
                float s = Mathf.Lerp(1, 1.4f, e);
                clone.localScale = new Vector3(s, s, 1);
                clone.localEulerAngles = new Vector3(0, 0, (side == 0 ? 8 : -8) * e);
                cg.alpha = t < dur * 0.9f ? 1 : Mathf.Max(0, 1 - (t - dur * 0.9f) / (dur * 0.6f));
                yield return null;
            }
            view.ReleaseFlyTile(fly);
        }
    }
}
