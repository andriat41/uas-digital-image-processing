import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Fungsi untuk membaca dan melakukan segmentasi gambar
def segment_image(image_path, k=3):
    # Membaca gambar
    image = cv2.imread(image_path)
    # Mengubah gambar dari BGR ke RGB (OpenCV menggunakan BGR secara default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Mengubah gambar menjadi 2D array untuk pemrosesan clustering
    reshaped_image = image_rgb.reshape((-1, 3))

    # Menggunakan KMeans untuk melakukan clustering
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(reshaped_image)

    # Mendapatkan label dan centroids
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    # Mengubah kembali ke format gambar berdasarkan label
    segmented_image = centroids[labels].reshape(image_rgb.shape).astype(int)

    # Menampilkan gambar asli dan hasil segmentasi
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(image_rgb)
    plt.title("Original Image")
    plt.axis("off")
    
    plt.subplot(1, 2, 2)
    plt.imshow(segmented_image)
    plt.title(f"Segmented Image (K={k})")
    plt.axis("off")

    plt.show()

# Ganti dengan path gambar yang sesuai
image_path = 'img/multi-objects.jpg'

# Menjalankan fungsi segmentasi dengan 3 cluster (3 objek berbeda)
segment_image(image_path, k=3)
