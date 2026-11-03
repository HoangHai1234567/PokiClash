// Bảng chặng của đảo 70 ải (prefab Assets/04 Prefabs/Dialogs/BangChang, biến thể tờ giấy gốc HopThoai, dựng bằng menu
// "PokiClash/Prefab/Đảo 70 ải (ChamAi, DongChang, BangChang)"): chặng là các ải từ một ải tướng tới trước ải tướng sau.
// Tên chặng, dòng "Ải a–b · ra mắt <tướng>", danh sách ải cuộn dọc (Items/DongChang), nút Đóng. Chạm ải đã mở thì đóng bảng và mở
// hộp Chuẩn bị trận; ải chưa mở thì báo. Mở từ màn Đảo (ZoneScene) khi chạm mốc hoặc chấm ải.
using System;
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ZoneChapterDialog : Dialog
    {
        [SerializeField] TextMeshProUGUI title, sub;
        [SerializeField] ScrollRect scroll;
        [SerializeField] RectTransform list;
        [SerializeField] SketchButton close;
        [SerializeField] ZoneChapterRow rowPrefab;

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Dùng khi dựng prefab (Editor).
        public void Setup(TextMeshProUGUI titleText, TextMeshProUGUI subText, ScrollRect scrollRect, RectTransform listRt, SketchButton closeBtn,
            ZoneChapterRow row)
        {
            title = titleText;
            sub = subText;
            scroll = scrollRect;
            list = listRt;
            close = closeBtn;
            rowPrefab = row;
        }

        // stages: các ải của chặng theo thứ tự; openStage(id): mở hộp Chuẩn bị trận
        public void Show(List<StageDef> stages, GameData d, SaveData s, Action<int> openStage)
        {
            var head = stages[0];
            title.text = head.name;
            sub.text = $"Ải {head.idx}–{stages[stages.Count - 1].idx} · ra mắt {d.Hero(head.enemies[0].hero).name}";
            for (int i = list.childCount - 1; i >= 0; i--) Destroy(list.GetChild(i).gameObject);
            int now = -1;
            for (int i = 0; i < stages.Count; i++)
            {
                var st = stages[i];
                bool cleared = Progress.StageCleared(s, st), open = Progress.StageOpen(s, st), current = open && !cleared;
                if (current) now = i;
                Ui.Spawn(rowPrefab, list).Bind(st, d, open, cleared, current, Progress.StageBalls(d, st, !cleared), () =>
                {
                    if (!Progress.StageOpen(App.Save.Data, st))
                    {
                        App.Audio.Play("error");
                        App.Toasts.Show($"Qua ải {st.idx - 1} trước đã", Icon("lock"));
                        return;
                    }
                    App.Audio.Play("click");
                    Close();
                    openStage(st.id);
                });
            }
            close.SetOnClick(Close);
            StartCoroutine(ScrollTo(now));
        }

        // cuộn tới ải đang đánh (để nó ở khoảng giữa khung)
        IEnumerator ScrollTo(int i)
        {
            yield return null;
            Canvas.ForceUpdateCanvases();
            var view = (RectTransform)scroll.viewport;
            float total = list.rect.height, viewH = view.rect.height;
            if (i < 3 || total <= viewH) yield break;
            float y = i * (ZoneChapterRow.Height + 10) - viewH * 0.35f;
            scroll.verticalNormalizedPosition = 1 - Mathf.Clamp01(y / (total - viewH));
        }
    }
}
