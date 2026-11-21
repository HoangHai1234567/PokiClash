// Chuyến tàu qua mây (người dùng 2026-11-19): chuyển giữa sảnh (bến cạnh đảo Thủy) và Nhà (bến mép dưới đảo), và màn tải lúc mở game.
// Người dùng dặn "phải nối nhau như trong cùng 1 thế giới, không phải kiểu fade": mọi thứ nằm trên một dải thế giới dọc theo hướng đi,
// camera bám theo tàu:
//   [ảnh chụp màn cũ] → [dải mây trên biển] → [ảnh chụp màn mới]
// - Đi: tàu rời bến trong màn cũ (PierShip.Depart); lớp này chụp màn cũ (ẩn tàu và giao diện cố định của màn: SceneRoot.Chrome) làm
//   nền đúng chỗ, nhận tàu, camera theo tàu đi lên (Nhà) / xuống (sảnh): màn cũ trôi khỏi màn hình, mây phủ mép màn cũ khép vào từ
//   hai bên, rồi dải mây: đi tới đâu mây toả ra quanh tàu rồi khép lại sau đuôi tới đó.
// - Tới: màn mới nạp dưới lớp này; camera màn mới đặt chỗ đậu ở giữa, tàu của màn đặt ở điểm vào bến (ẩn), chụp lại. Ảnh màn mới
//   đặt tiếp sau dải mây, tàu đi đường cong vào đúng điểm vào bến, camera dừng đúng lúc ảnh màn mới vào chỗ; mây phủ mép màn mới
//   dạt ra hai bên trên màn thật sau khi camera dừng. Lớp này tắt (màn thật y như ảnh), tàu của màn chạy nốt vào bến
//   (PierShip.Arrive), giao diện cố định hiện lại.
// - Mây vành rời của màn (CloudRing: sảnh) không nằm trong ảnh chụp: lớp này mang từng đám sang dải thế giới đúng chỗ, đúng độ toả,
//   để chúng tiếp tục toả quanh tàu; lúc tới thì trả độ toả về mây của màn mới.
// - Màn tải (App gọi BeginBoot khi mở thẳng vào sảnh): biển mở, tàu đi lên, logo, thanh tải, mẹo. Tải xong (đủ 2,4 giây) thì dải mây
//   hiện ra phía trước, tàu đi qua rồi tới bến sảnh như trên.
// Theo giờ (DayCycle, như sảnh, đảo; người dùng 2026-11-19 "mây và thời tiết ở loading cũng phải đổi theo giờ"): lớp nhuộm
// (day_multiply) và tia nắng (day_rays) phủ biển, dưới ảnh chụp màn (ảnh đã nhuộm sẵn); biển tối thêm về đêm (DayCycle.SeaNight);
// mây nhân CloudTint × màu cảnh như mây sảnh; tàu nhân màu cảnh, đêm thắp đèn lồng.
// Canvas riêng thứ tự 9 (dưới thanh trên 10: thanh trên đứng yên như giao diện, thế giới trôi); màn tải 15 (che thanh trên).
// SceneRouter dùng lớp này thay màn mây CloudCover khi Takes(cũ, mới) đúng. Không sinh GameObject lúc chạy: mây, sóng, bọt là ảnh dựng
// sẵn trong prefab (menu "PokiClash/Prefab/Bến tàu: tàu sảnh, chuyến tàu qua mây, màn tải", Editor/ShipBuild.cs).
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using TMPro;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ShipVoyage : MonoBehaviour, ISceneCover
    {
        const float Cruise = 1450; // tốc độ tàu trong dải mây (đơn vị/giây)
        const float BootSpeed = 460; // màn tải: đi chậm trên biển
        const float Accel = 1100, Decel = 1250;
        const float CamLead = 0.2f; // camera đi trước tàu 0,2 chiều cao màn
        const float Overlap = 0.3f; // dải mây phủ lên mép ảnh màn cũ / mới 0,3 chiều cao màn
        const float MinCruise = 0.35f;
        const float BootMin = 2.4f;
        const int OrderVoyage = 9, OrderBoot = 15;

        static readonly string[] Tips =
        {
            "Thủy khắc Hỏa, Hỏa khắc Kim, Kim khắc Mộc, Mộc khắc Thổ, Thổ khắc Thủy.",
            "Đánh vào hệ mình khắc: sát thương ×1,5. Bị khắc thì chỉ còn ×0,75.",
            "Mỗi lượt chọn 5 lần, mỗi lần 1 trong 3 thẻ.",
            "Chiêu và Tuyệt kỹ không tốn lần chọn, chỉ tốn mana và nộ.",
            "Ải đã qua tự đánh ra bi khi bạn vắng mặt.",
            "Cấp người chơi cũng là cấp của mọi tướng.",
            "Bấm vào con tàu ở bến để về Nhà.",
        };

        [SerializeField] PokiCanvas view;
        [SerializeField] RectTransform area; // phủ kín màn (Nen của canvas)
        [SerializeField] Image blocker;
        [SerializeField] RectTransform sea; // ảnh biển lát (Tiled), trôi theo camera
        [SerializeField] Image[] waves = new Image[0];
        [SerializeField] Image tint; // lớp nhuộm theo giờ (day_multiply), trên biển, dưới ảnh chụp màn
        [SerializeField] RawImage rays; // tia nắng (day_rays)
        [SerializeField] RawImage oldShot, newShot; // ảnh chụp màn cũ / mới, cỡ bằng màn
        [SerializeField] ShipLook look;
        [SerializeField] Image[] clouds = new Image[0];
        [SerializeField] Image[] carry = new Image[0]; // mây vành của màn mang sang dải (CloudRing)
        [SerializeField] float holeRadius = 290;
        [Header("Màn tải")]
        [SerializeField] CanvasGroup bootUi;
        [SerializeField] RectTransform logo;
        [SerializeField] Image barFill;
        [SerializeField] RectTransform barPencil;
        [SerializeField] TextMeshProUGUI pct, tip;

        public static ShipVoyage I { get; private set; }
        public static bool Booting => I && I.booting;

        public bool Closed { get; private set; }

        int dir = 1; // 1: đi lên (bắc), -1: đi xuống
        // toạ độ dải thế giới: x ngang (như màn), q dọc theo hướng đi; màn hình y = dir * (q - qc)
        float qc, closedAt; // camera
        Vector2 sp, sv; // tàu (x, q), vận tốc
        float speed, targetSpeed, followX;
        bool follow, arriving, running, booting, loaded;
        float bandA = float.PositiveInfinity, bandB = float.PositiveInfinity, kA = 1, kB = 1; // dải mây [A, B]; độ khép mây ở hai mép
        float qNew = float.PositiveInfinity; // tâm ảnh màn mới
        RenderTexture rtOld, rtNew;
        readonly List<Vector2> arc = new List<Vector2>();
        readonly List<float> arcAcc = new List<float>();
        float arcLen, arcS, arcQc0, camAt = 1, vEnd;
        float bootT0, tipT;
        int tipIdx;
        Vector2 lastSize, logoPos;
        Vector2[] cBase, cOff, wBase;
        float[] cW, wPhase;
        float period, wSpan;
        float[] cJit;
        bool seaOn;
        // mây mang: vị trí gốc (x, q), độ toả, chỉ số trong CloudRing của màn mới (-1: mây màn cũ)
        Vector2[] kBase, kOff;
        int[] kRing;
        int kCount, kArr;
        CloudRing ringNew;

        // Dùng khi dựng prefab (Editor).
        public void Setup(PokiCanvas canvas, RectTransform areaRt, Image block, RectTransform seaRt, Image[] waveImgs, Image tintImg,
            RawImage raysImg, RawImage oldImg,
            RawImage newImg, ShipLook ship, Image[] cloudImgs, Image[] carryImgs, CanvasGroup boot, RectTransform logoRt, Image fill,
            RectTransform pencil, TextMeshProUGUI pctText, TextMeshProUGUI tipText)
        {
            carry = carryImgs;
            view = canvas;
            area = areaRt;
            blocker = block;
            sea = seaRt;
            waves = waveImgs;
            tint = tintImg;
            rays = raysImg;
            oldShot = oldImg;
            newShot = newImg;
            look = ship;
            clouds = cloudImgs;
            bootUi = boot;
            logo = logoRt;
            barFill = fill;
            barPencil = pencil;
            pct = pctText;
            tip = tipText;
        }

        void Awake()
        {
            I = this;
            logoPos = logo ? logo.anchoredPosition : Vector2.zero;
            Hide();
        }

        void OnDestroy()
        {
            if (I == this) I = null;
            Release();
        }

        Vector2 Size
        {
            get
            {
                var s = area.rect.size;
                return s.x > 1 ? s : new Vector2(PokiCanvas.RefW, PokiCanvas.RefH);
            }
        }

        float H => Size.y;

        // ---------- SceneRouter ----------

        // chuyến này có đi tàu không (và hướng đi)
        public bool Takes(string from, string to)
        {
            if (booting && to == SceneIds.Hub)
            {
                dir = 1;
                return true;
            }
            if (from == SceneIds.Hub && to == SceneIds.Home)
            {
                dir = 1;
                return true;
            }
            if (from == SceneIds.Home && to == SceneIds.Hub)
            {
                dir = -1;
                return true;
            }
            return false;
        }

        public void Block(bool on)
        {
            if (blocker) blocker.raycastTarget = on;
        }

        void Show(int order)
        {
            running = true;
            gameObject.SetActive(true);
            if (view && view.Canvas) view.Canvas.sortingOrder = order;
            Block(true);
        }

        void Hide()
        {
            running = false;
            Closed = false;
            follow = arriving = false;
            if (look) look.Show(false);
            if (bootUi) bootUi.alpha = 0;
            Release();
            gameObject.SetActive(false);
        }

        void Release()
        {
            foreach (var rt in new[] { rtOld, rtNew })
                if (rt)
                {
                    rt.Release();
                    Destroy(rt);
                }
            rtOld = rtNew = null;
            if (oldShot) oldShot.texture = null;
            if (newShot) newShot.texture = null;
        }

        void Restart()
        {
            seaOn = false;
            kCount = 0;
            followX = 0;
            ringNew = null;
            foreach (var c in carry)
                if (c) c.gameObject.SetActive(false);
            qc = 0;
            follow = arriving = false;
            bandA = bandB = qNew = float.PositiveInfinity;
            kA = kB = 1;
            sv = Vector2.zero;
            Release();
            if (look) look.Show(false);
            if (bootUi) bootUi.alpha = 0;
        }

        // rời màn cũ: tàu rời bến, chụp màn cũ làm nền, camera theo tàu; trả về khi màn cũ gỡ được
        public IEnumerator Close()
        {
            if (Closed)
            {
                Block(true);
                yield break;
            }
            Show(OrderVoyage);
            Restart();
            Daylight();
            Layout(0);
            bool north = dir > 0;
            var root = App.Router ? App.Router.CurrentRoot : null;
            if (root) root.Chrome(false, true);
            var from = PierShip.Active;
            if (from && from.isActiveAndEnabled && from.Has(north))
            {
                if (from.Glide != null) yield return from.Glide(from.FocusFor(north));
                yield return from.Depart(north, 0.55f);
                float rootRatio = from.Look.transform.lossyScale.x / Mathf.Max(1e-5f, look.transform.lossyScale.x);
                look.Size = from.ShipRect.lossyScale.x / Mathf.Max(1e-5f, look.transform.lossyScale.x);
                var s = Local(from.ShipRect.position);
                sp = new Vector2(s.x, dir * s.y + qc);
                var h = from.Look.Heading;
                speed = from.CurrentSpeed * rootRatio;
                sv = new Vector2(h.x, dir * h.y) * speed;
                look.Face(h, true);
                from.Look.Show(false);
            }
            else
            {
                // màn cũ không có bến: tàu từ mép sau màn chạy vào
                yield return new WaitForSecondsRealtime(0.25f);
                sp = new Vector2(0, qc - H / 2 - 180);
                speed = 600;
                sv = new Vector2(0, speed);
                look.Size = 1;
                look.Face(new Vector2(0, dir), true);
            }
            if (root) root.Chrome(false, false);
            var ringOld = CloudRing.Active;
            if (ringOld && root && ringOld.gameObject.scene != root.gameObject.scene) ringOld = null;
            if (ringOld)
            {
                Carry(ringOld, 0, false);
                ringOld.Show(false);
            }
            rtOld = Snap();
            if (oldShot) oldShot.texture = rtOld;
            seaOn = true;
            look.Pos = Screen_(sp);
            look.Show(true);
            followX = sp.x; // giữ hướng ngang: đi thẳng dọc biển ngoài rìa đảo, không đè lên đảo của màn cũ
            bandA = H / 2 - Overlap * H;
            kA = 0;
            follow = true;
            targetSpeed = Cruise;
            Layout(0);
            App.Audio?.Play("whoosh");
            const float T = 0.75f;
            for (float t = 0; t < T; t += Dt)
            {
                kA = Smooth(t / T);
                look.Size = Mathf.Lerp(look.Size, 1.1f, 1 - Mathf.Exp(-3 * Dt));
                yield return null;
            }
            kA = 1;
            Closed = true;
            closedAt = Time.unscaledTime;
        }

        // tới màn mới: chụp màn mới (đã đặt camera, tàu của màn ẩn ở điểm vào bến), nối sau dải mây, tàu đi vào; tắt lớp, tàu cập bến
        public IEnumerator Open()
        {
            if (booting) yield return BootEnd();
            else
                while (Time.unscaledTime - closedAt < MinCruise)
                    yield return null;
            bool fromNorth = dir < 0;
            var to = PierShip.Active;
            var root = App.Router ? App.Router.CurrentRoot : null;
            if (root) root.Chrome(false, false);
            bool pier = to && to.isActiveAndEnabled && to.Has(fromNorth);
            Vector2 E, T;
            float rootRatio = 1, sizeTo = 1.1f;
            if (pier)
            {
                to.Park();
                to.Frame?.Invoke(to.FocusFor(fromNorth), World(Vector2.zero)); // giữa chỗ đậu và điểm vào bến ra giữa màn (camera tự kẹp)
                to.HoldAtExit(fromNorth);
                // chờ camera, bố cục màn mới đứng yên rồi mới chụp
                for (int f = 0; f < 3; f++) yield return null;
                yield return new WaitForSecondsRealtime(0.12f);
                E = Local(to.ExitWorld(fromNorth));
                T = to.EntryDir(fromNorth);
                if (T.sqrMagnitude < 1e-4f) T = new Vector2(0, dir);
                rootRatio = to.Look.transform.lossyScale.x / Mathf.Max(1e-5f, look.transform.lossyScale.x);
                sizeTo = to.ShipRect.lossyScale.x / Mathf.Max(1e-5f, look.transform.lossyScale.x);
            }
            else
            {
                yield return null;
                E = new Vector2(0, dir * (H / 2 + 320)); // màn mới không có bến: tàu đi khuất phía trước
                T = new Vector2(0, dir);
            }
            ringNew = CloudRing.Active;
            if (ringNew && root && ringNew.gameObject.scene != root.gameObject.scene) ringNew = null;
            kArr = kCount;
            if (ringNew)
            {
                Carry(ringNew, 0, true); // q tương đối, cộng qNew khi biết
                ringNew.Show(false);
            }
            rtNew = Snap();
            if (newShot) newShot.texture = rtNew;
            // còn trong mây: dạt ngang tới đúng hàng của điểm vào bến, rồi xuôi thẳng vào (không cắt ngang đảo của màn mới)
            followX = E.x;
            for (float t = 0; t < 1.1f && Mathf.Abs(sp.x - E.x) > 24; t += Dt) yield return null;
            // ảnh màn mới: mép gần phải ở xa ngoài màn, dải mây đủ dài, tàu đủ đường để hãm
            qNew = Mathf.Max(qc + 1.45f * H, (float.IsInfinity(bandA) ? qc : bandA) + 1.6f * H, sp.y + 1.25f * H - dir * E.y);
            for (int k = kArr; k < kCount; k++) kBase[k].y += qNew;
            bandB = qNew - H / 2 + Overlap * H;
            kB = 1;
            var ew = new Vector2(E.x, qNew + dir * E.y);
            var tw = new Vector2(T.x, dir * T.y).normalized;
            BuildArc(sp, sv.sqrMagnitude > 1 ? sv.normalized : Vector2.up, ew, tw);
            vEnd = pier ? to.Speed * rootRatio * 0.9f : Cruise * 0.6f;
            arcQc0 = qc;
            arcS = 0;
            camAt = pier ? 1 : 0.8f;
            targetSpeed = Cruise;
            follow = false;
            arriving = true;
            float size0 = look.Size;
            while (arcS < arcLen - 0.5f)
            {
                look.Size = Mathf.Lerp(size0, sizeTo, Smooth(arcS / arcLen));
                yield return null;
            }
            qc = qNew;
            arriving = false;
            Layout(0);
            // camera đã dừng, ảnh màn mới đúng chỗ: trả mây vành, tắt ảnh chụp và biển (màn thật y như ảnh), tàu của màn chạy tiếp;
            // mây dải phủ mép màn mới dạt ra hai bên trên màn thật
            HandBack();
            Release();
            seaOn = false;
            Coroutine dock = null;
            if (pier)
            {
                look.Show(false);
                to.Look.Show(true);
                dock = to.StartCoroutine(to.Arrive(fromNorth, vEnd / Mathf.Max(0.01f, rootRatio)));
            }
            else look.Show(false);
            Layout(0);
            for (float t = 0; t < 0.5f; t += Dt)
            {
                kB = 1 - Smooth(t / 0.5f);
                yield return null;
            }
            kB = 0;
            Hide();
            if (dock != null)
                while (to && to.Busy)
                    yield return null;
            if (root) root.Chrome(true, true);
            booting = false;
        }

        // ---------- màn tải ----------

        // mở game thẳng vào sảnh: che màn bằng biển có tàu đi lên, logo, thanh tải (App gọi trước Router.Go(Hub))
        public void BeginBoot()
        {
            booting = true;
            loaded = false;
            Show(OrderBoot);
            dir = 1;
            Restart();
            seaOn = true;
            sp = new Vector2(0, -H * 0.16f);
            speed = targetSpeed = BootSpeed;
            sv = new Vector2(0, speed);
            follow = true;
            look.Size = 1.1f;
            look.Pos = Screen_(sp);
            look.Face(Vector2.up, true);
            look.Show(true);
            bootT0 = Time.unscaledTime;
            tipIdx = Random.Range(0, Tips.Length);
            ShowTip();
            if (bootUi) bootUi.alpha = 1;
            SetBar(0);
            Closed = true;
            closedAt = Time.unscaledTime;
            Daylight(); // nhuộm theo giờ ngay khung đầu
            Layout(0);
        }

        IEnumerator BootEnd()
        {
            loaded = true;
            while (Time.unscaledTime - bootT0 < BootMin) yield return null;
            SetBar(1);
            yield return new WaitForSecondsRealtime(0.2f);
            // dải mây hiện ra ngay trước mặt, tàu tăng tốc đi vào
            bandA = qc + H / 2 + 40;
            kA = 1;
            targetSpeed = Cruise;
            App.Audio?.Play("whoosh");
            for (float t = 0; t < 0.4f; t += Dt)
            {
                if (bootUi) bootUi.alpha = 1 - Smooth(t / 0.4f);
                yield return null;
            }
            if (bootUi) bootUi.alpha = 0;
            if (view && view.Canvas) view.Canvas.sortingOrder = OrderVoyage; // thanh trên của sảnh hiện trên mây
        }

        void SetBar(float v)
        {
            if (!barFill) return;
            v = Mathf.Clamp01(v);
            barFill.fillAmount = v;
            if (barPencil)
            {
                float w = barFill.rectTransform.rect.width;
                var pp = barPencil.anchoredPosition;
                barPencil.anchoredPosition = new Vector2(-w / 2 + w * v + 18, pp.y);
            }
            if (pct) pct.text = $"{Mathf.RoundToInt(v * 100)}%";
        }

        void ShowTip()
        {
            if (!tip) return;
            tip.text = Loc.F("<color=#b8382a><b>Mẹo:</b></color> {0}", Loc.T(NextTip()));
            tipIdx++;
        }

        // người mới chỉ thấy câu về vòng chơi; các câu khác hiện khi đã học tới phần đó (GD_Claude/25_FTUE.md bước A1, mục 6)
        string NextTip()
        {
            var s = App.Save?.Data;
            if (s == null || Tutorial.IsLegacy(s)) return Tips[tipIdx % Tips.Length];
            if (!Tutorial.CoreDone(s)) return "Thắng ải lấy bi, thả bi vào máy để mạnh lên.";
            for (int k = 0; k < Tips.Length; k++)
            {
                int i = (tipIdx + k) % Tips.Length;
                if (TipOpen(s, i))
                {
                    tipIdx += k;
                    return Tips[i];
                }
            }
            return "Thắng ải lấy bi, thả bi vào máy để mạnh lên.";
        }

        // thứ tự như Tips: khắc hệ ×2, lượt đánh, chiêu và tuyệt kỹ, AFK, cấp chung, tàu về Nhà
        static bool TipOpen(SaveData s, int i)
        {
            switch (i)
            {
                case 0:
                case 1: return Tutorial.Done(s, Tutorial.Counter);
                case 2: return Tutorial.Done(s, Tutorial.RunQueue);
                case 3: return Tutorial.Done(s, Tutorial.Ult);
                case 4: return Tutorial.Done(s, Tutorial.AfkBtn);
                case 5: return Tutorial.Done(s, Tutorial.Exp);
                case 6: return Home.Open(s, GameData.Current.Cfg);
                default: return true;
            }
        }

        // ---------- mỗi khung ----------

        static float Dt => Mathf.Min(Time.unscaledDeltaTime, 0.05f);

        // màu theo giờ: biển, nhuộm, nắng, mây, tàu (gọi mỗi khung; giờ đổi chậm nên rẻ)
        void Daylight()
        {
            float hr = DayCycle.Hour, night = DayCycle.Night(hr), sun = DayCycle.Sun(hr), dusk = DayCycle.Dusk(hr) * (1 - night);
            var tintC = DayCycle.Tint(hr);
            if (sea)
            {
                var img = sea.GetComponent<Image>();
                if (img) img.color = Color.Lerp(Color.white, DayCycle.SeaNight, night);
            }
            if (tint)
            {
                bool on = seaOn && (tintC.r < 0.995f || tintC.g < 0.995f || tintC.b < 0.995f);
                if (tint.enabled != on) tint.enabled = on;
                if (on) tint.color = tintC;
            }
            if (rays)
            {
                float k = Mathf.Max(sun, dusk * 0.3f);
                bool on = seaOn && k > 0.01f;
                if (rays.enabled != on) rays.enabled = on;
                if (on)
                {
                    rays.color = new Color(1, Mathf.Lerp(1, 0.66f, dusk), Mathf.Lerp(1, 0.42f, dusk), k);
                    // dải nắng cố định trong thế giới: trôi theo camera
                    rays.uvRect = new Rect(0, dir * qc / Mathf.Max(1, H), 1, 1);
                }
            }
            var ct = DayCycle.CloudTint(hr) * tintC;
            foreach (var c in clouds)
                if (c && c.gameObject.activeSelf) c.color = new Color(ct.r, ct.g, ct.b, 1);
            for (int k = 0; k < kCount; k++) carry[k].color = new Color(ct.r, ct.g, ct.b, 1);
            if (look)
            {
                look.SetTint(tintC);
                look.Night(night);
            }
            waveTint = tintC;
        }

        Color waveTint = Color.white;

        void Update()
        {
            if (!running) return;
            float dt = Dt;
            if (dt <= 0) return;
            Daylight();
            var prev = sp;
            float prevQc = qc;
            if (follow)
            {
                // tàu đi thẳng theo hướng đi, dạt dần vào giữa; camera theo sau, không lùi
                speed = Mathf.MoveTowards(speed, targetSpeed, Accel * dt);
                sp = new Vector2(Mathf.Lerp(sp.x, followX, 1 - Mathf.Exp(-1.6f * dt)), sp.y + speed * dt);
                float want = sp.y + CamLead * H;
                qc = Mathf.Max(qc, Mathf.Lerp(qc, want, 1 - Mathf.Exp(-2.6f * dt)));
            }
            else if (arriving)
            {
                // theo đường cong vào bến: hãm để tới nơi đúng tốc độ vào bến; camera tới đích cùng lúc tàu tới điểm vào bến
                float vmax = Mathf.Sqrt(vEnd * vEnd + 2 * Decel * Mathf.Max(0, arcLen - arcS));
                speed = Mathf.Max(vEnd * 0.6f, Mathf.Min(Mathf.MoveTowards(speed, targetSpeed, Accel * dt), vmax));
                arcS = Mathf.Min(arcLen, arcS + speed * dt);
                sp = ArcAt(arcS);
                qc = Mathf.Lerp(arcQc0, qNew, Mathf.Clamp01(arcS / (arcLen * camAt)));
            }
            sv = (sp - prev) / dt;
            float camV = (qc - prevQc) / dt;
            look.Pos = Screen_(sp);
            var vs = new Vector2(sv.x, dir * sv.y);
            if (vs.sqrMagnitude > 30 * 30) look.Face(vs);
            look.Flow = new Vector2(0, -dir * camV); // bọt nằm trong thế giới
            look.Tick(dt, sv.magnitude);
            Layout(dt);
            if (booting && bootUi && bootUi.alpha > 0)
            {
                float e = Time.unscaledTime - bootT0;
                SetBar(loaded ? Mathf.Min(1, e / BootMin) : Mathf.Min(0.9f, e / BootMin));
                tipT += dt;
                if (tipT > 2.6f)
                {
                    tipT = 0;
                    ShowTip();
                }
                if (logo) logo.anchoredPosition = logoPos + new Vector2(0, Mathf.Sin(e * 1.6f) * 6);
            }
        }

        void Build(Vector2 size)
        {
            lastSize = size;
            int n = clouds.Length;
            const int cols = 6;
            int rows = Mathf.Max(1, Mathf.CeilToInt(n / (float)cols));
            float margin = 260;
            float dx = (size.x + margin * 2) / cols, dy = (size.y + margin * 2) / rows;
            period = rows * dy;
            cBase = new Vector2[n];
            cOff = new Vector2[n];
            cW = new float[n];
            cJit = new float[n];
            var rng = new System.Random(19);
            for (int i = 0; i < n; i++)
            {
                int r = i / cols, c = i % cols;
                float x = -size.x / 2 - margin + (c + 0.5f + (r % 2 == 0 ? -0.25f : 0.25f)) * dx + (float)(rng.NextDouble() - 0.5) * dx * 0.35f;
                float q = (r + 0.5f) * dy + (float)(rng.NextDouble() - 0.5) * dy * 0.4f;
                cBase[i] = new Vector2(x, q);
                cW[i] = dx * (1.9f + (float)rng.NextDouble() * 0.5f);
                cJit[i] = ((float)rng.NextDouble() - 0.5f) * 0.32f * size.y; // mép dải so le, không thẳng như bức tường
                var crt = clouds[i].rectTransform;
                float aspect = clouds[i].sprite ? clouds[i].sprite.rect.height / clouds[i].sprite.rect.width : 0.5f;
                crt.sizeDelta = new Vector2(cW[i], cW[i] * aspect);
                crt.localScale = new Vector3(rng.NextDouble() < 0.5 ? -1 : 1, 1, 1);
            }
            int m = waves.Length;
            wBase = new Vector2[m];
            wPhase = new float[m];
            wSpan = size.y + 240;
            for (int i = 0; i < m; i++)
            {
                wBase[i] = new Vector2((float)(rng.NextDouble() - 0.5) * (size.x + 100), (float)rng.NextDouble() * wSpan);
                wPhase[i] = (float)rng.NextDouble() * 10;
                waves[i].rectTransform.localScale = new Vector3(rng.NextDouble() < 0.5 ? -1 : 1, 1, 1);
            }
            if (sea) sea.sizeDelta = new Vector2(size.x + 1024, size.y + 1024);
            foreach (var shot in new[] { oldShot, newShot })
                if (shot) shot.rectTransform.sizeDelta = size;
        }

        // vị trí lặp gần camera của một vật cố định trong thế giới (chu kỳ p)
        float Near(float q, float p) => qc + Mathf.Repeat(q - qc + p / 2, p) - p / 2;

        // biển, sóng, ảnh màn cũ / mới, mây theo camera; mây ở mép ảnh khép / dạt theo kA / kB, toả quanh tàu
        void Layout(float dt)
        {
            var size = Size;
            if (cBase == null || size != lastSize) Build(size);
            float h = size.y;
            if (sea)
            {
                if (sea.gameObject.activeSelf != seaOn) sea.gameObject.SetActive(seaOn);
                sea.anchoredPosition = new Vector2(0, dir * (256 - Mathf.Repeat(qc, 512)));
            }
            float tNow = Time.unscaledTime;
            for (int i = 0; i < waves.Length; i++)
            {
                var w = waves[i];
                if (w.gameObject.activeSelf != seaOn) w.gameObject.SetActive(seaOn);
                float q = Near(wBase[i].y, wSpan);
                w.rectTransform.anchoredPosition = new Vector2(wBase[i].x + Mathf.Sin(tNow * 0.7f + wPhase[i]) * 10, dir * (q - qc));
                w.color = new Color(waveTint.r, waveTint.g, waveTint.b, 0.35f + 0.65f * Mathf.Clamp01(Mathf.Sin(tNow * 0.55f + wPhase[i]) * 0.5f + 0.6f));
            }
            Place(oldShot, rtOld, 0);
            Place(newShot, rtNew, qNew);
            float Wh = size.x / 2 + 220;
            float edge = Overlap * h + 260; // vùng mây khép / dạt ở mép dải
            // vùng toả: quanh thân tàu; mây dạt ngang hai bên, mở trước mũi, khép lại đúng chỗ sau đuôi (người dùng: thấy rõ thuyền,
            // mây không lùi lại)
            float lsz = look ? look.Size : 1;
            var center = Screen_(sp) + new Vector2(0, 110 * lsz);
            var head = look ? look.Heading : Vector2.up;
            float R = holeRadius * (look ? Mathf.Max(0.7f, look.Size) : 1), R2 = R * 2.6f;
            for (int i = 0; i < clouds.Length; i++)
            {
                var img = clouds[i];
                float q = Near(cBase[i].y, period);
                float a0 = bandA + cJit[i], b0 = bandB - cJit[i];
                bool on = q >= a0 && q <= b0;
                float kk = 1;
                if (on && q < a0 + edge) kk = Mathf.Min(kk, kA);
                if (on && q > b0 - edge) kk = Mathf.Min(kk, kB);
                on &= kk > 0.002f;
                if (img.gameObject.activeSelf != on) img.gameObject.SetActive(on);
                if (!on)
                {
                    cOff[i] = Vector2.zero;
                    continue;
                }
                float x = cBase[i].x, ax = Mathf.Abs(x);
                float g = (1 - kk) * Wh;
                float xd = Mathf.Sign(x == 0 ? 1 : x) * (g + ax * (1 - g / Wh) + Mathf.Pow(1 - kk, 2) * cW[i] * 0.62f);
                var p = new Vector2(xd, dir * (q - qc));
                cOff[i] = Part(p, center, head, R, R2, cOff[i], dt, i);
                img.rectTransform.anchoredPosition = p + cOff[i];
            }
            // mây vành mang theo: cố định trong thế giới, toả quanh tàu
            for (int k = 0; k < kCount; k++)
            {
                var img = carry[k];
                var p = new Vector2(kBase[k].x, dir * (kBase[k].y - qc));
                bool on = Mathf.Abs(p.y) < h * 0.5f + 400;
                if (img.gameObject.activeSelf != on) img.gameObject.SetActive(on);
                kOff[k] = Part(p, center, head, R, R2, kOff[k], dt, k);
                if (on) img.rectTransform.anchoredPosition = p + kOff[k];
            }
        }

        // độ toả một đám mây quanh tàu: nhanh lúc toả, chậm lúc khép
        static Vector2 Part(Vector2 p, Vector2 center, Vector2 head, float R, float R2, Vector2 cur, float dt, int i)
        {
            var target = Side(p, center, head, R, R2, i);
            float rate = target.sqrMagnitude > cur.sqrMagnitude ? 24f : 3.2f;
            return dt > 0 ? Vector2.Lerp(cur, target, 1 - Mathf.Exp(-rate * dt)) : target;
        }

        // đích dạt của một đám mây khi tàu chạy qua: chỉ dạt NGANG (vuông góc hướng đi), mạnh khi gần đường tàu; cửa sổ dọc đường đi mở
        // trước mũi tới 2,4R và khép sau đuôi từ -0,6R tới -1,8R, nên mây dạt ra rồi về đúng chỗ, không bị đẩy lùi theo tàu
        public static Vector2 Side(Vector2 p, Vector2 center, Vector2 head, float R, float R2, int i)
        {
            var d = p - center;
            var h = head.sqrMagnitude > 1e-4f ? head.normalized : Vector2.up;
            var n = new Vector2(-h.y, h.x);
            float along = Vector2.Dot(d, h), lat = Vector2.Dot(d, n), al = Mathf.Abs(lat);
            if (al >= R2) return Vector2.zero;
            float g = along > 1.2f * R ? 1 - Mathf.InverseLerp(1.2f * R, 2.4f * R, along)
                : along < -0.6f * R ? 1 - Mathf.InverseLerp(-0.6f * R, -1.8f * R, along) : 1;
            g = Smooth(g);
            if (g <= 0) return Vector2.zero;
            float k = 1 - al / R2;
            float s = al > 1 ? Mathf.Sign(lat) : (i % 2 == 0 ? 1 : -1);
            return n * (s * R * k * k * g);
        }

        // mang mây vành của màn (đang đúng chỗ trên màn hình) sang dải thế giới: q = q0 + dir * y màn hình
        void Carry(CloudRing ring, float q0, bool arrival)
        {
            if (kBase == null || kBase.Length != carry.Length)
            {
                kBase = new Vector2[carry.Length];
                kOff = new Vector2[carry.Length];
                kRing = new int[carry.Length];
            }
            if (!arrival) kCount = 0;
            float al = Mathf.Max(1e-5f, area.lossyScale.x);
            float layer = ring.Layer.lossyScale.x / al;
            var half = Size / 2;
            // mây gần màn hình trước (kho có hạn): trong màn và một dải quanh màn
            var order = new List<(float d, int i, Vector2 s)>();
            for (int i = 0; i < ring.Count; i++)
            {
                var s1 = Local(ring.Layer.TransformPoint(ring.Home(i)));
                float ex = Mathf.Max(0, Mathf.Abs(s1.x) - half.x), ey = Mathf.Max(0, Mathf.Abs(s1.y) - half.y);
                if (ex > 420 || ey > 700) continue;
                order.Add((ex + ey, i, s1));
            }
            order.Sort((x, y) => x.d.CompareTo(y.d));
            foreach (var (_, i, s0) in order)
            {
                if (kCount >= carry.Length) break;
                var src = ring.Cloud(i);
                var img = carry[kCount];
                img.sprite = src.sprite;
                var srt = src.rectTransform;
                float sc = srt.lossyScale.y / al;
                img.rectTransform.sizeDelta = srt.rect.size * sc;
                img.rectTransform.localScale = new Vector3(Mathf.Sign(srt.localScale.x), 1, 1);
                kBase[kCount] = new Vector2(s0.x, q0 + dir * s0.y);
                kOff[kCount] = ring.Offset(i) * layer;
                kRing[kCount] = arrival ? i : -1;
                kCount++;
            }
        }

        // trả độ toả mây mang về mây vành của màn mới, ẩn mây mang
        void HandBack()
        {
            float al = Mathf.Max(1e-5f, area.lossyScale.x);
            for (int k = 0; k < kCount; k++)
            {
                if (ringNew && kRing[k] >= 0) ringNew.SetOffset(kRing[k], kOff[k] / (ringNew.Layer.lossyScale.x / al));
                carry[k].gameObject.SetActive(false);
            }
            kCount = 0;
            if (ringNew) ringNew.Show(true);
            ringNew = null;
        }

        void Place(RawImage shot, RenderTexture rt, float q)
        {
            if (!shot) return;
            bool on = rt && Mathf.Abs(q - qc) < H * 1.05f;
            if (shot.gameObject.activeSelf != on) shot.gameObject.SetActive(on);
            if (on) shot.rectTransform.anchoredPosition = new Vector2(0, dir * (q - qc));
        }

        // ---------- đường cong vào bến ----------

        void BuildArc(Vector2 p0, Vector2 d0, Vector2 p3, Vector2 t3)
        {
            float D = Vector2.Distance(p0, p3);
            var p1 = p0 + d0 * D * 0.35f;
            var p2 = p3 - t3 * Mathf.Min(D * 0.3f, 520);
            arc.Clear();
            arcAcc.Clear();
            arcLen = 0;
            for (int i = 0; i <= 96; i++)
            {
                float t = i / 96f, s = 1 - t;
                var q = s * s * s * p0 + 3 * s * s * t * p1 + 3 * s * t * t * p2 + t * t * t * p3;
                if (arc.Count > 0) arcLen += Vector2.Distance(arc[arc.Count - 1], q);
                arc.Add(q);
                arcAcc.Add(arcLen);
            }
        }

        Vector2 ArcAt(float s)
        {
            if (arc.Count == 0) return sp;
            if (s <= 0) return arc[0];
            if (s >= arcLen) return arc[arc.Count - 1];
            int lo = 0, hi = arcAcc.Count - 1;
            while (hi - lo > 1)
            {
                int m = (lo + hi) / 2;
                if (arcAcc[m] <= s) lo = m;
                else hi = m;
            }
            float seg = arcAcc[hi] - arcAcc[lo];
            return Vector2.Lerp(arc[lo], arc[hi], seg > 0 ? (s - arcAcc[lo]) / seg : 0);
        }

        // ---------- chụp màn ----------

        // chụp màn hiện tại qua camera UI (không lớp này, không thanh trên) vào ảnh cỡ màn
        RenderTexture Snap()
        {
            var cam = PokiCanvas.UiCamera;
            if (!cam) return null;
            var rt = new RenderTexture(Mathf.Max(16, Screen.width), Mathf.Max(16, Screen.height), 24, RenderTextureFormat.ARGB32) { name = "chuyen_tau_chup" };
            var own = view ? view.Canvas : null;
            bool ownOn = own && own.enabled;
            if (own) own.enabled = false;
            var bars = App.Bars ? App.Bars.GetComponentInParent<Canvas>() : null;
            bool barsOn = bars && bars.enabled;
            if (bars) bars.enabled = false;
            Canvas.ForceUpdateCanvases();
            var req = new RenderPipeline.StandardRequest { destination = rt };
            if (RenderPipeline.SupportsRenderRequest(cam, req)) RenderPipeline.SubmitRenderRequest(cam, req);
            else
            {
                var prev = cam.targetTexture;
                cam.targetTexture = rt;
                cam.Render();
                cam.targetTexture = prev;
            }
            if (own) own.enabled = ownOn;
            if (bars) bars.enabled = barsOn;
            return rt;
        }

        // ---------- toạ độ ----------

        Vector2 Screen_(Vector2 p) => new Vector2(p.x, dir * (p.y - qc));

        Vector2 Local(Vector3 world) => area.InverseTransformPoint(world);

        Vector3 World(Vector2 local) => area.TransformPoint(local);

        static float Smooth(float u)
        {
            u = Mathf.Clamp01(u);
            return u * u * (3 - 2 * u);
        }
    }
}
