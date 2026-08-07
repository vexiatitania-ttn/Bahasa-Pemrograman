# Fyna Cchio


## Struktur

- `app.py`: inisialisasi Flask, autentikasi, seluruh route, dan proses aplikasi.
- `config.py`: konfigurasi Flask/MySQL dan akun bawaan.
- `database.py`: koneksi dan inisialisasi database.
- `analytics.py`: class OOP analisis kesehatan finansial.
- `utils.py`: format Rupiah, kuantitas, dan pembersihan input.
- `templates_content.py`: seluruh template HTML/Jinja asli.
- `requirements.txt`: dependensi Python.

## Menjalankan

1. Pastikan MySQL aktif.
2. Buka terminal pada folder ini.
3. Instal dependensi:

   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan aplikasi:

   ```bash
   python app.py
   ```

5. Buka `http://127.0.0.1:5000`.