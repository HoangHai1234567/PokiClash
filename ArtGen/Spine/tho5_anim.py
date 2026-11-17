# -*- coding: utf-8 -*-
"""Năm tướng đầu đảo Thổ: ĐỀ XUẤT animation (Claude, 2026-11-17). Người dùng: "dựa vào bộ skill anim và vfx, tự sáng tạo các animation cần
thiết dựa trên con gốc". Chỉ là bản đề xuất chờ người dùng duyệt; chưa dựng rig.

Theo skill-petclash: idle 2 s lặp có điểm phá nhịp, attack 0,8–1,1 s trúng 0,4–0,55 s, cast ~1,2 s, skill 1,6–2,4 s; lấy đà ngược chiều,
khựng lúc chạm; hình hệ Thổ = khối đá góc cạnh trồi lên, rơi nặng nảy một lần, bụi tròn, sỏi (mục 5). Độ mạnh leo theo ải
(memory combat-epic-theo-do-kho). Mỗi con một kiểu đòn khác nhau. Rig không vẽ VFX (đạn, cột đá, lốc là lớp hạt trên sân); mảnh của rig bay tới
đối thủ rồi về thì code lái (xương far / fly_*).

    tho5_anim.py xem     trang so: concept + clip gốc (tờ khung) cạnh từng clip đề xuất → inbox/tho5_xem_anim.html
"""
import html
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SXS = r"D:\Ripper\SwordxStaff\scan"

