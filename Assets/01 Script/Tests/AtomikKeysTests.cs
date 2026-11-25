// Khoá gọn của .atomik (2026-11-13, dung lượng build): AtomikImporter đổi khoá sải 7 / 12 sang AtomikCurve. Kiểm mọi file .atomik
// trong Assets: lấy mẫu khoá cũ và khoá gọn ở mọi giờ khoá, giữa hai khoá và mỗi 1/60 giây phải ra đúng từng bit; khoá bậc và bezier
// (file hiện chưa có) kiểm bằng khoá tự dựng; asset đã nhập không còn khoá cũ và không mang icon.
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using NUnit.Framework;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;

namespace PokiClash.Tests
{
    public class AtomikKeysTests
    {
        static AtomikAsset Read(string path)
        {
            var bytes = File.ReadAllBytes(path);
            string json;
            using (var ms = new MemoryStream(bytes, 6, bytes.Length - 6))
            using (var gz = new GZipStream(ms, CompressionMode.Decompress))
            using (var br = new BinaryReader(gz))
                json = Encoding.UTF8.GetString(br.ReadBytes(br.ReadInt32()));
            return AtomikAsset.FromJson(json);
        }

        static IEnumerable<string> Files() =>
            Directory.GetFiles("Assets", "*.atomik", SearchOption.AllDirectories).Select(p => p.Replace('\\', '/'));

        static List<float> Times(float[] k, int stride, float dur)
        {
            var ts = new List<float> { -0.1f, 0, dur, dur + 0.1f };
            for (float t = 0; t <= dur + 1e-4f; t += 1 / 60f) ts.Add(t);
            for (int i = 0; i + stride <= k.Length; i += stride)
            {
                ts.Add(k[i]);
                if (i + stride < k.Length) ts.Add((k[i] + k[i + stride]) * 0.5f);
            }
            return ts;
        }

        [Test]
        public void PackedKeysMatchOldKeysBitForBit()
        {
            int files = 0, curves = 0;
            long samples = 0;
            foreach (var path in Files())
            {
                var old = Read(path);
                var packed = Read(path);
                AtomikPose.PackAll(packed);
                files++;
                for (int ci = 0; ci < old.anims.Length; ci++)
                {
                    var co = old.anims[ci];
                    var cn = packed.anims[ci];
                    for (int ti = 0; co.tls != null && ti < co.tls.Length; ti++)
                    {
                        var k = co.tls[ti].keys;
                        var c = cn.tls[ti].c;
                        Assert.AreEqual(0, cn.tls[ti].keys.Length, $"{path}: khoá cũ chưa bỏ");
                        curves++;
                        bool rot = co.tls[ti].type == 0;
                        foreach (var t in Times(k, rot ? 7 : 12, co.dur))
                        {
                            samples++;
                            if (rot)
                            {
                                float a = AtomikPose.Sample1(k, t), b = AtomikPose.SampleC1(c, t);
                                if (a != b) Assert.Fail($"{path} clip {co.name} xương {co.tls[ti].bone} xoay t={t}: {a} khác {b}");
                            }
                            else
                            {
                                AtomikPose.Sample2(k, t, out float ax, out float ay);
                                AtomikPose.SampleC2(c, t, out float bx, out float by);
                                if (ax != bx || ay != by)
                                    Assert.Fail($"{path} clip {co.name} xương {co.tls[ti].bone} kiểu {co.tls[ti].type} t={t}: ({ax}, {ay}) khác ({bx}, {by})");
                            }
                        }
                    }
                    for (int si = 0; co.sa != null && si < co.sa.Length; si++)
                    {
                        var k = co.sa[si].keys;
                        var c = cn.sa[si].c;
                        curves++;
                        foreach (var t in Times(k, 7, co.dur))
                        {
                            samples++;
                            float a = AtomikPose.Sample1(k, t), b = AtomikPose.SampleC1(c, t);
                            if (a != b) Assert.Fail($"{path} clip {co.name} độ đậm slot {co.sa[si].slot} t={t}: {a} khác {b}");
                        }
                    }
                }
                Object.DestroyImmediate(old);
                Object.DestroyImmediate(packed);
            }
            Assert.Greater(files, 0, "không thấy file .atomik nào");
            TestContext.WriteLine($"{files} file, {curves} đường khoá, {samples} lần lấy mẫu khớp");
        }

