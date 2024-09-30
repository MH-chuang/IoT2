import cv2
import os

def crop(file_name):
    x=7
    y=7
    w=80-7
    h=27-5
    img = cv2.imread(file_name,cv2.IMREAD_GRAYSCALE)
    crop_img = img[y:y+h, x:x+w]
    cv2.imwrite(file_name, crop_img)


def main():
    #this is for massive image to be cropped
    x=7
    y=7
    w=80-7
    h=27-5
    # load all img filenames
    img_filenames = os.listdir('./check_code')
    for img_filename in img_filenames:
        if '.png' not in img_filename:
            continue

        img = cv2.imread("check_code/{0}".format(img_filename),cv2.IMREAD_GRAYSCALE)
        crop_img = img[y:y+h, x:x+w]
        cv2.imwrite("check_code/{0}".format(img_filename), crop_img)

if __name__ == '__main__':
    main()