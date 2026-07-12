import cv2 as cv
import os
import matplotlib.pyplot as plt 
import numpy as np


# Reading and writing images
# def readImage():
#     img_path = "./images/img.png"
#     img = cv.imread(img_path)
#     cv.imshow('img',img)
#     cv.waitKey(0)



# def writeImage():
#     img_path = "./images/img.png"
#     img = cv.imread(img_path)
#     out_path = "./images/outimg.png"
#     cv.imwrite(out_path,img)


# Read and Write Video
# def vidFromWebcam():
#     cap = cv.VideoCapture(0)   # Open default webcam

#     if not cap.isOpened():
#         print("Cannot open webcam")
#         return

#     while True:
#         ret, frame = cap.read()

#         if not ret:
#             print("Can't receive frame.")
#             break

#         cv.imshow("Webcam", frame)

#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv.destroyAllWindows()

# def read_and_write_single_pixel():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)
#     img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#     plt.figure()
#     plt.imshow(img_rgb)
#     plt.show()

#     pixel = img_rgb[160,180]
#     img_rgb[160,180] = (255,0,0)

#     plt.figure()
#     plt.imshow(img_rgb)
#     plt.show()

# def readAndWritePixelRegion():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)
#     imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    
#     plt.figure()
#     plt.imshow(imgRGB)
#     plt.show()
    
#     eyeRegion = imgRGB[290:340,326:380]
#     eyeRegion = imgRGB[290:340,326:380]

#     dx = 340-290
#     dy = 380-326

#     startX = 238
#     startY = 411

#     imgRGB[startX:startX+dx, startY:startY+dy] = eyeRegion
#     plt.figure()
#     plt.imshow(imgRGB)
#     plt.show()

# def grayscale():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)
#     imgGray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    
#     cv.imshow('gray',imgGray)
#     cv.waitKey(0)



# def hsvColorSegmentation():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)
#     imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
#     hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
#     lowerBound = np.array([0,0,50])
#     upperBound = np.array([10,120,100])
#     mask = cv.inRange(hsv,lowerBound,upperBound)
    
#     plt.figure()
#     plt.imshow(imgRGB)
#     plt.show()
    
#     cv.imshow('mask',mask)
#     cv.waitKey(0)

# def imageResize():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)
#     img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
#     img = img[286:345,322:389,:]
#     height,width,_ = img.shape
    
#     scale = 1/4
    
#     interpMethods = [
#         cv.INTER_AREA,
#         cv.INTER_LINEAR,
#         cv.INTER_NEAREST,
#         cv.INTER_CUBIC,
#         cv.INTER_LANCZOS4
#     ]

#     interpTitle = ['area','linear','nearest','cubic','lanczos']

#     plt.figure()
#     plt.subplot(2,3,1)
#     plt.imshow(img)

#     for i in range(len(interpMethods)):
#         plt.subplot(2,3,i+2)
#         imgResize = cv.resize(img,(int(width*scale),int(height*scale)),
#         interpolation=interpMethods[i])
#         plt.imshow(imgResize)
#         plt.title(interpTitle[i])
#     plt.show()


# def grayHistogram():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath,cv.IMREAD_GRAYSCALE)
    
#     plt.figure()
#     plt.imshow(img,cmap='gray')
    
#     hist = cv.calcHist([img],[0],None,[256],[0,256])
    
#     plt.figure()
#     plt.plot(hist)
#     plt.xlabel('bins')
#     plt.ylabel('# of pixels')
#     plt.show()

# def colorHistogram():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)
#     imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    
#     plt.figure()
#     plt.imshow(imgRGB)
    
#     colors = ['b','g','r']
#     plt.figure()
#     for i in range(len(colors)):
#         hist = cv.calcHist([imgRGB],[i],None,[256],[0,256])
#         plt.plot(hist,colors[i])
        
#     plt.xlabel('pixel intensity')
#     plt.ylabel('# of pixels')
    
#     plt.show()


# def convolution2d():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)
#     imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)

#     n = 100
#     kernel = np.ones((n,n), np.float32)/(n*n)
#     imgFilter = cv.filter2D(imgRGB,-1,kernel=kernel)

