import os
import io
import json
import calendar
import re
from datetime import datetime, date, timedelta
from collections import defaultdict
from typing import List, Dict, Optional
from functools import wraps

from flask import Flask, request, render_template_string, redirect, url_for, flash, send_file, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from config import ACCOUNTS, Config
from database import configure_database, get_db_connection, init_db
from analytics import BaseFinance, FinancialAnalyzer
from utils import clean_string_input, format_qty, format_rupiah
from templates_content import (
    TPL_BUDGETS,
    TPL_DASHBOARD,
    TPL_LOGIN_FULL,
    TPL_PORTFOLIOS,
    TPL_REGISTER_FULL,
    TPL_REPORTS,
    TPL_TRANSACTIONS,
)

app = Flask(__name__)
app.config.from_object(Config)
configure_database(app)

GLOBAL_APP_BOOT_TIME = datetime.now().strftime("%d %b %Y %H:%M")
GLOBAL_ACTIVE_SESSIONS = 0

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')

        if not user_id:
            return redirect(url_for('login'))

        conn = get_db_connection()
        if not conn:
            session.clear()
            flash("Koneksi database gagal. Silakan login kembali.", "danger")
            return redirect(url_for('login'))

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            user_exists = cursor.fetchone()
        except Error as e:
            print(f"Session validation error: {e}")
            user_exists = None
        finally:
            if cursor:
                cursor.close()
            conn.close()

        if not user_exists:
            session.clear()
            flash("Sesi lama tidak lagi valid. Silakan daftar atau login kembali.", "warning")
            return redirect(url_for('login'))

        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user_profile():
    data = {
        'current_username': '',
        'current_display_name': 'Pengguna',
        'current_avatar': '',
        'global_boot_time': GLOBAL_APP_BOOT_TIME,
        'global_active_sessions': GLOBAL_ACTIVE_SESSIONS
    }

    user_id = session.get('user_id')
    if not user_id:
        return data

    conn = get_db_connection()
    if not conn:
        return data

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, display_name, avatar FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            data['current_username'] = user['username']
            data['current_display_name'] = user.get('display_name') or user['username']
            data['current_avatar'] = user.get('avatar') or ''
    except Error as e:
        print(f"Profile context error: {e}")
    finally:
        if cursor:
            cursor.close()
        conn.close()

    return data

app.jinja_env.filters['rupiah'] = format_rupiah
app.jinja_env.filters['qty'] = format_qty


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session: return redirect(url_for('dashboard'))

    if request.method == 'POST':
        display_name = request.form['display_name'].strip()
        username = request.form['username'].strip()
        password = request.form['password']

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                flash("Koneksi database gagal. Silakan coba lagi beberapa saat lagi.", "danger")
                return redirect(url_for('register'))

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
            if cursor.fetchone():
                flash("Username sudah terdaftar! Gunakan username lain.", "danger")
                return redirect(url_for('register'))

            hashed_pw = generate_password_hash(password)
            cursor.execute("INSERT INTO users (username, display_name, password_hash) VALUES (%s, %s, %s)", (username, display_name, hashed_pw))
            user_id = cursor.lastrowid

            cat_defaults = [
                (user_id, 'Makanan', 'Pengeluaran'),
                (user_id, 'Transport', 'Pengeluaran'),
                (user_id, 'Tagihan', 'Pengeluaran'),
                (user_id, 'Kesehatan', 'Pengeluaran'),
                (user_id, 'Kuliah', 'Pengeluaran'),
                (user_id, 'Belanja', 'Pengeluaran'),
                (user_id, 'Lain-lain', 'Pengeluaran'),
                (user_id, 'Gaji', 'Pemasukan'),
                (user_id, 'Uang Makan', 'Pemasukan'),
                (user_id, 'Freelance', 'Pemasukan'),
                (user_id, 'Lain-lain', 'Pemasukan')
            ]
            cursor.executemany("INSERT INTO categories (user_id, name, type) VALUES (%s, %s, %s)", cat_defaults)

            port_defaults = [(user_id, 'Ajaib'), (user_id, 'Bibit'), (user_id, 'Tring'), (user_id, 'Pluang'), (user_id, 'Stockbit')]
            cursor.executemany("INSERT INTO portfolios (user_id, name) VALUES (%s, %s)", port_defaults)

            acc_defaults = [(user_id, acc) for acc in ACCOUNTS]
            cursor.executemany("INSERT INTO user_accounts (user_id, name) VALUES (%s, %s)", acc_defaults)

            conn.commit()
            flash("Pendaftaran berhasil! Silakan Login dengan Username Anda.", "success")
            return redirect(url_for('login'))
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Registration database error: {e}")
            flash("Pendaftaran gagal karena terjadi gangguan database. Silakan coba kembali.", "danger")
            return redirect(url_for('register'))
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    return render_template_string(TPL_REGISTER_FULL)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session: return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                flash("Koneksi database gagal. Silakan coba lagi beberapa saat lagi.", "danger")
                return redirect(url_for('login'))

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
        except Error as e:
            print(f"Login database error: {e}")
            flash("Login gagal karena terjadi gangguan database. Silakan coba kembali.", "danger")
            return redirect(url_for('login'))
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

        if user:
            if check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']

                global GLOBAL_ACTIVE_SESSIONS
                GLOBAL_ACTIVE_SESSIONS += 1

                return redirect(url_for('dashboard'))
            else:
                flash("Password salah! Periksa kembali password Anda.", "danger")
        else:
            flash("Username tidak ditemukan! Silakan daftar terlebih dahulu.", "danger")

    return render_template_string(TPL_LOGIN_FULL)

