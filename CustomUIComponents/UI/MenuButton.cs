using System.Drawing;
using System.Windows.Forms;

namespace Professionals.UI
{
    public class MenuButton : System.Windows.Forms.Button
    {

        public void SetImage(Bitmap image)
        {
            if(image != null)
            {
                const int width = 24;
                const int height = 24;

                Bitmap resized = new Bitmap(image, new Size(width, height));

                Image = resized;
                ImageAlign = ContentAlignment.MiddleLeft;
                TextAlign = ContentAlignment.MiddleRight;
                TextImageRelation = TextImageRelation.ImageBeforeText;
            }
        }
        public MenuButton() : base()
        {
            AutoSize = false;
            FlatStyle = FlatStyle.Flat;
            FlatAppearance.BorderSize = 0;
            Width = 180;
            Height = 45;
            TextAlign = ContentAlignment.MiddleLeft;
            Padding = new Padding(0, 0, 0, 0);
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
