# Photomosaics
An application used for making a photomosaic using 'pillow' library. 
User can choose size of pixels. Original image is stored in 'InputImage' directory. Source images are stored in 'SourceImages'.
File 'rgbsource.txt' is used to store average RGB values of source images to speed up the program. Its contents should be deleted each time when 'SourceImages' directory contents are modified.
Function 'crop_sourceIMG' should be disabled after first compilation unless 'SourceImages' directory contents are modified.

## Known issues:
- random rotation of source images
- might occur memory error for big number of source images (tested up to 2000 photos)



## Example
![example](https://user-images.githubusercontent.com/25506665/75587660-409f2100-5a77-11ea-9b3c-9b736b01c30e.JPG)
