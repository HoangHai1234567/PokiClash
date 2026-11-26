// Lão Mực, dealer của Bến Lữ Khách (GD_Claude/31_LaoMuc_Dealer.md, mốc D3): một rig AtomSpine (.atomik nạp từ TextAsset như rương
// máy bi) vẽ thành HAI lớp UI dùng chung một trạng thái: lớp sau (thân, mặt, lưỡi trai) nằm sau mặt bàn, lớp trước (ống tay, nịt tay,
// nơ, bàn tay, lá bài trên tay) nằm trên mặt bàn và đồ trên bàn (bài, chip), đúng lớp vẽ ở mục 3 của kế hoạch.
// - Toạ độ: gốc rig (giữa hai bàn chân) ở gốc RectTransform của lớp; 1 px rig = scale đơn vị canvas. Mép bàn sau là y = TableY trong rig.
// - Clip một lần tự nối về idle (hoặc clip kế trong hàng chờ). Thiếu clip (rig cũ chưa có clip mới) thì bỏ qua, báo xong ngay để màn
//   không kẹt.
// - Sự kiện của clip (cham_chip, vo_xong, tra_chip, bung, lat...) bắn qua Fired; vị trí bàn tay lấy bằng BoneCanvas("tay_pb").
// Mọi vật dựng sẵn trong prefab (menu "PokiClash/Prefab/Đảo Casino/Lều lữ khách: dựng 3 scene"); ở đây không sinh GameObject.
using System;
using System.Collections.Generic;
using AtomSpine;
using UnityEngine;

namespace PokiClash
{
    public sealed class DealerRig : MonoBehaviour
    {
        public const float TableY = 500f;   // mép bàn sau trong thế giới rig (ArtGen/Casino/dealer/rig/dong_co.py TABLE_Y)
        public const string Idle = "idle";

        [SerializeField] TextAsset rigFile;
        [SerializeField] DealerLayer back, front;
        [SerializeField] float scale = 0.79f;
        // slot vẽ ở lớp trước (trên mặt bàn): tên bắt đầu bằng một trong các tiền tố này (ống tay, nịt tay, nơ, bàn tay, lá bài trên tay,
        // lá xoè bài); còn lại (thân, mặt, giọt mồ hôi, lưỡi trai) vẽ ở lớp sau. Theo tiền tố để slot mới của rig tự vào đúng lớp.
        [SerializeField] string[] frontPrefixes = { "tay_", "nit_", "no", "ban_tay_", "la_", "xao_" };

        public float Scale => scale;
        public AtomikAsset Asset { get; private set; }
        public AtomikState State { get; private set; }
        public string Current => State?.CurrentName;
        public bool IsIdle => State == null || State.CurrentName == Idle && State.QueueCount == 0;
        public event Action<string> Fired;

        static readonly Dictionary<int, AtomikAsset> cache = new Dictionary<int, AtomikAsset>();
        bool[] frontMask;
        Action onDone;
        string doneClip;
        bool scrubbing;      // đang kéo thời gian bằng tay (Scrub): Update không tự chạy clip
        float scrubMix;

        // Dùng khi dựng prefab (Editor).
        public void Setup(TextAsset file, DealerLayer backLayer, DealerLayer frontLayer, float pxScale)
        {
            rigFile = file;
            back = backLayer;
            front = frontLayer;
            scale = pxScale;
        }

        public bool Ready()
        {
            if (State != null) return true;
            if (!rigFile) return false;
            int key = rigFile.GetInstanceID();
            if (!cache.TryGetValue(key, out var a) || !a)
            {
                try
                {
                    a = AtomikFile.Load(rigFile.bytes);
                }
                catch (Exception e)
                {
                    Debug.LogWarning("[Lão Mực] Không nạp được rig " + rigFile.name + ": " + e.Message);
                    a = null;
                }
                cache[key] = a;
            }
            if (!a) return false;
            Asset = a;
            State = new AtomikState(a);
            State.EventFired += (n, s) => Fired?.Invoke(n);
            State.Completed += OnCompleted;
            State.SetOverlay("");
            frontMask = new bool[a.slots.Length];
            for (int i = 0; i < a.slots.Length; i++)
            {
                string n = a.slots[i].name;
                foreach (var pre in frontPrefixes)
                    if (n.StartsWith(pre, StringComparison.Ordinal)) { frontMask[i] = true; break; }
            }
            State.Start(a.FindClip(Idle), true, 0, 0, false);
            if (back) back.Bind(this, frontMask, false);
            if (front) front.Bind(this, frontMask, true);
            return true;
        }

