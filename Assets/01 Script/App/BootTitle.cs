// Màn mở game "Sa bàn giấy" (chép ý tưởng A của Web/src/view/boot/sceneTable.ts, người dùng chọn 2026-11-06; GD_Claude/16_ManBoot.md).
// Bàn gỗ, tấm bản đồ đảo nằm nghiêng như sa bàn; 5 tướng khởi đầu bật dựng lên như sách pop-up ở đảo cùng hệ, mũi tên kế hoạch
// vẽ theo vòng khắc (Thủy → Hỏa → Kim → Mộc → Thổ), khoanh "Xuất phát!" quanh đảo Thủy, logo bật lên. Chạm: tướng ra đòn,
// camera lao vào đảo Thủy, mây khép rồi mở ra sảnh.
// Sa bàn là canvas thế giới đặt ở xa; một camera phối cảnh riêng (chiếu lệch tâm như perspective của CSS) render ra RenderTexture,
// RawImage trên canvas màn boot hiện ảnh đó. Tướng là AolaSticker (camera riêng như trên sân đấu), gắn vào tấm dựng của sa bàn.
// Prefab Assets/04 Prefabs/Screens/BootTitle (menu "PokiClash/Prefab/Màn mở game: sa bàn"). App mở màn này khi game chạy
// thẳng vào sảnh; có scene khác được mở (tour thử, nút) thì màn tự tắt ngay.
using System;
using System.Collections;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BootTitle : MonoBehaviour
    {
        // thứ tự khắc, cũng là thứ tự đảo: mũi tên i đi từ Cycle[i] tới Cycle[i + 1]
        public static readonly Elem[] Cycle = { Elem.Thuy, Elem.Hoa, Elem.Kim, Elem.Moc, Elem.Tho };
        public const float Tilt = 46; // độ nghiêng tấm bản đồ (độ)
        public const float HeroHeight = 266; // chiều cao dáng đứng của tướng trên tấm dựng (đơn vị UI)
        const float IntroLen = 4.3f;

        static readonly string[] Tips =
        {
            "Thủy khắc Hỏa, Hỏa khắc Kim, Kim khắc Mộc, Mộc khắc Thổ, Thổ khắc Thủy.",
            "Đánh vào hệ mình khắc: sát thương ×1,5. Bị khắc thì chỉ còn ×0,75.",
            "Mỗi lượt chọn 5 lần, mỗi lần 1 trong 3 thẻ.",
            "Chiêu và Tuyệt kỹ không tốn lần chọn, chỉ tốn mana và nộ.",
            "Ải đã qua tự đánh ra bi khi bạn vắng mặt.",
            "Cấp người chơi cũng là cấp của mọi tướng.",
            "Gom đủ mảnh để thu phục tướng mới.",
        };

        [Serializable]
        public sealed class Standee
        {
            public RectTransform up; // tấm dựng, gốc ở chân: quay quanh trục X từ nằm phẳng (0) lên đứng (-Tilt)
            public RectTransform flag; // cờ hệ, gốc ở chân cán
            public RectTransform bases; // đế màu và viền mực, nằm trên bản đồ
            public bool flip; // tướng bên phải bản đồ quay mặt sang trái
        }

        [Serializable]
        public sealed class Parts
        {
            [Header("Canvas màn boot")]
            public PokiCanvas view;
            public RectTransform stage; // khung 1080 × 1920 giữa màn
            public ClickCatcher catcher; // mặt bàn nhận chạm
            public RawImage saBan; // ảnh camera sa bàn, đặt đúng vùng region
            public RectTransform logo, tagline, note;
            public CanvasGroup taglineGroup, props; // props: thẻ úp và bút chì trên bàn
            public GameObject loading, tap;
            public Image barFill;
            public RectTransform barPencil;
            public TextMeshProUGUI pct, tip;
            public RectTransform tapText;

            [Header("Sa bàn (canvas thế giới ở xa)")]
            public RectTransform world;
            public Camera cam;
            public Vector3 eye; // vị trí camera so với canvas thế giới (đơn vị UI)
            public Rect region; // vùng ảnh trên mặt canvas thế giới = chỗ RawImage trên khung (đơn vị UI, gốc giữa)
            public RectTransform sheet;
            public CanvasGroup sheetGroup;
            public Image island;
            public InkPath[] arrowInk = new InkPath[0], arrowColor = new InkPath[0], arrowHead = new InkPath[0];
            public InkPath ring;
            public CanvasGroup start; // vòng khoanh và chữ "Xuất phát!"
            public Standee[] standees = new Standee[0]; // theo Cycle
        }

        public Parts p = new Parts();

        public static BootTitle Current { get; private set; }

        RenderTexture rt;
        readonly AolaSticker[] heroes = new AolaSticker[5];
        readonly string[] clip = new string[5];
        readonly float[] clipT = new float[5];
        Vector2 sheetPos, notePos, logoPos, saBanPos;
        float logoRot, flow, tipT, tapT;
        int entered, tipIdx;
        bool ready, tapped, idle;

        // mở màn (App gọi khi game chạy thẳng vào sảnh)
        public static void Spawn(BootTitle prefab)
        {
            if (Current || !prefab) return;
            var b = Instantiate(prefab);
            b.name = prefab.name;
            DontDestroyOnLoad(b.gameObject);
        }

        // tắt ngay, không diễn (tour thử, scene khác được mở)
        public static void Dismiss()
        {
            if (Current) Destroy(Current.gameObject);
        }

        void Awake()
        {
            Current = this;
            if (App.Router != null) App.Router.Entered += OnEntered;
        }

        void OnDestroy()
        {
            if (Current == this) Current = null;
            if (App.Router != null) App.Router.Entered -= OnEntered;
            foreach (var h in heroes) h?.Destroy();
            if (p.cam) p.cam.targetTexture = null;
            if (rt) rt.Release();
        }

        // lần vào sảnh đầu tiên là của màn này; scene nào được mở sau đó thì màn tắt
        void OnEntered(SceneRoot root)
        {
            entered++;
            if (entered > 1 && !tapped) Destroy(gameObject);
        }

        IEnumerator Start()
        {
            p.catcher.OnClick = OnTap;
            sheetPos = p.sheet.anchoredPosition;
            notePos = p.note.anchoredPosition;
            logoPos = p.logo.anchoredPosition;
            logoRot = p.logo.localEulerAngles.z;
            saBanPos = p.saBan.rectTransform.anchoredPosition;
            tipIdx = UnityEngine.Random.Range(0, Tips.Length);
            ShowTip();
            PrepareCamera();
            CreateHeroes();
            HideAll();
            // mây (canvas phủ, trên màn này) còn che lúc sảnh đang nạp: đợi mây mở rồi mới diễn
            while (App.Router == null || App.Router.Busy || App.Router.CurrentRoot == null) yield return null;
            yield return Intro();
        }

        // ---------- camera sa bàn ----------

        void PrepareCamera()
        {
            var r = p.region;
            float scale = p.view && p.view.Canvas ? p.view.Canvas.scaleFactor : 0;
            if (scale <= 0.01f) scale = Screen.height / PokiCanvas.RefH;
            int w = Mathf.Clamp(Mathf.RoundToInt(r.width * scale), 256, 2048);
            int h = Mathf.Clamp(Mathf.RoundToInt(r.height * scale), 256, 2048);
            // URP báo lỗi mỗi khung nếu RenderTexture đích không có depth buffer (như AolaSticker)
            rt = new RenderTexture(w, h, 16, RenderTextureFormat.ARGB32) { name = "sa_ban", antiAliasing = 2 };
            p.cam.targetTexture = rt;
            p.saBan.texture = rt;
            // camera ở "mắt" nhìn thẳng vào mặt canvas thế giới; khung chiếu lệch tâm đúng bằng vùng region trên mặt đó,
            // nên ảnh ra khớp với vị trí RawImage trên khung (như perspective + perspective-origin của CSS)
            p.cam.transform.SetPositionAndRotation(p.world.TransformPoint(p.eye), p.world.rotation);
            float d = -p.eye.z, n = 20, f = d * 3, k = n / d;
            p.cam.projectionMatrix = Matrix4x4.Frustum((r.xMin - p.eye.x) * k, (r.xMax - p.eye.x) * k, (r.yMin - p.eye.y) * k, (r.yMax - p.eye.y) * k, n, f);
            p.cam.enabled = true; // tắt sẵn trong prefab để khung đầu không vẽ ra màn hình
        }

        void CreateHeroes()
        {
            var data = App.Data;
            for (int i = 0; i < Cycle.Length && i < p.standees.Length; i++)
            {
                HeroDef hero = null;
                foreach (var id in data.Starters)
                {
                    var hd = data.Hero(id);
                    if (hd != null && hd.elem == Cycle[i]) hero = hd;
                }
                if (hero == null || hero.forms.Length == 0) continue;
                var s = AolaSticker.TryCreate(p.standees[i].up, hero, hero.forms[0].aola, HeroHeight, p.standees[i].flip);
                if (s == null) continue;
                s.HideShadow();
                heroes[i] = s;
                clip[i] = StageView.Idle;
                clipT[i] = UnityEngine.Random.value * 3;
            }
        }

        void Play(int i, string c)
        {
            if (heroes[i] == null) return;
            clip[i] = c;
            clipT[i] = 0;
        }

        // ---------- cảnh mở ----------

        void HideAll()
        {
            p.sheetGroup.alpha = 0;
            p.island.fillAmount = 0;
            foreach (var s in p.standees)
            {
                s.up.gameObject.SetActive(false);
                s.flag.gameObject.SetActive(false);
                s.bases.localScale = Vector3.zero;
            }
            foreach (var a in p.arrowInk) a.Reveal = 0;
            foreach (var a in p.arrowColor) a.Reveal = 0;
            foreach (var a in p.arrowHead) a.Reveal = 0;
            p.ring.Reveal = 0;
            p.start.alpha = 0;
            p.logo.localScale = new Vector3(1, 0, 1);
            p.taglineGroup.alpha = 0;
            p.note.anchoredPosition = notePos + new Vector2(0, -320);
            p.loading.SetActive(true);
            p.tap.SetActive(false);
            SetBar(0);
        }

        IEnumerator Intro()
        {
            float t0 = Time.unscaledTime;
            // tấm bản đồ trượt vào bàn, giấy ghi chú trồi lên
            Run(0.05f, 0.7f, Ease.Out, k =>
            {
                p.sheetGroup.alpha = k;
                p.sheet.anchoredPosition = sheetPos + new Vector2(0, -840 * (1 - k));
                p.sheet.localEulerAngles = new Vector3(Tilt + 20 * (1 - k), 0, 0);
            });
            Run(0.2f, 0.5f, Ease.Back, k => p.note.anchoredPosition = notePos + new Vector2(0, -320 * (1 - k)));
            // đảo được tô dần từ trái sang
            Run(0.65f, 0.75f, Ease.InOut, k => p.island.fillAmount = k);
            // tướng và cờ bật dựng lên như sách pop-up
            for (int i = 0; i < p.standees.Length; i++)
            {
                var s = p.standees[i];
                float d = 1.45f + i * 0.2f;
                Run(d, 0.22f, Ease.Back, k => s.bases.localScale = Vector3.one * Mathf.LerpUnclamped(0.2f, 1, k));
                Run(d + 0.06f, 0.48f, Ease.Out, k =>
                {
                    s.up.gameObject.SetActive(true);
                    s.up.localEulerAngles = new Vector3(Pop(k, Tilt + 22), 0, 0);
                });
                Run(d + 0.2f, 0.42f, Ease.Out, k =>
                {
                    s.flag.gameObject.SetActive(true);
                    s.flag.localEulerAngles = new Vector3(Pop(k, Tilt + 18), 0, 0);
                });
                After(d + 0.12f, () => App.Audio?.Play("pick"));
            }
            // mũi tên kế hoạch theo vòng khắc; tới nơi thì tướng bị khắc giật mình
            for (int i = 0; i < Cycle.Length && i < p.arrowInk.Length; i++)
            {
                int a = i;
                float d = 2.55f + i * 0.28f;
                Run(d, 0.3f, Ease.InOut, k =>
                {
                    p.arrowInk[a].Reveal = k;
                    p.arrowColor[a].Reveal = k;
                });
                Run(d + 0.28f, 0.12f, Ease.Out, k => p.arrowHead[a].Reveal = k);
                After(d + 0.3f, () =>
                {
                    App.Audio?.Play("card");
                    Play((a + 1) % Cycle.Length, StageView.Hit);
                });
            }
            // khoanh "Xuất phát!" quanh đảo Thủy
            After(4f, () => p.start.alpha = 1);
            Run(4f, 0.42f, Ease.InOut, k => p.ring.Reveal = k);
            // logo gấp bật lên rồi đóng dấu, băng keo chữ dán ngang
            Run(3.7f, 0.56f, Ease.Out, k =>
            {
                float sy = k < 0.6f ? Mathf.Lerp(0.02f, 1.12f, k / 0.6f) : Mathf.Lerp(1.12f, 1, (k - 0.6f) / 0.4f);
                p.logo.localScale = new Vector3(1, sy, 1);
            });
            After(4.26f, () => App.Audio?.Play("stamp"));
            Run(4.26f, 0.26f, Ease.Out, k =>
            {
                p.taglineGroup.alpha = k;
                p.tagline.localScale = new Vector3(Mathf.Lerp(0.2f, 1, k), 1, 1);
            });

            // thanh tải chạy theo cảnh
            while (Time.unscaledTime - t0 < IntroLen)
            {
                SetBar((Time.unscaledTime - t0) / IntroLen);
                yield return null;
            }
            SetBar(1);
            idle = true;
            yield return new WaitForSecondsRealtime(0.25f);
            p.loading.SetActive(false);
            p.tap.SetActive(true);
            tapT = 0;
            ready = true;
        }

        // pop-up: nằm phẳng (0) → quá đà (-over) → đứng (-Tilt)
        static float Pop(float k, float over) =>
            k < 0.65f ? Mathf.Lerp(0, -over, Ease.Out(k / 0.65f)) : Mathf.Lerp(-over, -Tilt, Ease.Out((k - 0.65f) / 0.35f));

        void SetBar(float v)
        {
            v = Mathf.Clamp01(v);
            p.barFill.fillAmount = v;
            float w = p.barFill.rectTransform.rect.width;
            var pp = p.barPencil.anchoredPosition;
            p.barPencil.anchoredPosition = new Vector2(-w / 2 + w * v + 18, pp.y);
            p.pct.text = $"{Mathf.RoundToInt(v * 100)}%";
        }

        void ShowTip()
        {
            p.tip.text = $"<color=#b8382a><b>Mẹo:</b></color> {Tips[tipIdx % Tips.Length]}";
            tipIdx++;
        }

        // ---------- chạm để vào ----------

        void OnTap()
        {
            if (!ready || tapped) return;
            tapped = true;
            StartCoroutine(Exit());
        }

        IEnumerator Exit()
        {
            App.Audio?.Play("whoosh");
            for (int i = 0; i < heroes.Length; i++) Play(i, StageView.Attack);
            Run(0.15f, 0.7f, Ease.In, k =>
            {
                p.logo.anchoredPosition = logoPos + new Vector2(0, 520 * k);
                p.logo.localEulerAngles = new Vector3(0, 0, logoRot + 6 * k);
            });
            Run(0, 0.3f, Ease.Linear, k => p.taglineGroup.alpha = 1 - k);
            Run(0.15f, 0.5f, Ease.In, k => p.note.anchoredPosition = notePos + new Vector2(0, -400 * k));
            Run(0, 0.4f, Ease.Linear, k => p.props.alpha = 1 - k);
            // lao vào đảo Thủy (chỗ xuất phát): phóng ảnh sa bàn quanh điểm chân tướng Thủy trên khung
            var rtr = p.saBan.rectTransform;
            var vp = p.cam.WorldToViewportPoint(p.standees[0].up.position);
            var r = p.region;
            var focus = new Vector2(r.xMin + vp.x * r.width, r.yMin + vp.y * r.height);
            Run(0.25f, 1f, Ease.In, k =>
            {
                float s = Mathf.Lerp(1, 2.8f, k);
                rtr.localScale = new Vector3(s, s, 1);
                rtr.anchoredPosition = focus + (saBanPos - focus) * s;
            });
            yield return new WaitForSecondsRealtime(1.2f);
            App.I.StartCoroutine(App.CoverThen(() => Destroy(gameObject)));
        }

        // ---------- mỗi khung ----------

        void Update()
        {
            float dt = Mathf.Min(0.05f, Time.unscaledDeltaTime);
            for (int i = 0; i < heroes.Length; i++)
            {
                var h = heroes[i];
                if (h == null) continue;
                clipT[i] += dt;
                var c = clip[i];
                bool loop = c == StageView.Idle;
                if (!loop && clipT[i] >= h.Duration(c))
                {
                    c = clip[i] = StageView.Idle;
                    clipT[i] = 0;
                    loop = true;
                }
                if (c == StageView.Attack) h.FarAhead(c, 1.3f);
                else h.Far(c, null, false);
                h.Show(c, clipT[i], loop, 1, false, 0);
            }
            if (!idle) return;
            // nét kế hoạch chạy, cờ bay
            flow += dt * 45;
            foreach (var a in p.arrowInk) a.Offset = flow;
            foreach (var a in p.arrowColor) a.Offset = flow;
            for (int i = 0; i < p.standees.Length; i++)
            {
                float w = 0.5f - 0.5f * Mathf.Cos((Time.unscaledTime + i * 0.37f) * Mathf.PI * 2 / 1.8f);
                p.standees[i].flag.localScale = new Vector3(1 - 0.08f * w, 1, 1);
            }
            tipT += dt;
            if (p.loading.activeSelf && tipT > 2.6f)
            {
                tipT = 0;
                ShowTip();
            }
            if (ready && !tapped)
            {
                tapT += dt;
                float w = 0.5f - 0.5f * Mathf.Cos(tapT * Mathf.PI * 2 / 1.4f);
                p.tapText.localScale = Vector3.one * (1 + 0.07f * w);
                p.tapText.localEulerAngles = new Vector3(0, 0, 1 - 2 * w);
            }
        }

        // ---------- tween nhỏ ----------

        void Run(float delay, float dur, Func<float, float> ease, Action<float> set) => StartCoroutine(Tween(delay, dur, ease, set));

        void After(float delay, Action a) => StartCoroutine(Tween(delay, 0, Ease.Linear, k => a()));

        static IEnumerator Tween(float delay, float dur, Func<float, float> ease, Action<float> set)
        {
            if (delay > 0) yield return new WaitForSecondsRealtime(delay);
            for (float t = 0; t < dur; t += Time.unscaledDeltaTime)
            {
                set(ease(t / dur));
                yield return null;
            }
            set(ease(1));
        }

        static class Ease
        {
            public static float Linear(float k) => k;
            public static float Out(float k) => 1 - Mathf.Pow(1 - k, 3);
            public static float In(float k) => k * k * k;
            public static float InOut(float k) => k < 0.5f ? 4 * k * k * k : 1 - Mathf.Pow(-2 * k + 2, 3) / 2;
            public static float Back(float k)
            {
                const float c1 = 1.70158f, c3 = c1 + 1;
                return 1 + c3 * Mathf.Pow(k - 1, 3) + c1 * Mathf.Pow(k - 1, 2);
            }
        }
    }
}

