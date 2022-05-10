from pyzbar import pyzbar
import argparse
import cv2

image = cv2.imread("horn.png")
# find the barcodes in the image and decode each of the barcodes
barcodes = pyzbar.decode(image)