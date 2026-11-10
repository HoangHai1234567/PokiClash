# Ghi chú nghiên cứu: hiệu năng và cách dựng hiệu ứng trên uGUI (2026-11-10)

Cho Unity 6 (URP), Android tầm trung và thấp, hiệu ứng là Image trong hàng chờ cộng lưới tự dựng (`HatLua`, `HatMang`). Mỗi dòng có
nguồn. **[chưa kiểm chứng]** / **[chưa đo]**: chưa đọc được trang gốc hoặc chưa có số đo, coi là gợi ý.

Bài "Optimizing Unity UI" trên Unity Learn đã bị gỡ. Mã nguồn uGUI đọc là bản 1.0.0, chưa đối chiếu bản 2.0 của Unity 6.

## 1. Chi phí uGUI

- Một phần tử đổi là cả Canvas bị đánh dấu và phải phân tích lại batch. Canvas con cô lập với cha và anh em. Gom các phần tử cùng
  nhịp cập nhật, cùng Z, cùng material và texture vào một Canvas. https://unity.com/how-to/unity-ui-optimization-tips
- Batch chỉ gộp khi cùng Canvas, cùng Material, cùng texture, đồng phẳng và cùng Mask. Dựng lại hiện trong Profiler là
  `Canvas.SendWillRenderCanvases`. https://www.slideshare.net/slideshow/unite-2017-tokyounity-ui/75767146
- `Image.color` gọi `SetVerticesDirty()`: dựng lại lưới của Image đó (`OnPopulateMesh` → `FillMesh` → `CanvasRenderer.SetMesh`).
  `canvasRenderer.SetColor` (đường của `CrossFadeColor`) không dựng lại lưới.
  https://github.com/needle-mirror/com.unity.ugui/blob/master/Runtime/UI/Core/Graphic.cs
- Đổi kích thước rect gọi `SetVerticesDirty` + `SetLayoutDirty`. Đổi vị trí không gọi lại `OnPopulateMesh`. Suy ra phóng hạt bằng
  `localScale` rẻ hơn `sizeDelta` **[chưa đo]**. (cùng file)
- `Image.sprite` gọi `SetAllDirty()`, nhưng bỏ layout nếu ảnh mới cùng kích thước rect và bỏ material nếu cùng texture: ảnh chạy
  khung nên cùng atlas, cùng cỡ ô. https://github.com/needle-mirror/com.unity.ugui/blob/master/Runtime/UI/Core/Image.cs
- Tắt/bật Graphic: `OnDisable` gọi `canvasRenderer.Clear()` và đánh dấu layout; `OnEnable` gọi `SetAllDirty()`. Bật tắt mỗi khung
  hình là đắt. (Graphic.cs)
- Alpha 0 vẫn có thể tốn lệnh vẽ. Ẩn cả lớp thì tắt component `Canvas`, không tắt GameObject: giữ bộ đệm đỉnh, không dựng lại khi
  bật. https://unity.com/blog/games/optimize-your-mobile-game-performance-get-expert-tips-on-physics-ui-and-audio-settings
- `CanvasRenderer.cullTransparentMesh` bỏ hình khi alpha mọi đỉnh gần 0.
  https://docs.unity.com/en-us/engine/current/script-reference/unityengine/canvasrenderer/culltransparentmesh
- Số đo bên thứ ba (Pixel 1, Unity 2022.3): 8 phần tử chuyển động làm batching tăng 0,65 → 1,10 ms; bọc từng phần tử vào canvas
  con làm batching gấp đôi. https://hackernoon.com/how-to-optimize-uis-in-unity-slow-performance-causes-and-solutions
- Bên thứ ba: bật tắt tần suất cao nên dùng `localScale` 0/1 thay `SetActive`.
  https://dev.to/gameoptim/unity-ugui-optimization-why-renderingupdatebatches-can-cost-more-than-your-combat-scene-13oc
- Sprite Atlas: chỉ batch được ảnh cùng texture. https://mcrvaz.github.io/blog/unity-ui-tips-draw-calls

