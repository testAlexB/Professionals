using CustomUIComponents;
using Professionals.UI;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace Professionals
{
    public partial class MainForm : Form
    {
        private void ApplyStyle()
        {
            BackColor = Color.FromArgb(240, 243, 247);
            MinimumSize = new Size(1200, 760);

            panelSidebar.BackColor = Color.FromArgb(18, 27, 41);
            topBar.BackColor = Color.FromArgb(23, 28, 38);
            panelContent.BackColor = Color.FromArgb(240, 243, 247);
            menuContainer.BackColor = Color.Transparent;
            menuContainer.Padding = new Padding(0, 8, 0, 0);
        }

        private void BuildSidebar()
        {
            menuContainer.Controls.Clear();

            var menuItems = new Dictionary<string, List<string>>
            {
                { "Главная", null },
                { "Монитор ТА", null },
                { "Детальные отчёты", null },
                { "Учёт ТМЦ", null },
                {
                    "Администрирование",
                    new List<string>
                    {
                        "Торговые автоматы",
                        "Компании",
                        "Пользователи",
                        "Модемы",
                        "Дополнительные"
                    }
                }
            };

            foreach (KeyValuePair<string, List<string>> item in menuItems)
            {
                var button = new MenuButtonContainer(item.Key, item.Value)
                {
                    Margin = new Padding(0, 0, 0, 1)
                };

                menuContainer.Controls.Add(button);
            }
        }

        public MainForm()
        {
            InitializeComponent();

            ApplyStyle();
            BuildSidebar();
            TopBarBuilder.Build(topBar);
            DashboardHomeBuilder.Build(panelContent);
        }
    }
}
