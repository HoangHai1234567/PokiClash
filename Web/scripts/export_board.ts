// Xuất hình học mặt máy bi (đinh, đoạn thẳng, cốc, ô) ra JSON cho draw_machine.py vẽ ảnh tĩnh của Unity:
// npx tsx scripts/export_board.ts > board.json
import { BH, BW, buildBoard, DROP_Y, FLOOR, LEFT, RIGHT, SLOT_TOP } from '../src/core/pachinko';

const b = buildBoard();
process.stdout.write(JSON.stringify({ BW, BH, LEFT, RIGHT, SLOT_TOP, FLOOR, DROP_Y, ...b }, null, 1) + '\n');
