// Hang Tiềm Năng, bản sân khấu. Người dùng 2026-11-27 (chê bản danh sách 10 hàng chữ): "thiết kế lại hang tiềm năng, ít chữ thôi nhưng
// vẫn phải đủ thông tin; tham khảo đấu trường ngầm và võ đường huy hiệu của Clash of Critters; phần thưởng phải để ở thanh progress ở
// trên, thể hiện bằng icon". Prefab Screens/Cave do menu "PokiClash/Prefab/Nhà và side meta/Hang Tiềm Năng: dựng sân khấu"
// (Editor/CaveStageMenu.cs) dựng; ảnh ở Assets/03 Art/Cave (ArtGen/Cave). Luật: Core/Potential.cs (CaveStage, WinCave...).
// - Sân khấu (dưới Canvas/Nen, rộng 1080, neo mép trên, dời xuống theo tai thỏ để khớp khung an toàn): nền hang (vòm cầu thang xuống
//   sâu, bảng đá trống trên vòm, bệ đá sáng ở giữa).
// - Thanh tiến độ (ngay dưới thanh tên màn): 10 nút tầng trên một rãnh, phần rãnh tới tầng đang chờ vượt tô vàng. Mỗi nút là ICON THƯỞNG
//   LẦN ĐẦU quý nhất của tầng (đá tiến hóa > đá tinh > đá tiềm năng) kèm số; tầng đã qua: icon mờ + dấu tích; tầng khoá: nút tối; tầng
//   đang xem: nút to, viền vàng, mũi tên chỉ xuống; tầng đang chờ vượt nhún nhẹ. Đầu thanh: hệ boss hôm nay (trái), đá tiềm năng và đá
//   tinh đang có (phải). Chạm nút: xem tầng đó.
// - Bảng đá trên vòm: "Tầng n · tên" (màu theo độ sâu, viền mực) và hàng icon thưởng lần đầu đủ món kèm số; đã qua thì dấu "Đã qua".
// - Bệ đá: boss (to, trước) và tướng phụ (sau) là rig thật đứng idle, nhìn sang trái; dưới chân thẻ cấp (boss đỏ khi người chơi thấp hơn
//   cấp tầng quá 2). Tầng khoá: hai con thành bóng tối, ổ khoá + "Qua tầng n để mở". Đổi tầng: vuốt ngang trên bệ, mũi tên hai bên hoặc
//   chạm nút; đôi cũ lướt ra, đôi mới chạy từ lòng vòm ra (nhỏ rồi to dần, nhún một cái).
// - Chạm bệ / bảng đá: hộp chi tiết (tên địch, cấp, thưởng, luật lượt, lịch hệ boss).
// - Dải đáy (khung an toàn): thẻ lượt thắng còn hôm nay (hết lượt thì thành nút "+1 lượt" quảng cáo nếu còn), nút Vượt / Đánh / Khoá /
//   Hết lượt, thẻ thưởng mỗi trận thắng (đá + đá tinh trận thắng đầu ngày ở tầng cao); hàng 5 hệ: ngày thường hệ hôm nay sáng, hệ khác
//   tối kèm thứ (T2…T6, chạm: báo ngày); cuối tuần cả 5 sáng, chạm để chọn hệ boss.
// Mọi vật dựng sẵn trong prefab; lúc chạy chỉ dựng sticker tướng (mỗi khung một cái).
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    // về lại Hang sau một trận (CaveResult "Về Hang"): xem lại tầng vừa đánh; vừa thắng tầng đang chờ vượt thì sang tầng vừa mở
    public sealed class CaveBack
    {
        public int tier;
        public bool won;
    }

    public sealed class CaveScene : SceneRoot
    {
        // một nút tầng trên thanh tiến độ
        [Serializable]
        public struct Node
        {
            public RectTransform root;
            public Image ring, disc, icon;
            public GameObject countTag, done; // thẻ số món, huy hiệu đã qua
            public TextMeshProUGUI count, num;
            public ClickCatcher click;
        }

        // chỗ đứng một địch trên bệ: gốc ở chân; body chứa sticker, portrait là chân dung tĩnh hiện trước khi rig sẵn; thẻ cấp dưới chân
        [Serializable]
        public struct Spot
        {
            public RectTransform root, body;
            public HeroPortrait portrait;
            public GameObject tag;
            public TextMeshProUGUI tagText;
        }

        // một món thưởng lần đầu trên bảng đá
        [Serializable]
        public struct Prize
        {
            public RectTransform root;
            public Image icon;
            public TextMeshProUGUI count;
        }

        // một ô hệ ở hàng đáy
        [Serializable]
        public struct Tab
        {
            public SketchButton button;
            public Image icon;
            public TextMeshProUGUI label;
        }

        public override string Title => Loc.T("Hang Tiềm Năng");

        [SerializeField] RectTransform stage;
        [SerializeField] Node[] nodes;
        [SerializeField] RectTransform trackFill, marker;
        [SerializeField] Image headElem;
        [SerializeField] GameObject headBadge; // đĩa kem chứa icon hệ ở đầu thanh
        [SerializeField] TextMeshProUGUI headText, stones, crystals;
        [SerializeField] RectTransform tablet;
        [SerializeField] TextMeshProUGUI floorName, passed, firstLabel;
        [SerializeField] Prize[] prizes;
        [SerializeField] ClickCatcher tabletTap;
        [SerializeField] RectTransform squad;
        [SerializeField] CanvasGroup squadGroup;
        [SerializeField] Spot[] spots; // 0 boss, 1 tướng phụ
        [SerializeField] GameObject lockMark, pickHint;
        [SerializeField] TextMeshProUGUI lockText;
        [SerializeField] SwipeArea swipe;
        [SerializeField] SketchButton prev, next;
        [SerializeField] GameObject winsTag, perWin, perWinCrystalIcon;
        [SerializeField] TextMeshProUGUI wins, perWinStones, perWinCrystal;
        [SerializeField] SketchButton ad, go;
        [SerializeField] Tab[] tabs;
        [SerializeField] Sprite stoneIcon, crystalIcon, evoIcon;

        static readonly string[] DayNames = { "Chủ nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy" };
        static readonly string[] DayShort = { "CN", "T2", "T3", "T4", "T5", "T6", "T7" };
        // màu tên tầng theo độ sâu: xanh lá → lam → cam → tím → đỏ
        static readonly string[] TierColors = { "#5fb544", "#3f9a2e", "#3f86d6", "#2f6fc0", "#f08f22", "#d9771b", "#9a4df0", "#7a2bd0", "#e0453a", "#c0202f" };
        // nút tầng (nền sáng để icon màu đọc rõ trên thanh tối; người dùng 2026-11-27 chê bản lõi tối "khó nhìn"): đã qua / đang chờ
        // vượt / khoá
        static readonly Color DoneFill = new Color32(0xc6, 0xe6, 0xb8, 0xff), NextFill = new Color32(0xff, 0xf1, 0xc4, 0xff),
            LockFill = new Color32(0xd6, 0xd0, 0xe4, 0xff), NodeInk = new Color32(0x2a, 0x1d, 0x16, 0xff);
        static readonly Color DimNum = new Color32(0xc9, 0xc3, 0xdc, 0xff);
        static readonly Color TabDark = new Color32(0x3e, 0x39, 0x58, 0xff);
        // lòng vòm (toạ độ sân khấu, gốc mép trên giữa): đôi mới chạy từ đây ra
        static readonly Vector2 Gate = new Vector2(-16, -930);
        // chỗ đứng (x, y chân, cao dáng đứng): boss trước bên trái, tướng phụ sau bên phải; đứng gần mép trước bệ
        static readonly Vector3[] Stand = { new Vector3(-90, -1322, 440), new Vector3(292, -1196, 290) };
        // sân khấu cao bằng ảnh nền 1144 x 2048 thu về bề ngang 1080; mũi tên cách tâm (đơn vị màn)
        const float StageH = 2048 * 1080f / 1144, ArrowX = 476;
        const float SlideOut = 0.13f, SlideX = 560, RunLen = 0.32f, RunLag = 0.08f, RigWait = 0.6f, PrizeGap = 132, FirstLabelW = 120;

        int cur, day = -1, bindFrame;
        Elem? elem;
        bool sliding, locked, stageKnown;
        float t, dragX, nextTick, fillTime, stageY0;
        Coroutine slideCo;
        readonly AolaSticker[] anim = new AolaSticker[2];
        readonly string[] waitForm = new string[2];
        readonly HeroDef[] heroes = new HeroDef[2];
        readonly float[] heights = new float[2];
        readonly Vector2[] standPos = new Vector2[2];

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static int Today => Afk.Today(SaveService.Now());
        static int Count => D.Cfg.cave.tiers.Count;
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // ---------- dựng prefab (Editor) ----------

        public void SetupBand(RectTransform stageRt, Node[] nodeList, RectTransform fill, RectTransform markerRt, GameObject elemBadge, Image elemIcon,
            TextMeshProUGUI head, TextMeshProUGUI stoneText, TextMeshProUGUI crystalText)
        {
            stage = stageRt; nodes = nodeList; trackFill = fill; marker = markerRt; headBadge = elemBadge; headElem = elemIcon; headText = head;
            stones = stoneText; crystals = crystalText;
        }

        public void SetupTablet(RectTransform tabletRt, TextMeshProUGUI nameText, TextMeshProUGUI passedText, TextMeshProUGUI firstText, Prize[] prizeList,
            ClickCatcher tap)
        {
            tablet = tabletRt; floorName = nameText; passed = passedText; firstLabel = firstText; prizes = prizeList; tabletTap = tap;
        }

        public void SetupStage(RectTransform squadRt, CanvasGroup squadCg, Spot[] spotList, GameObject lockRoot, TextMeshProUGUI lockLabel,
            GameObject pickRoot, SwipeArea swipeArea, SketchButton prevBtn, SketchButton nextBtn)
        {
            squad = squadRt; squadGroup = squadCg; spots = spotList; lockMark = lockRoot; lockText = lockLabel; pickHint = pickRoot; swipe = swipeArea;
            prev = prevBtn; next = nextBtn;
        }

        public void SetupBottom(GameObject winsRoot, TextMeshProUGUI winsText, SketchButton adBtn, SketchButton goBtn, GameObject perWinRoot,
            TextMeshProUGUI perWinStoneText, GameObject crystalIconGo, TextMeshProUGUI perWinCrystalText, Tab[] tabList)
        {
            winsTag = winsRoot; wins = winsText; ad = adBtn; go = goBtn; perWin = perWinRoot; perWinStones = perWinStoneText;
            perWinCrystalIcon = crystalIconGo; perWinCrystal = perWinCrystalText; tabs = tabList;
        }

        public void SetupIcons(Sprite stone, Sprite crystal, Sprite evo)
        {
            stoneIcon = stone; crystalIcon = crystal; evoIcon = evo;
        }

        // ---------- vào / ra ----------

        public override void Enter(object args)
        {
            Fit();
            prev.SetOnClick(() => Step(-1));
            next.SetOnClick(() => Step(1));
            swipe.Began = () => dragX = 0;
            swipe.Dragged = d => dragX += d.x;
            swipe.Ended = () =>
            {
                if (Mathf.Abs(dragX) > Screen.width * 0.06f) Step(dragX < 0 ? 1 : -1);
            };
            swipe.Tapped = _ => Detail();
            tabletTap.OnClick = Detail;
            for (int i = 0; i < nodes.Length; i++)
            {
                int k = i;
                nodes[i].click.OnClick = () => Jump(k);
            }
            go.SetOnClick(Fight);
            squad.anchoredPosition = Vector2.zero;
            squadGroup.alpha = 1;
            sliding = false;
            day = Today;
            int n = Count;
            int grow = -1;
            if (args is CaveBack back)
            {
                cur = back.tier;
                // vừa thắng tầng đang chờ vượt: sang tầng vừa mở, rãnh vàng chạy tới nút mới
                if (back.won && S.caveFloor == back.tier + 1 && back.tier + 1 < n)
                {
                    cur = back.tier + 1;
                    grow = back.tier;
                }
            }
            else cur = S.caveFloor; // tầng đang chờ vượt (qua hết thì tầng cuối)
            cur = Mathf.Clamp(cur, 0, Mathf.Max(0, n - 1));
            Render();
            FillSquad();
            slideCo = StartCoroutine(RunOut());
            if (grow >= 0) StartCoroutine(GrowFill(grow));
        }

        public override void Exit() => ClearSquad();

        void OnDestroy() => ClearSquad();

        // bản lưu đổi (quảng cáo +1 lượt, chọn hệ ở chỗ khác...): vẽ lại; hệ boss đổi thì bày lại đôi địch
        public override void Refresh()
        {
            var old = elem;
            Render();
            if (old == elem) return;
            FillSquad();
            if (slideCo != null) StopCoroutine(slideCo);
            slideCo = StartCoroutine(RunOut());
        }

        // sân khấu neo mép trên màn (Canvas/Nen phủ cả tai thỏ): dời xuống bằng phần tai thỏ để thanh tiến độ nằm ngay dưới thanh tên màn
        // và chữ trên bảng đá khớp ảnh; phần trên lộ ra là lớp "tran" cùng màu trần hang
        void Fit()
        {
            if (!stage || !Frame) return;
            if (!stageKnown)
            {
                stageY0 = stage.anchoredPosition.y;
                stageKnown = true;
            }
            var nen = (RectTransform)stage.parent;
            var a = new Vector3[4];
            var b = new Vector3[4];
            nen.GetWorldCorners(a);
            Frame.GetWorldCorners(b);
            float sc = nen.lossyScale.y;
            Inset = sc > 0 ? Mathf.Max(0, (a[1].y - b[1].y) / sc) : 0;
            stage.anchoredPosition = new Vector2(stage.anchoredPosition.x, stageY0 - Inset);
            // màn dài hơn ảnh: phóng sân khấu cho đáy ảnh chạm đáy màn (bệ xuống sát dải đáy, không chừa khoảng trống dưới tướng;
            // người dùng 2026-11-27); hai mũi tên giữ cỡ và chỗ trên màn
            float s = Mathf.Max(1f, (nen.rect.height - Inset) / StageH);
            stage.localScale = new Vector3(s, s, 1);
            foreach (var (btn, side) in new[] { (prev, -1), (next, 1) })
            {
                if (!btn) continue;
                btn.Rect.localScale = new Vector3(1 / s, 1 / s, 1);
                btn.Rect.anchoredPosition = new Vector2(side * ArrowX / s, btn.Rect.anchoredPosition.y);
            }
            Scale = s;
        }

        void Update()
        {
            t += Mathf.Min(0.05f, Time.unscaledDeltaTime);
            Fit();
            for (int i = 0; i < anim.Length; i++)
            {
                if (anim[i] == null) continue;
                anim[i].Tint = locked ? 0.12f : 1f;
                anim[i].Show(HeroViewer.Idle, t + i * 0.37f, true, squadGroup.alpha, false, 0);
            }
            // nút tầng đang chờ vượt nhún nhẹ (khi không phải tầng đang xem)
            int fr = S.caveFloor;
            if (fr >= 0 && fr < Count && fr < nodes.Length && fr != cur)
            {
                float sc = 1 + 0.07f * Mathf.Max(0, Mathf.Sin(t * 5f));
                nodes[fr].root.localScale = new Vector3(sc, sc, 1);
            }
            if (Time.unscaledTime < nextTick) return;
            nextTick = Time.unscaledTime + 0.5f;
            // qua 0 giờ: hệ boss, lượt đổi; bày lại
            if (Today != day)
            {
                day = Today;
                Render();
                FillSquad();
                if (slideCo != null) StopCoroutine(slideCo);
                slideCo = StartCoroutine(RunOut());
            }
        }

        // dựng sticker đang chờ: không trong khung vừa bày, mỗi khung một cái, boss trước
        void LateUpdate()
        {
            if (Time.frameCount <= bindFrame || !AolaSticker.CanBuildNow) return;
            bool late = Time.unscaledTime - fillTime > RigWait;
            for (int i = 0; i < waitForm.Length; i++)
                if (waitForm[i] != null && heroes[i] != null && late) spots[i].portrait.gameObject.SetActive(true);
            for (int i = 0; i < waitForm.Length; i++)
            {
                if (waitForm[i] == null) continue;
                if (heroes[i] == null)
                {
                    waitForm[i] = null;
                    continue;
                }
                if (!AolaActor.Ready(waitForm[i])) continue;
                anim[i] = AolaSticker.TryCreate(spots[i].body, heroes[i], waitForm[i], heights[i], true);
                if (anim[i] != null)
                {
                    anim[i].HideShadow();
                    spots[i].portrait.gameObject.SetActive(false);
                }
                waitForm[i] = null;
                return;
            }
        }

        // ---------- vẽ ----------

        // thưởng lần đầu đủ món: đá tiềm năng, đá tinh, đá tiến hóa
        List<(Sprite icon, int n)> FirstItems(CaveTier ct)
        {
            var list = new List<(Sprite, int)>();
            if (ct.firstStones > 0) list.Add((stoneIcon, ct.firstStones));
            if (ct.firstCrystals > 0) list.Add((crystalIcon, ct.firstCrystals));
            if (ct.firstEvo > 0) list.Add((evoIcon, ct.firstEvo));
            return list;
        }

        // món quý nhất của thưởng lần đầu (icon trên nút tầng)
        (Sprite icon, int n) Best(CaveTier ct) =>
            ct.firstEvo > 0 ? (evoIcon, ct.firstEvo) : ct.firstCrystals > 0 ? (crystalIcon, ct.firstCrystals) : (stoneIcon, ct.firstStones);

        static string FirstText(CaveTier ct)
        {
            var parts = new List<string>();
            if (ct.firstStones > 0) parts.Add(Loc.F("{0} đá tiềm năng", ct.firstStones));
            if (ct.firstCrystals > 0) parts.Add(Loc.F("{0} đá tinh", ct.firstCrystals));
            if (ct.firstEvo > 0) parts.Add(Loc.F("{0} đá tiến hóa", ct.firstEvo));
            return string.Join(", ", parts);
        }

        float NodeX(int k) => nodes[Mathf.Clamp(k, 0, nodes.Length - 1)].root.anchoredPosition.x;

        void SetFill(float x)
        {
            float x0 = NodeX(0);
            trackFill.sizeDelta = new Vector2(Mathf.Max(0, x - x0), trackFill.sizeDelta.y);
        }

        void Render()
        {
            var s = S;
            var d = D;
            var cfg = d.Cfg;
            int n = Count;
            if (n == 0) return;
            int wd = Potential.WeekdayOf(day);
            bool choose = cfg.cave.Weekday(wd) == null;
            elem = Potential.CaveElem(s, cfg, day);
            cur = Mathf.Clamp(cur, 0, n - 1);
            var ct = cfg.cave.tiers[cur];
            bool unlocked = Potential.CaveUnlocked(s, cfg, cur), first = Potential.CaveFirst(s, cur);
            locked = !unlocked;

            // đầu thanh: hệ boss hôm nay, đá đang có
            (headBadge ? headBadge : headElem.gameObject).SetActive(elem != null);
            if (elem is Elem z0)
            {
                headElem.sprite = Icon("e_" + Keys.Of(z0));
                headText.text = Loc.F("Boss hệ {0}", Elements.Name(z0));
            }
            else headText.text = Loc.T("Cuối tuần: chọn hệ boss");
            stones.text = s.potentialStones.ToString();
            crystals.text = s.potentialCrystals.ToString();

            // nút tầng
            for (int i = 0; i < nodes.Length; i++)
            {
                bool on = i < n;
                nodes[i].root.gameObject.SetActive(on);
                if (on) BindNode(nodes[i], i, cfg.cave.tiers[i], i == cur);
            }
            nodes[cur].root.SetAsLastSibling(); // nút đang xem (to hơn) vẽ đè hai nút cạnh
            SetFill(NodeX(Mathf.Min(s.caveFloor, n - 1)));
            marker.anchoredPosition = new Vector2(NodeX(cur), marker.anchoredPosition.y);

            // bảng đá: tên tầng, thưởng lần đầu
            floorName.text = Loc.F("Tầng {0} · {1}", cur + 1, ct.Name);
            floorName.color = Theme.Hex(TierColors[Mathf.Min(cur, TierColors.Length - 1)]);
            var items = FirstItems(ct);
            passed.gameObject.SetActive(!first);
            passed.text = Loc.T("Đã qua");
            // "Lần đầu" + các món, cả hàng căn giữa bảng
            float rowX = firstLabel ? FirstLabelW / 2 : 0;
            for (int i = 0; i < prizes.Length; i++)
            {
                bool on = first && i < items.Count;
                prizes[i].root.gameObject.SetActive(on);
                if (!on) continue;
                prizes[i].icon.sprite = items[i].icon;
                prizes[i].count.text = "×" + items[i].n;
                prizes[i].root.anchoredPosition = new Vector2(rowX + (i - (items.Count - 1) / 2f) * PrizeGap, prizes[i].root.anchoredPosition.y);
            }
            if (firstLabel)
            {
                firstLabel.gameObject.SetActive(first && items.Count > 0);
                firstLabel.text = Loc.T("Lần đầu");
                float edge = rowX - (items.Count - 1) / 2f * PrizeGap - PrizeGap / 2;
                firstLabel.rectTransform.anchoredPosition = new Vector2(edge, firstLabel.rectTransform.anchoredPosition.y);
            }

            // bệ: khoá, chọn hệ, thẻ cấp
            lockMark.SetActive(elem != null && locked);
            lockText.text = Loc.F("Qua tầng {0} để mở", cur);
            pickHint.SetActive(elem == null);
            prev.gameObject.SetActive(n > 1);
            next.gameObject.SetActive(n > 1);
            var st = elem is Elem z1 ? Potential.CaveStage(d, z1, cur) : null;
            for (int i = 0; i < spots.Length; i++)
            {
                var en = st != null && i < st.enemies.Count ? st.enemies[i] : null;
                bool show = en != null && !locked;
                spots[i].tag.SetActive(show);
                if (!show) continue;
                spots[i].tagText.text = $"Lv{en.level}";
                spots[i].tagText.color = en.boss && s.level < ct.level - 2 ? Theme.RedD : Theme.Ink;
            }

            // dải đáy: lượt, nút chính, thưởng mỗi trận thắng
            int left = Potential.CaveLeft(s, cfg, day);
            int total = cfg.cave.winsPerDay + AdGate.Used(s, day, AdGate.CaveExtra) * cfg.cave.adExtra;
            bool showAd = left <= 0 && Ads.Ready && Ads.Left(Ads.CaveExtra) > 0;
            winsTag.SetActive(!showAd);
            wins.text = left > 0 ? Loc.F("Lượt {0}/{1}", left, total) : Loc.T("Hết lượt");
            wins.color = left > 0 ? Theme.Ink : Theme.RedD;
            ad.gameObject.SetActive(showAd);
            if (showAd)
                ad.SetOnClick(() =>
                    Ads.Show(Ads.CaveExtra, ok =>
                    {
                        if (ok)
                        {
                            App.Save.Save();
                            App.Toasts.Show(Loc.T("+1 lượt Hang hôm nay"), stoneIcon);
                        }
                        Render();
                    }));
            bool can = elem != null && Potential.CaveCanEnter(s, cfg, day, cur);
            go.name = "vao_tang_" + cur;
            go.SetText(elem == null ? Loc.T("Chọn hệ") : locked ? Loc.T("Khoá") : first ? Loc.T("Vượt") : left > 0 ? Loc.T("Đánh") : Loc.T("Hết lượt"));
            go.SetRole(!can ? BtnColor.Paper : first ? BtnColor.Green : BtnColor.Yellow);
            go.Interactable = can;
            perWin.SetActive(elem != null);
            perWinStones.text = "+" + ct.stones;
            bool daily = cur + 1 >= cfg.cave.crystalFloor && cfg.cave.crystalDaily > 0 && Potential.CaveOf(s, day).wins == 0;
            perWinCrystalIcon.SetActive(daily);
            perWinCrystal.gameObject.SetActive(daily);
            perWinCrystal.text = "+" + cfg.cave.crystalDaily;

            // hàng hệ
            var zones = d.Zones.OrderBy(x => x.order).ToList();
            for (int k = 0; k < tabs.Length; k++)
            {
                bool on = k < zones.Count;
                tabs[k].button.gameObject.SetActive(on);
                if (!on) continue;
                var z = zones[k].id;
                var tb = tabs[k];
                int dayOf = Array.IndexOf(cfg.cave.weekday, (int)z);
                bool today = elem == z;
                tb.button.name = "chon_" + Keys.Of(z);
                tb.icon.sprite = Icon("e_" + Keys.Of(z));
                tb.label.text = today ? Loc.T("Hôm nay") : choose ? Elements.Name(z) : dayOf >= 0 ? Loc.T(DayShort[dayOf]) : "";
                // ô tô màu hệ (hệ không phải hôm nay ngả tối), icon trên đĩa kem viền mực nên luôn rõ (người dùng 2026-11-27 chê icon
                // mờ trên nền sọc tối "nhìn khó quá")
                var c = Theme.Of(z);
                tb.button.SetColor(today ? c : Color.Lerp(c, TabDark, choose ? 0.25f : 0.5f));
                tb.icon.color = Color.white;
                tb.label.color = today ? Theme.Yellow : Color.white;
                float sc = today ? 1.08f : 1f;
                tb.button.Rect.localScale = new Vector3(sc, sc, 1);
                tb.button.SetOnClick(() => PickElem(z, dayOf));
            }
        }

        void BindNode(Node nd, int i, CaveTier ct, bool sel)
        {
            var s = S;
            var cfg = D.Cfg;
            bool unlocked = Potential.CaveUnlocked(s, cfg, i), first = Potential.CaveFirst(s, i);
            var best = Best(ct);
            nd.icon.sprite = best.icon;
            nd.countTag.SetActive(best.n > 1);
            nd.count.text = "×" + best.n;
            nd.num.text = (i + 1).ToString();
            nd.done.SetActive(!first);
            nd.disc.color = !first ? DoneFill : unlocked ? NextFill : LockFill;
            nd.icon.color = !first ? new Color(1, 1, 1, 0.6f) : unlocked ? Color.white : new Color(1, 1, 1, 0.78f);
            nd.ring.color = sel ? Theme.Yellow : NodeInk;
            nd.num.color = sel ? Theme.Yellow : unlocked ? Color.white : DimNum;
            float sc = sel ? 1.16f : 1f;
            nd.root.localScale = new Vector3(sc, sc, 1);
        }

        // ---------- địch trên bệ ----------

        void ClearSquad()
        {
            for (int i = 0; i < anim.Length; i++)
            {
                anim[i]?.Destroy();
                anim[i] = null;
                waitForm[i] = null;
                heroes[i] = null;
            }
        }

        // bày đôi địch của tầng đang xem (boss, tướng phụ): sticker dựng dần ở LateUpdate; tướng chưa nhập rig thì chân dung tĩnh ngay
        void FillSquad()
        {
            ClearSquad();
            var d = D;
            var st = elem is Elem z ? Potential.CaveStage(d, z, cur) : null;
            for (int i = 0; i < spots.Length; i++)
            {
                var sp = spots[i];
                var en = st != null && i < st.enemies.Count ? st.enemies[i] : null;
                var h = en != null ? d.Hero(en.hero) : null;
                sp.root.gameObject.SetActive(h != null);
                if (h == null) continue;
                int star = Math.Max(1, Teams.EnemyStar(en.level));
                var stand = Stand[Mathf.Min(i, Stand.Length - 1)];
                heroes[i] = h;
                heights[i] = stand.z;
                standPos[i] = new Vector2(stand.x, stand.y);
                sp.root.anchoredPosition = standPos[i];
                sp.root.localScale = Vector3.one;
                string form = HeroArt.FormOf(h, star).aola;
                bool rig = AolaActor.Find(form, out _, out _);
                // chân dung tĩnh: phần có hình cao ~1,2 dáng đứng, đáy ở chân, lật như sticker (nhìn sang trái); tầng khoá thì bóng tối
                var c = PortraitBoxes.Of(form);
                sp.portrait.Bind(h, stand.z * 1.2f / Mathf.Max(0.2f, c.height), locked, star);
                var pr = sp.portrait.Rect;
                pr.anchorMin = pr.anchorMax = new Vector2(0.5f, 0);
                pr.pivot = new Vector2(c.center.x, c.yMin);
                pr.anchoredPosition = Vector2.zero;
                pr.localScale = new Vector3(-1, 1, 1);
                sp.portrait.gameObject.SetActive(!rig);
                if (rig)
                {
                    waitForm[i] = form;
                    AolaActor.Ready(form);
                }
            }
            bindFrame = Time.frameCount;
            fillTime = Time.unscaledTime;
        }

        // đôi vừa bày chạy từ lòng vòm ra chỗ đứng: chờ rig (tối đa RigWait), rồi từng con nhỏ → to, nhún một cái
        IEnumerator RunOut()
        {
            sliding = true;
            squad.anchoredPosition = Vector2.zero;
            squadGroup.alpha = 0;
            float t0 = Time.unscaledTime;
            while (App.Router.Busy && Time.unscaledTime - t0 < 10) yield return null; // vừa vào màn: chờ mây chuyển cảnh tan
            t0 = Time.unscaledTime;
            fillTime = Mathf.Max(fillTime, t0);
            while (waitForm.Any(w => w != null) && Time.unscaledTime - t0 < RigWait) yield return null;
            int n = heroes.Count(h => h != null);
            if (n > 0) App.Audio.Play("whoosh", 0.45f, 1.1f);
            float len = RunLen + RunLag * Mathf.Max(0, n - 1);
            for (float u = 0; u < len; u += Time.unscaledDeltaTime)
            {
                squadGroup.alpha = Mathf.Clamp01(u / 0.08f);
                for (int i = 0; i < spots.Length; i++)
                {
                    if (heroes[i] == null) continue;
                    float a = Mathf.Clamp01((u - i * RunLag) / RunLen);
                    float e = 1 - Mathf.Pow(1 - a, 3);
                    var p = Vector2.LerpUnclamped(Gate, standPos[i], e);
                    p.y += Mathf.Sin(a * Mathf.PI) * 46;
                    spots[i].root.anchoredPosition = p;
                    float sc = Mathf.Lerp(0.3f, 1f, e);
                    spots[i].root.localScale = new Vector3(sc, sc, 1);
                }
                yield return null;
            }
            squadGroup.alpha = 1;
            for (int i = 0; i < spots.Length; i++)
            {
                if (heroes[i] == null) continue;
                spots[i].root.anchoredPosition = standPos[i];
                spots[i].root.localScale = Vector3.one;
            }
            sliding = false;
            slideCo = null;
        }

        // vừa vượt tầng: rãnh vàng chạy từ nút cũ tới nút mới, nút mới nảy
        IEnumerator GrowFill(int from)
        {
            SetFill(NodeX(from));
            float t0 = Time.unscaledTime;
            while (App.Router.Busy && Time.unscaledTime - t0 < 10) yield return null;
            yield return new WaitForSecondsRealtime(0.35f);
            float x0 = NodeX(from), x1 = NodeX(from + 1);
            for (float u = 0; u < 0.45f; u += Time.unscaledDeltaTime)
            {
                float a = u / 0.45f;
                SetFill(Mathf.Lerp(x0, x1, 1 - (1 - a) * (1 - a)));
                yield return null;
            }
            SetFill(x1);
            App.Audio.Play("stamp", 0.55f, 1.15f);
            Haptics.Play(Haptic.UiTap);
            if (from + 1 < nodes.Length) yield return ChestBox.Pop(nodes[from + 1].root, 1.35f);
            Render();
        }

        // ---------- chọn tầng / hệ ----------

        void Step(int dir)
        {
            int n = Count;
            if (sliding || n < 2) return;
            Go((cur + dir + n) % n, dir);
        }

        void Jump(int k)
        {
            if (sliding || k == cur || k < 0 || k >= Count) return;
            Go(k, k > cur ? 1 : -1);
        }

        void Go(int k, int dir)
        {
            SketchButton.Sound?.Invoke("pick");
            Haptics.Play(Haptic.UiTap);
            if (slideCo != null) StopCoroutine(slideCo);
            slideCo = StartCoroutine(Slide(k, dir));
        }

        // đôi cũ lướt ra phía ngược hướng vuốt, đôi mới chạy từ lòng vòm ra; bảng đá nảy
        IEnumerator Slide(int k, int dir)
        {
            sliding = true;
            for (float u = 0; u < SlideOut; u += Time.unscaledDeltaTime)
            {
                float a = u / SlideOut;
                squad.anchoredPosition = new Vector2(-dir * SlideX * a * a, 0);
                squadGroup.alpha = 1 - a;
                yield return null;
            }
            cur = k;
            Render();
            FillSquad();
            StartCoroutine(ChestBox.Pop(tablet, 1.06f));
            yield return RunOut();
        }

        // ngày thường: hệ cố định theo thứ, chạm hệ khác chỉ báo ngày; cuối tuần: chọn hệ boss rồi bày lại đôi địch
        void PickElem(Elem z, int dayOf)
        {
            if (sliding) return;
            var cfg = D.Cfg;
            if (cfg.cave.Weekday(Potential.WeekdayOf(day)) != null)
            {
                if (elem == z) return;
                string when = dayOf >= 0 ? Loc.T(DayNames[dayOf]) : Loc.T("cuối tuần");
                App.Toasts.Show(Loc.F("Boss hệ {0}: {1} (cuối tuần tự chọn)", Elements.Name(z), when), Icon("e_" + Keys.Of(z)));
                return;
            }
            if (elem == z) return;
            Potential.CavePick(S, cfg, day, z);
            App.Save.Save();
            Go(cur, 1);
        }

        // ---------- hộp chi tiết, vào trận ----------

        // lịch hệ boss: "T2 Kim, T3 Mộc, …; T7, CN tự chọn"
        static string Schedule(BalanceConfig cfg)
        {
            var fixedDays = new List<string>();
            var free = new List<string>();
            foreach (int wd in new[] { 1, 2, 3, 4, 5, 6, 0 })
            {
                if (cfg.cave.Weekday(wd) is Elem z) fixedDays.Add(Loc.T(DayShort[wd]) + " " + Elements.Name(z));
                else free.Add(Loc.T(DayShort[wd]));
            }
            string text = string.Join(", ", fixedDays);
            if (free.Count > 0) text += Loc.F("; {0} tự chọn", string.Join(", ", free));
            return text;
        }

        void Detail()
        {
            if (sliding) return;
            var s = S;
            var d = D;
            var cfg = d.Cfg;
            var ct = cfg.cave.tiers[cur];
            var sb = new StringBuilder();
            if (elem is Elem z)
                foreach (var en in Potential.CaveStage(d, z, cur).enemies)
                    sb.AppendLine(Loc.F("{0}: {1}, cấp {2}", en.boss ? Loc.T("Boss") : Loc.T("Phụ"), d.Hero(en.hero)?.name ?? en.hero, en.level));
            else sb.AppendLine(Loc.T("Cuối tuần: chọn hệ boss ở hàng dưới."));
            if (!Potential.CaveUnlocked(s, cfg, cur)) sb.AppendLine(Loc.F("Chưa mở: qua tầng {0} trước.", cur));
            sb.AppendLine(Loc.F("Cấp đề nghị {0} (bạn cấp {1})", ct.level, s.level));
            sb.AppendLine();
            sb.AppendLine(Potential.CaveFirst(s, cur) ? Loc.F("Lần đầu qua: {0} (không cần lượt)", FirstText(ct)) : Loc.T("Đã qua lần đầu."));
            string win = Loc.F("Mỗi trận thắng: +{0} đá tiềm năng", ct.stones);
            if (cur + 1 >= cfg.cave.crystalFloor && cfg.cave.crystalDaily > 0)
                win += Loc.F(", trận thắng đầu ngày thêm {0} đá tinh", cfg.cave.crystalDaily);
            sb.AppendLine(win);
            sb.AppendLine(Loc.F("Mỗi ngày {0} lượt thắng, thua không mất lượt.", cfg.cave.winsPerDay));
            sb.Append(Loc.F("Hệ boss theo ngày: {0}.", Schedule(cfg)));
            App.Modals.Alert(Loc.F("Tầng {0} · {1}", cur + 1, ct.Name), sb.ToString(), Loc.T("Đóng"));
        }

        void Fight()
        {
            if (sliding) return;
            if (elem is Elem z && Potential.CaveCanEnter(S, D.Cfg, day, cur)) StagePrep.OpenCave(z, cur, day);
        }

        // ---------- cho lượt chụp ----------

        public void JumpForTest(int k) => Jump(k);
        public void StepForTest(int dir) => Step(dir);
        public void DetailForTest() => Detail();
        public bool SquadReady => !sliding && waitForm.All(w => w == null);
        public int Current => cur;
        public float Inset { get; private set; } // phần tai thỏ (đơn vị canvas) sân khấu đang dời xuống
        public float Scale { get; private set; } = 1; // hệ số phóng sân khấu cho vừa chiều cao màn
    }
}
