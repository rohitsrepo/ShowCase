import sys
import cv2
import numpy as np
import os.path
import multiprocessing
from itertools import starmap

NBHD_SIZE = 19
UNSHARP_T = 48
ADAPT_T   = 24
INVERT = True
ASPECT = 8.5/11.0


def processImage(fname):
    source = cv2.imread(fname, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    cv2.imwrite(rename(fname, "gray"), source)
    if INVERT:
        source = 255 - source
    return bitone(source, fname)

def bitone(image, fname):
    blur = cv2.blur(image,(NBHD_SIZE,NBHD_SIZE))
    diff = cv2.absdiff(image, blur)
    _,mask = cv2.threshold(blur,UNSHARP_T,1,cv2.THRESH_BINARY)
    blur = cv2.multiply(blur,mask)
    sharpened = cv2.addWeighted(image,2,blur,-1,0)
    thresh = cv2.adaptiveThreshold(sharpened, 255,
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY,
                                   NBHD_SIZE, ADAPT_T)
    return thresh

def findPaper(image):
    squares = []
    # Blur image to emphasize bigger features.
    blur = cv2.blur(image,(2,2))
    retval, edges = cv2.threshold(blur,0,255,
                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(edges,
                                    cv2.RETR_LIST,
                                    cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        clen = cv2.arcLength(c,True)
        c = cv2.approxPolyDP(c,0.02*clen,True)
        area = abs(cv2.contourArea(c))
        if len(c) == 4 and \
           0.1*edges.size <= area <= 0.9*edges.size and \
           cv2.isContourConvex(c):
                squares.append(c)
    return max(squares,key=lambda s: cv2.arcLength(s,True))

def warpSheet(image):
    '''
    Automatically crops an image to paper size if possible.
    '''
    try:
        sheet = findPaper(image)
    except ValueError:
        return image
    h, w = image.shape
    src = sheet[::,0,::].astype('float32')
    # Compute distances from topleft corner (0,0)
    # to find topleft and bottomright
    d = np.sum(np.abs(src)**2,axis=-1)**0.5
    t_l = np.argmin(d)
    b_r = np.argmax(d)
    # Compute distances from topright corner (w,0)
    # to find topright and bottomleft
    y = np.array([[w,0],]*4)
    d = np.sum(np.abs(src-y)**2,axis=-1)**0.5
    t_r = np.argmin(d)
    b_l = np.argmax(d)
    #Now assemble these together
    if h >= w:
        destH, destW = h, int(h*ASPECT)
    else:
        destW, destH = h, int(h*ASPECT)
    dest = np.zeros(src.shape,dtype='float32')
    dest[t_l] = np.array([0,0])
    dest[t_r] = np.array([destW,0])
    dest[b_l] = np.array([0,destH])
    dest[b_r] = np.array([destW,destH])
    transform = cv2.getPerspectiveTransform(src,dest)
    return cv2.warpPerspective(image,transform,(destW,destH))


def rename(originalName, suffix):
    file_path, file_name = os.path.split(originalName)
    name, extension = os.path.splitext(file_name)
    return os.path.join(file_path, '{0}_{1}{2}'.format(name, suffix, extension))


def GrayScaleAndSketch(source_file_path):
    processed = processImage(source_file_path)
    newnames = rename(source_file_path, "outline")
    cv2.imwrite(newnames, processed)


def FilterG(source_file_path):
    source_image = cv2.imread(source_file_path)
    b, g, r = cv2.split(source_image)

    for i in range(0, g.shape[0]):
        for j in range(0, g.shape[1]):
            g[i][j] = 0

    new_image = cv2.merge([b, g, r])
    cv2.imwrite(rename(source_file_path, "withoutGreen"), new_image)


def FilterB(source_file_path):
    source_image = cv2.imread(source_file_path)
    b, g, r = cv2.split(source_image)

    for i in range(0, b.shape[0]):
        for j in range(0, b.shape[1]):
            b[i][j] = 0

    new_image = cv2.merge([b, g, r])
    cv2.imwrite(rename(source_file_path, "withoutBlue"), new_image)


def FilterR(source_file_path):
    source_image = cv2.imread(source_file_path)
    b, g, r = cv2.split(source_image)

    for i in range(0, r.shape[0]):
        for j in range(0, r.shape[1]):
            r[i][j] = 0

    new_image = cv2.merge([b, g, r])
    cv2.imwrite(rename(source_file_path, "withoutRed"), new_image)
