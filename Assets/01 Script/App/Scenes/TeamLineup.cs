// Đội hình đầu màn Tướng (khung "doi_hinh" trong prefab Screens/Heroes, dựng bằng menu
// "PokiClash/Prefab/Popup gọn (ô thưởng, đội hình, lực chiến)"): 3 ô đội đứng thành hàng, con giữa to và đứng cao hơn, hai con hai bên
// lùi ra sau và đứng thấp xuống. Vuốt ngang xoay vòng (con bên trái / phải vào giữa); chạm con bên cạnh cũng xoay tới nó, chạm con
// giữa mở hộp chi tiết. Dưới mỗi tướng: số thứ tự ra trận, tên, lực chiến. Dưới hàng: 4 chỉ số của con giữa (icon + số), chấm vị trí.
// Đầu khung: lực chiến cả đội, nút Đổi đội (hộp chọn đội ChonDoi). Ô trống: dấu + mở hộp chọn đội; ô khoá: điều kiện mở.
// Tướng có hình aola thì đứng động (AolaSticker, clip Đứng), không thì chân dung tĩnh. Bind lại (sau mỗi lần lưu) giữ sticker của tướng
// cùng dạng, kể cả khi tướng dời sang ô khác; chỉ dựng sticker mới cho tướng mới hoặc dạng mới (dựng camera + RenderTexture tốn, người
// dùng báo giật khi đổi đội, lên cấp 2026-11-07).
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class TeamLineup : MonoBehaviour, IBeginDragHandler, IDragHandler, IEndDragHandler
    {
        // khoảng cách ngang giữa hai ô, cao tướng giữa, tỉ lệ hai bên, độ hạ thấp của hai bên
        public const float Gap = 330, HeroH = 330, SideScale = 0.74f, SideDrop = 70;

        [Serializable]
        public struct Spot
        {
            public RectTransform root, body;
            public HeroPortrait portrait;
            public ClickCatcher click;
            public Image plate, shadow;
            public TextMeshProUGUI order, name, power;
            public GameObject empty;
            public TextMeshProUGUI emptyText;
        }

        [Serializable]
        public struct Parts
        {
            public Spot[] spots;
            public TextMeshProUGUI teamPower, focusName;
            public TextMeshProUGUI[] stats; // Máu, Công, Thủ, Tốc
            public Image[] dots;
            public SketchButton edit;
        }

        [SerializeField] Parts p;
        [SerializeField] TeamPickerDialog pickerPrefab;

        Action onChange;
        readonly string[] ids = new string[3];
        readonly AolaSticker[] anim = new AolaSticker[3];
        readonly string[] animKey = new string[3]; // "<tướng>|<dạng>" của sticker trong ô
        readonly string[] waitForm = new string[3]; // ô đang hiện chân dung chờ dựng sticker (LateUpdate)
        int bindFrame; // khung Bind gần nhất (khung chạm): không dựng sticker trong khung này
        float pos, target, t; // pos: ô đang ở giữa (liên tục khi vuốt), target: ô sẽ dừng
        bool dragging;

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Parts parts, TeamPickerDialog picker)
        {
            p = parts;
            pickerPrefab = picker;
        }

        // onTeamChange: gọi sau khi đổi đội (màn Tướng vẽ lại lưới)
        public void Bind(Action onTeamChange)
        {
            onChange = onTeamChange;
            var d = App.Data;
            var s = App.Save.Data;
            var cfg = d.Cfg;
            int open = Progress.TeamSlots(s);
            var team = s.team.Where(h => s.Hero(h)?.owned == true).Take(open).ToList();
            int total = 0;
            // sticker cũ: tướng nào còn trong đội với cùng dạng thì dùng lại
            var old = new List<(string key, AolaSticker s)>();
            for (int i = 0; i < anim.Length; i++)
            {
                if (anim[i] != null) old.Add((animKey[i], anim[i]));
                anim[i] = null;
                animKey[i] = null;
                waitForm[i] = null;
            }
            for (int i = 0; i < p.spots.Length; i++)
            {
                var sp = p.spots[i];
                ids[i] = i < team.Count ? team[i] : null;
                bool locked = i >= open, filled = ids[i] != null;
                sp.empty.SetActive(!filled);
                sp.portrait.gameObject.SetActive(false);
                sp.plate.gameObject.SetActive(filled);
                sp.shadow.gameObject.SetActive(filled);
                int k = i;
                sp.click.OnClick = () => Tap(k);
                if (!filled)
                {
                    sp.emptyText.text = locked ? $"Khoá\n<size=70%>{Progress.SlotNeed(i)}</size>" : "<size=220%>+</size>\nThêm tướng";
                    continue;
                }
                var h = d.Hero(ids[i]);
                int power = HeroStats.Power(cfg, h, Teams.MemberOf(s, h.id, d));
                total += power;
                sp.order.text = (i + 1).ToString();
                sp.name.text = h.name;
                sp.power.text = TeamPower.Text(power);
                string form = HeroArt.FormOf(h).aola, key = h.id + "|" + form;
                int reuse = old.FindIndex(o => o.key == key);
                if (reuse >= 0)
                {
                    anim[i] = old[reuse].s;
                    old.RemoveAt(reuse);
                    anim[i].Rect.SetParent(sp.body, false);
                }
                else if (Game.AolaActor.Find(form, out _, out _))
                {
                    // chân dung tĩnh trước; LateUpdate dựng sticker ở khung sau (mỗi khung một cái, khi animation đã đọc xong)
                    waitForm[i] = form;
                    Game.AolaActor.Ready(form);
                }
                animKey[i] = anim[i] != null ? key : null;
                if (anim[i] == null)
                {
                    sp.portrait.gameObject.SetActive(true);
                    sp.portrait.Bind(h, HeroH / 0.62f);
                }
            }
            foreach (var o in old) o.s.Destroy();
            bindFrame = Time.frameCount;
            p.teamPower.text = TeamPower.Text(total);
            p.edit.SetOnClick(OpenPicker);
            pos = target = 0;
            Layout();
            Focus();
        }

        void OnDestroy()
        {
            foreach (var a in anim) a?.Destroy();
        }

        void OnDisable()
        {
            dragging = false;
            pos = target;
        }

        // vòng 3 ô: độ lệch của ô i so với giữa trong [-1,5; 1,5)
        float Offset(int i)
        {
            int n = p.spots.Length;
            float o = (i - pos) % n;
            if (o < -n / 2f) o += n;
            if (o >= n / 2f) o -= n;
            return o;
        }

        int Center => ((Mathf.RoundToInt(target) % p.spots.Length) + p.spots.Length) % p.spots.Length;

        void Layout()
        {
            // ô xa giữa vẽ trước (đứng sau)
            var order = Enumerable.Range(0, p.spots.Length).OrderByDescending(i => Mathf.Abs(Offset(i))).ToList();
            for (int k = 0; k < order.Count; k++)
            {
                int i = order[k];
                float o = Offset(i), a = Mathf.Min(1, Mathf.Abs(o));
                var r = p.spots[i].root;
                r.SetSiblingIndex(k);
                r.anchoredPosition = new Vector2(o * Gap, -a * SideDrop);
                float sc = Mathf.Lerp(1, SideScale, a);
                r.localScale = new Vector3(sc, sc, 1);
                // ô ra quá hai bên (đang vòng qua sau) thì mờ đi
                float fade = Mathf.Clamp01(1 - (Mathf.Abs(o) - 1) * 2);
                var cg = r.GetComponent<CanvasGroup>();
                if (cg) cg.alpha = fade;
            }
        }

        void Update()
        {
            t += Mathf.Min(0.05f, Time.unscaledDeltaTime);
            if (!dragging && Mathf.Abs(pos - target) > 0.001f)
            {
                pos = Mathf.Lerp(pos, target, 1 - Mathf.Exp(-14 * Time.unscaledDeltaTime));
                if (Mathf.Abs(pos - target) < 0.002f) pos = target;
                Layout();
            }
            for (int i = 0; i < anim.Length; i++) anim[i]?.Show(HeroViewer.Idle, t + i * 0.37f, true, 1, false, 0);
        }

        // dựng sticker đang chờ: không trong khung Bind (khung chạm), mỗi khung một cái, ô giữa trước; LateUpdate để ô xem của hộp chi
        // tiết (Update) giành lượt dựng trong khung trước
        void LateUpdate()
        {
            if (Time.frameCount <= bindFrame || !AolaSticker.CanBuildNow) return;
            for (int k = 0; k < waitForm.Length; k++)
            {
                int i = (Center + k) % waitForm.Length;
                if (waitForm[i] == null) continue;
                if (ids[i] == null)
                {
                    waitForm[i] = null;
                    continue;
                }
                if (!Game.AolaActor.Ready(waitForm[i])) continue;
                var h = App.Data.Hero(ids[i]);
                var sp = p.spots[i];
                anim[i] = AolaSticker.TryCreate(sp.body, h, waitForm[i], HeroH, false);
                animKey[i] = anim[i] != null ? h.id + "|" + waitForm[i] : null;
                if (anim[i] != null) sp.portrait.gameObject.SetActive(false);
                waitForm[i] = null;
                return;
            }
        }

        public void OnBeginDrag(PointerEventData e) => dragging = true;

        // độ dời ngón tay đổi ra đơn vị khung (canvas có camera: không chia theo lossyScale được)
        public void OnDrag(PointerEventData e)
        {
            var rt = (RectTransform)transform;
            var canvas = GetComponentInParent<Canvas>().rootCanvas;
            var cam = canvas.renderMode == RenderMode.ScreenSpaceOverlay ? null : canvas.worldCamera;
            if (!RectTransformUtility.ScreenPointToLocalPointInRectangle(rt, e.position, cam, out var now)) return;
            if (!RectTransformUtility.ScreenPointToLocalPointInRectangle(rt, e.position - e.delta, cam, out var before)) return;
            pos -= (now.x - before.x) / Gap;
            Layout();
        }

        public void OnEndDrag(PointerEventData e)
        {
            dragging = false;
            // vuốt nhanh thì sang ô kế dù chưa quá nửa
            float v = e.delta.x;
            target = Mathf.Abs(v) > 12 ? (v < 0 ? Mathf.Ceil(pos) : Mathf.Floor(pos)) : Mathf.Round(pos);
            if (Mathf.Abs(target - pos) > 1) target = Mathf.Round(pos);
            SketchButton.Sound?.Invoke("pick");
            Focus();
        }

        void Tap(int i)
        {
            float o = Offset(i);
            if (Mathf.Abs(o) > 0.5f)
            {
                SketchButton.Sound?.Invoke("pick");
                target = Mathf.Round(pos + o);
                Focus();
                return;
            }
            if (ids[i] == null)
            {
                bool locked = i >= Progress.TeamSlots(App.Save.Data);
                if (locked)
                {
                    App.Audio.Play("error");
                    App.Toasts.Show($"Ô đội {i + 1} mở khi {Progress.SlotNeed(i)}", Icon("lock"));
                    return;
                }
                App.Audio.Play("click");
                OpenPicker();
                return;
            }
            App.Audio.Play("click");
            HeroDetail.Open(ids[i], () =>
            {
                Bind(onChange);
                onChange?.Invoke();
            });
        }

        // 4 chỉ số và tên của ô sẽ dừng ở giữa, chấm vị trí
        void Focus()
        {
            int c = Center;
            for (int i = 0; i < p.dots.Length; i++) p.dots[i].color = i == c ? Theme.Ink : Theme.Paper3;
            var id = ids[c];
            foreach (var st in p.stats) st.transform.parent.gameObject.SetActive(id != null);
            if (id == null)
            {
                p.focusName.text = c >= Progress.TeamSlots(App.Save.Data) ? "Ô đội đang khoá" : "Ô đội trống";
                return;
            }
            var d = App.Data;
            var s = App.Save.Data;
            var h = d.Hero(id);
            var hp = s.Hero(id);
            var stats = HeroStats.Compute(d.Cfg, h, s.level, hp.star, false, Potential.Mods(s, d, h)); // như hộp chi tiết
            p.focusName.text = $"{h.name} <color=#{ColorUtility.ToHtmlStringRGB(Theme.Of(h.rarity))}>· {Elements.RarityName(h.rarity)}</color>";
            double[] v = { stats.hp, stats.atk, stats.def, stats.spd };
            for (int i = 0; i < p.stats.Length && i < v.Length; i++) p.stats[i].text = TeamPower.Text((int)v[i]);
        }

        void OpenPicker()
        {
            var s = App.Save.Data;
            var team = s.team.Where(h => s.Hero(h)?.owned == true).ToList();
            App.Modals.Open(pickerPrefab).Show(team, Progress.TeamSlots(s), null, picked =>
            {
                s.team = new List<string>(picked);
                App.Save.Save();
                Bind(onChange);
                onChange?.Invoke();
            });
        }
    }
}
