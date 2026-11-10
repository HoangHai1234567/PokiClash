// Trang trại là một cảnh thật (người dùng dặn 2026-11-10): ảnh nền vẽ tay (Assets/03 Art/Farm/farm_bg.png, gói ArtGen/SideMeta/build_farm.py)
// kéo được như sảnh (HubPan); 8 chỗ làm (FarmSlot) đặt sẵn trên các khu: ao vịt, ruộng rau, vườn cây, lò bánh, xưởng nông cụ; bảng tên khu
// vẽ sẵn trong prefab. Mỗi tướng hiện là một con thú (FarmPet):
// - tướng đang làm đứng ở chỗ làm, cử động theo việc của khu; hết sức thì ngồi nghiêng;
// - tướng rảnh (tối đa MaxRoam con: trong đội trước, rồi theo sao, độ hiếm) đi lang thang trong bãi cỏ giữa; chạm thì nhún nhảy, thả tim;
//   kéo thả vào một chỗ làm còn trống là giao việc;
// - tướng vừa rút ra (đang nghỉ, tối đa MaxSleep con) ngủ trên ổ rơm.
// Chạm chỗ làm mở danh sách chọn tướng (FarmPickerDialog, đổi ca, rút ra); chạm bong bóng bi hoặc "Thu hoạch" để lấy bi. Luật ở Core/Farm.
// Prefab Assets/04 Prefabs/Screens/Farm dựng bằng menu "PokiClash/Prefab/Trang trại: cảnh thật" (Editor/FarmSceneMenu.cs): nền, lớp kéo,
// chỗ làm, bảng khu, bãi cỏ, ổ rơm, lớp thú, lớp hạt, hàng nút ở đáy. Thú và hạt là prefab mục Items/ThuTrangTrai, Items/HatTrangTrai.
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using Random = UnityEngine.Random;

namespace PokiClash
{
    // đồ nghề và hạt của cảnh (thứ tự trùng mảng props của FarmScene)
    public enum FarmProp { Hoe, Can, Basket, Bread, Hammer, Sack, Apple, Carrot, Dust, Spark, Smoke, Heart, Seed, Drop, Zzz, Ball }

    public sealed class FarmScene : SceneRoot
    {
        public override string Title => "Trang trại";

        const int MaxRoam = 10, MaxSleep = 4;
        const float DropRadius = 150;

        [SerializeField] TextMeshProUGUI info, boostLeft;
        [SerializeField] SketchButton harvest, auto, boost;
        [SerializeField] FarmPickerDialog pickerPrefab;
        [Header("Cảnh")]
        [SerializeField] RectTransform petLayer, fxLayer, meadow, bed; // lớp thú, lớp hạt (cùng khung), bãi cỏ (bầu dục nội tiếp), ổ rơm
        [SerializeField] FarmSlot[] slots;
        [SerializeField] float[] slotFace; // hướng nhìn khi làm (1 phải, -1 trái) của từng chỗ
        [SerializeField] FarmPet petPrefab;
        [SerializeField] FarmFx fxPrefab;
        [SerializeField] Sprite[] props; // theo FarmProp; thiếu thì dùng icon thay

        readonly Dictionary<string, FarmPet> pets = new Dictionary<string, FarmPet>();
        readonly List<FarmFx> fxPool = new List<FarmFx>();
        float timer, sortTimer;
        bool busy, placed;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        public RectTransform PetLayer => petLayer;

        public static string KindIcon(string kind) =>
            kind == "duck" ? "wave" : kind == "veg" ? "seed" : kind == "orchard" ? "leaf" : kind == "bakery" ? "flame" : "hammer";

        public static string Num(double v) => v.ToString("0.##", System.Globalization.CultureInfo.InvariantCulture).Replace('.', ',');

        public static string Dec(double v) => v.ToString("0.0", System.Globalization.CultureInfo.InvariantCulture).Replace('.', ',');

        public static string Clock(double hours)
        {
            int m = (int)Math.Ceiling(Math.Max(0, hours) * 60);
            return m >= 60 ? $"{m / 60}:{m % 60:00}" : $"{m}p";
        }

