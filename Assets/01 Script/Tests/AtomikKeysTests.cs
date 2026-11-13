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
            var a = ScriptableObject.CreateInstance<AtomikAsset>();
            JsonUtility.FromJsonOverwrite(json, a);
            return a;
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
                if (!rig || !rig.atlas) continue;
                float s = EditorTools.AtomikImporter.AtlasScale(rig, rig.atlas.width, rig.atlas.height);
                Assert.Greater(s, 0.95f, $"{path}: atlas {rig.atlas.width}x{rig.atlas.height} còn quá trần (hệ số {s:0.00})");
                n++;
                after += (long)((rig.atlas.width + 7) / 8) * ((rig.atlas.height + 7) / 8) * 16;
            }
            TestContext.WriteLine($"{n} atlas trong trần {EditorTools.AtomikImporter.AtlasCap}; ASTC 8x8 tổng {after / 1048576f:0.0} MB");
        }

        [Test]
        public void ImportedRigsArePackedWithoutIcon()
        {
            foreach (var path in Files())
            {
                var all = AssetDatabase.LoadAllAssetsAtPath(path);
                var rig = all.OfType<AtomikAsset>().FirstOrDefault();
                Assert.IsNotNull(rig, $"{path}: chưa nhập");
                Assert.IsFalse(all.OfType<Texture2D>().Any(t => t.name.EndsWith("_icon")), $"{path}: còn icon trong asset");
                foreach (var c in rig.anims)
                {
                    Assert.IsTrue(c.tls == null || c.tls.All(tl => tl.keys == null || tl.keys.Length == 0), $"{path} clip {c.name}: còn khoá cũ");
                    Assert.IsTrue(c.sa == null || c.sa.All(k => k.keys == null || k.keys.Length == 0), $"{path} clip {c.name}: còn khoá độ đậm cũ");
                }
            }
        }
    }
}