#     plt.figure()
#     plt.subplot(121)
#     plt.imshow(imgRGB)

#     plt.subplot(122)
#     plt.imshow(imgFilter)
#     plt.show()


# def callback(x):
#     # Callback function for trackbar (can be a pass statement)
#     pass

# def averageFiltering():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)
    
#     winName = 'avg filter'
#     cv.namedWindow(winName)
#     cv.createTrackbar('n', winName, 1, 100, callback)
    
#     height, width, _ = img.shape
#     scale = 1/4
#     width = int(width * scale)
#     height = int(height * scale)
#     img = cv.resize(img, (width, height))
    
#     while True:
#         if cv.waitKey(1) == ord('q'):
#             break
        
#         n = cv.getTrackbarPos('n', winName)
        
#         # Simple fix to prevent OpenCV crash when n is 0
#         if n < 1:
#             n = 1
            
#         imgFilter = cv.blur(img, (n, n))
#         cv.imshow(winName, imgFilter)
        
#     cv.destroyAllWindows()

# def medianFiltering():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)
    
#     imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

#     noisyImg = imgRGB.copy()
#     noiseProb = 0.05
#     noise = np.random.rand(noisyImg.shape[0], noisyImg.shape[1])
#     noisyImg[noise < noiseProb/2] = 0
#     noisyImg[noise > 1 - noiseProb/2] = 255

#     imgFilter = cv.medianBlur(noisyImg, 5)

#     plt.figure()
#     plt.subplot(121)
#     plt.imshow(noisyImg)
#     plt.subplot(122)
#     plt.imshow(imgFilter)

#     plt.show()
# def gaussianKernel(size,sigma):
#     kernel = cv.getGaussianKernel(size,sigma)
#     kernel = np.outer(kernel,kernel)
#     return kernel

# def gaussianFiltering():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)
#     img = cv.imread(imgPath)

#     n = 51
#     fig = plt.figure()
#     plt.subplot(121)
#     kernel = gaussianKernel(n,8)
#     plt.imshow(kernel)

#     ax = fig.add_subplot(122,projection='3d')
#     x = np.arange(0,n,1)
#     y = np.arange(0,n,1)
#     X,Y = np.meshgrid(x,y)
#     ax.plot_surface(X,Y,kernel,cmap='viridis')
#     plt.show()

# def thresholding():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)
#     img = cv.imread(imgPath)
    
#     if img is None:
#         print(f"Error: Could not load image from {imgPath}")
#         return

#     imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#     # 1. Calculate and plot the histogram
#     hist = cv.calcHist([imgGray], [0], None, [256], [0, 256])
#     plt.figure()
#     plt.plot(hist)
#     plt.xlabel('bins')
#     plt.ylabel('# of pixels')
#     plt.show()

#     # 2. Options for various thresholding methods
#     thresOpt = [
#         cv.THRESH_BINARY,
#         cv.THRESH_BINARY_INV,
#         cv.THRESH_TOZERO,
#         cv.THRESH_TOZERO_INV,
#         cv.THRESH_TRUNC
#     ]

#     thresNames = ['binary', 'binaryInv', 'toZero', 'toZeroInv', 'trunc']

#     # 3. Create grid plots for thresholded outputs
#     plt.figure()
#     plt.subplot(231)
#     plt.imshow(imgGray, cmap='gray')
#     plt.title('Original Gray')

#     for i in range(len(thresOpt)):
#         plt.subplot(2, 3, i + 2)
#         _, imgThres = cv.threshold(imgGray, 70, 255, thresOpt[i])
#         plt.imshow(imgThres, cmap='gray')
#         plt.title(thresNames[i])

#     plt.show()



# def callback(x):
#     """Dummy callback function for cv.createTrackbar"""
#     pass


# def cannyEdge():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)

#     if img is None:
#         print("Error: Could not load image.")
#         return

#     # Resize image
#     height, width = img.shape[:2]
#     scale = 1 / 5
#     img = cv.resize(
#         img,
#         (int(width * scale), int(height * scale)),
#         interpolation=cv.INTER_LINEAR,
#     )

