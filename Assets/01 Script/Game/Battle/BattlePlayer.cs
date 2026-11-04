// Phát lại sự kiện trận kèm hoạt cảnh (chép playEv của Web/src/view/battle/battleScreen.ts).
// Mỗi loại sự kiện một handler; chờ tính theo giây sân (StageView.Wait: lúc ra đòn sân chậm thì chờ chậm cùng); đòn đánh, tuyệt kỹ,
// chiêu chờ tới khung trúng đòn rồi mới chạy tiếp,
// phần còn lại của clip chạy song song; trước sự kiện card/turn/ult/attack/round/swap và chiêu (innate "skill") thì chờ clip trước xong.
// Thanh số chỉ vẽ theo ảnh chụp của sự kiện (không đọc trạng thái trận, vì trạng thái đã đi trước hoạt cảnh).
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

        static string StatName(Stat s) =>
            s == Stat.Atk ? "Công" : s == Stat.Def ? "Thủ" : s == Stat.Crit ? "Chí mạng" : s == Stat.Lifesteal ? "Hút máu" : s == Stat.Dodge ? "Né" : "Sát thương nhận";

        object W(float ms) => st.Wait(ms / 1000f);

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
            var h = st.Play(side, clip, () => { });
            pending = h;
            while (!h.hit) yield return null;
        }

        // clip bắn, tới khung trúng thì phóng tia; chờ tia tới thân đối thủ rồi mới hiện sát thương
        IEnumerator PlayBeam(int side)
        {
            float travel = 0;
            var h = st.Play(side, StageView.Cast, () => travel = st.Beam(side));
            pending = h;
            while (!h.hit) yield return null;
            yield return st.Wait(travel);
        }

        public IEnumerator Play(BattleEvent e)
        {
            var sfx = App.Audio;
            if (e.t == EvType.Card || e.t == EvType.Turn || e.t == EvType.Ult || e.t == EvType.Attack || e.t == EvType.Round || e.t == EvType.Swap)
                yield return WaitPending();
            switch (e.t)
            {
                case EvType.Start:
                    break;
                case EvType.Round:
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
                    var c = b.Data.Card(e.card);
                    sfx.Play("card");
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
                    bool up = e.stat == Stat.DmgTaken ? e.v < 0 : e.v > 0;
                    string v = e.stat == Stat.DmgTaken
                        ? $"{StatName(e.stat)} {(e.v > 0 ? "+" : "−")}{CardText.Pct(Math.Abs(e.v))}"
                        : $"{(e.v > 0 ? "+" : "−")}{CardText.Pct(Math.Abs(e.v))} {StatName(e.stat)}";
                    st.Text(e.side, $"{(up ? "▲" : "▼")} {v}", up ? "#9be36a" : "#ff8a7a", 21);
                    sfx.Play(up ? "buff" : "debuff");
                    yield return W(230);
                    break;
                }
                case EvType.Heal:
                    st.Number(e.side, e.amount, Theme.Hex("#7be36a"));
                    st.Ring(e.side, "#6cbf4f");
                    sfx.Play("heal");
                    yield return W(260);
                    break;
                case EvType.MaxHp:
                    st.Text(e.side, $"+{e.amount} máu tối đa", "#7be36a", 21);
                    st.Ring(e.side, "#f7c948");
                    sfx.Play("heal");
                    yield return W(260);
                    break;
                case EvType.Shield:
                    st.Text(e.side, $"+{e.amount} khiên", "#8ec5ff", 22);
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
                    string name = e.status == StatusId.Burn ? "Bỏng!" : e.status == StatusId.Stun ? "Choáng!" : e.status == StatusId.Regen ? "Hồi phục" : "Sẵn sàng né";
                    st.Text(e.side, name, e.status == StatusId.Burn ? "#ffb070" : e.status == StatusId.Stun ? "#ffe14a" : "#bfe8a0", 26);
                    sfx.Play(e.status == StatusId.Stun || e.status == StatusId.Burn ? "debuff" : "buff");
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
                    if (LastSnap != null && LastSnap.active[e.side] != e.idx) break;
                    st.Text(e.side, $"◆ {b.Data.Card(e.card).name}", "#e3c4ff", 20);
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
                    yield return PlayClip(e.side, StageView.Skill);
                    break;
                }
                case EvType.Dmg:
                {
                    if (e.dmgKind == DmgKind.Self)
                    {
                        st.Number(e.to, e.amount, Theme.Hex("#ff8a7a"));
                        sfx.Play("debuff");
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
                    if (e.dmgKind == DmgKind.Burn)
                    {
                        st.Number(e.to, e.amount, Theme.Hex("#ffb070"));
                        st.Hurt(e.to);
                        sfx.Hit(false);
                        yield return W(360);
                        break;
                    }
                    bool big = e.crit || e.dmgKind == DmgKind.Ult;
                    st.Hurt(e.to, big);
                    st.Burst(e.to, big);
                    st.Number(e.to, e.amount, e.crit ? Theme.Hex("#ffe14a") : Theme.Hex("#ff6a5a"), big);
                    if (e.crit) st.Text(e.to, "CHÍ MẠNG!", "#ffe14a", 28);
                    if (e.elem > 1) st.Text(e.to, "Khắc hệ ×1,5", "#9be36a", 18);
                    if (e.elem < 1) st.Text(e.to, "Bị khắc ×0,75", "#c9c0b0", 18);
                    if (e.blocked > 0) st.Text(e.to, $"Khiên đỡ {e.blocked}", "#8ec5ff", 18);
                    sfx.Hit(big);
                    yield return W(big ? 330 : 240);
                    break;
                }
                case EvType.Revive:
                    yield return WaitPending();
                    st.Text(e.side, "Hồi sinh!", "#ffe08a", 30);
                    st.Ring(e.side, "#f7c948");
                    st.Flash("#fff6c9");
                    sfx.Play("level");
                    yield return W(700);
                    break;
                case EvType.Evolve:
                {
                    // boss lên dạng sau: hiệu ứng như hồi sinh, đổi hình và tên dạng (thanh máu đổi theo ảnh chụp)
                    yield return WaitPending();
                    var f = b.sides[e.side].fighters[e.idx];
                    string formName = f.hero.forms[e.form].name;
                    st.Text(e.side, "Tiến hóa!", "#ffe08a", 34);
                    st.Ring(e.side, "#f7c948");
                    st.Flash("#fff6c9");
                    sfx.Play("level");
                    if (e.side == 1) st.SetPhase(e.form + 1); // sàn đấu boss đổi theo dạng (trong lúc chớp trắng)
                    if (e.side == 1) view.SetFoeForm(e.idx, e.form); // mặt boss ở góc trên trái đổi theo dạng
                    st.SetActor(e.side, f.hero, f.boss, false, Teams.FormStar(b.Data.Cfg, e.form));
                    view.SetPlateName(e.side, formName);
                    st.Text(e.side, formName, "#fff6c8", 22);
                    yield return W(900);
                    break;
                }
                case EvType.Death:
                    yield return WaitPending();
                    st.Die(e.side);
                    st.Text(e.side, "Gục!", "#c9c0b0", 34);
                    sfx.Play("lose");
                    yield return W(900);
                    break;
                case EvType.Swap:
                {
                    sfx.Play("swap");
                    yield return W(st.Retreat(e.side) * 1000);
                    var f = b.sides[e.side].fighters[e.to];
                    st.SetActor(e.side, f.hero, f.boss, true, Teams.LookStar(b.Data.Cfg, f));
                    view.FillPlate(e.side);
                    st.Text(e.side, e.side == 0 ? $"{f.hero.name}, ra sân!" : $"{f.hero.name} ra sân", "#fff6c8", 22);
                    yield return W(480);
                    break;
                }
                case EvType.End:
                    break;
            }
            LastSnap = e.snap;
            view.ApplySnap(e.snap);
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
