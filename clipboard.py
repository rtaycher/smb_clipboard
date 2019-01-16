import json
import os
import socket
import sys
from pathlib import Path

from PySide2.QtCore import QStringListModel, QStandardPaths
from PySide2.QtGui import QClipboard
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QListView, QLineEdit, \
    QDesktopWidget, QHBoxLayout, QPushButton, QFileDialog

_dir = Path(__file__).absolute().parent


class ClipboardManager:
    def __init__(self):
        self.clips = []
        self.clipboard_save_dir = _dir / "clip"
        self.app_settings_file = Path(
            QStandardPaths.writableLocation(QStandardPaths.GenericConfigLocation)) / "network_clipboard_settings.json"
        if self.app_settings_file.exists():
            self.clipboard_save_dir = Path(json.loads(self.app_settings_file.read_text())["clipboard_save_dir"])

        self.hostname = socket.gethostname()
        self.clipboard_save_file = self.clipboard_save_dir / f"{self.hostname}.clips.json"

    def read_clips_on_start(self):
        for json_filepath in self.clipboard_save_dir.glob("*.clips.json"):
            with json_filepath.open() as f:
                self.clips += json.load(f)
        self.clips = list(set(self.clips))
        self.clips_model.setStringList(self.clips)

    def on_clip(self, mode):
        print(f'on_clip mode:{mode}')
        if mode == QClipboard.Mode.Clipboard:
            self.save_clipboard_contents_and_update_gui()

    def update_save_folder(self, new_save_folder):
        new_save_folder_path = Path(new_save_folder)
        if new_save_folder_path.exists():
            self.app_settings_file.write_text(json.dumps(dict(clipboard_save_dir=new_save_folder)))
            self.clipboard_save_dir = new_save_folder_path
            self.clipboard_save_file = self.clipboard_save_dir / f"{self.hostname}.clips.json"

    def pick_save_folder(self):
        self.update_save_folder(QFileDialog.getExistingDirectory(self.window,
                                                                      "Pick shared network folder to sync clipboards",
                                                                      os.fspath(Path.home()), 0))

    def save_clipboard_contents_and_update_gui(self):
        last_clipboard_contents = self.clipboard.text(QClipboard.Mode.Clipboard)
        self.clips.insert(0, last_clipboard_contents)
        self.clips_model.setStringList(self.clips)
        print(f'new clipboard contents: {last_clipboard_contents}')
        self.clipboard_save_dir.mkdir(parents=True, exist_ok=True)
        with open(self.clipboard_save_file, 'w') as f:
            json.dump(self.clips, f)

    def run(self):
        app = QApplication(sys.argv)
        self.clipboard = app.clipboard()
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.clipboard_save_dir_line_widget = QLineEdit()
        self.clipboard_save_dir_line_widget.setText(os.fspath(self.clipboard_save_dir))
        self.clipboard_save_dir_line_widget.textChanged.connect(self.update_save_folder)
        self.launch_file_dialog_button = QPushButton()
        self.launch_file_dialog_button.clicked.connect(self.pick_save_folder)
        self.clips_view = QListView()
        self.clips_model = QStringListModel()
        self.clips_view.setModel(self.clips_model)
        self.read_clips_on_start()
        self.save_folders_label = QLabel("clipboard network saves folder")
        self.layout.addWidget(self.save_folders_label)
        line = QWidget()
        line.setLayout(QHBoxLayout())
        line.layout().addWidget(self.clipboard_save_dir_line_widget)
        line.layout().addWidget(self.launch_file_dialog_button)
        self.layout.addWidget(line)
        self.layout.addWidget(self.clips_view)
        self.window.setLayout(self.layout)
        self.clipboard.changed.connect(self.on_clip)
        self.window.resize(QDesktopWidget().availableGeometry(self.window).size() * 0.5)
        self.window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    ClipboardManager().run()
