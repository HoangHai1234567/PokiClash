// Màn chọn bạn đồng hành (prefab Assets/04 Prefabs/Dialogs/ChonTuongKhoiDau, biến thể tờ giấy gốc HopThoai trải kín màn, nền đen;
// dựng bằng menu "PokiClash/Prefab/Hộp thoại và màn/Hộp chọn tướng khởi đầu (ChonTuongKhoiDau)"). Người chơi mới chọn 1 trong 5 tướng
// khởi đầu, mỗi hệ một con (GD_Claude/15_TuongKhoiDau.md). Bắt buộc.
// Người dùng 2026-11-24: 5 tướng xếp vòng tròn 3D theo độ sâu (con trước to, con sau nhỏ dần, cao hơn, tối dần trên nền đen, xếp lớp
// theo độ sâu); vuốt ngang để xoay, thả thì trôi rồi dừng đúng một con, chạm con phía sau thì xoay nó ra trước. Con đứng trước hiện
// tên, hệ, vai, danh hiệu và chỉ số Máu, Công, Thủ: số kèm thanh 5 nấc tượng trưng (xếp theo 5 tướng khởi đầu, thấp nhất 2 nấc, cao
// nhất 5 nấc; nấc bình hành nền trắng, Máu xanh lá, Công đỏ, Thủ xanh dương: StatPips), Lực chiến. 5 con chạy dáng đứng lệch nhịp, thỉnh thoảng làm trò (đánh, tung chiêu, nhún); con vừa ra trước nhún bật và
// tung chiêu; bấm Chọn rồi đồng ý: con đó tung chiêu, 4 con kia nhún chào, rồi mới đóng.
using System;
using System.Collections;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class StarterDialog : Dialog
    {
        [Serializable]
        public struct Parts
        {
            public RectTransform ring; // tâm vòng (chân con đứng trước)
            public RectTransform[] slots; // 5 ô theo thứ tự App.Data.Starters, gốc ở giữa đáy
            public HeroViewer[] viewers;
            public CanvasGroup[] fades; // tối dần theo độ sâu (nền đen: độ đục thấp là tối)
            public SwipeArea swipe;
            public TextMeshProUGUI name, elem, title, power;
            public Image elemIcon;
            public StatPips[] stats; // Máu, Công, Thủ: nấc bình hành nền trắng, màu xanh lá, đỏ, xanh dương
            public SketchButton pick;
        }

        [SerializeField] Parts p;

        // bán kính vòng, độ nâng con xa nhất, cỡ con xa nhất, px kéo cho một con, cạnh ô xem tướng
        public const float Radius = 330, Lift = 170, FarScale = 0.55f, SlotPx = 300, ViewSize = 500;
        const float FarAlpha = 0.55f, FarTint = 0.32f; // con xa nhất: độ đục (chân dung) và nhân màu hình rig (AolaSticker không theo độ đục)

        string[] ids;
        Action<string> onPicked;
        float rot, target, vel, dragVel, lastDrag;
        bool dragging, picking;
        int focus = -1, cheered = -1;
        float[] funAt, hopAt;
        // nấc của từng chỉ số (Máu, Công, Thủ) từng tướng, xếp theo 5 tướng khởi đầu
        int[,] pips;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        int N => ids.Length;

        public void Show(Action<string> picked = null)
        {
            var d = App.Data;
            onPicked = picked;
            ids = d.Starters.Take(p.slots.Length).ToArray();
            funAt = new float[N];
            hopAt = new float[N];
            var vals = new int[N, 3];
            for (int i = 0; i < p.slots.Length; i++)
            {
                bool on = i < N;
                p.slots[i].gameObject.SetActive(on);
                if (!on) continue;
                var s = HeroStats.Compute(d.Cfg, d.Hero(ids[i]), 1, 1);
                vals[i, 0] = (int)s.hp;
                vals[i, 1] = (int)s.atk;
                vals[i, 2] = (int)s.def;
                p.viewers[i].Centred = true;
                p.viewers[i].Bind(d.Hero(ids[i]), ViewSize, false);
                funAt[i] = Time.unscaledTime + 2.5f + i * 1.1f + UnityEngine.Random.value * 2;
                hopAt[i] = -9;
            }
            pips = new int[N, 3];
            for (int k = 0; k < 3; k++)
            {
                int lo = int.MaxValue, hi = int.MinValue;
                for (int i = 0; i < N; i++)
                {
                    lo = Math.Min(lo, vals[i, k]);
                    hi = Math.Max(hi, vals[i, k]);
                }
                for (int i = 0; i < N; i++)
                    pips[i, k] = hi == lo ? 4 : 2 + Mathf.RoundToInt(3f * (vals[i, k] - lo) / (hi - lo));
            }
            rot = target = vel = 0;
            p.swipe.Began = () =>
            {
                if (picking) return;
                dragging = true;
                dragVel = 0;
                lastDrag = Time.unscaledTime;
            };
            p.swipe.Dragged = Drag;
            p.swipe.Ended = Release;
            p.swipe.Tapped = Tap;
            p.pick.SetOnClick(Confirm);
            Layout();
            Focus(0);
        }

        void Drag(Vector2 delta)
        {
            if (!dragging || picking) return;
            float dx = delta.x / Scale();
            float step = -dx / SlotPx;
            rot += step;
            float dt = Mathf.Max(0.001f, Time.unscaledTime - lastDrag);
            lastDrag = Time.unscaledTime;
            dragVel = Mathf.Lerp(dragVel, step / dt, 0.5f);
        }

        // thả: trôi theo đà rồi dừng đúng một con (tối đa 2 con mỗi lần vuốt)
        void Release()
        {
            if (!dragging) return;
            dragging = false;
            float fling = Mathf.Clamp(dragVel * 0.18f, -2, 2);
            target = Mathf.Round(rot + fling);
            vel = 0;
        }

        // chạm: con gần chỗ chạm nhất (con trước được ưu tiên); con phía sau thì xoay nó ra trước, con đang đứng trước thì làm trò
        void Tap(Vector2 screen)
        {
            if (picking) return;
            var canvas = GetComponentInParent<Canvas>();
            var cam = canvas && canvas.rootCanvas.renderMode != RenderMode.ScreenSpaceOverlay ? canvas.rootCanvas.worldCamera : null;
            if (!RectTransformUtility.ScreenPointToLocalPointInRectangle(p.ring, screen, cam, out var lp)) return;
            int best = -1;
            float bestD = float.MaxValue;
            for (int i = 0; i < N; i++)
            {
                var rt = p.slots[i];
                float s = rt.localScale.x;
                var c = rt.anchoredPosition + new Vector2(0, ViewSize * 0.35f * s); // giữa thân
                float dx = Mathf.Abs(lp.x - c.x), dy = Mathf.Abs(lp.y - c.y);
                if (dx > 150 * s || dy > 190 * s) continue;
                float dd = dx / s - Depth(i) * 60; // con trước nằm trên: ưu tiên
                if (dd < bestD)
                {
                    bestD = dd;
                    best = i;
                }
            }
            if (best < 0) return;
            if (best == focus && Mathf.Abs(rot - target) < 0.05f)
            {
                Cheer(best, HeroViewer.Attack);
                return;
            }
            App.Audio.Play("click");
            target = Mathf.Round(rot) + Shortest(best - Mod(Mathf.RoundToInt(rot)));
            vel = 0;
        }

        float Scale()
        {
            var canvas = GetComponentInParent<Canvas>();
            return canvas ? canvas.rootCanvas.scaleFactor : 1;
        }

        int Shortest(int d)
        {
            d = Mod(d);
            return d > N / 2 ? d - N : d;
        }

        int Mod(int i) => ((i % N) + N) % N;

        // góc của con i: 0 ở trước mặt
        float Angle(int i) => 2 * Mathf.PI * (i - rot) / N;

        // độ sâu: 1 trước mặt, -1 xa nhất
        float Depth(int i) => Mathf.Cos(Angle(i));

        void Update()
        {
            if (ids == null) return;
            float dt = Mathf.Min(0.05f, Time.unscaledDeltaTime);
            if (!dragging) rot = Mathf.SmoothDamp(rot, target, ref vel, 0.16f, Mathf.Infinity, dt);
            Layout();
            int f = Mod(Mathf.RoundToInt(rot));
            if (f != focus) Focus(f);
            // dừng hẳn ở một con: con đó nhún bật, tung chiêu (mỗi lần ra trước một lần)
            if (!dragging && !picking && Mathf.Abs(rot - target) < 0.02f && cheered != focus)
            {
                cheered = focus;
                Cheer(focus, HeroViewer.Skill);
            }
            Fun();
        }

        void Layout()
        {
            var order = Enumerable.Range(0, N).OrderBy(Depth).ToArray();
            for (int k = 0; k < order.Length; k++) p.slots[order[k]].SetSiblingIndex(k); // xa trước, gần sau (vẽ đè)
            for (int i = 0; i < N; i++)
            {
                float a = Angle(i), z = Mathf.Cos(a), near = (z + 1) / 2;
                float s = Mathf.Lerp(FarScale, 1, near);
                float hop = Hop(i) * 46 * s;
                p.slots[i].anchoredPosition = new Vector2(Radius * Mathf.Sin(a), (1 - near) * Lift + hop);
                p.slots[i].localScale = new Vector3(s, s, 1);
                p.fades[i].alpha = Mathf.Lerp(FarAlpha, 1, near);
                p.viewers[i].Tint = Mathf.Lerp(FarTint, 1, near * near);
            }
        }

        // nhún: 0 → 1 → 0 trong 0,42 giây sau hopAt
        float Hop(int i)
        {
            float k = (Time.unscaledTime - hopAt[i]) / 0.42f;
            return k is >= 0 and <= 1 ? Mathf.Sin(k * Mathf.PI) : 0;
        }

        void Cheer(int i, string clip)
        {
            hopAt[i] = Time.unscaledTime;
            if (clip != null) p.viewers[i].Play(clip);
            funAt[i] = Time.unscaledTime + 4 + UnityEngine.Random.value * 3;
        }

        // trò vui: mỗi con 4–7 giây một lần; con trước và hai con bên đánh hoặc tung chiêu, hai con xa chỉ nhún
        void Fun()
        {
            if (picking) return;
            for (int i = 0; i < N; i++)
            {
                if (Time.unscaledTime < funAt[i]) continue;
                float z = Depth(i);
                string clip = z > 0.9f ? (UnityEngine.Random.value < 0.5f ? HeroViewer.Attack : HeroViewer.Skill)
                    : z > 0 ? (UnityEngine.Random.value < 0.6f ? HeroViewer.Attack : null)
                    : null;
                Cheer(i, clip);
            }
        }

        void Focus(int f)
        {
            focus = f;
            var d = App.Data;
            var h = d.Hero(ids[f]);
            string role = Tutorial.Role(h.id);
            var col = Theme.Of(h.elem);
            p.name.text = h.name;
            p.elem.text = Loc.F("Hệ {0}", Elements.Name(h.elem)) + (string.IsNullOrEmpty(role) ? "" : " · " + role);
            p.elem.color = Color.Lerp(col, Color.white, 0.25f);
            if (p.elemIcon) Theme.SetSprite(p.elemIcon, App.Art.Icon(ElemIcon(h.elem)));
            p.title.text = h.title;
            var st = HeroStats.Compute(d.Cfg, h, 1, 1);
            int[] v = { (int)st.hp, (int)st.atk, (int)st.def };
            // các nấc chạy đầy lại từ đầu, dòng sau trễ 0,1 giây
            for (int k = 0; k < p.stats.Length && k < 3; k++) p.stats[k].Set(TeamPower.Text(v[k]), pips[f, k], k * 0.1f);
            p.power.text = Loc.F("Lực chiến {0}", TeamPower.Text(HeroStats.Power(d.Cfg, st, 1)));
            p.pick.SetText(Loc.F("Chọn {0}", h.name));
        }

        static string ElemIcon(Elem e) => e == Elem.Hoa ? "e_hoa" : e == Elem.Thuy ? "e_thuy" : e == Elem.Moc ? "e_moc" : e == Elem.Kim ? "e_kim" : "e_tho";

        // người mới chưa biết thẻ là gì (GD_Claude/25_FTUE.md bước A3–A4): chỉ tên, hệ, danh hiệu và một chữ vai. Hệ khắc, 3 thẻ xem ở
        // hộp chi tiết tướng sau. Bản cũ (hệ khắc, 3 thẻ ở cấp 1) giữ ở DescribeFull.
        public static string Describe(GameData d, HeroDef h)
        {
            string role = Tutorial.Role(h.id);
            return Loc.F("<b>{0}</b> · hệ {1}\n", h.name, Elements.Name(h.elem)) +
                   (string.IsNullOrEmpty(role) ? "" : Loc.F("<size=120%><b>{0}</b></size>\n", role)) +
                   $"<i>{h.title}</i>";
        }

        // hệ, khắc và bị khắc, 3 thẻ ở cấp 1
        public static string DescribeFull(GameData d, HeroDef h)
        {
            string Card(string id)
            {
                var c = d.Card(id);
                return $"<b>{Elements.KindName(c.kind)} · {c.name}:</b> {CardText.Text(c, 1, d.Cfg.cardLvStep)}";
            }
            return Loc.F("<b>{0}</b> · hệ {1} · {2}\n", h.name, Elements.Name(h.elem), h.title) +
                   Loc.F("Khắc {0}, bị {1} khắc ", Elements.Name(Elements.Beats(h.elem)), Elements.Name(Progress.CounterOf(h.elem))) +
                   Loc.T("(bạn đồng hành không sợ bị khắc)\n") +
                   $"{Card(h.skill)}\n{Card(h.ult)}\n{Card(h.passive)}";
        }

        void Confirm()
        {
            if (picking || focus < 0) return;
            string sel = ids[focus];
            var h = App.Data.Hero(sel);
            App.Modals.Confirm(Loc.F("Đi cùng {0} nhé?", h.name),
                Loc.T("Không đổi lại được. Bạn sẽ gặp lại 4 bạn kia trên các đảo."),
                Loc.T("Đi thôi!"), () =>
                {
                    App.Save.Data.ChooseStarter(sel);
                    App.Save.Save();
                    // đảo của tướng vừa chọn là đảo vào đầu tiên: nạp gói của nó trước (GD_Claude/27)
                    PokiClash.Game.ContentPacks.Request(PokiClash.Core.Keys.Of(h.elem), true);
                    App.Audio.Play("chest");
                    Haptics.Play(Haptic.Reward);
                    StartCoroutine(Picked(sel));
                }, Loc.T("Xem lại"), BtnColor.Green);
        }

        // con được chọn tung chiêu, 4 con kia nhún chào lệch nhịp, rồi đóng
        IEnumerator Picked(string sel)
        {
            picking = true;
            p.pick.gameObject.SetActive(false);
            Cheer(focus, HeroViewer.Skill);
            for (int i = 0; i < N; i++)
                if (i != focus) hopAt[i] = Time.unscaledTime + 0.15f + 0.12f * i;
            yield return new WaitForSecondsRealtime(1.3f);
            Close();
            onPicked?.Invoke(sel);
        }

#if UNITY_EDITOR
        // menu chụp thử (StarterRingShots): xoay tới vị trí r (đơn vị con), không trôi
        public void DebugRotate(float r)
        {
            rot = target = r;
            vel = 0;
        }

        public int DebugFocus => focus;
#endif
    }
}