        // Dùng khi nướng prefab (Editor).
        public void SetupScene(RectTransform pets_, RectTransform fx, RectTransform meadowRt, RectTransform bedRt, FarmSlot[] slotList, float[] face,
            FarmPet pet, FarmFx fxItem, Sprite[] propSprites)
        {
            petLayer = pets_;
            fxLayer = fx;
            meadow = meadowRt;
            bed = bedRt;
            slots = slotList;
            slotFace = face;
            petPrefab = pet;
            fxPrefab = fxItem;
            props = propSprites;
        }

        public override void Enter(object args)
        {
            if (!petLayer) return;
            harvest.SetOnClick(Harvest);
            auto.SetOnClick(AutoAssign);
            boost.SetOnClick(Boost);
            Build();
        }

        public override void Refresh() => Build();

        void Update()
        {
            if (!petLayer) return;
            if ((sortTimer += Time.unscaledDeltaTime) > 0.15f)
            {
                sortTimer = 0;
                SortPets();
            }
            if (busy || (timer += Time.unscaledDeltaTime) < 10) return;
            Build(); // sức và bi đổi theo giờ
        }

        // ---------- dựng ----------

        void Build()
        {
            timer = 0;
            if (!petLayer) return;
            var s = S;
            var d = D;
            var cfg = d.Cfg;
            double now = Now;
            Farm.Tick(s, d, now);
            var f = Farm.Of(s, cfg, now);

            int stock = f.spots.Sum(sp => (int)Math.Floor(sp.stock));
            bool anyWorking = f.spots.Any(sp => sp.hero != null);
            info.text = anyWorking
                ? $"Đúng hệ của khu ×{Num(cfg.farm.match)} bi. Hết sức thì chạm để đổi ca."
                : "Kéo một bạn trên bãi cỏ thả vào khu để giao việc, hoặc chạm vào khu.";
            harvest.SetText($"Thu hoạch ({stock})");
            harvest.Interactable = stock > 0;
            bool boosting = Farm.Boosting(f, now);
            boostLeft.gameObject.SetActive(boosting);
            if (boosting) boostLeft.text = $"Năng suất ×2: còn {Clock((f.boostUntil - now) / 3600000)}";
            boost.gameObject.SetActive(!boosting && Ads.Ready);
            if (!boosting && Ads.Ready) Ads.Bind(boost, "×2 năng suất", Ads.FarmBoost);

            int open = Farm.SpotsOpen(cfg, s.level);
            for (int i = 0; i < slots.Length && i < f.spots.Count; i++)
            {
                int k = i;
                slots[i].Bind(d, s, i, i < open, f.spots[i], () => Picker(k), Harvest);
            }
            SyncPets(s, d, f, now);
            placed = true;
        }

