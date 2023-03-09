import os
from PyQt5 import QtWidgets, QtGui, QtCore


class EmbeddedResourceGenerator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Set the window title and size
        self.setWindowTitle('Embedded Resource Generator')
        self.setFixedSize(600, 450)  # set a fixed size for the window

        # Create a button to generate resources
        btn_generate = QtWidgets.QPushButton('Choose Directory', self)
        btn_generate.clicked.connect(self.generate_resources)
        btn_generate.setStyleSheet('''
            background-color: #3b3b3b;
            color: #ffffff;
            font-size: 18px;
            padding: 10px;
            border: none;
            border-radius: 5px;
            margin-top: 20px;
            margin-right: 400px;
            margin-bottom: 10px;
        ''')

        # Center the button horizontally and place it at the top of the screen with some spacing
        btn_generate_width = btn_generate.sizeHint().width()
        self.btn_generate_x = (self.width() - btn_generate_width) // 2
        btn_generate.move(self.btn_generate_x, 10)

        # Add a label to describe the program
        program_desc = QtWidgets.QLabel(self)
        program_desc.setText(
            'Click "Choose Directory" to select a directory\n to generate the embedded resource string.')
        program_desc.setStyleSheet(
            'color: #ffffff; font-size: 14px; margin-left: 10px; margin-right: 10px; margin-top: 5px;')
        program_desc.setWordWrap(True)
        program_desc.setAlignment(QtCore.Qt.AlignLeft)
        program_desc.setGeometry(175, 30, 580, 60)

        # Create a text box to display the generated resources
        self.text_box = QtWidgets.QPlainTextEdit(self)
        self.text_box.setStyleSheet('''
            background-color: #353535;
            color: #ffffff;
            font-size: 14px;
            padding: 10px;
            border: none;
            border-radius: 5px;
        ''')
        self.text_box.setGeometry(10, 100, 580, 290)

    def generate_embedded_resources(self, dir_path):
        resources = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.startswith('.') or root.startswith('.'):
                    continue
                full_path = os.path.join(root, file)
                item_path = full_path
                item_name = os.path.splitext(os.path.basename(full_path))[0]
                resource = f'<EmbeddedResource Include="{item_path}">\n'
                resource += '  <CopyToOutputDirectory>Always</CopyToOutputDirectory>\n'
                resource += '</EmbeddedResource>'
                resources.append(resource)
        return resources

    def generate_resources(self):
        try:
            dir_path = QtWidgets.QFileDialog.getExistingDirectory(
                self, 'Select Directory')
            if dir_path:
                resources = self.generate_embedded_resources(dir_path)
                if not resources:
                    raise ValueError(
                        'The selected directory does not contain any valid files.')
                self.text_box.clear()
                for resource in resources:
                    self.text_box.appendPlainText(resource + '\n')
        except Exception as e:
            error_msg = f'Error: {e}'
            QtWidgets.QMessageBox.critical(self, 'Error', error_msg)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#2d2d2d'))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor('#3b3b3b'))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor('#2d2d2d'))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor('#3b3b3b'))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    app.setPalette(palette)

    window = EmbeddedResourceGenerator()
    window.show()

    app.exec_()
