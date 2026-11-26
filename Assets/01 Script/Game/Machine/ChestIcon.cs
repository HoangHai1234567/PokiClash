// Hình rương, prefab kit Kit/Ruong. Bind đặt loại, bề rộng, màu thân.
// Có ảnh gen (ArtGen/Pachinko, "build.py --duyet ruong": pk_ruong_go / _bac / _vang, bản mở thêm "_mo") thì dùng ảnh đó, bỏ khoá
// vẽ tạm; không thì vẽ tạm như cũ (thân giấy tô màu + khoá tròn, vật liệu UIKit). Rương có màu riêng (fill) giữ hình vẽ tạm cho
// khỏi mất màu (rương AFK từ 2026-11-27 thôi tô màu riêng, dùng rương gỗ thật có rig). Open(): đổi sang ảnh rương mở, giữ bề rộng và mép đáy (bản mở cao hơn vì có nắp lật và sao).
// Rig AtomSpine (GD_Claude/23_MayBi_TraiNghiem.md, ArtGen/Pachinko/ruong_rig/build_rig.py): con "rig" (AtomSpine.AtomikGraphic, tắt
// sẵn) và ba file ruong_<bậc>.bytes, menu "PokiClash/Prefab/Máy bi/rig rương (AtomSpine)". PlayRig bật rig thay ảnh tĩnh: cho (đứng
// thở), nhac (nhắc mở: nhún, lắc, nắp hé có sáng ấm và tia lọt khe), gong (gồng), bat (nắp bật, sự kiện "open"), mo (mở rồi, lòng
// sáng). Mặc định tắt: icon nhỏ trên mặt máy, bảng tỉ lệ vẫn là ảnh tĩnh, chỉ chỗ nào gọi PlayRig mới chạy rig.
using System.Collections.Generic;
using AtomSpine;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ChestIcon : MonoBehaviour
    {
        [SerializeField] Image body, lockImg;
        [SerializeField] AtomikGraphic rig;
        [SerializeField] TextAsset rigGo, rigBac, rigVang;

        public RectTransform Rect => (RectTransform)transform;
        public SlotKind Kind { get; private set; }
        public bool RigOn => rig && rig.gameObject.activeSelf;
        public bool Bound { get; private set; } // đã Bind trong lần chạy này (icon nướng sẵn trong prefab thì chưa: Kind, art chưa có)
        public AtomikGraphic Rig => rig;

        Sprite sketch; // hình vẽ tạm của prefab (khi ảnh gen chưa có)
        Material sketchMat;
        bool art;
        float openShift; // Open() nhích lên giữ mép đáy; Bind sau đó trả lại (hộp mở rương dùng lại một icon cho nhiều rương)
        const float RigW = 320; // bề ngang rương trong rig (px rig) = bề ngang ảnh rương

        // rig nạp một lần cho mỗi bậc, dùng chung mọi icon (atlas, vật liệu sống tới khi thoát game)
        static readonly Dictionary<SlotKind, AtomikAsset> rigCache = new Dictionary<SlotKind, AtomikAsset>();

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bodyImg, Image lockImage)
        {
            body = bodyImg;
            lockImg = lockImage;
        }

        // Dùng khi nướng prefab (Editor).
        public void SetupRig(AtomikGraphic graphic, TextAsset go, TextAsset bac, TextAsset vang)
        {
            rig = graphic;
            rigGo = go;
            rigBac = bac;
            rigVang = vang;
        }

        AtomikAsset RigAsset(SlotKind k)
        {
            if (rigCache.TryGetValue(k, out var a) && a) return a;
            var src = k == SlotKind.ChestGold ? rigVang : k == SlotKind.ChestSilver ? rigBac : rigGo;
            if (!src) return null;
            try
            {
                a = AtomikFile.Load(src.bytes);
            }
            catch (System.Exception e)
            {
                Debug.LogWarning("[Rương] Không nạp được rig " + src.name + ": " + e.Message);
                a = null;
            }
            rigCache[k] = a;
            return a;
        }

        /// <summary>Bật rig thay ảnh tĩnh và chạy clip (đang chạy đúng clip đó thì để yên). phase: tua tới giây này (lệch nhịp nhiều
        /// rương). Trả false khi không có rig (rương vẽ tạm, thiếu file): ảnh tĩnh giữ nguyên.</summary>
        public bool PlayRig(string clip, bool loop = true, float phase = 0)
        {
            if (!rig || !art) return false;
            var a = RigAsset(Kind);
            if (!a) return false;
            if (RigOn && rig.asset == a && rig.CurrentClip == clip) return true;
            rig.asset = a;
            rig.scaleMode = AtomikGraphicScale.RigPixels;
            rig.pixelScale = Rect.sizeDelta.x / RigW;
            rig.updateMode = AtomikUpdateMode.Unscaled;
            rig.raycastTarget = false;
            var rt = rig.rectTransform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0); // gốc rig (đáy rương) ở giữa mép đáy icon
            rt.anchoredPosition = Vector2.zero;
            rt.sizeDelta = Rect.sizeDelta;
            if (!rig.gameObject.activeSelf) rig.gameObject.SetActive(true);
            body.enabled = false;
            rig.Play(clip, loop);
            if (phase > 0) rig.Seek(phase);
            return true;
        }

        /// <summary>Tắt rig, hiện lại ảnh tĩnh.</summary>
        public void StopRig()
        {
            if (rig && rig.gameObject.activeSelf) rig.gameObject.SetActive(false);
            if (body) body.enabled = true;
        }

        static string ArtName(SlotKind kind) =>
            kind == SlotKind.ChestGold ? "pk_ruong_vang" : kind == SlotKind.ChestSilver ? "pk_ruong_bac" : "pk_ruong_go";

        static Sprite Art(string name) => ArtLibrary.Current && ArtLibrary.Current.HasArt(name) ? ArtLibrary.Current.Get(name) : null;

        public ChestIcon Bind(SlotKind kind, float w, Color? fill = null)
        {
            Kind = kind;
            Bound = true;
            StopRig(); // icon dùng lại cho nhiều rương: tắt rig của rương trước
            name = "ruong_" + Pachinko.Key(kind);
            if (openShift != 0)
            {
                Rect.anchoredPosition -= new Vector2(0, openShift);
                openShift = 0;
            }
            if (!sketch)
            {
                sketch = body.sprite;
                sketchMat = body.material;
            }
            var sprite = fill == null ? Art(ArtName(kind)) : null;
            art = sprite;
            lockImg.gameObject.SetActive(!art);
            if (art)
            {
                body.sprite = sprite;
                body.material = null;
                body.color = Color.white;
                body.preserveAspect = true;
                Rect.sizeDelta = new Vector2(w, w * sprite.rect.height / sprite.rect.width);
                return this;
            }
            body.sprite = sketch;
            body.material = sketchMat;
            body.preserveAspect = false;
            body.color = fill ?? MachineBoard.ChestColor(kind);
            Rect.sizeDelta = new Vector2(w, w * 88 / 96f);
            lockImg.color = kind == SlotKind.ChestGold ? Theme.Orange : Theme.Hex("#ffd24a");
            lockImg.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -w * 0.05f), new Vector2(w * 0.22f, w * 0.22f));
            return this;
        }

        // rương bật nắp (hộp mở rương): ảnh rương mở nếu có
        public void Open()
        {
            var sprite = art ? Art(ArtName(Kind) + "_mo") : null;
            if (!sprite) return;
            var size = Rect.sizeDelta;
            float h = size.x * sprite.rect.height / sprite.rect.width;
            body.sprite = sprite;
            float shift = (h - size.y) * Rect.pivot.y;
            Rect.anchoredPosition += new Vector2(0, shift);
            openShift += shift;
            Rect.sizeDelta = new Vector2(size.x, h);
        }
    }
}
