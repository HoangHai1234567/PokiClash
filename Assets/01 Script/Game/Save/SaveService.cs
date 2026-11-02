// Ghi và đọc bản lưu ở persistentDataPath/save_v{n}.json. Ghi qua file tạm rồi đổi tên, để tắt ngang không làm hỏng.
// Bản cũ hơn: chạy bước di chuyển nếu có; không có (hoặc file hỏng) thì giữ file thành .bak và báo người chơi trước khi làm mới.
using System;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.Core;
using UnityEngine;

namespace PokiClash.Game
{
    public sealed class SaveService
    {
        public SaveData Data { get; private set; }
        public string Dir { get; }
        public string Notice { get; private set; } // câu báo cho người chơi sau khi đọc (null nếu không có gì)
        public bool IsNew { get; private set; }
        public event Action Changed;

        readonly GameData data;
        int Version => data.Cfg.saveVersion;
        public string FilePath => Path.Combine(Dir, $"save_v{Version}.json");
        string TmpPath => FilePath + ".tmp";

        public static long Now() => DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();

        public SaveService(GameData data, string dir = null)
        {
            this.data = data;
            Dir = dir ?? Application.persistentDataPath;
        }

        // Đọc bản lưu. Trả true nếu đã có Data dùng được; false nghĩa là phải báo Notice rồi gọi CreateNew().
        public bool Load()
        {
            Notice = null;
            IsNew = false;
            Directory.CreateDirectory(Dir);

            // bản tạm còn sót (tắt ngang giữa lúc đổi tên): dùng nếu bản chính mất
            if (!File.Exists(FilePath) && File.Exists(TmpPath))
            {
                if (SaveCodec.Read(File.ReadAllText(TmpPath, Encoding.UTF8), data, out var fromTmp) != LoadStatus.Corrupt && fromTmp != null)
                {
                    Data = fromTmp;
                    Save();
                    return true;
                }
                File.Delete(TmpPath);
            }

            if (File.Exists(FilePath))
            {
                var st = SaveCodec.Read(File.ReadAllText(FilePath, Encoding.UTF8), data, out var s);
                if (st == LoadStatus.Ok || st == LoadStatus.Migrated)
                {
                    Data = s;
                    return true;
                }
                Backup(FilePath, Path.Combine(Dir, $"save_v{Version}.bak"));
                Notice = st == LoadStatus.Corrupt
                    ? "Bản lưu bị hỏng, không đọc được. Đã giữ bản cũ thành file dự phòng, game sẽ bắt đầu lại."
                    : "Bản lưu của phiên bản khác, không dùng được. Đã giữ bản cũ thành file dự phòng, game sẽ bắt đầu lại.";
                return false;
            }

            // bản lưu phiên bản cũ (tên file khác): di chuyển nếu được, không thì giữ .bak và báo
            var old = Directory.GetFiles(Dir, "save_v*.json")
                .Select(p => (p, v: SaveCodec.VersionOf(File.ReadAllText(p, Encoding.UTF8))))
                .Where(x => x.v >= 0 && x.v < Version)
                .OrderByDescending(x => x.v)
                .ToList();
            if (old.Count > 0)
            {
                var (path, v) = old[0];
                var st = SaveCodec.Read(File.ReadAllText(path, Encoding.UTF8), data, out var s);
                foreach (var o in old) Backup(o.p, Path.ChangeExtension(o.p, ".bak"));
                if (st == LoadStatus.Migrated || st == LoadStatus.Ok)
                {
                    Data = s;
                    Save();
                    return true;
                }
                Notice = "Dữ liệu bản thử cũ không dùng được, sẽ bắt đầu lại.";
                return false;
            }

            CreateNew();
            IsNew = true;
            return true;
        }

        public void CreateNew()
        {
            Data = SaveData.New(data, Now());
            Save();
        }

        // Ghi ngay (gọi sau mỗi thay đổi tiến trình). Ghi file tạm, xoá bản chính, đổi tên file tạm.
        public void Save()
        {
            if (Data == null) return;
            try
            {
                Directory.CreateDirectory(Dir);
                File.WriteAllText(TmpPath, SaveCodec.Write(Data), new UTF8Encoding(false));
                if (File.Exists(FilePath)) File.Delete(FilePath);
                File.Move(TmpPath, FilePath);
            }
            catch (Exception e)
            {
                Debug.LogError("[Lưu] Không ghi được bản lưu: " + e.Message);
            }
            Changed?.Invoke();
        }

        // Xoá dữ liệu: về người chơi mới (cấp 1, 10 bi, chỉ có tướng khởi đầu, mọi đảo 0/8).
        public void Reset()
        {
            CreateNew();
        }

        static void Backup(string from, string to)
        {
            try
            {
                if (File.Exists(to)) File.Delete(to);
                File.Move(from, to);
            }
            catch (Exception e)
            {
                Debug.LogWarning($"[Lưu] Không giữ được bản dự phòng {to}: {e.Message}");
            }
        }
    }
}
