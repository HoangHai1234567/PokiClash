// Tướng aola trên sân đấu: prefab tướng (AolaActor, Assets/04 Prefabs/Heroes) đặt ở xa trong thế giới, một camera riêng render
// ra RenderTexture, RawImage trên sân hiện ảnh đó qua shader viền sticker. Dạng chưa nhập vào project (menu PokiClash/Tướng/
// Nhập hình tướng aola) thì TryCreate trả null và ô tướng trên sân để trống.
// Camera chỉ chụp khi hình đổi (AolaActor.Version: animation 25 khung/giây trên màn 60 khung, khung camera dời), các khung khác tắt và
// RawImage giữ ảnh cũ; cứ 30 khung chụp lại một lần phòng RenderTexture mất nội dung (Android đi nền rồi về).
// Khung camera đi theo thân (2026-11-19, người dùng: "vài tướng khi dùng chiêu bị biến mất kiểu chui vào một cái mask", vd. Tiểu Quỷ
// Lava đâm giáo): camera bám xương move của rig (AolaActor.Follow), ảnh dời ngược lại đúng chừng đó nên trên màn không đổi gì; clip vươn
// xa hơn khung (AtomikAsset.fit) thì camera lùi ra trong lúc clip chạy, viền giấy chia lại cho dày như cũ. Rect là khung ngoài cho nơi
// gọi đặt chỗ, đổi tỉ lệ, bật tắt; ảnh là con của nó, sticker tự dời.
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class AolaSticker
    {
        const float DefSpan = 3.4f; // khung camera mặc định = 3,4 lần chiều cao dáng đứng (đủ chỗ cho clip lao thường)
        // khung của tướng này: rig khai game.span lớn hơn (Viêm Đao: nhát bổ, liên hoàn chém vươn tới 2,9 lần chiều cao quanh chân) thì theo
        // rig để hình không bị mép khung cắt dọc (2026-11-14)
        float Span = DefSpan;
        const float FootV = 0.2f; // chân nằm ở 20% chiều cao ảnh
        // khung nới theo clip (AtomikAsset.fit): chừa mép cho viền giấy, trần để ảnh không nhoè quá (RenderTexture giữ cỡ của Span)
        const float FitMargin = 0.06f, MaxSpan = 8f;
        float curSpan = DefSpan;  // khung camera đang dùng (Span hoặc nới cho clip)
        float uiHeight;           // chiều cao dáng đứng trên UI
        int px;                   // cạnh RenderTexture
        Vector2 follow;           // chỗ xương move (AolaActor.Follow), đơn vị = chiều cao dáng đứng, +y lên
        Vector2 farShift;         // hình aola: khung dời theo đích ở xa (Far), cùng đơn vị
        Vector2 win;              // dời khung camera (cùng đơn vị): tâm ngang, chân khung ở win.y − FootV·cỡ khung (Fit)
        // Khung tự nới theo hình vẽ thật (2026-11-20, quét HeroFrameScan: 161 clip ở 58 dạng bị mép ảnh cắt: hiệu ứng ở chỗ đối thủ,
        // khung dời theo đích làm lọt phía sau, clip aura phủ lên, cú đâm nhanh lọt giữa hai mẫu đo của fit, dạng aola lao xa). Ảnh
        // trên UI có cỡ theo khung và dời ngược đúng chừng camera dời nên đổi khung không làm tướng xê dịch hay to nhỏ trên màn, chỉ đổi
        // độ nét: ưu tiên dời khung; chỉ nới cỡ khi hình rộng hoặc cao hơn khung, nới thì giữ tới hết lần hiện clip đó và nhớ theo clip để
        // lần sau mở sẵn (độ nét không nhảy giữa chừng).
        float winSpan;            // cỡ khung của lần hiện clip đang chạy
        string winClip;           // clip của lần hiện đó
        float winT = -1;          // giờ clip lần gọi trước (lùi lại: clip chạy lại)
        readonly Dictionary<string, float> clipSpan = new(); // cỡ khung lớn nhất mỗi clip đã cần
        static int count, builtFrame = -1;

        // Dựng sticker tốn (prefab, hàng chục hình, RenderTexture có depth): giao diện (hộp chi tiết, đội hình) mỗi khung dựng tối đa
        // một cái và không dựng trong khung chạm, chờ khung sau thì giữ hình cũ hoặc chân dung (người dùng dặn phản hồi phải ngay,
        // 2026-11-07). Sân đấu dựng cả đội lúc vào trận thì không hỏi.
        public static bool CanBuildNow => builtFrame != Time.frameCount;

        public RectTransform Rect { get; private set; }
        RawImage img;
        Material mat;
        AolaActor actor;
        GameObject world;
        Camera cam;
        RenderTexture rt;
        // hạt không viền (AolaActor.SplitFx, rig khai game.plain: hạt lá...): camera thứ hai chụp lưới hạt ở cao FxLift ra RT riêng,
        // ảnh thứ hai (con của ảnh tướng, cùng khung) hiện qua cùng shader nhưng _Plain = 1 (không viền giấy)
        RawImage fxImg;
        Material fxMat;
        Camera fxCam;
        RenderTexture fxRt;
        bool flip;
        float stageHeight; // chiều cao dáng đứng trên sân (đơn vị web)
        int seenVersion = -1, lastShot = -1000; // AolaActor.Version lúc chụp gần nhất, khung (Time.frameCount) chụp gần nhất
        bool camDirty = true; // khung camera vừa dời: chụp lại

        // clip đi bộ của rig .atomik (màn Nhà: tướng đi lại; dạng chưa có clip này thì nơi gọi dùng dáng đứng)
        public const string Walk = "walk";

        static string ClipName(string c) =>
            c == StageView.Attack ? AolaActor.Attack : c == StageView.Skill ? AolaActor.Skill : c == StageView.Cast ? AolaActor.Cast :
            c == StageView.Hit ? AolaActor.Hit : c == AolaActor.Evolve ? AolaActor.Evolve :
            c == AolaActor.Appear || c == AolaActor.Die || c == Walk ? c : AolaActor.Idle;

        // dạng có clip này không (clip tiến hóa: chỉ dạng .atomik có, HeroViewer phát trước khi đổi dạng)
        public bool HasClip(string clip) => actor.HasClip(ClipName(clip));

        // aola: tên dạng cần hiện (HeroDef.Form theo sao). maxPx: cạnh RenderTexture tối đa (mặc định 1024; màn mở khoá tướng hiện tướng
        // to giữa màn thì 2048, đỡ nhoè)
        public static AolaSticker TryCreate(RectTransform parent, HeroDef hero, string aola, float uiHeight, bool flip, int maxPx = 1024)
        {
            if (!AolaActor.Find(aola, out var prefab, out int form)) return null;
            builtFrame = Time.frameCount;
            var actor = Object.Instantiate(prefab, new Vector3(10000 + 50 * (count++ % 40), 0, 0), Quaternion.identity);
            var go = actor.gameObject;
            go.name = "aola_" + hero.id;
            actor.Manual = true;
            actor.SplitFx = true;
            if (!actor.LoadForm(form, 1f, flip, 0))
            {
                Object.Destroy(go);
                return null;
            }
            float span = Mathf.Max(DefSpan, actor.Span);
            var s = new AolaSticker
            {
                actor = actor, world = go, flip = flip, stageHeight = uiHeight / StageView.K, Span = span, curSpan = span, uiHeight = uiHeight
            };
            // khung rộng hơn mặc định: ảnh không cần luỹ thừa 2, trần 1536 (2048 thì mỗi tướng 24 MB kể depth) để giữ độ nét trên sân
            int px = s.px = span > DefSpan
                ? Mathf.Clamp(Mathf.CeilToInt(uiHeight * span / 64f) * 64, 256, Mathf.Max(1536, maxPx))
                : Mathf.Clamp(Mathf.NextPowerOfTwo((int)(uiHeight * span)), 256, maxPx);
            // URP render graph báo lỗi mỗi khung nếu RenderTexture đích của camera không có depth buffer
            s.rt = new RenderTexture(px, px, 16, RenderTextureFormat.ARGB32) { name = "aola_" + hero.id };
            var camGo = new GameObject("cam");
            camGo.transform.SetParent(go.transform, false);
            camGo.transform.localPosition = new Vector3(0, span * (0.5f - FootV), -10);
            var cam = s.cam = camGo.AddComponent<Camera>();
            cam.orthographic = true;
            cam.orthographicSize = span / 2;
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0, 0, 0, 0);
            cam.targetTexture = s.rt;
            cam.nearClipPlane = 0.1f;
            cam.farClipPlane = 50;

            // khung ngoài: nơi gọi đặt chỗ, đổi tỉ lệ, bật tắt (cỡ, chân như ảnh cũ); ảnh: con, chân trùng chân khung ngoài, sticker tự dời
            s.Rect = (RectTransform)new GameObject("aola", typeof(RectTransform)).transform;
            s.Rect.SetParent(parent, false);
            s.Rect.anchorMin = s.Rect.anchorMax = new Vector2(0.5f, 0);
            s.Rect.pivot = new Vector2(0.5f, FootV);
            s.Rect.sizeDelta = new Vector2(uiHeight * span, uiHeight * span);
            s.img = new GameObject("anh", typeof(RectTransform)).AddComponent<RawImage>();
            var ir = s.img.rectTransform;
            ir.SetParent(s.Rect, false);
            ir.anchorMin = ir.anchorMax = ir.pivot = new Vector2(0.5f, FootV);
            ir.sizeDelta = new Vector2(uiHeight * span, uiHeight * span);
            s.img.texture = s.rt;
            s.img.raycastTarget = false;
            var baseMat = Theme.Assets ? Theme.Assets.sticker : null;
            if (baseMat)
            {
                s.mat = new Material(baseMat);
                // bề dày viền tính bằng điểm ảnh của ảnh chụp: khung rộng hơn thì cùng số điểm ảnh ra viền dày hơn trên sân, nên chia lại
                s.mat.SetFloat("_White", 3f * px / 512f * DefSpan / span);
                s.mat.SetFloat("_Ink", 2.5f * px / 512f * DefSpan / span);
                s.img.material = s.mat;
            }
            if (actor.HasPlainFx) s.MakeFxLayer(px, baseMat);
            return s;
        }

        void MakeFxLayer(int px, Material baseMat)
        {
            fxRt = new RenderTexture(px, px, 16, RenderTextureFormat.ARGB32) { name = rt.name + "_fx" };
            var camGo = new GameObject("cam_fx");
            camGo.transform.SetParent(world.transform, false);
            fxCam = camGo.AddComponent<Camera>();
            fxCam.CopyFrom(cam); // CopyFrom chép cả vị trí: đặt lại sau
            camGo.transform.localPosition = cam.transform.localPosition + new Vector3(0, AolaActor.FxLift, 0);
            fxCam.targetTexture = fxRt;
            fxImg = new GameObject("aola_fx", typeof(RectTransform)).AddComponent<RawImage>();
            var r = fxImg.rectTransform;
            r.SetParent(img.rectTransform, false); // cùng khung, dời theo ảnh tướng
            r.anchorMin = Vector2.zero;
            r.anchorMax = Vector2.one;
            r.offsetMin = r.offsetMax = Vector2.zero;
            fxImg.texture = fxRt;
            fxImg.raycastTarget = false;
            if (baseMat)
            {
                fxMat = new Material(baseMat);
                fxMat.SetFloat("_Plain", 1f);
                fxImg.material = fxMat;
            }
        }

        // chiêu bắn của tướng không có clip bắn (1_5): đứng dáng đứng, sân tự nhún tới (StageView.Place), tia phóng ở giữa
        public const float CastLen = 0.6f;
        public bool HasCast => actor.HasClip(AolaActor.Cast);
        public bool ManaUsesClip => actor.ManaUsesClip;

        public float Duration(string clip) =>
            clip == StageView.Cast && !HasCast ? CastLen :
            clip == StageView.Skill && Jumps ? SkillLen + actor.Duration(AolaActor.SkillLand) : actor.Duration(ClipName(clip));

        public float HitTime(string clip) =>
            clip == StageView.Cast && !HasCast ? CastLen * 0.5f :
            clip == StageView.Skill && Jumps ? SkillLen + LandHit : actor.HitFrame(ClipName(clip)) / actor.Fps;

        // Chiêu cuối nhảy đè, hai clip (người dùng 2026-11-11, Tí Tách): "skill" (phình, nhún, bật; hết clip là dáng đang bay) rồi
        // "skill_land" (rơi, bẹp nặng, nảy). Nơi gọi coi như MỘT clip Skill dài bằng tổng hai clip (Duration, Show); khung trúng là
        // lúc chạm của clip sau (HitTime); cung nhảy tới chỗ đối thủ và cú bật về do Jump tính.
        public bool Jumps => actor.HasClip(AolaActor.Skill) && actor.HasClip(AolaActor.SkillLand);
        float SkillLen => actor.Duration(AolaActor.Skill);
        float JumpOff => actor.HitFrame(AolaActor.Skill) / actor.Fps;     // sự kiện "bat": rời đất
        float LandHit => actor.HitFrame(AolaActor.SkillLand) / actor.Fps; // sự kiện "cham_dat"
        const float JumpStay = 0.16f, JumpBack = 0.42f;                   // đè trên chỗ đáp, rồi bật về chỗ cũ (giây)
        // Chiêu cuối TÔNG THẲNG (người dùng 2026-11-12, Cầu Gai: "xoay liên tục rồi tông thẳng vào đối thủ, tông xong bị bật ngược
        // về chỗ cũ"): rig khai sự kiện "tong" trong clip skill_land. Bay gần như ngang, nhanh dần, tới THÂN đối thủ (không rơi từ
        // trên xuống đầu); nơi gọi đặt chỗ đáp ngang thân (StageView.Place).
        public bool Rams => Jumps && actor.EventTime(AolaActor.SkillLand, "tong") >= 0;

        // Độ dời của cú nhảy ở giây t của clip Skill. to: chỗ đáp so với chân (x theo màn, y LÊN là dương), h: chiều cao tướng,
        // cùng đơn vị; o trả cùng đơn vị, y lên là dương. false: clip này không phải chiêu nhảy.
        public bool Jump(string clip, float t, Vector2 to, float h, out Vector2 o)
        {
            o = Vector2.zero;
            if (clip != StageView.Skill || !Jumps) return false;
            float t0 = JumpOff, t1 = SkillLen + LandHit;
            if (t <= t0) return true;
            if (t < t1)
            {
                // bay theo parabol: ngang đều, đỉnh cao hơn chỗ đáp để rơi từ trên xuống
                float u = (t - t0) / Mathf.Max(0.01f, t1 - t0);
                if (Rams)
                {
                    // tông thẳng: nhanh dần tới lúc chạm, chỉ nhấc nhẹ khỏi đất
                    float v2 = u * u * (0.4f + 0.6f * u);
                    o = new Vector2(to.x * v2, to.y * v2 + h * 0.10f * 4 * u * (1 - u));
                    return true;
                }
                float up = Mathf.Max(0, to.y) * 0.35f + h * 0.85f;
                o = new Vector2(to.x * u, to.y * u + up * 4 * u * (1 - u));
                return true;
            }
            float v = (t - t1 - JumpStay) / JumpBack;
            if (v <= 0)
            {
                o = to;
                return true;
            }
            if (v >= 1) return true;
            float s = v * v * (3 - 2 * v);
            // tông thẳng: bị bật ngược về theo VÒNG CUNG cao (người dùng 2026-11-12); nhảy đè: nảy thấp về chỗ
            o = new Vector2(to.x * (1 - s), to.y * (1 - s) + h * (Rams ? 0.85f : 0.4f) * 4 * v * (1 - v));
            return true;
        }

        // Tâm hình đang hiện so với chân, đơn vị sân (y xuống), đo theo khung bao các lưới của tướng (bỏ lớp hạt không viền đặt cao FxLift).
        // Sân dùng để đặt hiệu ứng đúng chỗ thân đang nằm trong clip chết (clip chết hay dời thân khỏi chỗ đứng; 2026-11-17, StageViewShow).
        public bool Center(out Vector2 c)
        {
            c = Vector2.zero;
            if (!actor || !world) return false;
            var o = actor.transform.position;
            var b = new Bounds();
            bool any = false;
            foreach (var r in world.GetComponentsInChildren<Renderer>())
            {
                if (!r.enabled || r.bounds.size.sqrMagnitude <= 1e-8f || Mathf.Abs(r.bounds.center.y - o.y) > 50) continue;
                if (!any) b = r.bounds;
                else b.Encapsulate(r.bounds);
                any = true;
            }
            if (!any) return false;
            c = new Vector2((b.center.x - o.x) * stageHeight, -(b.center.y - o.y) * stageHeight);
            return true;
        }

        // clip tự diễn đoạn giữ chiêu: không ghìm giờ clip ở khung nhả (AolaActor.SelfHold)
        public bool SelfHold(string clip) => actor.SelfHold(ClipName(clip));
        // giờ của một sự kiện trong clip rig (-1: không có): sân dùng "cham_dat" của clip ra sân để rung màn lúc tướng nện đất
        public float EventTime(string clip, string name) => actor.EventTime(ClipName(clip), name);
        // lần thứ nth (0 = đầu) của sự kiện khai nhiều lần
        public float EventTime(string clip, string name, int nth) => actor.EventTime(ClipName(clip), name, nth);

        // Chỗ xương `bone` ở giây t của clip so với chân (đơn vị sân, y xuống, đã lật theo phía), chưa tính cú lao của sân; false: rig không có
        public bool BoneAt(string clip, string bone, float t, out Vector2 p)
        {
            p = Vector2.zero;
            if (!actor || !actor.BoneAt(ClipName(clip), bone, t, out var b)) return false;
            float k = stageHeight / Mathf.Max(1, actor.IdleHeightPx);
            p = new Vector2((flip ? -b.x : b.x) * k, -b.y * k);
            return true;
        }

        // Chiêu bắn tia (AolaActor.Beam): chỗ bắn so với chân (đơn vị sân, y xuống, đã lật theo phía) và cỡ tia; không khai: false
        public bool Beam(out Vector2 muzzle, out float scale)
        {
            muzzle = Vector2.zero;
            if (!actor.Beam(out var m, out scale)) return false;
            float k = stageHeight / Mathf.Max(1, actor.IdleHeightPx);
            muzzle = new Vector2((flip ? -m.x : m.x) * k, m.y * k);
            return true;
        }

        // kiểu tia riêng (AolaActor.BeamStyle: tia_bang, tia_xoay, tia_trieu của 3 boss cuối đảo Thủy); null = tia nước thường
        public string BeamStyle => actor ? actor.BeamStyle : null;

        // cảm giác trúng của clip sân (AolaActor.Impact)
        public bool Impact(string clip, out float stop, out float shake, out float push, out string flash)
        {
            stop = shake = push = 0;
            flash = null;
            return actor && actor.Impact(ClipName(clip), out stop, out shake, out push, out flash);
        }

        // clip đứng một chỗ bắn (AolaActor.Stays): sân không tự nhún tới đối thủ
        public bool Stays(string clip) => actor && actor.Stays(ClipName(clip));

        // Độ lệch thêm (đơn vị sân) để đỉnh lao của clip đánh rơi vào 72% quãng tới đối thủ: A·m(t) − m(t) như bản web.
        // Clip khác (chiêu cuối) chỉ lao khi anim.json khai "lunge" (AolaActor.Lunges).
        public bool Lunge(string clip, float t, float tx, float ty, out Vector2 o)
        {
            o = Vector2.zero;
            var name = ClipName(clip);
            if (!actor.Lunges(name) || !actor.HasClip(name)) return false;
            int n = actor.FrameCount(name);
            int fi = Mathf.Min(n - 1, Mathf.FloorToInt(t * actor.Fps));
            float scale = stageHeight / Mathf.Max(1, actor.IdleHeightPx);
            var d = actor.Disp(name, fi);
            var pk = actor.Disp(name, actor.PeakFrame(name));
            float mx = (flip ? -d.x : d.x) * scale, my = d.y * scale;
            float Mx = (flip ? -pk.x : pk.x) * scale, My = pk.y * scale;
            float M = Mathf.Sqrt(Mx * Mx + My * My);
            if (M <= 30) return false; // clip bắn từ xa: sân đấu tự nhún tới
            float k = Mathf.Sqrt(tx * tx + ty * ty) / M;
            float ang = Mathf.Atan2(ty, tx) - Mathf.Atan2(My, Mx);
            float cs = Mathf.Cos(ang) * k, sn = Mathf.Sin(ang) * k;
            o = new Vector2(mx * cs - my * sn - mx, mx * sn + my * cs - my);
            return true;
        }

        // Chỗ bắn tính theo chiều cao dáng đứng (1 = cao bằng tướng; x theo phía đang quay, y xuống): nơi vẽ tướng ở cỡ khác
        // (khung xem tướng) tự nhân với chiều cao của nó
        public bool BeamUnit(out Vector2 muzzle)
        {
            muzzle = Vector2.zero;
            if (!Beam(out var m, out _)) return false;
            muzzle = m / Mathf.Max(1e-4f, stageHeight);
            return true;
        }

        // Hiệu ứng ở xa của clip (đạn bay, vụ nổ ở chỗ đối thủ của trận gốc, AolaActor.FarTarget): to = đối thủ so với chân
        // (đơn vị sân, y xuống); null hoặc clip không có: như bản gốc. Rig .atomik: khung camera tự dời / nới cho hiệu ứng ở đích (Fit).
        // Hình aola (giữ như cũ, người dùng 2026-11-20 chỉ sửa .atomik): shift = khung dời về phía đối thủ nửa quãng, ảnh dời ngược lại
        // để thân đứng yên trên sân (sân đấu; nơi tự đặt chỗ ảnh thì không dịch).
        public void Far(string clip, Vector2? to, bool shift = true)
        {
            var name = ClipName(clip);
            if (to == null || !actor.HasFar(name))
            {
                actor.SetFarTarget(null);
                if (shift) farShift = Vector2.zero;
                return;
            }
            float h = Mathf.Max(1, stageHeight);
            var d = to.Value;
            actor.SetFarTarget(new Vector2((flip ? -d.x : d.x) / h, -d.y / h));
            // Đích ở TRÊN (khung sẵn có 2,7 chiều cao phía trên chân): chỉ dời lên khi đích cao quá 1,9 chiều cao, vì dời lên là mất phần
            // dưới chân (đuôi Linh Điểu thõng dưới chân bị cắt ngang lúc ra chiêu mana).
            float up = -d.y / h;
            if (shift) farShift = new Vector2(Mathf.Clamp(d.x / h * 0.5f, -1.1f, 1.1f), up > 0 ? Mathf.Clamp(up - 1.9f, 0, 0.8f) : Mathf.Max(up * 0.5f, -0.8f));
        }

        // khung xem tướng (không có đối thủ): hiệu ứng ở xa hiện trước mặt, cách chân heights lần chiều cao, trong khung camera
        public void FarAhead(string clip, float heights) =>
            Far(clip, new Vector2((flip ? -1 : 1) * heights * stageHeight, -0.4f * stageHeight), false);

        // Khung camera cho tư thế vừa dựng: khung nền (khung của tướng nới theo fit đo lúc nhập, hoặc cỡ lần hiện trước của clip này) đặt
        // ngang theo thân, chân ở FootV; hình vẽ thật (AolaActor.Drawn) cộng lề viền giấy lọt ra thì dời khung vừa đủ, rộng / cao hơn khung
        // thì nới cỡ (trần MaxSpan; quá trần thì giữ thân trong khung).
        void Fit(string clip, float t)
        {
            if (!actor.IsAtomik) // hình aola: như cũ (khung của tướng, dời theo đích ở xa nửa quãng)
            {
                SetSpan(SpanFor(clip));
                win = farShift + follow;
                return;
            }
            if (clip != winClip || t < winT - 1e-3f)
            {
                winClip = clip;
                winSpan = SpanFor(clip);
                if (clipSpan.TryGetValue(clip, out float prev)) winSpan = Mathf.Max(winSpan, prev);
            }
            winT = t;
            float cap = Mathf.Max(Span, MaxSpan);
            float cx = follow.x, cy = follow.y + (0.5f - FootV) * winSpan; // tâm khung nền
            if (actor.Drawn(out var lo, out var hi))
            {
                lo -= new Vector2(FitMargin, FitMargin);
                hi += new Vector2(FitMargin, FitMargin);
                float need = Mathf.Min(Mathf.Max(hi.x - lo.x, hi.y - lo.y), cap);
                if (need > winSpan)
                {
                    winSpan = need;
                    clipSpan[clip] = clipSpan.TryGetValue(clip, out float had) ? Mathf.Max(had, need) : need;
                    cy = follow.y + (0.5f - FootV) * winSpan;
                }
                cx = Contain(cx, lo.x, hi.x, winSpan);
                cy = Contain(cy, lo.y, hi.y, winSpan);
            }
            SetSpan(winSpan);
            win = new Vector2(cx, cy - (0.5f - FootV) * winSpan);
        }

        // tâm khung cạnh s gần c nhất mà khung chứa đoạn [lo, hi]; đoạn dài hơn khung (quá trần): giữ c (thân). Dung sai: khung vừa
        // nới đúng bằng đoạn, so ngặt thì sai số làm tròn (Mono tính hiệu ở độ chính xác cao hơn float) đẩy sang nhánh "dài hơn".
        static float Contain(float c, float lo, float hi, float s) =>
            hi - lo > s + 1e-3f ? c : Mathf.Clamp(c, hi - s / 2, lo + s / 2);

        // đặt khung camera theo Fit, ảnh dời ngược lại cùng chừng đó: thân đứng đúng chỗ trên màn
        void Frame()
        {
            if (!cam) return;
            var w = win;
            var lp = new Vector3(w.x, curSpan * (0.5f - FootV) + w.y, -10);
            if (cam.transform.localPosition != lp)
            {
                cam.transform.localPosition = lp;
                if (fxCam) fxCam.transform.localPosition = lp + new Vector3(0, AolaActor.FxLift, 0);
                camDirty = true;
                cam.enabled = true;
                if (fxCam) fxCam.enabled = true;
            }
            img.rectTransform.anchoredPosition = w * uiHeight;
        }

        // khung camera cho clip đang hiện: khung của tướng (Span), nới khi số đo của clip vươn xa hơn (AtomikAsset.fit)
        float SpanFor(string actorClip)
        {
            if (!actor.Extent(actorClip, out float mx, out float top, out float bot)) return Span;
            float need = Mathf.Max(2 * (mx + FitMargin), (top + FitMargin) / (1 - FootV), (FitMargin - bot) / FootV);
            return Mathf.Clamp(need, Span, Mathf.Max(Span, MaxSpan));
        }

        // đổi khung camera: cỡ chụp, cỡ ảnh trên UI, viền giấy chia lại theo khung (RenderTexture giữ nguyên cỡ)
        void SetSpan(float s)
        {
            if (!cam || Mathf.Abs(s - curSpan) < 1e-3f) return;
            curSpan = s;
            cam.orthographicSize = s / 2;
            if (fxCam) fxCam.orthographicSize = s / 2;
            img.rectTransform.sizeDelta = new Vector2(uiHeight * s, uiHeight * s);
            if (mat)
            {
                mat.SetFloat("_White", 3f * px / 512f * DefSpan / s);
                mat.SetFloat("_Ink", 2.5f * px / 512f * DefSpan / s);
            }
            camDirty = true;
        }

        // bật camera đúng khung hình đổi; trong cùng một khung đã bật thì giữ (Show gọi hai lần không tắt mất lần chụp)
        void SyncCamera()
        {
            if (!cam) return;
            int now = Time.frameCount;
            if (lastShot == now) return;
            bool shoot = camDirty || actor.Version != seenVersion || now - lastShot > 30 || !rt.IsCreated() ||
                         (fxRt && !fxRt.IsCreated());
            cam.enabled = shoot;
            if (fxCam) fxCam.enabled = shoot;
            if (!shoot) return;
            seenVersion = actor.Version;
            camDirty = false;
            lastShot = now;
        }

        // khung này không Show (ngoài khung nhìn, đứng yên, vẽ thưa khung): tắt camera, RenderTexture giữ lần chụp cuối. Không gọi thì
        // camera giữ trạng thái của lần Show cuối, có thể vẽ lại mỗi khung dù hình không đổi (đo 2026-11-18: 10 tướng đảo vùng đất
        // chiếm 102k / 109k tris)
        public void Hold()
        {
            if (!cam || lastShot == Time.frameCount) return;
            cam.enabled = false;
            if (fxCam) fxCam.enabled = false;
        }

        // nhân màu hình (1: nguyên màu; đảo vùng đất: tướng ở vùng boss chưa mở tô tối, ZoneSceneLand)
        public float Tint = 1;

        // sáng thêm (shader _Lift: nhân 1 + Lift; màn Nhà ban đêm cho tướng sáng hơn cảnh đã nhuộm tối)
        public float Lift;

        public void Show(string clip, float t, bool loop, float alpha, bool gray, float flash)
        {
            // hình aola theo khung (floor t·fps), rig .atomik theo thời gian liên tục (AolaActor.ShowTime)
            // chiêu cuối hai clip: hết "skill" thì chạy tiếp "skill_land" (khung cuối clip trước trùng khung đầu clip sau)
            string shown = clip == StageView.Skill && !loop && Jumps && t >= SkillLen ? AolaActor.SkillLand : ClipName(clip);
            if (shown == AolaActor.SkillLand) actor.ShowTime(shown, t - SkillLen, false);
            else actor.ShowTime(shown, t, loop);
            follow = actor.Follow;
            Fit(actor.HasClip(shown) ? shown : AolaActor.Idle, t);
            Frame();
            SyncCamera();
            img.color = new Color(Tint, Tint, Tint, alpha);
            if (mat)
            {
                mat.SetFloat("_Gray", gray ? 1 : 0);
                mat.SetFloat("_Flash", Mathf.Min(1, flash * 5) * 0.65f);
                mat.SetFloat("_Lift", Lift);
            }
            if (fxImg)
            {
                fxImg.color = new Color(Tint, Tint, Tint, alpha);
                if (fxMat)
                {
                    fxMat.SetFloat("_Gray", gray ? 1 : 0);
                    fxMat.SetFloat("_Lift", Lift);
                }
            }
        }

        // bỏ bóng dưới chân (màn boot)
        public void HideShadow() => actor.HideShadow = true;

        // Xoá cả ảnh trên UI, RT và material. Nơi dựng lại trong cùng khung (ô xem tướng khi tiến hóa, đội hình màn Tướng) mà để
        // sót ảnh cũ thì nó trỏ vào RT đã giải phóng: trên Android hiện thành ô đen đặc che sau tướng mới.
        public void Destroy()
        {
            if (cam) cam.enabled = false;
            if (fxCam) fxCam.enabled = false;
            if (Rect) Object.Destroy(Rect.gameObject); // ảnh tướng, ảnh hạt là con, đi theo
            if (world) Object.Destroy(world);
            if (rt)
            {
                rt.Release();
                Object.Destroy(rt);
            }
            if (fxRt)
            {
                fxRt.Release();
                Object.Destroy(fxRt);
            }
            if (mat) Object.Destroy(mat);
            if (fxMat) Object.Destroy(fxMat);
        }
    }
}
