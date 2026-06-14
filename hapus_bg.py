from rembg import remove
from PIL import Image

# Nama file asli Anda
input_path = 'gambar.jpeg' 
# Nama file hasil yang sudah transparan
output_path = 'icon.png'   

print("Sedang diproses oleh AI, tunggu sebentar...")

# Buka gambar
input_image = Image.open(input_path)

# Proses hapus background!
output_image = remove(input_image)

# Simpan sebagai PNG
output_image.save(output_path)

print("✅ Selesai! Background berhasil dihapus, file tersimpan sebagai icon.png")