        // mỗi tướng một con: đang làm ở chỗ làm, rảnh ra bãi cỏ, nghỉ lên ổ rơm; đổi trạng thái thì nhảy lò cò sang chỗ mới
        void SyncPets(SaveData s, GameData d, FarmState f, double now)
        {
            var want = new Dictionary<string, (FarmPet.Mode mode, int spot)>();
            for (int i = 0; i < f.spots.Count && i < slots.Length; i++)
            {
                var sp = f.spots[i];
                if (sp.hero != null) want[sp.hero] = (sp.energy > 0 ? FarmPet.Mode.Work : FarmPet.Mode.Tired, i);
            }
            var owned = d.Heroes.Where(h => s.Hero(h.id) != null && s.Hero(h.id).owned && !want.ContainsKey(h.id)).ToList();
            foreach (var h in owned.Where(h => Farm.RestLeft(f, h.id, now) > 0).OrderBy(h => Farm.RestLeft(f, h.id, now)).Take(MaxSleep))
                want[h.id] = (FarmPet.Mode.Sleep, -1);
            var team = s.team ?? new List<string>();
            foreach (var h in owned.Where(h => Farm.Free(s, f, h.id, now))
                         .OrderBy(h => team.Contains(h.id) ? 0 : 1).ThenByDescending(h => s.Hero(h.id).star).ThenByDescending(h => (int)h.rarity)
                         .Take(MaxRoam))
                want[h.id] = (FarmPet.Mode.Roam, -1);

            foreach (var id in pets.Keys.Where(id => !want.ContainsKey(id)).ToList())
            {
                Destroy(pets[id].gameObject);
                pets.Remove(id);
            }
            int sleepIdx = 0;
            foreach (var kv in want)
            {
                var (mode, spot) = kv.Value;
                string kind = spot >= 0 ? d.Cfg.farm.spots[spot].kind : null;
                Vector2 at = mode == FarmPet.Mode.Work || mode == FarmPet.Mode.Tired ? SlotPos(spot)
                    : mode == FarmPet.Mode.Sleep ? BedPoint(sleepIdx++) : RoamPoint(null);
                if (!pets.TryGetValue(kv.Key, out var pet))
                {
                    pet = Ui.Spawn(petPrefab, petLayer);
                    pet.Bind(this, d.Hero(kv.Key));
                    pets[kv.Key] = pet;
                    if (!placed || mode == FarmPet.Mode.Roam || mode == FarmPet.Mode.Sleep) pet.Place(mode, at, spot, kind);
                    else
                    {
                        // tướng mới vào làm mà chưa có trên cảnh: từ bãi cỏ nhảy sang
                        pet.Place(FarmPet.Mode.Roam, ClampMeadow(at), -1, null);
                        pet.WalkTo(at, mode, spot, kind);
                    }
                    continue;
                }
                bool same = pet.State == mode && pet.Spot == spot;
                bool roamish = (pet.State == FarmPet.Mode.Roam || pet.State == FarmPet.Mode.Walk) && mode == FarmPet.Mode.Roam && spot < 0;
                bool workSwap = pet.Spot == spot && spot >= 0 && (mode == FarmPet.Mode.Work || mode == FarmPet.Mode.Tired) &&
                                (pet.State == FarmPet.Mode.Work || pet.State == FarmPet.Mode.Tired);
                if (pet.State == FarmPet.Mode.Drag || same || roamish) continue;
                if (workSwap) pet.Place(mode, at, spot, kind); // hết sức / được đổi ca tại chỗ
                else pet.WalkTo(at, mode, spot, kind);
            }
        }

        void SortPets()
        {
            // xa (cao) vẽ trước; con đang kéo luôn trên cùng
            var list = pets.Values.OrderByDescending(p => p.State == FarmPet.Mode.Drag ? float.MinValue : p.Pos.y).ToList();
            for (int i = 0; i < list.Count; i++) list[i].transform.SetSiblingIndex(i);
        }

        // ---------- toạ độ (trong lớp thú) ----------

        Vector2 Local(RectTransform rt, Vector2 normalized)
        {
            var r = rt.rect;
            var w = rt.TransformPoint(new Vector3(r.xMin + r.width * normalized.x, r.yMin + r.height * normalized.y));
            return petLayer.InverseTransformPoint(w);
        }

        public Vector2 SlotPos(int i) => petLayer.InverseTransformPoint(slots[i].Rt.position);

        public float SpotFace(int i) => slotFace != null && i >= 0 && i < slotFace.Length && slotFace[i] != 0 ? Mathf.Sign(slotFace[i]) : 1;

        // điểm ngẫu nhiên trong bầu dục bãi cỏ, ưu tiên gần chỗ đang đứng
        public Vector2 RoamPoint(Vector2? near)
        {
            for (int k = 0; k < 8; k++)
            {
                var a = Random.insideUnitCircle * 0.86f;
                var pt = Local(meadow, new Vector2(0.5f + a.x * 0.5f, 0.5f + a.y * 0.5f));
                if (near == null || (pt - near.Value).magnitude < 320) return pt;
            }
            return Local(meadow, new Vector2(0.5f, 0.5f));
        }

