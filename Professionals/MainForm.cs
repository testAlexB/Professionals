using CustomUIComponents;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace Professionals
{
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
            var menuItems = new Dictionary<string, List<string>>() {
                { "Главная", null },
                { "Монитор ТА", null },
                { "Детальные отчёты", null },
                { "Учёт ТМЦ", null },
                { "Администрирование", new List<string> { "ТА",
                                                          "Компании",
                                                          "Пользователи",
                                                          "Модемы",
                                                          "Дополнительные"
                } 
                } };

            foreach (KeyValuePair<string, List<string>> item in menuItems)
            {
                var button = new MenuButtonContainer(item.Key, item.Value);
                menuContainer.Controls.Add(button);
            }
        }

        public MainForm()
        {
            InitializeComponent();
            ApplyStyle();
            BuildSidebar();
        }
    }
}
