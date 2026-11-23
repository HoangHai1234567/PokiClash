// Thú trên cảnh Trang trại (prefab Items/ThuTrangTrai, người dùng dặn 2026-11-10: trang trại là cảnh thật, thú thả đi lại, chạm được, nhún
// nhún, mỗi khu một việc thật). Hình là chân dung tướng (sticker đã có viền giấy) cử động bằng code, gốc ở chân; FarmScene giữ mỗi tướng
// một con và đổi trạng thái:
// - Rảnh (Roam): đứng thở nhún, ngó quanh, nhảy lò cò tới chỗ khác trong bãi cỏ; chạm thì bật lên, thả tim, hiện tên; kéo thả vào một chỗ
//   làm để giao việc (FarmScene.PetDropped), thả ra ngoài thì nhảy về bãi cỏ.
// - Làm (Work): cử động theo loại chỗ, cầm đồ nghề, có hạt: ruộng rau cuốc đất (bụi), ao vịt rắc thóc, vườn cây nhảy hái quả, lò bánh
//   nhào bột (khói), xưởng nông cụ rèn (tia lửa); thỉnh thoảng nảy sản phẩm. Hết sức (Tired): ngồi nghiêng, giọt mồ hôi. Chạm: mở danh sách
//   chọn tướng của chỗ đó.
// - Nghỉ (Sleep, vừa rút khỏi chỗ làm): nằm trên ổ rơm, thở chậm, "z" bay lên; chạm thì hiện còn nghỉ bao lâu.
// - Đi (Walk): nhảy lò cò tới một điểm rồi vào trạng thái đích (đổi chỗ, về ổ rơm, ra bãi cỏ).
// Toạ độ: localPosition trong lớp thú (FarmScene.PetLayer) là điểm chân; lớp hạt trùng khung với lớp thú.
// Cảnh chủ là IFarmPetHost: Trang trại (FarmScene) hoặc màn Nhà (HomeScene, quái đi lang thang trên đất đã mở, kéo vào công trình).
// Màn Nhà bật UseRig (người dùng 2026-11-20: "để các tướng chạy bằng animation walk/idle luôn, buổi đêm làm chúng phát sáng nhẹ"):
// - hình là rig .atomik qua AolaSticker thay chân dung tĩnh: đi thì clip walk, đứng / làm / hết sức thì idle (tư thế code vẫn chồng lên),
//   ngủ vẫn chân dung nằm; dạng chưa có clip walk thì đi bằng dáng đứng, nhún nhẹ (người dùng: "làm tạm idle di chuyển", walk bổ sung
//   sau). Không nhảy lò cò, không thở bằng code (rig tự thở). Chỉ con trong khung nhìn mới chụp rig (mỗi con một camera), dựng mỗi khung
//   tối đa một con (AolaSticker.CanBuildNow); cỡ theo HeroForm.size như trên sân (rồng to, lính nhỏ), nén giãn / lò xo / quay mặt bằng
//   code còn 30% (người dùng 2026-11-20: "tỉ lệ không đúng và bị vỡ"; nét vỡ do atlas thu nhỏ nhiều: PetPart lấy mẫu nhiều điểm);
// - đêm (chạng vạng sáng dần theo DayCycle): tướng sáng hơn cảnh đã nhuộm (sticker _Lift) và vầng sáng màu hệ thật nhạt sau lưng (aura,
//   cộng sáng, cùng lớp với tướng nên khuất sau công trình như tướng).
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using Random = UnityEngine.Random;

namespace PokiClash
{
    // cảnh chứa thú: chỗ làm (spot), hạt, chỗ đi chơi, chạm / kéo thả
    public interface IFarmPetHost
    {
        float SpotFace(int spot);
        Sprite Prop(FarmProp k);
        Sprite ProductOf(string kind);
        void Fx(Sprite s, Color c, Vector2 pos, Vector2 vel, float gravity, float life, float size0, float size1, float spin = 0, bool pop = false, float drag = 0);
        Vector2 RoamPoint(Vector2 near);
        Vector2 ClampMeadow(Vector2 pt);
        void PetTapped(FarmPet pet);
        void PetDragging(FarmPet pet, Vector2 pt);
        bool PetDropped(FarmPet pet, Vector2 pt);
    }