        public Vector2 RoamPoint(Vector2 near) => RoamPoint((Vector2?)near);

        public Vector2 ClampMeadow(Vector2 pt)
        {
            var c = Local(meadow, new Vector2(0.5f, 0.5f));
            var e = Local(meadow, new Vector2(1, 1)) - c; // bán trục
            var q = new Vector2((pt.x - c.x) / Mathf.Max(1, e.x), (pt.y - c.y) / Mathf.Max(1, e.y));
            if (q.magnitude > 0.85f) q = q.normalized * 0.85f;
            return c + new Vector2(q.x * e.x, q.y * e.y);
        }

        Vector2 BedPoint(int i) => Local(bed, new Vector2(Mathf.Clamp01(0.18f + 0.22f * i), 0.35f + (i % 2) * 0.2f));

        // ---------- thú gọi về ----------

        public void PetTapped(FarmPet pet)
        {
            if (pet.State == FarmPet.Mode.Sleep)
            {
                double left = Farm.RestLeft(Farm.Of(S, D.Cfg, Now), pet.Hero, Now) / 60000;
                App.Toasts.Show($"{D.Hero(pet.Hero).name} đang ngủ, còn {Math.Ceiling(left):0} phút", Icon("moon"));
                return;
            }
            if (pet.Spot >= 0) Picker(pet.Spot);
        }

        int Nearest(Vector2 pt, out float dist)
        {
            int best = -1;
            dist = float.MaxValue;
            for (int i = 0; i < slots.Length; i++)
            {
                float dd = (SlotPos(i) - pt).magnitude;
                if (dd < dist)
                {
                    dist = dd;
                    best = i;
                }
            }
            return best;
        }

        bool Accepts(int i, FarmState f) => i < Farm.SpotsOpen(D.Cfg, S.level) && f.spots[i].hero == null;

        public void PetDragging(FarmPet pet, Vector2 pt)
        {
            var f = Farm.Of(S, D.Cfg, Now);
            int n = Nearest(pt, out float dist);
            for (int i = 0; i < slots.Length; i++) slots[i].Highlight(Accepts(i, f), i == n && dist < DropRadius);
        }

        public bool PetDropped(FarmPet pet, Vector2 pt)
        {
            foreach (var sl in slots) sl.Highlight(false, false);
            var s = S;
            var d = D;
            double now = Now;
            Farm.Tick(s, d, now);
            var f = Farm.Of(s, d.Cfg, now);
            int i = Nearest(pt, out float dist);
            if (i < 0 || dist > DropRadius) return false;
            var def = d.Cfg.farm.spots[i];
            if (i >= Farm.SpotsOpen(d.Cfg, s.level))
            {
                App.Toasts.Show($"{def.name} mở ở cấp {Farm.SpotLevel(d.Cfg, i)}", Icon("lock"));
                return false;
            }
            if (f.spots[i].hero != null)
            {
                App.Toasts.Show($"{def.name} đã có {d.Hero(f.spots[i].hero).name}: chạm vào khu để đổi ca", Icon("team"));
                return false;
            }
            if (!Farm.Place(s, d, now, i, pet.Hero)) return false;
            App.Save.Save();
            App.Audio.Play("buff");
            bool match = d.Hero(pet.Hero).elem == def.elem;
            App.Toasts.Show($"{d.Hero(pet.Hero).name} vào {def.name}: {Dec(Farm.Rate(s, d, pet.Hero, i))} bi/giờ{(match ? " (đúng hệ)" : "")}", Icon(KindIcon(def.kind)));
            pet.Place(FarmPet.Mode.Work, SlotPos(i), i, def.kind);
            Build();
            return true;
        }

        // ---------- hạt ----------

