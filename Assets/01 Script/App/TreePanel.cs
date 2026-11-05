// Hộp Cây bi (công trình "Cây bi" trên sảnh): 5 cây, cây đã mở ghi bi đang có / sức chứa kèm thanh đầy, cây chưa mở ghi điều kiện;
// "Hái" lấy bi mọi cây (giữ phần lẻ), "Hái ×2" qua quảng cáo tree_double (3 lần mỗi ngày). Số liệu tự làm mới mỗi nửa giây.
// Prefab Assets/04 Prefabs/Dialogs/CayBi (hộp dùng chung, mở bằng TreePanel.Open); ô cây là Items/OCay.
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class TreePanel : Dialog
    {
        [SerializeField] TextMeshProUGUI info;
        [SerializeField] RectTransform row;
        [SerializeField] TreeCell cellPrefab;
        [SerializeField] SketchButton harvestBtn, doubleBtn;

        TreeCell[] trees;
        float timer;
        bool busy;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI infoText, RectTransform treeRow, TreeCell cell, SketchButton harvest, SketchButton dbl)
        {
            info = infoText;
            row = treeRow;
            cellPrefab = cell;
            harvestBtn = harvest;
            doubleBtn = dbl;
        }

        public static void Open() => App.Modals.Open<TreePanel>().Show();

        static string Dec(double v) => v.ToString("0.#", System.Globalization.CultureInfo.InvariantCulture).Replace('.', ',');

        void Show()
        {
            for (int i = row.childCount - 1; i >= 0; i--) Destroy(row.GetChild(i).gameObject);
            var c = D.Cfg.trees;
            int n = c.unlockLevels.Count + 1;
            trees = new TreeCell[n];
            for (int i = 0; i < n; i++)
            {
                var cell = Ui.Spawn(cellPrefab, row);
                cell.name = "cay_" + i;
                cell.Rect.anchoredPosition = new Vector2((i - (n - 1) / 2f) * 158, 0);
                trees[i] = cell;
            }
            harvestBtn.SetOnClick(() => Harvest(1));
            doubleBtn.SetOnClick(Double);
            Refresh();
        }

        void Refresh()
        {
            if (trees == null || Modal == null || !Modal.IsOpen) return;
            var s = S;
            var cfg = D.Cfg;
            double now = Now;
            int stock = Trees.Stock(s, cfg, now);
            double cap = Trees.Cap(s, cfg, now);
            bool pass = AdGate.PassActive(s, now);
            info.text = $"Mỗi cây {Dec(Trees.Rate(s, cfg, now))} bi mỗi giờ, chứa tối đa {cap:0} bi; đầy thì ngừng." + (pass ? " Đang có Thẻ Phiêu Lưu (×1,5)." : "");
            var st = Trees.Of(s, now).stock;
            for (int i = 0; i < trees.Length; i++)
            {
                if (i < st.Count) trees[i].SetOpen(st[i], cap);
                else trees[i].SetLocked(i == 0 ? "Qua ải 1" : $"Đạt\ncấp {cfg.trees.unlockLevels[i - 1]}");
            }
            harvestBtn.SetText(stock > 0 ? $"Hái +{stock}" : "Hái");
            harvestBtn.Interactable = stock > 0;
            doubleBtn.gameObject.SetActive(Ads.Ready);
            Ads.Bind(doubleBtn, "Hái ×2", Ads.TreeDouble, stock > 0);
        }

        void Update()
        {
            if (busy) return;
            if ((timer += Time.unscaledDeltaTime) < 0.5f) return;
            timer = 0;
            Refresh();
        }

        void Harvest(int mult)
        {
            int n = Trees.Harvest(S, D.Cfg, Now, mult);
            if (n <= 0) return;
            App.Save.Save();
            App.Audio.Play("coin");
            App.Toasts.Show($"Hái {n} bi" + (mult > 1 ? " (×2)" : ""), App.Art.Icon("ball"));
            App.Bars.Refresh();
            if (App.Router.CurrentRoot) App.Router.CurrentRoot.Refresh();
            Refresh();
        }

        void Double()
        {
            busy = true;
            Ads.Show(Ads.TreeDouble, ok =>
            {
                busy = false;
                if (ok) Harvest(2);
                else Refresh();
            });
        }
    }
}
