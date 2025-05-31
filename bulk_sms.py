import time
from android_sms import AndroidSMS
import random
from datetime import datetime

def generate_code():
    # Generate kode 6 digit
    return str(random.randint(100000, 999999))

def read_template(template_file):
    try:
        with open(template_file, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error membaca template: {str(e)}")
        return None

def send_bulk_sms(txt_file, template_file):
    try:
        # Baca template pesan
        template = read_template(template_file)
        if not template:
            return

        # Baca file nomor
        with open(txt_file, 'r') as file:
            phone_numbers = file.readlines()
        
        # Inisialisasi AndroidSMS
        sms = AndroidSMS()
        
        # Hitung total nomor
        total_nomor = len(phone_numbers)
        print(f"\n=== MULAI PENGIRIMAN SMS ===")
        print(f"Total nomor yang akan dikirim: {total_nomor}")
        print(f"Waktu mulai: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 30 + "\n")
        
        # Loop melalui setiap nomor telepon
        for index, phone_number in enumerate(phone_numbers, 1):
            # Bersihkan nomor dari whitespace dan newline
            phone_number = phone_number.strip()
            
            # Hapus karakter '+' jika ada
            if phone_number.startswith('+'):
                phone_number = phone_number[1:]
            
            # Generate kode unik untuk setiap nomor
            kode = generate_code()
            
            # Format pesan dengan data dinamis
            message = template.format(
                nama="Customer",  # Bisa diganti dengan nama dari database jika ada
                kode=kode
            )
            
            print(f"\n[{index}/{total_nomor}] Mengirim SMS ke {phone_number}")
            print(f"Kode verifikasi: {kode}")
            
            # Kirim SMS
            sms.send(phone_number, message)
            
            print(f"✓ SMS berhasil terkirim!")
            print(f"  Waktu: {datetime.now().strftime('%H:%M:%S')}")
            
            # Tunggu 2 detik antara setiap pengiriman
            if index < total_nomor:  # Jangan tunggu setelah nomor terakhir
                print("Menunggu 2 detik...")
                time.sleep(2)
        
        print("\n=== PENGIRIMAN SELESAI ===")
        print(f"Total SMS terkirim: {total_nomor}")
        print(f"Waktu selesai: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 30)
            
    except Exception as e:
        print(f"\n❌ Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    # File nomor dan template
    txt_file = "nomor.txt"
    template_file = "template.txt"
    
    send_bulk_sms(txt_file, template_file) 