        public Sprite Prop(FarmProp k)
        {
            int i = (int)k;
            if (props != null && i < props.Length && props[i]) return props[i];
            switch (k)
            {
                case FarmProp.Hoe: return Icon("farm_field");
                case FarmProp.Can: return Icon("drop");
                case FarmProp.Basket: return Icon("farm_orchard");
                case FarmProp.Bread: return Icon("farm_oven");
                case FarmProp.Hammer: return Icon("hammer");
                case FarmProp.Sack: return Icon("seed");
                case FarmProp.Apple: return Icon("farm_orchard");
                case FarmProp.Carrot: return Icon("leaf");
                case FarmProp.Dust: return App.Art ? App.Art.Get("anim_smoke_small") : null;
                case FarmProp.Spark: return App.Art ? App.Art.Get("anim_sparkle") : null;
                case FarmProp.Smoke: return App.Art ? App.Art.Get("anim_smoke_big") : null;
                case FarmProp.Heart: return Icon("heart");
                case FarmProp.Seed: return Icon("seed");
                case FarmProp.Drop: return Icon("drop");
                case FarmProp.Zzz: return Icon("moon");
                default: return Icon("ball");
            }
        }

        // sản phẩm nảy lên khi làm: ao vịt (thóc → bi), ruộng (cà rốt), vườn (táo), lò (bánh), xưởng (cuốc mới)
        public Sprite ProductOf(string kind) =>
            Prop(kind == "veg" ? FarmProp.Carrot : kind == "orchard" ? FarmProp.Apple : kind == "bakery" ? FarmProp.Bread :
                kind == "smithy" ? FarmProp.Hoe : FarmProp.Ball);

        // pos, vel theo toạ độ lớp thú (lớp hạt cùng khung)
        public void Fx(Sprite s, Color c, Vector2 pos, Vector2 vel, float gravity, float life, float size0, float size1, float spin = 0,
            bool pop = false, float drag = 0)
        {
            if (!s || !fxPrefab) return;
            var fx = fxPool.Find(x => !x.Busy);
            if (!fx)
            {
                if (fxPool.Count >= 60) return;
                fx = Ui.Spawn(fxPrefab, fxLayer);
                fxPool.Add(fx);
            }
            fx.Play(s, c, fxLayer.InverseTransformPoint(petLayer.TransformPoint(pos)), vel, gravity, life, size0, size1, spin, pop, drag);
        }

        // ---------- danh sách chọn tướng ----------

        void Picker(int i)
        {
            App.Modals.Open(pickerPrefab).Show(i, reopen =>
            {
                Build();
                if (reopen) Picker(i);
            });
        }

        // ---------- việc ----------

        void Harvest()
        {
            var f = Farm.Of(S, D.Cfg, Now);
            Farm.Tick(S, D, Now);
            var from = new List<(Vector2 at, int n)>();
            for (int i = 0; i < f.spots.Count && i < slots.Length; i++)
                if (f.spots[i].stock >= 1) from.Add((SlotPos(i) + new Vector2(0, 200), (int)Math.Floor(f.spots[i].stock)));
            int n = Farm.Harvest(S, D, Now);
            if (n <= 0) return;
            App.Save.Save();
            App.Audio.Play("coin");
            var ball = Prop(FarmProp.Ball);
            foreach (var (at, k) in from)
                for (int j = 0; j < Mathf.Min(k, 6); j++)
                    Fx(ball, Color.white, at, new Vector2(Random.Range(-140f, 140f), Random.Range(280f, 480f)), 900, 0.9f, 44, 36, 0, true);
            App.Toasts.Show($"Thu hoạch {n} bi", Icon("ball"));
            Build();
        }

        void AutoAssign()
        {
            var done = Farm.Auto(S, D, Now);
            App.Save.Save();
            App.Toasts.Show(done.Count > 0 ? $"Đã xếp {done.Count} tướng" : "Không còn tướng rảnh hoặc chỗ trống", Icon("team"));
            Build();
        }

        void Boost()
        {
            busy = true;
            Ads.Show(Ads.FarmBoost, ok =>
            {
                busy = false;
                if (ok && Farm.Boost(S, D, Now))
                {
                    App.Save.Save();
                    App.Toasts.Show("Năng suất ×2 trong 1 giờ", Icon("seed"));
                }
                Build();
            });
        }
    }
}
