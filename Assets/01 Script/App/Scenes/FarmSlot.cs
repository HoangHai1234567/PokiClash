// Một chỗ làm trên cảnh Trang trại (prefab Items/ChoLamTrangTrai, gốc ở điểm chân tướng đứng, đặt sẵn trong Screens/Farm theo ảnh nền).
// Vòng nét đứt dưới đất; chỗ chưa mở: ổ khoá và "Cấp N"; chỗ trống: dấu "+" nhún (chạm mở danh sách chọn tướng, hoặc kéo thú thả vào);
// có tướng: bong bóng bi tích trên đầu (chạm để thu hoạch) và vòng sức còn cạnh đầu. Thú (FarmPet) do FarmScene đặt lên trên.
// Khi đang kéo thú: chỗ nhận được sáng lên, chỗ gần nhất phồng to.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class FarmSlot : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Image ground, plus, ring, lockIcon;
            public TextMeshProUGUI ringText, lockText, stock;
            public GameObject bubble, ringRoot;
            public ClickCatcher click, bubbleClick;
        }

        [SerializeField] Parts p;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        bool open, empty, glow, near;
        float t;

        public RectTransform Rt => (RectTransform)transform;

        public void Bind(GameData d, SaveData s, int i, bool isOpen, FarmSpot sp, Action onClick, Action onHarvest)
        {
            open = isOpen;
            empty = sp.hero == null;
            name = "cho_" + i;
            p.click.OnClick = open ? onClick : null;
            p.bubbleClick.OnClick = onHarvest;
            p.lockIcon.gameObject.SetActive(!open);
            p.lockText.gameObject.SetActive(!open);
            p.lockText.text = open ? "" : $"Cấp {Farm.SpotLevel(d.Cfg, i)}";
            p.plus.gameObject.SetActive(open && empty);
            p.ground.color = open ? new Color(1, 1, 1, empty ? 0.85f : 0.45f) : new Color(0.3f, 0.24f, 0.18f, 0.35f);

            p.bubble.SetActive(open && sp.stock >= 1);
            if (sp.stock >= 1) p.stock.text = ((int)Math.Floor(sp.stock)).ToString();

            bool hero = open && !empty;
            p.ringRoot.SetActive(hero);
            if (hero)
            {
                bool working = sp.energy > 0;
                double hours = Farm.Hours(s, d, sp.hero);
                p.ring.color = working ? Theme.Green : Theme.Paper3;
                p.ring.fillAmount = working ? Mathf.Clamp01((float)(sp.energy / hours)) : 1;
                p.ringText.text = working ? FarmScene.Clock(sp.energy) : "hết";
                p.ringText.color = working ? Theme.Ink : Theme.RedD;
            }
        }

        // đang kéo thú: canAccept = chỗ này nhận được; isNear = chỗ gần nhất dưới tay
        public void Highlight(bool canAccept, bool isNear)
        {
            glow = canAccept;
            near = canAccept && isNear;
        }

        void Update()
        {
            t += Time.unscaledDeltaTime;
            float pulse = glow ? 1 + 0.08f * Mathf.Sin(t * 8) : 1;
            float k = near ? 1.3f : 1;
            p.ground.rectTransform.localScale = Vector3.one * pulse * k;
            if (glow) p.ground.color = near ? new Color(1f, 0.9f, 0.4f, 1) : new Color(1, 1, 1, 0.95f);
            else if (open) p.ground.color = new Color(1, 1, 1, empty ? 0.85f : 0.45f);
            if (p.plus.gameObject.activeSelf) p.plus.rectTransform.anchoredPosition = new Vector2(0, 54 + Mathf.Sin(t * 3) * 8);
            if (p.bubble.activeSelf) p.bubble.transform.localScale = Vector3.one * (1 + 0.05f * Mathf.Sin(t * 4));
        }
    }
}
