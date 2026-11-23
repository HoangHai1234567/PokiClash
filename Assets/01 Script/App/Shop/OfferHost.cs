// Máy hiện popup ưu đãi (GD_Claude/26_CuaHang_IAP_QuangCao.md mục 7): gắn trong App.prefab (menu "PokiClash/Prefab/Khác/Hộp thoại và màn∕Cửa hàng: dựng hết").
// Lần vào sảnh đầu sau khi mở game, hoặc quay lại game sau reopenMin phút, gọi Offers.Open (hàng popup lúc vào game). Màn khác báo sự
// kiện qua Raise (thua, thắng boss, hết bi, bi ít, jackpot, rương Huyền thoại). Popup chỉ hiện khi màn rảnh: không trận, không lúc đang
// thả bi, không chuyển cảnh, không có hộp thoại hay bước hướng dẫn, không màn tải / cốt truyện. Hiện bằng tờ cửa hàng (ShopSheet).
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.Game;
using UnityEngine;

namespace PokiClash
{
    public sealed class OfferHost : MonoBehaviour
    {
        public static OfferHost I { get; private set; }

        static readonly List<Popup> queue = new List<Popup>();
        static bool needOpen = true;
        static double pausedAt;
        bool showing, hooked;
        float enteredAt;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();

        public static int Pending => queue.Count;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void ResetStatics()
        {
            queue.Clear();
            needOpen = true;
            pausedAt = 0;
        }

        void Awake() => I = this;

        void OnDestroy()
        {
            if (I == this) I = null;
            if (hooked && App.Router != null) App.Router.Entered -= OnEntered;
        }

        void OnEntered(SceneRoot root)
        {
            enteredAt = Time.unscaledTime;
            if (App.Router.Current == SceneIds.Hub) OpenIfNeeded();
            if (App.Router.Current == SceneIds.Machine && S.shop != null) LowBallsCheck();
        }

        void OnApplicationPause(bool paused)
        {
            if (paused)
            {
                pausedAt = Now;
                return;
            }
            if (pausedAt > 0 && App.Data != null && Now - pausedAt >= App.Data.Cfg.shop.caps.reopenMin * 60000)
            {
                needOpen = true;
                if (App.Router != null && App.Router.Current == SceneIds.Hub) OpenIfNeeded();
            }
        }

        // hàng popup lúc vào game (một lần mỗi lần mở / quay lại)
        static void OpenIfNeeded()
        {
            if (!needOpen || App.Save == null) return;
            needOpen = false;
            var list = Offers.Open(S, D, Now, new Rng(Rng.RandomSeed()));
            queue.AddRange(list);
            App.Save.Save();
            if (list.Count > 0) Debug.Log("[Ưu đãi] Vào game: " + string.Join(", ", list));
        }

        // vào máy bi lúc bi còn ít
        static void LowBallsCheck()
        {
            // bi không đủ một đợt thả đầy ở cược ×1
            if (S.balls > 0 && S.balls < D.Cfg.MaxPerDrop(S.level)) Raise(new OfferCtx { e = OfferEvent.LowBalls });
        }

        public static void Raise(OfferCtx x)
        {
            if (App.Save == null) return;
            var list = Offers.On(S, D, x, Now, new Rng(Rng.RandomSeed()));
            App.Save.Save();
            if (list.Count == 0) return;
            Debug.Log($"[Ưu đãi] {x.e}: " + string.Join(", ", list));
            queue.AddRange(list);
        }

        // bản dev: đưa thẳng một popup vào hàng (menu thử)
        public static void Push(Popup p) => queue.Add(p);

        bool CanShow()
        {
            if (!App.I || App.Booting || App.Covered || App.Modals.Count > 0 || App.Router == null || App.Router.Busy) return false;
            if (!Guide.Idle || StoryIntro.Current != null || EggHatchView.Playing || HeroUnlockView.Playing || Time.unscaledTime - enteredAt < 0.8f) return false;
            string cur = App.Router.Current;
            if (cur == SceneIds.Battle) return false;
            if (cur == SceneIds.Machine && !(App.Router.CurrentRoot is MachineScene m && m.Idle)) return false;
            return true;
        }

        static bool Valid(Popup p)
        {
            switch (p.kind)
            {
                case "offer":
                case "comeback":
                    var o = Shop.FindOffer(S, p.id);
                    return o != null && !o.bought && (o.until <= 0 || o.until > Now);
                case "claims": return Offers.AnyClaim(S, D, Now);
                case "piggy": return Shop.PiggyCanBreak(S, D.Cfg.shop);
                case "chain": return Shop.ChainLive(S, Now);
                default: return true;
            }
        }

        void Update()
        {
            if (!hooked && App.Router != null)
            {
                App.Router.Entered += OnEntered;
                hooked = true;
                if (App.Router.Current == SceneIds.Hub && !App.Booting) OpenIfNeeded();
            }
            if (showing || queue.Count == 0 || !CanShow()) return;
            var p = queue[0];
            queue.RemoveAt(0);
            if (!Valid(p)) return;
            Offers.Shown(S, D, p, Now);
            App.Save.Save();
            ShopLog.Event("offer_shown", p.ToString(), 0);
            showing = true;
            ShopSheet.OpenPopup(p, (bought, mute) =>
            {
                Offers.Closed(S, p, bought, mute, Now);
                App.Save.Save();
                ShopLog.Event(bought ? "offer_bought" : "offer_closed", p.ToString(), 0);
                if (mute) queue.RemoveAll(q => !q.free);
                showing = false;
            });
        }
    }
}
