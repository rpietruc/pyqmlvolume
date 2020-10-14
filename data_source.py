import ctypes

from PySide2 import QtCore, QtGui
from PySide2.QtDataVisualization import QtDataVisualization


class DataSource(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self._volume = None

    @QtCore.Slot(QtDataVisualization.QCustom3DVolume)
    def fillVolume(self, volume):
        index = 0
        textureSize = 128
        midPoint = QtGui.QVector3D(float(textureSize) / 2.0,
                                   float(textureSize) / 2.0,
                                   float(textureSize) / 2.0)

        textureData = (ctypes.c_ubyte * int(textureSize *
                                            textureSize *
                                            textureSize / 2))()
        for i in range(textureSize):
            for j in range(int(textureSize / 2)):
                for k in range(textureSize):
                    colorIndex = 0
                    # Take a section out of the ellipsoid
                    if i >= textureSize / 2 or \
                       j >= textureSize / 4 or \
                       k >= textureSize / 2:
                        distVec = QtGui.QVector3D(float(k),
                                                  float(j * 2),
                                                  float(i)) - midPoint
                        adjLen = min(255.0, (distVec.length() * 512.0
                                             / float(textureSize)))
                        colorIndex = int(255 - int(adjLen))
                    textureData[index] = ctypes.c_ubyte(colorIndex)
                    index += 1

        volume.setScaling(QtGui.QVector3D(1.0, 1.0, 1.0))
        volume.setTextureWidth(textureSize)
        volume.setTextureHeight(int(textureSize / 2))

        # todo: causes Segmentation fault (core dumped)
        # volume.setTextureDepth(textureSize)

        volume.setTextureFormat(QtGui.QImage.Format_Indexed8)

        # todo: causes Segmentation fault (core dumped)
        # volume.setTextureData(textureData)

        colorTable = [QtGui.qRgba(0, 0, 0, 0)] * 256
        for i in range(256):
            if i < 15:
                colorTable[i] = QtGui.qRgba(0, 0, 0, 0)
            elif i < 60:
                colorTable[i] = QtGui.qRgba((i * 2) + 120, 0, 0, 15)
            elif i < 120:
                colorTable[i] = QtGui.qRgba(0, ((i - 60) * 2) + 120, 0, 50)
            elif i < 180:
                colorTable[i] = QtGui.qRgba(0, 0, ((i - 120) * 2) + 120, 255)
            else:
                colorTable[i] = QtGui.qRgba(i, i, i, 255)

        volume.setColorTable(colorTable)
