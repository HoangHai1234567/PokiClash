// Phát một rig .atomik: tính xương từng khung, biến dạng lưới có trọng số trên CPU, vẽ bằng một Mesh (một lần vẽ, tam giác
// theo thứ tự slot). GameObject, MeshFilter, MeshRenderer dựng sẵn trong scene/prefab; ở đây chỉ sinh Mesh (luật PrefabOnly).
// Phần tính tư thế và dựng lưới dùng chung với AolaActor (dạng tướng là .atomik): AtomikPose.
using UnityEngine;

namespace PokiClash.Game
{
    [ExecuteAlways]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public sealed class AtomikPlayer : MonoBehaviour
    {
        public AtomikAsset asset;
        public string clip = "idle";
        public bool loop = true;
        public float speed = 1f;
        public float mixTime = 0.12f;   // trộn tư thế khi đổi clip

        public float Time01 => cur >= 0 && asset.anims[cur].dur > 0 ? Mathf.Repeat(time, asset.anims[cur].dur) / asset.anims[cur].dur : 0;
        public bool Done => cur >= 0 && !loop && time >= asset.anims[cur].dur;

        Mesh mesh;
        AtomikAsset built;
        AtomikPose pose;
        int cur = -1;
        int aura = -1;      // clip lặp "aura" (mây bay vòng...): phủ lên clip chính theo đồng hồ riêng, liền qua mọi lần đổi clip
        float time, mixLeft, auraTime;
        Vector3[] verts;
        Vector2[] uvs;
        Color32[] cols;

        public void Play(string name, bool loopClip = true)
        {
            if (!Ready()) return;
            int i = asset.FindClip(name);
            if (i < 0) { Debug.LogWarning($"[Atomik] {asset.rigName}: không có clip {name}"); return; }
            if (cur >= 0 && mixTime > 0)
            {
                pose.Snapshot();
                mixLeft = mixTime;
            }
            cur = i;
            clip = name;
            loop = loopClip;
            time = 0;
            Apply();
        }

        // Dựng đúng một thời điểm (Editor chụp khung, kiểm so với khung Python).
        public void Sample(string name, float t)
        {
            if (!Ready()) return;
            cur = asset.FindClip(name);
            clip = name;
            time = t;
            mixLeft = 0;
            Apply();
        }

        void OnEnable()
        {
            if (!Ready()) return;
            cur = asset.FindClip(clip);
            time = 0;
            Apply();
        }

        void OnDisable()
        {
            if (mesh == null) return;
            if (Application.isPlaying) Destroy(mesh); else DestroyImmediate(mesh);
            mesh = null;
            built = null;
        }

        void Update()
        {
            if (!Ready()) return;
            if (Application.isPlaying)
            {
                float dt = UnityEngine.Time.deltaTime * speed;
                time += dt;
                auraTime += dt;
                if (mixLeft > 0) mixLeft = Mathf.Max(0, mixLeft - dt);
            }
            else if (cur < 0 || asset.anims[cur].name != clip) cur = asset.FindClip(clip);
            Apply();
        }

        bool Ready()
        {
            if (asset == null || asset.bones == null || asset.bones.Length == 0) return false;
            if (built == asset && mesh != null) return true;
            pose = new AtomikPose(asset);
            verts = new Vector3[pose.maxVerts];
            uvs = new Vector2[pose.maxVerts];
            cols = new Color32[pose.maxVerts];
            if (mesh == null)
            {
                mesh = new Mesh { name = "atomik_" + asset.rigName, hideFlags = HideFlags.DontSave };
                mesh.MarkDynamic();
            }
            GetComponent<MeshFilter>().sharedMesh = mesh;
            var r = GetComponent<MeshRenderer>();
            if (asset.material != null && r.sharedMaterial != asset.material) r.sharedMaterial = asset.material;
            built = asset;
            cur = -1;
            aura = asset.FindClip("aura");
            return true;
        }

        void Apply()
        {
            float t = 0;
            if (cur >= 0)
            {
                var c = asset.anims[cur];
                t = c.dur <= 0 ? 0 : loop ? Mathf.Repeat(time, c.dur) : Mathf.Min(time, c.dur);
            }
            pose.Sample(cur, t);
            if (mixLeft > 0 && mixTime > 0) pose.Mix(1 - mixLeft / mixTime);
            if (aura >= 0 && aura != cur) pose.Overlay(aura, Mathf.Repeat(auraTime, Mathf.Max(1e-3f, asset.anims[aura].dur)));
            pose.World();
            int nv = pose.Skin(verts, uvs, cols, 1f / Mathf.Max(1e-3f, asset.ppu), false, -1, out bool trisChanged);
            if (trisChanged)
            {
                mesh.Clear();
                mesh.SetVertices(verts, 0, nv);
                mesh.SetUVs(0, uvs, 0, nv);
                mesh.SetColors(cols, 0, nv);
                mesh.SetTriangles(pose.Tris, 0, true);
            }
            else
            {
                mesh.SetVertices(verts, 0, nv);
                mesh.SetColors(cols, 0, nv);
                mesh.RecalculateBounds();
            }
        }
    }
}
