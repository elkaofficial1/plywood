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

    def update_preview(self):
        self.dirty = True
        self.p.setHtml(markdown.markdown(self.e.toPlainText()))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Notes()
    win.show()
    sys.exit(app.exec())