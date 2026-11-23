// Lưới ô của màn cửa hàng (prefab Items/LuoiCuaHang): GridLayoutGroup 2 hoặc 3 cột, cỡ ô đặt lúc chạy theo bề rộng trang. ShopPage.
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
    public sealed class ShopGrid : MonoBehaviour
    {
        [SerializeField] GridLayoutGroup grid;
        public const float Width = 1000;

        public void Setup(GridLayoutGroup g) => grid = g;

        public RectTransform Rect => (RectTransform)transform;

        // cols cột, ô cao h
        public ShopGrid Set(int cols, float h)
        {
            float gap = grid.spacing.x;
            grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            grid.constraintCount = cols;
            grid.cellSize = new Vector2((Width - gap * (cols - 1)) / cols, h);
            return this;
        }
    }
}
