from PIL import Image
from hash import average_hash
import os
import numpy as np


#maybe change originals to hash so that multiple originals go under the same table
#add hash size as a 'degree of similarity' for the algorithm'


def find_duplicates(directory):
    fnames = os.listdir(directory)
    image_dict = {}
    duplicates = []
    originals = []
    print("Finding Duplicates Now!\n")
    for image in fnames:
        path = os.path.join(directory, image)
        if check_ifimage(path) == True:
            with Image.open(path) as img:

                img90, img180, img270 = rotate_image(img)

                temp_hash = average_hash(img, 8)
                temp_hash90 = average_hash(img90, 8)
                temp_hash180 = average_hash(img180, 8)
                temp_hash270 = average_hash(img270, 8)#move these to if statement

                if temp_hash90 in image_dict:
                    temp_hash = temp_hash90
                elif temp_hash180 in image_dict:
                    temp_hash = temp_hash180
                elif temp_hash270 in image_dict:
                    temp_hash = temp_hash270


                if temp_hash in image_dict:
                    #makes sure that the Original image is the one with higher resolution
                    if get_image_size(directory, image, image_dict[temp_hash]):
                        duplicates.append(image)
                        originals.append(image_dict[temp_hash])
                    else:
                        duplicates.append(image_dict[temp_hash])
                        originals.append(image)
                        image_dict[temp_hash] = image
                else:
                    image_dict[temp_hash] = image

    if len(duplicates) != 0:
        return duplicates, originals
    else:
        print("No Duplicates Found")
        return None

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

#ignores files that are not some sort of image
def check_ifimage(path):
    try:
        Image.open(path)
    except IOError:
        return False
    return True

""" DELETE STUFF (RIPPED FORM OLD THING)
a = input("Do you want to delete these {} Images? Press Y or N:  ".format(len(duplicates)))
space_saved = 0
if(a.strip().lower() == "y"):
    for duplicate in duplicates:
        space_saved += os.path.getsize(os.path.join(self.directory,duplicate))        
        os.remove(os.path.join(self.directory,duplicate))
        print("{} Deleted Succesfully!".format(duplicate))
    
    print("\n\nYou saved {} mb of Space!".format(round(space_saved/1000000),2))
else:
    """


if __name__ == "__main__":
    directory = "vyvan"
    duplicates, originals = find_duplicates(directory)
    for i in range(len(duplicates)):
         print("Duplicate: {} \nOriginal: {}!\n".format(
                        duplicates[i], originals[i]))
    print(duplicates)
    print(originals)