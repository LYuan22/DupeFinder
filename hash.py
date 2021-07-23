from PIL import Image
import numpy


def _binary_array_to_hex(arr):
	#Converts Binary array into hex
	bit_string = ''.join(str(b) for b in 1 * arr.flatten())
	width = int(numpy.ceil(len(bit_string)/4))
	return '{:0>{width}x}'.format(int(bit_string, 2), width=width)


def average_hash(image, hash_size = 8, mean=numpy.mean):
	if hash_size < 2:
		raise ValueError("Hash size must be greater than or equal to 2")
	#shrinks image down to hash_size x hash_size
	image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
	# find average pixel value; 'pixels' is an array of the pixel values, ranging from 0 (black) to 255 (white)
	pixels = numpy.asarray(image)
	avg = mean(pixels)
	#Creation of bitstring
	hash = pixels > avg
	#Creates the hash
	return hash

def similarity(hash1, hash2):
	#checks number of differences between two arrays
	similarity = numpy.count_nonzero(hash1.flatten() != hash2.flatten())
	return similarity

def hash_equals(hash1, hash2):
	#checks if both arrays are equal
	return numpy.array_equal(hash1.flatten(), hash2.flatten())

def hash_to_hex(hash):
	string = _binary_array_to_hex(hash)
	return string