    public sealed class FarmPet : MonoBehaviour, IPointerClickHandler, IBeginDragHandler, IDragHandler, IEndDragHandler
    {
        public enum Mode { Roam, Walk, Work, Tired, Sleep, Drag }

        [Serializable]
        public struct Parts
        {
            public RectTransform body; // gốc ở chân: nhún, nghiêng, nhảy
            public RectTransform flip; // con của body: lật ngang theo hướng nhìn
            public HeroPortrait portrait;
            public Image shadow, tool, emote;
            public TextMeshProUGUI tag;
            public Image aura; // con của body, sau lat: vầng sáng đêm (màn Nhà), cộng sáng
        }

        public const float Height = 150, SleepHeight = 128;
        const float HopTime = 0.38f, HopHeight = 24, WalkSpeed = 150;

        [SerializeField] Parts p;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        public string Hero { get; private set; }
        public Mode State { get; private set; }
        public int Spot { get; private set; } = -1;
        public Vector2 Pos => pos;
        // kéo trên con không kéo được (đang làm, nghỉ, đi tới chỗ làm) thì chuyển cú kéo cho bản đồ: Trang trại bật; màn Nhà tắt để chạm, giữ
        // tướng không bao giờ dời máy (người dùng 2026-11-23), thả tay vẫn là chạm (mở bảng công trình)
        public bool PassPan = true;

        IFarmPetHost scene;
        UnityEngine.Object sceneObj; // để biết cảnh chủ đã huỷ chưa (interface không so được với null của Unity)
        PointerEventData dragEvent; // ngón đang kéo: mỗi khung đặt lại theo ngón (ngón thứ hai có thể kéo bản đồ trong lúc cầm)
        // camera của cú chạm, lưu lúc bắt đầu kéo: ngoài hàm sự kiện, dragEvent.pressEventCamera có thể là null. InputSystemUIInputModule
        // dùng chung một PointerEventData cho chuột trái / phải / giữa: khung nào ngón di chuyển, xử lý xong nút giữa thì trạng thái nhấn
        // trong đó là của nút giữa (không có raycast). Update tính chỗ ngón bằng camera null thì sai toạ độ, tướng văng khỏi màn
        // (người dùng 2026-11-23: "hold tướng rồi drag đi thì hình tướng bị mất")
        Camera dragCam;
        string kind;
        Vector2 pos, walkTo, dragOffset;
        Mode after; // trạng thái khi đi tới nơi
        float face = 1, faceShown = 1;
        float wait, hopT = -1, lift, squash, squashV, phase, speed, nextProduct, tagLeft, emoteT = -1, zT;
        float breathe; // chu kỳ thở riêng mỗi con
        Color toolColor = Color.white;

        // rig .atomik (màn Nhà)
        const float StandK = 0.62f;   // dáng đứng ≈ 62% khung chân dung (như ZoneSceneLand)
        const float NightLift = 0.45f; // đêm: sticker sáng thêm 45% (cảnh nhuộm còn ~66–93%)
        // nén giãn, lò xo, quay mặt bằng code còn 30% khi rig chạy: rig tự diễn, đè nguyên mức của chân dung giấy làm hình méo
        // (người dùng 2026-11-20: "tỉ lệ không đúng")
        const float RigSquash = 0.3f;
        // hệ số cỡ của dạng (HeroForm.size, 0,48–1,56, như trên sân đấu): màn Nhà (rig) theo cỡ này để các tướng đúng tỉ lệ với nhau;
        // Trang trại (chân dung) giữ mọi con cùng cỡ như cũ
        float sizeK = 1;
        float H => Height * sizeK;
        float SleepH => SleepHeight * sizeK;
        // đỉnh hình đang hiện: rig cao bằng dáng đứng (H x StandK), chân dung cao H. Nhãn, biểu cảm, hạt nổi bám theo đây (người dùng
        // 2026-11-21: chữ "Hết sức" lơ lửng cao, không thấy tướng bên dưới)
        float TopH => RigOn ? H * StandK * 1.08f : H;
        public float ViewHeight => TopH; // khung hình để cảnh chủ xếp thứ tự vẽ (HomeScene.SortObjectsAndPets)
        bool rig, rigFailed, hasWalk;
        AolaSticker sticker;
        string clipShown;
        float clipT;
        Color auraColor = Color.white;
        Canvas rootCanvas;

