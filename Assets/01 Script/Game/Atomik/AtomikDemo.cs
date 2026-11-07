// Scene thử rig .atomik (menu PokiClash/Thử/Atomik): nút đổi clip cho từng con, chỉnh tốc độ, tên clip dưới chân.
// Chỉ dùng trong scene thử, không vào bản build.
using UnityEngine;

namespace PokiClash.Game
{
    public sealed class AtomikDemo : MonoBehaviour
    {
        public AtomikPlayer[] players;
        public Camera cam;
        float speed = 1f;
        GUIStyle label, button;

        void OnGUI()
        {
            if (players == null || players.Length == 0) return;
            float k = Mathf.Min(Screen.width, Screen.height) / 720f;
            label ??= new GUIStyle(GUI.skin.label) { alignment = TextAnchor.UpperCenter, fontStyle = FontStyle.Bold };
            button ??= new GUIStyle(GUI.skin.button);
            label.fontSize = Mathf.RoundToInt(18 * k);
            label.normal.textColor = new Color(0.17f, 0.13f, 0.09f);
            button.fontSize = Mathf.RoundToInt(16 * k);
            for (int i = 0; i < players.Length; i++)
            {
                var p = players[i];
                if (p == null || p.asset == null) continue;
                var sp = cam ? cam.WorldToScreenPoint(p.transform.position) : Vector3.zero;
                float x = sp.x, y = Screen.height - sp.y + 10 * k, w = 230 * k, h = 32 * k;
                GUI.Label(new Rect(x - w / 2, y, w, h), p.clip + (p.loop ? "" : " (một lần)"), label);
                var clips = p.asset.anims;
                float bw = Mathf.Min(110 * k, w / clips.Length);
                for (int j = 0; j < clips.Length; j++)
                    if (GUI.Button(new Rect(x - bw * clips.Length / 2 + j * bw, y + h, bw - 4 * k, h), clips[j].name, button))
                        p.Play(clips[j].name, clips[j].name == "idle");
            }
            GUI.Label(new Rect(12 * k, 10 * k, 300 * k, h0(k)), $"Tốc độ x{speed:0.00}", label);
            float ns = GUI.HorizontalSlider(new Rect(12 * k, 40 * k, 260 * k, 24 * k), speed, 0.1f, 2f);
            if (!Mathf.Approximately(ns, speed))
            {
                speed = ns;
                foreach (var p in players) if (p) p.speed = speed;
            }
        }

        static float h0(float k) => 30 * k;

        void LateUpdate()
        {
            // xếp theo khung: màn dọc (điện thoại) xếp cột, màn ngang xếp hàng; camera ôm vừa cả ba con
            if (!cam || players == null || players.Length == 0) return;
            bool portrait = cam.aspect < 1f;
            const float gapX = 3.6f, gapY = 5.1f, h = 3.6f;
            int n = players.Length;
            for (int i = 0; i < n; i++)
                if (players[i])
                    players[i].transform.localPosition = portrait
                        ? new Vector3(0, (n - 1 - i) * gapY, 0)
                        : new Vector3((i - (n - 1) * 0.5f) * gapX, 0, 0);
            float spanY = portrait ? (n - 1) * gapY + h : h, spanX = portrait ? gapX : n * gapX;
            float size = Mathf.Max(spanY * 0.5f + 0.9f, (spanX * 0.5f + 0.3f) / cam.aspect);
            cam.orthographicSize = size;
            var p = cam.transform.localPosition;
            cam.transform.localPosition = new Vector3(0, spanY * 0.5f - 0.35f, p.z);
        }

        void Update()
        {
            // clip chạy một lần xong thì về idle
            foreach (var p in players)
                if (p && p.Done) p.Play("idle", true);
        }
    }
}