# mỗi clip: (tên clip game, dài s, clip gốc làm nguồn hoặc None, diễn, VFX, ghi chú rig / code)
ANIM = {
    "cong_da": dict(ten="Tatu mai đá", ai=1, muc="nhẹ nhất (tướng khởi đầu)", mon="monster_3378", clips=[
        ("appear", 1.5, None,
         "Chỉ thấy cái MAI ĐÁ rơi phịch xuống sân, nảy một lần, nằm im → mõm thò ra hít hít → bốn chân, đuôi bật ra, lắc mình rũ bụi, cau mày nhìn đối thủ.",
         "bụi tròn lúc chạm đất, vài viên sỏi lăn ra.",
         "thân co dẹt dưới mai (tỉ lệ xương thân), mặt và chân giấu; sự kiện cham_dat, bung."),
        ("idle", 2.0, "idle_01",
         "Thở nhún; mai trễ nửa nhịp so với thân; ba viên sỏi ở mép mai nảy lệch pha; cụm hổ phách rung nhẹ. Điểm phá nhịp ~1,3 s: hít hít mõm rồi hắt xì ra một hơi bụi.",
         "1–2 hạt bụi rơi khi nhún; một phụt bụi nhỏ lúc hắt xì.", "giữ chu kỳ 2 s của họ."),
        ("walk", 0.47, "run_01", "Lon ton, mai nảy theo bước, sỏi lắc.", "—", ""),
        ("attack", 0.93, "skill_01_1",
         "Lùi mông lấy đà 0,2 s → phóng tới HÚC ĐẦU (trúng ~0,42 s), sỏi trên mai văng tới trước rồi rơi về chỗ như clip của họ; nén giãn (0,9; 1,09) lúc chạm.",
         "mức nhẹ: chớp sao gai kem, 4–6 dăm đá, bụi.", ""),
        ("cast", 1.2, "skill_02",
         "Nhún, bật lên, giữa không trung LẮC MAI thật mạnh như chó rũ nước → sỏi văng ra một chùm về phía đối thủ; đáp phịch.",
         "chùm 6–8 viên sỏi bay vòng cung tới đối thủ, trúng lả tả, bụi.", "sỏi của rig chỉ nảy lên rồi về; sỏi bay là hạt; sự kiện ran (lắc), ban."),
        ("skill", 1.9, "skill_02 kéo dài",
         "Rụt vào mai (thân co dẹt), mai rung lạch cạch 0,5 s, sỏi bật nảy (gồng) → hốc hổ phách trên đỉnh BẮN một loạt pha lê lên trời → đứng dậy, chĩa mõm về đối thủ → MƯA PHA LÊ HỔ PHÁCH rơi xuống người nó, mảnh cuối to nhất cắm xuống đất.",
         "pha lê bay vút lên rồi rơi chéo xuống chỗ đối thủ, mỗi mảnh vỡ thành dăm vàng + bụi; mức nặng (rung 0,5).",
         "rig: cụm pha lê bung lên (tỉ lệ) rồi về; sự kiện gong, ban_troi, mua."),
        ("hit", 0.5, "hit_01", "Mai lạch cạch, sỏi nảy, mặt nhăn.", "dăm đá nhỏ.", ""),
        ("die", 1.2, "die_01",
         "Rụt vào mai, lật ngửa, mai nứt toác, sỏi văng, mờ dần.", "bụi, vài mảnh đá bay lên rồi tan.", "khung cuối trống."),
    ]),
    "than_lan_cat": dict(ten="Thằn lằn áo choàng đất nung", ai=5, muc="nhẹ", mon="monster_3257", clips=[
        ("appear", 1.6, None,
         "Một gò cát nhô lên, rung rung → hai chân trước thò ra BẤU mép gò (điểm tựa), kéo đầu đội mũ giáp và thân trồi lên, rũ cát; áo choàng phiến đất nung bật mở một lần rồi xếp lại.",
         "gò cát, cát trào ra hai bên, hạt cát rơi.", "chân trước bám chỗ cố định trong lúc thân được kéo lên (dong-tac-co-diem-tua)."),
        ("idle", 2.0, "idle_01",
         "Thở; các phiến áo choàng phập phồng so le từ phiến gần đầu ra ngoài; họng phập phồng; đuôi cuộn chậm. Phá nhịp: chớp mắt chậm rồi THÈ LƯỠI LIẾM MẮT (trò của thằn lằn).",
         "1–2 hạt cát rơi khỏi áo choàng.", "idle gốc 4 s: lấy một vòng 2 s."),
        ("walk", 0.8, "run_01", "Bò lạch bạch, áo choàng nảy so le.", "—", ""),
        ("attack", 1.0, "skill_01",
         "Chồm lên lấy đà → phóng mình rạp sát đất ĐỚP (hàm nanh mở to, lưỡi quất), trúng ~0,56 s, giữ dáng rạp rồi lùi về.",
         "mức nhẹ: hai cung vết cắn kem, cát văng.", "lưỡi `P_shetou` của họ dùng lại."),
        ("cast", 1.4, "skill_02",
         "Áo choàng xoè bung từng phiến (so le 0,05 s) như mũ trùm, há miệng rít → BA PHIẾN ĐẤT NUNG rời áo bay vút tới đối thủ như phi tiêu, găm vào, rồi bay về lắp đúng chỗ trên áo.",
         "vệt bụi sau mỗi phiến, mảnh gốm vỡ lúc găm.", "phiến bay là mảnh của rig: code lái tới đối thủ (fly_* / far), anim lo đoạn lắp về (vat-bay-trung-dich-bang-code)."),
        ("skill", 2.0, "skill_02 + dậm",
         "Áo choàng xoè to nhất, nhổm cao, đập hai chân trước xuống đất → LỐC CÁT cuộn lên trùm lấy đối thủ, bên trong có mảnh đất nung xoay; thằn lằn giữ dáng mũ trùm rít tới khi lốc tan.",
         "lốc cát (mảng liền các vòng dẹt lắc lệch pha + hạt cát, mảnh gốm), bụi tan dài; mức nặng.", "sự kiện dam, het; giữ dáng tới khi lốc gần tan."),
        ("hit", 0.5, "hit_01", "Áo choàng giật lệch, nhăn mặt.", "cát văng.", ""),
        ("die", 1.2, "die_01", "Các phiến áo choàng rơi lả tả từng mảnh, thằn lằn nằm bẹp, mờ dần.", "bụi cát.", ""),
    ]),
    "thu_da": dict(ten="Cóc tê giác pha lê", ai=10, muc="vừa", mon="monster_3525", clips=[
        ("appear", 1.6, None,
         "Một TẢNG ĐÁ cuộn tròn (con cóc cuộn mình, cụm pha lê lộ ra) lăn vào từ mép sân, nảy một lần, bung ra đứng, khịt mũi, cụm pha lê dựng lên.",
         "bụi theo vệt lăn, bụi tròn lúc nảy.", "cần một ảnh riêng 'cuộn tròn' (dang-kho-gen-anh-rieng), đổi ảnh trong clip như họ làm ở skill_03."),
        ("idle", 2.0, "idle_01",
         "Thở nặng, TÚI HỌNG phập phồng (cóc), hàm nhai; cụm pha lê rung trễ pha. Phá nhịp: dậm một chân trước, khịt hai luồng bụi từ mũi.",
         "bụi rơi khi dậm, hai phụt bụi ở mũi.", "idle gốc 7,67 s: cắt một vòng 2 s."),
        ("walk", 0.73, "run_01", "Ì ạch nặng nề, bụi nhỏ mỗi bước.", "bụi chân.", ""),
        ("attack", 1.07, "skill_01_1",
         "Chồm nửa thân trước lên, nhấc chân gần → GIÁNG SỪNG và cằm xuống đất (trúng ~0,47 s), nảy nhẹ một lần.",
         "mức vừa: chớp, đá văng, vết nứt nhỏ, bụi tròn.", ""),
        ("cast", 1.3, "skill_02_1",
         "Há hàm thật rộng, trong miệng tụ một cục đá → PHUN TẢNG ĐÁ bay vòng cung, vỡ tung trên người đối thủ; giật đầu về sau lúc phun.",
         "tụ: bụi xoáy hút vào miệng; đạn đá có đuôi bụi; vỡ: đá vụn, dăm pha lê, bụi.", "xương `mieng` ở miệng; sự kiện tu, phun."),
        ("skill", 2.3, "skill_03",
         "Co mình → đổi sang ảnh CUỘN TRÒN, xoay tại chỗ tóe bụi (gồng 0,5 s) → lăn bật tới đối thủ theo cung, NỆN vào nó → nảy về chỗ, bung ra đứng, lắc đầu.",
         "vệt bụi lăn, nện: pha lê vỡ toé vòng, vòng sóng đất, đá rơi; mức nặng.", "thân đi tới đối thủ như cú lao (sân nắn quãng, lunge)."),
        ("hit", 0.5, "hit_01", "Thân nặng giật lùi ít, pha lê rung.", "dăm đá.", ""),
        ("die", 1.3, "die_01", "Lật ngửa, chân đạp vài cái, pha lê rụng lăn ra, mờ dần.", "bụi, dăm pha lê.", ""),
    ]),
    "rong_cat": dict(ten="Rồng giáp sa thạch", ai=15, muc="nặng", mon="monster_3424", clips=[
        ("appear", 1.8, None,
         "Mặt đất nứt, MỘT VUỐT đâm lên bấu đất, rồi vuốt kia, kéo cả thân trồi lên (điểm tựa giữ yên), rũ cát khỏi giáp, ngẩng đầu GẦM.",
         "đất nứt, đất nổ tung, cát rơi, bụi tròn.", "vuốt bám chỗ cố định khi thân được kéo lên."),
        ("idle", 2.67, "idle_01",
         "Thân lắc vòng như thú săn rình mồi, đầu giữ yên nhìn đối thủ, đuôi quất chậm trễ pha, giáp vai nảy nhẹ. Phá nhịp: CÀO ĐẤT bằng vuốt trước (cát văng) rồi thè lưỡi.",
         "cát văng lúc cào, 1–2 sỏi rơi khỏi giáp.", "giữ chu kỳ của họ."),
        ("walk", 0.67, "run_01", "Bò rình, đầu thấp.", "—", ""),
        ("attack", 1.0, "skill_01",
         "Đứng lên chân sau, vuốt gần giơ cao → CHÉM chéo xuống (trúng ~0,44 s), quá đà rồi về.",
         "mức vừa–nặng: ba vệt vuốt màu cát, dăm đá, bụi.", ""),
        ("cast", 1.3, "skill_02",
         "Đứng dậy dang hai tay → hai vuốt chém chéo vào không khí → BA LƯỠI CÁT TRĂNG KHUYẾT bay tới đối thủ, trúng so le.",
         "lưỡi cát liền (mảng trăng khuyết, mép trước sắc), vệt mờ, sỏi; trúng: vết chém + cát toé.", "công thức lưỡi của bộ Thủy đổi sang cát."),
        ("skill", 2.2, "skill_03 kéo dài",
         "Đứng thẳng, giơ hai tay gồng (hai dáng lệch 2–3° đổi nhau, đá vụn rơi khỏi giáp, sừng hổ phách loé) → NỆN hai vuốt xuống đất → khe nứt lan tới đối thủ → CỘT SA THẠCH trồi lên quanh nó ba nhịp, nhịp cuối cột to nhất hất tung, đá rơi như mưa.",
         "nứt đất, cột đá (mảng liền) trồi rồi lún, đá rơi nảy một lần, bụi tan dài; mức tuyệt kỹ.", "giáp lưng bật lên rồi về như họ (0,74 s); sự kiện gong, nen, cot1..3."),
        ("hit", 0.5, "hit_01", "Giật lùi, giáp rung.", "dăm đá.", ""),
        ("die", 1.3, "die_01", "Khuỵu, đổ nghiêng, giáp sa thạch rơi từng tấm, bụi.", "bụi, mảnh giáp.", ""),
    ]),
    "quy_nui": dict(ten="Vượn núi đá bốn tay", ai=20, muc="mạnh nhất", mon="monster_3612", clips=[
        ("appear", 2.0, None,
         "Nhảy từ trên cao xuống, đáp quỳ một gối + hai nắm đấm NỆN đất → đứng dậy ĐẤM NGỰC bằng cả bốn tay (thùm thụp so le như khỉ đột) rồi gầm.",
         "hố, vòng bụi lớn, đá văng lúc đáp; bụi nhỏ mỗi cú đấm ngực; rung mạnh.", ""),
        ("idle", 2.0, "idle_01",
         "Thở nặng, vai nhô lên hạ xuống, chống nắm đấm; hai tay phụ co duỗi ngón chậm lệch pha. Phá nhịp: một tay phụ GÃI ĐẦU / bẻ khớp ngón; sỏi rơi khỏi vai lúc thở sâu.",
         "sỏi rơi.", "idle gốc 4 s: lấy một vòng 2 s."),
        ("walk", 0.8, "run_01", "Đi chống nắm đấm như khỉ đột.", "bụi chân.", ""),
        ("attack", 1.2, "skill_01 rút gọn",
         "Liên hoàn ba nhịp: đấm thẳng tay phải → móc tay trái → hai tay phụ ĐẬP BÚA xuống; khựng ở nhịp 1 và 3.",
         "mức nặng: chớp kem, đá vụn mỗi nhịp, nhịp cuối vòng bụi.", "clip gốc dài 2,17 s, nén lại."),
        ("cast", 1.3, "skill_02",
         "Giơ hai nắm đấm chính quá đầu, NỆN xuống đất (hai tay phụ dang ra giữ thăng bằng) → SÓNG CHẤN: một bức tường đất cuộn đá lăn tới hất tung đối thủ.",
         "sóng đất (mảng liền) + đá lăn, bụi; mức nặng.", ""),
        ("skill", 2.6, "skill_03 + skill_02",
         "Hai tay phụ giơ lên trời, đá dưới đất bay lên hợp thành một TẢNG ĐÁ KHỔNG LỒ giữa hai bàn tay phụ → hai nắm đấm chính nện đất hai nhịp gồng → cả bốn tay NÉM tảng đá → rơi nện lên đối thủ, sau đó mưa đá nhỏ.",
         "tụ: đá vụn hút lên, tảng lớn dần; nện: chớp màn kem, rung mạnh nhất, đá vỡ toé, bụi dày, mưa đá; mức tuyệt kỹ đầy đủ.", "tay phụ ôm đúng quanh chỗ tảng đá (điểm cầm); rig chỉ diễn phần tụ, đường bay do code (vat-bay-trung-dich-bang-code)."),
        ("hit", 0.5, "hit_01", "Lắc nặng, bật ít.", "dăm đá.", ""),
        ("die", 1.5, "die_01", "Loạng choạng, hai tay phụ rũ xuống, quỳ, đổ sấp lên nắm đấm, mạch hổ phách đổi màu tối, thân đá nứt, mờ dần.", "đá vụn, bụi.", ""),
    ]),
}


