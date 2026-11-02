// Cấu hình cân bằng (CFG và hằng số tiến trình của bản web), dựng từ balance.json.
using PokiClash.Core;
using UnityEngine;

namespace PokiClash.Game
{
    [CreateAssetMenu(menuName = "PokiClash/BalanceConfig", fileName = "BalanceConfig")]
    public sealed class BalanceConfigAsset : ScriptableObject
    {
        public BalanceConfig cfg = new BalanceConfig();
    }
}
