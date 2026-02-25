using System.Drawing;
using System.Windows.Forms;

namespace Professionals.UI
{
    internal static class TopBarBuilder
    {
        public static void Build(Panel topBar)
        {
            topBar.Controls.Clear();

            var layout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 1,
                Padding = new Padding(18, 8, 18, 8),
                BackColor = Color.Transparent
            };

            layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 70F));
            layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));

            var logoLabel = new Label
            {
                Text = "ООО Торговые Автоматы",
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 10F, FontStyle.Bold),
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft
            };

            var roleLabel = new Label
            {
                Text = "Автоматов А.А. · Администратор",
                ForeColor = Color.FromArgb(190, 197, 210),
                Font = new Font("Segoe UI", 9F, FontStyle.Regular),
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleRight
            };

            layout.Controls.Add(logoLabel, 0, 0);
            layout.Controls.Add(roleLabel, 1, 0);
            topBar.Controls.Add(layout);
        }
    }
}
