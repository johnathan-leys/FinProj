import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, 
    QLabel, QLineEdit, QMessageBox
)
from StockObj import StockData  

class FinanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Initialize StockData object with your API key
        with open(".APIkeys", 'r') as file:
            API_KEY = file.readline().strip().split()[0]
        self.stock_data = StockData(API_KEY)

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel('Welcome to the Finance App')
        layout.addWidget(self.label)

        # basic input to get stock symbol
        self.symbol_input = QLineEdit(self)
        self.symbol_input.setPlaceholderText('Enter stock symbol...')
        layout.addWidget(self.symbol_input)

        btn_fetch_data = QPushButton('Fetch Data', self)
        btn_fetch_data.clicked.connect(self.fetch_data)
        layout.addWidget(btn_fetch_data)

        # button to trigger plotting
        btn_plot_data = QPushButton('Plot Data', self)
        btn_plot_data.clicked.connect(self.plot_data)
        layout.addWidget(btn_plot_data)

        # button to export data to CSV
        btn_export_csv = QPushButton('Export to CSV', self)
        btn_export_csv.clicked.connect(self.export_csv)
        layout.addWidget(btn_export_csv)

        self.setLayout(layout)
        self.setWindowTitle('Finance App')
        self.resize(400, 300)  
        self.show()

    def fetch_data(self):
        symbol = self.symbol_input.text()
        self.stock_data.fetch_and_process(symbol)
        self.label.setText(f'Data fetched for {symbol}!')

    def plot_data(self):
        try:
            self.stock_data.plot_prices()
            self.stock_data.plot_mplfinance(style='nightclouds', mav=(5, 20), volume=True)
            QMessageBox.information(self, 'Success', 'Data plotted successfully!')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'An error occurred while plotting data: {str(e)}')

    def export_csv(self):
        try:
            self.stock_data.df_to_csv()
            QMessageBox.information(self, 'Success', 'Data exported to CSV successfully!')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'An error occurred while exporting data: {str(e)}')

# Create application instance

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FinanceApp()
    sys.exit(app.exec_())
