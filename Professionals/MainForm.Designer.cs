namespace Professionals
{
    partial class MainForm
    {
        /// <summary>
        /// Обязательная переменная конструктора.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Освободить все используемые ресурсы.
        /// </summary>
        /// <param name="disposing">истинно, если управляемый ресурс должен быть удален; иначе ложно.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Код, автоматически созданный конструктором форм Windows

        /// <summary>
        /// Требуемый метод для поддержки конструктора — не изменяйте 
        /// содержимое этого метода с помощью редактора кода.
        /// </summary>
        private void InitializeComponent()
        {
            this.panelSidebar = new System.Windows.Forms.Panel();
            this.menuContainer = new System.Windows.Forms.FlowLayoutPanel();
            this.topBar = new System.Windows.Forms.Panel();
            this.panelContent = new System.Windows.Forms.Panel();
            this.topTableLayout = new System.Windows.Forms.TableLayoutPanel();
            this.leftTopBarPanel = new System.Windows.Forms.FlowLayoutPanel();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.userInfoWidget = new CustomUIComponents.WIdgets.UserInfoWidget();
            this.panelSidebar.SuspendLayout();
            this.topBar.SuspendLayout();
            this.topTableLayout.SuspendLayout();
            this.leftTopBarPanel.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // panelSidebar
            // 
            this.panelSidebar.BackColor = System.Drawing.SystemColors.Control;
            this.panelSidebar.Controls.Add(this.menuContainer);
            this.panelSidebar.Dock = System.Windows.Forms.DockStyle.Left;
            this.panelSidebar.Location = new System.Drawing.Point(0, 60);
            this.panelSidebar.Name = "panelSidebar";
            this.panelSidebar.Size = new System.Drawing.Size(203, 390);
            this.panelSidebar.TabIndex = 0;
            // 
            // menuContainer
            // 
            this.menuContainer.AutoScroll = true;
            this.menuContainer.AutoSize = true;
            this.menuContainer.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.menuContainer.Dock = System.Windows.Forms.DockStyle.Fill;
            this.menuContainer.FlowDirection = System.Windows.Forms.FlowDirection.TopDown;
            this.menuContainer.Location = new System.Drawing.Point(0, 0);
            this.menuContainer.Name = "menuContainer";
            this.menuContainer.Size = new System.Drawing.Size(203, 390);
            this.menuContainer.TabIndex = 0;
            this.menuContainer.WrapContents = false;
            this.menuContainer.Paint += new System.Windows.Forms.PaintEventHandler(this.menuContainer_Paint);
            // 
            // topBar
            // 
            this.topBar.Controls.Add(this.topTableLayout);
            this.topBar.Dock = System.Windows.Forms.DockStyle.Top;
            this.topBar.Location = new System.Drawing.Point(0, 0);
            this.topBar.Name = "topBar";
            this.topBar.Size = new System.Drawing.Size(581, 60);
            this.topBar.TabIndex = 1;
            // 
            // panelContent
            // 
            this.panelContent.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panelContent.Location = new System.Drawing.Point(203, 60);
            this.panelContent.Name = "panelContent";
            this.panelContent.Size = new System.Drawing.Size(378, 390);
            this.panelContent.TabIndex = 2;
            // 
            // topTableLayout
            // 
            this.topTableLayout.BackColor = System.Drawing.Color.Transparent;
            this.topTableLayout.ColumnCount = 2;
            this.topTableLayout.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 70F));
            this.topTableLayout.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 30F));
            this.topTableLayout.Controls.Add(this.leftTopBarPanel, 0, 0);
            this.topTableLayout.Controls.Add(this.userInfoWidget, 1, 0);
            this.topTableLayout.Dock = System.Windows.Forms.DockStyle.Fill;
            this.topTableLayout.Location = new System.Drawing.Point(0, 0);
            this.topTableLayout.Name = "topTableLayout";
            this.topTableLayout.Padding = new System.Windows.Forms.Padding(18, 8, 18, 8);
            this.topTableLayout.RowCount = 1;
            this.topTableLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.topTableLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.topTableLayout.Size = new System.Drawing.Size(581, 60);
            this.topTableLayout.TabIndex = 0;
            // 
            // leftTopBarPanel
            // 
            this.leftTopBarPanel.AutoSize = true;
            this.leftTopBarPanel.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.leftTopBarPanel.Controls.Add(this.pictureBox1);
            this.leftTopBarPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.leftTopBarPanel.Location = new System.Drawing.Point(21, 11);
            this.leftTopBarPanel.Name = "leftTopBarPanel";
            this.leftTopBarPanel.Padding = new System.Windows.Forms.Padding(10, 0, 0, 0);
            this.leftTopBarPanel.Size = new System.Drawing.Size(375, 38);
            this.leftTopBarPanel.TabIndex = 0;
            this.leftTopBarPanel.WrapContents = false;
            // 
            // pictureBox1
            // 
            this.pictureBox1.Image = global::Professionals.Properties.Resources.Logo;
            this.pictureBox1.Location = new System.Drawing.Point(10, 3);
            this.pictureBox1.Margin = new System.Windows.Forms.Padding(0, 3, 0, 3);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(108, 30);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox1.TabIndex = 0;
            this.pictureBox1.TabStop = false;
            // 
            // userInfoWidget
            // 
            this.userInfoWidget.AccessibleRole = System.Windows.Forms.AccessibleRole.None;
            this.userInfoWidget.Dock = System.Windows.Forms.DockStyle.Right;
            this.userInfoWidget.Location = new System.Drawing.Point(402, 11);
            this.userInfoWidget.Name = "userInfoWidget";
            this.userInfoWidget.Size = new System.Drawing.Size(158, 38);
            this.userInfoWidget.TabIndex = 1;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Control;
            this.ClientSize = new System.Drawing.Size(581, 450);
            this.Controls.Add(this.panelContent);
            this.Controls.Add(this.panelSidebar);
            this.Controls.Add(this.topBar);
            this.Name = "MainForm";
            this.Text = "Form1";
            this.panelSidebar.ResumeLayout(false);
            this.panelSidebar.PerformLayout();
            this.topBar.ResumeLayout(false);
            this.topTableLayout.ResumeLayout(false);
            this.topTableLayout.PerformLayout();
            this.leftTopBarPanel.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Panel panelSidebar;
        private System.Windows.Forms.Panel topBar;
        private System.Windows.Forms.Panel panelContent;
        private System.Windows.Forms.FlowLayoutPanel menuContainer;
        private System.Windows.Forms.TableLayoutPanel topTableLayout;
        private System.Windows.Forms.PictureBox pictureBox1;
        private CustomUIComponents.WIdgets.UserInfoWidget userInfoWidget;
        public System.Windows.Forms.FlowLayoutPanel leftTopBarPanel;
    }
}

