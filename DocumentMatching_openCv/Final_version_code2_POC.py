import cv2
import imutils
import fitz
import pytesseract
 
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def image_generation(pdffile_name):
    pdf_data = fitz.open(pdffile_name)
    for i in range(0,pdf_data.page_count):
        page = pdf_data.load_page(i)  # number of page
        pix = page.get_pixmap(matrix=fitz.Matrix(150/72,150/72))
        output = f"{pdffile_name}_{i}.png"
        pix.save(output)


def compare_images(actual_data,virtual_data):
    list_of_allmismatches=[]
    pdf_data = fitz.open(actual_data)
    for i in range(0,pdf_data.page_count):
        original = cv2.imread(f"{actual_data}_{i}.png")
        new = cv2.imread(f"{virtual_data}_{i}.png")
        diff = original.copy()
        cv2.absdiff(original, new, diff)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        #increasing the size of differences so we can capture them all
        for j in range(0, 3):
            dilated = cv2.dilate(gray.copy(), None, iterations= j+ 1)
        (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)
    # now we need to find contours in the binarised image
        cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts=cnts[::-1]
        for c in cnts:
            # fit a bounding box to the contour
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cropped = new[y:y + h, x:x + w]
            text = pytesseract.image_to_string(cropped)
            list_of_allmismatches.append(text)
        cv2.imwrite(f"updated_changes_{i}.png", new)
    
    return list_of_allmismatches


def getLogos(pdffile_name):
    # open the file
    pdf_file = fitz.open(pdffile_name)
    i=1
    number_of_logo=0
    for page_index in range(len(pdf_file)): 
        # get the page itself
        page = pdf_file[page_index]
        for image_index, img in enumerate(page.getImageList(), start=1):
            xref = img[0]
            #Drawing the image
            pix = fitz.Pixmap(pdf_file, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.writePNG(f"{pdffile_name}_logo_{i}.png")
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG(f"{pdffile_name}_logo_{i}.png")
                pix1 = None
            pix=None
            i+=1
            number_of_logo+=1
    return number_of_logo
            
            


# image_generation("cv1.pdf")

# image_generation("cv_doc1_changed.pdf")

final_mismatch=compare_images("cv1.pdf","cv_doc1_changed.pdf")
print(final_mismatch)

# number_of_logo=getLogos("cv1.pdf")

# print(number_of_logo)