        [Test]
        public void SteppedAndBezierKeysMatch()
        {
            // xoay: khoá 0 thẳng, khoá 1 bậc, khoá 2 bezier, khoá 3 cuối
            var r = new float[]
            {
                0f, 10f, 0, 0, 0, 0, 0,
                0.3f, 40f, 1, 0, 0, 0, 0,
                0.5f, -20f, 2, 0.6f, 0f, 0.8f, 30f,
                1f, 5f, 0, 0, 0, 0, 0,
            };
            // dời: khoá 0 bezier, khoá 1 bậc, khoá 2 cuối
            var m = new float[]
            {
                0f, 1f, 2f, 2, 0.1f, 5f, 0.3f, 1f, 0.1f, -4f, 0.2f, 8f,
                0.4f, 7f, -3f, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                0.9f, 0f, 0f, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            };
            var cr = AtomikPose.Pack(r, 1);
            var cm = AtomikPose.Pack(m, 2);
            CollectionAssert.AreEqual(new[] { 1, 2 }, cr.ck);
            CollectionAssert.AreEqual(new[] { 0, 1 }, cm.ck);
            for (float t = -0.2f; t <= 1.2f; t += 0.01f)
            {
                Assert.AreEqual(AtomikPose.Sample1(r, t), AtomikPose.SampleC1(cr, t), $"xoay t={t}");
                AtomikPose.Sample2(m, t, out float ax, out float ay);
                AtomikPose.SampleC2(cm, t, out float bx, out float by);
                Assert.AreEqual(ax, bx, $"dời x t={t}");
                Assert.AreEqual(ay, by, $"dời y t={t}");
            }
        }

        // atlas đã nhập: dáng đứng không quá trần độ nét (EditorTools.AtomikImporter.AtlasCap) trên atlas
        [Test]
        public void ImportedAtlasWithinCap()
        {
            int n = 0;
            long after = 0;
            foreach (var path in Files())
            {
                var rig = AssetDatabase.LoadAssetAtPath<AtomikAsset>(path);
                if (!rig || rig.atlasSize.x <= 0) continue; // cỡ atlas ghi lúc nhập (atlas mã hoá, khỏi giải)
                int aw = rig.atlasSize.x, ah = rig.atlasSize.y;
                float s = EditorTools.AtomikImporter.AtlasScale(rig, aw, ah);
                Assert.Greater(s, 0.95f, $"{path}: atlas {aw}x{ah} còn quá trần (hệ số {s:0.00})");
                n++;
                after += (long)((aw + 7) / 8) * ((ah + 7) / 8) * 16;
            }
            TestContext.WriteLine($"{n} atlas trong trần {EditorTools.AtomikImporter.AtlasCap}; ASTC 8x8 tổng {after / 1048576f:0.0} MB");
        }

