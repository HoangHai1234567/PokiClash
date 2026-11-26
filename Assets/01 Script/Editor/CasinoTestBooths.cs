// Casino.TestAllBooths (mở hết lều may rủi; App.cs bật lúc mở game khi chưa phát hành, người dùng 2026-11-26): dự án tắt Reload Domain khi vào
// Play nên biến tĩnh còn true sau khi ra Play. Về Edit mode thì tắt, để EditMode test (CasinoTests) chạy theo lịch thật.
using PokiClash.Core;
using UnityEditor;

namespace PokiClash.EditorTools
{
    [InitializeOnLoad]
    public static class CasinoTestBooths
    {
        static CasinoTestBooths()
        {
            if (!EditorApplication.isPlayingOrWillChangePlaymode) Casino.TestAllBooths = false;
            EditorApplication.playModeStateChanged += st =>
            {
                if (st == PlayModeStateChange.EnteredEditMode) Casino.TestAllBooths = false;
            };
        }
    }
}