        RectTransform Rt => (RectTransform)transform;

        public void Bind(IFarmPetHost owner, HeroDef h)
        {
            scene = owner;
            sceneObj = owner as UnityEngine.Object;
            Hero = h.id;
            name = "thu_" + h.id;
            p.portrait.Bind(h, Height);
            breathe = Random.Range(1.3f, 1.8f);
            phase = Random.value;
            speed = Random.Range(0.9f, 1.1f);
            face = faceShown = Random.value < 0.5f ? -1 : 1;
            p.emote.gameObject.SetActive(false);
            p.tag.gameObject.SetActive(false);
            p.tool.gameObject.SetActive(false);
            auraColor = Color.Lerp(Theme.Of(h.elem), Color.white, 0.5f);
            if (p.aura) p.aura.gameObject.SetActive(false);
        }

        // màn Nhà: hình là rig chạy walk / idle, đêm sáng nhẹ (chú thích đầu file)
        public void UseRig(bool on)
        {
            rig = on;
            var h = App.Data.Hero(Hero);
            float k = on && h != null ? Mathf.Clamp((float)HeroArt.FormOf(h).size, 0.4f, 1.8f) : 1;
            if (!Mathf.Approximately(k, sizeK))
            {
                sizeK = k;
                DropRig(); // dựng lại theo cỡ mới
                if (h != null) p.portrait.Bind(h, State == Mode.Sleep ? SleepH : H);
                if (p.aura) // vầng sáng đêm nướng theo Height (HomePetMenu): theo cỡ dạng
                {
                    p.aura.rectTransform.anchoredPosition = new Vector2(0, H * 0.42f);
                    p.aura.rectTransform.localScale = Vector3.one * sizeK;
                }
            }
            if (!on) DropRig();
        }

        void DropRig()
        {
            sticker?.Destroy();
            sticker = null;
            clipShown = null;
            if (p.portrait) p.portrait.gameObject.SetActive(true);
        }

        void OnDestroy() => sticker?.Destroy();

        // đặt thẳng vào trạng thái (lần đầu vào cảnh)
        public void Place(Mode mode, Vector2 at, int spot, string spotKind)
        {
            pos = at;
            Rt.localPosition = pos;
            Enter(mode, spot, spotKind);
        }

        // nhảy lò cò tới at rồi vào trạng thái mode
        public void WalkTo(Vector2 at, Mode mode, int spot, string spotKind)
        {
            if ((at - pos).sqrMagnitude < 4)
            {
                Enter(mode, spot, spotKind);
                return;
            }
            Spot = spot;
            kind = spotKind;
            walkTo = at;
            after = mode;
            State = Mode.Walk;
            p.tool.gameObject.SetActive(false);
            p.tag.gameObject.SetActive(false);
            Look(at.x - pos.x);
            if (hopT < 0) hopT = 0;
        }

        void Enter(Mode mode, int spot, string spotKind)
        {
            State = mode;
            Spot = spot;
            kind = spotKind;
            wait = Random.Range(0.4f, 2.5f);
            nextProduct = Random.Range(3f, 6f);
            p.portrait.Bind(App.Data.Hero(Hero), mode == Mode.Sleep ? SleepH : H);
            ToolFor(mode);
            p.tag.gameObject.SetActive(false);
            p.emote.gameObject.SetActive(false);
            emoteT = -1;
            if (mode == Mode.Tired) ShowTag(Loc.T("Hết sức"), 0, Theme.Hex("#ffd6c8"));
            if (mode == Mode.Sleep) face = 1;
            if (mode == Mode.Work || mode == Mode.Tired) face = scene.SpotFace(spot);
            Kick(0.12f);
        }

