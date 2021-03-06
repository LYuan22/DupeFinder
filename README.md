# DupeFinder

I built this project in order to help some photographer friends out with some of their photo editing as they would often save multiple similar photos with filters on them or different resolutions that online duplicate searchers didn't find. 

This is a program that runs an average hashing algorithm to look for duplicate photos in folders. The GUI is written using PyQt5. 

My hashing algorithm takes the image, shrinks it down and converts the entire picture to black and white. This solves both the filter issue as well as the differing resolutions as it shrinks the image down to at maximum a 50x50 image (depending on the similarity level the user selects)

It then gets the average black/white value of the image and compares every pixel with this value to get a binary list which is used to identify similar images. 

**SETUP**

Download the DupeFinder.exe file and run it. 

Or if you don't trust me you can compile all the files into an exe with

`pip install pyinstaller`

`pyinstaller --onefile -w main.py`

then run the exe file in the dist folder

You should see this window

![54c0b0a0c7d284555eef5c5476c1027c](https://user-images.githubusercontent.com/10456113/126706813-8da843fd-ba42-4b08-9e70-bd6613ee6371.png)


Either hit Browse Folder or File -> Open Folder to select the folder you want to look for duplicates. 

Use the Similarity Slider in order to select the similarity you would like to set it to, then hit Find Duplicates to search the Folder you have selected. 

You should find a screen that looks like this.

![image](https://user-images.githubusercontent.com/10456113/126707717-b04ff06b-9479-4ba6-8554-8b98901d4861.png)

You can hit Show Image to open up the image in whatever image finder you have on your computer.

Use the checkboxes to select which files you would like to delete, and click Delete Selected when you are done
