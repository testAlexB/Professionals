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
            panelSidebar.BackColor = Color.FromArgb(33, 43, 54);
            topBar.BackColor = Color.White;
            panelContent.BackColor = Color.FromArgb(245, 247, 250);
            menuContainer.BackColor = Color.Transparent;
        }

        private void BuildSidebar()
        {
            List<string> menuItems = new List<string>() { 
                "Главная",
                "Монитор ТА", 
                "Детальные отчёты",
                "Учёт ТМЦ", 
                "Администрирование" };

            foreach (string item in menuItems)
            {
                var button = new MenuButton();
                button.Text = item;
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
