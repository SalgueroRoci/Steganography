# hiddentext

Rocio Salguero

Program can open a JPG image and inputs a text (from command promt or  text file) and saves it in the image by manipulating the lsb of each RGB value starting from the bottom right pixel to top left. Counts the text length and converts to binary string, then converts the text to a binary string (ASCII/UTF-8). The text and length are concatenated and written into the program. When extracting the ordering is kept in mind. 
LSB ( Least significant bit ) is determined whether the number is even or odd. To change add 1 or -1 based on (-1)^bit. 

PIL libary used and developed using Python 3.5.

How to use:
Terminal run $pythom3 hidden.py
Save hidden text to image:
Choose a doe terminal input text
enter image to save it in
enter text 
image is saved as png in the same image name as the JPG entered

Choose text file input 
enter image to save it in
enter text file 
image is saved as png in the same image name as the JPG entered

Extract text from picture (PNG only) 
enter image file name 
text is printed out in the terminal. 
