import sys, os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QAction
import markdown

NOTES_DIR = os.path.expanduser("~/")

class Notes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("plywood")
        self.resize(1200, 1080)
        os.makedirs(NOTES_DIR, exist_ok=True)

        # Создаем меню бар
        menubar = self.menuBar()
        
        # Меню "File"
        file_menu = menubar.addMenu("&File")
        
        # Меню "Help" с пунктом "About"
        help_menu = menubar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        m = QFileSystemModel()
        m.setRootPath(NOTES_DIR)
        m.setNameFilters(["*.md"])
        m.setNameFilterDisables(False)
        t = QTreeView()
        t.setModel(m)
        t.setRootIndex(m.index(NOTES_DIR))
        [t.setColumnHidden(i, True) for i in range(1,4)]
        # t.clicked.connect(self.open_note)

        self.e = QTextEdit()
        self.e.textChanged.connect(self.update_preview)
        self.p = QTextBrowser()
        self.p.setOpenExternalLinks(True)
        self.p.setStyleSheet("background:#222;color:#eee;font-size:16px;")
        
        s = QSplitter()
        s2 = QSplitter(Qt.Horizontal)
        s.addWidget(t)
        s2.addWidget(self.e)
        s2.addWidget(self.p)
        s.addWidget(s2)
        self.setCentralWidget(s)
        
        self.m, self.t = m, t
        self.current_file, self.dirty = None, False
    
    def show_about(self):
        """Показывает окно 'About'"""
        about_text = """
        <h2>plywood</h2>
        <p>Простой Markdown редактор</p>
        <p>Версия 1.0</p>
        <p>© 2023</p>
        """
        QMessageBox.about(self, "About plywood", about_text)
    
    def update_preview(self):
        self.dirty = True
        self.p.setHtml(markdown.markdown(self.e.toPlainText()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Notes()
    win.show()
    sys.exit(app.exec())
