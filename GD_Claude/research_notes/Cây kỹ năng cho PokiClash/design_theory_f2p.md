# Lý thuyết thiết kế, UX và kinh tế F2P của cây kỹ năng / talent tree / progression tree

Ghi chú nghiên cứu (2026-11-24). Viết tiếng Việt, giữ thuật ngữ tiếng Anh. Mỗi dữ kiện có link nguồn. Chỗ nào chỉ có tóm tắt từ kết quả tìm kiếm (chưa mở trang gốc) thì ghi rõ "(theo tóm tắt tìm kiếm)". Phần "Inferences" là suy luận của người nghiên cứu, không phải dữ kiện có nguồn.

## 1. Lý thuyết: điều gì làm một lựa chọn trên cây "có nghĩa" (Meier, Schell, ngang/dọc, ảo giác lựa chọn, SDT, động lực người chơi, skill atoms)

### Takeaway
Lựa chọn trên cây chỉ "thú vị" khi có đánh đổi thật, phụ thuộc tình huống, đủ thông tin để hiểu và có phản hồi rõ khi chọn; nhánh chỉ khác nhau vài % chỉ số là lựa chọn danh nghĩa. Về động lực, cây phục vụ cùng lúc nhu cầu competence (thấy mình mạnh lên) và autonomy (tự chọn hướng), và chạm vào ba nhóm người chơi Power, Completion và Strategy/Mastery của Quantic Foundry.

