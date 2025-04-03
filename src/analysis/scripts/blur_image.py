import cv2



def main():

    Fullimage = cv2.imread('/home/juli/Documentos/GFSG/experimentos/atascamiento/2024/Mezclas/0.0-1.0-320/24-05-2024/test1.jpg')
    blur = cv2.blur(Fullimage, (2,2))
    cv2.imwrite('/home/juli/Documentos/GFSG/experimentos/atascamiento/2024/Mezclas/0.0-1.0-320/24-05-2024/test2.png', blur)



if __name__ == '__main__':
    main()
