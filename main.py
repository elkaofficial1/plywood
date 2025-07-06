import sys, os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QAction
import markdown

NOTES_DIR = os.path.expanduser("~/")

class Notes(QMainWindow):
    def __init__(self):
        self.current_file = None
        super().__init__()
        self.setWindowTitle("plywood")
        self.resize(1000, 1000)
        os.makedirs(NOTES_DIR, exist_ok=True)

        m = QFileSystemModel()
        m.setRootPath(NOTES_DIR)
        m.setNameFilters(["*.md"])
        m.setNameFilterDisables(False)
        t = QTreeView()
        t.setModel(m)
        t.setRootIndex(m.index(NOTES_DIR))
        [t.setColumnHidden(i, True) for i in range(1,4)]
        t.clicked.connect(self.open_note)
        self.m, self.t = m, t

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
        self.menu()

    def menu(self):
        fm = self.menuBar().addMenu("File")
        actions = [
            ("New Note", self.new_note),
        ]
        safe = [
            ("Save Note", self.save_note),
            ("Open Note", lambda: self.open_note(self.t.currentIndex())),
            ("Save As", lambda: self.save_note()), 
        ]
        actions.extend(safe)
        actions.append(("Exit", self.close))
         
        for n, f in actions:
            a = QAction(n, self)
            a.triggered.connect(f)
            fm.addAction(a)
            if n == "Delete":
                fm.addSeparator()
        # Добавим Help-меню
        help_menu = self.menuBar().addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self):
        QMessageBox.about(self, "About plywood", "Минималистичный markdown-блокнот на PySide6.\n(c) plywoodproject 2025")

    def new_note(self):
        name, ok = QInputDialog.getText(self, "New Note", "Note name:")
        if ok and name:
            p = os.path.join(NOTES_DIR, f"{name}.md")
            if os.path.exists(p):
                QMessageBox.warning(self, "Exists", "Note already exists.")
                return
            open(p, "w", encoding="utf-8").close()
            idx = self.m.index(p)
            self.t.setCurrentIndex(idx)
            self.open_note(idx)

    def open_note(self, idx):
        p = self.m.filePath(idx)
        if os.path.isfile(p):
            if hasattr(self, 'dirty') and self.dirty and self.current_file:
                if QMessageBox.question(self, "Unsaved", "Save changes?") == QMessageBox.Yes:
                    self.save_note()
            with open(p, "r", encoding="utf-8") as f:
                self.e.setPlainText(f.read())
            self.current_file, self.dirty = p, False
            self.update_preview()
        
    def save_note(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.e.toPlainText())
            self.dirty = False
            self.update_preview()
        else:
            QMessageBox.warning(self, "Error", "No note to save.")
            
    def update_preview(self):
        self.dirty = True
        self.p.setHtml(markdown.markdown(self.e.toPlainText()))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Notes()
    win.show()
    
    sys.exit(app.exec())
