using System.Drawing;
using System.Windows.Forms;

namespace Professionals.UI
{
    internal static class DashboardHomeBuilder
    {
        private static readonly Font HeaderFont = new Font("Segoe UI", 10F, FontStyle.Bold);
        private static readonly Font CaptionFont = new Font("Segoe UI", 9F, FontStyle.Regular);

        public static void Build(Panel panelContent)
        {
            panelContent.Controls.Clear();

            var pageContainer = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                Padding = new Padding(18),
                ColumnCount = 1,
                RowCount = 2
            };

            pageContainer.RowStyles.Add(new RowStyle(SizeType.Absolute, 38F));
            pageContainer.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));

            var title = new Label
            {
                Text = "Личный кабинет · Главная",
                Font = new Font("Segoe UI", 14F, FontStyle.Bold),
                ForeColor = Color.FromArgb(28, 35, 49),
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft
            };

            var grid = new TableLayoutPanel
            {
                ColumnCount = 3,
                RowCount = 3,
                Dock = DockStyle.Fill,
                Padding = new Padding(0, 8, 0, 0)
            };

            grid.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33.33F));
            grid.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33.33F));
            grid.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33.34F));
            grid.RowStyles.Add(new RowStyle(SizeType.Absolute, 160F));
            grid.RowStyles.Add(new RowStyle(SizeType.Absolute, 220F));
            grid.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));

            grid.Controls.Add(CreateEfficiencyCard(), 0, 0);
            grid.Controls.Add(CreateNetworkStateCard(), 1, 0);
            grid.Controls.Add(CreateSummaryCard(), 2, 0);

            var salesTrendCard = CreateSalesTrendCard();
            grid.Controls.Add(salesTrendCard, 0, 1);
            grid.SetColumnSpan(salesTrendCard, 2);

            grid.Controls.Add(CreateNewsCard(), 2, 1);

            var pushCard = CreatePushInfoCard();
            grid.Controls.Add(pushCard, 0, 2);
            grid.SetColumnSpan(pushCard, 3);

            pageContainer.Controls.Add(title, 0, 0);
            pageContainer.Controls.Add(grid, 0, 1);
            panelContent.Controls.Add(pageContainer);
        }

        private static Panel CreateCard(string title)
        {
            var card = new Panel
            {
                Margin = new Padding(6),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle,
                Dock = DockStyle.Fill,
                Padding = new Padding(12)
            };

            var titleLabel = new Label
            {
                Text = title,
                Font = HeaderFont,
                ForeColor = Color.FromArgb(46, 60, 80),
                Dock = DockStyle.Top,
                Height = 22,
                TextAlign = ContentAlignment.MiddleLeft
            };

            card.Controls.Add(titleLabel);
            return card;
        }

        private static Control CreateEfficiencyCard()
        {
            var card = CreateCard("Эффективность сети");

            var content = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 2,
                Padding = new Padding(4, 10, 4, 0)
            };

            content.RowStyles.Add(new RowStyle(SizeType.Percent, 65F));
            content.RowStyles.Add(new RowStyle(SizeType.Percent, 35F));

            var percent = new Label
            {
                Text = "87%",
                Font = new Font("Segoe UI", 26F, FontStyle.Bold),
                ForeColor = Color.FromArgb(38, 166, 91),
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft
            };

            var text = new Label
            {
                Text = "Работают 174 из 200 аппаратов",
                Font = CaptionFont,
                ForeColor = Color.FromArgb(95, 108, 127),
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.TopLeft
            };

            content.Controls.Add(percent, 0, 0);
            content.Controls.Add(text, 0, 1);
            card.Controls.Add(content);
            return card;
        }

        private static Control CreateNetworkStateCard()
        {
            var card = CreateCard("Состояние сети");

            var content = new FlowLayoutPanel
            {
                Dock = DockStyle.Fill,
                FlowDirection = FlowDirection.TopDown,
                WrapContents = false,
                Padding = new Padding(4, 10, 4, 0)
            };

            content.Controls.Add(CreateLegendItem("Работает", Color.FromArgb(38, 166, 91)));
            content.Controls.Add(CreateLegendItem("На обслуживании", Color.FromArgb(52, 152, 219)));
            content.Controls.Add(CreateLegendItem("Не работает", Color.FromArgb(231, 76, 60)));

            card.Controls.Add(content);
            return card;
        }

        private static Control CreateLegendItem(string text, Color color)
        {
            var row = new TableLayoutPanel
            {
                ColumnCount = 2,
                RowCount = 1,
                Width = 250,
                Height = 24,
                Margin = new Padding(0, 0, 0, 6)
            };

            row.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 18F));
            row.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));

            var dot = new Panel
            {
                BackColor = color,
                Width = 12,
                Height = 12,
                Margin = new Padding(0, 6, 0, 0),
                Anchor = AnchorStyles.Left
            };

            var label = new Label
            {
                Text = text,
                Font = CaptionFont,
                ForeColor = Color.FromArgb(70, 82, 100),
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft
            };

            row.Controls.Add(dot, 0, 0);
            row.Controls.Add(label, 1, 0);
            return row;
        }

        private static Control CreateSummaryCard()
        {
            var card = CreateCard("Сводка");

            var summary = new ListView
            {
                View = View.Details,
                HeaderStyle = ColumnHeaderStyle.None,
                FullRowSelect = false,
                GridLines = false,
                Dock = DockStyle.Fill,
                BorderStyle = BorderStyle.None,
                Font = CaptionFont
            };

            summary.Columns.Add("Параметр", 180);
            summary.Columns.Add("Значение", 95);
            summary.Items.Add(new ListViewItem(new[] { "Продажи за сегодня", "142 600 ₽" }));
            summary.Items.Add(new ListViewItem(new[] { "Инкассация", "9 точек" }));
            summary.Items.Add(new ListViewItem(new[] { "Обслуживание", "6 задач" }));
            summary.Items.Add(new ListViewItem(new[] { "Критические события", "2" }));

            card.Controls.Add(summary);
            return card;
        }

        private static Control CreateSalesTrendCard()
        {
            var card = CreateCard("Динамика продаж за последние 10 дней");

            var content = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 2
            };

            content.RowStyles.Add(new RowStyle(SizeType.Absolute, 34F));
            content.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));

            var filterPanel = new FlowLayoutPanel
            {
                Dock = DockStyle.Fill,
                FlowDirection = FlowDirection.LeftToRight,
                WrapContents = false,
                Padding = new Padding(0, 4, 0, 0)
            };

            filterPanel.Controls.Add(CreateChip("По сумме", true));
            filterPanel.Controls.Add(CreateChip("По количеству", false));

            var chartLayout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 10,
                RowCount = 1,
                Padding = new Padding(12, 6, 12, 10)
            };

            for (var i = 0; i < 10; i++)
            {
                chartLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 10F));
            }

            var bars = new[] { 40, 58, 76, 60, 88, 92, 74, 68, 80, 95 };
            for (var i = 0; i < bars.Length; i++)
            {
                var barHost = new Panel
                {
                    Dock = DockStyle.Fill,
                    Padding = new Padding(6, 0, 6, 0)
                };

                var bar = new Panel
                {
                    Dock = DockStyle.Bottom,
                    Height = bars[i],
                    BackColor = Color.FromArgb(139, 194, 245)
                };

                barHost.Controls.Add(bar);
                chartLayout.Controls.Add(barHost, i, 0);
            }

            content.Controls.Add(filterPanel, 0, 0);
            content.Controls.Add(chartLayout, 0, 1);
            card.Controls.Add(content);
            return card;
        }

        private static Control CreateChip(string text, bool active)
        {
            return new Button
            {
                Text = text,
                Width = 96,
                Height = 24,
                FlatStyle = FlatStyle.Flat,
                BackColor = active ? Color.FromArgb(52, 152, 219) : Color.FromArgb(245, 247, 250),
                ForeColor = active ? Color.White : Color.FromArgb(70, 82, 100),
                FlatAppearance =
                {
                    BorderColor = Color.FromArgb(203, 213, 225),
                    BorderSize = 1
                },
                Font = new Font("Segoe UI", 8F, FontStyle.Regular),
                Margin = new Padding(0, 0, 8, 0)
            };
        }

        private static Control CreateNewsCard()
        {
            var card = CreateCard("Новости");

            var list = new ListBox
            {
                Dock = DockStyle.Fill,
                BorderStyle = BorderStyle.None,
                Font = CaptionFont
            };

            list.Items.Add("01.05 · Плановое обновление API в 23:00");
            list.Items.Add("30.04 · Добавлены шаблоны push-уведомлений");
            list.Items.Add("28.04 · Обновлён отчёт по инкассациям");
            list.Items.Add("27.04 · Запуск 5 новых ТА в регионе #3");

            card.Controls.Add(list);
            return card;
        }

        private static Control CreatePushInfoCard()
        {
            var card = CreateCard("Push-уведомления (демо)");

            var layout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 3
            };

            layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33.33F));
            layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33.33F));
            layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33.34F));

            layout.Controls.Add(CreateNotificationTile("Критические", "3", Color.FromArgb(231, 76, 60)), 0, 0);
            layout.Controls.Add(CreateNotificationTile("Предупреждения", "7", Color.FromArgb(243, 156, 18)), 1, 0);
            layout.Controls.Add(CreateNotificationTile("Информационные", "18", Color.FromArgb(38, 166, 91)), 2, 0);

            card.Controls.Add(layout);
            return card;
        }

        private static Control CreateNotificationTile(string title, string count, Color color)
        {
            var tile = new Panel
            {
                Margin = new Padding(6),
                Dock = DockStyle.Fill,
                BackColor = Color.FromArgb(248, 250, 253),
                BorderStyle = BorderStyle.FixedSingle,
                Padding = new Padding(10)
            };

            var inner = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 2
            };

            inner.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 8F));
            inner.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            inner.RowStyles.Add(new RowStyle(SizeType.Absolute, 24F));
            inner.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));

            var marker = new Panel
            {
                BackColor = color,
                Dock = DockStyle.Fill,
                Margin = new Padding(0)
            };

            var titleLabel = new Label
            {
                Text = title,
                Font = new Font("Segoe UI", 9F, FontStyle.Regular),
                ForeColor = Color.FromArgb(70, 82, 100),
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft,
                Padding = new Padding(8, 0, 0, 0)
            };

            var countLabel = new Label
            {
                Text = count,
                Font = new Font("Segoe UI", 20F, FontStyle.Bold),
                ForeColor = Color.FromArgb(33, 43, 54),
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft,
                Padding = new Padding(6, 0, 0, 0)
            };

            inner.Controls.Add(marker, 0, 0);
            inner.SetRowSpan(marker, 2);
            inner.Controls.Add(titleLabel, 1, 0);
            inner.Controls.Add(countLabel, 1, 1);

            tile.Controls.Add(inner);
            return tile;
        }
    }
}