#     # Convert to grayscale
#     gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#     winname = "Canny Edge Detection"
#     cv.namedWindow(winname)

#     cv.createTrackbar("Min Threshold", winname, 0, 255, callback)
#     cv.createTrackbar("Max Threshold", winname, 100, 255, callback)

#     while True:
#         minThres = cv.getTrackbarPos("Min Threshold", winname)
#         maxThres = cv.getTrackbarPos("Max Threshold", winname)

#         edges = cv.Canny(gray, minThres, maxThres)

#         cv.imshow(winname, edges)

#         key = cv.waitKey(1) & 0xFF
#         if key == ord("q"):
#             break

#     cv.destroyAllWindows()

# def houghLineTransform():
#     imgPath = "./images/img.png"
#     img = cv.imread(imgPath)

#     if img is None:
#         print(f"Error: Could not load image from {imgPath}")
#         return

#     imgBlur = cv.GaussianBlur(img, (21, 21), 3)
#     cannyEdge = cv.Canny(imgBlur, 50, 180)

#     plt.figure(figsize=(12, 4))
#     plt.subplot(141)
#     plt.imshow(img, cmap='gray')
#     plt.title('Original')
    
#     plt.subplot(142)
#     plt.imshow(imgBlur, cmap='gray')
#     plt.title('Blur')
    
#     plt.subplot(143)
#     plt.imshow(cannyEdge, cmap='gray')
#     plt.title('Canny')

#     distResol = 1
#     angleResol = np.pi / 180
#     threshold = 150
#     lines = cv.HoughLines(cannyEdge, distResol, angleResol, threshold)

#     k = 3000

#     # Safety check: only draw lines if any were detected
#     if lines is not None:
#         for curLine in lines:
#             rho, theta = curLine[0]
#             dhat = np.array([[np.cos(theta)], [np.sin(theta)]])
#             d = rho * dhat
#             lhat = np.array([[-np.sin(theta)], [np.cos(theta)]])
            
#             p1 = d + k * lhat
#             p2 = d - k * lhat
            
#             p1 = p1.astype(int)
#             p2 = p2.astype(int)
            
#             # Since img is grayscale, the color value (255, 255, 255) defaults to white (255)
#             cv.line(img, (p1[0][0], p1[1][0]), (p2[0][0], p2[1][0]), (255, 255, 255), 10)

#     plt.subplot(144)
#     plt.imshow(img, cmap='gray')
#     plt.title('Hough Lines')

#     plt.show()

def harrisCorner():
    imgPath = "./images/img.png"
    img = cv.imread(imgPath)

    
    if img is None:
        print(f"Error: Could not load image from {imgPath}")
        return

    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgGray = np.float32(imgGray)

    plt.figure(figsize=(12, 4))
    
    # 1. Plot the grayscale image
    plt.subplot(131)
    plt.imshow(imgGray, cmap='gray')
    plt.title('Grayscale')

    # 2. Harris Corner Parameter Setup and Response Calculation
    plt.subplot(132)
    blockSize = 5
    sobelSize = 3
    k = 0.04
    harris = cv.cornerHarris(imgGray, blockSize, sobelSize, k)
    plt.imshow(harris, cmap='jet')  # Added a colormap for better visibility of response intensity
    plt.title('Harris Response')

    # 3. Threshold and overlay corners onto the color image
    plt.subplot(133)
    imgRGB[harris > 0.05 * harris.max()] = [255, 0, 0]
    plt.imshow(imgRGB)  # Fixed: Added the missing display call from the image
    plt.title('Detected Corners')
    plt.imshow(img)
    plt.show()

if __name__ == "__main__":
    # vidFromWebcam()
    # read_and_write_single_pixel()
    # readAndWritePixelRegion()
    # pureColors()
    # grayscale()
    # hsvColorSegmentation()
    # imageResize()
    # grayHistogram()
    # colorHistogram()
    # convolution2d()
    # averageFiltering()
    # medianFiltering()
    # gaussianFiltering()
    # thresholding()
    #cannyEdge()
    # houghLineTransform()
    harrisCorner()