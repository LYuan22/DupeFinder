from PIL import Image
import math
import os
from image_funcs import check_ifimage, hash_rotate, get_image_size, dict_array_update

def similarity_to_hashsize(similarity):
    hash_size = 2 ** ((similarity + 1)/11)
    hash_size = math.sqrt(hash_size) + 0.6
    return int(hash_size)

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


#80% - 16
#90% - 32 9
#100% - 64 10

if __name__ == "__main__":
    directory = "Pictures"
    counter = 0
    duplicates, originals = find_duplicates(directory, 8)
    print(originals)
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
