import os
from  PutMask import  PutMaskInFace
import random

def main():
    """
    By: @EstebanJS_
    """
    URL_IMAGES_FACE = "./Face/"
    URL_IMAGES_MASK = "./Mask/"
    OUT_PUT_DIR = "./FaceWithMask/"

    ListImgFace = os.listdir(URL_IMAGES_FACE)
    ListImgMask = os.listdir(URL_IMAGES_MASK)

    cant = 0
    err = 0

    for ImgFace in ListImgFace:
        cant += 1
        print("imagen ",cant," de ",len(ListImgFace)," ⏳")
        mask_position = random.randint(0,(len(ListImgMask)-1))
        IMG = os.path.join(URL_IMAGES_FACE,ImgFace)
        MASK = os.path.join(URL_IMAGES_MASK,ListImgMask[mask_position])
        OUT = os.path.join(OUT_PUT_DIR,ImgFace)
        try:
            PutMaskInFace(IMG,MASK,OUT)
        except:
            err += 1
    print(err," Errores de imagen.")

main()