        void ToolFor(Mode mode)
        {
            Sprite s = null;
            if (mode == Mode.Work)
                s = kind == "veg" ? scene.Prop(FarmProp.Hoe) : kind == "smithy" ? scene.Prop(FarmProp.Hammer) :
                    kind == "duck" ? scene.Prop(FarmProp.Sack) : kind == "orchard" ? scene.Prop(FarmProp.Basket) :
                    kind == "bakery" ? scene.Prop(FarmProp.Bread) : null;
            p.tool.gameObject.SetActive(s);
            if (!s) return;
            p.tool.sprite = s;
            p.tool.color = toolColor;
            var t = p.tool.rectTransform;
            // đồ cầm tay ở trước bụng; giỏ quả, ổ bánh đặt dưới đất bên cạnh
            bool ground = kind == "orchard" || kind == "bakery";
            t.anchoredPosition = ground ? new Vector2(70, 4) : new Vector2(46, 46);
            t.sizeDelta = ground ? new Vector2(70, 70) : new Vector2(84, 84);
            t.localEulerAngles = Vector3.zero;
        }

        // ---------- chạm, kéo ----------

        public void OnPointerClick(PointerEventData e)
        {
            if (State == Mode.Drag) return;
            Haptics.Play(Haptic.Peg);
            if (Free)
            {
                // bật lên, thả tim, hiện tên (con đang nhảy tới chỗ làm hay ổ rơm thì vẫn đi tiếp)
                if (State == Mode.Walk && after == Mode.Roam)
                {
                    hopT = -1;
                    State = Mode.Roam;
                    lift = 0;
                }
                wait = Random.Range(1f, 2f);
                Kick(-0.22f);
                if (State == Mode.Roam) jumpT = 0;
                Emote(scene.Prop(FarmProp.Heart));
                ShowTag(App.Data.Hero(Hero).name, 1.6f, Theme.Paper);
                App.Audio.Play("pick");
                scene.Fx(scene.Prop(FarmProp.Heart), Color.white, pos + new Vector2(Random.Range(-30f, 30f), TopH * 0.9f), new Vector2(Random.Range(-40f, 40f), 160), 0, 1.1f, 34, 26, 0, true);
                return;
            }
            Kick(0.14f);
            scene.PetTapped(this);
        }

        // rảnh: đang đứng chơi hoặc nhảy trong bãi cỏ
        bool Free => State == Mode.Roam || (State == Mode.Walk && after == Mode.Roam);

        bool CanDrag => Free;

        public void OnBeginDrag(PointerEventData e)
        {
            if (!CanDrag)
            {
                if (!PassPan) return; // màn Nhà: nuốt cú kéo, thả tay trên tướng vẫn là chạm
                // không kéo được thì chuyển cú kéo cho bản đồ (HubPan ở cha)
                var pan = ExecuteEvents.GetEventHandler<IBeginDragHandler>(transform.parent.gameObject);
                e.pointerDrag = pan;
                if (pan) ExecuteEvents.Execute(pan, e, ExecuteEvents.beginDragHandler);
                return;
            }
            State = Mode.Drag;
            hopT = -1;
            dragEvent = e;
            dragCam = e.pressEventCamera; // trong hàm sự kiện: đúng camera của nút trái
            p.tag.gameObject.SetActive(false);
            dragOffset = pos - Local(e);
            Kick(-0.18f);
            App.Audio.Play("click");
            Haptics.Play(Haptic.Peg);
            transform.SetAsLastSibling();
        }

        public void OnDrag(PointerEventData e)
        {
            if (State != Mode.Drag) return;
            dragEvent = e;
            FollowFinger(e);
        }

        void FollowFinger(PointerEventData e)
        {
            var to = Local(e) + dragOffset;
            Look(to.x - pos.x);
            pos = to;
            Rt.localPosition = pos;
            scene.PetDragging(this, pos);
        }

