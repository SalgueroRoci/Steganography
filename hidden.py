'''
Programmer: Rocio Salguero 
Date: 03/29/18

Github: https://github.com/SalgueroRoci/Steganography
Program:
Hide a rext in am image in the R,G,B using the least significant bit of each byte.
Acccepts a JPG file to hide a text and outputs a PNG with the hidden text. 
To retrieve a text input is a PNG and prints out the text

Steganography is the study of hiding data (text, images, audio, etc.) within data (text,
images, audio, etc.). Some uses of steganography are exchanging hidden messages,
watermarking, or exfiltrate data from a network.

#References:
	https://stackoverflow.com/questions/40557335/binary-to-string-text-in-python
	http://web.math.princeton.edu/math_alive/1/Lab1/Conversion.html
	https://stackoverflow.com/questions/36468530/changing-pixel-color-value-in-pil
	https://stackoverflow.com/questions/3596433/is-it-possible-to-change-the-color-of-one-individual-pixel-in-python
	https://stackoverflow.com/questions/10411085/converting-integer-to-binary-in-python
	https://stackoverflow.com/questions/18815820/convert-string-to-binary-in-python
'''

from PIL import Image as PilImage
import sys

def writeToImage(imageJPG, text, outname): 
	width, height = imageJPG.size 
	manipImg = imageJPG.load()
	count = len(text)-1
	newImg = outname.split(".")[0] + ".png" 
	
	#Check if text fits 
	if (width * height - 11)*3 < len(text): 
		input("Text too big for photo. Closing...Press any key.") 
		sys.exit() 
	
	#start from bottom right to top left 
	for y in range(height-1, -1, -1): 
		for x in range(width-1, -1, -1):
			colors = manipImg[x,y]
			newColors = [0,0,0]		
			
			for z in range(0,3):
				lsb = colors[z] % 2
				if(lsb != int(text[count]) ):
					val = (-1) ** lsb 
					newColors[z] = int(colors[z]) + val
				count -= 1 
				if(count < 0): 
					manipImg[x,y] = tuple(newColors)
					imageJPG.save(newImg) 
					return 
			manipImg[x,y] = tuple(newColors)
	
	
	imageJPG.save(newImg) 

#convert a byte string to char 
def bits2string(s=''):
	return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

#Read the text length in the first 11 pixels. 
def readLength(readImg, size): 
	width, height = size
	txt = ""
	count = 0
	for y in range(height-1, -1, -1): 
		for x in range(width-1, -1, -1):
			count += 1 
			colors = readImg[x,y]	
			for z in range(0,3):
				val = colors[z]
				if(count <= 11): 	
					if(val % 2 == 0): 
						txt = '0' + txt 
					else: 
						txt = '1' + txt 
				else:
					return  (int(txt, 2), x , y ) 
 
#read the text based on the length read before. read the lsb in R,G,B of each pixel	
def readText(readImg, size, widthStart, heightStart, length):
	txt = ""
	width, height = size
	max = length*8+33
	
	for y in range(height-1, -1, -1):
		for x in range(width-1, -1, -1):
			colors = readImg[x,y]	
			for z in range(0,3):			  
				val = colors[z] 				
				if(val % 2 == 0): 
					txt = '0' + txt 
				else: 
					txt = '1' + txt
				if(len(txt) == max): return txt[:-33]		



#============ Main ==============
print("Steganography - hiding text in and image or extracting text from an image program:\n Select one of the following options:")
while(1): 
	choice = input("a) Hide a text to an image (input one line terminal)\nb) Hide a text file in image\nc) Extract a text from image\nd) exit\n") 

	if(choice.lower() == 'a'):
		#Add a hidden text to an image 	
		#Obtain the image file name 
		print("Hide Text in Image.") 
		img = input("Type in the image file name:  ") 
	
		#Check if file exit else exit 
		try: 
			userImage = PilImage.open(img)
			userImage = userImage.convert('RGB')
		except IOError: 
			print("FILE NOT FOUND. Exiting...") 
			sys.exit()
	
		#Obtain the text that should be hidden 
		text = input("\nType in the Text to hide in the image:  ") 	 
		txtLength = len(text) 

		#get text length and convert length and text to binary 	
		bintxtLength = bin(txtLength)[2:].zfill(33)
		binTxt = ""
	
		#Convert the string to binary string (8 bits) 
		for count in text: 
			binTxt += bin(ord(count))[2:].zfill(8)
	  
		hiddenString = binTxt + bintxtLength
		writeToImage(userImage, hiddenString, img) 	
		
		print("Image outputted to: ", img.split(".")[0]+ ".png")
		userImage.close() 
		sys.exit()
	elif choice.lower() == 'b':
		#Add a hidden text file to an image 	
		#Obtain the image file name 
		print("Hide Text in Image.") 
		img = input("Type in the image file name:  ") 
	
		#Check if file exit else exit 
		try: 
			userImage = PilImage.open(img)
			userImage = userImage.convert('RGB')
		except IOError: 
			print("FILE NOT FOUND. Exiting...") 
			sys.exit()
	
		#Obtain the text that should be hidden 
		fileName = input("\nText File:  ") 
		try: 
			f = open(fileName,"r")
		except IOError: 
			print("FILE NOT FOUND. Exiting...") 
			sys.exit()

		#get text file text
		text = f.read()
		txtLength = len(text)

		#get text length and convert length and text to binary 	
		bintxtLength = bin(txtLength)[2:].zfill(33)
		binTxt = ""
	
		#Convert the string to binary string (8 bits) 
		for count in text: 
			binTxt += bin(ord(count))[2:].zfill(8)

		hiddenString = binTxt + bintxtLength
		writeToImage(userImage, hiddenString, img) 	
		
		print("Image outputted to: ", img.split(".")[0]+ ".png")
		userImage.close()
		f.close() 
		sys.exit()
	elif choice.lower() == 'c':
		print("Extract text from image.") 
		img = input("Type in the image file name:  ") 
		
		#Check if file exit else exit 
		try: 
			userImage = PilImage.open(img)
			userImage = userImage.convert('RGB')
		except IOError: 
			print("FILE NOT FOUND. Exiting...") 
			sys.exit()
		
		size = userImage.size 
		hiddenImg = userImage.load()
		
		lengthTxt, startW, startH = readLength(hiddenImg, size) 
		if(lengthTxt * 8 > size[0] * size[1]):
			print("No hidden text in image")
		 
		byteString = readText(hiddenImg, userImage.size, startW, startH, lengthTxt)

		print("Hidden Message:\n")
		print(bits2string(byteString) )

		userImage.close()
		sys.exit()
	elif choice.lower() == 'd':
		print("Exiting...")
		sys.exit()
	else: 
		print("Not a valid input!!\n") 
	



