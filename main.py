import sys, os
from PySide6.QtCore import Qt, QCoreApplication, QMetaObject, QRect
from PySide6.QtWidgets import * 
from PySide6.QtGui import QAction
import markdown

NOTES_DIR = os.path.expanduser("~/")

class Notes(QMainWindow):
    def __init__(self):
        self.current_file = None
        super().__init__()
        self.setWindowTitle("plywood")
        self.resize(1000, 900)
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
        self.move(
        self.screen().availableGeometry().center() - 
        self.rect().center()
        )
    def show_ui_dialog(self):
        dialog = QDialog(self)  
        ui = Ui_Dialog()
        ui.setupUi(dialog)     
        dialog.exec()  
    
    def menu(self):
        fm = self.menuBar().addMenu("File")
        fm1 = self.menuBar().addMenu("settings")
        
        actions = [
            ("New Note", self.new_note),
            ("Save Note", self.save_note),
            ("Open Note", lambda: self.open_note(self.t.currentIndex())),
            ("Save As", lambda: self.save_note()),
            ("Delete", lambda: self.m.remove(self.t.currentIndex())),
            ("about", self.show_about),
        ]
        
        actions1 = [
            ("norm", self.show_ui_dialog),
        ]
        
        settings = [
            ("settings", self.show_ui_dialog)]
        
        actions1.extend(settings)
        
        actions.append(("Exit", self.close))
         
        for n, f in actions:
            a = QAction(n, self)
            a.triggered.connect(f)
            fm.addAction(a)
            if n == "Delete":
                fm.addSeparator()

        for n, f in actions1:
            a = QAction(n, self)
            a.triggered.connect(f)
            fm1.addAction(a)

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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"settings")
        Dialog.resize(400, 300)
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 10, 102, 271))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton_4 = QPushButton(self.widget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.verticalLayout.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.verticalLayout.addWidget(self.pushButton_5)

        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout.addWidget(self.pushButton_3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u043e\u0441\u043d\u043e\u0432\u043d\u044b\u0435", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
        self.pushButton_4.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
        self.pushButton_5.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
    # retranslateUi

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Notes()
    win.show()
    
    sys.exit(app.exec())
