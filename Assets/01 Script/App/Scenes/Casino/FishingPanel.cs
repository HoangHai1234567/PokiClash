// Bến câu (GD_Claude/29_DaoCasino.md mục 6.2, mốc C3): một ngón, màn dọc.
// 1. Quăng: vuốt lên trên mặt nước, độ dài vuốt là lực (thanh lực bên trái); thả tay thì phao bay ra, xa theo lực.
// 2. Chờ: phao nhấp nhô; cá cắn thì phao chìm, hiện "!", có biteWindow giây để chạm "giật". Hụt thì mất mồi.
// 3. Kéo: thanh dọc bên phải; giữ ngón thì vùng xanh nổi lên, thả thì chìm; giữ con cá trong vùng xanh để đầy vòng kéo, cạn là sổng.
// Lõi: Core/Casino/Fishing.cs (mồi, chọn cá, Sổ Cá, Cá Vua, bán). Hình cá tạm: chấm màu hệ viền màu độ hiếm (C8 thay ảnh cá).
// Mọi phần tử dựng sẵn trong prefab (menu "PokiClash/Prefab/Đảo Casino/Trò: dựng màn chơi"), không sinh lúc chạy.
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class FishingPanel : MonoBehaviour
    {
        [System.Serializable]
        public struct DexCell
        {
            public Image dot, ring;
            public TextMeshProUGUI name, info;
        }

        [Header("Mặt nước")]
        [SerializeField] SwipeArea swipe;
        [SerializeField] HoldArea hold;
        [SerializeField] RectTransform water, rodTip, bobber, line, bang;
        [SerializeField] Image power;
        [SerializeField] TextMeshProUGUI hint;
        [Header("Kéo")]
        [SerializeField] RectTransform reel, reelZone, reelFish;
        [SerializeField] Image reelFishImg, reelProgress;
        [Header("Trên")]
        [SerializeField] SketchButton[] spotBtns;
        [SerializeField] TextMeshProUGUI baitText, rodText;
        [SerializeField] SketchButton rodBtn;
        [Header("Dưới")]
        [SerializeField] SketchButton dexBtn, sellBtn, baitBtn;
        [Header("Kết quả")]
        [SerializeField] GameObject result;
        [SerializeField] Image resDot, resRing;
        [SerializeField] TextMeshProUGUI resName, resInfo, resRewards;
        [SerializeField] SketchButton resOk;
        [Header("Sổ Cá")]
        [SerializeField] GameObject dex;
        [SerializeField] TextMeshProUGUI dexHead;
        [SerializeField] DexCell[] dexCells;
        [SerializeField] SketchButton dexClose;

        enum St { Idle, Aim, Fly, Wait, Bite, Reel, Result }

        St st;
        int spot;
        float aim, t, flyFrom, flyTo;
        Vector2 bobPos;
        FishBite bite;
        string assist;
        float zoneC, zoneV, zoneH, fishP, fishTarget, fishSpeed, prog, nextTurn;
        bool holding;
        Rng rng;
        System.Action onRefresh;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static FishingConfig C => D.Cfg.casino.fishing;
        static double Now => SaveService.Now();
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // cho lượt chụp thử: trạng thái hiện tại
        public string State => st.ToString();

        // Dùng khi dựng prefab (Editor).
        public void Setup(SwipeArea sw, HoldArea ho, RectTransform waterRt, RectTransform tip, RectTransform bob, RectTransform lineRt, RectTransform bangRt,
            Image powerImg, TextMeshProUGUI hintText, RectTransform reelRt, RectTransform zone, RectTransform fish, Image fishImg, Image progImg,
            SketchButton[] spots, TextMeshProUGUI bait, TextMeshProUGUI rod, SketchButton rodUp, SketchButton dexB, SketchButton sellB, SketchButton baitB,
            GameObject res, Image rDot, Image rRing, TextMeshProUGUI rName, TextMeshProUGUI rInfo, TextMeshProUGUI rRewards, SketchButton rOk,
            GameObject dexGo, TextMeshProUGUI dHead, DexCell[] cells, SketchButton dClose)
        {
            swipe = sw; hold = ho; water = waterRt; rodTip = tip; bobber = bob; line = lineRt; bang = bangRt; power = powerImg; hint = hintText;
            reel = reelRt; reelZone = zone; reelFish = fish; reelFishImg = fishImg; reelProgress = progImg;
            spotBtns = spots; baitText = bait; rodText = rod; rodBtn = rodUp; dexBtn = dexB; sellBtn = sellB; baitBtn = baitB;
            result = res; resDot = rDot; resRing = rRing; resName = rName; resInfo = rInfo; resRewards = rRewards; resOk = rOk;
            dex = dexGo; dexHead = dHead; dexCells = cells; dexClose = dClose;
        }

        public void Open(System.Action refresh)
        {
            onRefresh = refresh;
            rng = new Rng(Rng.RandomSeed());
            gameObject.SetActive(true);
            spot = 0;
            if (swipe)
            {
                swipe.Began = () => { if (st == St.Idle) { st = St.Aim; aim = 0; } };
                swipe.Dragged = dlt => { if (st == St.Aim) aim = Mathf.Clamp01(aim + dlt.y / (Screen.height * 0.33f)); };
                swipe.Ended = () => { if (st == St.Aim) Release(); };
            }
            if (hold)
            {
                hold.Down = () =>
                {
                    holding = true;
                    if (st == St.Bite) Hook();
                };
                hold.Up = () => holding = false;
            }
            for (int i = 0; i < spotBtns.Length; i++)
            {
                int k = i;
                spotBtns[i].SetOnClick(() => PickSpot(k));
            }
            rodBtn.SetOnClick(UpgradeRod);
            dexBtn.SetOnClick(ShowDex);
            sellBtn.SetOnClick(Sell);
            baitBtn.SetOnClick(BuyBait);
            resOk.SetOnClick(() => { result.SetActive(false); ToIdle(); });
            dexClose.SetOnClick(() => dex.SetActive(false));
            result.SetActive(false);
            dex.SetActive(false);
            ToIdle();
            Render();
        }

        public void Close() => gameObject.SetActive(false);

        // ---------- trên, dưới ----------

        void Render()
        {
            var s = S;
            var d = D;
            double now = Now;
            int free = Fishing.FreeLeft(s, d, now);
            baitText.text = Loc.F("Mồi: {0} miễn phí · {1} mua", free, Casino.Of(s).bait);
            int cost = Fishing.RodCost(s, d);
            rodText.text = Loc.F("Cần câu cấp {0}", Casino.Of(s).rod);
            rodBtn.gameObject.SetActive(cost >= 0);
            if (cost >= 0) rodBtn.SetText(Loc.F("Nâng · {0} bi", NumFmt.Short(cost)));
            int open = Fishing.Spots(s, d);
            for (int i = 0; i < spotBtns.Length; i++)
            {
                bool ok = i < open && i < C.spots.Count;
                spotBtns[i].gameObject.SetActive(i < C.spots.Count);
                if (i >= C.spots.Count) continue;
                spotBtns[i].SetText(C.spots[i].Name);
                spotBtns[i].SetRole(i == spot ? BtnColor.Yellow : BtnColor.Paper);
                spotBtns[i].Locked = !ok;
            }
            int v = Fishing.CreelValue(s, d);
            sellBtn.SetText(v > 0 ? Loc.F("Bán cá · {0} bi", NumFmt.Short(v)) : Loc.T("Bán cá"));
            sellBtn.Locked = v <= 0;
            baitBtn.SetText(Loc.F("Mua {0} mồi · {1} bi", C.baitPack, Fishing.BaitCost(s, d)));
            dexBtn.SetText(Loc.F("Sổ Cá {0}/{1}", Casino.Of(s).dex.Count(kv => kv.Value.n > 0 && C.fish.Any(f => f.id == kv.Key)), C.fish.Count));
        }

        void PickSpot(int k)
        {
            if (st != St.Idle) return;
            if (k >= Fishing.Spots(S, D))
            {
                App.Toasts.Show(Loc.T("Nâng cần câu để câu chỗ này"), Icon("lock"));
                return;
            }
            spot = k;
            Render();
        }

        void UpgradeRod()
        {
            int cost = Fishing.RodCost(S, D);
            if (cost < 0) return;
            App.Modals.Confirm(Loc.T("Nâng cần câu"), Loc.F("Tốn {0} bi. Vùng xanh to hơn, mở thêm chỗ câu xa.", cost), Loc.T("Nâng"), () =>
            {
                if (!Fishing.UpgradeRod(S, D)) App.Toasts.Show(Loc.T("Không đủ bi"), Icon("ball"));
                else
                {
                    App.Save.Save();
                    App.Toasts.Show(Loc.F("Cần câu cấp {0}", Casino.Of(S).rod), Icon("star"));
                }
                Render();
            }, null, BtnColor.Green);
        }

        void Sell()
        {
            int v = Fishing.SellCreel(S, D);
            if (v <= 0) return;
            App.Save.Save();
            App.Audio.Play("coin");
            App.Toasts.Show(Loc.F("Bán cá được {0} bi", v), Icon("ball"));
            Render();
            onRefresh?.Invoke();
        }

        void BuyBait()
        {
            if (!Fishing.BuyBait(S, D))
            {
                App.Toasts.Show(Loc.T("Không đủ bi"), Icon("ball"));
                return;
            }
            App.Save.Save();
            Render();
        }

        // ---------- câu ----------

        void ToIdle()
        {
            st = St.Idle;
            bite = null;
            assist = null;
            aim = 0;
            power.fillAmount = 0;
            bobber.gameObject.SetActive(false);
            line.gameObject.SetActive(false);
            bang.gameObject.SetActive(false);
            reel.gameObject.SetActive(false);
            hint.text = Fishing.BaitLeft(S, D, Now) > 0 ? Loc.T("Vuốt lên trên mặt nước để quăng") : Loc.T("Hết mồi: mua mồi hoặc làm nhiệm vụ quán trọ");
        }

        void Release()
        {
            float pw = aim;
            power.fillAmount = 0;
            if (pw < 0.08f)
            {
                st = St.Idle;
                return;
            }
            var s = S;
            var d = D;
            double now = Now;
            bool firstEver = Casino.Of(s).dex.Count == 0 && spot == 0;
            string why = null;
            bite = firstEver ? Fishing.FirstCast(s, d, now, rng) : Fishing.Cast(s, d, spot, pw, now, rng, out why);
            if (bite == null)
            {
                App.Toasts.Show(why, Icon("lock"));
                ToIdle();
                return;
            }
            App.Save.Save();
            Render();
            App.Audio.Play("whoosh");
            // phao bay từ đầu cần tới chỗ quăng: càng mạnh càng xa (cao trên màn)
            var wr = water.rect;
            flyFrom = rodTip.anchoredPosition.y;
            flyTo = Mathf.Lerp(wr.yMin + wr.height * 0.25f, wr.yMax - wr.height * 0.12f, pw);
            bobPos = new Vector2(rodTip.anchoredPosition.x + (float)rng.Range(-120, 120) * pw, flyFrom);
            bobber.gameObject.SetActive(true);
            line.gameObject.SetActive(true);
            st = St.Fly;
            t = 0;
            hint.text = "";
        }

        void Hook()
        {
            st = St.Reel;
            bang.gameObject.SetActive(false);
            Haptics.Play(Haptic.UiTap);
            if (bite.king)
            {
                // Cá Vua: gọi tướng khắc hệ cá phụ kéo (tướng đã có), có thì vùng xanh to thêm
                assist = D.Heroes.Where(h => !h.minion && S.Hero(h.id)?.owned == true && Elements.Beats(h.elem) == bite.fish.elem)
                    .OrderByDescending(h => S.Hero(h.id).star).Select(h => h.id).FirstOrDefault();
                App.Toasts.Show(assist != null ? Loc.F("Cá Vua! {0} phụ kéo", D.Hero(assist).name) : Loc.T("Cá Vua! Không có tướng khắc hệ để phụ kéo"), Icon("star"));
            }
            zoneH = (float)Fishing.Zone(S, D, bite, assist);
            zoneC = 0.3f;
            zoneV = 0;
            fishP = 0.3f;
            fishTarget = 0.5f;
            fishSpeed = 0.22f * (float)bite.pull;
            prog = 0.3f;
            nextTurn = 0;
            reel.gameObject.SetActive(true);
            reelFishImg.color = Theme.Of(bite.fish.elem);
            hint.text = Loc.T("Giữ để kéo vùng xanh lên, thả để hạ xuống");
        }

        void Update()
        {
            if (!water) return;
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            switch (st)
            {
                case St.Aim:
                    power.fillAmount = aim;
                    hint.text = Loc.F("Lực {0}%", Mathf.RoundToInt(aim * 100));
                    break;
                case St.Fly:
                    t += dt / 0.55f;
                    bobPos.y = Mathf.Lerp(flyFrom, flyTo, Mathf.SmoothStep(0, 1, t)) + Mathf.Sin(Mathf.Clamp01(t) * Mathf.PI) * 160;
                    if (t >= 1)
                    {
                        bobPos.y = flyTo;
                        st = St.Wait;
                        t = 0;
                        App.Audio.Play("splash");
                        hint.text = Loc.T("Chờ cá cắn câu...");
                    }
                    break;
                case St.Wait:
                    t += dt;
                    if (t >= bite.wait)
                    {
                        st = St.Bite;
                        t = 0;
                        bang.gameObject.SetActive(true);
                        Haptics.Play(Haptic.UiTap);
                        hint.text = Loc.T("Chạm ngay!");
                    }
                    break;
                case St.Bite:
                    t += dt;
                    if (t > C.biteWindow + 0.1f)
                    {
                        App.Toasts.Show(Loc.T("Cá sổng mất, mất mồi"), Icon("fish"));
                        ToIdle();
                    }
                    break;
                case St.Reel:
                    StepReel(dt);
                    break;
            }
            // đầu cần: đỉnh thanh cần (neo đáy giữa mặt nước, lệch 150, cao 420, nghiêng 18 độ; CasinoFishingMenu)
            rodTip.anchoredPosition = new Vector2(150 - Mathf.Sin(18 * Mathf.Deg2Rad) * 420, water.rect.yMin - 40 + Mathf.Cos(18 * Mathf.Deg2Rad) * 420);
            // phao, dây
            if (bobber.gameObject.activeSelf)
            {
                float bob = st == St.Wait ? Mathf.Sin(Time.unscaledTime * 3.2f) * 6 : st == St.Bite ? -18 + Mathf.Sin(Time.unscaledTime * 30) * 6 : 0;
                bobber.anchoredPosition = bobPos + new Vector2(0, bob);
                bang.anchoredPosition = bobber.anchoredPosition + new Vector2(0, 70);
                Vector2 a = rodTip.anchoredPosition, b = bobber.anchoredPosition;
                line.anchoredPosition = (a + b) / 2;
                line.sizeDelta = new Vector2(4, (b - a).magnitude);
                line.localEulerAngles = new Vector3(0, 0, Mathf.Atan2(b.y - a.y, b.x - a.x) * Mathf.Rad2Deg - 90);
            }
        }

        void StepReel(float dt)
        {
            // cá: đổi đích theo nhịp, cá hiếm đổi nhanh, giật mạnh
            nextTurn -= dt;
            if (nextTurn <= 0)
            {
                fishTarget = (float)rng.Range(0.05, 0.95);
                nextTurn = (float)rng.Range(0.5, 1.3) / Mathf.Max(0.6f, (float)bite.pull * 0.6f);
            }
            fishP = Mathf.MoveTowards(fishP, fishTarget, fishSpeed * dt * (1 + 0.6f * Mathf.Sin(Time.unscaledTime * 7)));
            // vùng xanh: giữ thì nổi, thả thì chìm
            zoneV += (holding ? 2.4f : -2.0f) * dt;
            zoneV = Mathf.Clamp(zoneV, -1.2f, 1.2f);
            zoneC += zoneV * dt;
            float half = zoneH / 2;
            if (zoneC < half) { zoneC = half; zoneV = Mathf.Max(0, zoneV) * 0.3f; }
            if (zoneC > 1 - half) { zoneC = 1 - half; zoneV = Mathf.Min(0, zoneV) * 0.3f; }
            bool inside = Mathf.Abs(fishP - zoneC) <= half;
            prog += (inside ? 0.32f : -0.2f * (0.7f + 0.15f * (float)bite.pull)) * dt;
            float h = reel.rect.height;
            reelZone.anchoredPosition = new Vector2(0, zoneC * h);
            reelZone.sizeDelta = new Vector2(reelZone.sizeDelta.x, zoneH * h);
            reelFish.anchoredPosition = new Vector2(0, fishP * h);
            reelProgress.fillAmount = Mathf.Clamp01(prog);
            reelProgress.color = inside ? Theme.Green : Theme.Orange;
            if (prog >= 1) Land();
            else if (prog <= 0)
            {
                App.Toasts.Show(bite.king ? Loc.T("Cá Vua thoát rồi!") : Loc.T("Cá sổng mất"), Icon("fish"));
                Haptics.Play(Haptic.Lose);
                ToIdle();
            }
        }

        void Land()
        {
            var s = S;
            var d = D;
            var c = Fishing.Land(s, d, bite, Now, rng);
            App.Save.Save();
            App.Audio.Play(bite.fish.rar >= Rarity.Epic || bite.king ? "win" : "coin");
            Haptics.Play(bite.fish.rar >= Rarity.Rare ? Haptic.Win : Haptic.UiTap);
            st = St.Result;
            reel.gameObject.SetActive(false);
            bobber.gameObject.SetActive(false);
            line.gameObject.SetActive(false);
            hint.text = "";
            result.SetActive(true);
            resDot.color = Theme.Of(c.fish.elem);
            resRing.color = Theme.Of(c.fish.rar);
            resName.text = c.fish.Name;
            var tags = new List<string> { Elements.RarityName(c.fish.rar), Loc.F("{0} cm", c.size.ToString("0.#")) };
            if (c.king) tags.Add(Loc.T("Cá Vua"));
            if (c.first) tags.Add(Loc.T("Lần đầu!"));
            else if (c.record) tags.Add(Loc.T("Kỷ lục!"));
            resInfo.text = string.Join(" · ", tags);
            string rw = CasinoUi.Rewards(c.rewards);
            if (c.setDone is Elem e) rw = Loc.F("Đủ 6 loài hệ {0}!", Elements.Name(e)) + (rw.Length > 0 ? "\n" + rw : "");
            if (!c.king) rw = (rw.Length > 0 ? rw + "\n" : "") + Loc.F("Vào giỏ, bán ở đây được {0} bi", Fishing.Price(d, new CaughtFish { id = c.fish.id, size = c.size }));
            resRewards.text = rw;
            Render();
            onRefresh?.Invoke();
        }

        // ---------- Sổ Cá ----------

        void ShowDex()
        {
            var s = S;
            var st2 = Casino.Of(s);
            var fish = C.fish;
            for (int i = 0; i < dexCells.Length; i++)
            {
                var cell = dexCells[i];
                bool has = i < fish.Count;
                cell.dot.transform.parent.gameObject.SetActive(has);
                if (!has) continue;
                var f = fish[i];
                bool caught = st2.dex.TryGetValue(f.id, out var rec) && rec.n > 0;
                cell.dot.color = caught ? Theme.Of(f.elem) : new Color(0.8f, 0.77f, 0.7f);
                cell.ring.color = caught ? Theme.Of(f.rar) : new Color(0.7f, 0.66f, 0.6f);
                cell.name.text = caught ? f.Name : "???";
                cell.info.text = caught ? Loc.F("×{0} · {1} cm", rec.n, rec.best.ToString("0.#")) : (f.night ? Loc.T("cắn ban đêm") : Elements.RarityName(f.rar));
            }
            var king = Fishing.KingOf(D, Now);
            dexHead.text = Loc.F("Đã bắt {0}/{1} loài · đủ bộ hệ: {2}", st2.dex.Count(kv => kv.Value.n > 0 && fish.Any(f => f.id == kv.Key)), fish.Count,
                               st2.sets.Count == 0 ? "—" : string.Join(", ", st2.sets.Select(k => Elements.Name(Keys.ToElem(k))))) +
                           (king != null ? "\n" + Loc.F("Cá Vua tuần này: {0} ({1}) ở {2}, cần câu cấp {3}", king.Name, Elements.Name(king.elem),
                               C.spots[C.spots.Count - 1].Name, C.kingRod) : "");
            dex.SetActive(true);
        }

        // cho lượt chụp thử: quăng lực pw, chờ cắn, giật, tự kéo tới khi xong
        public System.Collections.IEnumerator AutoCast(float pw, System.Action<string> shot)
        {
            if (st != St.Idle) yield break;
            st = St.Aim;
            aim = pw;
            yield return null;
            shot?.Invoke("ngam");
            Release();
            while (st == St.Fly || st == St.Wait) yield return null;
            shot?.Invoke("can_cau");
            if (st == St.Bite) Hook();
            float t0 = Time.realtimeSinceStartup;
            bool shotReel = false;
            while (st == St.Reel && Time.realtimeSinceStartup - t0 < 20)
            {
                holding = zoneC < fishP; // kéo khéo: theo cá
                if (!shotReel && Time.realtimeSinceStartup - t0 > 1.2f)
                {
                    shotReel = true;
                    shot?.Invoke("keo");
                }
                yield return null;
            }
            holding = false;
            yield return new WaitForSecondsRealtime(0.4f);
            shot?.Invoke("ket_qua");
        }

        public void ShowDexForTest() => ShowDex();
    }

    // chữ thưởng của đảo (ô thưởng đẹp dùng chung để C8)
    public static class CasinoUi
    {
        public static string Rewards(List<Reward> rs)
        {
            if (rs == null || rs.Count == 0) return "";
            var d = App.Data;
            var parts = new List<string>();
            foreach (var r in rs)
                switch (r.k)
                {
                    case RewardKind.Balls: parts.Add(Loc.F("+{0} bi", r.n)); break;
                    case RewardKind.Bait: parts.Add(Loc.F("+{0} mồi", r.n)); break;
                    case RewardKind.Shards:
                        string h = r.res?.hero ?? r.hero;
                        parts.Add(Loc.F("+{0} mảnh {1}", r.res?.n ?? r.n, h != null ? d.Hero(h)?.name : "")); break;
                    case RewardKind.EvoStones: parts.Add(Loc.F("+{0} đá tiến hóa", r.n)); break;
                    case RewardKind.Stones: parts.Add(Loc.F("+{0} đá tiềm năng", r.n)); break;
                    case RewardKind.Crystal: parts.Add(Loc.F("+{0} đá tinh", r.n)); break;
                    case RewardKind.Card: parts.Add(Loc.T("+1 bản sao thẻ")); break;
                    case RewardKind.Egg: parts.Add(Loc.F("+{0} trứng", r.n)); break;
                    case RewardKind.Exp: parts.Add(Loc.F("+{0} EXP", r.n)); break;
                    default: parts.Add("+" + r.n); break;
                }
            return string.Join(" · ", parts);
        }
    }
}
