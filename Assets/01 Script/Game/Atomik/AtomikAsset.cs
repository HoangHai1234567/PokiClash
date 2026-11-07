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
        public float[] keys;      // [t, giá trị..., kiểu (0 thẳng, 1 bậc, 2 bezier), điểm điều khiển...]
    }

    [Serializable]
    public sealed class AtomikSlotKeys
    {
        public int slot;
        public float[] times;
        public int[] atts;
    }

    [Serializable]
    public sealed class AtomikClip
    {
        public string name;
        public float dur;
        public AtomikTimeline[] tls;
        public AtomikSlotKeys[] sk;
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
        public Texture2D atlas;
        public Material material;

        public int FindClip(string clip)
        {
            if (anims == null) return -1;
            for (int i = 0; i < anims.Length; i++)
                if (anims[i].name == clip) return i;
            return -1;
        }
    }
}
