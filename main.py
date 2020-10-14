import os
import sys

from PySide2 import QtCore, QtGui, QtQuick

from data_source import DataSource

if __name__ == "__main__":
    app = QtGui.QGuiApplication(sys.argv)
    view = QtQuick.QQuickView()
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
    data_source = DataSource()

    view.rootContext().setContextProperty("dataSource", data_source)
    qml_file = os.path.join(os.path.dirname(__file__), "main.qml")
    view.setSource(QtCore.QUrl.fromLocalFile(os.path.abspath(qml_file)))

    if view.status() == QtQuick.QQuickView.Error:
        sys.exit(-1)
    view.show()

    app.exec_()
    del view
