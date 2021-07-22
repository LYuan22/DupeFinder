from image_funcs import check_ifimage, hash_rotate, get_image_size, dict_array_update, rotate_similarity_checker, \
                        similarity_to_hashsize, hashsize_to_similarity, get_similarity, find_duplicates, delete_picture, show_image, get_size, convert_size




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