        public void OnEndDrag(PointerEventData e)
        {
            dragEvent = null;
            if (State != Mode.Drag) return;
            State = Mode.Roam;
            lift = 0;
            Kick(0.2f);
            App.Audio.Play("drop", 0.8f);
            if (!scene.PetDropped(this, pos)) WalkTo(scene.ClampMeadow(pos), Mode.Roam, -1, null);
        }

        Vector2 Local(PointerEventData e)
        {
            RectTransformUtility.ScreenPointToLocalPointInRectangle((RectTransform)transform.parent, e.position, dragCam, out var lp);
            return lp;
        }

        // ---------- cử động ----------

        float jumpT = -1; // cú bật khi chạm (0..1)

        void Kick(float amount) => squashV += amount * 18;

        void Look(float dx)
        {
            if (Mathf.Abs(dx) > 2) face = dx < 0 ? -1 : 1;
        }

        void Emote(Sprite s)
        {
            if (!s) return;
            p.emote.sprite = s;
            p.emote.gameObject.SetActive(true);
            emoteT = 0;
        }

        void ShowTag(string text, float seconds, Color c)
        {
            p.tag.text = text;
            p.tag.color = c;
            p.tag.gameObject.SetActive(true);
            tagLeft = seconds; // 0: giữ mãi
        }

        void Update()
        {
            if (sceneObj == null) return;
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            float t = Time.unscaledTime;
            float rot = 0, extraLift = 0;
            float breath = Mathf.Sin((t + phase * 3) * Mathf.PI * 2 / breathe);
            if (RigOn) breath = 0; // rig tự thở trong clip idle
            float sy = 1 + 0.035f * breath, sx = 1 - 0.02f * breath;

            switch (State)
            {
                case Mode.Roam:
                    if ((wait -= dt) <= 0)
                    {
                        float r = Random.value;
                        if (r < 0.65f) WalkTo(scene.RoamPoint(pos), Mode.Roam, -1, null);
                        else if (r < 0.85f) { face = -face; Kick(0.1f); wait = Random.Range(1f, 2.5f); } // ngó quanh
                        else { jumpT = 0; Kick(-0.15f); wait = Random.Range(1.5f, 3f); } // nhảy mừng
                    }
                    break;
                case Mode.Walk:
                    Hop(dt);
                    break;
                case Mode.Drag:
                    if (dragEvent != null) FollowFinger(dragEvent);
                    extraLift = 26 + Mathf.Sin(t * 14) * 4;
                    rot = Mathf.Sin(t * 9) * 7;
                    break;
                case Mode.Work:
                    Work(dt, t, ref rot, ref extraLift, ref sx, ref sy);
                    break;
                case Mode.Tired:
                    rot = -9;
                    sy = 1 + 0.02f * Mathf.Sin(t * 2);
                    sx = 1;
                    if (emoteT < 0 && Random.value < dt * 0.5f) Emote(scene.Prop(FarmProp.Drop));
                    break;
                case Mode.Sleep:
                    rot = -12;
                    float slow = Mathf.Sin((t + phase * 5) * Mathf.PI * 2 / 3.2f);
                    sy = 0.94f + 0.04f * slow;
                    sx = 1 + 0.02f * slow;
                    if ((zT -= dt) <= 0)
                    {
                        zT = Random.Range(1.4f, 2.2f);
                        scene.Fx(scene.Prop(FarmProp.Zzz), Theme.Ink2, pos + new Vector2(24, SleepH * 0.8f), new Vector2(26, 50), 0, 2f, 22, 40, 20);
                    }
                    break;
            }

            // cú bật khi chạm / nhảy mừng
            if (jumpT >= 0)
            {
                jumpT += dt / 0.5f;
                extraLift += Mathf.Sin(Mathf.Clamp01(jumpT) * Mathf.PI) * 70;
                rot += Mathf.Sin(Mathf.Clamp01(jumpT) * Mathf.PI * 2) * 8 * face;
                if (jumpT >= 1)
                {
                    jumpT = -1;
                    Kick(0.25f);
                }
            }

            // lò xo nén giãn
            squashV += (-160 * squash - 11 * squashV) * dt;
            squash += squashV * dt;
            sy *= 1 - squash;
            sx *= 1 + squash * 0.7f;
            float l = lift + extraLift;
            if (l > 1) sy *= 1.05f; // đang bay: dãn ra

            if (RigOn)
            {
                sx = 1 + (sx - 1) * RigSquash;
                sy = 1 + (sy - 1) * RigSquash;
            }
            faceShown = RigOn ? face : Mathf.MoveTowards(faceShown, face, dt * 10); // rig: quay mặt ngay, không bóp dẹt qua 0
            p.flip.localScale = new Vector3(faceShown, 1, 1);
            p.body.anchoredPosition = new Vector2(0, l);
            p.body.localScale = new Vector3(sx, sy, 1);
            p.body.localEulerAngles = new Vector3(0, 0, rot);
            float shadow = Mathf.Clamp01(1 - l / 160);
            p.shadow.rectTransform.localScale = new Vector3(shadow * sizeK * (State == Mode.Sleep ? 1.25f : 1), shadow * sizeK, 1);

            // cảm xúc nổi trên đầu
            if (emoteT >= 0)
            {
                emoteT += dt;
                float k = emoteT < 0.15f ? emoteT / 0.15f * 1.25f : emoteT < 0.3f ? Mathf.Lerp(1.25f, 1, (emoteT - 0.15f) / 0.15f) : 1;
                var er = p.emote.rectTransform;
                er.localScale = Vector3.one * k;
                er.anchoredPosition = new Vector2(46, TopH + 10 + emoteT * 30 + l);
                var c = p.emote.color;
                c.a = emoteT > 1.1f ? Mathf.Clamp01(1 - (emoteT - 1.1f) / 0.4f) : 1;
                p.emote.color = c;
                if (emoteT > 1.5f)
                {
                    emoteT = -1;
                    p.emote.gameObject.SetActive(false);
                }
            }
            if (tagLeft > 0 && (tagLeft -= dt) <= 0) p.tag.gameObject.SetActive(false);
            p.tag.rectTransform.anchoredPosition = new Vector2(0, (State == Mode.Sleep ? SleepH : TopH) + 18 + l);
            RigTick(dt, t);
        }

