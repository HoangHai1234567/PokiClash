// Bến tàu, chuyến tàu qua mây, màn tải (người dùng 2026-11-19). Menu "PokiClash/Prefab/Sảnh và đảo/Bến tàu: tàu sảnh, chuyến tàu qua mây, màn tải"
// (chạy lại thì dựng lại):
// 1. Assets/04 Prefabs/Screens/ChuyenTau.prefab: ShipVoyage trên canvas riêng (thứ tự 9 khi đi tàu, 15 lúc màn tải; ShipVoyage đặt):
//    lớp chặn chạm, biển lát (tau_bien), 18 nét sóng, ảnh chụp màn cũ / mới (RawImage), tàu + vệt chữ V + 18 cụm bọt, 96 đám mây
//    (land_thuy_may_2), nhóm màn tải (logo, giấy ghi có thanh tải, mẹo; ảnh màn sa bàn cũ ở Assets/03 Art/Boot). Gán App.voyagePrefab.
// 2. Screens/Hub: tàu ở bến cạnh đảo Thủy (con của ảnh bản đồ "dao", trên lớp mây che để luôn thấy tàu), chỗ đậu và đường ra khơi
//    bắc (sang Nhà, qua kênh phía đông) / nam (màn tải: tàu từ mây phía nam vào bến); HubPan kéo dư trên / dưới để bến ra khỏi
//    hàng nút đáy; giao diện cố định (hang_nut, cot_cong_trinh) có CanvasGroup để chuyến tàu ẩn khi chụp màn (HubScene.Chrome). Toạ độ đo trên ảnh 1024 x 1536 (ArtGen/Islands/sanh_moi/concept_I_ben_tau.png, bến ghép bằng ben_tau/ghep_ben.py).
// Hàm Pier(...) dùng chung: màn Nhà gọi trong menu dựng màn của nó (toạ độ local của lớp kéo `world`).
// Ảnh tàu Assets/03 Art/Ship (ArtGen/Islands/sanh_moi/ben_tau/cat_tau.py).
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class ShipBuild
    {
        public const string ArtDir = "Assets/03 Art/Ship/";
        const string VoyagePath = "Assets/04 Prefabs/Screens/ChuyenTau.prefab";
        const string AppPath = "Assets/04 Prefabs/App/App.prefab";
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const string MapJson = "Assets/03 Art/Islands/hub_map.json";
        const string CloudPath = "Assets/03 Art/Islands/land_thuy_may_2.png";
        const string BootDir = "Assets/03 Art/Boot/";

        // bến sảnh, toạ độ ảnh 1024 x 1536: chỗ đậu (mớn nước, mặt nam cầu tàu), mũi quay ra khơi (sang phải)
        // (mớn nước thấp hơn chân cọc cầu để thân tàu đè lên mép trước cầu, không như ngồi trên sàn cầu)
        static readonly Vector2 HubDock = new Vector2(790, 1460);
        // bến trên (người dùng: "thêm 1 bến đỗ nữa ở phần trên của các đảo"): cầu gỗ ở khe giữa đảo Hỏa và Kim chĩa lên bắc
        // (bo_dao/ben_tren.txt); tàu đậu bên phải đầu cầu, mũi quay về phía người xem; chuyến về Nhà / từ Nhà về đi từ đây thẳng lên
        static readonly Vector2 HubDock2 = new Vector2(632, 62);
        static readonly Vector2[] HubNorth2 = { new Vector2(640, -30), new Vector2(645, -130) };
        // chuyển bến sau màn tải: từ bến dưới vòng biển phía đông, ngoài rìa đảo Thổ, Kim (x > 1005 là biển), lên bến trên
        static readonly Vector2[] HubTransfer = { new Vector2(880, 1478), new Vector2(985, 1470), new Vector2(1065, 1405), new Vector2(1100, 1290),
            new Vector2(1112, 1000), new Vector2(1105, 700), new Vector2(1085, 420), new Vector2(1050, 230), new Vector2(985, 110),
            new Vector2(880, 40), new Vector2(760, 20), new Vector2(690, 32) };
        // từ chỗ đậu ra phía nam: lùi theo mặt nam cầu tàu, ra mép mây dưới (màn tải: tàu từ đây vào bến)
        static readonly Vector2[] HubSouth = { new Vector2(735, 1476), new Vector2(690, 1486), new Vector2(648, 1492) };

        [MenuItem("PokiClash/Prefab/Sảnh và đảo/Bến tàu: tàu sảnh, chuyến tàu qua mây, màn tải", priority = 64)]
        static void Build()
        {
            var assets = AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiAssets")[0]));
            Theme.Init(assets);
            AssetDatabase.ImportAsset(ArtDir.TrimEnd('/'), ImportAssetOptions.ImportRecursive | ImportAssetOptions.ForceUpdate);
            if (!Spr("tau_ngang"))
            {
                Debug.LogError("[Bến tàu] Thiếu ảnh tàu ở " + ArtDir + ": chạy ArtGen/Islands/sanh_moi/ben_tau/cat_tau.py");
                return;
            }
            BuildVoyage(assets.prefabs);
            BuildHub();
            AssetDatabase.SaveAssets();
        }

        // ---------- chuyến tàu qua mây + màn tải ----------

        static void BuildVoyage(UiKit kit)
        {
            var root = new GameObject("ChuyenTau");
            try
            {
                var view = Ui.Spawn(kit.canvas, root.transform);
                view.name = "Canvas";
                view.Canvas.sortingOrder = 15;
                var area = view.Bg;

                var block = Img(area, "chan_cham", null, new Color(1, 1, 1, 0), true);
                block.rectTransform.Stretch();

                var seaRt = Node(area, "bien");
                seaRt.Stretch();
                var tile = Img(seaRt, "mat_bien", Spr("tau_bien"), Color.white);
                tile.type = Image.Type.Tiled;
                tile.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(PokiCanvas.RefW + 1024, PokiCanvas.RefH + 1024));
                var waveSprites = Enumerable.Range(1, 4).Select(i => Spr("tau_song_" + i)).Where(s => s).ToArray();
                var waves = new List<Image>();
                for (int i = 0; i < 18; i++)
                {
                    var w = Img(seaRt, "song", waveSprites[i % waveSprites.Length], Color.white);
                    w.SetNativeSize();
                    w.rectTransform.anchorMin = w.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
                    waves.Add(w);
                }

                // theo giờ: lớp nhuộm và tia nắng dùng chung material với sảnh, đảo (menu Sáng tối), phủ biển, dưới ảnh chụp màn
                var tintImg = Img(area, "nhuom", null, Color.white);
                tintImg.material = AssetDatabase.LoadAssetAtPath<Material>("Assets/03 Art/Islands/day_multiply.mat");
                tintImg.rectTransform.Stretch();
                tintImg.enabled = false;
                var raysGo = new GameObject("nang", typeof(RectTransform), typeof(CanvasRenderer), typeof(RawImage));
                raysGo.layer = LayerMask.NameToLayer("UI");
                raysGo.transform.SetParent(area, false);
                var raysImg = raysGo.GetComponent<RawImage>();
                raysImg.material = AssetDatabase.LoadAssetAtPath<Material>("Assets/03 Art/Islands/day_rays.mat");
                raysImg.raycastTarget = false;
                raysImg.rectTransform.Stretch();
                raysImg.enabled = false;
                if (!tintImg.material || !raysImg.material) Debug.LogWarning("[Bến tàu] Thiếu day_multiply.mat / day_rays.mat: chạy menu Sáng tối trước");

                RawImage Shot(string n)
                {
                    var go = new GameObject(n, typeof(RectTransform), typeof(CanvasRenderer), typeof(RawImage));
                    go.layer = LayerMask.NameToLayer("UI");
                    go.transform.SetParent(area, false);
                    var ri = go.GetComponent<RawImage>();
                    ri.raycastTarget = false;
                    ri.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(PokiCanvas.RefW, PokiCanvas.RefH));
                    go.SetActive(false);
                    return ri;
                }
                var oldShot = Shot("man_cu");
                var newShot = Shot("man_moi");

                var look = Look(area, "tau", 1, 24, false);

                var cloudRt = Node(area, "may");
                cloudRt.Stretch();
                var cloud = AssetDatabase.LoadAssetAtPath<Sprite>(CloudPath);
                var clouds = new List<Image>();
                for (int i = 0; i < 96; i++)
                {
                    var c = Img(cloudRt, "may", cloud, Color.white);
                    c.rectTransform.anchorMin = c.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
                    c.rectTransform.sizeDelta = new Vector2(400, 200);
                    clouds.Add(c);
                }

                // mây vành của màn (CloudRing) mang sang dải: ảnh, cỡ gán lúc chạy
                var carryRt = Node(area, "may_mang");
                carryRt.Stretch();
                var carry = new List<Image>();
                for (int i = 0; i < 140; i++)
                {
                    var c = Img(carryRt, "may", cloud, Color.white);
                    c.rectTransform.anchorMin = c.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
                    c.gameObject.SetActive(false);
                    carry.Add(c);
                }

                // màn tải: logo trên, giấy ghi chú dưới có thanh tải và mẹo (ảnh, cỡ như màn sa bàn cũ)
                var bootRt = Node(view.Frame, "man_tai", typeof(CanvasGroup));
                bootRt.Stretch();
                var bootCg = bootRt.GetComponent<CanvasGroup>();
                bootCg.blocksRaycasts = false;
                var logo = Img(bootRt, "logo", BootSpr("boot_logo"), Color.white).rectTransform;
                logo.Place(new Vector2(0.5f, 1), new Vector2(0, -SceneRoot.BarHeight - 40), new Vector2(698, 423), new Vector2(0.5f, 1));
                logo.localEulerAngles = new Vector3(0, 0, 2);
                var note = Img(bootRt, "giay_ghi", BootSpr("boot_giay_ghi"), Color.white).rectTransform;
                note.Place(new Vector2(0.5f, 0), new Vector2(0, 150), new Vector2(812, 248));
                note.localEulerAngles = new Vector3(0, 0, 1);
                var bar = Img(note, "khung", BootSpr("boot_thanh_tai"), Color.white).rectTransform;
                bar.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 37), new Vector2(608, 56));
                var fill = Img(bar, "loi", BootSpr("boot_thanh_tai_loi"), Color.white);
                fill.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(588, 36));
                fill.type = Image.Type.Filled;
                fill.fillMethod = Image.FillMethod.Horizontal;
                fill.fillOrigin = (int)Image.OriginHorizontal.Left;
                var art = AssetDatabase.LoadAssetAtPath<ArtLibrary>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:ArtLibrary")[0]));
                var pen = Img(bar, "but", art ? art.Icon("pencil") : null, Color.white).rectTransform;
                pen.Place(new Vector2(0.5f, 0.5f), new Vector2(-276, 50), new Vector2(68, 68));
                pen.localEulerAngles = new Vector3(0, 0, -8);
                var pct = Text(note, "phan_tram", Theme.Bold, 30, Theme.Ink2, "0%");
                pct.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -10), new Vector2(200, 40));
                var tip = Text(note, "meo", Theme.Body, 27, Theme.Ink2, "Mẹo");
                tip.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -68), new Vector2(720, 76));
                tip.textWrappingMode = TextWrappingModes.Normal;
                tip.lineSpacing = -12;

                var voyage = root.AddComponent<ShipVoyage>();
                voyage.Setup(view, area, block, tile.rectTransform, waves.ToArray(), tintImg, raysImg, oldShot, newShot, look, clouds.ToArray(), carry.ToArray(), bootCg, logo, fill, pen,
                    pct, tip);
                Folder(Path.GetDirectoryName(VoyagePath).Replace('\\', '/'));
                PrefabUtility.SaveAsPrefabAsset(root, VoyagePath);
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
            var prefab = AssetDatabase.LoadAssetAtPath<ShipVoyage>(VoyagePath);
            var appRoot = PrefabUtility.LoadPrefabContents(AppPath);
            try
            {
                appRoot.GetComponentInChildren<App>(true).voyagePrefab = prefab;
                PrefabUtility.SaveAsPrefabAsset(appRoot, AppPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(appRoot);
            }
            Debug.Log($"[Bến tàu] Đã dựng {VoyagePath} (96 mây, 18 sóng, 18 bọt) và gán App.voyagePrefab.");
        }

        // ---------- bến sảnh ----------

        static void BuildHub()
        {
            var json = AssetDatabase.LoadAssetAtPath<TextAsset>(MapJson);
            var root = J.Obj(MiniJson.Parse(json.text));
            var img = J.Arr(root, "img");
            var view = J.Arr(root, "view");
            float iw = System.Convert.ToSingle(img[0]), ih = System.Convert.ToSingle(img[1]);
            float vw = System.Convert.ToSingle(view[0]), vh = System.Convert.ToSingle(view[1]);
            var offA = J.Arr(root, "offset"); // tranh gốc → ảnh nới thêm biển (build_sanh.py TOP)
            float ox = offA.Count > 1 ? System.Convert.ToSingle(offA[0]) : 0, oy = offA.Count > 1 ? System.Convert.ToSingle(offA[1]) : 0;
            Vector2 L(Vector2 p) => new Vector2(((p.x + ox) / iw - 0.5f) * vw, (0.5f - (p.y + oy) / ih) * vh);
            var contents = PrefabUtility.LoadPrefabContents(HubPath);
            try
            {
                var dao = contents.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == "dao");
                var scene = contents.GetComponentInChildren<HubScene>(true);
                if (!dao || !scene)
                {
                    Debug.LogError("[Bến tàu] Hub chưa có bản đồ thế giới (dao): chạy menu Sảnh bản đồ thế giới trước");
                    return;
                }
                var pier = Pier(dao, L(HubDock), Vector2.right, HubSouth.Select(L).ToArray(), new Vector2[0], 1, 560);
                pier.SetupDock2(L(HubDock2), Vector2.down, HubNorth2.Select(L).ToArray(), HubTransfer.Select(L).ToArray(), 2.4f);
                // ngay dưới mây vành rời (mây toả quanh tàu, tàu đi dưới mây như trong chuyến tàu); mây che đảo chừa chỗ đậu (AVOID)
                var ringT = dao.Find("may_vien_roi");
                if (ringT) pier.transform.SetSiblingIndex(ringT.GetSiblingIndex());
                else pier.transform.SetAsLastSibling();
                var chrome = new List<CanvasGroup>();
                foreach (var n in new[] { "hang_nut", "cot_cong_trinh" })
                {
                    var t = contents.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(r => r.name == n);
                    if (!t)
                    {
                        Debug.LogWarning("[Bến tàu] Không thấy " + n + " trong Hub");
                        continue;
                    }
                    var cg = t.GetComponent<CanvasGroup>();
                    if (!cg) cg = t.gameObject.AddComponent<CanvasGroup>();
                    chrome.Add(cg);
                }
                scene.SetupPier(pier, chrome.ToArray());
                // quầng đèn lồng của tàu vẽ trên lớp đèn đêm của sảnh (trên lớp nhuộm), không bị nhân tối
                var dn = contents.GetComponentInChildren<DayNight>(true);
                var lampLayer = dn ? new SerializedObject(dn).FindProperty("lights").objectReferenceValue as RectTransform : null;
                if (lampLayer)
                {
                    var oldLamp = lampLayer.Find("den_tau");
                    if (oldLamp) Object.DestroyImmediate(oldLamp.gameObject);
                    var lamp = Img(lampLayer, "den_tau", AssetDatabase.LoadAssetAtPath<Sprite>("Assets/03 Art/Islands/Anim/anim_glow.png"), new Color(1, 0.86f, 0.55f, 0));
                    lamp.rectTransform.anchorMin = lamp.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
                    lamp.rectTransform.sizeDelta = new Vector2(78, 78);
                    lamp.enabled = false;
                    pier.Look.SetLanternTop(lamp);
                    EditorUtility.SetDirty(pier.Look);
                }
                var so = new SerializedObject(scene);
                var pan = so.FindProperty("pan").objectReferenceValue as HubPan;
                if (pan) pan.SetPads(0, 0); // ảnh đã nới biển trên / dưới (build_sanh.py TOP, BOT): không cần kéo dư
                EditorUtility.SetDirty(scene);
                PrefabUtility.SaveAsPrefabAsset(contents, HubPath);
                Debug.Log($"[Bến tàu] Sảnh: bến dưới {L(HubDock)} (đường nam {HubSouth.Length} điểm), bến trên {L(HubDock2)} (đường bắc {HubNorth2.Length} điểm, chuyển bến {HubTransfer.Length} điểm); mây vành {(ringT ? "có" : "chưa có")}.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // ---------- dùng chung (màn Nhà gọi) ----------

        /// <summary>
        /// Dựng tàu đậu ở bến làm con của lớp kéo <paramref name="world"/> (thay con cùng tên nếu có). Toạ độ là toạ độ local của world
        /// (gốc ở pivot của world, y lên). dock: chỗ tàu đậu (mớn nước); dockFace: hướng mũi khi đậu; south / north: các điểm từ chỗ
        /// đậu ra khơi, điểm cuối là chỗ lớp mây nhận / giao tàu (để trống hướng nào thì tàu không đi hướng đó). scale: cỡ tàu (1 = cỡ
        /// trên sảnh, tàu nhìn ngang rộng 259); speed: đơn vị local / giây. Màn gán PierShip.Frame, Glide, OnTap lúc Enter.
        /// </summary>
        public static PierShip Pier(RectTransform world, Vector2 dock, Vector2 dockFace, Vector2[] south, Vector2[] north, float scale = 1,
            float speed = 520, string name = "ben_tau")
        {
            var old = world.Find(name);
            if (old) Object.DestroyImmediate(old.gameObject);
            var look = Look(world, name, scale, 16, true);
            var hull = look.Ship.GetComponentsInChildren<Image>(true).First(i => i.name == "hinh");
            var tap = hull.gameObject.AddComponent<ClickCatcher>();
            var pier = look.gameObject.AddComponent<PierShip>();
            pier.Setup(look, dock, dockFace, north ?? new Vector2[0], south ?? new Vector2[0], speed, tap);
            var focus = Node(look.transform, "tam_nhin");
            focus.anchorMin = focus.anchorMax = look.Ship.anchorMin;
            focus.sizeDelta = Vector2.zero;
            focus.anchoredPosition = dock;
            pier.SetFocus(focus);
            look.Ship.anchoredPosition = dock;
            return pier;
        }

        // tàu + bọt: gốc phủ khung cha, cùng gốc toạ độ (pivot) với khung cha; con neo ở pivot nên anchoredPosition = toạ độ local cha
        static ShipLook Look(RectTransform parent, string name, float scale, int foamCount, bool raycast)
        {
            var root = Node(parent, name);
            root.anchorMin = Vector2.zero;
            root.anchorMax = Vector2.one;
            root.pivot = parent.pivot;
            root.offsetMin = root.offsetMax = Vector2.zero;
            var pv = root.pivot;
            var foamSprites = Enumerable.Range(1, 3).Select(i => Spr("tau_bot_" + i)).Where(s => s).ToArray();
            var bot = Node(root, "bot");
            bot.anchorMin = bot.anchorMax = pv;
            bot.sizeDelta = Vector2.zero;
            bot.anchoredPosition = Vector2.zero;
            var foams = new List<Image>();
            for (int i = 0; i < foamCount; i++)
            {
                var f = Img(bot, "bot", foamSprites[i % foamSprites.Length], Color.white);
                f.SetNativeSize();
                f.rectTransform.anchorMin = f.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
                f.gameObject.SetActive(false);
                foams.Add(f);
            }
            var ship = Node(root, "tau");
            ship.anchorMin = ship.anchorMax = pv;
            ship.sizeDelta = Vector2.zero;
            var wake = Img(ship, "vet", Spr("tau_vet"), new Color(1, 1, 1, 0));
            wake.rectTransform.anchorMin = wake.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            wake.rectTransform.pivot = new Vector2(0.5f, 1);
            wake.SetNativeSize();
            var bowFrames = Enumerable.Range(1, 6).Select(i => Spr("tau_mui_" + i)).Where(s => s).ToArray();
            var bow = Img(ship, "song_mui", bowFrames.Length > 0 ? bowFrames[0] : null, new Color(1, 1, 1, 0));
            bow.rectTransform.anchorMin = bow.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            bow.rectTransform.pivot = new Vector2(0.5f, 0.8f);
            bow.SetNativeSize();
            bow.enabled = false;
            var body = Node(ship, "than");
            body.anchorMin = body.anchorMax = new Vector2(0.5f, 0.5f);
            body.sizeDelta = Vector2.zero;
            var side = Spr("tau_ngang");
            var hull = Img(body, "hinh", side, Color.white, raycast);
            hull.rectTransform.anchorMin = hull.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            hull.rectTransform.pivot = new Vector2(0.5f, 0.25f);
            hull.SetNativeSize();
            hull.rectTransform.anchoredPosition = Vector2.zero;
            var lantern = Img(body, "den_long", AssetDatabase.LoadAssetAtPath<Sprite>("Assets/03 Art/Islands/Anim/anim_glow.png"), new Color(1, 0.86f, 0.55f, 0));
            lantern.rectTransform.anchorMin = lantern.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            lantern.rectTransform.sizeDelta = new Vector2(78, 78);
            lantern.enabled = false;
            var look = root.gameObject.AddComponent<ShipLook>();
            look.Setup(ship, body, hull, wake, lantern, Spr("tau_len"), Spr("tau_xuong"), side, foams.ToArray(), foamSprites, scale);
            look.SetBow(bow, bowFrames);
            look.SetWakeFrames(Enumerable.Range(1, 10).Select(i => Spr("tau_vet_" + i)).Where(s => s).ToArray());
            // tàu 3D: 32 khung theo hướng (ArtGen/Islands/sanh_moi/ben_tau/tau3d), gốc ở tâm thân mớn nước
            var meta3d = AssetDatabase.LoadAssetAtPath<TextAsset>(ArtDir + "3d/tau_hd.json");
            if (meta3d)
            {
                var root3d = J.Obj(MiniJson.Parse(meta3d.text));
                var sz = J.Arr(root3d, "size");
                float W = System.Convert.ToSingle(sz[0]), H = System.Convert.ToSingle(sz[1]);
                var fr = J.Arr(root3d, "frames");
                var sprites = new List<Sprite>();
                var angles = new List<float>();
                var bows = new List<Vector2>();
                var lanterns = new List<Vector2>();
                Vector2 piv = Vector2.zero;
                for (int i = 0; i < fr.Count; i++)
                {
                    var f = J.Obj(fr[i]);
                    var sp = AssetDatabase.LoadAssetAtPath<Sprite>(ArtDir + $"3d/tau_hd_{i:00}.png");
                    if (!sp) continue;
                    var p = J.Arr(f, "pivot");
                    piv = new Vector2(System.Convert.ToSingle(p[0]), System.Convert.ToSingle(p[1]));
                    Vector2 Rel(string key)
                    {
                        var q = J.Arr(f, key);
                        return new Vector2(System.Convert.ToSingle(q[0]) - piv.x, piv.y - System.Convert.ToSingle(q[1]));
                    }
                    sprites.Add(sp);
                    angles.Add((float)J.Num(f, "angle"));
                    bows.Add(Rel("bow"));
                    lanterns.Add(Rel("lantern"));
                }
                if (sprites.Count > 0)
                {
                    look.SetDirFrames(sprites.ToArray(), angles.ToArray(), bows.ToArray(), lanterns.ToArray());
                    hull.sprite = sprites[0];
                    hull.SetNativeSize();
                    hull.rectTransform.pivot = new Vector2(piv.x / W, 1 - piv.y / H);
                    hull.rectTransform.anchoredPosition = Vector2.zero;
                }
            }
            ship.localScale = new Vector3(scale, scale, 1);
            return look;
        }

        // ---------- tiện ích ----------

        static Sprite Spr(string n) => AssetDatabase.LoadAssetAtPath<Sprite>(ArtDir + n + ".png");

        static Sprite BootSpr(string n)
        {
            var s = AssetDatabase.LoadAssetAtPath<Sprite>(BootDir + n + ".png");
            if (!s) Debug.LogError($"[Bến tàu] Thiếu ảnh {BootDir}{n}.png");
            return s;
        }

        static void Folder(string path)
        {
            if (AssetDatabase.IsValidFolder(path)) return;
            var parent = Path.GetDirectoryName(path).Replace('\\', '/');
            Folder(parent);
            AssetDatabase.CreateFolder(parent, Path.GetFileName(path));
        }

        static RectTransform Node(Transform parent, string name, params System.Type[] extra)
        {
            var go = new GameObject(name, new[] { typeof(RectTransform) }.Concat(extra).ToArray());
            go.layer = LayerMask.NameToLayer("UI");
            go.transform.SetParent(parent, false);
            return (RectTransform)go.transform;
        }

        static Image Img(Transform parent, string name, Sprite s, Color c, bool raycast = false)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
            go.layer = LayerMask.NameToLayer("UI");
            go.transform.SetParent(parent, false);
            var img = go.GetComponent<Image>();
            Theme.SetSprite(img, s);
            img.color = c;
            img.raycastTarget = raycast;
            return img;
        }

        static TextMeshProUGUI Text(Transform parent, string name, TMP_FontAsset font, float size, Color color, string text)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(TextMeshProUGUI));
            go.layer = LayerMask.NameToLayer("UI");
            go.transform.SetParent(parent, false);
            var t = go.GetComponent<TextMeshProUGUI>();
            t.font = font;
            t.fontSize = size;
            t.color = color;
            t.alignment = TextAlignmentOptions.Center;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Overflow;
            t.raycastTarget = false;
            t.text = text;
            return t;
        }
    }
}
