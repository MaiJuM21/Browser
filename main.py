import json
import os
import atexit
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from urllib.parse import urlparse

history_file = "browser/history.json"
bookmarks_file = "browser/bookmarks.json"

def ensure_files_exist():
    if not os.path.exists(history_file):
        with open(history_file, 'w') as f:
            json.dump([], f)
    if not os.path.exists(bookmarks_file):
        with open(bookmarks_file, 'w') as f:
            json.dump([], f)

ensure_files_exist()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        ensure_files_exist()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setWindowIcon(QtGui.QIcon("browser_icon.png"))

        self.load_stylesheet()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.topToolbar = QtWidgets.QHBoxLayout()
        self.topToolbar.setObjectName("topToolbar")

        self.btnBack = QtWidgets.QPushButton(self.centralwidget)
        self.btnBack.setIcon(QtGui.QIcon("icons/back.png"))
        self.btnBack.setIconSize(QtCore.QSize(24, 24))

        self.btnForward = QtWidgets.QPushButton(self.centralwidget)
        self.btnForward.setIcon(QtGui.QIcon("icons/forward.png"))
        self.btnForward.setIconSize(QtCore.QSize(24, 24))

        self.btnRefresh = QtWidgets.QPushButton(self.centralwidget)
        self.btnRefresh.setIcon(QtGui.QIcon("icons/refresh.png"))
        self.btnRefresh.setIconSize(QtCore.QSize(24, 24))

        self.btnHome = QtWidgets.QPushButton(self.centralwidget)
        self.btnHome.setIcon(QtGui.QIcon("icons/home.png"))
        self.btnHome.setIconSize(QtCore.QSize(24, 24))

        self.Go = QtWidgets.QLineEdit(self.centralwidget)
        self.Go.setObjectName("Go")
        self.Go.setPlaceholderText("Enter URL here...")
        self.Go.setMinimumHeight(30)
        self.btnNewTab = QtWidgets.QPushButton(self.centralwidget)
        self.btnNewTab.setIcon(QtGui.QIcon("icons/new_tab.png"))
        self.btnNewTab.setIconSize(QtCore.QSize(24, 24))

        self.history = []

        self.btnHistory = QtWidgets.QPushButton(self.centralwidget)
        self.btnHistory.setIcon(QtGui.QIcon("icons/history.png"))
        self.btnHistory.setIconSize(QtCore.QSize(24, 24))
        self.topToolbar.addWidget(self.btnHistory)

        self.btnRemoveBookmark = QtWidgets.QPushButton(self.centralwidget)
        self.btnRemoveBookmark.setIcon(QtGui.QIcon("icons/remove_bookmark.png"))
        self.btnRemoveBookmark.setIconSize(QtCore.QSize(24, 24))
        self.topToolbar.addWidget(self.btnRemoveBookmark)

        self.btnAddBookmark = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddBookmark.setIcon(QtGui.QIcon("icons/bookmark.png"))
        self.btnAddBookmark.setIconSize(QtCore.QSize(24, 24))
        self.topToolbar.addWidget(self.btnAddBookmark)

        self.bookmarks = []
        self.bookmarksMenu = QtWidgets.QComboBox(self.centralwidget)
        self.topToolbar.addWidget(self.bookmarksMenu)

        self.topToolbar.addWidget(self.btnBack)
        self.topToolbar.addWidget(self.btnForward)
        self.topToolbar.addWidget(self.btnRefresh)
        self.topToolbar.addWidget(self.btnHome)
        self.topToolbar.addWidget(self.Go)
        self.topToolbar.addWidget(self.btnNewTab)

        self.verticalLayout.addLayout(self.topToolbar)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabsClosable(True)
        self.verticalLayout.addWidget(self.tabWidget)
        self.tabWidget.setMovable(True)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.Go.returnPressed.connect(self.navigate_to_url)
        self.btnBack.clicked.connect(self.go_back)
        self.btnForward.clicked.connect(self.go_forward)
        self.btnRefresh.clicked.connect(self.reload_page)
        self.btnHome.clicked.connect(self.go_home)
        self.btnNewTab.clicked.connect(lambda: self.add_new_tab())
        self.btnHistory.clicked.connect(self.show_history)
        self.btnAddBookmark.clicked.connect(self.add_to_bookmarks)
        self.bookmarksMenu.currentIndexChanged.connect(self.open_bookmark)
        self.btnRemoveBookmark.clicked.connect(self.remove_bookmark)


    





        self.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.home_url = "https://www.google.com"
        self.add_new_tab(QUrl(self.home_url))

        self.load_history_and_bookmarks()

        atexit.register(lambda: self.save_history_and_bookmarks())

    def load_stylesheet(self):
        with open("styles.css", "r") as f:
            stylesheet = f.read()
            QtWidgets.QApplication.instance().setStyleSheet(stylesheet)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Enhanced Web Browser"))

    def navigate_to_url(self):
        current_browser = self.tabWidget.currentWidget()
        url = self.Go.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        current_browser.setUrl(QUrl(url))

        self.history.append(url)

    def update_url(self, q):
        self.Go.setText(q.toString())

        url = q.toString()
        if url not in self.history:
            self.history.append(url)

    def go_home(self):
        current_browser = self.tabWidget.currentWidget()
        current_browser.setUrl(QUrl(self.home_url))

    def reload_page(self):
        current_browser = self.tabWidget.currentWidget()
        current_browser.reload()

    def go_back(self):
        current_browser = self.tabWidget.currentWidget()
        current_browser.back()

    def go_forward(self):
        current_browser = self.tabWidget.currentWidget()
        current_browser.forward()

    def add_new_tab(self, url=None):
        if url is None:
            url = QUrl(self.home_url)

        new_browser = QWebEngineView()
        new_browser.setUrl(url)

        i = self.tabWidget.addTab(new_browser, "New Tab")
        self.tabWidget.setCurrentIndex(i)
        new_browser.urlChanged.connect(lambda q: self.update_tab_title(new_browser))
        new_browser.urlChanged.connect(lambda q: self.update_url(q))

    def update_tab_title(self, browser):
        index = self.tabWidget.indexOf(browser)
        if index != -1:
            url = browser.url().toString()

            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            if domain.startswith("www."):
                domain = domain[4:]

            self.tabWidget.setTabText(index, domain)

    def close_tab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)

    def show_history(self):
        history_dialog = QtWidgets.QDialog()
        history_dialog.setWindowTitle("History")
        history_dialog.resize(400, 300)

        layout = QtWidgets.QVBoxLayout(history_dialog)

        history_list = QtWidgets.QListWidget(history_dialog)
        history_list.addItems(self.history)
        layout.addWidget(history_list)

        history_list.itemDoubleClicked.connect(self.open_history_link)

        btnClearHistory = QtWidgets.QPushButton("Clear History", history_dialog)
        btnClearHistory.clicked.connect(lambda: self.clear_history(history_list))
        layout.addWidget(btnClearHistory)

        history_dialog.exec_()

    def open_history_link(self, item):
        url = item.text()
        self.add_new_tab(QUrl(url))

    def clear_history(self, history_list):
        self.history.clear()
        history_list.clear()


    def add_to_bookmarks(self):
        current_browser = self.tabWidget.currentWidget()
        current_url = current_browser.url().toString()
        current_title = current_browser.page().title()

        parsed_url = urlparse(current_url)
        domain = parsed_url.netloc

        if domain.startswith("www."):
            domain = domain[4:]

        if current_url not in [bookmark['full_url'] for bookmark in self.bookmarks]:
            bookmark_data = {
                'full_url': current_url,
                'display_url': domain,
                'title': current_title
            }
            self.bookmarks.append(bookmark_data)
            self.bookmarksMenu.addItem(current_title, bookmark_data)

    def open_bookmark(self, index):
        if index >= 0:
            bookmark_data = self.bookmarksMenu.itemData(index)
            if bookmark_data:
                self.add_new_tab(QUrl(bookmark_data['full_url']))

    def remove_bookmark(self):
        selected_index = self.bookmarksMenu.currentIndex()

        if selected_index >= 0:
            bookmark_data = self.bookmarksMenu.itemData(selected_index)
            self.bookmarks = [bookmark for bookmark in self.bookmarks if bookmark['full_url'] != bookmark_data['full_url']]
            self.bookmarksMenu.removeItem(selected_index)

    def save_history_and_bookmarks(self):
        data = {
            'history': self.history,
            'bookmarks': [{'full_url': bookmark['full_url'], 'display_url': bookmark['display_url'], 'title': bookmark['title']} for bookmark in self.bookmarks]
        }

        with open('browser/browser_data.json', 'w') as f:
            json.dump(data, f)

    def load_history_and_bookmarks(self):
        if os.path.exists('browser/browser_data.json'):
            with open('browser/browser_data.json', 'r') as f:
                data = json.load(f)
                self.history = data.get('history', [])
                self.bookmarks = data.get('bookmarks', [])

                for bookmark in self.bookmarks:
                    self.bookmarksMenu.addItem(bookmark['title'], bookmark)

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
