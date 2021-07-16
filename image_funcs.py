import os
from PIL import Image
from hash import average_hash



#function gets the size of both images, returns True if image2 is larger
def get_image_size(dir, image1, image2):
    size1 = os.stat(os.path.join(dir, image1)).st_size
    size2 = os.stat(os.path.join(dir, image2)).st_size
    if size1 < size2:
        return True
    else:
        return False

#rotates image to ensure that the images arent just rotations of previos images 
def rotate_image(img):
    img90 = img.transpose(Image.ROTATE_90)
    img180 = img90.rotate(Image.ROTATE_90)
    img270 = img180.rotate(Image.ROTATE_90)
    return img90, img180, img270

#uses rotateimg to 
def rotate_checker(originals, img, hash_size):
    temp_hash = average_hash(img, hash_size)

    img90, img180, img270 = rotate_image(img) 
    temp_hash90 = average_hash(img90, hash_size)
    temp_hash180 = average_hash(img180, hash_size)
    temp_hash270 = average_hash(img270, hash_size)

    if temp_hash90 in originals:
        temp_hash = temp_hash90
    elif temp_hash180 in originals:
        temp_hash = temp_hash180
    elif temp_hash270 in originals:
        temp_hash = temp_hash270
    return temp_hash
    

#ignores files that are not some sort of image
def check_ifimage(path):
    try:
        Image.open(path)
    except IOError:
        return False
    return True

#Creates array under a dictionary by hash and updates it when needed
def _dict_array_update(dict, hash, element):
    if hash in dict: 
        temp = dict[hash]
        temp.append(element)
        dict[hash] = temp
    else:
        dict[hash] = [element]