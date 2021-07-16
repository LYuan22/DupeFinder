from PIL import Image
from hash import average_hash
import os
from image_funcs import check_ifimage, rotate_checker, get_image_size, _dict_array_update


#maybe change originals to hash so that multiple originals go under the same table
def find_duplicates(directory, hash_size):
    fnames = os.listdir(directory)
    originals = {}
    duplicates = {}
    print("Finding Duplicates Now!\n")
    for image in fnames:
        path = os.path.join(directory, image)
        if check_ifimage(path) == True:
            with Image.open(path) as img:
                #Checks if rotated picture is in originals, otherwise gives normal temp_hash
                temp_hash = rotate_checker(originals, img, hash_size)

                if temp_hash in originals:
                    temp = originals[temp_hash]
                    #makes sure that the Original image is the one with higher resolution
                    if get_image_size(directory, image, temp):
                        originals[temp_hash] = temp
                        _dict_array_update(duplicates, temp_hash, image)
                    else:
                        originals[temp_hash] = image
                        _dict_array_update(duplicates, temp_hash, temp)
                else:
                    originals[temp_hash] = image
    return duplicates, originals


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
    directory = "Pictures"
    counter = 0
    duplicates, originals = find_duplicates(directory, 8)
    hashes = originals.keys()
    for key in hashes:
        if key in duplicates:
            dupes = duplicates[key]
            print("Original: {}".format(originals[key]))
            for i in dupes:
                print("Duplicate: {}".format(i))
                counter = counter + 1
            print()
    if counter == 0:
        print("No Duplicates Found")
