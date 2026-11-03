// Bật bộ ải cũ (8 ải mỗi đảo) cho script xuất sang Unity, tới khi Unity chép hệ thống ải mới (islands.ts).
// Phải import file này TRƯỚC mọi import khác của script: stages.ts đọc cờ lúc nạp. Chép xong sang Unity thì bỏ dòng import.
(globalThis as { __POKI_STAGES_V1__?: boolean }).__POKI_STAGES_V1__ = true;
export {};
