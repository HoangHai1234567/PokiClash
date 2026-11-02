// Tên các scene chức năng (trùng tên file .unity trong Assets/00 Scenes, và thứ tự trong Build Settings sau Boot).
namespace PokiClash
{
    public static class SceneIds
    {
        public const string Boot = "Boot";
        public const string Hub = "Hub";
        public const string Zone = "Zone";
        public const string Battle = "Battle";
        public const string Machine = "Machine";
        public const string Heroes = "Heroes";
        public const string Cards = "Cards";
        public const string Notebook = "Notebook";
        public const string Badges = "Badges";
        public const string Cave = "Cave";
        public const string Farm = "Farm";

        public static readonly string[] Features = { Hub, Zone, Battle, Machine, Heroes, Cards, Notebook, Badges, Cave, Farm };
    }
}
