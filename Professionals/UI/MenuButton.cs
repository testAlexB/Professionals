using System.Drawing;
using System.Windows.Forms;

namespace Professionals.UI
{
    public class MenuButton : System.Windows.Forms.Button
    {
        public MenuButton() : base()
        {
            FlatStyle = FlatStyle.Flat;
            FlatAppearance.BorderSize = 0;
            Width = 150;
            Height = 45;
            TextAlign = ContentAlignment.MiddleLeft;
            Padding = new Padding(15, 0, 0, 0);
            ForeColor = Color.White;
            BackColor = Color.FromArgb(33, 43, 54);

            MouseEnter += (s, e) =>
            {
                BackColor = Color.FromArgb(45, 55, 72);
            };

            MouseLeave += (s, e) =>
            {
                BackColor = Color.FromArgb(33, 43, 54);
            };
        }
    }
}
