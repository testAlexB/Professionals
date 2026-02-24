using Professionals.UI;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace CustomUIComponents
{
    public partial class MenuButtonContainer : UserControl
    {
        private MenuButton button_ = new MenuButton();

        private FlowLayoutPanel subMenu_ = new FlowLayoutPanel()
        {
            FlowDirection = FlowDirection.TopDown,
            WrapContents = false,
            AutoSize = true,
            AutoSizeMode = AutoSizeMode.GrowAndShrink,
            BackColor = Color.FromArgb(40, 50, 60),
            Visible = false,
        };

        private bool isExpanded_;
        public MenuButtonContainer(string text, List<string> subItems = null)
            : base()
        {
            InitializeComponent();

            Margin = new Padding(0);

            {
                button_.Text = text;
                button_.Click += Button__Click;
            }

            mainLayout.Controls.Add(button_);

            if (subItems != null && subItems.Count > 0)
            {
                foreach (string item in subItems)
                {
                    var btn = new MenuButton();
                    btn.Text = "      " + item;
                    btn.BackColor = Color.FromArgb(40, 50, 60);
                    subMenu_.Controls.Add(btn);
                }

                mainLayout.Controls.Add(subMenu_);
            }

            UpdateArrow();
        }

        private void UpdateArrow()
        {
            if (subMenu_.Controls.Count == 0)
            {
                return;
            }

            button_.Text = isExpanded_
                ? button_.Text.Replace("▼", "▲")
                : button_.Text.Replace("▲", "▼");

            if (!button_.Text.Contains("▼") && !button_.Text.Contains("▲"))
            {
                button_.Text += "  ▼";
            }
        }

        private void Button__Click(object sender, System.EventArgs e)
        {
            if (subMenu_.Controls.Count == 0)
            {
                return;
            }

            isExpanded_ = !isExpanded_;
            subMenu_.Visible = isExpanded_;

            UpdateArrow();
        }
    }
}
