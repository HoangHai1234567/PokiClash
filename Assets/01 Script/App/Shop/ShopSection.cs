// Mục của màn cửa hàng (prefab Items/MucCuaHang): băng tím caro thoi viền mực, tên mục vàng viền mực ở giữa, đồng hồ bên phải (mục hẹn
// giờ). Bản 3 (2026-11-27, học băng tiêu đề mục cửa hàng Clash of Critters). ShopPage, GD_Claude/26 mục 15.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ShopSection : MonoBehaviour
    {
        [SerializeField] TextMeshProUGUI title, timer;
        [SerializeField] GameObject timerBox; // nền viên thuốc của đồng hồ (chữ là con)
        double until;
        float next;

        public void Setup(TextMeshProUGUI titleText, TextMeshProUGUI timerText, GameObject timerBg)
        {
            title = titleText;
            timer = timerText;
            timerBox = timerBg;
        }

        public ShopSection Set(string text, double untilMs = 0)
        {
            title.text = text;
            until = untilMs;
            (timerBox ? timerBox : timer.gameObject).SetActive(untilMs > 0);
            Tick();
            return this;
        }

        void Tick()
        {
            if (until <= 0) return;
            timer.text = ShopUi.Clock(until - SaveService.Now());
        }

        void Update()
        {
            if (until <= 0 || Time.unscaledTime < next) return;
            next = Time.unscaledTime + 0.5f;
            Tick();
        }
    }
}