        // rig đang hiện thay chân dung (màn Nhà, không ngủ, đã dựng xong)
        bool RigOn => rig && sticker != null && State != Mode.Sleep;

        void RigTick(float dt, float t)
        {
            // độ đêm: chạng vạng sáng dần, đủ sớm hơn lúc trời tối hẳn
            float k = 0;
            if (rig)
            {
                k = Mathf.Clamp01(DayCycle.Night(DayCycle.Hour) * 1.6f);
                k = k * k * (3 - 2 * k);
            }
            if (p.aura)
            {
                bool on = k > 0.01f;
                if (p.aura.gameObject.activeSelf != on) p.aura.gameObject.SetActive(on);
                if (on) p.aura.color = new Color(auraColor.r, auraColor.g, auraColor.b, k * (0.3f + 0.07f * Mathf.Sin(t * 1.7f + phase * 6)));
            }
            if (!rig) return;
            bool want = State != Mode.Sleep;
            bool vis = OnScreen();
            if (want && sticker == null && !rigFailed && vis && AolaSticker.CanBuildNow) BuildRig();
            if (sticker == null) return;
            if (sticker.Rect.gameObject.activeSelf != want) sticker.Rect.gameObject.SetActive(want);
            if (p.portrait.gameObject.activeSelf == want) p.portrait.gameObject.SetActive(!want);
            if (!want || !vis)
            {
                sticker.Hold();
                return;
            }
            string clip = State == Mode.Walk && hasWalk ? AolaSticker.Walk : StageView.Idle;
            if (clip != clipShown)
            {
                clipShown = clip;
                clipT = 0;
            }
            clipT += dt * speed;
            sticker.Lift = NightLift * k;
            sticker.Show(clip, clipT, true, 1, false, 0);
        }

