// Đa ngôn ngữ lúc chạy (2026-11-21): chọn ngôn ngữ, nạp bảng dịch, dịch chữ có sẵn trong prefab/scene.
// - Ngôn ngữ: PlayerPrefs "PokiClash.Lang" (nút Ngôn ngữ ở Sổ tay); chưa chọn thì máy tiếng Việt ra "vi", máy khác ra "en".
//   Trong Editor chưa chọn thì là "vi" (đổi ở Sổ tay hoặc menu PokiClash/Ngôn ngữ).
// - Bảng: mọi TextAsset trong Assets/Resources/Loc/<mã>/ gộp lại (object phẳng { "chuỗi Việt": "bản dịch" }).
// - Chữ trong prefab/scene: Tree(go) dịch mọi TMP_Text có chữ khớp bảng. Gọi ở Ui.Spawn, SceneRouter (scene vừa nạp),
//   App (khung app, màn tải). Chữ code gán sau đó đã qua Loc.T / Loc.F nên không bị dịch hai lần.
//   Mỗi chữ nhớ bản gốc tiếng Việt để đổi ngôn ngữ lúc chạy dịch lại được (chỉ khi code chưa gán chữ khác đè lên).
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using PokiClash.Core;
using TMPro;
using UnityEngine;

namespace PokiClash.Game
{
    public static class LocService
    {
        public const string PrefKey = "PokiClash.Lang";
        public static readonly string[] Langs = { Loc.Vi, Loc.En };

        sealed class Orig
        {
            public string vi; // chữ gốc trong prefab
            public string shown; // chữ đã gán lần dịch trước
        }

        static readonly ConditionalWeakTable<TMP_Text, Orig> origs = new ConditionalWeakTable<TMP_Text, Orig>();
        static readonly List<TMP_Text> buf = new List<TMP_Text>();
        static bool touched; // đã dịch ít nhất một chữ prefab trong phiên

#if UNITY_EDITOR || DEVELOPMENT_BUILD
        // chuỗi chưa dịch gặp lúc chạy (bản dev): menu PokiClash/Ngôn ngữ/Ghi chuỗi thiếu
        public static readonly HashSet<string> Missing = new HashSet<string>();
#endif

        // Vào Play không reload domain: trả về tiếng Việt, Init chọn lại
        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void ResetStatics()
        {
            Loc.UseVi();
            touched = false;
        }

        public static string Saved => PlayerPrefs.GetString(PrefKey, "");

        public static string Detect()
        {
#if UNITY_EDITOR
            return Loc.Vi;
#else
            return Application.systemLanguage == SystemLanguage.Vietnamese ? Loc.Vi : Loc.En;
#endif
        }

        // lúc mở game, trước khi dựng dữ liệu (GameDb.Build dịch tên theo ngôn ngữ đang dùng)
        public static void Init()
        {
            var lang = Saved;
            Apply(System.Array.IndexOf(Langs, lang) >= 0 ? lang : Detect());
        }

        // chọn ngôn ngữ và nhớ lại; gọi xong thì dựng lại dữ liệu, dịch lại khung app (App.SetLanguage)
        public static void Set(string lang)
        {
            PlayerPrefs.SetString(PrefKey, lang);
            PlayerPrefs.Save();
            Apply(lang);
        }

        static void Apply(string lang)
        {
            if (lang == Loc.Vi)
            {
                Loc.UseVi();
                return;
            }
            Loc.Use(lang, Load(lang));
#if UNITY_EDITOR || DEVELOPMENT_BUILD
            Loc.OnMiss = s =>
            {
                if (Missing.Add(s)) Debug.LogWarning($"[Loc] Chưa dịch ({lang}): {s}");
            };
#endif
        }

        public static Dictionary<string, string> Load(string lang)
        {
            var t = new Dictionary<string, string>();
            foreach (var ta in Resources.LoadAll<TextAsset>("Loc/" + lang))
            {
                var o = J.Obj(MiniJson.Parse(ta.text));
                if (o == null)
                {
                    Debug.LogError($"[Loc] {ta.name}: không đọc được JSON");
                    continue;
                }
                foreach (var kv in o)
                    if (kv.Value is string s && s.Length > 0)
                        t[kv.Key] = s;
            }
            return t;
        }

        // dịch chữ có sẵn trong cây go (kể cả con đang ẩn)
        public static void Tree(GameObject go)
        {
            // tiếng Việt từ đầu phiên: chữ prefab đã đúng, không quét (chỉ quét khi từng dịch để trả chữ về)
            if (!go || Loc.Lang == Loc.Vi && !touched) return;
            buf.Clear();
            go.GetComponentsInChildren(true, buf);
            foreach (var t in buf) Text(t);
            buf.Clear();
        }

        public static void Tree(Component c)
        {
            if (c) Tree(c.gameObject);
        }

        static void Text(TMP_Text t)
        {
            if (origs.TryGetValue(t, out var o))
            {
                if (t.text != o.shown) return; // code đã gán chữ khác: chữ đó tự lo ngôn ngữ
            }
            else
            {
                if (Loc.Lang == Loc.Vi || string.IsNullOrEmpty(t.text)) return;
                o = new Orig { vi = t.text, shown = t.text };
                origs.Add(t, o);
                touched = true;
            }
            string s = o.vi;
            if (Loc.Lang != Loc.Vi)
            {
                if (Loc.Find(o.vi, out var tr)) s = tr;
                else if (Loc.LooksVi(o.vi)) Loc.OnMiss?.Invoke(o.vi);
            }
            if (s != t.text) t.text = s;
            o.shown = s;
        }
    }
}