## 2. Vẽ đè (overdraw)

- Tránh ảnh trong suốt chồng nhau; điện thoại chịu nặng vì vẽ đè và trộn alpha.
  https://unity.com/blog/games/optimize-your-mobile-game-performance-expert-tips-on-graphics-and-assets
- Mốc của Arm: hệ số vẽ đè khoảng 2,5 lần đã là "khá cao"; lý tưởng 1 lần mỗi điểm ảnh. Không có ngân sách chính thức cho hạt UI.
  https://developer.arm.com/community/arm-community-blogs/b/mobile-graphics-and-gaming-blog/posts/mali-gpu-tools-a-case-study-part-2-frame-analysis-with-mali-graphics-debugger
- Editor: Window > Analysis > Rendering Debugger, chế độ Overdraw ở Rendering > Rendering Debug. Trên máy: chạm đúp ba ngón, chỉ ở
  bản Development và phải tắt "Strip Debug Variants".
  https://docs.unity.com/en-us/engine/6000.0/manual/analysis/graphics-performance-profiling/in-urp/understand-performance/rendering-debugger/use
- Profiler UI Details có xem trước "Overdraw" và "Composite Overdraw" cho từng canvas.
  https://docs.unity3d.com/2022.3/Documentation/Manual/ProfilerUI.html
- Android: dùng Android GPU Inspector hoặc Arm Streamline / Frame Advisor ("Profile GPU Rendering" không dùng được với app NDK).
  https://developer.android.com/topic/performance/rendering/inspect-gpu-rendering
- `Image.useSpriteMesh = true` cùng `SpriteMeshType = Tight`: lưới ôm sát hình thay cho ô chữ nhật đầy.
  https://docs.unity3d.com/Packages/com.unity.ugui@2.0/api/UnityEngine.UI.Image.html

## 3. Lưới Graphic tự dựng (như HatMang)

- Mỗi lần `SetVerticesDirty`: `OnPopulateMesh(VertexHelper)` → quét `IMeshModifier` → `FillMesh` → `canvasRenderer.SetMesh`. Chi phí
  tỉ lệ số đỉnh, cộng phân tích lại batch của canvas. (Graphic.cs)
- `VertexHelper.FillMesh` ném lỗi khi từ 65000 đỉnh.
  https://github.com/needle-mirror/com.unity.ugui/blob/master/Runtime/UI/Core/Utility/VertexHelper.cs
- Tự giữ `Mesh` rồi gọi `CanvasRenderer.SetMesh` thì bỏ được VertexHelper nhưng canvas vẫn phân tích lại batch **[mức lợi chưa đo]**.
  https://docs.unity.com/en-us/engine/current/script-reference/unityengine/canvasrenderer/setmesh

## 4. Phương án thay thế

- UIParticle (mob-sakai) nướng ParticleSystem thành lưới qua `CanvasRenderer`, giới hạn 65535 đỉnh. Số đo trong README (khung/giây,
  Xperia XZ): ParticleSystem thường 22, UIParticle 4, UIParticle + Mesh Sharing 30.
  https://github.com/mob-sakai/ParticleEffectForUGUI
- Gộp các phần tử chồng lớp thành ít phần tử, ít batch hơn là khuyến nghị chính thức; một lưới nhiều ô (một `CanvasRenderer`) là
  dạng áp dụng **[mức lợi chưa đo]**. https://unity.com/how-to/unity-ui-optimization-tips
- GPU instancing chỉ cho MeshRenderer và `Graphics.RenderMeshInstanced`, không cho Canvas.
  https://docs.unity.com/en-us/engine/6000.0/manual/analysis/graphics-performance-profiling/reduce-draw-calls/gpuinstancing/gpuinstancing

## 5. Ảnh hạt xám

- ASTC, ảnh 1024²: 4x4 = 1,0 MB; 5x5 = 0,64 MB; 6x6 = 0,45 MB; 8x8 = 0,25 MB.
  https://docs.unity.com/en-us/engine/6000.0/manual/materials-and-shaders/textures/textures-getting-started/texture-compression-formats/texture-formats-reference