def nguon_anh(mon, clip):
    if not clip:
        return None
    c = clip.split()[0]
    for sub in ("khung5", "khung"):
        p = os.path.join(SXS, mon, sub, c + ".jpg")
        if os.path.exists(p):
            return p
    return None


def xem():
    e = html.escape
    rows = []
    for code, a in ANIM.items():
        concept = f"{code}_1/tai_ve/L1_duyet.png"
        cl = []
        for ten, dai, nguon, dien, vfx, ghi in a["clips"]:
            p = nguon_anh(a["mon"], nguon)
            img = (f'<img src="file:///{p.replace(os.sep, "/")}" loading=lazy>' if p else '<div class=tu>Claude tự nghĩ</div>')
            cl.append(f"<tr><td class=c><b>{ten}</b><br>{dai:.2f} s<br><small>{e(nguon or 'mới')}</small></td><td>{e(dien)}"
                      f"<div class=v><b>VFX:</b> {e(vfx)}</div>" + (f"<div class=g>{e(ghi)}</div>" if ghi else "") + f"</td><td class=s>{img}</td></tr>")
        rows.append(f"<h2>{a['ai'] and ''}Ải {a['ai']}: {e(a['ten'])} <small>(<code>{code}</code>, con gốc {a['mon']}, độ mạnh: {e(a['muc'])})"
                    f"</small></h2><div class=top><img class=cc src='{concept}'></div><table>{''.join(cl)}</table>")
    page = ("<!doctype html><meta charset=utf-8><title>Thổ: đề xuất animation</title><style>body{font:15px sans-serif;margin:16px;"
            "background:#f4f1ea;color:#222}h2{margin:28px 0 8px}table{border-collapse:collapse;width:100%;background:#fff}td{border:1px solid "
            "#ddd;padding:8px;vertical-align:top}td.c{width:110px}td.s{width:520px}td.s img{width:520px}.v{margin-top:6px;color:#6a4a1e}"
            ".g{margin-top:4px;color:#666;font-size:13px}.tu{color:#999;padding:20px}.cc{width:420px;border:1px solid #ddd;background:#fff}"
            "</style><h1>Đảo Thổ: đề xuất animation năm tướng đầu</h1><p>Cột phải: tờ khung clip của con gốc làm nguồn (game tham khảo, chỉ xem "
            "trong máy). Mỗi con một kiểu đòn; độ mạnh leo theo ải.</p>" + "".join(rows))
    p = os.path.join(HERE, "inbox", "tho5_xem_anim.html")
    open(p, "w", encoding="utf-8").write(page)
    print(p)


if __name__ == "__main__":
    if (sys.argv[1:] or [""])[0] == "xem":
        xem()
    else:
        print(__doc__)
