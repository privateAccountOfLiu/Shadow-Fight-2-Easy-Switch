from PyQt6 import QtWidgets, QtGui, uic
from functions import *


def add_file(regulation: str, file_label: QtWidgets.QLabel, btn: QtWidgets.QPushButton):
    file_dia: QtWidgets.QFileDialog = QtWidgets.QFileDialog()
    file_dia.setNameFilter(regulation)
    if file_dia.exec():
        file_label.setText(str(file_dia.selectedFiles()[0]))
    btn.clicked.disconnect()
    file_dia.close()


def build_page_obj_to_xml_signal1(ori_ui):
    file_label: QtWidgets.QLabel = ori_ui.label_2
    if file_name := file_label.text():
        config = {
            'x': [float(ori_ui.doubleSpinBox.text()), float(ori_ui.doubleSpinBox_2.text())],
            'y': [float(ori_ui.doubleSpinBox_3.text()), float(ori_ui.doubleSpinBox_4.text())],
            'z': [float(ori_ui.doubleSpinBox_5.text()), float(ori_ui.doubleSpinBox_6.text())],
            'type': ori_ui.comboBox_4.currentText(),
            'rotate_method': ori_ui.comboBox.currentText(),
            'is_zoom': True if ori_ui.comboBox_2.currentText() == 'True' else False,
            'is_draw_edge': True if ori_ui.comboBox_3.currentText() == 'True' else False
        }
        obj = edit_obj_data(config, file_name)
        write_xml(config, obj)
    file_label.clear()
    ori_ui.buttonBox.accepted.disconnect()
    ori_ui.close()


def build_page_obj_to_xml_signal2(ori_ui):
    ori_ui.label_2.clear()
    ori_ui.buttonBox.rejected.disconnect()
    ori_ui.close()


def build_page_objs_to_py_signal1(ori_ui):
    config = {
        'x': [float(ori_ui.doubleSpinBox.text()), float(ori_ui.doubleSpinBox_2.text())],
        'y': [float(ori_ui.doubleSpinBox_3.text()), float(ori_ui.doubleSpinBox_4.text())],
        'z': [float(ori_ui.doubleSpinBox_5.text()), float(ori_ui.doubleSpinBox_6.text())],
        'rotate_method': ori_ui.comboBox.currentText(),
        'is_zoom': True if ori_ui.comboBox_2.currentText() == 'True' else False,
    }
    write_py_bin(config)
    ori_ui.buttonBox.accepted.disconnect()
    ori_ui.close()


def build_page_objs_to_py_signal2(ori_ui):
    ori_ui.buttonBox.rejected.disconnect()
    ori_ui.close()


def build_page_bin_to_py_signal1(ori_ui):
    file_label: QtWidgets.QLabel = ori_ui.label_2
    scale: QtWidgets.QDoubleSpinBox = ori_ui.doubleSpinBox
    if file_name := file_label.text():
        config = {'bin_shape_arg': float(scale.text())}
        move_bin = edit_bin_data(config, file_name)
        bin_decode(move_bin)
    file_label.clear()
    ori_ui.buttonBox.accepted.disconnect()
    ori_ui.close()


def build_page_bin_to_py_signal2(ori_ui):
    ori_ui.label_2.clear()
    ori_ui.buttonBox.rejected.disconnect()
    ori_ui.close()


def build_page_py_to_bin_signal1(ori_ui):
    file_label: QtWidgets.QLabel = ori_ui.label_2
    if file_name := file_label.text():
        bin_encode(file_name)
    file_label.clear()
    ori_ui.buttonBox.accepted.disconnect()
    ori_ui.close()


def build_page_py_to_bin_signal2(ori_ui):
    ori_ui.label_2.clear()
    ori_ui.buttonBox.rejected.disconnect()
    ori_ui.close()


def build_page_obj_to_xml(ori_ui):
    file_btn: QtWidgets.QPushButton = ori_ui.pushButton
    ok_btn: QtWidgets.QDialogButtonBox = ori_ui.buttonBox
    file_label: QtWidgets.QLabel = ori_ui.label_2
    file_btn.clicked.connect(lambda: add_file('*.obj', file_label, file_btn))
    ok_btn.accepted.connect(lambda: build_page_obj_to_xml_signal1(ori_ui))
    ok_btn.rejected.connect(lambda: build_page_obj_to_xml_signal2(ori_ui))


def build_page_objs_to_py(ori_ui):
    ok_btn: QtWidgets.QDialogButtonBox = ori_ui.buttonBox
    ok_btn.accepted.connect(lambda: build_page_objs_to_py_signal1(ori_ui))
    ok_btn.rejected.connect(lambda: build_page_objs_to_py_signal2(ori_ui))


def build_page_bin_to_py(ori_ui):
    file_btn: QtWidgets.QPushButton = ori_ui.pushButton
    ok_btn: QtWidgets.QDialogButtonBox = ori_ui.buttonBox
    file_label: QtWidgets.QLabel = ori_ui.label_2
    file_btn.clicked.connect(lambda: add_file('*.bin', file_label, file_btn))
    ok_btn.accepted.connect(lambda: build_page_bin_to_py_signal1(ori_ui))
    ok_btn.rejected.connect(lambda: build_page_bin_to_py_signal2(ori_ui))


def build_page_py_to_bin(ori_ui):
    file_btn: QtWidgets.QPushButton = ori_ui.pushButton
    ok_btn: QtWidgets.QDialogButtonBox = ori_ui.buttonBox
    file_label: QtWidgets.QLabel = ori_ui.label_2
    file_btn.clicked.connect(lambda: add_file('*.py', file_label, file_btn))
    ok_btn.accepted.connect(lambda: build_page_py_to_bin_signal1(ori_ui))
    ok_btn.rejected.connect(lambda: build_page_py_to_bin_signal2(ori_ui))


def show_subpages(index, pages, funcs):
    funcs[index](pages[index])
    pages[index].show()


def build_ui(ori_ui, pages, funcs):
    for page in pages:
        page.setWindowIcon(QtGui.QIcon(get_dir('./ui/Image.png')))
    obj_to_xml_btn: QtWidgets.QPushButton = ori_ui.pushButton_3
    obj_to_xml_btn.clicked.connect(lambda: show_subpages(0, pages, funcs))
    objs_to_py_btn: QtWidgets.QPushButton = ori_ui.pushButton
    objs_to_py_btn.clicked.connect(lambda: show_subpages(1, pages, funcs))
    bin_to_py_btn: QtWidgets.QPushButton = ori_ui.pushButton_4
    bin_to_py_btn.clicked.connect(lambda: show_subpages(2, pages, funcs))
    py_to_bin_btn: QtWidgets.QPushButton = ori_ui.pushButton_5
    py_to_bin_btn.clicked.connect(lambda: show_subpages(3, pages, funcs))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    make_dir()
    ui_main = uic.loadUi(get_dir('./ui/main_page.ui'))
    ui_main.setWindowIcon(QtGui.QIcon(get_dir('./ui/Image.png')))
    sub_pages = [uic.loadUi(get_dir('./ui/obj_to_xml_page.ui')),
                 uic.loadUi(get_dir('./ui/objs_to_py.ui')),
                 uic.loadUi(get_dir('./ui/bin_to_py.ui')),
                 uic.loadUi(get_dir('./ui/py_to_bin.ui'))]
    sub_funcs = [build_page_obj_to_xml,
                 build_page_objs_to_py,
                 build_page_bin_to_py,
                 build_page_py_to_bin]
    build_ui(ui_main, sub_pages, sub_funcs)
    ui_main.show()
    sys.exit(app.exec())
