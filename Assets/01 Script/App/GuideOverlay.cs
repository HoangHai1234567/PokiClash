// Lớp phủ hướng dẫn người mới (GD_Claude/25_FTUE.md). Prefab Assets/04 Prefabs/Kit/HuongDan nằm trong App.prefab trên canvas riêng
// (thứ tự 30: trên thanh trên, hộp thoại và mây), dựng bằng menu "PokiClash/Prefab/Hộp thoại và màn/Hướng dẫn người mới (lớp phủ)".
// - Ép (Force): 4 dải tối quanh lỗ khoét đúng chỗ cần chạm; chạm lọt qua lỗ xuống nút thật (canvas này không có gì ở lỗ), chạm
//   ra ngoài bị dải nuốt. Nhả tay trong lỗ là xong bước.
// - Khoanh (Hint): vòng bút chì và ghi chú, không chặn chạm; xong khi chạm trong vòng hoặc hết giờ.
// - Ghi chú (Note): một tờ ghi chú cạnh chỗ đó (hoặc giữa màn), tự tắt.
// - Lời tướng (Say): nền tối kín, chân dung tướng đồng hành cạnh ghi chú, "Chạm để tiếp tục".
// Vòng khoanh là nét mực vẽ dần (InkPath), bút chì nhún chỉ vào. Chỗ cần khoanh nằm dưới hộp thoại đang mở thì chờ hộp đóng; đang
// chuyển scene, màn tải, mây chặn chạm thì chờ. Không tìm thấy chỗ cần khoanh quá lâu thì bỏ bước (không kẹt người chơi).
// Lời Lão Mực (Guide.SayMuc / Quip, đảo Casino 2026-11-27): màn có ông đứng sẵn (Guide.MucActor) thì cho chính ông nói và không tối màn;
// không thì ông trồi lên góc dưới màn (khung cắt ngang ngực, rig DealerRig dựng sẵn trong prefab, menu GuideLaoMucMenu), ghi chú cạnh đầu.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class GuideOverlay : MonoBehaviour
    {
        public sealed class Req
        {
            public string id, key, text, hero;
            public string clip; // lời Lão Mực: clip mở câu (greet, react_*...), rồi "talk" lặp
            public string scene; // scene lúc xin hiện: sang scene khác thì bỏ (chỗ cần khoanh đã mất)
            public Guide.Mode mode;
            public Action done;
            public bool repeat;
            public float secs, missing;
        }

        [SerializeField] RectTransform area; // phủ kín màn (Nen của canvas hướng dẫn)
        [SerializeField] CanvasGroup group;
        [SerializeField] Image[] blockers = new Image[4]; // trên, dưới, trái, phải
        [SerializeField] InkPath ring;
        [SerializeField] InkPath ringUnder; // nét lót màu giấy dưới vòng đỏ (nổi trên nền tối, nền đỏ như máy bi)
        [SerializeField] RectTransform pencil;
        [SerializeField] UiHint note;
        [SerializeField] HeroPortrait face;
        [SerializeField] Image me; // chân dung nhân vật chính (Guide.SayMe); ảnh trống thì không hiện
        [SerializeField] TextMeshProUGUI tapText;
        // Lão Mực ở góc màn: khung cắt (RectMask2D, gốc giữa mép dưới), lớp trượt (trồi lên), rig
        [SerializeField] RectTransform mucFrame, mucSlide;
        [SerializeField] DealerRig muc;

        public static GuideOverlay I { get; private set; }

        // Dùng khi dựng prefab (Editor).
        public void SetupMuc(RectTransform frame, RectTransform slide, DealerRig rig)
        {
            mucFrame = frame;
            mucSlide = slide;
            muc = rig;
        }

        // Dùng khi dựng prefab (Editor).
        public void Setup(RectTransform areaRt, CanvasGroup cg, Image[] blockImgs, InkPath ringPath, InkPath ringLine, RectTransform pencilRt,
            UiHint noteView, HeroPortrait faceView, Image meView, TextMeshProUGUI tap)
        {
            me = meView;
            area = areaRt;
            group = cg;
            blockers = blockImgs;
            ring = ringPath;
            ringUnder = ringLine;
            pencil = pencilRt;
            note = noteView;
            face = faceView;
            tapText = tap;
        }

        const float Pad = 14, MissingForce = 12, MissingSoft = 4, NoteW = 660, Margin = 36;
        public const float MucW = 400, MucH = 390; // khung Lão Mực góc màn (menu dựng dùng chung)
        const float MucNoteW = 560, MucPop = 0.3f;

        DealerRig mucNow;   // Lão Mực đang nói (góc màn hoặc trên sân khấu)
        bool mucCorner;     // đang hiện ở góc màn
        float mucEnd = -10; // lúc câu Lão Mực trước tắt: câu nối liền thì không trồi lại, không chào lại
        float mucPopT = 1;
        Color dim;          // màu dải chắn (ông đứng trên sân khấu thì dải trong suốt)
        bool dimKnown;

        readonly List<Req> queue = new List<Req>();
        Req cur;
        float shownT;
        bool visible;
        Rect hole; // lỗ theo toạ độ giữa area
        Rect lastRing;
        Rect screenHole;

        public bool Blocking => visible && cur != null && (cur.mode == Guide.Mode.Force || cur.mode == Guide.Mode.Say);
        public bool Idle => cur == null && queue.Count == 0;

        public bool Has(string id) => (cur != null && cur.id == id) || queue.Exists(q => q.id == id);

        Canvas canvas;

        void Awake()
        {
            I = this;
            canvas = area ? area.GetComponentInParent<Canvas>() : null;
            HideAll();
        }

        // Screen Space - Overlay: vẽ sau mọi camera, nằm trên mọi canvas của game (kể cả màn mở rương thứ tự 400). App.Awake gắn camera UI
        // cho mọi PokiCanvas con của nó (gồm canvas này), nên đổi lại ở Start.
        void Start()
        {
            if (!canvas) return;
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvas.sortingOrder = 500;
        }

        Camera AreaCam => canvas && canvas.renderMode != RenderMode.ScreenSpaceOverlay ? canvas.worldCamera : null;

        // camera vẽ chỗ cần khoanh (canvas gốc của nó); Overlay thì không camera
        static Camera CamOf(RectTransform t)
        {
            var c = t ? t.GetComponentInParent<Canvas>() : null;
            if (c) c = c.rootCanvas;
            if (!c || c.renderMode == RenderMode.ScreenSpaceOverlay) return null;
            return c.worldCamera ? c.worldCamera : PokiCanvas.UiCamera;
        }

        void OnDestroy()
        {
            if (I == this) I = null;
        }

        public bool Enqueue(Req r)
        {
            if (Has(r.id)) return true;
            r.scene = App.Router != null ? App.Router.Current : null;
            queue.Add(r);
            return true;
        }

        // hiện được ngay: không chờ chuyển scene, chỗ cần khoanh thấy được (lời tướng: không có hộp nào đang mở)
        bool ReadyNow(Req q)
        {
            if (Busy) return false;
            // lời tướng, ghi chú không gắn chỗ nào: chờ hết hộp thoại (không đè lên hộp lên cấp, hộp kết quả)
            if (string.IsNullOrEmpty(q.key)) return App.Modals == null || App.Modals.Count == 0;
            return Visible(TargetOf(q));
        }

        public void Cancel(string id)
        {
            queue.RemoveAll(q => q.id == id);
            if (cur != null && cur.id == id)
            {
                cur = null;
                HideAll();
            }
        }

        void HideAll()
        {
            visible = false;
            if (group)
            {
                group.alpha = 0;
                group.blocksRaycasts = false;
            }
            foreach (var b in blockers)
                if (b)
                    b.gameObject.SetActive(false);
            if (ring) ring.gameObject.SetActive(false);
            if (ringUnder) ringUnder.gameObject.SetActive(false);
            if (pencil) pencil.gameObject.SetActive(false);
            if (note) note.gameObject.SetActive(false);
            if (face) face.gameObject.SetActive(false);
            if (me) me.gameObject.SetActive(false);
            if (tapText) tapText.gameObject.SetActive(false);
            HideMuc();
        }

        void HideMuc()
        {
            if (mucNow)
            {
                mucEnd = Time.unscaledTime;
                mucNow.Stop();
            }
            mucNow = null;
            mucCorner = false;
            if (mucFrame) mucFrame.gameObject.SetActive(false);
            if (dimKnown)
                foreach (var b in blockers)
                    if (b)
                        b.color = dim;
        }

        // lời Lão Mực: chọn ai nói (trên sân khấu / góc màn), clip mở câu rồi talk lặp
        void OpenMuc(Req r)
        {
            if (r.hero != Guide.Muc) return;
            var stage = Guide.MucActor;
            if (stage && stage.isActiveAndEnabled && stage.Ready()) mucNow = stage;
            else if (muc && mucFrame)
            {
                mucFrame.gameObject.SetActive(true);
                if (muc.Ready())
                {
                    mucNow = muc;
                    mucCorner = true;
                }
                else mucFrame.gameObject.SetActive(false);
            }
            if (!mucNow) return;
            bool say = r.mode == Guide.Mode.Say;
            // ông đứng trên sân khấu: dải chắn trong suốt (vẫn nuốt chạm) để không tối chính người đang nói
            if (!mucCorner && say && string.IsNullOrEmpty(r.key) && blockers.Length > 0 && blockers[0])
            {
                if (!dimKnown)
                {
                    dim = blockers[0].color;
                    dimKnown = true;
                }
                foreach (var b in blockers) b.color = new Color(dim.r, dim.g, dim.b, 0);
            }
            if (mucCorner) note.Set(r.text, MucNoteW);
            bool chain = Time.unscaledTime - mucEnd < 0.35f;
            mucPopT = mucCorner && !chain ? 0 : 1;
            var a = mucNow;
            string clip = string.IsNullOrEmpty(r.clip) && say && !chain ? "greet" : r.clip;
            CasinoGuide.Mumble();
            if (clip == "react_win_big") App.Audio?.Play("mucBoing");
            if (!string.IsNullOrEmpty(clip) && a.Has(clip))
                a.Play(clip, () =>
                {
                    if (say && visible && mucNow == a) a.Loop("talk");
                });
            else if (say) a.Loop("talk");
        }

        static bool Busy => App.Booting || App.Covered || (App.Router != null && App.Router.Busy);

        RectTransform TargetOf(Req r) => string.IsNullOrEmpty(r.key) ? null : Guide.Target(r.key);

        // chỗ cần khoanh có thấy được không: đang hiện, có kích thước, không nằm dưới hộp thoại khác
        static bool Visible(RectTransform t)
        {
            if (!t || !t.gameObject.activeInHierarchy) return false;
            var r = LocalBounds(t);
            if (r.width < 2 || r.height < 2) return false;
            var top = App.Modals != null ? App.Modals.TopRoot : null;
            return top ? t.IsChildOf(top) : !InModal(t);
        }

        // khung của chỗ cần khoanh theo toạ độ của chính nó; gốc cỡ 0 (vd. bảng tên đảo ở sảnh: gốc là điểm neo, hình nằm ở con) thì lấy
        // khung bao các con đang hiện
        static Rect LocalBounds(RectTransform t)
        {
            var r = t.rect;
            if (r.width >= 8 && r.height >= 8) return r;
            var b = RectTransformUtility.CalculateRelativeRectTransformBounds(t);
            return Rect.MinMaxRect(b.min.x, b.min.y, b.max.x, b.max.y);
        }

        static bool InModal(RectTransform t)
        {
            for (var p = t.parent; p; p = p.parent)
                if (p.GetComponent<ModalSheet>())
                    return true;
            return false;
        }

        void Update()
        {
            // đã sang scene khác: bỏ các bước xin ở scene cũ
            if (!Busy && App.Router != null)
            {
                string scene = App.Router.Current;
                queue.RemoveAll(q => q.scene != null && q.scene != scene);
                if (cur != null && cur.scene != null && cur.scene != scene)
                {
                    cur = null;
                    HideAll();
                }
            }
            if (cur == null)
            {
                if (queue.Count == 0) return;
                cur = queue[0];
                queue.RemoveAt(0);
                shownT = 0;
                visible = false;
            }
            var r = cur;
            var t = TargetOf(r);
            bool needTarget = !string.IsNullOrEmpty(r.key);
            bool ok = !Busy;
            if (ok && needTarget && !Visible(t))
            {
                ok = false;
                // không thấy chỗ cần khoanh (chưa dựng, đã ẩn): đếm giờ, quá lâu thì bỏ bước. Bị hộp khác che thì chờ, không đếm.
                bool covered = t && t.gameObject.activeInHierarchy && App.Modals != null && App.Modals.Count > 0;
                if (!covered) r.missing += Time.unscaledDeltaTime;
                if (r.missing > (r.mode == Guide.Mode.Force ? MissingForce : MissingSoft))
                {
                    // bỏ khỏi hàng, không đánh dấu xong: màn gọi lại khi chỗ đó hiện (vd. vào lại sảnh)
                    Guide.Log(r.id, "bo_qua_khong_thay");
                    Finish(r, false, false);
                    return;
                }
            }
            if (ok && !needTarget && App.Modals != null && App.Modals.Count > 0) ok = false;
            if (!ok)
            {
                if (visible) HideAll();
                // bước đang chờ bị che (vd. chỗ trên màn nằm dưới hộp vừa mở): bước khác hiện được ngay (vd. nút trong hộp đó) lên trước
                int k = queue.FindIndex(ReadyNow);
                if (k >= 0)
                {
                    var nx = queue[k];
                    queue.RemoveAt(k);
                    queue.Insert(0, cur);
                    cur = nx;
                    shownT = 0;
                }
                return;
            }
            if (!visible) Open(r);
            shownT += Time.unscaledDeltaTime;
            Layout(r, t);
            Animate();
            Check(r);
        }

        void Open(Req r)
        {
            visible = true;
            shownT = 0;
            lastRing = default;
            Guide.Log(r.id, "hien");
            bool block = r.mode == Guide.Mode.Force || r.mode == Guide.Mode.Say;
            group.alpha = 1;
            group.blocksRaycasts = block;
            foreach (var b in blockers) b.gameObject.SetActive(block);
            // Say có chỗ khoanh (Guide.SayAt): vẽ vòng, và vòng (khung chữ nhật đúng bằng lỗ) chặn chạm để cú chạm "để qua" không bấm
            // xuống công trình, nút bên dưới; Force, Hint để chạm lọt qua lỗ
            bool sayAt = r.mode == Guide.Mode.Say && !string.IsNullOrEmpty(r.key);
            ring.gameObject.SetActive(r.mode == Guide.Mode.Force || r.mode == Guide.Mode.Hint || sayAt);
            ring.raycastTarget = sayAt;
            ring.Reveal = 0;
            if (ringUnder)
            {
                ringUnder.gameObject.SetActive(ring.gameObject.activeSelf);
                ringUnder.Reveal = 0;
            }
            pencil.gameObject.SetActive(r.mode == Guide.Mode.Force || r.mode == Guide.Mode.Hint);
            note.gameObject.SetActive(!string.IsNullOrEmpty(r.text));
            note.Set(r.text, NoteW);
            // lời nhân vật chính: chân dung cậu bé bên trái, tướng đồng hành (nếu đã chọn) nhỏ hơn bên phải
            bool byMe = r.mode == Guide.Mode.Say && r.hero == Guide.Me;
            bool meOn = byMe && me && me.sprite;
            string heroId = byMe ? App.Save?.Data?.starter : r.hero == Guide.Muc ? null : r.hero;
            var hero = r.mode == Guide.Mode.Say && !string.IsNullOrEmpty(heroId) ? App.Data.Hero(heroId) : null;
            if (me) me.gameObject.SetActive(meOn);
            face.gameObject.SetActive(hero != null);
            if (hero != null) face.Bind(hero, meOn ? 170 : 220);
            tapText.gameObject.SetActive(r.mode == Guide.Mode.Say);
            OpenMuc(r);
            App.Audio?.Play("open", 0.5f);
        }

        // lỗ theo toạ độ giữa area (gốc ở tâm area) từ bốn góc của chỗ cần khoanh
        bool HoleOf(RectTransform t, out Rect local, out Rect screen)
        {
            local = screen = default;
            if (!t) return false;
            var cam = CamOf(t);
            var areaCam = AreaCam;
            var lb = LocalBounds(t);
            var corners = new Vector3[]
            {
                t.TransformPoint(new Vector3(lb.xMin, lb.yMin)), t.TransformPoint(new Vector3(lb.xMin, lb.yMax)),
                t.TransformPoint(new Vector3(lb.xMax, lb.yMax)), t.TransformPoint(new Vector3(lb.xMax, lb.yMin)),
            };
            Vector2 smin = new Vector2(float.MaxValue, float.MaxValue), smax = new Vector2(float.MinValue, float.MinValue);
            Vector2 lmin = smin, lmax = smax;
            var c = area.rect.center;
            foreach (var w in corners)
            {
                var sp = RectTransformUtility.WorldToScreenPoint(cam, w);
                smin = Vector2.Min(smin, sp);
                smax = Vector2.Max(smax, sp);
                RectTransformUtility.ScreenPointToLocalPointInRectangle(area, sp, areaCam, out var lp);
                lp -= c;
                lmin = Vector2.Min(lmin, lp);
                lmax = Vector2.Max(lmax, lp);
            }
            local = Rect.MinMaxRect(lmin.x - Pad, lmin.y - Pad, lmax.x + Pad, lmax.y + Pad);
            screen = Rect.MinMaxRect(smin.x, smin.y, smax.x, smax.y);
            return true;
        }

        void Layout(Req r, RectTransform t)
        {
            var full = area.rect;
            float L = -full.width / 2, R = full.width / 2, B = -full.height / 2, T = full.height / 2;
            if (!HoleOf(t, out hole, out screenHole))
            {
                hole = new Rect(0, 0, 0, 0); // không lỗ: dải trên và dưới phủ kín
                screenHole = default;
            }
            // 4 dải chắn
            if (blockers[0].gameObject.activeSelf)
            {
                Place(blockers[0].rectTransform, Rect.MinMaxRect(L, Mathf.Min(hole.yMax, T), R, T));
                Place(blockers[1].rectTransform, Rect.MinMaxRect(L, B, R, Mathf.Max(hole.yMin, B)));
                Place(blockers[2].rectTransform, Rect.MinMaxRect(L, hole.yMin, Mathf.Max(hole.xMin, L), hole.yMax));
                Place(blockers[3].rectTransform, Rect.MinMaxRect(Mathf.Min(hole.xMax, R), hole.yMin, R, hole.yMax));
            }
            // vòng khoanh: elip quanh lỗ, dựng lại khi lỗ đổi
            if (ring.gameObject.activeSelf && hole.width > 0 && (Mathf.Abs(hole.x - lastRing.x) > 1.5f || Mathf.Abs(hole.y - lastRing.y) > 1.5f ||
                                                                 Mathf.Abs(hole.width - lastRing.width) > 1.5f || Mathf.Abs(hole.height - lastRing.height) > 1.5f))
            {
                lastRing = hole;
                var rt = ring.rectTransform;
                rt.anchoredPosition = hole.center;
                rt.sizeDelta = hole.size;
                float rx = hole.width / 2 + 10, ry = hole.height / 2 + 8;
                var pts = new Vector2[40];
                for (int i = 0; i < pts.Length; i++)
                {
                    // nét tay: bắt đầu lệch một chút, bán kính dao động nhẹ
                    float a = Mathf.PI * 0.62f + i * Mathf.PI * 2 / pts.Length;
                    float wob = 1 + 0.035f * Mathf.Sin(i * 1.7f);
                    pts[i] = new Vector2(Mathf.Cos(a) * rx * wob, Mathf.Sin(a) * ry * wob);
                }
                ring.Setup(pts, 8, 0, 0, true);
                if (ringUnder)
                {
                    var ur = ringUnder.rectTransform;
                    ur.anchoredPosition = rt.anchoredPosition;
                    ur.sizeDelta = rt.sizeDelta;
                    ringUnder.Setup(pts, 16, 0, 0, true);
                }
            }
            // bút chì (ảnh nằm ngang, ngòi bên trái, gốc ở ngòi): đặt ngòi ở góc trên phải của lỗ, chĩa chéo xuống vào lỗ; sát mép phải
            // thì lật sang góc trên trái. Nhún dọc hướng ngòi.
            bool flip = hole.xMax + pencil.rect.width * 0.8f > R;
            if (pencil.gameObject.activeSelf)
            {
                float bob = 8 * (0.5f + 0.5f * Mathf.Sin(Time.unscaledTime * 6f));
                var corner = new Vector2(flip ? hole.xMin : hole.xMax, hole.yMax);
                var dir = flip ? new Vector2(0.87f, -0.5f) : new Vector2(-0.87f, -0.5f); // hướng ngòi
                pencil.pivot = new Vector2(0.02f, 0.5f);
                pencil.anchoredPosition = corner - dir * (10 + bob);
                pencil.localScale = new Vector3(flip ? -1 : 1, 1, 1);
                pencil.localEulerAngles = new Vector3(0, 0, flip ? -30 : 30);
            }
            // Lão Mực góc màn: khung đứng trên mép dưới, bên trái (chỗ khoanh nằm dưới bên trái thì sang phải)
            bool mucLeft = true;
            if (mucCorner)
            {
                mucLeft = !(hole.width > 0 && hole.center.x < 0 && hole.yMin < B + MucH + 40);
                mucFrame.anchorMin = mucFrame.anchorMax = new Vector2(0.5f, 0.5f);
                mucFrame.pivot = new Vector2(0.5f, 0);
                mucFrame.sizeDelta = new Vector2(MucW, MucH);
                mucFrame.anchoredPosition = new Vector2(mucLeft ? L + MucW / 2 + 4 : R - MucW / 2 - 4, B);
            }
            // ghi chú: trên lỗ nếu lỗ ở nửa dưới, dưới lỗ nếu ở nửa trên; không lỗ thì giữa màn (lời tướng: lệch phải chừa chỗ chân dung)
            if (note.gameObject.activeSelf)
            {
                var nr = note.Rect;
                float h = Mathf.Max(80, nr.rect.height);
                float w = Mathf.Min(mucCorner ? MucNoteW : NoteW, full.width - Margin * 2);
                Vector2 pos;
                // nửa dưới: đặt dưới lỗ nếu còn chỗ (không đè thứ ngay trên nút, vd. hàng ô thưởng trên nút Máy bi), không thì trên lỗ
                bool roomBelow = hole.yMin - 60 - h > B + Margin + 40;
                bool meOn = me && me.gameObject.activeSelf, faceOn = face.gameObject.activeSelf;
                // Lão Mực: góc màn thì ghi chú cạnh đầu ông; trên sân khấu thì ghi chú thấp xuống (không che mặt ông)
                if (hole.width <= 0 && mucCorner)
                    pos = new Vector2(mucLeft ? L + MucW - 30 + w / 2 : R - MucW + 30 - w / 2, B + MucH * 0.72f);
                else if (hole.width <= 0 && mucNow) pos = new Vector2(0, B + full.height * 0.27f);
                else if (hole.width <= 0) pos = new Vector2(meOn && faceOn ? 0 : meOn || faceOn ? 80 : 0, 40);
                else if (hole.center.y < 0 && roomBelow && hole.height < full.height * 0.25f) pos = new Vector2(hole.center.x, hole.yMin - 50 - h / 2);
                else if (hole.center.y < 0) pos = new Vector2(hole.center.x, hole.yMax + 60 + h / 2);
                else pos = new Vector2(hole.center.x, hole.yMin - 60 - h / 2);
                pos.x = Mathf.Clamp(pos.x, L + Margin + w / 2, R - Margin - w / 2);
                pos.y = Mathf.Clamp(pos.y, B + Margin + h / 2, T - Margin - h / 2);
                nr.anchorMin = nr.anchorMax = nr.pivot = new Vector2(0.5f, 0.5f);
                nr.anchoredPosition = pos;
                if (meOn)
                {
                    var mr = me.rectTransform;
                    mr.anchorMin = mr.anchorMax = mr.pivot = new Vector2(0.5f, 0.5f);
                    mr.anchoredPosition = new Vector2(pos.x - w / 2 - 50, pos.y + 40);
                }
                if (faceOn)
                {
                    face.Rect.anchorMin = face.Rect.anchorMax = new Vector2(0.5f, 0.5f);
                    face.Rect.anchoredPosition = meOn ? new Vector2(pos.x + w / 2 + 30, pos.y + 10) : new Vector2(pos.x - w / 2 - 40, pos.y + 20);
                }
                if (tapText.gameObject.activeSelf)
                {
                    var tr = tapText.rectTransform;
                    tr.anchorMin = tr.anchorMax = tr.pivot = new Vector2(0.5f, 0.5f);
                    tr.anchoredPosition = new Vector2(pos.x, pos.y - h / 2 - 48);
                }
            }
        }

        static void Place(RectTransform rt, Rect r)
        {
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = r.center;
            rt.sizeDelta = new Vector2(Mathf.Max(0, r.width), Mathf.Max(0, r.height));
        }

        void Animate()
        {
            if (ring.gameObject.activeSelf) ring.Reveal = Mathf.Clamp01(shownT / 0.4f);
            if (ringUnder && ringUnder.gameObject.activeSelf) ringUnder.Reveal = ring.Reveal;
            // ghi chú bật ra nhẹ lúc hiện
            float k = Mathf.Clamp01(shownT / 0.22f);
            float s = Mathf.Lerp(0.85f, 1, 1 - Mathf.Pow(1 - k, 3)) + Mathf.Sin(k * Mathf.PI) * 0.05f;
            note.Rect.localScale = new Vector3(s, s, 1);
            if (tapText.gameObject.activeSelf) tapText.alpha = 0.55f + 0.45f * Mathf.Sin(Time.unscaledTime * 3f);
            // Lão Mực trồi lên từ mép dưới, nảy nhẹ
            if (mucCorner && mucSlide)
            {
                mucPopT = Mathf.Min(1, mucPopT + Time.unscaledDeltaTime / MucPop);
                const float c1 = 1.4f, c3 = c1 + 1;
                float x = mucPopT - 1;
                float e = 1 + c3 * x * x * x + c1 * x * x;
                mucSlide.anchoredPosition = new Vector2(0, Mathf.LerpUnclamped(-MucH, 0, e));
            }
        }

        void Check(Req r)
        {
            var p = Pointer.current;
            bool released = p != null && p.press.wasReleasedThisFrame;
            Vector2 pos = released ? p.position.ReadValue() : default;
            bool inHole = released && screenHole.width > 0 && Expand(screenHole, 12).Contains(pos);
            switch (r.mode)
            {
                case Guide.Mode.Force:
                    if (inHole && shownT > 0.15f) Finish(r, !r.repeat);
                    break;
                case Guide.Mode.Hint:
                    if (inHole || shownT > (r.secs > 0 ? r.secs : 7)) Finish(r, !r.repeat);
                    break;
                case Guide.Mode.Note:
                    if (shownT > (r.secs > 0 ? r.secs : 3.4f) || (released && shownT > 0.6f)) Finish(r, !r.repeat);
                    break;
                case Guide.Mode.Say:
                    if (released && shownT > 0.35f) Finish(r, !r.repeat);
                    break;
            }
        }

        static Rect Expand(Rect r, float k) => Rect.MinMaxRect(r.xMin - k, r.yMin - k, r.xMax + k, r.yMax + k);

#if UNITY_EDITOR
        // tour thử (menu "PokiClash/Thử/Hướng dẫn: người chơi mới…"): bước đang hiện, và chạm giả đúng chỗ khoanh
        public string ShownId => visible && cur != null ? cur.id : null;
        public Guide.Mode ShownMode => cur != null ? cur.mode : Guide.Mode.Note;

        public string DebugState =>
            $"đang: {(cur != null ? $"{cur.id} ({(visible ? "hiện" : "chờ")}, khoá {cur.key}, thiếu {cur.missing:0.0}s)" : "-")}; hàng: " +
            string.Join(", ", queue.ConvertAll(q => q.id));

        public void DebugTap()
        {
            if (!visible || cur == null) return;
            var r = cur;
            var t = TargetOf(r);
            if (t && (r.mode == Guide.Mode.Force || r.mode == Guide.Mode.Hint))
            {
                var es = UnityEngine.EventSystems.EventSystem.current;
                var ev = new UnityEngine.EventSystems.PointerEventData(es) { button = UnityEngine.EventSystems.PointerEventData.InputButton.Left };
                var go = t.gameObject;
                var down = go.GetComponentInChildren<UnityEngine.EventSystems.IPointerDownHandler>(false) as Component;
                var click = go.GetComponentInChildren<UnityEngine.EventSystems.IPointerClickHandler>(false) as Component;
                if (down) UnityEngine.EventSystems.ExecuteEvents.Execute(down.gameObject, ev, UnityEngine.EventSystems.ExecuteEvents.pointerDownHandler);
                if (down) UnityEngine.EventSystems.ExecuteEvents.Execute(down.gameObject, ev, UnityEngine.EventSystems.ExecuteEvents.pointerUpHandler);
                if (click) UnityEngine.EventSystems.ExecuteEvents.Execute(click.gameObject, ev, UnityEngine.EventSystems.ExecuteEvents.pointerClickHandler);
            }
            if (cur == r) Finish(r, !r.repeat);
        }
#endif

        void Finish(Req r, bool mark, bool invoke = true)
        {
            if (mark && App.Save?.Data != null)
            {
                Tutorial.Mark(App.Save.Data, r.id);
                App.Save.Save();
            }
            if (invoke) Guide.Log(r.id, "xong");
            cur = null;
            HideAll();
            if (invoke) r.done?.Invoke();
        }
    }
}
