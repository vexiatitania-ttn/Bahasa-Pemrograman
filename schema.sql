CREATE DATABASE IF NOT EXISTS fynacchio;
USE fynacchio;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    avatar LONGTEXT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    type ENUM('Pemasukan', 'Pengeluaran') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS portfolios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    target_amount DECIMAL(15,2) NOT NULL,
    current_amount DECIMAL(15,2) DEFAULT 0,
    deadline DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

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
);

CREATE TABLE IF NOT EXISTS budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    period VARCHAR(7) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    UNIQUE KEY unique_budget_cat (user_id, category_id, period)
);
