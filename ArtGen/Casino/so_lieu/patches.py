# Sửa nhỏ vào file có sẵn (áp lên bản stage lúc biên dịch; cuối cùng áp thẳng vào Assets bằng apply_patches.py)
PATCHES = [
    ("Core/Pachinko.cs",
     "public enum RewardKind { Exp, Balls, Card, Shards, Hero, LegendCopies, Chest, Stones, EvoStones, Crystal, HeroChest, GoldChest, Ticket, Perk, Egg }",
     "public enum RewardKind { Exp, Balls, Card, Shards, Hero, LegendCopies, Chest, Stones, EvoStones, Crystal, HeroChest, GoldChest, Ticket, Perk, Egg, Bait }"),
    ("Core/SaveData.cs",
     "        public ShopState shop; // cửa hàng, ưu đãi, Lọ Bi, thẻ, túi Rương Tướng (Shop.cs, 2026-11-23; null = chưa dùng)\n",
     "        public ShopState shop; // cửa hàng, ưu đãi, Lọ Bi, thẻ, túi Rương Tướng (Shop.cs, 2026-11-23; null = chưa dùng)\n"
     "        public CasinoState casino; // đảo Casino (Casino.cs, GD_Claude/29_DaoCasino.md; null = chưa ra đảo)\n"),
    ("Core/SaveData.cs",
     "            \"shop\", \"sophep\",\n",
     "            \"shop\", \"sophep\", \"casino\",\n"),
    ("Core/SaveData.cs",
     "            s.sophep = SoPhepState.Read(J.Obj(o, \"sophep\"));\n",
     "            s.sophep = SoPhepState.Read(J.Obj(o, \"sophep\"));\n"
     "            s.casino = CasinoState.Read(J.Obj(o, \"casino\"));\n"),
    ("Core/SaveData.cs",
     "            if (s.sophep != null) o[\"sophep\"] = s.sophep.Write();\n",
     "            if (s.sophep != null) o[\"sophep\"] = s.sophep.Write();\n"
     "            if (s.casino != null) o[\"casino\"] = s.casino.Write();\n"),
    ("Core/BalanceConfig.cs",
     "        public ShopConfig shop = new ShopConfig(); // cửa hàng, ưu đãi (2026-11-23, ShopConfig.cs)\n",
     "        public ShopConfig shop = new ShopConfig(); // cửa hàng, ưu đãi (2026-11-23, ShopConfig.cs)\n"
     "        public CasinoConfig casino = new CasinoConfig(); // đảo Casino (2026-11-25, CasinoConfig.cs, GD_Claude/29_DaoCasino.md)\n"),
    ("Core/BalanceConfig.cs",
     "            c.shop = ShopConfig.FromJson(J.Obj(root, \"shop\"));\n",
     "            c.shop = ShopConfig.FromJson(J.Obj(root, \"shop\"));\n"
     "            c.casino = CasinoConfig.Parse(J.Obj(root, \"casino\"), Rolls);\n"),
]


def apply(root, patches=PATCHES, write=True):
    import os
    out = []
    for rel, old, new in patches:
        p = os.path.join(root, rel)
        with open(p, encoding="utf-8-sig") as f:
            t = f.read()
        crlf = "\r\n" in t
        tt = t.replace("\r\n", "\n")
        if new in tt:
            out.append(("da co", rel))
            continue
        if tt.count(old) != 1:
            raise SystemExit("PATCH KHONG KHOP (%d lan): %s :: %s" % (tt.count(old), rel, old[:80]))
        tt = tt.replace(old, new)
        if crlf:
            tt = tt.replace("\n", "\r\n")
        if write:
            bom = open(p, "rb").read(3) == b"\xef\xbb\xbf"
            with open(p, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
                f.write(tt)
        out.append(("sua", rel))
    return out

# ---- C2: SceneIds, máy bi ↔ đảo ----
PATCHES_C2 = [
    ("App/SceneIds.cs",
     "        public const string Home = \"Home\"; // Nhà (2026-11-18), thay Trang trại trên sảnh\n",
     "        public const string Home = \"Home\"; // Nhà (2026-11-18), thay Trang trại trên sảnh\n"
     "        public const string Casino = \"Casino\"; // đảo Casino \"Bến Lữ Khách\" (2026-11-25, GD_Claude/29_DaoCasino.md)\n"),
    ("App/SceneIds.cs",
     "Badges, Cave, Farm, Home };",
     "Badges, Cave, Farm, Home, Casino };"),
    ("App/Scenes/MachineScene.cs",
     "        public override string Title => Loc.T(\"Máy bi\");\n",
     "        public override string Title => Loc.T(\"Máy bi\");\n"
     "        // vào từ đảo Casino (args = SceneIds.Casino) thì nút quay lại về đảo (GD_Claude/29_DaoCasino.md mục 4)\n"
     "        public override string BackTo => from == SceneIds.Casino ? SceneIds.Casino : SceneIds.Hub;\n"
     "        string from;\n"
     "        [Tooltip(\"Nút Ra đảo: sang đảo Casino (menu PokiClash/Prefab/Đảo Casino/Máy bi: nút Ra đảo)\")]\n"
     "        [SerializeField] SketchButton toIsland;\n"
     "        public void SetupIsland(SketchButton b) => toIsland = b;\n"),
    ("App/Scenes/MachineScene.cs",
     "        public override void Enter(object args)\n        {\n            rng = new Rng(Rng.RandomSeed());\n",
     "        public override void Enter(object args)\n        {\n            from = args as string;\n"
     "            if (toIsland)\n            {\n                toIsland.gameObject.SetActive(Casino.Open(S, D));\n"
     "                toIsland.SetOnClick(() =>\n                {\n                    if (Busy) return;\n"
     "                    App.Router.Go(SceneIds.Casino);\n                });\n            }\n"
     "            rng = new Rng(Rng.RandomSeed());\n"),
]

PATCHES_C2_EDITOR = [
    ("Editor/ArtImporter.cs",
     "                || assetPath.Contains(\"/Home/home_base\") // nền đảo Nhà (GD_Claude/21)\n",
     "                || assetPath.Contains(\"/Home/home_base\") // nền đảo Nhà (GD_Claude/21)\n"
     "                || assetPath.Contains(\"/Casino/casino_map\") // nền đảo Casino (GD_Claude/29), 1536 x 1024 trải 2,7 màn ngang\n"),
]
