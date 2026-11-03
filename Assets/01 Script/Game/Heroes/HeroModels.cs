// Danh mục prefab tướng (Assets/04 Prefabs/Heroes/<id>.prefab, mỗi prefab một dòng tiến hóa, AolaActor giữ các dạng). Dựng
// bằng menu PokiClash/Tướng/Nhập hình tướng aola; UiAssets.heroes trỏ tới. Tra theo tên dạng (HeroForm.aola).
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash.Game
{
    public sealed class HeroModels : ScriptableObject
    {
        public AolaActor[] heroes = new AolaActor[0];

        Dictionary<string, (AolaActor prefab, int form)> index;

        // Dùng khi nhập (Editor).
        public void Setup(AolaActor[] prefabs)
        {
            heroes = prefabs;
            index = null;
        }

        public bool Find(string form, out AolaActor prefab, out int formIndex)
        {
            prefab = null;
            formIndex = -1;
            if (string.IsNullOrEmpty(form)) return false;
            if (index == null)
            {
                index = new Dictionary<string, (AolaActor, int)>();
                foreach (var h in heroes)
                {
                    if (!h) continue;
                    var fs = h.Forms;
                    for (int i = 0; i < fs.Length; i++)
                        if (fs[i]) index[fs[i].name] = (h, i);
                }
            }
            if (!index.TryGetValue(form, out var hit)) return false;
            (prefab, formIndex) = hit;
            return prefab;
        }

        public AolaAnim Anim(string form) => Find(form, out var p, out int i) ? p.Forms[i] : null;

        void OnValidate() => index = null;
    }
}
