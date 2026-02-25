using CustomUIComponents;
using Professionals.Properties;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace Professionals
{
    struct MenuButtonInfo
    {
        public string Name { get; set; }
        public Bitmap Icon { get; set; }
    }

    public partial class MainForm : Form
    {
        private void ApplyStyle()
        {
            panelSidebar.BackColor = Color.FromArgb(33, 43, 54);
            topBar.BackColor = Color.White;
            panelContent.BackColor = Color.FromArgb(245, 247, 250);
            menuContainer.BackColor = Color.Transparent;
        }

        private void BuildSidebar()
        {
            var menuItems = new Dictionary<MenuButtonInfo, List<string>>() {
                { new MenuButtonInfo {Name = "Главная", Icon = Resources.search}, null },
                { new MenuButtonInfo {Name = "Монитор ТА", Icon = Resources.desktop }, null },
                { new MenuButtonInfo {Name = "Детальные отчёты", Icon = Resources.file_text_o }, null },
                { new MenuButtonInfo {Name = "Учёт ТМЦ", Icon = Resources.shopping_cart }, null },
                { new MenuButtonInfo {Name = "Администрирование", Icon = Resources.cogs }, new List<string> { "ТА",
                                                          "Компании",
                                                          "Пользователи",
                                                          "Модемы",
                                                          "Дополнительные"
                } 
                } };

            foreach (KeyValuePair<MenuButtonInfo, List<string>> item in menuItems)
            {
                var button = new MenuButtonContainer(item.Key.Name, item.Value, item.Key.Icon);
                menuContainer.Controls.Add(button);
            }
        }

        public MainForm()
        {
            InitializeComponent();
            ApplyStyle();
            BuildSidebar();
        }

        private void menuContainer_Paint(object sender, PaintEventArgs e)
        {

        }
    }
}
