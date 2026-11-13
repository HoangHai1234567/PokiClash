// Một rig .atomik đã nhập (Editor/AtomikImporter): xương, slot (thứ tự vẽ), hình lưới có trọng số, animation, atlas, material.
// Định dạng riêng của PokiClash, xuất từ ArtGen/Spine/atomik.py (đọc JSON Spine 4.2 do bộ rig tự viết sinh ra). Đơn vị pixel,
// y lên, gốc ở chân; AtomikPlayer chia cho ppu khi dựng lưới.
using System;
using UnityEngine;

namespace PokiClash.Game
{
    [Serializable]
    public sealed class AtomikBone
    {
        public string name;
        public int parent = -1;
        public float x, y, rot;
        public float sx = 1, sy = 1;
        public bool noScale;      // nhận vị trí, góc của cha, bỏ tỉ lệ (thân dẹp giãn không làm méo tay, vũ khí)
    }

    [Serializable]
    public sealed class AtomikSlot
    {
        public string name;
        public int bone;
        public int att = -1;      // hình mặc định (chỉ số trong atts), -1 = trống
        public float fade;        // bản 3: độ mờ mặc định (0 hiện đủ, 1 ẩn). Slot hiệu ứng ẩn sẵn, clip bật bằng khoá sa. Rig cũ: 0
    }

    [Serializable]
    public sealed class AtomikAtt
    {
        public int slot;
        public string name;
        public float[] uvs;       // UV Unity theo atlas, 2 số mỗi đỉnh
        public int[] tris;
        public float[] wInfo;     // mỗi đỉnh: n, rồi n lần (xương, x, y, trọng số) theo xương ở tư thế gốc
    }

    [Serializable]
    public sealed class AtomikTimeline
    {
        public int bone;
        public int type;          // 0 xoay (sải 7), 1 dời, 2 tỉ lệ (sải 12)
        public float[] keys;      // [t, giá trị..., kiểu (0 thẳng, 1 bậc, 2 bezier), điểm điều khiển...]; rỗng khi đã gọn
        public AtomikCurve c;     // khoá gọn (AtomikImporter đổi từ keys, 2026-11-13)
    }

    // Khoá gọn: giờ, giá trị (dim số mỗi khoá), chỉ khoá không nối thẳng mới ghi kiểu và điểm điều khiển. Khoá trong file .atomik
    // luôn chừa ô điểm điều khiển (sải 7 hay 12) dù gần như mọi khoá đều nối thẳng (0 trong 1,48 triệu khoá ngày 2026-11-13 là bezier),
    // nên bản build mang toàn số 0: 44 MB khoá thành ~12 MB.
    [Serializable]
    public sealed class AtomikCurve
    {
        public float[] t;         // giờ từng khoá, tăng dần
        public float[] v;         // giá trị: dim số mỗi khoá
        public int[] ck;          // chỉ số khoá không nối thẳng, tăng dần (thường rỗng)
        public float[] cp;        // mỗi khoá trong ck: [kiểu (1 bậc, 2 bezier), 4 x dim điểm điều khiển như trong keys]
    }

    [Serializable]
    public sealed class AtomikSlotKeys
    {
        public int slot;
        public float[] times;
        public int[] atts;
    }

    // độ đậm của slot theo thời gian (bản 2): hiệu ứng hiện dần, tan dần; sải 7 như khoá xoay [t, a, kiểu, c1..c4]
    [Serializable]
    public sealed class AtomikAlphaKeys
    {
        public int slot;
        public float[] keys;
        public AtomikCurve c;     // khoá gọn như AtomikTimeline.c
    }

    // sự kiện của clip (bản 3): mốc cho VFX, âm thanh (đầu nào bắt đầu phun, khung cắn trúng...). AtomikPlayer.Fired bắn ra khi
    // đầu phát đi qua giây t.
    [Serializable]
    public sealed class AtomikEvent
    {
        public float t;
        public string name;
        public string s;          // chuỗi kèm (vd. tên đầu), có thể rỗng
    }

    [Serializable]
    public sealed class AtomikClip
    {
        public string name;
        public float dur;
        public AtomikTimeline[] tls;
        public AtomikSlotKeys[] sk;
        public AtomikAlphaKeys[] sa;   // bản 2
        public AtomikEvent[] ev;       // bản 3, xếp theo giờ
    }

