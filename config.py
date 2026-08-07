"""Konfigurasi aplikasi dan daftar akun bawaan Fyna Cchio."""

class Config:
    SECRET_KEY = ''
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASS = ''
    DB_NAME = 'fynacchio'

# Akun Bank Default
ACCOUNTS = ['Cash', 'BCA', 'Bank Jago', 'Blu', 'GoPay', 'OVO', 'DANA', 'Mandiri', 'ShopeePay', 'Superbank']