### Cited Findings
**Sid Meier, "Interesting Decisions" (GDC 2012)**
- Câu gốc từ GDC 1989: "a game is a series of interesting decisions"; năm 2012 Meier nói lại và thừa nhận nó không hợp với game nhịp điệu hay puzzle thao tác. Dễ nhận ra cái *không* thú vị: lúc nào cũng chọn phương án đầu trong ba, hoặc chọn bừa — [Game Developer](https://www.gamedeveloper.com/design/gdc-2012-sid-meier-on-how-to-see-games-as-sets-of-interesting-decisions); trang talk: [GDC Vault](https://gdcvault.com/play/1015756/Interesting)
- Các loại quyết định thú vị Meier liệt kê: trade-off (mọi phương án đều tốn một thứ gì đó), situational ("good decisions are situational"), thể hiện lối chơi riêng (thận trọng thì xây phòng thủ, hiếu chiến thì đầu tư tấn công), persistent (ảnh hưởng lâu dài nên phải trình bày cẩn thận), risk/reward, ngắn hạn hay dài hạn (wonder lâu mà bền, chariot nhanh mà nhẹ), mục tiêu nhiều tầng thời gian, customization nhỏ (đặt tên, chọn màu) — [Game Developer](https://www.gamedeveloper.com/design/gdc-2012-sid-meier-on-how-to-see-games-as-sets-of-interesting-decisions)
- Về thông tin: "It's almost worth erring on the side of providing the player with too much information." Về phản hồi: "The worst thing you can do is just move on", chỉ một tiếng động xác nhận cũng có ích — [Game Developer](https://www.gamedeveloper.com/design/gdc-2012-sid-meier-on-how-to-see-games-as-sets-of-interesting-decisions)
- Về nhịp: nhiều quyết định phức tạp liền nhau thì thấy mất kiểm soát, quá ít và quá đơn giản thì chán; Meier bỏ khoảng một phần ba số ý tưởng vì không đủ vui. Các nút chỉnh độ thú vị: tác động, lượng thông tin, giới hạn thời gian, số phương án — [Game Developer](https://www.gamedeveloper.com/design/gdc-2012-sid-meier-on-how-to-see-games-as-sets-of-interesting-decisions)

**Jesse Schell, The Art of Game Design**
- Lens of Meaningful Choices (#32): hỏi người chơi đang được chọn gì, có thật sự quan trọng không, số lượng có vừa không (thêm có thấy quyền lực hơn, bớt có rõ ràng hơn), có chiến lược trội (dominant strategy) không — [Gitbook tóm tắt lens 32](https://gamefroot-developer.gitbooks.io/jesse-schell-the-art-of-game-design-lenses-1-to-1/content/032.html)
- Lens of Triangularity: chọn giữa chơi an toàn lấy thưởng nhỏ và mạo hiểm lấy thưởng lớn, thưởng phải tương xứng rủi ro; trong mục lục sách nó nằm dưới "Balance Type #3: Meaningful Choices". Số thứ tự lens khác nhau giữa các bản (#33 hay #40) — [Gitbook lens 33](https://gamefroot-developer.gitbooks.io/jesse-schell-the-art-of-game-design-lenses-1-to-1/content/033.html); [CIRCA, U. Alberta](https://circa.cs.ualberta.ca/index.php/CIRCA:The_Art_of_Game_Design_-_Jesse_Schell)

**Lars Doucet (2011): cân bằng phương án**
- "If one stands out above the rest, players will always pick it - there's no real choice there." Phương án nên khác về chất chứ không chỉ khác về số; nếu quá giống nhau thì "it doesn't matter what the player picks." Số phương án cùng lúc: "the fewer, the better" — [Game Developer, Doucet](https://www.gamedeveloper.com/design/upgrades-equipment-and-skill-trees)
- Phương án mơ hồ thì "aren't interesting"; khuyên "Kleenex testing" (cho người chưa từng chơi thử) để tìm chỗ khó hiểu — [Game Developer, Doucet](https://www.gamedeveloper.com/design/upgrades-equipment-and-skill-trees)

**Lựa chọn danh nghĩa và ảo giác lựa chọn**
- Cây tốt phải có đánh đổi chứ không phải danh sách nâng cấp kiểu gì cũng mua; nhánh chỉ khác nhau chút chỉ số là "nominal choice" chứ không thể hiện được lối chơi — [Bugnet](https://bugnet.io/blog/how-to-design-a-skill-tree-thats-fun-to-plan) (theo tóm tắt tìm kiếm)
- "Illusion of choice" được dùng như cách tiết kiệm cho studio nhỏ (tạo cảm giác lựa chọn mà không cần hàng trăm kỹ năng khác hẳn nhau), kèm cảnh báo phải pha với lựa chọn thật và minh bạch — [Wayline](https://www.wayline.io/blog/marketing-tutorials-illusion-of-choice-skill-tree) (theo tóm tắt tìm kiếm)
- Embark về cây kỹ năng làm lại của ARC Raiders: "you can't have everything... we believe that creates more interesting choices and supports more playstyles" (câu trích nằm ngay trong tiêu đề bài) — [PC Gamer](https://www.pcgamer.com/games/third-person-shooter/you-cant-have-everything-in-arc-raiders-reworked-skill-tree-we-believe-that-creates-more-interesting-choices-and-supports-more-playstyles/)

**Tiến triển ngang và dọc (horizontal vs vertical)**
- Phần lớn game trộn cả hai; mẫu hay gặp là "vertical for the sense of growth, horizontal to prevent power creep and add strategic depth" — [Game Developer, The Fundamentals of Game Progression](https://gamedeveloper.com/design/the-fundamentals-of-game-progression); [GTSTU](https://gtstu.com/game-progression-system-design-keep-players-hooked/) (theo tóm tắt tìm kiếm)
- Tiến triển ngang không dễ quản lý hơn, và tổng thể có thể kém thoả mãn hơn hẳn — [Massively OP, 2025](https://massivelyop.com/2025/04/03/vague-patch-notes-whats-so-hopeless-about-horizontal-progression-in-mmos/); so sánh nền: [Engadget 2014](https://www.engadget.com/2014-02-05-mmo-mechanics-comparing-vertical-and-horizontal-progression.html) (theo tóm tắt tìm kiếm)

**Self-Determination Theory (SDT)**
- Ryan, Rigby & Przybylski (2006), "The Motivational Pull of Video Games", *Motivation and Emotion*: ba nhu cầu autonomy, competence, relatedness *độc lập* dự báo mức thích thú và việc chơi tiếp. Nghiên cứu 1–3 (chơi 1, 2, 4 game) cho thấy autonomy và competence cảm nhận trong game gắn với mức thích thú, sở thích và thay đổi well-being trước và sau khi chơi; competence và autonomy còn liên quan tới điều khiển trực quan và cảm giác nhập vai — [Springer PDF](https://link.springer.com/content/pdf/10.1007%2Fs11031-006-9051-8.pdf); [DOI](https://www.doi.org/10.1007/S11031-006-9051-8). Lưu ý: số trang trích dẫn lệch giữa các nguồn (344–360 hoặc 347–363).

**Động lực người chơi (Quantic Foundry, thay cho Bartle)**
- Mô hình 12 động lực. *Completion*: săn mọi nhiệm vụ, đồ sưu tầm, chỗ ẩn; là động lực ổn định nhất theo tuổi và cao hơn ở nữ. *Power*: thích bắt đầu yếu rồi mạnh dần qua nâng cấp. Hai cái hay đi chung nhưng có người sưu tầm đồ trang trí mà không cần sức mạnh, và có người thích đạt sức mạnh qua lựa chọn chiến thuật. *Strategy* (nay thuộc cụm "Mastery" cùng "Challenge"): điểm cao thích độ sâu và độ phức tạp; điểm thấp thích "accessible and forgiving when mistakes are made" — [Quantic Foundry Model Reference (PDF)](https://quanticfoundry.com/wp-content/uploads/2019/04/Gamer-Motivation-Model-Reference.pdf); [ironSource LevelUp](https://medium.com/ironsource-levelup/a-closer-look-into-the-12-gamer-motivations-8d156ff0151a) (theo tóm tắt tìm kiếm). Cỡ mẫu nêu khác nhau theo thời điểm (hơn 400.000 ở bài cũ, hơn 2 triệu ở trang mới).

**Daniel Cook: skill atoms, skill chains**
- "The Chemistry of Game Design" (Gamasutra) đưa ra "skill atoms" (vòng hành động, mô phỏng, phản hồi, người chơi học được), "skill chains" và "burnout" — [Game Developer](https://www.gamedeveloper.com/pc/feature-the-chemistry-of-game-design-) (theo tóm tắt tìm kiếm, chưa mở toàn văn)
- Bài học thuật mô tả skill chain là đồ thị có hướng của các skill atom, atom sau được nuôi bằng kỹ năng của atom trước; có phê bình rằng designer thường dựng skill chain theo ý đồ thiết kế mà không kiểm chứng trên người chơi — [AAAI paper](https://cdn.aaai.org/ojs/13040/13040-52-16557-1-2-20201228.pdf); [Horn, Cooper, Deterding](https://eprints.whiterose.ac.uk/120653/1/Horn_Cooper_Deterding_CTAGAMES.pdf) (theo tóm tắt tìm kiếm; chưa đối chiếu câu nào thuộc bài nào)

### Inferences
- Áp Meier vào cây: mỗi nút nên trả lời được "đổi lấy cái gì?". Nút chỉ tăng +x% chỉ số mà ai cũng mua thì không phải quyết định mà là thuế; chỗ cho quyết định nên là nút chọn một trong hai, thứ tự mở nhánh, hoặc nhánh theo hệ hay vai trò.
- SDT gợi ý cây phải cho thấy competence (con số trước và sau, sức mạnh tăng thấy được trong trận) và autonomy (người chơi tự chọn nút, không bị random). Archero cho random nút nâng là ví dụ ngược (mục 2).
- Thoả mãn cả hai nhóm: Completion cần thanh % hoàn thành và mốc rõ; Strategy/Mastery cần vài nút đổi lối chơi thật. Nhóm Strategy thấp cần "forgiving": dễ reset hoặc có đường gợi ý mặc định.
- Trộn ngang và dọc: phần dọc (chỉ số) làm xương sống cho cảm giác mạnh lên; phần ngang (nút chọn, hiệu ứng theo hệ) giữ độ sâu mà không đội trần sức mạnh.

### Gaps
- Chưa mở toàn văn bài Daniel Cook và các bài Lost Garden về progression; nội dung skill atom dựa trên tóm tắt thứ cấp.
- Không tìm và trích nguồn gốc về Bartle (1996). Phân loại người chơi dùng Quantic Foundry thay.
- Không tìm được nghiên cứu thực nghiệm đo riêng tác động của cây kỹ năng lên autonomy và competence; áp SDT vào cây là suy luận.

## 2. GDC talk và bài phân tích chuyên về talent tree / progression (Blizzard, Kongregate, Deconstructor of Fun...)

### Takeaway
Nguồn công khai sâu nhất về thiết kế talent tree là bài triết lý Dragonflight của Blizzard: hai cây class/spec, khoá hàng theo số điểm đã tiêu, nút chọn một trong hai, đưa kỹ năng bắt buộc thành mặc định để không có nút "phải lấy", và giữ tổng sức mạnh ngang bản cũ. Với mobile F2P, bài mổ Archero của Deconstructor of Fun cho bài học trực tiếp: talent random với mức tăng phẳng làm hỏng cảm giác thưởng và tính tự chủ, góp phần gây churn trung và dài hạn.

### Cited Findings
**Blizzard, WoW Dragonflight, triết lý talent (bản preview 2022)**
- Mục tiêu: "increase player agency over your character's progression and build", củng cố gắn bó với class và spec; chọn hình cây vì nó cho thấy đường đi, phụ thuộc và độ lớn mà không cần thêm luật — [Warcraft Secrets (chép bài Blizzard)](https://warcraft-secrets.com/news/world-of-warcraft-dragonflight-talent-system-design-philosophy)
- Muốn có "intuitive paths that lead you to reasonable builds" thay vì bắt người chơi tự làm những lựa chọn rắc rối mới ra được build dùng được — [Warcraft Secrets](https://warcraft-secrets.com/news/world-of-warcraft-dragonflight-talent-system-design-philosophy)
- Hai cây: class tree (kỹ năng lõi chung cho mọi spec, nhiều tiện ích) và spec tree ("predominantly focused on bonuses that enhance your power in your main role"); tách ra để lấy tiện ích không phải hy sinh sức mạnh vai chính — [Warcraft Secrets](https://warcraft-secrets.com/news/world-of-warcraft-dragonflight-talent-system-design-philosophy); thêm tóm tắt: [Laptop Mag, phỏng vấn Ion Hazzikostas](https://www.laptopmag.com/features/wow-dragonflight-game-director-ion-hazzikostas-discusses-new-talent-trees-and-the-fate-of-covenant-abilities)
- Nhịp điểm: bắt đầu ở cấp 10 (class) và 11 (spec) rồi xen kẽ; ở cấp 70 có 31 điểm class và 30 điểm spec. Khoá theo điểm đã tiêu: hàng 5 cần 8 điểm, hàng 8 cần 20 điểm. Mũi tên tiên quyết: phải mua đủ ít nhất một nút trước — [Warcraft Secrets](https://warcraft-secrets.com/news/world-of-warcraft-dragonflight-talent-system-design-philosophy)
- Nút tầng trên "expected to be more commonly chosen"; nút tầng dưới "more optional and more geared towards shaping max-level builds". Nút hình bát giác: chọn một trong hai — [Warcraft Secrets](https://warcraft-secrets.com/news/world-of-warcraft-dragonflight-talent-system-design-philosophy)
- Chống nút bắt buộc: kỹ năng lõi cho cấp 1–10, cho sẵn trong class tree, hoặc đặt đầu spec tree; kỹ năng ai cũng cần (interrupt) đặt ở chỗ "still leaves the rest of your build choices very open". Thừa nhận vẫn có thể ra build rất yếu, nhưng có "guardrails" là các kỹ năng cho sẵn — [Warcraft Secrets](https://warcraft-secrets.com/news/world-of-warcraft-dragonflight-talent-system-design-philosophy)
- Kiểm soát power creep khi thay hệ thống: mục tiêu là nhân vật Dragonflight có sức mạnh và độ phức tạp tương đương nhân vật Shadowlands — [Warcraft Secrets](https://warcraft-secrets.com/news/world-of-warcraft-dragonflight-talent-system-design-philosophy)

**Lars Doucet, "Upgrades, Equipment, and Skill Trees" (Game Developer, 1/4/2011)**
- Defender's Quest: mỗi kỹ năng cần nhân vật đạt cấp tối thiểu và có 3 điểm ở kỹ năng nối trước; khoá như vậy giảm tê liệt vì nhiều lựa chọn lúc đầu và giữ cân bằng; đi sâu một nhánh tốn hơn rải nhiều nhánh nên chuyên sâu là một đánh đổi có chủ ý — [Game Developer](https://www.gamedeveloper.com/design/upgrades-equipment-and-skill-trees)
- Điểm kỹ năng cộng dồn nên "there's no way to entirely 'waste' a skill point", khác trang bị (mua bây giờ hay để dành). Nâng cấp chiến lược thường vĩnh viễn, nâng cấp chiến thuật thường tạm thời — [Game Developer](https://www.gamedeveloper.com/design/upgrades-equipment-and-skill-trees)

**Deconstructor of Fun: Archero (Habby), 2019**
- Bài "How Archero Shot to the Top, and How You Can Do Better" (Michail Katkoff; mổ xẻ bởi Eva Grillova và Abhimanyu Kumar). Talent mua được mỗi lần lên cấp avatar nếu đủ coin; lần mở đầu cho "a significant boost... or access to a fresh new skill", sau đó tăng phẳng (Strength gốc 200, mỗi lần nâng chỉ +100); nút được nâng là random nên "the player has no control over which talent to upgrade"; càng vào dungeon sâu coin vào chậm, lên cấp thưa nên khoảng chờ giữa các lần nâng talent dài ra — [Deconstructor of Fun](http://www.deconstructoroffun.com/blog/2019/8/9/why-archero-banked-25m-but-leaves-25m-hanging-hlx9n)
- Phê bình: mức tăng phẳng cuối game làm việc chờ thấy không đáng; random làm mất tự chủ; meta thành "grindy", gây "medium-long term churn" và rút ngắn đuôi LTV. Đề xuất: thêm % chỉ số toàn cục mỗi lần lên cấp, cân lại độ khó dungeon cho khớp, cho người chơi tự đầu tư coin vào talent mình cần — [Deconstructor of Fun](http://www.deconstructoroffun.com/blog/2019/8/9/why-archero-banked-25m-but-leaves-25m-hanging-hlx9n)
- Bài cho rằng hệ meta có lẽ được thêm vội trong khoảng một tháng soft launch trước global, ít thời gian cân bằng — [Deconstructor of Fun](http://www.deconstructoroffun.com/blog/2019/8/9/why-archero-banked-25m-but-leaves-25m-hanging-hlx9n)

**Deconstructor of Fun: Warcraft Rumble (2023)**
- Khen meta tiến triển leader + troop nhưng chỉ ra đường cong học ban đầu là vấn đề; cần xử lý đường cong học, ưu đãi giữa game và tinh chỉnh tiến trình mở khoá — [Deconstructor of Fun](https://www.deconstructoroffun.com/blog/2023/10/29/deconstructing-warcraft-rumble) (theo tóm tắt tìm kiếm)

**Kongregate (Anthony Pecorella), "Quest for Progress: The Math of Idle Games" (GDC 2016)** — xem số liệu ở mục 3 — [Kongregate blog](https://blog.kongregate.com/quest-for-progress-the-math-of-idle-games); [slide GDC Europe 2016](https://www.slideshare.net/slideshow/quest-for-progress-gdc-europe-2016/65405507)

**Naavik: 4X (Whiteout Survival)** — nền cố định, khác Rise of Kingdoms xây tự do; 4X cộng lõi team battler — [Naavik](https://naavik.co/deep-dives/four-x-evolution-2/) (theo tóm tắt tìm kiếm)

### Inferences
- Cơ chế Dragonflight chuyển thẳng sang mobile được: (a) khoá theo số điểm đã tiêu trong cây thay vì chỉ theo cấp người chơi; (b) nút chọn một trong hai làm chỗ quyết định duy nhất ở mỗi tầng; (c) cái gì ai cũng cần thì cho mặc định, không bắt mua.
- Bài học Archero cho cây trên mobile: cho người chơi chọn nút (autonomy); mức tăng mỗi nút về sau không nên phẳng một cách vô vị. Nên có nút mốc (milestone) đổi lối chơi xen giữa các nút chỉ số; khoảng chờ giữa hai lần nâng không được giãn mãi.

### Gaps
- Không tìm được GDC talk hay bài công khai của Supercell, Playrix, Moon Active, Habby nói *riêng* về skill tree hay talent tree. Các studio này hầu như không công bố tài liệu thiết kế nội bộ về hệ này.
- Chưa mở bài primer Tuts+ "Let's Spec Into Talent Trees" ([link](https://code.tutsplus.com/lets-spec-into-talent-trees-a-primer-for-game-designers--gamedev-6691a)) và dev diary talent tree của MY.GAMES ([link](https://about.my.games/news/295)); có thể bổ sung nếu cần.
- Không có số liệu công khai về retention trước và sau khi thêm talent tree cho bất kỳ game mobile nào.

## 3. Kinh tế F2P: cây làm sink tiền mềm, đường giá, gating, LTV, dữ liệu retention

### Takeaway
Mô hình chuẩn trong game tăng trưởng là giá tăng theo cấp số nhân, lợi ích tăng tuyến tính, nên một đồng tiền mua được ít sức mạnh dần: cây thành sink "không đáy" mà đường sức mạnh vẫn phẳng lại (tiền mềm thực chất "lấy log" của tăng trưởng). Hướng freemium phổ biến: người chơi miễn phí được mọi thứ thiết yếu, tiền thật chỉ mua tốc độ, reset hay tiện lợi. Chưa có số liệu công khai riêng cho "skill tree" trong top-grossing.

### Cited Findings
**Toán đường giá (Kongregate / Anthony Pecorella)**
- Mô hình: cost_next = base × rate^owned; sản lượng tăng tuyến tính theo số sở hữu ("costs grow exponentially while production grows at a linear or polynomial rate"). AdVenture Capitalist, Lemonade Stand: rate 1.07, base cost 4, base production 1.67/s; ví dụ có 10 quầy thì quầy tiếp giá khoảng 7.87, sản lượng 16.7/s — [Kongregate blog](https://blog.kongregate.com/quest-for-progress-the-math-of-idle-games); [Game Developer Part I](https://gamedeveloper.com/design/the-math-of-idle-games-part-i) (theo tóm tắt tìm kiếm)
- Part II dùng giá 5 × 1.1^n (High Schoolers): giá vẫn mũ trong khi tăng trưởng dưới mũ — [Game Developer Part II](https://www.gamedeveloper.com/game-platforms/the-math-of-idle-games-part-ii) (theo tóm tắt tìm kiếm)
- Part III: vì giá nâng cấp tăng theo mũ, tiền tệ thực chất lấy logarit của đường tăng trưởng tổng — [Game Developer Part III](https://gamedeveloper.com/design/the-math-of-idle-games-part-iii) (theo tóm tắt tìm kiếm)

**Gating và trả phí (Adrian Crook, "Skill Tree Design: Ultimate Guide for Freemium Games", 11/10/2025)**
- Bài không có số liệu hay ví dụ game cụ thể, chỉ là khung hướng dẫn. Ba loại rào: level requirement (mốc XP), resource (tiền, gem, skill point), time gate (đồng hồ huấn luyện, giới hạn ngày) — [Adrian Crook](https://adriancrook.com/?p=8095)
- Bảng free và premium: kỹ năng cơ bản thì free đủ, premium mở nhanh hơn; kỹ năng nâng cao thì free bị hạn chế; nhánh đặc biệt thì free được xem trước; reset thì free theo thời gian chờ, premium dùng ngay. Các món bán: skill point, reset token, mở nhánh sớm, accelerator; subscription cho điểm nhanh hơn, reset thường hơn — [Adrian Crook](https://adriancrook.com/?p=8095)
- Nguyên tắc: premium "should add value, not block critical content"; "gameplay equity" (đồ trả phí nên nghiêng về tiện lợi hay trang trí hơn là sức mạnh); có trần hoặc mốc mà mọi người chơi đều tới, bất kể chi tiêu. Đo: tốc độ tiến, điểm rơi rụng, A/B test yêu cầu mở khoá và tốc độ nhận điểm, phân tích cohort theo lần đầu chạm vào cây — [Adrian Crook](https://adriancrook.com/?p=8095)
- Cây theo sự kiện, có thời hạn: kỹ năng riêng sự kiện, khớp hệ tiến triển vĩnh viễn, reset hoặc chuyển đổi khi hết sự kiện — [Adrian Crook](https://adriancrook.com/?p=8095)

**Ví dụ sink trên mobile**
- Archero: coin tiêu vào talent và nâng cấp đồ (đồ cần thêm scroll); talent khoá theo cấp avatar; bài không nêu số coin cụ thể — [Deconstructor of Fun](http://www.deconstructoroffun.com/blog/2019/8/9/why-archero-banked-25m-but-leaves-25m-hanging-hlx9n)
- Whiteout Survival: Research Center có các nhánh Growth, Economy, Battle; càng lên cao tài nguyên và thời gian mỗi dự án tăng mạnh, kinh tế yếu thì nghiên cứu sẽ tắc — [BlueStacks guide](https://www.bluestacks.com/blog/game-guides/white-out-survival/wos-research-center-guide-en.html) (theo tóm tắt tìm kiếm). Bài review cho rằng gần như mọi hệ chiến lược đều bọc trong đồng hồ chờ, kinh tế xây quanh áp lực "pay-to-progress", bán speedup — [Orcz review](https://orcz.com/whiteout-survival-review-strategy-survival-and-the-tyranny-of-the-timer/) (theo tóm tắt tìm kiếm; nguồn ý kiến)

**Dữ liệu tính năng top-grossing (GameRefinery)**
- Không tìm được tỉ lệ dùng "skill tree"/"talents" trong top-grossing. Số liệu lân cận (theo tóm tắt tìm kiếm, cách gán số nào cho trang nào chưa xác minh): gacha có ở 58% top-100 grossing iOS Mỹ; battle pass khoảng 60% top-grossing iOS Mỹ, so với 14% ở nhóm ngoài top 20%; guild 54% và skin trang trí 44% ở top 20% grossing Mỹ; thị trường đang chuyển sang "meta-heavier" và phải rất cẩn thận khi động vào meta — [GameRefinery: Back to the Features](https://www.gamerefinery.com/mobile-game-features/); [GameRefinery infograph top 100](https://www.gamerefinery.com/infograph-top-100-grossing-others-not/); [PocketGamer.biz: battle pass](https://www.pocketgamer.biz/gamerefinery-battle-pass-implementation-in-top-grossing-mobile-games/)
- Bản tin GameRefinery tháng 5/2025 có nhắc mở khoá kỹ năng khi nâng nhân vật trong Squad Busters (không rõ chi tiết) — [GameRefinery May 2025](https://www.gamerefinery.com/mobile-game-market-review-may-2025/) (theo tóm tắt tìm kiếm)

### Inferences
- Phép tính nhanh cho đường giá cost_n = base × r^(n−1):
  - Số cấp để giá gấp đôi = ln2 / ln r: r = 1.07 khoảng 10.2 cấp; r = 1.10 khoảng 7.3 cấp; r = 1.15 khoảng 5.0 cấp.
  - Tổng giá n cấp = base × (r^n − 1)/(r − 1). Ví dụ r = 1.07, n = 50: 1.07^50 ≈ 29.5, tổng ≈ 406 × base; cấp cuối ≈ 27.5 × base, tức chỉ khoảng 7% tổng. Đường mũ dồn phần lớn chi phí vào nửa sau.
  - Áp vào thiết kế: chọn r sao cho thời gian kiếm đủ tiền cho nút kế tiếp tăng chậm hơn thu nhập theo ngày (thu nhập tiền mềm cũng tăng theo tiến độ ải), để khoảng chờ giữa hai lần nâng ổn định, tránh lỗi Archero (chờ giãn mãi).
- Lợi ích tuyến tính + giá mũ tự kìm power creep: sức mạnh từ cây tăng theo log tiền đã tiêu, nên dồn tiền vào cây không làm vỡ cân bằng ải PvE nếu tổng lợi ích tối đa của cây có trần biết trước.
- Với game không bán sức mạnh trực tiếp: tiền thật nên chỉ mua tốc độ (đẩy nhanh thu tiền mềm) hoặc reset, không mua nút riêng trả phí, đúng "gameplay equity" của Crook.
- Cây là "mục tiêu dài hạn nhìn thấy được": thanh % hoàn thành và nút đắt kế tiếp hiện rõ tạo lý do quay lại (session goal: "còn X coin nữa là mở nút Y").

### Gaps
- Không có số liệu công khai về tác động của talent tree lên D1/D7/D30 hay LTV cho bất kỳ game mobile cụ thể nào.
- Không tìm được tỉ lệ game top-grossing có skill tree từ GameRefinery hay Sensor Tower.
- Hệ số 1.15 hay được nhắc (vd. Cookie Clicker, Exponential Idle) chưa xác minh được trang gốc nên không ghi thành dữ kiện.
- Không có số liệu chuẩn về tỉ lệ tiền mềm nên dồn vào cây so với các sink khác (nâng tướng, trang bị...).

## 4. Respec: miễn phí, trả phí hay giới hạn; cách game mobile làm; cảm nhận người chơi

### Takeaway
Xu hướng gần đây nghiêng hẳn về respec rẻ hoặc miễn phí (Diablo Immortal bỏ giới hạn 7 ngày và gộp build vào loadout; Diablo IV respec không giới hạn, có phí nhưng hứa "không quá đắt"). Lý lẽ giữ phí là để quyết định có trọng lượng, nhưng phí cao làm người chơi ngừng thử nghiệm và tăng ma sát. Mô hình freemium thường thấy: free có reset theo thời gian chờ hoặc token kiếm được, trả phí thì reset ngay.

### Cited Findings
- Blizzard với Diablo IV: respec không giới hạn nhưng không miễn phí; đầu game miễn phí, giá tăng theo cấp, trả bằng vàng trong game; Rod Fergusson hứa respec sẽ không "prohibitively expensive" — [PC Gamer](https://pcgamer.com/diablo-4-boss-has-reassuring-words-for-buildcrafters-respeccing-wont-be-prohibitively-expensive); bài phản biện: [Laptop Mag](https://laptopmag.com/news/diablo-4-lets-you-respec-at-a-cost-heres-why-thats-a-problem-in-games) (theo tóm tắt tìm kiếm)
- Diablo Immortal (mobile F2P): các hướng dẫn cũ ghi reset Paragon miễn phí 7 ngày một lần; GameSpot đưa tin Blizzard bỏ timer 7 ngày và đưa build Paragon vào Armory loadout đã lưu. Đổi class miễn phí 7 ngày một lần, đổi class thì cây Paragon cũng reset — [GameSpot](https://Gamespot.com/articles/diablo-immortal-is-improving-rewards-for-premium-battle-pass-owners/1100-6513126/); [Fextralife wiki](https://diabloimmortal.wiki.fextralife.com/Paragon+Trees); [Gameranx class change](https://gameranx.com/features/id/327772/article/diablo-immortal-everything-you-need-to-know-about-class-change/) (theo tóm tắt tìm kiếm; ngày bỏ timer chưa xác minh)
- Rise of Kingdoms: bản Talent Tree 2.0 (2018) reset talent mọi commander và trả lại điểm; cộng đồng làm công cụ lập kế hoạch talent ngoài game để khỏi phải reset trong game — [AppGamer](https://www.appgamer.com/talent-tree-2-0-update); [rok-talents (GitHub)](https://awesome.ecosyste.ms/projects/github.com%2Fthesimonho%2Frok-talents) (theo tóm tắt tìm kiếm). Thông tin về token reset miễn phí chỉ có từ trang bán gem nên không dùng.
- Người chơi (Last Epoch forum) muốn reset miễn phí sau mỗi patch lớn "like PoE does"; phí lớn chỉ làm tăng ma sát và đẩy người chơi đi — [Last Epoch forum](https://forum.lastepoch.com/t/costs-to-respeccing-insta-kill-mechanics-are-a-bad-idea/47372/7) (theo tóm tắt tìm kiếm; ý kiến cộng đồng)
- Lập luận giữ phí: respec miễn phí và tức thì thì lựa chọn build không còn trọng lượng; quá dễ thì người chơi bớt suy nghĩ. Phương án giữa: respec giới hạn, "free respec coupon every 10 levels", một lần reset toàn bộ sau thay đổi cân bằng lớn. Một hướng dẫn kể phí respec ban đầu cao tới mức người chơi bỏ hẳn tính năng; giảm nhẹ phí thì mức hài lòng và thử nghiệm tăng rõ — [Bugnet: how to design a respec system](https://bugnet.io/blog/how-to-design-a-respec-system); [Wayline](https://www.wayline.io/blog/respec-your-game-respecing-without-restarting) (theo tóm tắt tìm kiếm; giai thoại, không có số liệu)
- Bài báo chung: năm 2023 respec trong RPG một người chơi vẫn phiền — [PC Gamer](https://www.pcgamer.com/for-the-love-of-all-that-is-holy-its-2023why-is-it-still-so-annoying-to-respec-in-singleplayer-rpgs) (theo tóm tắt tìm kiếm)
- Freemium (Crook): reset token là món bán; free reset theo thời gian chờ, premium dùng ngay; subscription cho reset thường hơn — [Adrian Crook](https://adriancrook.com/?p=8095)
- Doucet (2011) coi điểm là vĩnh viễn ("once you assign a point it's spent forever"), không bàn hệ quả của respec — [Game Developer](https://www.gamedeveloper.com/design/upgrades-equipment-and-skill-trees)

### Inferences
- Khi cây chủ yếu là sink chỉ số (mua hết dần theo thời gian), respec ít giá trị; respec chỉ cần cho các nút chọn (choice node). Có thể cho đổi nút chọn miễn phí hoặc rẻ, còn các nút chỉ số không có gì để hoàn lại.
- Nếu cây có nhánh theo hệ hay vai trò mà người chơi phải chọn thứ tự đầu tư: hoàn 100% tiền khi reset (vì tiền đã tiêu là nỗ lực thật) cộng một phí nhỏ hoặc thời gian chờ, và miễn phí sau mỗi lần cân bằng lại.
- Bán reset bằng tiền thật dễ bị coi là "phạt người thử nghiệm"; nếu bán thì nên có kênh free song song (token từ nhiệm vụ hoặc sự kiện).

### Gaps
- Không có số liệu A/B công khai về tác động của chính sách respec lên retention hay doanh thu ở game mobile.
- Chưa xác minh chính sách reset hiện tại của Rise of Kingdoms và thời điểm Diablo Immortal bỏ timer từ nguồn chính thức.

## 5. UX/UI cây trên mobile: bố cục dọc, số nút mỗi màn, đọc số, xem trước, nút "kế tiếp", chấm đỏ, nâng một chạm, FTUE

### Takeaway
Gần như không có tài liệu công khai đáng tin về bố cục cây kỹ năng dọc trên mobile (hướng cuộn, cỡ nút, số nút mỗi màn). Nguyên tắc dùng được đến từ UX mobile chung (vùng ngón cái, panel chi tiết), từ Meier và Doucet (thông tin rõ, phản hồi, ít phương án cùng lúc), và từ UX badge (chấm đỏ dùng tràn lan gây "badge blindness"). Phần lớn khuyến nghị cụ thể ở đây là suy luận.

### Cited Findings
- Màn dọc hợp chơi một tay bằng ngón cái; nút cần bấm nhanh không nên đặt góc trên trái — [RocketBrush](https://rocketbrush.com/game-art/game-ui-design-mobile); [Epicstream](https://epicstream.com/article/mobile-slot-ux-guide-portrait-mode-thumb-friendly-controls-and-animation-overload) (theo tóm tắt tìm kiếm)
- Điện thoại thường dọc, tablet thường ngang; bố cục cố định sẽ gãy một bên, cần neo co giãn (anchor) — [Unity blog: Mobile UI design best practices](https://blog.unity.com/en/games/mobile-ui-design-best-practices-part-1) (theo tóm tắt tìm kiếm; gán nguồn chưa chắc)
- Mẫu hay gặp: cây dạng nút; chọn nút thì hiện cửa sổ thông tin kỹ năng ở góc; chuyển cảnh mượt và phát sáng nhẹ để rõ đang chọn và vừa nâng — [itch.io devlog](https://itch.io/post/12538063) (theo tóm tắt tìm kiếm; nguồn indie)
- Bố cục cây theo Crook: linear (dạy kỹ năng lõi cho người mới), branching, hybrid (gốc tuyến tính rồi rẽ nhánh), web (nhiều tiên quyết, cho người chơi sâu) — [Adrian Crook](https://adriancrook.com/?p=8095)
- Hình cây truyền đạt đường đi, phụ thuộc và độ lớn mà không cần thêm luật; mũi tên tiên quyết; hình nút khác nhau cho nút chọn (bát giác) — [Warcraft Secrets / Blizzard](https://warcraft-secrets.com/news/world-of-warcraft-dragonflight-talent-system-design-philosophy)
- Thông tin và phản hồi: thà thừa thông tin; ghi nhận ngay mỗi quyết định (âm thanh, chữ, hình) — [Game Developer, Meier](https://www.gamedeveloper.com/design/gdc-2012-sid-meier-on-how-to-see-games-as-sets-of-interesting-decisions)
- Badge và chấm đỏ: gắn badge lên mọi thứ làm người dùng ngợp và mất tác dụng; badge thường trực gây "badge blindness"; vendor đề xuất badge tối màu ít xâm phạm hơn — [Mobbin](https://mobbin.com/glossary/badge); [Gravitec](https://gravitec.net/blog/?p=3708); [Braze](https://www.braze.com/resources/articles/beware-red-dot-badging) (nguồn vendor, cẩn trọng). Bài ý kiến ước khoảng 50-50 khả năng chấm đỏ là thứ "thật" — [The Week](https://theweek.com/articles/816655/scourge-overeager-notifications). Góc văn hoá: ở UI game Trung Quốc, chấm đỏ dày được đọc là hoạt động hay phần thưởng chứ không bị xem là spam — [LinkedIn post](https://pt.linkedin.com/in/alenakulikova13) (nguồn yếu)
- Đường cong học là điểm yếu của meta Warcraft Rumble — [Deconstructor of Fun](https://www.deconstructoroffun.com/blog/2023/10/29/deconstructing-warcraft-rumble) (theo tóm tắt tìm kiếm)
- Gating theo cấp giảm tê liệt lựa chọn lúc đầu — [Game Developer, Doucet](https://www.gamedeveloper.com/design/upgrades-equipment-and-skill-trees)

### Inferences (chưa có nguồn trực tiếp, là đề xuất)
- **Hình cây cho màn dọc:** cây mọc theo trục dọc (cuộn dọc một chiều, không zoom/pan tự do), tối đa khoảng 3 cột hay nhánh vừa bề ngang điện thoại để nút đủ lớn cho ngón tay; tránh dạng web hay toả tròn cần pan hai chiều. Cây dài thì chia trang theo tầng hoặc chương, kèm thanh tiến độ, thay vì một bản đồ khổng lồ.
- **Panel chi tiết ở đáy** (vùng ngón cái): tên nút, hiệu ứng ghi số "trước → sau" (vd. "Công +4% → +6%"), giá và số tiền đang có, nút nâng lớn. Nút chọn một trong hai thì đặt hai thẻ cạnh nhau để so.
- **Nút "kế tiếp":** tự cuộn tới và làm nổi nút rẻ nhất đang mua được, hoặc nút tiếp theo trên đường gợi ý; có "nâng một chạm" hoặc giữ để nâng liên tục cho các nút chỉ số nhiều cấp.
- **Chấm đỏ:** chỉ hiện khi đủ tiền mua ít nhất một nút *và* nút đó chưa từng được báo; không treo chấm đỏ thường trực chỉ vì "còn nút chưa mua". Lý do: badge blindness.
- **Hiển thị tổng:** thanh % hoàn thành cây (cho nhóm Completion), tổng chỉ số cây đang cho (cho nhóm Power), mốc phần thưởng ở 25/50/75/100%.
- **FTUE:** mở cây sau khi người chơi đã hiểu vòng trận và đã có tiền mềm; bước đầu ép bấm một nút rẻ có hiệu ứng thấy ngay trong trận kế tiếp; các nhánh và nút chọn mở dần (đúng gợi ý "linear trước, branching sau" của Crook).
- **Khả năng tiếp cận:** không chỉ dùng màu để phân biệt trạng thái (khoá, mua được, đã mua); thêm biểu tượng ổ khoá, dấu tích, viền; chữ số hiệu ứng đủ to.

### Gaps
- Không tìm được nghiên cứu UX hay case study công khai về bố cục talent tree dọc trên mobile (hướng cuộn, cỡ chạm, số nút mỗi màn).
- Không có dữ liệu về tác động của chấm đỏ lên tỉ lệ tương tác với cây trong game mobile; nguồn badge chủ yếu là vendor marketing hoặc app phi game.
- Không có nguồn về khả năng tiếp cận (accessibility) riêng cho cây kỹ năng.

## 6. Lỗi thường gặp: nút % bắt buộc, nút bẫy, quá nhiều nút nhỏ, giá trị mơ hồ, gating ẩn, cây quá to, power creep phá cân bằng ải PvE

### Takeaway
Các lỗi được ghi nhận nhiều nhất: phương án trội làm lựa chọn thành hiển nhiên; nút thiết yếu bị đặt thành "thuế bắt buộc"; nút chỉ khác vài % (lựa chọn danh nghĩa); mức tăng phẳng và random (Archero) làm việc chờ vô nghĩa; build yếu không có rào chắn; quá nhiều phương án cùng lúc; đường cong học quá dốc. Power creep thường được trị bằng giữ tổng sức mạnh hệ mới ngang hệ cũ, giá mũ với lợi ích tuyến tính, và chuyển phần mở rộng sang tiến triển ngang.

### Cited Findings
- **Phương án trội:** "If one stands out above the rest, players will always pick it - there's no real choice there." Phương án quá giống nhau thì chọn gì cũng như nhau — [Game Developer, Doucet](https://www.gamedeveloper.com/design/upgrades-equipment-and-skill-trees); Schell yêu cầu soát dominant strategy — [Lens 32](https://gamefroot-developer.gitbooks.io/jesse-schell-the-art-of-game-design-lenses-1-to-1/content/032.html)
- **Nút bắt buộc:** Blizzard chuyển kỹ năng lõi thành mặc định hoặc đặt đầu cây, và đặt kỹ năng ai cũng cần ở chỗ không bó các lựa chọn khác — [Warcraft Secrets / Blizzard](https://warcraft-secrets.com/news/world-of-warcraft-dragonflight-talent-system-design-philosophy)
- **Build bẫy:** Blizzard thừa nhận vẫn ra được build rất yếu, dựa vào "guardrails"; mục tiêu là "intuitive paths that lead you to reasonable builds" — [Warcraft Secrets / Blizzard](https://warcraft-secrets.com/news/world-of-warcraft-dragonflight-talent-system-design-philosophy)
- **Lựa chọn danh nghĩa:** nhánh chỉ khác chút chỉ số thì không thể hiện được lối chơi — [Bugnet](https://bugnet.io/blog/how-to-design-a-skill-tree-thats-fun-to-plan) (theo tóm tắt tìm kiếm)
- **Mức tăng phẳng, random, chờ giãn dài:** Archero (+100 phẳng, nút random, chờ dài dần), dẫn tới churn trung và dài hạn — [Deconstructor of Fun](http://www.deconstructoroffun.com/blog/2019/8/9/why-archero-banked-25m-but-leaves-25m-hanging-hlx9n)
- **Quá nhiều lựa chọn hay quá phức tạp:** "the fewer, the better" — [Doucet](https://www.gamedeveloper.com/design/upgrades-equipment-and-skill-trees); nhiều quyết định phức tạp liền nhau làm mất kiểm soát — [Meier](https://www.gamedeveloper.com/design/gdc-2012-sid-meier-on-how-to-see-games-as-sets-of-interesting-decisions); cho người chơi phương án vô dụng hoặc quá nhiều phương án thiếu ngữ cảnh làm hại trải nghiệm — [gamedev.net forum](https://gamedev.net/forums/topic/602884-horizontal-growth-vs-vertical-growth/4816050/) (theo tóm tắt tìm kiếm; forum)
- **Giá trị mơ hồ:** lựa chọn không rõ thì "aren't interesting"; test bằng người mới — [Doucet](https://www.gamedeveloper.com/design/upgrades-equipment-and-skill-trees)
- **Rào thời gian và pay-to-progress:** cây nghiên cứu 4X bị phê bình vì mọi thứ bọc trong timer và áp lực trả tiền — [Orcz review Whiteout Survival](https://orcz.com/whiteout-survival-review-strategy-survival-and-the-tyranny-of-the-timer/) (nguồn ý kiến)
- **Trả phí lấn sức mạnh:** premium không được "block critical content"; nên có trần hoặc mốc mà mọi người chơi đều tới — [Adrian Crook](https://adriancrook.com/?p=8095)
- **Power creep:** được xem là vấn đề dài hạn nguy hiểm nhất, nội dung mới làm đường cũ mất giá trị; tiến triển ngang chỉ giảm power creep khi các phương án khác nhau thật — [GTSTU](https://gtstu.com/game-progression-system-design-keep-players-hooked/); [Massively OP 2025](https://massivelyop.com/2025/07/03/massively-overthinking-is-vertical-progression-still-sustainable-for-mmos/) (theo tóm tắt tìm kiếm). Blizzard giữ tổng sức mạnh hệ talent mới ngang hệ cũ — [Warcraft Secrets](https://warcraft-secrets.com/news/world-of-warcraft-dragonflight-talent-system-design-philosophy)
- **Thêm meta vội, cân bằng kém:** Archero có lẽ thêm hệ meta trong khoảng một tháng soft launch — [Deconstructor of Fun](http://www.deconstructoroffun.com/blog/2019/8/9/why-archero-banked-25m-but-leaves-25m-hanging-hlx9n)

### Inferences
- **Ngân sách sức mạnh của cây:** đặt trước tổng % sức mạnh tối đa cây được phép cho (vd. cây đầy = +X% chỉ số đội), rồi chỉnh độ khó ải PvE theo mức cây *dự kiến* ở từng mốc ngày chơi. Như vậy cây là một phần của đường cong cân bằng chứ không phải lớp cộng thêm phá ải.
- **Tránh nút % bắt buộc:** gộp các nút +1% lẻ thành ít nút lớn có cấp (một nút 10 cấp thay vì 10 nút), xen nút mốc đổi lối chơi; nút nào ai cũng mua thì cân nhắc cho mặc định hoặc gộp vào đường chính.
- **Gating ẩn:** mọi điều kiện khoá (cấp người chơi, ải, số điểm đã tiêu trong cây) phải hiện trên nút khoá ("Mở ở ải 30" / "Cần 8 điểm trong nhánh"), không để người chơi tự đoán.
- **Cây quá to:** với mobile dọc nên chia cây theo chương hay tầng, mở dần, để màn đầu luôn nắm được trong tầm mắt.

### Gaps
- Không có số liệu định lượng (A/B, telemetry công khai) về tác hại của từng lỗi (vd. nút % bắt buộc làm tụt tương tác bao nhiêu).
- Không có nguồn mobile cụ thể đo power creep do cây gây ra ở game PvE nhiều ải; phần ngân sách sức mạnh là suy luận.
