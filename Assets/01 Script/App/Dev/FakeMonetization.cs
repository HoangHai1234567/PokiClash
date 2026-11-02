#if UNITY_EDITOR || DEVELOPMENT_BUILD
// Quảng cáo và cửa hàng giả lập cho bản dev (Editor, Development Build): gắn vào Ads.Current / Store.Current trước khi nạp scene đầu.
// Bản phát hành không có file này (bước kiểm tra trước build chặn nếu lọt): chưa có SDK thì các nút quảng cáo và mục gói ẩn đi.
// Hộp quảng cáo là prefab dùng chung Dialogs/QuangCaoGia (FakeAdDialog), mở chồng lên hộp đang mở (AFK, Cây bi...).
using System;
using System.Collections;
using UnityEngine;

namespace PokiClash
{
    public static class FakeMonetization
    {
        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
        static void Install()
        {
            Ads.Current ??= new FakeRewardAds();
            Store.Current ??= new FakeStore();
        }
    }

    // hộp "Quảng cáo giả lập" đếm 3 giây như bản web, có nút "Bỏ qua"
    public sealed class FakeRewardAds : IRewardAds
    {
        public float Seconds = 3;

        public void Show(string placement, Action<bool> done)
        {
            bool ok = false, cancelled = false;
            var dlg = App.Modals.Open<FakeAdDialog>(() => done?.Invoke(ok), mandatory: true);
            var m = dlg.Modal;
            dlg.Show(Mathf.RoundToInt(Seconds), () =>
            {
                cancelled = true;
                m.Close();
            });
            App.I.StartCoroutine(Count());

            IEnumerator Count()
            {
                for (float t = Seconds; t > 0 && !cancelled && m.IsOpen; t -= Time.unscaledDeltaTime)
                {
                    dlg.SetCount(Mathf.CeilToInt(t));
                    yield return null;
                }
                if (cancelled || !m.IsOpen) yield break;
                ok = true;
                m.Close();
            }
        }
    }

    // cửa hàng giả lập: mua thành công ngay, không trừ tiền
    public sealed class FakeStore : IStore
    {
        public void Buy(string product, Action<bool> done) => done?.Invoke(true);
    }
}
#endif
