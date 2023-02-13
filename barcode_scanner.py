# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

itemlist = {
    '5012345678900': 'item1',
    '0076950450479': 'item2'

}

priceList = {
    '5012345678900': '10',
    '0076950450479': '20'

}


def get_name(barcode_id):
    if barcode_id not in itemlist:
        return 'item not recognized'
    else:
        return itemlist[barcode_id]


def get_price(barcode_id):
    if barcode_id not in priceList:
        return 'nil'
    else:
        return itemlist[barcode_id]


def main():
    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    # vs = VideoStream(src=0).start()
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    # open the output CSV file for writing and initialize the set of
    # barcodes found thus far

    found = set()

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        # frame = imutils.resize(frame, width=400)
        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)

        # loop over the detected barcodes
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # draw the barcode data and barcode type on the image

            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # if the barcode text is currently not in our CSV file, write
            # the timestamp + barcode to disk and update the set
            if barcodeData not in found:
                csv = open('barcodes.txt', "w")

                csv.write(get_name(barcodeData) + "," +
                          get_price(barcodeData)+"\n")
                csv.flush()
                found.add(barcodeData)
                csv.close()
        # show the output frame
        # cv2.imshow("Barcode Scanner", frame)
        # open('barcodes.txt', 'w').close()
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # close the output CSV file do a bit of cleanup
    print("[INFO] cleaning up...")

    cv2.destroyAllWindows()
    vs.stop()


if __name__ == "__main__":
    main()
