"""Koneksi MySQL dan inisialisasi skema database Fyna Cchio."""

from typing import Optional

import mysql.connector
from mysql.connector import Error

_APP = None


def configure_database(app) -> None:
    global _APP
    _APP = app


def get_db_connection() -> Optional[mysql.connector.connection.MySQLConnection]:
    try:
        conn = mysql.connector.connect(
            host=_APP.config['DB_HOST'], user=_APP.config['DB_USER'],
            password=_APP.config['DB_PASS'], database=_APP.config['DB_NAME']
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db() -> None:
    try:
        conn = mysql.connector.connect(host=_APP.config['DB_HOST'], user=_APP.config['DB_USER'], password=_APP.config['DB_PASS'])
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {_APP.config['DB_NAME']}")
        conn.close()

        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                display_name VARCHAR(100) NOT NULL,
                avatar LONGTEXT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, name VARCHAR(100) NOT NULL, type ENUM('Pemasukan', 'Pengeluaran') NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE)")
        cursor.execute("CREATE TABLE IF NOT EXISTS portfolios (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, name VARCHAR(100) NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE)")
        cursor.execute("CREATE TABLE IF NOT EXISTS goals (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, name VARCHAR(100) NOT NULL, target_amount DECIMAL(15,2) NOT NULL, current_amount DECIMAL(15,2) DEFAULT 0, deadline DATE NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE)")

        # Menyimpan Akun Bank
        cursor.execute("CREATE TABLE IF NOT EXISTS user_accounts (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, name VARCHAR(50) NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE)")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS finance_transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                tgl DATE NOT NULL,
                type ENUM('Pemasukan', 'Pengeluaran') NOT NULL,
                account VARCHAR(50) NOT NULL,
                category_id INT NULL,
                portfolio_id INT NULL,
                goal_id INT NULL,
                asset_type VARCHAR(50) NULL,
                asset_name VARCHAR(100) NULL,
                quantity DECIMAL(15,4) NULL,
                nominal DECIMAL(15,2) NOT NULL,
                description VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
                FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE SET NULL,
                FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE SET NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                category_id INT NOT NULL,
                period VARCHAR(7) NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
                UNIQUE KEY unique_budget_cat (user_id, category_id, period)
            )
        """)

        try:
            cursor.execute("SHOW COLUMNS FROM users LIKE 'display_name'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE users ADD COLUMN display_name VARCHAR(100) DEFAULT 'Pengguna'")
            cursor.execute("SHOW COLUMNS FROM users LIKE 'avatar'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE users ADD COLUMN avatar LONGTEXT NULL")

            cursor.execute("SHOW COLUMNS FROM categories LIKE 'user_id'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE categories ADD COLUMN user_id INT")
                cursor.execute("ALTER TABLE portfolios ADD COLUMN user_id INT")
                cursor.execute("ALTER TABLE goals ADD COLUMN user_id INT")
                cursor.execute("ALTER TABLE finance_transactions ADD COLUMN user_id INT")
                cursor.execute("ALTER TABLE budgets ADD COLUMN user_id INT")
        except Error: pass

        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Database Initialization Error: {e}")
