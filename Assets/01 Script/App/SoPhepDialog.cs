// Màn Sổ Phép (prefab Assets/04 Prefabs/Dialogs/SoPhep, biến thể tờ giấy gốc HopThoai trải kín màn như cửa hàng; menu "PokiClash/Prefab/
// Hộp thoại và màn/Sổ Phép"). Logic ở Core/SoPhep.cs, thiết kế GD_Claude/28_SoPhep.md (người dùng duyệt 2026-11-24).
// Nền tối, cây toả ra nối bằng đường (người dùng 2026-11-27: "nền tối thôi để nổi bật các skill tree, làm dạng cây hoặc graph toả ra nối
// bằng line"; tiêu đề không dùng chữ đen đậm). Đầu màn: số nét còn, số đá tiến hóa, đã vẽ x/40. Giữa: trang cuộn dọc 4 chương; mỗi chương
// một băng tên toả xuống 4 ô, 4 ô hội về ô chốt, ô chốt nối thân cây sang băng chương sau (prefab Items/OSoPhep đặt sẵn). Đường sáng màu
// chương khi ô ở đầu dưới đã vẽ; thân cây sáng khi chương sau đã mở. Chương khoá: băng và ô tối, ghi điều kiện mở. Đáy cố định (vùng ngón
// cái): tên ô, hiệu ứng (đang có → vẽ tiếp), nút mặt của ô chọn (đổi tự do), giá hoặc lý do chưa vẽ được, nút Vẽ, Gợi ý (vẽ theo đường
// gợi ý), Tẩy sổ (hoàn hết nét và đá, hỏi lại). Mở màn thì cuộn tới ô đang chọn.
// Lần đầu mở (khoảnh khắc "h_sophep" ở sảnh): chọn sẵn Lật Trang, khoanh nút Vẽ.
using System;
using System.Collections;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class SoPhepDialog : Dialog
    {
        public const int Chapters = 4, PerChapter = 5, MaxFaces = 5;
        // đường mỗi chương: 0..3 băng → ô thường j, 4..7 ô thường j → ô chốt, 8 ô chốt → băng chương sau (chương cuối không có)
        public const int LinesPerChapter = 9;
        public const string TutorDraw = "h_sophep3";

        [Serializable]
        public struct Parts
        {
            public TextMeshProUGUI points, stones, progress;
            public ScrollRect scroll;
            public TextMeshProUGUI[] chapterLabels, chapterTitles, chapterNeeds; // theo chương: "CHƯƠNG n", tên, điều kiện mở
            public Image[] chapterRims; // viền băng tên chương
            public CanvasGroup[] chapterGroups; // khối ô của chương
            public SoPhepTile[] tiles; // Chapters × PerChapter, theo thứ tự ô của chương trong cấu hình (ô chốt cuối)
            public Image[] lines; // Chapters × LinesPerChapter
            public Image panelRim; // vạch màu chương trên mép bảng đáy
            public TextMeshProUGUI selName, selDesc, selCost;
            public SketchButton[] faces; // MaxFaces nút mặt
            public SketchButton draw, suggest, reset;
            public Sprite[] icons; // icon vẽ riêng theo thứ tự ô của cấu hình (03 Art/SoPhep/<id>.png); thiếu thì mượn bộ icon chung
        }

        [SerializeField] Parts p;
        string sel;

        static SaveData S => App.Save.Data;
        static BalanceConfig Cfg => App.Data.Cfg;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        public static SoPhepDialog Open()
        {
            var dlg = App.Modals.Open<SoPhepDialog>();
            dlg.Show();
            return dlg;
        }

        void Show()
        {
            p.draw.SetOnClick(Draw);
            p.suggest.SetOnClick(Suggest);
            p.reset.SetOnClick(AskReset);
            for (int i = 0; i < p.faces.Length; i++)
            {
                int f = i;
                p.faces[i].SetOnClick(() => SetFace(f));
            }
            var c = Cfg.sophep;
            var buyable = c.nodes.FirstOrDefault(n => SoPhep.Block(S, Cfg, n.id) == "");
            sel = (buyable ?? c.nodes.FirstOrDefault())?.id;
            bool first = !Tutorial.Done(S, TutorDraw) && SoPhep.Spent(S, Cfg) == 0 && SoPhep.Block(S, Cfg, "lat_trang") == "";
            if (first) sel = "lat_trang";
            Refresh();
            ScrollTo(TileOf(sel));
            Guide.Mark("sophep.draw", p.draw);
            if (first) Guide.Force(TutorDraw, "sophep.draw", Loc.T("Vẽ Lật Trang: mỗi trận được đổi cả bộ thẻ đang chọn một lần."), null, true);
        }

        void Refresh()
        {
            var s = S;
            var cfg = Cfg;
            var c = cfg.sophep;
            p.points.text = Loc.F("Nét: {0}", SoPhep.Free(s, cfg));
            p.stones.text = Loc.F("Đá tiến hóa: {0}", s.evoStones);
            p.progress.text = Loc.F("Đã vẽ {0}/{1} nét", SoPhep.Spent(s, cfg), SoPhep.Total(cfg));
            for (int ch = 0; ch < Chapters && ch < c.chapters.Count; ch++)
            {
                bool open = SoPhep.ChapterOpen(s, cfg, ch);
                var chc = SoPhepColors.Chapter(ch);
                if (ch < p.chapterLabels.Length)
                {
                    p.chapterLabels[ch].text = Loc.F("Chương {0}", ch + 1).ToUpperInvariant();
                    p.chapterLabels[ch].color = open ? chc : SoPhepColors.Dim;
                }
                if (ch < p.chapterTitles.Length)
                {
                    p.chapterTitles[ch].text = c.chapters[ch].Name;
                    p.chapterTitles[ch].color = open ? SoPhepColors.Cream : SoPhepColors.Muted;
                }
                if (ch < p.chapterRims.Length) p.chapterRims[ch].color = open ? chc : SoPhepColors.Dim;
                if (ch < p.chapterNeeds.Length) p.chapterNeeds[ch].text = open ? "" : Loc.F("Mở khi {0}", SoPhep.ChapterNeed(cfg, ch));
                var nodes = c.nodes.Where(n => n.ch == ch).ToList();
                for (int j = 0; j < PerChapter; j++)
                {
                    int ti = ch * PerChapter + j;
                    if (ti >= p.tiles.Length || !p.tiles[ti]) continue;
                    var tile = p.tiles[ti];
                    tile.gameObject.SetActive(j < nodes.Count);
                    if (j >= nodes.Count) continue;
                    var n = nodes[j];
                    string id = n.id;
                    tile.Bind(n, IconOf(n), SoPhep.Lv(s, id), SoPhep.Face(s, id), open, SoPhep.Block(s, cfg, id) == "",
                        SoPhep.CostOf(s, cfg, n), id == sel, () => Select(id));
                    // đường của ô thường j: băng → ô, ô → ô chốt; sáng màu chương khi ô đã vẽ
                    if (j < PerChapter - 1)
                    {
                        var lc = SoPhep.Lv(s, id) > 0 ? chc : open ? SoPhepColors.LineOpen : SoPhepColors.LineLock;
                        SetLine(ch * LinesPerChapter + j, lc);
                        SetLine(ch * LinesPerChapter + PerChapter - 1 + j, lc);
                    }
                }
                // thân cây sang chương sau: sáng khi chương sau đã mở
                bool nextOpen = ch + 1 < c.chapters.Count && SoPhep.ChapterOpen(s, cfg, ch + 1);
                SetLine(ch * LinesPerChapter + LinesPerChapter - 1, nextOpen ? chc : open ? SoPhepColors.LineOpen : SoPhepColors.LineLock);
            }
            RefreshSel();
        }

        void SetLine(int i, Color c)
        {
            if (p.lines != null && i < p.lines.Length && p.lines[i]) p.lines[i].color = c;
        }

        // cuộn trang cho ô (giữa vùng nhìn), không vượt mép trang
        void ScrollTo(SoPhepTile tile)
        {
            if (!tile || !p.scroll || !p.scroll.content || !p.scroll.viewport) return;
            Canvas.ForceUpdateCanvases();
            var content = p.scroll.content;
            float ch = content.rect.height, vh = p.scroll.viewport.rect.height;
            if (ch <= vh) return;
            float y = -content.InverseTransformPoint(tile.Rect.position).y; // khoảng từ mép trên trang (pivot trên) tới tâm ô
            p.scroll.verticalNormalizedPosition = 1 - Mathf.Clamp01((y - vh * 0.45f) / (ch - vh));
        }

        void RefreshSel()
        {
            var s = S;
            var cfg = Cfg;
            var n = cfg.sophep.Node(sel);
            if (n == null) return;
            int lv = SoPhep.Lv(s, n.id), face = SoPhep.Face(s, n.id);
            bool maxed = lv >= n.MaxLv;
            p.selName.text = n.FaceCount > 1 ? $"{n.Name}" : n.Name;
            if (n.MaxLv > 1 && lv > 0 && !maxed)
                p.selDesc.text = Loc.F("Đang có: {0}\nVẽ tiếp: {1}", SoPhep.Describe(n, face, lv), SoPhep.Describe(n, face, lv + 1));
            else p.selDesc.text = SoPhep.Describe(n, face, Math.Max(1, lv));
            for (int i = 0; i < p.faces.Length; i++)
            {
                bool on = n.FaceCount > 1 && i < n.FaceCount;
                p.faces[i].gameObject.SetActive(on);
                if (!on) continue;
                p.faces[i].SetText(n.FaceName(i));
                p.faces[i].SetRole(i == face ? BtnColor.Orange : BtnColor.Paper);
            }
            string why = SoPhep.Block(s, cfg, n.id);
            int cost = SoPhep.CostOf(s, cfg, n);
            p.selCost.text = maxed ? Loc.T("Đã vẽ đủ") : why == "" ?
                (n.stones > 0 && lv == 0 ? Loc.F("Giá: {0} nét và {1} đá tiến hóa", cost, n.stones) : Loc.F("Giá: {0} nét", cost)) : why;
            p.selCost.color = maxed ? SoPhepColors.Chapter(n.ch) : why == "" ? SoPhepColors.Gold : SoPhepColors.Coral;
            if (p.panelRim) p.panelRim.color = SoPhepColors.Chapter(n.ch);
            p.draw.gameObject.SetActive(!maxed);
            p.draw.SetRole(why == "" ? BtnColor.Green : BtnColor.Paper);
            p.suggest.gameObject.SetActive(SoPhep.Open(s, cfg));
            p.reset.gameObject.SetActive(SoPhep.Spent(s, cfg) > 0);
        }

        void Select(string id)
        {
            sel = id;
            App.Audio.Play("click");
            Refresh();
        }

        void Draw()
        {
            string why = SoPhep.Block(S, Cfg, sel);
            if (why != "")
            {
                App.Audio.Play("error");
                App.Toasts.Show(why, App.Art.Icon("info"));
                return;
            }
            SoPhep.Buy(S, Cfg, sel);
            Guide.Skip(TutorDraw); // bước khoanh nút Vẽ: đánh dấu trong hàm bấm (nút có thể ẩn ngay khi vẽ đủ)
            App.Audio.Play("stamp");
            Haptics.Play(Haptic.Stamp);
            App.Save.Save();
            Refresh();
            var tile = TileOf(sel);
            if (tile) StartCoroutine(Pop(tile.Rect));
        }

        void Suggest()
        {
            int n = SoPhep.AutoBuy(S, Cfg);
            if (n == 0)
            {
                App.Audio.Play("error");
                App.Toasts.Show(Loc.T("Chưa vẽ thêm được ô nào theo gợi ý"), App.Art.Icon("info"));
                return;
            }
            App.Audio.Play("stamp");
            App.Toasts.Show(Loc.F("Đã vẽ {0} ô theo gợi ý", n), App.Art.Icon("pencil"));
            App.Save.Save();
            Refresh();
        }

        void AskReset() =>
            App.Modals.Confirm(Loc.T("Tẩy sổ?"), Loc.T("Hoàn lại hết nét và đá tiến hóa đã vẽ. Mặt đã chọn giữ nguyên."), Loc.T("Tẩy sổ"), () =>
            {
                SoPhep.Reset(S);
                App.Save.Save();
                Refresh();
            });

        void SetFace(int f)
        {
            var n = Cfg.sophep.Node(sel);
            if (n == null || n.FaceCount <= 1) return;
            SoPhep.SetFace(S, Cfg, sel, f);
            App.Audio.Play("click");
            App.Save.Save();
            Refresh();
        }

        Sprite IconOf(SoPhepNode n)
        {
            int i = Cfg.sophep.nodes.IndexOf(n);
            return p.icons != null && i >= 0 && i < p.icons.Length && p.icons[i] ? p.icons[i] : App.Art.Icon(string.IsNullOrEmpty(n.icon) ? "pencil" : n.icon);
        }

        SoPhepTile TileOf(string id)
        {
            var c = Cfg.sophep;
            var n = c.Node(id);
            if (n == null) return null;
            int j = c.nodes.Where(x => x.ch == n.ch).ToList().IndexOf(n);
            int ti = n.ch * PerChapter + j;
            return ti >= 0 && ti < p.tiles.Length ? p.tiles[ti] : null;
        }

        static IEnumerator Pop(RectTransform rt)
        {
            float[] at = { 0, 0.08f, 0.17f, 0.25f };
            float[] sc = { 1, 1.15f, 0.94f, 1 };
            for (float t = 0; t < 0.25f; t += Time.unscaledDeltaTime)
            {
                int i = 0;
                while (i < at.Length - 2 && t > at[i + 1]) i++;
                rt.localScale = Vector3.one * Mathf.Lerp(sc[i], sc[i + 1], Mathf.InverseLerp(at[i], at[i + 1], t));
                yield return null;
            }
            rt.localScale = Vector3.one;
        }
    }
}
