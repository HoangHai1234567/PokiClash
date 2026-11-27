// Đổi ảnh của màn sang bản theo mùa (mùa Noel: màn Nhà và đảo Casino phủ tuyết; người dùng 2026-11-27: "làm tuyết phủ lên đảo / cây
// cối / các building"). Bản mùa là ảnh gốc + tuyết, đúng cỡ ảnh gốc (ArtGen/Seasons/noel/map: GPT vẽ lại tờ ảnh có tuyết, tach_map.py
// tách tuyết rồi ghép lên ảnh gốc), đặt ở Resources/Seasons/<mùa>/map/<tên texture gốc>; ảnh cắt từ atlas (cây Nhà, home_trees) thì bản
// mùa là cả atlas cùng bố cục, sprite bản mùa cắt đúng khung sprite gốc.
// Đổi thẳng sprite, không chồng thêm Image: số lượt vẽ không tăng (rừng Nhà hàng trăm cây cùng một atlas), vật liệu (biển, sáng khi chọn,
// tự sáng đêm) giữ nguyên. Hai chỗ đổi:
// - nguồn: các trường Sprite, mảng Sprite, mảng struct có trường Sprite của SceneRoot (HomeScene: art, treeArt...) để vật dựng sau (cây
//   ô rừng, công trình mới đặt) ra luôn bản mùa;
// - Image con: quét ngay khi bật rồi mỗi giây một lần (ảnh đặt sẵn trong prefab: nền đảo, vách, đồ ven biển, công trình Casino).
// Hết mùa (Apply(None)) thì trả lại sprite gốc ở cả hai chỗ. Bản mùa phải cùng cỡ texture với ảnh gốc (khung sprite quyết định cỡ vật
// trên bản đồ): lệch cỡ thì bỏ qua, ghi cảnh báo.
using System;
using System.Collections.Generic;
using System.Reflection;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class SeasonSkin : MonoBehaviour
    {
        static readonly Dictionary<string, Texture2D> texOf = new Dictionary<string, Texture2D>(); // đường Resources → texture (null: không có)
        static readonly Dictionary<(SeasonId, Sprite), Sprite> skinOf = new Dictionary<(SeasonId, Sprite), Sprite>();
        static readonly Dictionary<Sprite, Sprite> origOf = new Dictionary<Sprite, Sprite>(); // sprite bản mùa đã tạo → sprite gốc

        public SeasonId Built { get; private set; } = SeasonId.None;
        public int ImageSwaps { get; private set; }
        public int DataSwaps { get; private set; }

        readonly List<Action> undo = new List<Action>(); // trả các trường dữ liệu
        readonly List<Image> buf = new List<Image>();
        float next;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void ResetStatics()
        {
            texOf.Clear();
            skinOf.Clear();
            origOf.Clear();
        }

        public static bool IsSkin(Sprite s) => s && origOf.ContainsKey(s);

        static string Folder(SeasonId s) => s == SeasonId.Noel ? "Seasons/noel/map/" : null;

        // sprite bản mùa của một sprite gốc (null: không có bản mùa)
        public static Sprite SkinOf(SeasonId season, Sprite s)
        {
            var dir = Folder(season);
            if (dir == null || !s || !s.texture || origOf.ContainsKey(s)) return null;
            if (skinOf.TryGetValue((season, s), out var r)) return r;
            string key = dir + s.texture.name;
            if (!texOf.TryGetValue(key, out var tex)) texOf[key] = tex = Resources.Load<Texture2D>(key);
            r = null;
            if (tex)
            {
                if (tex.width != s.texture.width || tex.height != s.texture.height)
                    Debug.LogWarning($"[Mùa] Bản mùa {key} cỡ {tex.width}x{tex.height} khác ảnh gốc {s.texture.width}x{s.texture.height}: bỏ qua");
                else
                {
                    var rc = s.rect;
                    r = Sprite.Create(tex, rc, new Vector2(s.pivot.x / rc.width, s.pivot.y / rc.height), s.pixelsPerUnit, 0, SpriteMeshType.FullRect, s.border);
                    r.name = s.name + "_" + season;
                    origOf[r] = s;
                }
            }
            skinOf[(season, s)] = r;
            return r;
        }

        public void Apply(SeasonId s)
        {
            if (s == Built) return;
            Restore();
            Built = s;
            if (Folder(s) == null) return;
            var root = GetComponent<SceneRoot>();
            if (root) SwapData(root);
            Scan();
            next = Time.unscaledTime + 1f;
        }

        void LateUpdate()
        {
            if (Folder(Built) == null || Time.unscaledTime < next) return;
            next = Time.unscaledTime + 1f;
            Scan();
        }

        void OnDestroy() => Restore();

        void Scan()
        {
            GetComponentsInChildren(true, buf);
            foreach (var img in buf)
            {
                var s = img.sprite;
                if (!s || origOf.ContainsKey(s)) continue;
                var r = SkinOf(Built, s);
                if (!r) continue;
                img.sprite = r;
                ImageSwaps++;
            }
            buf.Clear();
        }

        void SwapData(object root)
        {
            const BindingFlags F = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;
            foreach (var f in root.GetType().GetFields(F))
            {
                var t = f.FieldType;
                if (t == typeof(Sprite))
                {
                    var s = (Sprite)f.GetValue(root);
                    var r = SkinOf(Built, s);
                    if (!r) continue;
                    f.SetValue(root, r);
                    undo.Add(() => f.SetValue(root, s));
                    DataSwaps++;
                    continue;
                }
                if (!t.IsArray || !(f.GetValue(root) is Array arr)) continue;
                var et = t.GetElementType();
                if (et == typeof(Sprite))
                {
                    for (int i = 0; i < arr.Length; i++)
                    {
                        var s = (Sprite)arr.GetValue(i);
                        var r = SkinOf(Built, s);
                        if (!r) continue;
                        int at = i;
                        arr.SetValue(r, i);
                        undo.Add(() => arr.SetValue(s, at));
                        DataSwaps++;
                    }
                    continue;
                }
                // mảng struct có trường Sprite (HomeScene.ArtMeta, TreeArt): đổi trên bản đóng hộp rồi ghi lại phần tử; trả = ghi lại bản cũ
                if (!et.IsValueType) continue;
                var sf = new List<FieldInfo>();
                foreach (var x in et.GetFields(BindingFlags.Instance | BindingFlags.Public))
                    if (x.FieldType == typeof(Sprite)) sf.Add(x);
                if (sf.Count == 0) continue;
                for (int i = 0; i < arr.Length; i++)
                {
                    object old = arr.GetValue(i), el = arr.GetValue(i);
                    bool changed = false;
                    foreach (var x in sf)
                    {
                        var r = SkinOf(Built, (Sprite)x.GetValue(el));
                        if (!r) continue;
                        x.SetValue(el, r);
                        changed = true;
                    }
                    if (!changed) continue;
                    int at = i;
                    arr.SetValue(el, i);
                    undo.Add(() => arr.SetValue(old, at));
                    DataSwaps++;
                }
            }
        }

        void Restore()
        {
            // mọi Image đang mang bản mùa (đổi khi quét, hay dựng từ dữ liệu đã đổi) về sprite gốc
            if (Built != SeasonId.None)
            {
                GetComponentsInChildren(true, buf);
                foreach (var img in buf)
                    if (img.sprite && origOf.TryGetValue(img.sprite, out var o)) img.sprite = o;
                buf.Clear();
            }
            ImageSwaps = 0;
            for (int i = undo.Count - 1; i >= 0; i--) undo[i]();
            undo.Clear();
            DataSwaps = 0;
            Built = SeasonId.None;
        }
    }
}
