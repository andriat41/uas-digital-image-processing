import cv2
import numpy as np
import matplotlib.pyplot as plt
import time



# Mendeteksi tepi menggunakan canny
def canny(image):
    start_time = time.time()
    edges_canny = cv2.Canny(image,100,200)
    end_time = time.time()
    time_canny = end_time - start_time
    
    return edges_canny, time_canny

# Mendeteksi tepi menggunakan sobe
def sobel(image):
    start_time = time.time()
    edges_sobelx = cv2.Sobel(image,cv2.CV_8U,1,0,ksize=5)
    edges_sobely = cv2.Sobel(image,cv2.CV_8U,0,1,ksize=5)
    edges_sobel = edges_sobelx + edges_sobely
    end_time = time.time()
    time_sobel = end_time - start_time
    
    return edges_sobel, time_sobel

# Mendeteksi tepi menggunakan prewitt
def prewitt(image):
    start_time = time.time()
    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    edges_prewitt = cv2.filter2D(image, -1, kernelx)
    edges_prewitt = cv2.filter2D(image, -1, kernely)
    end_time = time.time()
    time_prewitt = end_time - start_time
    
    return edges_prewitt, time_prewitt

# Menampilkan hasil
# Membaca gambar grayscale
img = cv2.imread('img/kincir.jpg', 0)
imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(imgRgb, cv2.COLOR_RGB2GRAY)
img_gaussian = cv2.GaussianBlur(gray,(3,3),0)

edges_canny, time_canny = canny(img_gaussian)
edges_sobel, time_sobel = sobel(img_gaussian)
edges_prewitt, time_prewitt = prewitt(img_gaussian)

plt.figure(figsize=(15,5))
plt.subplot(1,4,1),plt.imshow(img_gaussian, cmap='gray')
plt.title('Gambar Asli')
plt.subplot(1,4,2),plt.imshow(edges_canny, cmap='gray')
plt.title('Canny ({} detik)'.format(round(time_canny, 5)))
plt.subplot(1,4,3),plt.imshow(edges_sobel, cmap='gray')
plt.title('Sobel ({} detik)'.format(round(time_sobel, 5)))
plt.subplot(1,4,4),plt.imshow(edges_prewitt, cmap='gray')
plt.title('Prewitt ({} detik)'.format(round(time_prewitt, 5)))

img = cv2.imread('img/bunga.jpg', 0)
imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(imgRgb, cv2.COLOR_RGB2GRAY)
img_gaussian = cv2.GaussianBlur(gray,(3,3),0)

edges_canny, time_canny = canny(img_gaussian)
edges_sobel, time_sobel = sobel(img_gaussian)
edges_prewitt, time_prewitt = prewitt(img_gaussian)

plt.figure(figsize=(15,5))
plt.subplot(2,4,1),plt.imshow(img_gaussian, cmap='gray')
plt.title('Gambar Asli')
plt.subplot(2,4,2),plt.imshow(edges_canny, cmap='gray')
plt.title('Canny ({} detik)'.format(round(time_canny, 5)))
plt.subplot(2,4,3),plt.imshow(edges_sobel, cmap='gray')
plt.title('Sobel ({} detik)'.format(round(time_sobel, 5)))
plt.subplot(2,4,4),plt.imshow(edges_prewitt, cmap='gray')
plt.title('Prewitt ({} detik)'.format(round(time_prewitt, 5)))


plt.show()