        public bool Has(string clip) => Ready() && Asset.FindClip(clip) >= 0;

        /// <summary>Phát clip một lần rồi về idle; done gọi khi clip hết (hoặc ngay khi rig không có clip đó).</summary>
        public void Play(string clip, Action done = null, float mix = 0.1f)
        {
            if (!Has(clip))
            {
                done?.Invoke();
                return;
            }
            FinishPending();
            scrubbing = false;
            onDone = done;
            doneClip = clip;
            State.Play(clip, false, mix);
            State.Enqueue(Idle, true, 0.12f);
        }

        /// <summary>Phát clip lặp (talk...) tới khi gọi Play / Stop.</summary>
        public void Loop(string clip, float mix = 0.12f)
        {
            if (!Has(clip)) return;
            FinishPending();
            scrubbing = false;
            State.Play(clip, true, mix);
        }

        public void Stop(float mix = 0.15f)
        {
            if (!Ready()) return;
            FinishPending();
            scrubbing = false;
            if (State.CurrentName != Idle) State.Play(Idle, true, mix);
        }

        /// <summary>Kéo thời gian một clip LẶP theo tham số ngoài (Vòng Xoay: rl_watch theo góc viên bi): mỗi khung gọi một lần với
        /// thời điểm trong clip (giây) và dt thật. Lần đầu hoà từ dáng đang có sang trong ~0,2 giây thật; sau đó dáng bám đúng
        /// thời điểm đưa vào. Dừng bằng EndScrub hoặc Play / Loop / Stop.</summary>
        public void Scrub(string clip, float time, float dt)
        {
            if (!Has(clip)) return;
            int i = Asset.FindClip(clip);
            float dur = Asset.anims[i].dur;
            if (dur <= 0) return;
            time = Mathf.Repeat(time, dur);
            if (!scrubbing || State.CurrentName != clip)
            {
                FinishPending();
                State.ClearQueue();
                scrubbing = true;
                scrubMix = 0.2f;
            }
            if (scrubMix > 0)
            {
                // chụp lại dáng đang hoà rồi hoà tiếp về dáng của thời điểm mới: phần hoà chạy theo giờ thật, không theo tốc độ kéo
                scrubMix = Mathf.Max(0, scrubMix - Mathf.Max(0, dt));
                State.Start(i, true, scrubMix + Mathf.Max(1e-4f, dt), time, false);
                State.Advance(Mathf.Max(1e-4f, dt));
                State.ClearQueue();
            }
            else State.Seek(time);
        }

        /// <summary>Thôi kéo thời gian: clip đang kéo chạy tiếp như clip lặp (thường gọi Play clip khác ngay sau).</summary>
        public void EndScrub() => scrubbing = false;

        void FinishPending()
        {
            var d = onDone;
            onDone = null;
            doneClip = null;
            d?.Invoke();
        }

        void OnCompleted(string clip)
        {
            if (clip != doneClip) return;
            var d = onDone;
            onDone = null;
            doneClip = null;
            d?.Invoke();
        }

        /// <summary>Vị trí thế giới (canvas) của một xương theo tư thế hiện tại.</summary>
        public Vector3 BoneWorld(string bone)
        {
            var rt = back ? back.rectTransform : (RectTransform)transform;
            if (!Ready()) return rt.position;
            int b = Asset.FindBone(bone);
            if (b < 0) return rt.position;
            State.Apply();
            var p = State.pose.BonePos(b) * scale;
            return rt.TransformPoint(new Vector3(p.x, p.y, 0));
        }

        /// <summary>Điểm rig (px, y lên, gốc giữa hai chân) đổi ra toạ độ thế giới canvas.</summary>
        public Vector3 RigToWorld(Vector2 rig)
        {
            var rt = back ? back.rectTransform : (RectTransform)transform;
            return rt.TransformPoint(new Vector3(rig.x * scale, rig.y * scale, 0));
        }

        void Update()
        {
            if (!Ready()) return;
            if (Application.isPlaying && !scrubbing) State.Advance(Time.deltaTime);
            State.Apply();
            if (back) back.SetVerticesDirty();
            if (front) front.SetVerticesDirty();
        }

        void OnDisable() => FinishPending();
    }
}