        // Khối gọn AtomikPack (2026-11-23): ghi rồi giải mọi file .atomik, cấu trúc giữ nguyên (số phần tử, tên, chỉ số), số thực lệch
        // không quá nửa bước lượng tử (cộng sai số làm tròn float), số ghi nguyên (khoá cũ, điểm điều khiển, giờ sự kiện) trùng từng bit.
        [Test]
        public void PackRoundTripWithinQuantum()
        {
            int files = 0;
            long raw = 0, packedBytes = 0;
            foreach (var path in Files())
            {
                var a = Read(path);
                AtomikPose.PackAll(a);
                var blob = AtomikPack.Write(a.atts, a.anims);
                AtomikPack.Read(blob, out var atts, out var anims);
                files++;
                packedBytes += blob.Length;
                Assert.AreEqual(a.atts.Length, atts.Length, path);
                for (int i = 0; i < atts.Length; i++)
                {
                    var o = a.atts[i];
                    var n = atts[i];
                    string at = $"{path} hình {o.name}";
                    Assert.AreEqual(o.slot, n.slot, at);
                    Assert.AreEqual(o.name ?? "", n.name, at);
                    Near(o.uvs, n.uvs, AtomikPack.QUv, at + " uv");
                    CollectionAssert.AreEqual(o.tris ?? new int[0], n.tris, at + " tam giác");
                    Assert.AreEqual(o.wInfo?.Length ?? 0, n.wInfo.Length, at + " trọng số");
                    for (int k = 0; k < n.wInfo.Length; k++)
                        Assert.AreEqual(o.wInfo[k], n.wInfo[k], 0.5 / AtomikPack.QPos + System.Math.Abs(o.wInfo[k]) * 1.2e-7, at + $" trọng số [{k}]");
                    raw += 4L * ((o.uvs?.Length ?? 0) + (o.tris?.Length ?? 0) + (o.wInfo?.Length ?? 0));
                }
                Assert.AreEqual(a.anims.Length, anims.Length, path);
                for (int ci = 0; ci < anims.Length; ci++)
                {
                    var o = a.anims[ci];
                    var n = anims[ci];
                    string at = $"{path} clip {o.name}";
                    Assert.AreEqual(o.name ?? "", n.name, at);
                    Assert.AreEqual(o.dur, n.dur, at);
                    Assert.AreEqual(o.tls?.Length ?? 0, n.tls.Length, at);
                    for (int ti = 0; ti < n.tls.Length; ti++)
                    {
                        var ot = o.tls[ti];
                        var nt = n.tls[ti];
                        Assert.AreEqual(ot.bone, nt.bone, at);
                        Assert.AreEqual(ot.type, nt.type, at);
                        CollectionAssert.AreEqual(ot.keys ?? new float[0], nt.keys, at + " khoá cũ");
                        double q = ot.type == 0 ? AtomikPack.QRot : ot.type == 1 ? AtomikPack.QPos : AtomikPack.QScale;
                        CurveNear(ot.c, nt.c, q, at + $" xương {ot.bone} kiểu {ot.type}");
                        raw += 4L * ((ot.c?.t?.Length ?? 0) + (ot.c?.v?.Length ?? 0));
                    }
                    Assert.AreEqual(o.sk?.Length ?? 0, n.sk.Length, at);
                    for (int si = 0; si < n.sk.Length; si++)
                    {
                        Assert.AreEqual(o.sk[si].slot, n.sk[si].slot, at);
                        Near(o.sk[si].times, n.sk[si].times, AtomikPack.QTime, at + " giờ đổi hình");
                        CollectionAssert.AreEqual(o.sk[si].atts ?? new int[0], n.sk[si].atts, at + " đổi hình");
                    }
                    Assert.AreEqual(o.sa?.Length ?? 0, n.sa.Length, at);
                    for (int si = 0; si < n.sa.Length; si++)
                    {
                        Assert.AreEqual(o.sa[si].slot, n.sa[si].slot, at);
                        CurveNear(o.sa[si].c, n.sa[si].c, AtomikPack.QAlpha, at + " độ đậm");
                    }
                    Assert.AreEqual(o.ev?.Length ?? 0, n.ev.Length, at);
                    for (int ei = 0; ei < n.ev.Length; ei++)
                    {
                        Assert.AreEqual(o.ev[ei].t, n.ev[ei].t, at);
                        Assert.AreEqual(o.ev[ei].name ?? "", n.ev[ei].name, at);
                        Assert.AreEqual(o.ev[ei].s ?? "", n.ev[ei].s, at);
                    }
                }
                Object.DestroyImmediate(a);
            }
            Assert.Greater(files, 0, "không thấy file .atomik nào");
            TestContext.WriteLine($"{files} file: float thô {raw / 1048576f:0.0} MB → khối gọn {packedBytes / 1048576f:0.0} MB");
        }

