#!/bin/bash
# dựng lại project AtomSpine của nhím thép từ mảnh đã cắt: rig.ops + anim.ops
cd "$(dirname "$0")/.." || exit 1
A="node d:/AtomSpine/packages/cli/dist/atom.mjs"
py -3 -I quai_kim_fx.py >/dev/null && py -3 -I quai_kim_rig.py >/dev/null && py -3 -I quai_kim_anim.py >/dev/null || exit 1
$A init quai_kim/atom --name quai_kim --force >/dev/null 2>&1
$A do -f quai_kim/atom/rig.ops -p quai_kim/atom 2>&1 | tail -1
$A do -f quai_kim/atom/anim.ops -p quai_kim/atom 2>&1 | tail -1
$A lint -p quai_kim/atom 2>&1 | tail -1
