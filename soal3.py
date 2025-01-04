import cv2
import numpy as np
import matplotlib.pyplot as plt

def text_to_bin(text):
    """Mengubah teks menjadi format biner."""
    return ''.join(format(ord(i), '08b') for i in text)

def decimal_to_binary(decimal_num, bit_size=8):
    """Mengubah bilangan desimal menjadi biner dengan panjang bit tertentu."""
    binary_str = bin(decimal_num)[2:].zfill(bit_size)
    return binary_str

def encode_image(image_path, secret_message, output_image_path):
    """Menyisipkan pesan ke dalam gambar menggunakan metode LSB.

    Args:
        image_path: Path gambar input (grayscale).
        secret_message: Pesan rahasia yang ingin disisipkan (dalam bentuk string).
        output_image_path: Path untuk menyimpan gambar yang sudah disisipkan pesan.
    """
    # Membaca gambar grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Mendapatkan ukuran gambar
    rows, cols = image.shape
    message_len = len(secret_message)

    # Mengecek apakah pesan bisa disisipkan ke dalam gambar
    if message_len > rows * cols:
        raise ValueError("Pesan terlalu panjang untuk gambar ini!")

    message_index = 0

    # Menyisipkan bit pesan ke dalam LSB setiap piksel
    for i in range(rows):
        for j in range(cols):
            pixel = image[i, j]

            if message_index < message_len:
                # Sisipkan bit pesan ke dalam LSB
                image[i, j] = (pixel & 0xFE) | int(secret_message[message_index])
                message_index += 1

    # Menyimpan gambar yang sudah disisipi pesan
    cv2.imwrite(output_image_path, image)
    print("Pesan berhasil disisipkan ke dalam gambar.")
    
def decode_image_lsb(image_path, message_length):
    """Mengekstrak pesan dari gambar yang disisipkan menggunakan LSB.

    Args:
        image_path: Path gambar yang sudah disisipkan pesan.
        message_length: Jumlah panjang pesan yang disisipkan dalam bit.

    Returns:
        str: Pesan yang diekstrak dari gambar.
    """
    # Membaca gambar grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Menyiapkan wadah untuk pesan biner
    binary_message = ""

    # Mendapatkan ukuran gambar
    rows, cols = image.shape

    # Mengekstrak LSB dari setiap piksel untuk mendapatkan pesan
    for i in range(rows):
        for j in range(cols):
            pixel = image[i, j]
            binary_message += str(pixel & 1)

    # Menyaring bit pesan yang telah disisipkan
    # Ambil sebanyak jumlah bit yang disisipkan (message_length)
    return binary_message[:message_length]  # Ambil sesuai panjang pesan yang disisipkan
    
def create_secret_message(birth_date):
  """Membuat pesan rahasia dari tanggal lahir.

  Args:
    birth_date: String yang berisi tanggal lahir dalam format DD-MM-YYYY.

  Returns:
    String: Pesan rahasia dalam bentuk biner.
  """

  # Memisahkan tanggal, bulan, dan tahun
  day, month, year = map(int, birth_date.split('-'))

  # Mengubah setiap bagian menjadi biner 8-bit
  binary_day = decimal_to_binary(day)
  binary_month = decimal_to_binary(month)
  binary_year1 = decimal_to_binary(int(year // 100))
  binary_year2 = decimal_to_binary(year % 100)

  # Menggabungkan semua bagian menjadi satu pesan rahasia
  secret_message = (binary_day + binary_month + binary_year1 + binary_year2) * 3
  return secret_message

def decode_secret_message(secret_message):
  """Mengembalikan tanggal lahir dari pesan rahasia.

  Args:
    secret_message: String yang berisi pesan rahasia dalam bentuk biner.

  Returns:
    String: Tanggal lahir dalam format "DD-MM-YYYY".
  """

  # Panjang setiap bagian (dalam bit)
  part_length = 8

  # Membagi pesan menjadi 4 bagian (hari, bulan, tahun1, tahun2)
  parts = [secret_message[i:i+part_length] for i in range(0, len(secret_message), part_length)]

  # Mengambil satu set pertama dari setiap bagian (karena diulang 3 kali)
  unique_parts = parts[:4]

  # Mengubah biner ke desimal
  decimal_parts = [int(part, 2) for part in unique_parts]

  # Membentuk tanggal
  day, month, year1, year2 = decimal_parts
  year = year1 * 100 + year2
  birth_date = f"{day:02d}-{month:02d}-{year}"

  return birth_date

def image_convertion_to_30x40_gray_png(image_path, output_image_path):
    """Mengubah gambar menjadi grayscale dan menyesuaikan ukuran menjadi 30x40 pixel."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img_resized = cv2.resize(img, (30, 40))
    cv2.imwrite(output_image_path, img_resized)
    print(f"Gambar berhasil diubah menjadi grayscale dan diresize menjadi 30x40 pixel. Disimpan di {output_image_path}")
    

image_convertion_to_30x40_gray_png('img/andriat.jpg', 'img/andriat_resized.png')
  
# Menyisipkan pesan rahasia ke dalam gambar
birth_date = '01-04-1986'
secret_message = create_secret_message(birth_date)
message_length = len(secret_message) 
print(f"Pesan rahasia yang akan disisipkan: {secret_message} (total bit: {message_length})")
encode_image('img/andriat_resized.png', secret_message, 'img/andriat_encoded.png')

binnary_message = decode_image_lsb('img/andriat_encoded.png', message_length)
decoded_message = decode_secret_message(binnary_message)
print(f"Pesan rahasia yang diekstrak: {decoded_message}")

# Menampilkan gambar asli dan gambar yang sudah disisipkan pesan
original_image = cv2.imread('img/andriat_resized.png', cv2.IMREAD_GRAYSCALE)
encoded_image = cv2.imread('img/andriat_encoded.png', cv2.IMREAD_GRAYSCALE)

plt.subplot(1, 2, 1)
plt.imshow(original_image, cmap='gray')
plt.title('Gambar Asli')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(encoded_image, cmap='gray')
plt.title(f"Pesan Rahasia yang Disisipkan {decoded_message}")
plt.axis('off')

plt.show()