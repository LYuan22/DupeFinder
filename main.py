from PIL import Image
import imagehash
import os
import numpy as np


def find_duplicates(directory):
    fnames = os.listdir(directory)
    image_dict = {}
    duplicates = []
    print("Finding Duplicates Now!\n")
    for image in fnames:
        path = os.path.join(directory, image)
        with Image.open(path) as img:
            temp_hash = imagehash.average_hash(img, 8)  #hashsize 8
            if temp_hash in image_dict:
                #makes sure that the Original image is the one with higher resolution
                if get_image_size(directory, image, image_dict[temp_hash]):
                    print("Duplicate: {} \nOriginal: {}!\n".format(
                        image, image_dict[temp_hash]))
                    duplicates.append(image)
                else:
                    print("Duplicate: {} \nOriginal: {}!\n".format(
                        image_dict[temp_hash], image))
                    duplicates.append(image_dict[temp_hash])
                    image_dict[temp_hash] = image
            else:
                image_dict[temp_hash] = image

    if len(duplicates) != 0:
        return duplicates
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


# Remove Duplicates

directory = "Pictures"
duplicates = find_duplicates(directory)
print(duplicates)