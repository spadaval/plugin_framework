import logging
import numpy as np
import base64

logger = logging.getLogger(__name__)

try:
    import krita
    from krita import *
except:
    logger.warn("Failed to load krita")


def getActiveDocument():
    """
    Get the Active Krita Document
    """
    document = Krita.activeDocument()
    node = document.rootNode()
    return node


def getChildNodes(node):
    """
    Get a List of Nodes of document (e.g Vector Layer, Fill Layer, Mask Layer)
    """
    children = node.childNodes()
    firstChild = children[0]
    return firstChild


def grabImage(node, x, y, w, h):
    """
    Grab the image from Krita Layer, given coordinates
    Parameters
    x	x position from where to start reading
    y	y position from where to start reading
    w	row length to read
    h	number of rows to read
    """
    imageData = node.pixelData(x, y, w, h)
    return imageData


def getColorModel(node):
    return node.colorModel()


def get_image_to_numpy(imageData):
    """
    convert image to Numpy Array
    """
    raw_image = base64.decodebytes(imageData.toBase64())
    return np.frombuffer(raw_image, dtype=np.float64)


def get_numpy_to_image(numpyImage):
    """
    Convert image from Numpy array to Krita native QByteArray
    """
    img_base64_converted = base64.b64encode(numpyImage)
    img_conv = QByteArray()
    imageData_converted_back = img_conv.fromBase64(img_base64_converted)
    return imageData_converted_back


def set_layer_data(node, imageData, x, y, w, h):
    """
    Set Krita layer's data
    Parameters
    x	the x position to start writing from
    y	the y position to start writing from
    w	the width of each row
    h	the number of rows to write
    """
    return node.setPixelData(imageData, x, y, w, h)