    // Mặt nạ cắt (bản 3, từ attachment "clipping" của Spine): mọi hình trong các slot từ slot tới end (theo thứ tự vẽ) chỉ còn phần
    // nằm TRONG đa giác. Đa giác lồi, bám một xương, luôn bật. Dùng cho thân trồi lên từ nước: phần dưới mép cắt biến mất, sóng
    // trước (ngoài khoảng slot) phủ lên đường cắt. AtomikPose.Skin cắt tam giác trên CPU.
    [Serializable]
    public sealed class AtomikMask
    {
        public int slot, end;
        public int bone;
        public float[] verts;     // x, y từng đỉnh theo xương bone (pixel, y lên)
    }

    // Thông tin trận của rig dùng làm dạng tướng (bản 2, AolaActor đọc): khung trúng, clip lao, chỗ bắn tia. Toạ độ theo pixel
    // rig, y lên, gốc ở chân (xương root).
    [Serializable]
    public sealed class AtomikGame
    {
        public float fps = 25;          // trận chạy theo khung như hình aola
        public float height;            // chiều cao dáng đứng (đỉnh khung đầu clip idle tới chân)
        public string[] hitClips;       // clip có khung trúng khai sẵn
        public float[] hitTimes;        // giây, cùng thứ tự hitClips
        public string[] lunge;          // clip ngoài attack cũng lao tới đối thủ
        public string[] stay;           // clip đứng tại chỗ dù xương move dời xa
        public string[] far;            // clip có hiệu ứng ở xa: xương "far" dời tới chỗ đối thủ, xương "fly*" (đạn) dời theo quãng đã bay
        // clip (trong far) mà mảnh bay phải CHĨA theo hướng bay thật (lá cánh Linh Điểu, người dùng 2026-11-12: "hướng lá có cùng vectơ
        // hướng bắn"): xương con của mỗi xương "fly*" xoay thêm góc lệch giữa hướng tới đích thật và hướng tới đích trong rig
        public string[] farAim;
        public float[] muzzle;          // [x, y] chỗ bắn tia ở khung trúng của clip cast; rỗng = không có chiêu bắn tia
        public float beam = 1;          // cỡ tia
        public string beamStyle;        // ảnh tia riêng, rỗng = tia nước thường
        public string move = "move";    // xương mang cú lao, cú nhảy (đo độ dời thân)
        public string shadow = "shadow"; // slot bóng dưới chân (HideShadow)
        // cảm giác trúng riêng của clip (skill pokiclash-hero-fx, 2026-11-09): lúc trúng StageView khựng cả sân, rung, đẩy lùi con
        // bị đánh. Rig không khai thì như cũ.
        public string[] impactClips;
        public float[] impactStop;      // giây thật sân gần như đứng (StageView.FreezeSlow)
        public float[] impactShake;     // trauma 0..1 cộng vào rung màn
        public float[] impactPush;      // quãng bật lùi con bị đánh, theo chiều cao nó
        public string[] impactFlash;    // màu chớp cả màn lúc trúng (hex, StageView.Flash), rỗng = không chớp
        // slot vẽ KHÔNG viền sticker (hạt lá bay, lá văng: người dùng dặn bỏ viền trắng ở hạt lá, 2026-11-09): AolaSticker chụp các
        // slot này riêng một ảnh, hiện không qua viền giấy. Rỗng = như cũ, mọi thứ chung một ảnh có viền.
        public string[] plain;
    }

    public sealed class AtomikAsset : ScriptableObject
    {
        public string rigName;
        public int version;
        public float ppu = 100;
        public AtomikBone[] bones;
        public AtomikSlot[] slots;
        public AtomikAtt[] atts;
        public AtomikClip[] anims;
        public AtomikMask[] masks;      // bản 3; rig cũ: null hoặc rỗng
        public AtomikGame game;
        public Texture2D atlas;
        public Material material;

        public int FindClip(string clip)
        {
            if (anims == null) return -1;
            for (int i = 0; i < anims.Length; i++)
                if (anims[i].name == clip) return i;
            return -1;
        }

        public int FindBone(string bone)
        {
            if (bones == null || string.IsNullOrEmpty(bone)) return -1;
            for (int i = 0; i < bones.Length; i++)
                if (bones[i].name == bone) return i;
            return -1;
        }

        public int FindSlot(string slot)
        {
            if (slots == null || string.IsNullOrEmpty(slot)) return -1;
            for (int i = 0; i < slots.Length; i++)
                if (slots[i].name == slot) return i;
            return -1;
        }
    }
}