@app.route('/logout')
def logout():
    session.clear()
    global GLOBAL_ACTIVE_SESSIONS
    GLOBAL_ACTIVE_SESSIONS = max(0, GLOBAL_ACTIVE_SESSIONS - 1)

    flash("Anda telah keluar dari sistem.", "success")
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    user_id = session['user_id']
    display_name = request.form['display_name'].strip()
    username = request.form['username'].strip()
    password = request.form.get('password')
    avatar_base64 = request.form.get('avatar_base64', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM users WHERE username=%s AND id != %s", (username, user_id))
    if cursor.fetchone():
        flash("Username sudah dipakai oleh pengguna lain!", "danger")
        conn.close()
        return redirect(request.referrer or url_for('dashboard'))

    if password:
        hashed_pw = generate_password_hash(password)
        cursor.execute("UPDATE users SET display_name=%s, username=%s, password_hash=%s, avatar=%s WHERE id=%s", (display_name, username, hashed_pw, avatar_base64, user_id))
    else:
        cursor.execute("UPDATE users SET display_name=%s, username=%s, avatar=%s WHERE id=%s", (display_name, username, avatar_base64, user_id))

    conn.commit(); conn.close()

    session['username'] = username
    flash("Profil berhasil diperbarui!", "success")
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/')
@login_required
def dashboard():
    user_id = session['user_id']

    analyzer = FinancialAnalyzer(user_id)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Memasukkan kategori baru untuk akun lama yang sudah telanjur dibuat
    cursor.execute("SELECT name, type FROM categories WHERE user_id = %s", (user_id,))
    existing_cats = cursor.fetchall()
    existing_income = [row['name'] for row in existing_cats if row['type'] == 'Pemasukan']
    existing_expense = [row['name'] for row in existing_cats if row['type'] == 'Pengeluaran']

    new_income_cats = ['Gaji', 'Uang Makan', 'Freelance', 'Lain-lain']
    new_expense_cats = ['Kuliah', 'Belanja', 'Lain-lain']

    cats_to_add = [(user_id, cat, 'Pemasukan') for cat in new_income_cats if cat not in existing_income]
    cats_to_add.extend([(user_id, cat, 'Pengeluaran') for cat in new_expense_cats if cat not in existing_expense])

    if cats_to_add:
        cursor.executemany("INSERT INTO categories (user_id, name, type) VALUES (%s, %s, %s)", cats_to_add)
        conn.commit()

    # Sinkronisasi Akun Bank bagi User Lama
    cursor.execute("SELECT name FROM user_accounts WHERE user_id = %s", (user_id,))
    existing_accs = [row['name'] for row in cursor.fetchall()]
    if not existing_accs:
        acc_defaults = [(user_id, acc) for acc in ACCOUNTS]
        cursor.executemany("INSERT INTO user_accounts (user_id, name) VALUES (%s, %s)", acc_defaults)
        conn.commit()
        existing_accs = ACCOUNTS

    cursor.execute("""
        SELECT t.*, c.name as cat_name, c.type as cat_type, p.name as port_name, g.name as goal_name
        FROM finance_transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        LEFT JOIN portfolios p ON t.portfolio_id = p.id
        LEFT JOIN goals g ON t.goal_id = g.id
        WHERE t.user_id = %s
        ORDER BY t.tgl DESC, t.id DESC
    """, (user_id,))
    all_tx = cursor.fetchall()

    cursor.execute("SELECT * FROM goals WHERE user_id = %s ORDER BY deadline ASC", (user_id,))
    goals_raw = cursor.fetchall()
    total_goals_funded = sum(float(g['current_amount']) for g in goals_raw)

    stats = {'income': 0.0, 'expense': 0.0, 'income_month': 0.0, 'expense_month': 0.0}
    expense_cat = defaultdict(float)
    invest_allocation = defaultdict(float)
    curr_month = datetime.now().strftime('%Y-%m')

    sel_year = int(request.args.get('year', datetime.now().year))
    sel_month = int(request.args.get('month', datetime.now().month))
    calendar_grid = calendar.monthcalendar(sel_year, sel_month)
    daily_summary = defaultdict(lambda: {'in': 0.0, 'out': 0.0, 'in_pct': 0, 'out_pct': 0})
    daily_tx_map = defaultdict(list)
    account_balances = {acc: 0.0 for acc in existing_accs}

    trend_view = request.args.get('trend_view', 'day')
    trend_month = int(request.args.get('trend_month', sel_month))
    if trend_view == 'year': trend_year = int(request.args.get('trend_year_y', sel_year))
    else: trend_year = int(request.args.get('trend_year_m', sel_year))

    default_end = datetime.now().date()
    default_start = default_end - timedelta(days=29)
    start_str = request.args.get('start_date', default_start.strftime('%Y-%m-%d'))
    end_str = request.args.get('end_date', default_end.strftime('%Y-%m-%d'))

    try:
        dt_start = datetime.strptime(start_str, '%Y-%m-%d').date()
        dt_end = datetime.strptime(end_str, '%Y-%m-%d').date()
    except ValueError:
        dt_end = datetime.now().date()
        dt_start = dt_end - timedelta(days=29)
        start_str, end_str = dt_start.strftime('%Y-%m-%d'), dt_end.strftime('%Y-%m-%d')

    if dt_start > dt_end:
        dt_start, dt_end = dt_end, dt_start
        start_str, end_str = dt_start.strftime('%Y-%m-%d'), dt_end.strftime('%Y-%m-%d')

    month_short = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agt', 'Sep', 'Okt', 'Nov', 'Des']
    trend_keys, trend_labels = [], []

    if trend_view == 'year':
        for m in range(1, 13):
            trend_keys.append(f"{trend_year}-{m:02d}")
            trend_labels.append(month_short[m])
    elif trend_view == 'month':
        num_days = calendar.monthrange(trend_year, trend_month)[1]
        for d in range(1, num_days + 1):
            trend_keys.append(f"{trend_year}-{trend_month:02d}-{d:02d}")
            trend_labels.append(f"{d} {month_short[trend_month]}")
    else:
        days_diff = (dt_end - dt_start).days
        for i in range(days_diff + 1):
            cur_dt = dt_start + timedelta(days=i)
            trend_keys.append(cur_dt.strftime('%Y-%m-%d'))
            trend_labels.append(f"{cur_dt.day} {month_short[cur_dt.month]}")

    trend_income_map, trend_expense_map, trend_invest_map = defaultdict(float), defaultdict(float), defaultdict(float)
    total_invested_modal = 0.0

    for tx in all_tx:
        val = float(tx['nominal'])
        tx_date = tx['tgl'] if isinstance(tx['tgl'], date) else datetime.strptime(str(tx['tgl'])[:10], '%Y-%m-%d').date()
        tx_month = tx_date.strftime('%Y-%m')

        acc = tx.get('account')
        if acc:
            if acc not in account_balances: account_balances[acc] = 0.0
            if tx['type'] == 'Pemasukan': account_balances[acc] += val
            else: account_balances[acc] -= val

        tx_key = tx_month if trend_view == 'year' else tx_date.strftime('%Y-%m-%d')

        if tx_date.year == sel_year and tx_date.month == sel_month:
            if tx['type'] == 'Pemasukan': daily_summary[tx_date.day]['in'] += val
            else: daily_summary[tx_date.day]['out'] += val

            daily_tx_map[str(tx_date.day)].append({
                'desc': tx['description'], 'nom': format_rupiah(val), 'type': tx['type'],
                'cat': tx['cat_name'] or tx['asset_type'] or tx['port_name'] or 'Mutasi Internal'
            })

        if tx['portfolio_id'] or tx['goal_id']:
            atype = tx.get('asset_type') or 'Lainnya'
            if tx['type'] == 'Pengeluaran':
                if tx['portfolio_id']:
                    invest_allocation[atype] += val
                    total_invested_modal += val
                if tx_key in trend_keys: trend_invest_map[tx_key] += val
            else:
                if tx['portfolio_id']:
                    invest_allocation[atype] = max(0.0, invest_allocation[atype] - val)
                    total_invested_modal = max(0.0, total_invested_modal - val)
        elif tx['category_id'] is not None:
            if tx['cat_type'] == 'Pemasukan' or tx['type'] == 'Pemasukan':
                stats['income'] += val
                if tx_month == curr_month: stats['income_month'] += val
                if tx_key in trend_keys: trend_income_map[tx_key] += val
            elif tx['cat_type'] == 'Pengeluaran' or tx['type'] == 'Pengeluaran':
                stats['expense'] += val
                if tx_month == curr_month:
                    stats['expense_month'] += val
                    expense_cat[tx['cat_name'] or 'Lainnya'] += val
                if tx_key in trend_keys: trend_expense_map[tx_key] += val

    # Evaluasi kesehatan menggunakan Metode OOP
    health = analyzer.evaluate_health(stats['income'], stats['expense'])

    sorted_accounts = sorted([item for item in account_balances.items() if item[1] != 0], key=lambda x: x[1], reverse=True)
    if not sorted_accounts: sorted_accounts = [('Cash', 0.0)]

    cursor.execute("""
        SELECT b.amount, COALESCE(SUM(t.nominal), 0) as spent
        FROM budgets b
        LEFT JOIN finance_transactions t ON b.category_id = t.category_id
        AND t.type = 'Pengeluaran' AND DATE_FORMAT(t.tgl, '%Y-%m') = b.period AND t.user_id = b.user_id
        WHERE b.period = %s AND b.user_id = %s
        GROUP BY b.id
    """, (curr_month, user_id))
    budgets_raw = cursor.fetchall()

    avg_budget_pct = 0
    if budgets_raw:
        tot_b_pct = sum((float(b['spent']) / float(b['amount']) * 100) if float(b['amount']) > 0 else 0 for b in budgets_raw)
        avg_budget_pct = int(tot_b_pct / len(budgets_raw))

    conn.close()

    max_in = max((d['in'] for d in daily_summary.values()), default=0.0)
    max_out = max((d['out'] for d in daily_summary.values()), default=0.0)
    for day_num, data in daily_summary.items():
        data['in_pct'] = max(25, int((data['in'] / max_in) * 100)) if max_in > 0 and data['in'] > 0 else 0
        data['out_pct'] = max(25, int((data['out'] / max_out) * 100)) if max_out > 0 and data['out'] > 0 else 0

    exp_labels = list(expense_cat.keys())
    exp_values = list(expense_cat.values())
    if not exp_labels: exp_labels, exp_values = ['Belum Ada Pengeluaran'], [1]

    inv_labels = [k for k, v in invest_allocation.items() if v > 0]
    inv_values = [v for k, v in invest_allocation.items() if v > 0]
    if not inv_labels: inv_labels, inv_values = ['Belum Ada Aset'], [1]

    month_names = ['', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    today_day = datetime.now().day if (sel_year == datetime.now().year and sel_month == datetime.now().month) else 0

    liquid_cash = stats['income'] - stats['expense'] - total_goals_funded - total_invested_modal
    net_worth = liquid_cash + total_goals_funded + total_invested_modal

    # Hitung rasio tabungan menggunakan Metode OOP
    savings_ratio_pct = analyzer.calculate_savings_ratio(stats['income'], stats['expense'])

    return render_template_string(
        TPL_DASHBOARD, stats=stats, health_score=health, recent_tx=all_tx[:3],
        chart_labels=exp_labels, chart_values=exp_values, inv_labels=inv_labels, inv_values=inv_values,
        calendar_grid=calendar_grid, daily_summary=daily_summary, daily_tx_json=json.dumps(daily_tx_map),
        sel_month=sel_month, sel_year=sel_year, month_names=month_names, today_day=today_day,
        start_date=start_str, end_date=end_str, trend_view=trend_view, trend_month=trend_month, trend_year=trend_year,
        trend_labels=trend_labels, trend_income=[trend_income_map[k] for k in trend_keys],
        trend_expense=[trend_expense_map[k] for k in trend_keys], trend_invest=[trend_invest_map[k] for k in trend_keys],
        liquid_cash=liquid_cash, account_balances=sorted_accounts, net_worth=net_worth,
        avg_budget_pct=avg_budget_pct, savings_ratio_pct=savings_ratio_pct
    )

@app.route('/transactions')
@login_required
def manage_transactions():
    filters = {
        'search': request.args.get('search', ''), 'period': request.args.get('period', ''),
        'account': request.args.get('account', ''), 'category_id': request.args.get('category_id', ''),
        'type': request.args.get('type', '')
    }
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT t.*, c.name as cat_name FROM finance_transactions t LEFT JOIN categories c ON t.category_id = c.id WHERE t.user_id=%s AND t.portfolio_id IS NULL AND t.goal_id IS NULL"
    params = [session['user_id']]

    if filters['search']: query += " AND (t.description LIKE %s OR c.name LIKE %s)"; params.extend([f"%{filters['search']}%", f"%{filters['search']}%"])
    if filters['period']: query += " AND t.tgl LIKE %s"; params.append(f"{filters['period']}-%")
    if filters['account']: query += " AND t.account = %s"; params.append(filters['account'])
    if filters['category_id']: query += " AND t.category_id = %s"; params.append(filters['category_id'])
    if filters['type']: query += " AND t.type = %s"; params.append(filters['type'])

    query += " ORDER BY t.tgl DESC"
    cursor.execute(query, tuple(params))
    txs = cursor.fetchall()

    cursor.execute("SELECT * FROM categories WHERE user_id=%s ORDER BY name ASC", (session['user_id'],))
    cats = cursor.fetchall()

    cursor.execute("SELECT * FROM user_accounts WHERE user_id=%s ORDER BY name ASC", (session['user_id'],))
    acc_objs = cursor.fetchall()
    acc_names = [a['name'] for a in acc_objs]
    if not acc_names: acc_names = ACCOUNTS

    conn.close()
    return render_template_string(TPL_TRANSACTIONS, transactions=txs, categories=cats, accounts=acc_names, account_objects=acc_objs, filters=filters, today=datetime.now().strftime('%Y-%m-%d'))

def get_account_balance(conn, account_name, user_id, exclude_tx_id=None):
    cursor = conn.cursor()
    query = "SELECT SUM(CASE WHEN type='Pemasukan' THEN nominal ELSE -nominal END) FROM finance_transactions WHERE account=%s AND user_id=%s"
    params = [account_name, user_id]
    if exclude_tx_id: query += " AND id != %s"; params.append(exclude_tx_id)
    cursor.execute(query, tuple(params))
    res = cursor.fetchone()[0]
    cursor.close()
    return float(res) if res else 0.0

def get_asset_qty(conn, portfolio_id, asset_type, asset_name, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(CASE WHEN type='Pengeluaran' THEN quantity ELSE -quantity END) FROM finance_transactions WHERE portfolio_id=%s AND asset_type=%s AND asset_name=%s AND user_id=%s", (portfolio_id, asset_type, asset_name, user_id))
    res = cursor.fetchone()[0]
    cursor.close()
    return float(res) if res else 0.0

@app.route('/transactions/add', methods=['POST'])
@login_required
def add_transaction():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            flash("Koneksi database gagal. Silakan coba kembali.", "danger")
            return redirect(url_for('manage_transactions'))

        type_str = request.form['type']
        acc = request.form['account']

        try:
            nominal = float(request.form['nominal'])
        except ValueError:
            flash("Gagal: Kolom nominal harus berupa angka, tidak boleh berisi huruf atau simbol!", "danger")
            return redirect(url_for('manage_transactions'))

        if nominal <= 0:
            flash("Gagal: Nominal transaksi harus lebih dari Rp0.", "danger")
            return redirect(url_for('manage_transactions'))

        if type_str == 'Pengeluaran':
            bal = get_account_balance(conn, acc, session['user_id'])
            if nominal > bal:
                flash(f"Gagal: Saldo {acc} tidak mencukupi! (Sisa: {format_rupiah(bal)})", "danger")
                return redirect(url_for('manage_transactions'))

        cursor = conn.cursor()
        cursor.execute("INSERT INTO finance_transactions (user_id, tgl, type, account, category_id, nominal, description) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (session['user_id'], request.form['tgl'], type_str, acc, request.form.get('category_id') or None, nominal, clean_string_input(request.form['description'])))
        conn.commit()
        flash("Transaksi berhasil dicatat!", "success")

    except Error as db_err:
        if conn:
            conn.rollback()
        flash(f"Database Error: Terjadi kesalahan pada sistem database ({db_err})", "danger")
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f"Sistem Error: Terjadi kesalahan tidak terduga ({e})", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return redirect(url_for('manage_transactions'))

@app.route('/transactions/edit', methods=['POST'])
@login_required
def edit_transaction():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            flash("Koneksi database gagal. Silakan coba kembali.", "danger")
            return redirect(url_for('manage_transactions'))

        tx_id, type_str, nominal, acc = request.form['tx_id'], request.form['type'], float(request.form['nominal']), request.form['account']

        if nominal <= 0:
            flash("Gagal Edit: Nominal transaksi harus lebih dari Rp0.", "danger")
            return redirect(url_for('manage_transactions'))

        if type_str == 'Pengeluaran':
            bal = get_account_balance(conn, acc, session['user_id'], exclude_tx_id=tx_id)
            if nominal > bal:
                flash(f"Gagal Edit: Saldo {acc} tidak mencukupi! (Sisa: {format_rupiah(bal)})", "danger")
                return redirect(url_for('manage_transactions'))

        cursor = conn.cursor()
        cursor.execute("UPDATE finance_transactions SET tgl=%s, type=%s, account=%s, category_id=%s, nominal=%s, description=%s WHERE id=%s AND user_id=%s",
                       (request.form['tgl'], type_str, acc, request.form.get('category_id') or None, nominal, clean_string_input(request.form['description']), tx_id, session['user_id']))
        conn.commit()
        flash("Transaksi berhasil diubah!", "success")
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f"Gagal edit: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('manage_transactions'))

@app.route('/transactions/transfer', methods=['POST'])
@login_required
def transfer_funds():
    conn = None
    cursor = None
    try:
        tgl, from_acc, to_acc, nominal, desc = request.form['tgl'], request.form['from_account'], request.form['to_account'], float(request.form['nominal']), clean_string_input(request.form['description'])
        if from_acc == to_acc: raise ValueError("Akun sumber dan tujuan sama!")
        if nominal <= 0: raise ValueError("Nominal transfer harus lebih dari Rp0!")

        conn = get_db_connection()
        if not conn:
            flash("Koneksi database gagal. Silakan coba kembali.", "danger")
            return redirect(url_for('manage_transactions'))

        bal = get_account_balance(conn, from_acc, session['user_id'])
        if nominal > bal:
            flash(f"Gagal Transfer: Saldo {from_acc} tidak mencukupi! (Sisa: {format_rupiah(bal)})", "danger")
            return redirect(url_for('manage_transactions'))

        desc = desc or f"Transfer ke {to_acc}"
        cursor = conn.cursor()
        cursor.execute("INSERT INTO finance_transactions (user_id, tgl, type, account, nominal, description) VALUES (%s, %s, 'Pengeluaran', %s, %s, %s)", (session['user_id'], tgl, from_acc, nominal, desc))
        cursor.execute("INSERT INTO finance_transactions (user_id, tgl, type, account, nominal, description) VALUES (%s, %s, 'Pemasukan', %s, %s, %s)", (session['user_id'], tgl, to_acc, nominal, f"Terima transfer dari {from_acc}"))
        conn.commit()
        flash(f"Transfer {format_rupiah(nominal)} ke {to_acc} berhasil.", "success")
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f"Gagal transfer: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('manage_transactions'))

@app.route('/transactions/bulk_action', methods=['POST'])
@login_required
def bulk_action():
    raw_ids = request.form.getlist('tx_ids')
    action = request.form.get('action')

    # Set digunakan untuk menyimpan ID numerik yang unik
    unique_ids = set()

    for item in raw_ids:
        if str(item).isdigit():
            unique_ids.add(int(item))

    # Diurutkan agar parameter query memiliki urutan yang konsisten
    ids = sorted(unique_ids)

    if action != 'delete':
        return redirect(url_for('manage_transactions'))

    if not ids:
        flash("Pilih minimal satu transaksi untuk dihapus.", "danger")
        return redirect(url_for('manage_transactions'))

    conn = None
    cursor = None

    try:
        conn = get_db_connection()

        if not conn:
            flash("Koneksi database gagal. Silakan coba kembali.", "danger")
            return redirect(url_for('manage_transactions'))

        cursor = conn.cursor()
        placeholders = ','.join(['%s'] * len(ids))

        cursor.execute(
            f"""
            DELETE FROM finance_transactions
            WHERE id IN ({placeholders}) AND user_id = %s
            """,
            tuple(ids) + (session['user_id'],)
        )

        deleted_count = cursor.rowcount
        conn.commit()

        flash(
            f"{deleted_count} transaksi dihapus.",
            "success"
        )

    except Exception as e:
        if conn:
            conn.rollback()

        flash(f"Gagal menghapus transaksi: {e}", "danger")

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

    return redirect(url_for('manage_transactions'))

@app.route('/accounts/add', methods=['POST'])
@login_required
def add_account():
    name = clean_string_input(request.form['name'])
    if name:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_accounts (user_id, name) VALUES (%s, %s)", (session['user_id'], name))
        conn.commit(); conn.close()
    return redirect(request.referrer or url_for('manage_transactions'))

@app.route('/accounts/delete/<int:id>', methods=['POST'])
@login_required
def delete_account(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_accounts WHERE id = %s AND user_id=%s", (id, session['user_id']))
        conn.commit(); conn.close()
    except Error: flash("Akun ini tidak bisa dihapus karena masih digunakan pada riwayat transaksi.", "danger")
    return redirect(request.referrer or url_for('manage_transactions'))

@app.route('/portfolios')
@login_required
def manage_portfolios():
    user_id = session['user_id']
    filters = {
        'search': request.args.get('search', ''), 'period': request.args.get('period', ''),
        'account': request.args.get('account', ''), 'platform': request.args.get('platform', ''), 'type': request.args.get('type', '')
    }

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM portfolios WHERE user_id=%s ORDER BY name ASC", (user_id,))
    ports = cursor.fetchall()
    cursor.execute("SELECT * FROM goals WHERE user_id=%s ORDER BY deadline ASC", (user_id,))
    goals = cursor.fetchall()

    cursor.execute("SELECT * FROM user_accounts WHERE user_id=%s ORDER BY name ASC", (session['user_id'],))
    acc_objs = cursor.fetchall()
    acc_names = [a['name'] for a in acc_objs]
    if not acc_names: acc_names = ACCOUNTS

    query = """
        SELECT t.*, p.name as port_name, g.name as goal_name
        FROM finance_transactions t
        LEFT JOIN portfolios p ON t.portfolio_id = p.id
        LEFT JOIN goals g ON t.goal_id = g.id
        WHERE t.user_id=%s AND (t.portfolio_id IS NOT NULL OR t.goal_id IS NOT NULL)
    """
    params = [user_id]
    if filters['search']: query += " AND (t.asset_name LIKE %s OR g.name LIKE %s)"; params.extend([f"%{filters['search']}%", f"%{filters['search']}%"])
    if filters['period']: query += " AND t.tgl LIKE %s"; params.append(f"{filters['period']}-%")
    if filters['account']: query += " AND t.account = %s"; params.append(filters['account'])
    if filters['platform']: query += " AND t.portfolio_id = %s"; params.append(filters['platform'])
    if filters['type']: query += " AND t.type = %s"; params.append(filters['type'])

    query += " ORDER BY t.tgl DESC, t.id DESC"
    cursor.execute(query, tuple(params))
    inv_tx = cursor.fetchall()

    cursor.execute("SELECT t.*, p.name as port_name FROM finance_transactions t JOIN portfolios p ON t.portfolio_id = p.id WHERE t.user_id=%s ORDER BY t.tgl DESC", (user_id,))
    all_inv_tx = cursor.fetchall()

    port_bals = {p['id']: {'name': p['name'], 'balance': 0.0, 'id': p['id']} for p in ports}
    holdings = {}

    for tx in all_inv_tx:
        if not tx['portfolio_id']: continue
        pid = tx['portfolio_id']
        atype = tx.get('asset_type') or 'Lainnya'
        aname = tx.get('asset_name') or 'Aset Umum'
        qty = float(tx.get('quantity') or 0)
        nom = float(tx['nominal'])
        h_key = (pid, atype, aname)

        if h_key not in holdings: holdings[h_key] = {'port_name': tx['port_name'], 'asset_type': atype, 'asset_name': aname, 'qty': 0.0, 'modal': 0.0}
        if tx['type'] == 'Pengeluaran':
            if pid in port_bals: port_bals[pid]['balance'] += nom
            holdings[h_key]['qty'] += qty; holdings[h_key]['modal'] += nom
        else:
            if pid in port_bals: port_bals[pid]['balance'] -= nom
            holdings[h_key]['qty'] -= qty; holdings[h_key]['modal'] -= nom

    active_holdings = [h for h in holdings.values() if h['qty'] > 0.0001]
    conn.close()

    return render_template_string(
        TPL_PORTFOLIOS, portfolios=ports, port_balances=port_bals.values(), inv_tx=inv_tx, active_holdings=active_holdings,
        total_assets=sum(p['balance'] for p in port_bals.values()), accounts=acc_names, account_objects=acc_objs, goals=goals, filters=filters, today=datetime.now().strftime('%Y-%m-%d')
    )

@app.route('/portfolios/transaction', methods=['POST'])
@login_required
def add_portfolio_tx():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            flash("Koneksi database gagal. Silakan coba kembali.", "danger")
            return redirect(url_for('manage_portfolios'))

        type_str, nominal, qty, acc = request.form['type'], float(request.form['nominal']), float(request.form['quantity'] or 0), request.form['account']
        pid = int(request.form.get('portfolio_id')) if request.form.get('portfolio_id') else None
        gid = int(request.form.get('goal_id')) if request.form.get('goal_id') else None
        asset_type = request.form.get('asset_type') or ''
        asset_name = clean_string_input(request.form.get('asset_name'))

        if nominal <= 0:
            flash("Gagal: Nominal investasi atau tabungan harus lebih dari Rp0.", "danger")
            return redirect(url_for('manage_portfolios'))
        if pid and qty <= 0:
            flash("Gagal: Kuantitas aset harus lebih dari 0.", "danger")
            return redirect(url_for('manage_portfolios'))

        if type_str == 'Pengeluaran':
            bal = get_account_balance(conn, acc, session['user_id'])
            if nominal > bal: flash(f"Gagal: Saldo {acc} tidak mencukupi! (Sisa: {format_rupiah(bal)})", "danger"); return redirect(url_for('manage_portfolios'))
        else:
            if pid:
                asset_qty_owned = get_asset_qty(conn, pid, asset_type, asset_name, session['user_id'])
                if qty > asset_qty_owned: flash(f"Gagal Jual Aset: Kuantitas {asset_name} tidak cukup!", "danger"); return redirect(url_for('manage_portfolios'))
            if gid:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT current_amount FROM goals WHERE id=%s AND user_id=%s", (gid, session['user_id']))
                goal_row = cursor.fetchone()
                if goal_row and nominal > float(goal_row['current_amount']): flash("Gagal Tarik: Saldo Goal tidak cukup!", "danger"); return redirect(url_for('manage_portfolios'))

        if cursor:
            cursor.close()
        cursor = conn.cursor()
        desc = f"{'Beli / Nabung' if type_str == 'Pengeluaran' else 'Jual / Tarik'} {asset_type}: {asset_name}" if asset_type else ("Nabung Goal" if type_str == 'Pengeluaran' else "Tarik Goal")

        cursor.execute("INSERT INTO finance_transactions (user_id, tgl, type, account, portfolio_id, goal_id, asset_type, asset_name, quantity, nominal, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (session['user_id'], request.form['tgl'], type_str, acc, pid, gid, asset_type, asset_name, qty, nominal, desc))
        if gid:
            if type_str == 'Pengeluaran': cursor.execute("UPDATE goals SET current_amount = current_amount + %s WHERE id = %s AND user_id=%s", (nominal, gid, session['user_id']))
            else: cursor.execute("UPDATE goals SET current_amount = current_amount - %s WHERE id = %s AND user_id=%s", (nominal, gid, session['user_id']))

        conn.commit()
        flash("Berhasil mencatat transaksi investasi.", "success")
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f"Gagal mencatat transaksi: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('manage_portfolios'))

@app.route('/portfolios/edit', methods=['POST'])
@login_required
def edit_portfolio_tx():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            flash("Koneksi database gagal. Silakan coba kembali.", "danger")
            return redirect(url_for('manage_portfolios'))

        cursor = conn.cursor(dictionary=True)
        tx_id, type_str, nominal, qty, acc = request.form['tx_id'], request.form['type'], float(request.form['nominal']), float(request.form['quantity'] or 0), request.form['account']
        pid = int(request.form.get('portfolio_id')) if request.form.get('portfolio_id') else None
        gid = int(request.form.get('goal_id')) if request.form.get('goal_id') else None
        asset_type, asset_name = request.form.get('asset_type') or '', clean_string_input(request.form.get('asset_name'))
        desc = f"{'Beli / Nabung' if type_str == 'Pengeluaran' else 'Jual / Tarik'} {asset_type}: {asset_name}" if asset_type else ("Nabung Goal" if type_str == 'Pengeluaran' else "Tarik Goal")

        if nominal <= 0:
            flash("Gagal Edit: Nominal investasi atau tabungan harus lebih dari Rp0.", "danger")
            return redirect(url_for('manage_portfolios'))
        if pid and qty <= 0:
            flash("Gagal Edit: Kuantitas aset harus lebih dari 0.", "danger")
            return redirect(url_for('manage_portfolios'))

        cursor.execute("SELECT * FROM finance_transactions WHERE id=%s AND user_id=%s", (tx_id, session['user_id']))
        old_tx = cursor.fetchone()
        if not old_tx: flash("Transaksi tidak ditemukan.", "danger"); return redirect(url_for('manage_portfolios'))

        if old_tx['goal_id']:
            old_nom = float(old_tx['nominal'])
            if old_tx['type'] == 'Pengeluaran': cursor.execute("UPDATE goals SET current_amount = current_amount - %s WHERE id = %s AND user_id = %s", (old_nom, old_tx['goal_id'], session['user_id']))
            else: cursor.execute("UPDATE goals SET current_amount = current_amount + %s WHERE id = %s AND user_id = %s", (old_nom, old_tx['goal_id'], session['user_id']))

        if gid:
            if type_str == 'Pengeluaran': cursor.execute("UPDATE goals SET current_amount = current_amount + %s WHERE id = %s AND user_id = %s", (nominal, gid, session['user_id']))
            else: cursor.execute("UPDATE goals SET current_amount = current_amount - %s WHERE id = %s AND user_id = %s", (nominal, gid, session['user_id']))

        cursor.execute("UPDATE finance_transactions SET tgl=%s, type=%s, account=%s, portfolio_id=%s, goal_id=%s, asset_type=%s, asset_name=%s, quantity=%s, nominal=%s, description=%s WHERE id=%s AND user_id=%s",
                       (request.form['tgl'], type_str, acc, pid, gid, asset_type, asset_name, qty, nominal, desc, tx_id, session['user_id']))
        conn.commit()
        flash("Riwayat aset/tabungan berhasil diubah!", "success")
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f"Gagal edit: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('manage_portfolios'))

@app.route('/portfolios/bulk_action', methods=['POST'])
@login_required
def bulk_action_portfolio():
    ids = request.form.getlist('tx_ids')
    conn = None
    cursor = None
    try:
        if request.form.get('action') == 'delete' and ids:
            ids_int = [int(item) for item in ids if str(item).isdigit()]
            if not ids_int:
                flash("Riwayat yang dipilih tidak valid.", "danger")
                return redirect(url_for('manage_portfolios'))

            conn = get_db_connection()
            if not conn:
                flash("Koneksi database gagal. Silakan coba kembali.", "danger")
                return redirect(url_for('manage_portfolios'))

            cursor = conn.cursor(dictionary=True)
            format_strings = ','.join(['%s'] * len(ids_int))
            cursor.execute(f"SELECT goal_id, type, nominal FROM finance_transactions WHERE id IN ({format_strings}) AND goal_id IS NOT NULL AND user_id=%s", tuple(ids_int) + (session['user_id'],))
            txs_to_revert = cursor.fetchall()

            for tx in txs_to_revert:
                gid, nom = tx['goal_id'], float(tx['nominal'])
                if tx['type'] == 'Pengeluaran': cursor.execute("UPDATE goals SET current_amount = current_amount - %s WHERE id = %s AND user_id = %s", (nom, gid, session['user_id']))
                else: cursor.execute("UPDATE goals SET current_amount = current_amount + %s WHERE id = %s AND user_id = %s", (nom, gid, session['user_id']))

            cursor.execute(f"DELETE FROM finance_transactions WHERE id IN ({format_strings}) AND user_id=%s", tuple(ids_int) + (session['user_id'],))
            conn.commit()
            flash(f"{len(ids_int)} riwayat investasi/tabungan dihapus.", "success")
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f"Gagal menghapus riwayat investasi/tabungan: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('manage_portfolios'))

@app.route('/portfolios/add', methods=['POST'])
@login_required
def add_portfolio():
    name = clean_string_input(request.form['name'])
    if name:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO portfolios (user_id, name) VALUES (%s, %s)", (session['user_id'], name))
        conn.commit(); conn.close()
    return redirect(url_for('manage_portfolios'))

@app.route('/portfolios/delete/<int:id>', methods=['POST'])
@login_required
def delete_portfolio(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM portfolios WHERE id = %s AND user_id=%s", (id, session['user_id']))
        conn.commit(); conn.close()
    except Error: flash("Platform masih digunakan pada riwayat transaksi aset.", "danger")
    return redirect(url_for('manage_portfolios'))

@app.route('/budgets')
@login_required
def manage_budgets():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    curr_period = request.args.get('period', datetime.now().strftime('%Y-%m'))
    try: sel_year, sel_month = curr_period.split('-')
    except ValueError:
        curr_period = datetime.now().strftime('%Y-%m')
        sel_year, sel_month = curr_period.split('-')

    cursor.execute("""
        SELECT b.id, b.amount, c.name as cat_name,
        COALESCE((SELECT SUM(nominal) FROM finance_transactions t WHERE t.category_id = b.category_id AND t.type='Pengeluaran' AND DATE_FORMAT(t.tgl, '%Y-%m') = b.period AND t.portfolio_id IS NULL AND t.goal_id IS NULL AND t.user_id = b.user_id), 0) as spent
        FROM budgets b JOIN categories c ON b.category_id = c.id WHERE b.period = %s AND b.user_id = %s
    """, (curr_period, session['user_id']))
    budgets = cursor.fetchall()

    cursor.execute("SELECT * FROM categories WHERE user_id=%s ORDER BY name ASC", (session['user_id'],))
    cats = cursor.fetchall()
    conn.close()

    b_labels = [b['cat_name'] for b in budgets]
    b_limits = [float(b['amount']) for b in budgets]
    b_spent = [float(b['spent']) for b in budgets]
    total_rem = sum(b_limits) - sum(b_spent)

    now = datetime.now()
    if int(sel_year) == now.year and int(sel_month) == now.month:
        days_left = max(1, calendar.monthrange(now.year, now.month)[1] - now.day + 1)
    elif int(sel_year) < now.year or (int(sel_year) == now.year and int(sel_month) < now.month): days_left = 1
    else: days_left = calendar.monthrange(int(sel_year), int(sel_month))[1]

    safe_daily = (total_rem / days_left) if total_rem > 0 else 0
    return render_template_string(TPL_BUDGETS, budgets=budgets, categories=cats, budget_labels=b_labels, budget_limits=b_limits, budget_spent=b_spent, days_left=days_left, curr_period=curr_period, safe_daily_budget=safe_daily)

@app.route('/goals/add', methods=['POST'])
@login_required
def add_goal():
    conn = None
    cursor = None
    try:
        name = clean_string_input(request.form['name'])
        target_amount = float(request.form['target_amount'])
        if not name:
            raise ValueError("Nama target tabungan wajib diisi.")
        if target_amount <= 0:
            raise ValueError("Nominal target tabungan harus lebih dari Rp0.")

        conn = get_db_connection()
        if not conn:
            flash("Koneksi database gagal. Silakan coba kembali.", "danger")
            return redirect(url_for('manage_portfolios'))

        cursor = conn.cursor()
        cursor.execute("INSERT INTO goals (user_id, name, target_amount, deadline) VALUES (%s, %s, %s, %s)", (session['user_id'], name, target_amount, request.form['deadline']))
        conn.commit()
    except (KeyError, ValueError) as e:
        if conn:
            conn.rollback()
        flash(f"Gagal membuat target tabungan: {e}", "danger")
    except Error as e:
        if conn:
            conn.rollback()
        flash(f"Gagal membuat target tabungan karena gangguan database: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('manage_portfolios'))

@app.route('/goals/delete/<int:id>', methods=['POST'])
@login_required
def delete_goal(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM goals WHERE id=%s AND user_id=%s", (id, session['user_id']))
    conn.commit(); conn.close()
    return redirect(url_for('manage_portfolios'))

@app.route('/budgets/add', methods=['POST'])
@login_required
def add_budget():
    conn = None
    cursor = None
    period = request.form.get('period', datetime.now().strftime('%Y-%m'))
    try:
        amount = float(request.form['amount'])
        if amount <= 0:
            raise ValueError("Nominal anggaran harus lebih dari Rp0.")

        conn = get_db_connection()
        if not conn:
            flash("Koneksi database gagal. Silakan coba kembali.", "danger")
            return redirect(f"/budgets?period={period}")

        cursor = conn.cursor()
        cursor.execute("INSERT INTO budgets (user_id, category_id, period, amount) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE amount=%s",
                       (session['user_id'], request.form['category_id'], period, amount, amount))
        conn.commit()
        flash(f"Anggaran untuk bulan {period} disimpan.", "success")
    except Exception as e:
        if conn:
            conn.rollback()
        flash(str(e), "danger")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(f"/budgets?period={period}")

@app.route('/budgets/delete/<int:id>', methods=['POST'])
@login_required
def delete_budget(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM budgets WHERE id=%s AND user_id=%s", (id, session['user_id']))
    conn.commit(); conn.close()
    return redirect(request.referrer or url_for('manage_budgets'))

@app.route('/reports')
@login_required
def reports():
    sel_month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.*, p.name as port_name, c.name as cat_name
        FROM finance_transactions t LEFT JOIN portfolios p ON t.portfolio_id = p.id LEFT JOIN categories c ON t.category_id = c.id
        WHERE t.user_id=%s AND DATE_FORMAT(t.tgl, '%Y-%m') <= %s ORDER BY t.tgl ASC, t.id ASC
    """, (session['user_id'], sel_month))
    all_tx = cursor.fetchall()
    conn.close()

    ledger, balance, tot_in, tot_out = [], 0.0, 0.0, 0.0
    for tx in all_tx:
        nom = float(tx['nominal'])
        is_month = (tx['tgl'].strftime('%Y-%m') if isinstance(tx['tgl'], date) else str(tx['tgl'])[:7]) == sel_month
        if tx['type'] == 'Pemasukan': balance += nom
        else: balance -= nom

        if is_month:
            pos = tx['cat_name'] or tx['asset_name'] or tx['port_name'] or 'Lainnya'
            if tx['type'] == 'Pemasukan': debit, kredit = nom, 0.0; tot_in += nom
            else: debit, kredit = 0.0, nom; tot_out += nom
            ledger.append({'tgl': tx['tgl'], 'account': tx['account'], 'desc': tx['description'], 'pos': pos, 'debit': debit, 'kredit': kredit, 'saldo': balance})

    return render_template_string(TPL_REPORTS, ledger=reversed(ledger), total_debit=tot_in, total_kredit=tot_out, selected_month=sel_month)

@app.route('/export/pdf')
@login_required
def export_pdf():
    sel_month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT t.*, p.name as port_name, c.name as cat_name FROM finance_transactions t LEFT JOIN portfolios p ON t.portfolio_id = p.id LEFT JOIN categories c ON t.category_id = c.id WHERE t.user_id=%s AND DATE_FORMAT(t.tgl, '%Y-%m') <= %s ORDER BY t.tgl ASC, t.id ASC", (session['user_id'], sel_month))
    data = cursor.fetchall()
    conn.close()

    buf = io.BytesIO()
    p = canvas.Canvas(buf, pagesize=A4)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 800, f"LAPORAN ARUS KAS - {sel_month}")
    p.setFont("Helvetica", 10)
    p.drawString(50, 780, f"Dicetak pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} oleh {session['username']}")

    y = 740
    p.setFont("Helvetica-Bold", 10)
    for i, title in enumerate(["Tanggal", "Akun", "Pos", "Deskripsi", "Masuk (Db)", "Keluar (Cr)", "Saldo"]):
        p.drawString(50 + [0, 60, 120, 190, 290, 360, 430][i], y, title)

    p.line(50, y-5, 550, y-5); y -= 20
    p.setFont("Helvetica", 9)

    bal, tot_in, tot_out = 0.0, 0.0, 0.0
    for r in data:
        nom = float(r['nominal'])
        if r['type'] == 'Pemasukan': bal += nom
        else: bal -= nom
        if (r['tgl'].strftime('%Y-%m') if isinstance(r['tgl'], date) else str(r['tgl'])[:7]) == sel_month:
            pos = str(r['cat_name'] or r['asset_name'] or r['port_name'] or "Lainnya")[:10]
            desc = str(r['description'])[:12] + ".." if len(str(r['description']))>12 else str(r['description'])
            if r['type'] == 'Pemasukan': db, cr = format_rupiah(nom), "-"; tot_in += nom
            else: db, cr = "-", format_rupiah(nom); tot_out += nom

            for i, val in enumerate([str(r['tgl']), str(r['account'])[:8], pos, desc, db, cr, format_rupiah(bal)]):
                p.drawString(50 + [0, 60, 120, 190, 290, 360, 430][i], y, val)
            y -= 20
            if y < 100: p.showPage(); p.setFont("Helvetica", 9); y = 800

    p.line(50, y, 550, y); y -= 20
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "TOTAL"); p.drawString(290, y, format_rupiah(tot_in)); p.drawString(360, y, format_rupiah(tot_out))

    p.save(); buf.seek(0)
    return send_file(buf, as_attachment=True, download_name=f'ArusKas_{sel_month}.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
