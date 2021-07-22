import os
from PIL import Image
from hash import average_hash
import math



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

#uses rotate img to check if any are just rotated copies
def hash_rotate(originals, img, hash_size):
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
def dict_array_update(dict, hash, element):
    if hash in dict: 
        temp = dict[hash]
        temp.append(element)
        dict[hash] = temp
    else:
        dict[hash] = [element]

def rotate_similarity_checker(orig, dupe):
    dupe_hash = average_hash(dupe, 50)
    orig_hash = average_hash(orig, 50)

    img90, img180, img270 = rotate_image(dupe) 
    dupe_hash90 = average_hash(img90, 50)
    dupe_hash180 = average_hash(img180, 50)
    dupe_hash270 = average_hash(img270, 50)

    least_hash = dupe_hash - orig_hash
    if dupe_hash90 - orig_hash < least_hash:
        least_hash = dupe_hash90 - orig_hash
    if dupe_hash180 - orig_hash < least_hash:
        least_hash = dupe_hash180 - orig_hash
    if dupe_hash270 - orig_hash < least_hash:
        least_hash = dupe_hash270 - orig_hash

    return least_hash

def similarity_to_hashsize(similarity):
    hash_size = 2 ** ((similarity + 1)/11)
    hash_size = math.sqrt(hash_size) + 0.6
    return int(hash_size*2)

def hashsize_to_similarity(hash_size):
    similarity = hash_size / 2
    similarity = (similarity - 0.6) ** 2
    similarity = math.log(similarity, 2)
    similarity = (similarity * 11) 
    return int(similarity)

def get_similarity(directory, orig, dupe):
    orig_image = Image.open(os.path.join(directory, orig))
    dupe_image = Image.open(os.path.join(directory, dupe))

    similarity = 100 - rotate_similarity_checker(orig_image, dupe_image)
    return str(similarity) + '%'


def find_duplicates(directory, hash_size):
    fnames = os.listdir(directory)
    originals = {}
    duplicates = {}
    #print("Finding Duplicates Now!\n")
    for image in fnames:
        path = os.path.join(directory, image)
        if check_ifimage(path) == True:
            with Image.open(path) as img:
                #Checks if rotated picture is in originals, otherwise gives normal temp_hash
                temp_hash = hash_rotate(originals, img, hash_size)

                if temp_hash in originals:
                    temp = originals[temp_hash]
                    #makes sure that the Original image is the one with higher resolution
                    if get_image_size(directory, image, temp):
                        originals[temp_hash] = temp
                        dict_array_update(duplicates, temp_hash, image)
                    else:
                        originals[temp_hash] = image
                        dict_array_update(duplicates, temp_hash, temp)
                else:
                    originals[temp_hash] = image
    return duplicates, originals


def delete_picture(directory, duplicate):
    space_saved = os.path.getsize(os.path.join(directory, duplicate))
    os.remove(os.path.join(directory, duplicate))
    return space_saved

def show_image(directory, name):
    path = os.path.join(directory, name)
    image = Image.open(path)
    image.show()

def get_size(directory, name):
    image = os.path.join(directory, name)
    return convert_size(os.path.getsize(image))

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])
