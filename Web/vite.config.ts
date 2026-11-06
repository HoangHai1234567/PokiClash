// Máy chủ dev: phục vụ thêm
//  /aola/*  từ thư mục reskin của dự án AolaRipper (hình tướng chỉ dùng trong bản thử, không chép vào đây);
//  /unity/* từ Assets/03 Art của project Unity (ảnh đảo, bệ đá... dùng chung, không chép sang web).
import { defineConfig, type Plugin } from 'vite';
import fs from 'node:fs';
import path from 'node:path';
import type { IncomingMessage, ServerResponse } from 'node:http';

// máy ổ D để aola ở D:/Aola-…, máy ổ E để cạnh project (E:/ProjectAtomik/aola); lấy chỗ nào có trước
const AOLA = path.resolve(
  process.env.AOLA_RESKIN ||
    ['D:/Aola-20261029T161238Z-1-001/Aola/AolaRipper/AolaRipper/reskin', path.resolve(import.meta.dirname, '../../aola/reskin')].find((p) => fs.existsSync(p)) ||
    'D:/Aola-20261029T161238Z-1-001/Aola/AolaRipper/AolaRipper/reskin',
);
const UNITY_ART = path.resolve(import.meta.dirname, '../Assets/03 Art');
const TYPES: Record<string, string> = { '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg' };

function serveDir(prefix: string, root: string, exts?: string[]) {
  return (req: IncomingMessage, res: ServerResponse, next: () => void) => {
    if (!req.url || !req.url.startsWith(prefix)) return next();
    const rel = decodeURIComponent(req.url.slice(prefix.length).split('?')[0]);
    const file = path.resolve(root, rel);
    const ext = path.extname(file).toLowerCase();
    if (!file.startsWith(root) || (exts && !exts.includes(ext)) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
      res.statusCode = 404;
      res.end();
      return;
    }
    res.setHeader('Content-Type', TYPES[ext] || 'application/octet-stream');
    res.setHeader('Cache-Control', 'max-age=600');
    fs.createReadStream(file).pipe(res);
  };
}

function artDirs(): Plugin {
  const aola = serveDir('/aola/', AOLA);
  const unity = serveDir('/unity/', UNITY_ART, ['.png', '.jpg']);
  return {
    name: 'art-dirs',
    configureServer(s) { s.middlewares.use(aola); s.middlewares.use(unity); },
    configurePreviewServer(s) { s.middlewares.use(aola); s.middlewares.use(unity); },
  };
}

export default defineConfig({
  plugins: [artDirs()],
  server: { port: 5180 },
  preview: { port: 5181 },
});
