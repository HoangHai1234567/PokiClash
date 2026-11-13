# -*- coding: utf-8 -*-
"""Cắt một bộ phận ra khỏi ảnh concept (nền trắng, nét mực nâu sẫm): các vùng kín (ngăn bởi nét mực) nằm phần lớn trong đa giác
khung, cộng nét mực ôm quanh. Trả ảnh RGBA cùng cỡ concept (ngoài bộ phận trong suốt).

    from cat_concept import cat
    rgba = cat(concept_rgb, polygon, ti=0.7, loai=lambda rgb: mask_bool)   # loai: px KHÔNG được lấy (vd. màu lá)
"""
import cv2
import numpy as np


def ink_mask(rgb, L_max=27):
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    return lab[..., 0] < L_max * 255 / 100


def cat(rgb, poly, ti=0.7, loai=None, vien=9, mo=1.2, mot_khoi=True, them=None, gioi_han=False):
    H, W = rgb.shape[:2]
    ink = ink_mask(rgb)
    white = rgb.min(2) > 238
    P = np.zeros((H, W), np.uint8)
    cv2.fillPoly(P, [np.round(np.asarray(poly)).astype(np.int32)], 1)
    P = P.astype(bool)
    free = ~ink & ~white
    if them is not None:                         # px tối nhưng KHÔNG phải mực (vd. lòng miệng đỏ sẫm): coi như vùng tô
        free |= them & ~white
        ink = ink & ~them
    if loai is not None:
        free &= ~loai
    n, lab = cv2.connectedComponents(free.astype(np.uint8), connectivity=4)
    inside = np.bincount(lab[P], minlength=n)
    tot = np.bincount(lab.ravel(), minlength=n)
    keep = (inside / np.maximum(tot, 1) >= ti) & (tot > 6)
    keep[0] = False
    body = keep[lab]
    if gioi_han:                                  # khối tô liền ra ngoài khung (lông hàm liền lông cổ): chỉ giữ phần trong khung
        body &= cv2.dilate(P.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool)
    near = cv2.dilate(body.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * vien + 1, 2 * vien + 1))).astype(bool)
    m = body | (near & ink & P)
    # lấp lỗ nhỏ (chấm sáng trong mắt, vạch) bằng đóng hình học rồi giữ thành phần lớn nhất
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))).astype(bool)
    cnt, cl, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
    if cnt > 1 and mot_khoi:
        big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        m = cl == big
    elif cnt > 1:                                 # giữ mọi khối đủ lớn
        keep2 = np.zeros(cnt, bool)
        keep2[1:] = st[1:, cv2.CC_STAT_AREA] > 150
        m = keep2[cl]
    # lấp lỗ kín bên trong
    ff = (~m).astype(np.uint8)
    cv2.floodFill(ff, None, (0, 0), 0)
    m |= ff.astype(bool)
    a = cv2.GaussianBlur(m.astype(np.float32), (0, 0), mo)
    a = np.clip((a - 0.25) / 0.5, 0, 1)
    out = np.dstack([rgb, (a * 255).astype(np.uint8)])
    return out, m
