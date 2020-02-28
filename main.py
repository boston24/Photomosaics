from PIL import Image
from PIL import ImageColor
import glob, os
from PIL import ImageFile
import ntpath
import math
import json
ImageFile.LOAD_TRUNCATED_IMAGES = True

im = Image.open(r'InputImage\input.jpg')
width = im.size[0]
height = im.size[1]
print(str(width) + " x " + str(height))
size_of_squares = 3000

outputIMG = Image.new('RGB',(width,height),'white')

def count_src_rgb():

    list = []
    counter = 0
    imgSum = 0

    source = glob.glob("SourceImagesCropped\*.jpg")
    for image in source:
        imgSum+=1

    source = glob.glob("SourceImagesCropped\*.jpg")
    for image in source:
        counter+=1
        img = Image.open(image)
        px = img.load()
        print("Obliczam RGB SourceImageCropped " + str(counter) + "/" + str(imgSum))
        SRCrgb = countRGB(px, img.size[0])
        list.append(SRCrgb)


    with open('rgbsource.txt', 'w') as outfile:
        json.dump(list,outfile)

    return list

def list_src_img(size):

    list = []

    source = glob.glob("SourceImagesCropped\*.jpg")
    for image in source:
        img = Image.open(image)
        list.append(img.resize((size,size)))

    return list

def insert(rgb, imgOUT, cords, size_of_squares,SRCrgbLIST,SRCimgLIST):

    min_distance = 1000
    min_distance_img = imgOUT

    for SRCrgb in SRCrgbLIST:
        distance = math.sqrt(((SRCrgb[0] - rgb[0]) ** 2) + ((SRCrgb[1] - rgb[1]) ** 2) + ((SRCrgb[2] - rgb[2]) ** 2))
        if (min_distance > distance):
            min_distance = distance
            min_distance_img = SRCimgLIST[SRCrgbLIST.index(SRCrgb)]


    imgOUT.paste(min_distance_img,cords)
    imgOUT.save(r'OutputImage\final.jpg')

def countRGB(im,size_of_squares):

    rgbSum = [0, 0, 0]

    x = 0
    y = 0

    for x in range(size_of_squares):
        temp = im[x,y]
        #print("Pixel ("+ str(x) + ", " + str(y) + ") = " + str(temp))
        rgbSum[0] = (rgbSum[0] + temp[0])
        rgbSum[1] = (rgbSum[1] + temp[1])
        rgbSum[2] = (rgbSum[2] + temp[2])
        for y in range(size_of_squares):
            temp = im[x, y]
            #print("Pixel (" + str(x) + ", " + str(y) + ") = " + str(temp))
            rgbSum[0] = (rgbSum[0] + temp[0])
            rgbSum[1] = (rgbSum[1] + temp[1])
            rgbSum[2] = (rgbSum[2] + temp[2])


    rgbSum[0] = round(rgbSum[0]/pow(size_of_squares,2))
    rgbSum[1] = round(rgbSum[1]/pow(size_of_squares,2))
    rgbSum[2] = round(rgbSum[2]/pow(size_of_squares,2))
    #print("RGB value of cropped image: " + str(rgbSum))

    return rgbSum

def getName(path):
    head, tail = ntpath.split(path)
    return tail or npath.basename(head)

def crop_sourceIMG():

    source = glob.glob("SourceImages\*.jpg")
    for image in source:
        img = Image.open(image)
        name = getName(img.filename)
        if(img.size[0]<img.size[1]):
            space = (0,round((img.size[1]-img.size[0])/2),img.size[0],round((img.size[1]-img.size[0])/2)+img.size[0])
            img_crop = img.crop(space)
        else:
            space = (round((img.size[0]-img.size[1])/2),0,round((img.size[0]-img.size[1])/2)+img.size[1],img.size[1])
            img_crop = img.crop(space)
        img_crop.save('SourceImagesCropped\cropped_' + name)


#print("Przycinam SourceImages")
#crop_sourceIMG()

try:
    with open('rgbsource.txt', 'r') as json_file:
        SRCrgbLIST = json.load(json_file)
except:
    SRCrgbLIST = count_src_rgb()

print("Dodaje SourceImagesCropped do listy")
SRCimgLIST = list_src_img(size_of_squares)

counter = 0
pixelAmount = round((width*height)/(size_of_squares**2))

for upper in range(0, height, size_of_squares):
    for left in range(0, width, size_of_squares):

        counter+=1

        x = left
        y = upper
        u = x + size_of_squares
        w = y + size_of_squares

        area = (x, y, u, w)

        im_crop = im.crop(area)
        px = im_crop.load()

        print("Obliczam RGB InputImage " + str(counter) + "/" + str(pixelAmount))
        rgb = countRGB(px, size_of_squares)
        print("Wchodze w funkcje INPUT")
        insert(tuple(rgb), outputIMG, area,size_of_squares,SRCrgbLIST,SRCimgLIST)

final = Image.open(r'OutputImage\final.jpg')
final.show()

#imFinal = Image.open("OutputImage\final.jpg")
#imFinal.crop((0,0,width,height))
#imFinal.save("OutputImage\final.jpg")