        void BuildRig()
        {
            var h = App.Data.Hero(Hero);
            string form = h != null ? HeroArt.FormOf(h).aola : null;
            sticker = string.IsNullOrEmpty(form) ? null : AolaSticker.TryCreate(p.flip, h, form, H * StandK, false);
            if (sticker == null)
            {
                rigFailed = true; // dạng chưa nhập rig: giữ chân dung
                return;
            }
            sticker.HideShadow(); // bóng dưới chân là của thú (p.shadow)
            sticker.Rect.SetSiblingIndex(p.portrait.transform.GetSiblingIndex()); // đồ nghề cầm tay vẫn ở trước
            hasWalk = sticker.HasClip(AolaSticker.Walk);
            clipShown = null;
        }

        // trong khung nhìn (nới mép): ngoài khung thì rig không chụp, không dựng
        bool OnScreen()
        {
            if (!rootCanvas) rootCanvas = GetComponentInParent<Canvas>()?.rootCanvas;
            Camera cam = null;
            if (rootCanvas && rootCanvas.renderMode != RenderMode.ScreenSpaceOverlay) cam = rootCanvas.worldCamera ? rootCanvas.worldCamera : Camera.main;
            var sp = RectTransformUtility.WorldToScreenPoint(cam, transform.position);
            float mx = Screen.width * 0.15f, my = Screen.height * 0.1f;
            return sp.x > -mx && sp.x < Screen.width + mx && sp.y > -my && sp.y < Screen.height + my * 2;
        }

        void Hop(float dt)
        {
            if (hopT < 0) hopT = 0;
            hopT += dt / HopTime;
            // rig (màn Nhà): clip walk tự bước nên không nhảy; dạng chưa có walk đi bằng dáng đứng, nhún nhẹ theo bước
            bool rigWalk = RigOn;
            float hopH = !rigWalk ? HopHeight : hasWalk ? 0 : 6;
            lift = Mathf.Sin(Mathf.Clamp01(hopT) * Mathf.PI) * hopH;
            var d = walkTo - pos;
            float step = WalkSpeed * dt;
            if (d.magnitude <= step) pos = walkTo;
            else pos += d.normalized * step;
            Rt.localPosition = pos;
            if (hopT >= 1)
            {
                if (!rigWalk) Kick(0.12f);
                if (pos == walkTo)
                {
                    hopT = -1;
                    lift = 0;
                    Enter(after, Spot, kind);
                    return;
                }
                hopT = 0;
                Look(walkTo.x - pos.x);
                if (Random.value < 0.3f) scene.Fx(scene.Prop(FarmProp.Dust), new Color(1, 1, 1, 0.7f), pos + new Vector2(-face * 20, 4), new Vector2(-face * 30, 20), 0, 0.5f, 26, 40);
            }
        }