        // Lưới dựng từ asset đã nhập (giải khối gọn) và từ JSON gốc của file: mọi clip, 5 khung/giây (15 khung/giây chạy quá 3 phút),
        // đỉnh lệch nhau dưới 0,05 px rig
        // (tướng trên sân cao ~300 điểm màn cho rig cao 600-1200 px: lệch thật dưới 1/40 điểm màn), UV dưới 1/100 texel, màu lệch tối
        // đa 1/255. Clip có cánh tay đòn rất dài (nham_than_1 appear: xương dời 19000 px, phóng x18) là ca khó nhất cho lượng tử góc.
        [Test, Timeout(300000)]
        public void ImportedPoseMatchesJson()
        {
            int files = 0;
            long verts = 0;
            double worstPos = 0, worstUv = 0;
            string worstAt = "";
            foreach (var path in Files())
            {
                var rig = AssetDatabase.LoadAssetAtPath<AtomikAsset>(path);
                if (!rig) continue;
                var src = Read(path);
                AtomikPose.PackAll(src);
                // so lưới trước mặt nạ cắt: đỉnh sát mép cắt dời 1/1000 px đã đủ đổi số tam giác bị xén (code cắt không đổi). Bản sao
                // của asset đã nhập còn kiểm luôn đường tuần tự Unity (ghi khối → đọc lại).
                var copy = Object.Instantiate(rig);
                src.masks = null;
                copy.masks = null;
                var pa = new AtomikPose(src);
                var pb = new AtomikPose(copy);
                Assert.AreEqual(pa.maxVerts, pb.maxVerts, path);
                int m = pa.maxVerts;
                var va = new Vector3[m]; var vb = new Vector3[m];
                var ua = new Vector2[m]; var ub = new Vector2[m];
                var ca = new Color32[m]; var cb = new Color32[m];
                float tex = rig.atlasSize.x > 0 ? Mathf.Max(rig.atlasSize.x, rig.atlasSize.y) : 2048;
                for (int ci = -1; ci < src.anims.Length; ci++)
                {
                    float dur = ci < 0 ? 0 : src.anims[ci].dur;
                    for (float t = 0; t <= dur + 1e-4f; t += 1 / 5f)
                    {
                        pa.Sample(ci, t); pa.World();
                        pb.Sample(ci, t); pb.World();
                        int na = pa.Skin(va, ua, ca, 1, false, -1, out _);
                        int nb = pb.Skin(vb, ub, cb, 1, false, -1, out _);
                        string at = $"{path} clip {(ci < 0 ? "gốc" : src.anims[ci].name)} t={t:0.000}";
                        Assert.AreEqual(na, nb, at + ": số đỉnh");
                        CollectionAssert.AreEqual(pa.Tris, pb.Tris, at + ": tam giác");
                        for (int i = 0; i < na; i++)
                        {
                            double dp = (va[i] - vb[i]).magnitude, du = (ua[i] - ub[i]).magnitude * tex;
                            if (dp > worstPos) { worstPos = dp; worstAt = at + $" đỉnh {i}"; }
                            worstUv = System.Math.Max(worstUv, du);
                            // độ đậm lượng tử 1/65536 có khi rơi đúng ngưỡng làm tròn byte: cho lệch 1 bậc (1/255)
                            if (System.Math.Abs(ca[i].r - cb[i].r) > 1 || System.Math.Abs(ca[i].g - cb[i].g) > 1 ||
                                System.Math.Abs(ca[i].b - cb[i].b) > 1 || System.Math.Abs(ca[i].a - cb[i].a) > 1)
                                Assert.Fail($"{at}: màu đỉnh {i} {ca[i]} khác {cb[i]}");
                        }
                        verts += na;
                        if (ci < 0) break;
                    }
                }
                Object.DestroyImmediate(src);
                Object.DestroyImmediate(copy);
                files++;
            }
            Assert.Greater(files, 0, "không thấy asset .atomik nào");
            TestContext.WriteLine($"{files} rig, {verts} đỉnh: lệch lớn nhất {worstPos:0.0000} px rig ({worstAt}), UV {worstUv:0.0000} texel");
            Assert.Less(worstPos, 0.05, $"đỉnh lệch {worstPos:0.0000} px ở {worstAt}");
            Assert.Less(worstUv, 0.01, "UV lệch");
        }

