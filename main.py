from PIL import Image
import imagehash
import os
import numpy as np


def find_duplicates(self):
    fnames = os.listdir(dirname)
    hashes = {}
    duplicates = []
    print("Finding Duplicates Now!\n")
    for image in fnames:
        with Image.open(os.path.join(dirname, image)) as img:
            temp_hash = imagehash.average_hash(img, 8)  # hashsize 8
            if temp_hash in hashes:
                print("Duplicate {} \nfound for Image {}!\n".format(
                    image, hashes[temp_hash]))
                duplicates.append(image)
            else:
                hashes[temp_hash] = image

    if len(duplicates) != 0:
        return duplicates
    else:
        print("No Duplicates Found :(")
        return None

            
        
"""
a = input("Do you want to delete these {} Images? Press Y or N:  ".format(len(duplicates)))
space_saved = 0
if(a.strip().lower() == "y"):
    for duplicate in duplicates:
        space_saved += os.path.getsize(os.path.join(self.dirname,duplicate))        
        os.remove(os.path.join(self.dirname,duplicate))
        print("{} Deleted Succesfully!".format(duplicate))
    
    print("\n\nYou saved {} mb of Space!".format(round(space_saved/1000000),2))
else:
    """


# Remove Duplicates

dirname = "Pictures"
duplicates = find_duplicates(dirname)