        // cử động làm việc theo loại chỗ; nhịp một vòng ~1 giây
        void Work(float dt, float t, ref float rot, ref float extraLift, ref float sx, ref float sy)
        {
            var tool = p.tool.rectTransform;
            Vector2 front = pos + new Vector2(face * 62, 8);
            switch (kind)
            {
                case "veg":
                case "smithy":
                {
                    // giơ lên 0..0,6, bổ xuống 0,6..0,72, rút về 0,72..1
                    float prev = Cycle(t - dt, 0.95f), c = Cycle(t, 0.95f);
                    float a = c < 0.6f ? Mathf.Lerp(-10, 70, Ease(c / 0.6f)) : c < 0.72f ? Mathf.Lerp(70, -55, (c - 0.6f) / 0.12f) : Mathf.Lerp(-55, -10, (c - 0.72f) / 0.28f);
                    tool.localEulerAngles = new Vector3(0, 0, a);
                    rot = c < 0.6f ? Mathf.Lerp(0, 6, c / 0.6f) : c < 0.8f ? -9 : Mathf.Lerp(-9, 0, (c - 0.8f) / 0.2f);
                    if (prev < 0.72f && c >= 0.72f)
                    {
                        Kick(0.1f);
                        if (kind == "veg")
                            for (int i = 0; i < 3; i++)
                                scene.Fx(scene.Prop(FarmProp.Dust), new Color(1, 1, 1, 0.85f), front, new Vector2(Random.Range(-60f, 60f), Random.Range(60f, 140f)), 260, 0.6f, 26, 46);
                        else
                        {
                            for (int i = 0; i < 5; i++)
                                scene.Fx(scene.Prop(FarmProp.Spark), Color.white, front + new Vector2(0, 30), new Vector2(Random.Range(-220f, 220f), Random.Range(80f, 260f)), 520, 0.45f, 26, 10, 300);
                            App.Audio.Play("click", 0.35f, Random.Range(1.3f, 1.6f));
                        }
                    }
                    break;
                }
                case "duck":
                {
                    // đung đưa, mỗi vòng rắc một nắm thóc về phía ao (sau lưng, phía trên)
                    float prev = Cycle(t - dt, 1.5f), c = Cycle(t, 1.5f);
                    rot = Mathf.Sin(c * Mathf.PI * 2) * 6;
                    tool.localEulerAngles = new Vector3(0, 0, c > 0.7f && c < 0.85f ? -35 : 0);
                    if (prev < 0.78f && c >= 0.78f)
                    {
                        Kick(0.08f);
                        for (int i = 0; i < 4; i++)
                            scene.Fx(scene.Prop(FarmProp.Seed), Color.white, pos + new Vector2(face * 40, 70), new Vector2(face * Random.Range(40f, 140f), Random.Range(160f, 260f)), 420, 0.7f, 16, 14, 200);
                    }
                    break;
                }
                case "orchard":
                {
                    // nhảy hái quả: lên đỉnh thì nảy một quả rơi vào giỏ
                    float prev = Cycle(t - dt, 1.8f), c = Cycle(t, 1.8f);
                    if (c < 0.45f)
                    {
                        extraLift = Mathf.Sin(c / 0.45f * Mathf.PI) * 64;
                        sy *= 1.06f;
                    }
                    if (prev < 0.02f && c >= 0.02f) Kick(-0.16f);
                    if (prev < 0.45f && c >= 0.45f) Kick(0.18f);
                    if (prev < 0.22f && c >= 0.22f)
                        scene.Fx(scene.Prop(FarmProp.Apple), Color.white, pos + new Vector2(face * 20, TopH + 40), new Vector2(face * 110, 120), 700, 0.6f, 40, 36, 180, true);
                    break;
                }
                case "bakery":
                {
                    // nhào bột: nén mạnh theo nhịp, thỉnh thoảng khói lò bốc lên
                    float c = Cycle(t, 0.7f);
                    float k = Mathf.Max(0, Mathf.Sin(c * Mathf.PI * 2));
                    sy *= 1 - 0.12f * k;
                    sx *= 1 + 0.08f * k;
                    rot = Mathf.Sin(c * Mathf.PI * 2) * 3;
                    if (Random.value < dt * 0.8f)
                        scene.Fx(scene.Prop(FarmProp.Smoke), new Color(1, 1, 1, 0.8f), pos + new Vector2(-face * 70, 40), new Vector2(Random.Range(-15f, 15f), 70), -10, 1.6f, 36, 80, 15);
                    break;
                }
            }
            // sản phẩm nảy lên
            if ((nextProduct -= dt) <= 0)
            {
                nextProduct = Random.Range(4f, 7f);
                scene.Fx(scene.ProductOf(kind), Color.white, pos + new Vector2(0, TopH + 10), new Vector2(0, 90), 0, 1.3f, 46, 46, 0, true, 1.5f);
            }
        }

        float Cycle(float t, float period) => Mathf.Repeat((t + phase * period) * speed / period, 1);

        static float Ease(float x) => 1 - (1 - x) * (1 - x);
    }
}
