// Máy chủ dev: phục vụ thêm /aola/* từ thư mục reskin của dự án AolaRipper (hình tướng chỉ dùng trong bản thử, không chép vào đây).
import { defineConfig, type Plugin } from 'vite';
import fs from 'node:fs';
import path from 'node:path';
import type { IncomingMessage, ServerResponse } from 'node:http';

const AOLA = path.resolve(process.env.AOLA_RESKIN || 'D:/Aola-20261029T161238Z-1-001/Aola/AolaRipper/AolaRipper/reskin');
const TYPES: Record<string, string> = { '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg' };

function aola(): Plugin {
  const handler = (req: IncomingMessage, res: ServerResponse, next: () => void) => {
    if (!req.url || !req.url.startsWith('/aola/')) return next();
    const rel = decodeURIComponent(req.url.slice(6).split('?')[0]);
    const file = path.resolve(AOLA, rel);
    if (!file.startsWith(AOLA) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
      res.statusCode = 404;
      res.end();
      return;
    }
    res.setHeader('Content-Type', TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream');
    res.setHeader('Cache-Control', 'max-age=600');
    fs.createReadStream(file).pipe(res);
  };
  return {
    name: 'aola-reskin',
    configureServer(s) { s.middlewares.use(handler); },
    configurePreviewServer(s) { s.middlewares.use(handler); },
  };
}

export default defineConfig({
  plugins: [aola()],
  server: { port: 5180 },
  preview: { port: 5181 },
});