        // lệch không quá nửa bước lượng tử cộng sai số làm tròn float của chính giá trị
        static void Near(float[] o, float[] n, double q, string at)
        {
            o ??= new float[0];
            Assert.AreEqual(o.Length, n.Length, at + " số phần tử");
            for (int i = 0; i < o.Length; i++)
            {
                double tol = 0.5 / q + System.Math.Abs(o[i]) * 1.2e-7;
                if (System.Math.Abs(o[i] - n[i]) > tol) Assert.Fail($"{at} [{i}]: {o[i]} → {n[i]} lệch quá {tol}");
            }
        }

        static void CurveNear(AtomikCurve o, AtomikCurve n, double q, string at)
        {
            Near(o?.t, n.t, AtomikPack.QTime, at + " giờ");
            Near(o?.v, n.v, q, at + " giá trị");
            CollectionAssert.AreEqual(o?.ck ?? new int[0], n.ck, at + " ck");
            CollectionAssert.AreEqual(o?.cp ?? new float[0], n.cp, at + " cp");
        }

        [Test]
        public void ImportedRigsArePackedWithoutIcon()
        {
            foreach (var path in Files())
            {
                var all = AssetDatabase.LoadAllAssetsAtPath(path);
                var rig = all.OfType<AtomikAsset>().FirstOrDefault();
                Assert.IsNotNull(rig, $"{path}: chưa nhập");
                Assert.Greater(rig.PackedBytes, 0, $"{path}: chưa ghi khối gọn (nhập lại)");
                Assert.IsTrue(rig.atts != null && rig.atts.Length > 0 && rig.anims != null && rig.anims.Length > 0, $"{path}: giải khối gọn ra rỗng");
                Assert.IsFalse(all.OfType<Texture2D>().Any(t => t.name.EndsWith("_icon")), $"{path}: còn icon trong asset");
                // bảo mật ảnh (bản nhập 9, GD_Claude/30): không còn Texture2D thô trong asset, atlas là blob mã hoá giải ra được
                Assert.IsFalse(all.OfType<Texture2D>().Any(), $"{path}: còn atlas thô (Texture2D) trong asset");
                Assert.IsTrue(rig.HasEncryptedAtlas, $"{path}: chưa có atlas mã hoá (nhập lại)");
                var plain = PokiClash.Security.PokiCrypt.TryDecrypt(rig.EncryptedAtlas, "texture");
                var tb = plain == null ? null : PokiClash.Security.TexBlob.Unpack(plain);
                Assert.IsNotNull(tb, $"{path}: atlas mã hoá không giải được");
                Assert.AreEqual(rig.atlasSize.x, tb.width, path);
                Assert.AreEqual(rig.atlasSize.y, tb.height, path);
                Assert.Greater(tb.raw.Length, 0, path);
                foreach (var c in rig.anims)
                {
                    Assert.IsTrue(c.tls == null || c.tls.All(tl => tl.keys == null || tl.keys.Length == 0), $"{path} clip {c.name}: còn khoá cũ");
                    Assert.IsTrue(c.sa == null || c.sa.All(k => k.keys == null || k.keys.Length == 0), $"{path} clip {c.name}: còn khoá độ đậm cũ");
                }
            }
        }
    }
}
