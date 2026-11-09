// Một dạng tướng aola đã nhập vào project (menu PokiClash/Tướng/Nhập hình tướng aola, Editor/AolaImport): ảnh ghép mọi hình
// mảnh (đã thu nhỏ về độ nét thật sự dùng, nén ASTC), chân dung, animation (anim.json của AolaRipper nén gzip). Hình gốc của
// Baitian, chỉ dùng trong bản thử. Tên asset = tên thư mục aola của dạng (HeroForm.aola), ví dụ goc_76.
// Atlas và chân dung nằm trong thư mục Resources, nạp khi cần (LoadAtlas, LoadPortrait): danh mục HeroModels được nạp từ lúc mở
// game, trỏ thẳng tới ảnh thì mọi ảnh tướng vào bộ nhớ cùng lúc.
using UnityEngine;

namespace PokiClash.Game
{
    public sealed class AolaAnim : ScriptableObject
    {
        public string res;        // đường dẫn Resources, không đuôi: <res>_atlas, <res>_portrait
        public TextAsset anim;    // anim.json gzip: fps, clips (mỗi khung: [hình, a, b, c, d, tx, ty, alpha, {tint, blend}])
        public Vector2[] sizes;   // cỡ gốc mỗi hình (điểm clip, trước khi thu nhỏ): ma trận trong anim.json tính theo cỡ này
        public Rect[] uvs;        // chỗ mỗi hình trong atlas (UV)
        public int shadow = -1;   // hình bóng dưới chân (điểm khớp giữa các clip), -1 nếu không có
        public string source;     // dấu bản nguồn (thời điểm sửa anim.json, hình, chân dung): nhập lại khi đổi
        public int brief;         // luật thu hình ít khung đã áp vào atlas (AolaImport.BriefRule); 0: chưa, xếp lại atlas sẽ thu
        // Dạng vẽ mới rig xương riêng (.atomik, ArtGen/Spine, 2026-11-08): AolaActor phát rig này thay cho anim/atlas aola; asset
        // vẫn giữ res cho chân dung. Gắn bằng menu PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng (Editor/AtomikForms).
        public AtomikAsset atomik;

        public Texture2D LoadAtlas() => string.IsNullOrEmpty(res) ? null : Resources.Load<Texture2D>(res + "_atlas");

        // khung 4:5 như HeroArt, gốc ở chân
        public Sprite LoadPortrait() => string.IsNullOrEmpty(res) ? null : Resources.Load<Sprite>(res + "_portrait");

        // Dùng khi nhập (Editor).
        public void Setup(string resPath, TextAsset animData, Vector2[] spriteSizes, Rect[] spriteUvs, int shadowSprite, string stamp)
        {
            res = resPath;
            anim = animData;
            sizes = spriteSizes;
            uvs = spriteUvs;
            shadow = shadowSprite;
            source = stamp;
        }
    }
}