- Mipmap tăng 33% dung lượng; vô ích với UI không co giãn.
  https://docs.unity.com/en-us/engine/6000.0/manual/materials-and-shaders/textures/textures-getting-started/texture-mipmaps-introduction
- Tắt Read/Write (bật thì bộ nhớ gấp đôi); Max Size nhỏ nhất còn chấp nhận được.
  https://unity.com/blog/games/optimize-your-mobile-game-performance-expert-tips-on-graphics-and-assets
- Sprite Atlas: Padding mặc định 4 px; tắt Allow Rotation cho UI; có Alpha Dilation chống viền.
  https://docs.unity.com/en-us/engine/6000.0/manual/unity2d/sprite/atlas/sprite-atlas-reference

## 6. Rác bộ nhớ (GC)

- Lambda bắt biến cục bộ cấp phát heap mỗi lần chạy; truyền tham chiếu phương thức cũng cấp phát. Tránh trong mã chạy mỗi khung.
  https://docs.unity.com/en-us/engine/6000.0/manual/analysis/performance-memory/managed-memory/optimizing-code-managed-memory/reference-types
- Nối chuỗi mỗi khung tạo chuỗi tạm (cùng trang). Tra ảnh bằng chỉ số hoặc từ điển dựng sẵn.
- Giữ `List` tái dùng giữa các khung; tránh LINQ; pool đối tượng cấp sẵn.
  https://docs.unity.com/en-us/engine/6000.0/manual/analysis/performance-memory/managed-memory/optimizing-code-managed-memory/arrays

## 7. Cách đo

- Ngân sách: chỉ dùng khoảng 65% khung hình, tức 22 ms ở 30 khung/giây và 11 ms ở 60. Đo bản Development trên máy đích.
  https://unity.com/blog/games/optimize-your-mobile-game-performance-tips-on-profiling-memory-and-code-architecture-from
- Profiler UI / UI Details: Layout, Render (ms), Batches, Vertices, cột "Batch Breaking Reason".
  https://docs.unity3d.com/2022.3/Documentation/Manual/ProfilerUI.html
- Frame Debugger liệt kê từng lệnh vẽ, gắn được vào bản build.
  https://docs.unity.com/en-us/engine/6000.0/manual/analysis/graphics-performance-profiling/profile-rendering/frame-debugger/frame-debugger
- Công thức ép tải (đề xuất, chưa có nguồn): bật cùng lúc chiêu nặng nhất ở cả ba lớp với hàng chờ đầy, mảng nước lớn nhất, trên
  máy yếu nhất, chạy 5–10 phút để lộ nóng máy; ghi `SendWillRenderCanvases`, `BuildBatch`, GC Alloc mỗi khung, số batch, ảnh vẽ đè.

## 8. Đối chiếu với mã hiện tại của dự án (chưa sửa, chưa đo)

- `HatLua.Render` mỗi khung gán `Image.color`, `sizeDelta`, `enabled`, đôi khi `sprite` cho từng hạt: theo mục 1, mỗi việc đều dựng
  lại lưới của Image đó, và bật tắt là đắt nhất. Hướng tối ưu nếu đo thấy nặng: đổi cỡ bằng `localScale`, nhuộm bằng
  `canvasRenderer.SetColor`, ẩn bằng `localScale` 0; hoặc gộp tất cả hạt của một lớp vào một lưới nhiều ô như `HatMang` (cần gom
  ảnh hạt vào một atlas).
- `HatNuoc.cs` và `HatLua.cs` tạo lambda cho từng hạt (`upd`, `draw`, `onDeath`) và nối chuỗi tên ảnh (`"wave_" + i`) mỗi khung:
  có cấp phát. Hướng tối ưu: tra ảnh bằng mảng dựng sẵn theo chỉ số, hàm vẽ dùng chung không bắt biến.
- Ba lớp hạt đã là ba Canvas con: đúng khuyến nghị, không tách nhỏ hơn.
