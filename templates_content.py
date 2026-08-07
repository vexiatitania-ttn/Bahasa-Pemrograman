TPL_AUTH = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Fyna Cchio</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Outfit', sans-serif; background-color: #f8f9fa; margin: 0; padding: 0; overflow-x: hidden; }
        .split-container { display: flex; min-height: 100vh; }
        .left-side {
            flex: 1;
            background: linear-gradient(135deg, #FFD861 0%, #F59E0B 100%);
            position: relative;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            color: #303030; padding: 4rem; text-align: center;
            overflow: hidden;
        }
        .left-side::before {
            content: ''; position: absolute; width: 150%; height: 150%;
            background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 60%);
            top: -25%; left: -25%;
        }
        .right-side { flex: 1; display: flex; justify-content: center; align-items: center; background-color: #F1F1F1; padding: 2rem; position: relative; }
        .auth-card {
            background: #ffffff; padding: 3.5rem 3rem; border-radius: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.08); width: 100%; max-width: 450px;
            position: relative; z-index: 10;
        }
        .brand-logo-large { font-size: 4rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 1rem; position: relative; z-index: 1; }
        .brand-tagline { font-size: 1.2rem; font-weight: 400; opacity: 0.9; max-width: 80%; position: relative; z-index: 1; }
        .form-control-custom { border-radius: 20px; padding: 0.8rem 1.5rem; background: #f8f9fa; border: 1px solid transparent; transition: 0.3s; }
        .form-control-custom:focus { background: #fff; border-color: #FFD861; box-shadow: 0 0 0 0.25rem rgba(255, 216, 97, 0.25); }
        .btn-auth { border-radius: 20px; padding: 0.8rem; font-weight: 600; font-size: 1rem; width: 100%; border: none; transition: 0.3s; }
        .btn-auth-primary { background-color: #303030; color: #FFD861; }
        .btn-auth-primary:hover { background-color: #1a1a1a; transform: translateY(-2px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
        .toast-container { position: fixed; top: 20px; right: 20px; z-index: 9999; }
        @media (max-width: 768px) {
            .split-container { flex-direction: column; }
            .left-side { padding: 3rem 1.5rem; flex: none; min-height: 30vh; }
            .brand-logo-large { font-size: 2.5rem; }
            .right-side { padding: 1.5rem; align-items: flex-start; }
            .auth-card { padding: 2rem 1.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
        }
    </style>
</head>
<body>
    <div class="toast-container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="toast align-items-center text-bg-{{ 'danger' if category == 'danger' else 'success' }} border-0 show mb-2" role="alert">
                        <div class="d-flex">
                            <div class="toast-body fw-medium"><i class="bi bi-info-circle me-2"></i> {{ message }}</div>
                            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                        </div>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>
    <div class="split-container">
        <div class="left-side">
            <img src="{{ url_for('static', filename='logo1.svg') }}" width="80" height="90" class="mb-3 position-relative z-1" alt="Logo Fyna Cchio">

            <div class="brand-logo-large">Fyna<span style="font-weight: 300;">Cchio</span></div>
            <div class="brand-tagline">Atur duit biar gak cuma jadi kenangan pas tanggal tua.</div>
        </div>
        <div class="right-side">
            <!-- CONTENT_AUTH_PLACEHOLDER -->
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>setTimeout(() => { document.querySelectorAll('.toast').forEach(t => new bootstrap.Toast(t).hide()); }, 4000);</script>
</body>
</html>
"""

HTML_LOGIN = """
<div class="auth-card">
    <div class="text-center mb-4">
        <h3 class="fw-bold text-dark mb-1">Welcome Back 👋</h3>
        <p class="text-muted small">Silakan masuk ke akun Anda.</p>
    </div>
    <form action="/login" method="POST">
        <div class="mb-3">
            <label class="form-label small fw-semibold text-muted ms-1">Username</label>
            <input type="text" name="username" class="form-control form-control-custom" placeholder="contoh: budi123" required>
        </div>
        <div class="mb-4">
            <label class="form-label small fw-semibold text-muted ms-1">Password</label>
            <input type="password" name="password" class="form-control form-control-custom" placeholder="••••••••" required>
        </div>
        <button type="submit" class="btn btn-auth btn-auth-primary mb-3">Login Sekarang</button>
    </form>
    <div class="text-center mt-3">
        <span class="text-muted small">Belum punya akun? <a href="/register" class="text-dark fw-bold text-decoration-none border-bottom border-dark">Daftar di sini</a></span>
    </div>
</div>
"""

HTML_REGISTER = """
<div class="auth-card">
    <div class="text-center mb-4">
        <h3 class="fw-bold text-dark mb-1">Let's Get Started!</h3>
        <p class="text-muted small">Buat akun untuk membangun portofolio Anda.</p>
    </div>
    <form action="/register" method="POST">
        <div class="mb-3">
            <label class="form-label small fw-semibold text-muted ms-1">Display Name</label>
            <input type="text" name="display_name" class="form-control form-control-custom" placeholder="contoh: Budi Santoso" required>
        </div>
        <div class="mb-3">
            <label class="form-label small fw-semibold text-muted ms-1">Username</label>
            <input type="text" name="username" class="form-control form-control-custom" placeholder="Username unik (tanpa spasi)" required pattern="[A-Za-z0-9_]{3,20}" title="Huruf dan angka saja, tanpa spasi">
        </div>
        <div class="mb-4">
            <label class="form-label small fw-semibold text-muted ms-1">Password</label>
            <input type="password" name="password" class="form-control form-control-custom" placeholder="Minimal 4 karakter" required minlength="4">
        </div>
        <button type="submit" class="btn btn-auth btn-auth-primary mb-3">Buat Akun Gratis</button>
    </form>
    <div class="text-center mt-3">
        <span class="text-muted small">Sudah punya akun? <a href="/login" class="text-dark fw-bold text-decoration-none border-bottom border-dark">Masuk di sini</a></span>
    </div>
</div>
"""

TPL_BASE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fyna Cchio - Ekosistem Finansial</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root { --bg-outer: #E4E5E7; --bg-inner: #F1F1F1; --bg-tint: #F3EAC7; --accent-yellow: #FFD861; --text-dark: #303030; --text-muted: #888888; }
        body { font-family: 'Outfit', sans-serif; background-color: var(--bg-outer); color: var(--text-dark); min-height: 100vh; padding: 2rem; margin: 0; }
        .app-container { max-width: 1400px; margin: auto; min-height: 88vh; background: linear-gradient(170deg, var(--bg-inner) 60%, var(--bg-tint) 100%); border-radius: 40px; padding: 2.5rem 3.5rem; box-shadow: 0 20px 50px rgba(0,0,0,0.05); }
        .top-nav { display: flex; justify-content: space-between; align-items: center; margin-bottom: 3rem; }
        .brand-logo { font-weight: 600; font-size: 1.3rem; display: flex; align-items: center; gap: 0.8rem; color: var(--text-dark); text-decoration: none; }
        .nav-pills-custom { background: rgba(255, 255, 255, 0.5); padding: 0.4rem; border-radius: 40px; display: flex; gap: 0.2rem; }
        .nav-pills-custom .nav-link { color: var(--text-muted); border-radius: 30px; padding: 0.6rem 1.8rem; font-weight: 500; transition: 0.3s; }
        .nav-pills-custom .nav-link:hover { color: var(--text-dark); }
        .nav-pills-custom .nav-link.active { background: var(--text-dark); color: var(--accent-yellow); }
        .card-custom { border: none; border-radius: 30px; background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(20px); padding: 1.5rem 1.8rem; box-shadow: 0 10px 30px rgba(0,0,0,0.02); height: 100%; transition: transform 0.2s ease, box-shadow 0.2s ease; }
        .card-custom-hover:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0,0,0,0.06); }
        .card-dark { background: var(--text-dark); color: #fff; }
        .btn-custom { border-radius: 30px; padding: 0.6rem 1.5rem; font-weight: 500; border: none; transition: 0.3s; }
        .btn-dark-custom { background: var(--text-dark); color: #fff; }
        .btn-dark-custom:hover { background: #404040; color: var(--accent-yellow); }
        .btn-yellow { background: var(--accent-yellow); color: var(--text-dark); font-weight: 600; }
        .form-control-custom, .form-select-custom { border-radius: 30px; border: 1px solid rgba(0,0,0,0.05); background: #ffffff; padding: 0.8rem 1.5rem; }
        .table-modern { border-collapse: separate; border-spacing: 0 10px; width: 100%; }
        .table-modern th { border: none; font-weight: 500; color: var(--text-muted); padding: 0.5rem 1.5rem; font-size: 0.9rem; }
        .table-modern tbody tr { background: #ffffff; box-shadow: 0 2px 8px rgba(0,0,0,0.02); transition: 0.2s; }
        .table-modern tbody tr:hover { transform: scale(1.005); box-shadow: 0 5px 15px rgba(255, 216, 97, 0.35); }
        .table-modern tbody tr:hover td { background-color: #FFD861 !important; transition: background-color 0.2s ease; }
        .table-modern td { border: none; padding: 1.2rem 1.5rem; vertical-align: middle; background-color: #ffffff; }
        .table-modern td:first-child { border-top-left-radius: 20px; border-bottom-left-radius: 20px; }
        .table-modern td:last-child { border-top-right-radius: 20px; border-bottom-right-radius: 20px; }
        .badge-pill { padding: 0.6em 1.2em; border-radius: 20px; font-weight: 500; font-size: 0.85rem; }
        .title-huge { font-size: 3rem; font-weight: 300; letter-spacing: -1px; line-height: 1.1; }
        .modal-content { border-radius: 30px; border: none; background: var(--bg-inner); padding: 1.5rem; }
        .toast-container { position: fixed; bottom: 20px; right: 20px; z-index: 9999; }
        .calendar-cell { transition: 0.2s; }
        .calendar-cell:hover { background-color: #FFFCE8 !important; border-color: #FFD861 !important; }
        .custom-scrollbar::-webkit-scrollbar { height: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.2); }

        /* CSS Sorting Header Table */
        th.sortable { cursor: pointer; user-select: none; transition: 0.2s; white-space: nowrap; }
        th.sortable:hover { color: var(--text-dark); }
        .sort-icon { font-size: 0.75rem; vertical-align: middle; }
    </style>
</head>
<body>
    <div class="app-container">
        <nav class="top-nav">
            <a href="/" class="brand-logo">
                <img src="{{ url_for('static', filename='logo2.svg') }}" style="height: 35px; width: auto;" alt="Logo Fyna Cchio">

                Fyna<span style="font-weight: 300; margin-left: 2px;">Cchio</span>
            </a>
            <div class="nav-pills-custom" id="mainNav">
                <a class="nav-link" href="/" data-path="/">Dashboard</a>
                <a class="nav-link" href="/transactions" data-path="/transactions">Transaksi</a>
                <a class="nav-link" href="/portfolios" data-path="/portfolios">Investasi</a>
                <a class="nav-link" href="/budgets" data-path="/budgets">Anggaran</a>
                <a class="nav-link" href="/reports" data-path="/reports">Laporan</a>
            </div>
            <div class="d-flex gap-2 align-items-center">
                <a href="#" class="btn btn-dark-custom rounded-circle p-0 d-flex align-items-center justify-content-center overflow-hidden" data-bs-toggle="modal" data-bs-target="#userProfileModal" style="width: 42px; height: 42px; border: 2px solid #FFD861;" title="Pengaturan Akun">
                    {% if current_avatar %}
                        <img src="{{ current_avatar }}" style="width: 100%; height: 100%; object-fit: cover;">
                    {% else %}
                        <span class="fw-bold" style="color: #FFD861; font-size: 1.2rem;">{{ current_display_name[:1] | upper if current_display_name else 'U' }}</span>
                    {% endif %}
                </a>
            </div>
        </nav>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'warning' if category == 'danger' else 'dark' }} alert-dismissible fade show rounded-4 bg-white border-0 shadow-sm">
                        <i class="bi bi-info-circle me-2"></i> {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <div class="toast-container" id="toastContainer"></div>

        <!-- Pengaturan Profil -->
        <div class="modal fade" id="userProfileModal">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content p-2">
                    <div class="modal-header border-0 pb-0">
                        <h5 class="modal-title fw-bold">Pengaturan Akun</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center pt-2 pb-4">
                        <form action="/edit_profile" method="POST">
                            <input type="file" id="avatarInput" accept="image/*" style="display: none;" onchange="previewAvatar(this)">
                            <input type="hidden" name="avatar_base64" id="avatarBase64" value="{{ current_avatar }}">

                            <div class="position-relative d-inline-block mb-1">
                                <div id="avatarPreviewContainer" style="width: 85px; height: 85px; background: {% if current_avatar %}transparent{% else %}#FFD861{% endif %}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; font-weight: bold; margin: 0 auto; color:#303030; cursor: pointer; overflow: hidden; border: 2px solid #E4E5E7;" onclick="document.getElementById('avatarInput').click()" title="Ubah Foto Profil">
                                    {% if current_avatar %}
                                        <img id="avatarPreview" src="{{ current_avatar }}" style="width: 100%; height: 100%; object-fit: cover;">
                                        <span id="avatarInitial" style="display: none;">{{ current_display_name[:1] | upper }}</span>
                                    {% else %}
                                        <span id="avatarInitial">{{ current_display_name[:1] | upper }}</span>
                                        <img id="avatarPreview" style="width: 100%; height: 100%; object-fit: cover; display: none;">
                                    {% endif %}
                                </div>
                                <div class="position-absolute bottom-0 end-0 bg-dark text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 28px; height: 28px; cursor: pointer; border: 2px solid #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.2);" onclick="document.getElementById('avatarInput').click()" title="Ubah Foto"><i class="bi bi-camera-fill" style="font-size: 0.8rem;"></i></div>
                            </div>

                            <!-- Tombol Hapus Avatar Dinamis -->
                            <div class="mb-3">
                                <button type="button" class="btn btn-link btn-sm text-danger text-decoration-none p-0 fw-medium" id="btnRemoveAvatar" onclick="removeAvatar()" style="display: {% if current_avatar %}inline-block{% else %}none{% endif %};"><i class="bi bi-trash3 me-1"></i>Hapus Foto Profil</button>
                            </div>

                            <div class="mb-3 text-start">
                                <label class="form-label small text-muted ms-1 mb-1 fw-medium">Nama Tampilan</label>
                                <input type="text" name="display_name" class="form-control form-control-custom" value="{{ current_display_name }}" required>
                            </div>
                            <div class="mb-3 text-start">
                                <label class="form-label small text-muted ms-1 mb-1 fw-medium">Username</label>
                                <input type="text" name="username" class="form-control form-control-custom" value="{{ current_username }}" required pattern="[A-Za-z0-9_]{3,20}" title="Huruf dan angka saja">
                            </div>
                            <div class="mb-4 text-start">
                                <label class="form-label small text-muted ms-1 mb-1 fw-medium">Password Baru <span class="fw-normal">(Opsional)</span></label>
                                <input type="password" name="password" class="form-control form-control-custom" placeholder="Kosongkan jika tidak ingin diubah" minlength="4">
                            </div>

                            <button type="submit" class="btn btn-dark-custom btn-custom w-100 mb-2">Simpan Perubahan</button>
                            <a href="/logout" class="btn btn-light btn-custom w-100 text-danger border fw-medium"><i class="bi bi-box-arrow-right me-2"></i>Keluar (Logout)</a>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <!-- CONTENT_PLACEHOLDER -->

        <div class="text-center mt-5 pb-3 d-none">
            <span class="badge bg-light text-muted border px-3 py-2" style="font-weight: 400; font-size: 0.75rem;">
                <i class="bi bi-server me-1"></i> Boot Server: {{ global_boot_time }} |
                <i class="bi bi-people-fill ms-2 me-1"></i> Trafik Sesi Aktif: {{ global_active_sessions }}
            </span>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const currentPath = window.location.pathname;
        document.querySelectorAll('.nav-pills-custom .nav-link').forEach(link => {
            if(link.getAttribute('data-path') === currentPath || (currentPath.startsWith(link.getAttribute('data-path')) && link.getAttribute('data-path') !== '/')) { link.classList.add('active'); }
            else if (currentPath === '/' && link.getAttribute('data-path') === '/') { link.classList.add('active'); }
        });
        if(window.Chart) { Chart.defaults.font.family = 'Outfit'; Chart.defaults.color = '#303030'; }

        function showToast(message, type='warning') {
            const container = document.getElementById('toastContainer');
            container.innerHTML = `<div class="toast align-items-center text-bg-${type} border-0 show"><div class="d-flex"><div class="toast-body fw-medium">${message}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div></div>`;
            new bootstrap.Toast(container.firstElementChild, { delay: 3000 }).show();
        }

        // Kompresi Gambar Otomatis
        function previewAvatar(input) {
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const img = new Image();
                    img.onload = function() {
                        const canvas = document.createElement('canvas');
                        const MAX_SIZE = 150;
                        let width = img.width;
                        let height = img.height;
                        if (width > height) {
                            if (width > MAX_SIZE) { height *= MAX_SIZE / width; width = MAX_SIZE; }
                        } else {
                            if (height > MAX_SIZE) { width *= MAX_SIZE / height; height = MAX_SIZE; }
                        }
                        canvas.width = width;
                        canvas.height = height;
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(img, 0, 0, width, height);
                        const base64 = canvas.toDataURL('image/jpeg', 0.8);

                        document.getElementById('avatarBase64').value = base64;
                        document.getElementById('avatarPreview').src = base64;
                        document.getElementById('avatarPreview').style.display = 'block';
                        const initial = document.getElementById('avatarInitial');
                        if(initial) initial.style.display = 'none';
                        document.getElementById('avatarPreviewContainer').style.background = 'transparent';
                        document.getElementById('btnRemoveAvatar').style.display = 'inline-block';
                    }
                    img.src = e.target.result;
                }
                reader.readAsDataURL(input.files[0]);
            }
        }

        // Hapus Foto Profil 
        function removeAvatar() {
            document.getElementById('avatarBase64').value = '';
            document.getElementById('avatarPreview').src = '';
            document.getElementById('avatarPreview').style.display = 'none';
            const initial = document.getElementById('avatarInitial');
            if(initial) initial.style.display = 'block';
            document.getElementById('avatarPreviewContainer').style.background = '#FFD861';
            document.getElementById('btnRemoveAvatar').style.display = 'none';
            document.getElementById('avatarInput').value = ''; // Reset input file
        }

        document.querySelectorAll('select, input[type="date"], input[type="month"]').forEach(el => {
            el.addEventListener('change', () => { sessionStorage.setItem('fyna_scroll_pos', window.scrollY); });
        });
        window.addEventListener('DOMContentLoaded', () => {
            const savedPos = sessionStorage.getItem('fyna_scroll_pos');
            if (savedPos && parseInt(savedPos, 10) > 0) {
                window.scrollTo(0, parseInt(savedPos, 10));
                sessionStorage.removeItem('fyna_scroll_pos');
            }
        });

        // FUNGSI SORTING TABEL (3-STATE: ASC -> DESC -> DEFAULT)
        function sortTable(tableId, colIndex) {
            const table = document.getElementById(tableId);
            if (!table) return;
            const tbody = table.querySelector("tbody");
            const rows = Array.from(tbody.querySelectorAll("tr"));

            // Simpan indeks asli (default) saat pertama kali fungsi dipanggil
            if (!table.dataset.indexed) {
                rows.forEach((row, i) => row.setAttribute('data-orig-idx', i));
                table.dataset.indexed = 'true';
            }

            const allThs = table.querySelectorAll("thead th");
            const targetTh = allThs[colIndex];

            // Tentukan state: asc -> desc -> default -> asc
            let dir = 'asc';
            if (targetTh.classList.contains("asc")) {
                dir = 'desc';
            } else if (targetTh.classList.contains("desc")) {
                dir = 'default';
            }

            // Reset semua tampilan header
            allThs.forEach(h => {
                h.classList.remove("asc", "desc");
                let icon = h.querySelector('.sort-icon');
                if(icon) { icon.className = 'bi bi-chevron-expand sort-icon opacity-50 ms-1'; }
            });

            if (dir === 'default') {
                // State ke-3: Kembalikan ke urutan asli database
                rows.sort((a, b) => parseInt(a.getAttribute('data-orig-idx')) - parseInt(b.getAttribute('data-orig-idx')));
            } else {
                // State 1 & 2: Terapkan Ascending atau Descending
                targetTh.classList.add(dir);
                let activeIcon = targetTh.querySelector('.sort-icon');
                if(activeIcon) { activeIcon.className = dir === 'asc' ? 'bi bi-chevron-up sort-icon text-dark ms-1' : 'bi bi-chevron-down sort-icon text-dark ms-1'; }

                if(rows.length === 1 && rows[0].cells.length === 1) return; // Skip if empty row placeholder

                rows.sort((a, b) => {
                    let valA = a.cells[colIndex].innerText.trim();
                    let valB = b.cells[colIndex].innerText.trim();

                    function parseValue(val) {
                        // Regex angka yang aman di dalam template Python.
                        if (val.startsWith('Rp') || val.startsWith('+Rp') || val.startsWith('-Rp')) {
                            return parseFloat(val.replace(/[Rp.+ ]/g, '').replace(',', '.')) || 0;
                        }
                        if (val.match(/^[0-9]{4}-[0-9]{2}-[0-9]{2}/)) {
                            return Date.parse(val.substring(0, 10)) || 0;
                        }
                        if (val.match(/^[0-9]/)) {
                            let num = parseFloat(val);
                            if(!isNaN(num)) return num;
                        }
                        return val.toLowerCase();
                    }

                    let parsedA = parseValue(valA);
                    let parsedB = parseValue(valB);

                    if (parsedA < parsedB) return dir === 'asc' ? -1 : 1;
                    if (parsedA > parsedB) return dir === 'asc' ? 1 : -1;
                    return 0;
                });
            }

            rows.forEach(row => tbody.appendChild(row));
        }
    </script>
</body>
</html>
"""

HTML_DASHBOARD = """
<div class="row mb-5 align-items-end">
    <div class="col-md-8">
        <h1 class="fw-light mb-2 title-huge text-dark">Welcome Back, <span class="fw-bold">{{ current_display_name }}</span></h1>
        <div class="d-flex align-items-center gap-3"><p class="text-muted mb-0">Skor Kesehatan</p><span class="badge-pill badge-yellow text-dark" style="background: var(--accent-yellow)">{{ health_score }}</span></div>
    </div>
</div>

<div class="row g-4 mb-4">
    <div class="col-md-4"><div class="card-custom card-dark d-flex flex-column justify-content-between p-4"><div class="d-flex justify-content-between mb-4"><span class="fs-5 text-white opacity-75">Kas & Saldo Cair</span><i class="bi bi-wallet-fill fs-4 text-white opacity-50"></i></div><div><div class="title-huge text-white mb-2">{{ liquid_cash | rupiah }}</div><div class="text-white opacity-75 small">Sisa Kas di Bank & E-Wallet</div></div></div></div>
    <div class="col-md-4"><div class="card-custom d-flex flex-column justify-content-between p-4" style="background: var(--accent-yellow);"><div class="d-flex justify-content-between mb-4"><span class="fs-5 text-dark fw-medium opacity-75">Total Pemasukan</span><i class="bi bi-arrow-down-left fs-4 text-dark opacity-50"></i></div><div><div class="title-huge text-dark mb-2">{{ stats.income | rupiah }}</div><div class="text-dark opacity-75 small">Bulan ini: <span class="fw-semibold">{{ stats.income_month | rupiah }}</span></div></div></div></div>
    <div class="col-md-4"><div class="card-custom bg-white d-flex flex-column justify-content-between p-4"><div class="d-flex justify-content-between mb-4"><span class="fs-5 text-muted fw-medium">Total Pengeluaran</span><i class="bi bi-arrow-up-right fs-4 text-muted opacity-50"></i></div><div><div class="title-huge text-dark mb-2">{{ stats.expense | rupiah }}</div><div class="text-muted small">Bulan ini: <span class="text-dark fw-semibold">{{ stats.expense_month | rupiah }}</span></div></div></div></div>
</div>

<div class="mb-4">
    <h6 class="fw-medium text-muted mb-3"><i class="bi bi-credit-card-2-front me-2"></i>Rincian Saldo Akun Kas</h6>
    <div class="d-flex gap-3 overflow-auto pb-2 custom-scrollbar">
        {% for acc_name, acc_bal in account_balances %}
        <div class="card-custom card-custom-hover bg-white flex-shrink-0 p-3" style="width: 200px; border-radius: 20px;"><div class="d-flex justify-content-between align-items-center mb-2"><span class="small text-muted fw-semibold">{{ acc_name }}</span><i class="bi bi-wallet2 text-muted opacity-50"></i></div><div class="fw-bold text-dark fs-5">{{ acc_bal | rupiah }}</div></div>
        {% endfor %}
    </div>
</div>

<div class="row g-4 mb-4">
    <div class="col-lg-4 col-md-6"><div class="card-custom card-custom-hover bg-white p-3 h-100 d-flex flex-column justify-content-between"><h6 class="fw-medium text-muted m-0 mb-2">Distribusi Pengeluaran</h6><div style="height: 230px; position: relative;"><canvas id="expenseChart"></canvas></div></div></div>
    <div class="col-lg-4 col-md-6"><div class="card-custom card-custom-hover bg-white p-3 h-100 d-flex flex-column justify-content-between clickable-card" onclick="window.location.href='/portfolios'" style="cursor: pointer;" title="Klik untuk mengelola portofolio investasi"><div class="d-flex justify-content-between align-items-center mb-2"><h6 class="fw-medium text-muted m-0">Alokasi Investasi</h6><span class="badge bg-light text-dark border small"><i class="bi bi-box-arrow-up-right"></i> Kelola</span></div><div style="height: 230px; position: relative;"><canvas id="investChart"></canvas></div></div></div>
    <div class="col-lg-4 col-md-12">
        <div class="card-custom card-custom-hover bg-white p-3 h-100 d-flex flex-column justify-content-between">
            <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-1">
                <h6 class="fw-medium m-0 small"><i class="bi bi-calendar3 me-1 text-muted"></i>Kalender Keuangan</h6>
                <form method="GET" action="/" class="d-flex gap-1 m-0">
                    <input type="hidden" name="trend_view" value="{{ trend_view }}"><input type="hidden" name="start_date" value="{{ start_date }}"><input type="hidden" name="end_date" value="{{ end_date }}"><input type="hidden" name="trend_month" value="{{ trend_month }}"><input type="hidden" name="trend_year" value="{{ trend_year }}">
                    <select name="month" class="form-select form-select-sm form-select-custom" style="padding: 0.2rem 1.4rem 0.2rem 0.5rem; font-size: 0.75rem;" onchange="this.form.submit()">{% for m_idx in range(1, 13) %}<option value="{{ m_idx }}" {% if sel_month == m_idx %}selected{% endif %}>{{ month_names[m_idx][:3] }}</option>{% endfor %}</select>
                    <select name="year" class="form-select form-select-sm form-select-custom" style="padding: 0.2rem 1.4rem 0.2rem 0.5rem; font-size: 0.75rem;" onchange="this.form.submit()">{% for y_idx in range(2023, 2030) %}<option value="{{ y_idx }}" {% if sel_year == y_idx %}selected{% endif %}>{{ y_idx }}</option>{% endfor %}</select>
                </form>
            </div>
            <div class="table-responsive flex-grow-1 d-flex flex-column justify-content-center">
                <table class="table table-bordered mb-0 text-center" style="table-layout: fixed; border-color: rgba(0,0,0,0.05); border-collapse: collapse; font-size: 0.7rem;">
                    <thead><tr class="text-muted"><th class="py-1 border-0">Sen</th><th class="py-1 border-0">Sel</th><th class="py-1 border-0">Rab</th><th class="py-1 border-0">Kam</th><th class="py-1 border-0">Jum</th><th class="py-1 border-0 text-primary">Sab</th><th class="py-1 border-0 text-danger">Min</th></tr></thead>
                    <tbody>
                        {% for week in calendar_grid %}
                        <tr>
                            {% for d in week %}
                            <td class="p-1 align-top calendar-cell {% if d == today_day %}bg-warning bg-opacity-25 fw-bold{% elif d == 0 %}bg-light bg-opacity-50{% endif %}" {% if d > 0 %}onclick="openDayDetail({{ d }}, '{{ d }} {{ month_names[sel_month] }} {{ sel_year }}', '{{ daily_summary[d].in | rupiah }}', '{{ daily_summary[d].out | rupiah }}')"{% endif %} style="height: 38px; border-color: rgba(0,0,0,0.06); border-radius: 6px; cursor: pointer; vertical-align: top;">
                                {% if d > 0 %}<div class="d-flex justify-content-between align-items-center px-1"><span class="{% if d == today_day %}text-dark fw-bold{% else %}text-muted{% endif %}">{{ d }}</span></div>
                                <div class="mt-1 px-1 d-flex flex-column gap-1">
                                    {% if daily_summary[d].in > 0 %}<div class="progress m-0" style="height: 3px; border-radius: 2px; background-color: rgba(16,185,129,0.15);"><div class="progress-bar bg-success" style="width: {{ daily_summary[d].in_pct }}%;"></div></div>{% endif %}
                                    {% if daily_summary[d].out > 0 %}<div class="progress m-0" style="height: 3px; border-radius: 2px; background-color: rgba(239,68,68,0.15);"><div class="progress-bar bg-danger" style="width: {{ daily_summary[d].out_pct }}%;"></div></div>{% endif %}
                                </div>{% endif %}
                            </td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <div class="d-flex justify-content-between align-items-center mt-2 text-muted" style="font-size: 0.68rem;"><span>* Klik tanggal untuk rincian</span><div class="d-flex gap-2"><span class="d-flex align-items-center gap-1"><span style="width: 7px; height: 7px; border-radius: 50%; background-color: #10B981; display: inline-block;"></span> Masuk</span><span class="d-flex align-items-center gap-1"><span style="width: 7px; height: 7px; border-radius: 50%; background-color: #EF4444; display: inline-block;"></span> Keluar</span></div></div>
        </div>
    </div>
</div>

<div class="row g-4 mb-4">
    <div class="col-12">
        <div class="card-custom card-custom-hover bg-white p-4">
            <div class="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
                <div><h5 class="fw-bold text-dark m-0"><i class="bi bi-cpu-fill me-2 text-warning" style="color: var(--accent-yellow) !important;"></i>Pusat Analitik Keuangan Anda</h5><span class="small text-muted">Integrasi real-time dari Transaksi, Investasi, Anggaran, Goals, dan Saldo Akun Bank</span></div>
            </div>
            <div class="row g-4 align-items-center">
                <div class="col-lg-7 border-end-lg">
                    <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
                        <h6 class="fw-medium text-muted small m-0">Tren Arus Kas & Investasi</h6>
                        <form method="GET" action="/" id="trendFilterForm" class="m-0 d-flex align-items-center gap-2 flex-wrap">
                            <input type="hidden" name="month" value="{{ sel_month }}"><input type="hidden" name="year" value="{{ sel_year }}">
                            <select name="trend_view" id="trendViewSelect" class="form-select form-select-sm form-select-custom fw-medium text-dark" style="padding: 0.25rem 2.0rem 0.25rem 0.7rem; font-size: 0.75rem; border-radius: 20px; cursor: pointer;" onchange="this.form.submit()">
                                <option value="day" {% if trend_view == 'day' %}selected{% endif %}>Per Hari</option><option value="month" {% if trend_view == 'month' %}selected{% endif %}>Per Bulan</option><option value="year" {% if trend_view == 'year' %}selected{% endif %}>Per Tahun</option>
                            </select>
                            <div id="inputDayRange" class="align-items-center gap-1 bg-light border px-3 py-1" style="border-radius: 20px; display: {% if trend_view == 'day' %}flex{% else %}none{% endif %};"><i class="bi bi-calendar-range text-muted small me-1"></i><input type="date" name="start_date" value="{{ start_date }}" class="border-0 bg-transparent small text-dark fw-medium" style="font-size: 0.75rem; outline: none; cursor: pointer;" onchange="this.form.submit()" title="Dari Tanggal"><span class="text-muted small px-1">s.d.</span><input type="date" name="end_date" value="{{ end_date }}" class="border-0 bg-transparent small text-dark fw-medium" style="font-size: 0.75rem; outline: none; cursor: pointer;" onchange="this.form.submit()" title="Sampai Tanggal"></div>
                            <div id="inputMonthSelect" class="align-items-center gap-1" style="display: {% if trend_view == 'month' %}flex{% else %}none{% endif %};"><select name="trend_month" class="form-select form-select-sm form-select-custom" style="padding: 0.25rem 1.6rem 0.25rem 0.6rem; font-size: 0.75rem; border-radius: 20px;" onchange="this.form.submit()">{% for m_idx in range(1, 13) %}<option value="{{ m_idx }}" {% if trend_month == m_idx %}selected{% endif %}>{{ month_names[m_idx] }}</option>{% endfor %}</select><select name="trend_year_m" class="form-select form-select-sm form-select-custom" style="padding: 0.25rem 1.6rem 0.25rem 0.6rem; font-size: 0.75rem; border-radius: 20px;" onchange="this.form.submit()">{% for y_idx in range(2023, 2030) %}<option value="{{ y_idx }}" {% if trend_year == y_idx %}selected{% endif %}>{{ y_idx }}</option>{% endfor %}</select></div>
                            <div id="inputYearSelect" class="align-items-center gap-1" style="display: {% if trend_view == 'year' %}flex{% else %}none{% endif %};"><select name="trend_year_y" class="form-select form-select-sm form-select-custom" style="padding: 0.25rem 1.6rem 0.25rem 0.6rem; font-size: 0.75rem; border-radius: 20px;" onchange="this.form.submit()">{% for y_idx in range(2023, 2030) %}<option value="{{ y_idx }}" {% if trend_year == y_idx %}selected{% endif %}>{{ y_idx }}</option>{% endfor %}</select></div>
                        </form>
                    </div>
                    <div style="height: 250px; position: relative;"><canvas id="trendChart"></canvas></div>
                </div>
                <div class="col-lg-5">
                    <div class="d-flex flex-column gap-3 px-lg-2">
                        <div class="p-3 rounded-4" style="background: var(--bg-inner);"><div class="d-flex justify-content-between align-items-center mb-1"><span class="small text-muted fw-semibold">Estimasi Net Worth</span><span class="badge bg-white text-dark border">Kas + Investasi</span></div><h4 class="fw-bold text-dark m-0">{{ net_worth | rupiah }}</h4></div>
                        <div><div class="d-flex justify-content-between align-items-center small mb-1"><span class="text-muted fw-medium"><i class="bi bi-pie-chart me-1"></i>Burn Rate Anggaran Bulanan</span><span class="fw-bold text-dark">{{ avg_budget_pct }}%</span></div><div class="progress" style="height: 8px; border-radius: 4px; background-color: rgba(0,0,0,0.05);"><div class="progress-bar {{ 'bg-danger' if avg_budget_pct > 100 else 'bg-warning' }}" style="width: {{ avg_budget_pct if avg_budget_pct <= 100 else 100 }}%;"></div></div></div>
                        <div><div class="d-flex justify-content-between align-items-center small mb-1"><span class="text-muted fw-medium"><i class="bi bi-graph-up-arrow me-1"></i>Savings & Invest Ratio</span><span class="fw-bold text-dark">{{ savings_ratio_pct }}%</span></div><div class="progress" style="height: 8px; border-radius: 4px; background-color: rgba(0,0,0,0.05);"><div class="progress-bar bg-dark" style="width: {{ savings_ratio_pct if savings_ratio_pct <= 100 else 100 }}%;"></div></div></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="dayDetailModal" tabindex="-1"><div class="modal-dialog modal-dialog-centered"><div class="modal-content p-3 border-0" style="border-radius: 30px;"><div class="modal-header border-0 pb-1"><h5 class="modal-title fw-bold text-dark" id="modalDayTitle">Rincian Tanggal</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><div class="row g-2 mb-3"><div class="col-6"><div class="p-2 border rounded-4 bg-white text-center"><span class="small text-muted d-block">Pemasukan</span><span class="fw-bold text-success" id="modalDayIn">Rp0</span></div></div><div class="col-6"><div class="p-2 border rounded-4 bg-white text-center"><span class="small text-muted d-block">Pengeluaran</span><span class="fw-bold text-danger" id="modalDayOut">Rp0</span></div></div></div><h6 class="fw-medium small text-muted mb-2">Transaksi pada hari ini:</h6><div id="modalDayTxList" class="list-group list-group-flush border rounded-4 overflow-hidden"></div></div></div></div></div>

<div class="row g-4">
    <div class="col-12">
        <div class="card-custom bg-transparent shadow-none p-0">
            <div class="d-flex justify-content-between align-items-center mb-3 px-2">
                <h5 class="fw-medium m-0">Aktivitas Terakhir</h5>
                <a href="/transactions" class="small text-muted text-decoration-none">Lihat Semua &rarr;</a>
            </div>
            <div class="table-responsive">
                <table class="table-modern">
                    <tbody>
                        {% for t in recent_tx %}
                        <tr>
                            <td style="width: 60px;"><div style="background: #E4E5E7; color: #303030; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-weight: 600;">{{ (t.cat_name or t.asset_type or t.port_name or 'NA')[:2] | upper }}</div></td>
                            <td><div class="fw-medium text-dark">{{ t.description }}</div><div class="small text-muted">{% if t.portfolio_id or t.goal_id %}<span class="badge border text-dark fw-medium bg-white" style="border-radius: 20px; padding: 0.25em 0.6em; font-size: 0.75rem;"><span style="display: inline-block; width: 5px; height: 5px; border-radius: 50%; background-color: #303030; margin-right: 4px; vertical-align: middle;"></span>{{ 'Investasi' if t.portfolio_id else 'Goal' }}</span> {{ t.asset_type or 'Aset' }} ({{ t.port_name or 'Tabungan' }}){% else %}Kategori: {{ t.cat_name or 'Lainnya' }}{% endif %}</div></td>
                            <td><span class="badge bg-light text-dark border">{{ t.account }}</span></td>
                            <td class="text-muted">{{ t.tgl }}</td>
                            <td class="text-end"><span class="badge border text-dark fw-medium" style="background: transparent; border-radius: 20px; padding: 0.45em 0.85em;"><span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background-color: {{ '#303030' if t.type == 'Pengeluaran' else '#10B981' }}; margin-right: 6px; vertical-align: middle;"></span><span class="fw-semibold {{ 'text-danger' if t.type == 'Pengeluaran' else 'text-success' }}">{{ '+' if t.type == 'Pemasukan' else '-' }}{{ t.nominal | rupiah }}</span></span></td>
                        </tr>
                        {% else %}
                        <tr><td colspan="5" class="text-center py-4 bg-white rounded-4 text-muted">Belum ada aktivitas tercatat.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<script>
    const dailyTxData = {{ daily_tx_json | safe }};
    function openDayDetail(dayNum, dateStr, inStr, outStr) {
        document.getElementById('modalDayTitle').innerText = 'Rincian ' + dateStr;
        document.getElementById('modalDayIn').innerText = inStr;
        document.getElementById('modalDayOut').innerText = outStr;
        const listContainer = document.getElementById('modalDayTxList');
        listContainer.innerHTML = '';
        const txList = dailyTxData[String(dayNum)] || [];
        if (txList.length === 0) { listContainer.innerHTML = '<div class="list-group-item text-center py-4 text-muted small bg-light">Tidak ada transaksi di hari ini.</div>'; }
        else {
            txList.forEach(tx => {
                const isOut = tx.type === 'Pengeluaran';
                const colorClass = isOut ? 'text-danger' : 'text-success';
                const sign = isOut ? '-' : '+';
                listContainer.innerHTML += `<div class="list-group-item d-flex justify-content-between align-items-center py-2 px-3 border-bottom"><div><div class="fw-medium text-dark small">${tx.desc}</div><span class="badge bg-light text-dark border" style="font-size:0.65rem;">${tx.cat}</span></div><span class="fw-bold small ${colorClass}">${sign}${tx.nom}</span></div>`;
            });
        }
        new bootstrap.Modal(document.getElementById('dayDetailModal')).show();
    }

    const chartOptions = { responsive: true, maintainAspectRatio: false, cutout: '60%', plugins: { legend: { display: true, position: 'bottom', labels: { boxWidth: 10, padding: 8, font: { size: 11, family: 'Outfit' } } }, tooltip: { backgroundColor: '#303030', titleFont: { family: 'Outfit', size: 12 }, bodyFont: { family: 'Outfit', size: 11 }, padding: 10, cornerRadius: 10 } } };
    const expLabels = {{ chart_labels | safe }}; const expBg = expLabels[0] === 'Belum Ada Pengeluaran' ? ['#E4E5E7'] : ['#FFD861', '#303030', '#10B981', '#6366F1', '#F59E0B', '#EC4899', '#3B82F6'];
    new Chart(document.getElementById('expenseChart').getContext('2d'), { type: 'doughnut', data: { labels: expLabels, datasets: [{ data: {{ chart_values | safe }}, backgroundColor: expBg, borderWidth: 0 }] }, options: chartOptions });
    const invLabels = {{ inv_labels | safe }}; const invBg = invLabels[0] === 'Belum Ada Aset' ? ['#E4E5E7'] : ['#FFD861', '#303030', '#10B981', '#6366F1', '#F59E0B'];
    new Chart(document.getElementById('investChart').getContext('2d'), { type: 'doughnut', data: { labels: invLabels, datasets: [{ data: {{ inv_values | safe }}, backgroundColor: invBg, borderWidth: 0 }] }, options: chartOptions });

    new Chart(document.getElementById('trendChart').getContext('2d'), {
        type: 'line',
        data: { labels: {{ trend_labels | safe }}, datasets: [
                { label: 'Pemasukan', data: {{ trend_income | safe }}, borderColor: '#10B981', backgroundColor: 'rgba(16, 185, 129, 0.12)', borderWidth: 3, tension: 0.35, pointBackgroundColor: '#10B981', pointBorderColor: '#ffffff', pointBorderWidth: 2, pointRadius: function(context) { return context.raw > 0 ? 4 : 0; }, pointHoverRadius: 6, fill: true },
                { label: 'Pengeluaran', data: {{ trend_expense | safe }}, borderColor: '#EF4444', backgroundColor: 'rgba(239, 68, 68, 0.08)', borderWidth: 3, tension: 0.35, pointBackgroundColor: '#EF4444', pointBorderColor: '#ffffff', pointBorderWidth: 2, pointRadius: function(context) { return context.raw > 0 ? 4 : 0; }, pointHoverRadius: 6, fill: true },
                { label: 'Beli Investasi & Goal', data: {{ trend_invest | safe }}, borderColor: '#F59E0B', backgroundColor: 'rgba(245, 158, 11, 0.08)', borderWidth: 3, tension: 0.35, pointBackgroundColor: '#F59E0B', pointBorderColor: '#ffffff', pointBorderWidth: 2, pointRadius: function(context) { return context.raw > 0 ? 4 : 0; }, pointHoverRadius: 6, fill: true }
        ]},
        options: { responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false }, plugins: { legend: { position: 'top', labels: { boxWidth: 10, usePointStyle: true, font: { size: 11, family: 'Outfit' } } }, tooltip: { backgroundColor: '#303030', titleFont: { family: 'Outfit', size: 13 }, bodyFont: { family: 'Outfit', size: 12 }, padding: 10, cornerRadius: 10 } }, scales: { x: { grid: { display: false }, ticks: { font: { family: 'Outfit', size: 10 }, maxTicksLimit: 7, maxRotation: 0, autoSkip: true } }, y: { border: { display: false }, grid: { color: 'rgba(0,0,0,0.05)' }, min: 0, suggestedMax: 1000000, ticks: { font: { family: 'Outfit', size: 10 }, callback: function(val) { return 'Rp' + (val >= 1000000 ? (val/1000000) + 'jt' : val); } } } } }
    });
    const trendViewSelect = document.getElementById('trendViewSelect');
    if (trendViewSelect) { trendViewSelect.addEventListener('change', function() { document.getElementById('inputDayRange').style.display = (this.value === 'day') ? 'flex' : 'none'; document.getElementById('inputMonthSelect').style.display = (this.value === 'month') ? 'flex' : 'none'; document.getElementById('inputYearSelect').style.display = (this.value === 'year') ? 'flex' : 'none'; }); }
</script>
"""

HTML_TRANSACTIONS = """
<div class="mb-4"><h1 class="fw-light mb-0 title-huge text-dark">Daftar Transaksi</h1></div>
<div class="bg-white p-3 mb-4 shadow-sm" style="border-radius: 20px;"><form method="GET" action="/transactions" class="row g-2 align-items-end"><div class="col-md-3"><label class="form-label small text-muted mb-1">Pencarian</label><input type="text" name="search" class="form-control form-control-sm form-control-custom" placeholder="Ketik deskripsi..." value="{{ filters.search }}"></div><div class="col-md-2"><label class="form-label small text-muted mb-1">Periode</label><input type="month" name="period" class="form-control form-control-sm form-control-custom" value="{{ filters.period }}"></div><div class="col-md-2"><label class="form-label small text-muted mb-1">Akun</label><select name="account" class="form-select form-select-sm form-select-custom"><option value="">Semua Akun</option>{% for a in accounts %}<option value="{{ a }}" {% if filters.account == a %}selected{% endif %}>{{ a }}</option>{% endfor %}</select></div><div class="col-md-2"><label class="form-label small text-muted mb-1">Kategori</label><select name="category_id" class="form-select form-select-sm form-select-custom"><option value="">Semua</option>{% for c in categories %}<option value="{{ c.id }}" {% if filters.category_id == c.id|string %}selected{% endif %}>{{ c.name }}</option>{% endfor %}</select></div><div class="col-md-2"><label class="form-label small text-muted mb-1">Jenis</label><select name="type" class="form-select form-select-sm form-select-custom"><option value="">Semua</option><option value="Pemasukan" {% if filters.type == 'Pemasukan' %}selected{% endif %}>Pemasukan</option><option value="Pengeluaran" {% if filters.type == 'Pengeluaran' %}selected{% endif %}>Pengeluaran</option></select></div><div class="col-md-1"><button type="submit" class="btn btn-dark-custom w-100" style="border-radius: 20px; padding: 0.35rem;"><i class="bi bi-funnel"></i></button></div></form></div>
<div class="d-flex justify-content-end align-items-center mb-3"><div class="d-flex gap-2">
    <button type="button" id="btnEditSelected" class="btn btn-custom bg-white border text-dark" style="padding: 0.4rem 1rem; font-size: 0.85rem;">
        <i class="bi bi-pencil-square me-1"></i> Edit Terpilih</button>
    <button type="button" id="btnDeleteSelected" class="btn btn-custom bg-white border text-danger" style="padding: 0.4rem 1rem; font-size: 0.85rem;">
        <i class="bi bi-trash3 me-1"></i> Hapus Terpilih</button>
    <button type="button" class="btn btn-custom bg-white border text-dark" data-bs-toggle="modal" data-bs-target="#transferModal" style="padding: 0.4rem 1rem; font-size: 0.85rem;">
        <i class="bi bi-arrow-left-right me-1"></i> Transfer</button>
    <button type="button" class="btn btn-custom btn-dark-custom" data-bs-toggle="modal" data-bs-target="#addModal" style="padding: 0.4rem 1rem; font-size: 0.85rem;">
        <i class="bi bi-plus-lg me-1"></i> Catat Baru</button>
    <button type="button" class="btn btn-custom bg-white border text-dark"data-bs-toggle="modal" data-bs-target="#accountModal"style="padding: 0.4rem 1rem; font-size: 0.85rem;">
        <i class="bi bi-wallet2 me-1"></i> Kelola Akun</button>
</div></div>
<form id="bulkActionForm" method="POST" action="/transactions/bulk_action"><div class="table-responsive">
    <table class="table-modern" id="txTable">
        <thead>
            <tr>
                <th style="width: 50px; text-align: center;"><input class="form-check-input" type="checkbox" id="selectAllCheckbox" style="border-radius: 4px; border-color: rgba(0,0,0,0.2); cursor: pointer;"></th>
                <th class="sortable" onclick="sortTable('txTable', 1)">Kode <i class="bi bi-chevron-expand sort-icon opacity-50 ms-1"></i></th>
                <th class="sortable" onclick="sortTable('txTable', 2)">Keterangan & Kategori <i class="bi bi-chevron-expand sort-icon opacity-50 ms-1"></i></th>
                <th class="sortable" onclick="sortTable('txTable', 3)">Sumber Akun <i class="bi bi-chevron-expand sort-icon opacity-50 ms-1"></i></th>
                <th class="sortable" onclick="sortTable('txTable', 4)">Tanggal <i class="bi bi-chevron-expand sort-icon opacity-50 ms-1"></i></th>
                <th class="sortable" onclick="sortTable('txTable', 5)">Jenis <i class="bi bi-chevron-expand sort-icon opacity-50 ms-1"></i></th>
                <th class="sortable text-end" onclick="sortTable('txTable', 6)">Nominal <i class="bi bi-chevron-expand sort-icon opacity-50 ms-1"></i></th>
            </tr>
        </thead>
        <tbody>
            {% for t in transactions %}
            <tr>
                <td class="text-center"><input class="form-check-input tx-checkbox" type="checkbox" name="tx_ids" value="{{ t.id }}" data-tgl="{{ t.tgl }}" data-type="{{ t.type }}" data-cat="{{ t.category_id }}" data-acc="{{ t.account }}" data-nom="{{ t.nominal | int }}" data-desc="{{ t.description }}" style="border-radius: 4px; border-color: rgba(0,0,0,0.2); cursor: pointer;"></td>
                <td><span class="text-muted small fw-semibold" style="letter-spacing: 0.5px;">{{ "TRX-%04d" % t.id }}</span></td>
                <td><div class="d-flex align-items-center gap-3"><div style="background: #E4E5E7; color: #303030; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-weight: 600;">{{ t.cat_name[:2] | upper if t.cat_name else 'NA' }}</div><div><div class="fw-medium text-dark">{{ t.description }}</div><div class="small text-muted">Kategori: {{ t.cat_name }}</div></div></div></td>
                <td><span class="badge bg-light text-dark border">{{ t.account }}</span></td>
                <td class="text-muted">{{ t.tgl }}</td>
                <td><span class="badge border text-dark fw-medium" style="background: transparent; border-radius: 20px; padding: 0.45em 0.85em;"><span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background-color: {{ '#303030' if t.type == 'Pengeluaran' else '#10B981' }}; margin-right: 6px; vertical-align: middle;"></span>{{ t.type }}</span></td>
                <td class="fw-semibold text-dark fs-6 text-end">{{ t.nominal | rupiah }}</td>
            </tr>
            {% else %}
            <tr><td colspan="7" class="text-center py-5 bg-white rounded-4 text-muted">Tidak ada transaksi.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div></form>
<div class="modal fade" id="deleteConfirmModal" tabindex="-1"><div class="modal-dialog modal-dialog-centered"><div class="modal-content p-3 border-0" style="border-radius: 30px;"><div class="modal-body text-center"><i class="bi bi-trash3 text-danger" style="font-size: 3rem;"></i><h4 class="mt-3 text-dark fw-semibold">Hapus Transaksi?</h4><p class="text-muted" id="deleteModalText">Anda yakin ingin menghapus transaksi yang dipilih?</p><div class="d-flex gap-2 mt-4 justify-content-center"><button type="button" class="btn btn-custom bg-light text-dark border px-4" data-bs-dismiss="modal">Batal</button><button type="button" class="btn btn-custom btn-danger px-4" id="confirmDeleteBtn">Ya, Hapus</button></div></div></div></div></div>
<div class="modal fade" id="addModal"><div class="modal-dialog modal-dialog-centered"><div class="modal-content"><form action="/transactions/add" method="POST"><div class="modal-header border-0"><h5 class="modal-title">Transaksi Baru</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><input type="date" name="tgl" class="form-control form-control-custom mb-3" required value="{{ today }}"><select name="type" id="addType" class="form-select form-select-custom mb-3" required><option value="Pengeluaran">Pengeluaran</option><option value="Pemasukan">Pemasukan</option></select><select name="category_id" id="addCat" class="form-select form-select-custom mb-3" required>{% for c in categories %}<option value="{{ c.id }}" data-type="{{ c.type }}">{{ c.name }}</option>{% endfor %}</select><select name="account" class="form-select form-select-custom mb-3" required>{% for acc in accounts %}<option value="{{ acc }}">{{ acc }}</option>{% endfor %}</select><input type="number" step="any" name="nominal" class="form-control form-control-custom mb-3" placeholder="Nominal" required><input type="text" name="description" class="form-control form-control-custom mb-3" placeholder="Deskripsi" required></div><div class="modal-footer border-0"><button type="submit" class="btn btn-yellow w-100 btn-custom">Simpan</button></div></form></div></div></div>
<div class="modal fade" id="editModal"><div class="modal-dialog modal-dialog-centered"><div class="modal-content"><form action="/transactions/edit" method="POST"><input type="hidden" name="tx_id" id="edit_tx_id"><div class="modal-header border-0"><h5 class="modal-title">Edit Transaksi</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><div class="alert bg-light border-0 small mb-3 text-muted">Periksa kembali data transaksi sebelum menyimpan.</div><input type="date" name="tgl" id="edit_tgl" class="form-control form-control-custom mb-3" required><select name="type" id="edit_type" class="form-select form-select-custom mb-3" required><option value="Pengeluaran">Pengeluaran</option><option value="Pemasukan">Pemasukan</option></select><select name="category_id" id="edit_cat" class="form-select form-select-custom mb-3" required>{% for c in categories %}<option value="{{ c.id }}" data-type="{{ c.type }}">{{ c.name }}</option>{% endfor %}</select><select name="account" id="edit_acc" class="form-select form-select-custom mb-3" required>{% for acc in accounts %}<option value="{{ acc }}">{{ acc }}</option>{% endfor %}</select><input type="number" step="any" name="nominal" id="edit_nom" class="form-control form-control-custom mb-3" required><input type="text" name="description" id="edit_desc" class="form-control form-control-custom mb-3" required></div><div class="modal-footer border-0"><button type="submit" class="btn btn-yellow w-100 btn-custom">Simpan Perubahan</button></div></form></div></div></div>
<div class="modal fade" id="transferModal"><div class="modal-dialog modal-dialog-centered"><div class="modal-content"><form action="/transactions/transfer" method="POST"><div class="modal-header border-0"><h5 class="modal-title">Transfer Dana</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><div class="alert bg-light border-0 small mb-3">Sistem mencatat Pengeluaran dari sumber dan Pemasukan ke tujuan.</div><input type="date" name="tgl" class="form-control form-control-custom mb-3" required value="{{ today }}"><select name="from_account" class="form-select form-select-custom mb-3" required><option value="">Dari Akun...</option>{% for acc in accounts %}<option value="{{ acc }}">{{ acc }}</option>{% endfor %}</select><select name="to_account" class="form-select form-select-custom mb-3" required><option value="">Ke Akun...</option>{% for acc in accounts %}<option value="{{ acc }}">{{ acc }}</option>{% endfor %}</select><input type="number" step="any" name="nominal" class="form-control form-control-custom mb-3" placeholder="Nominal" required><input type="text" name="description" class="form-control form-control-custom mb-3" placeholder="Catatan Transfer"></div><div class="modal-footer border-0"><button type="submit" class="btn btn-dark-custom w-100 btn-custom">Proses Transfer</button></div></form></div></div></div>
<div class="modal fade" id="accountModal"><div class="modal-dialog modal-dialog-centered"><div class="modal-content"><div class="modal-header border-0"><h5 class="modal-title">Kelola Akun / Dompet</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><form action="/accounts/add" method="POST" class="mb-4 d-flex gap-2"><input type="text" name="name" class="form-control form-control-custom" placeholder="Nama Akun baru..." required><button type="submit" class="btn btn-dark-custom btn-custom"><i class="bi bi-plus-lg"></i></button></form><div class="list-group">{% for a in account_objects %}<div class="list-group-item border-0 d-flex justify-content-between align-items-center px-0 py-2"><span class="fw-medium text-dark"><i class="bi bi-wallet2 me-2 text-muted"></i> {{ a.name }}</span><form action="/accounts/delete/{{ a.id }}" method="POST" class="m-0"><button type="submit" class="btn btn-sm text-danger shadow-none p-0"><i class="bi bi-trash3"></i></button></form></div>{% endfor %}</div></div></div></div></div>
<script>
    document.addEventListener('DOMContentLoaded', () => {
        const filterCat = (typeId, catId) => { const typeSel = document.getElementById(typeId), catSel = document.getElementById(catId); if(typeSel && catSel) { const opts = Array.from(catSel.options); const update = () => { catSel.innerHTML = ''; let first = true; opts.forEach(o => { if(o.dataset.type === typeSel.value) { catSel.appendChild(o); if(first){o.selected=true;first=false;} } }); }; update(); typeSel.addEventListener('change', update); } };
        filterCat('addType', 'addCat'); filterCat('edit_type', 'edit_cat');
        document.getElementById('selectAllCheckbox')?.addEventListener('change', (e) => { document.querySelectorAll('.tx-checkbox').forEach(cb => cb.checked = e.target.checked); });
        document.getElementById('btnEditSelected')?.addEventListener('click', () => { const chks = document.querySelectorAll('.tx-checkbox:checked'); if(chks.length !== 1) return showToast('Pilih TEPAT 1 transaksi untuk diedit!', 'warning'); const chk = chks[0]; document.getElementById('edit_tx_id').value = chk.value; document.getElementById('edit_tgl').value = chk.dataset.tgl; document.getElementById('edit_type').value = chk.dataset.type; document.getElementById('edit_type').dispatchEvent(new Event('change')); document.getElementById('edit_cat').value = chk.dataset.cat || ''; document.getElementById('edit_acc').value = chk.dataset.acc; document.getElementById('edit_nom').value = chk.dataset.nom; document.getElementById('edit_desc').value = chk.dataset.desc; new bootstrap.Modal(document.getElementById('editModal')).show(); });
        document.getElementById('btnDeleteSelected')?.addEventListener('click', () => { const chks = document.querySelectorAll('.tx-checkbox:checked'); if(chks.length === 0) { showToast('Pilih minimal 1 transaksi untuk dihapus.', 'danger'); return; } document.getElementById('deleteModalText').innerText = `Anda yakin ingin menghapus ${chks.length} transaksi yang dipilih? Data yang dihapus tidak dapat dikembalikan.`; new bootstrap.Modal(document.getElementById('deleteConfirmModal')).show(); });
        document.getElementById('confirmDeleteBtn')?.addEventListener('click', () => { const form = document.getElementById('bulkActionForm'); const actionInput = document.createElement('input'); actionInput.type = 'hidden'; actionInput.name = 'action'; actionInput.value = 'delete'; form.appendChild(actionInput); form.submit(); });
    });
</script>
"""

HTML_PORTFOLIOS = """
<div class="mb-4"><h1 class="fw-light mb-0 title-huge text-dark">Investasi & Portofolio</h1></div>
<div class="row g-4 mb-5">
    <div class="col-md-4 d-flex flex-column gap-3"><div class="card-custom p-4" style="background: var(--accent-yellow);"><span class="fs-6 text-dark fw-medium opacity-75">Total Modal Diinvestasikan</span><div class="title-huge text-dark mt-1">{{ total_assets | rupiah }}</div></div><div class="card-custom bg-white p-4 flex-grow-1"><div class="d-flex justify-content-between align-items-center mb-3"><h6 class="fw-bold m-0"><i class="bi bi-bullseye text-danger me-1"></i> Target Tabungan (Goals)</h6><button class="btn btn-sm btn-outline-dark rounded-pill" data-bs-toggle="modal" data-bs-target="#addGoalModal">+ Target</button></div><div class="d-flex flex-column gap-3">{% for g in goals %}<div class="p-3 border rounded-4 position-relative" style="background: var(--bg-inner);"><form action="/goals/delete/{{ g.id }}" method="POST" class="position-absolute top-0 end-0 m-2"><button type="submit" class="btn btn-sm text-danger shadow-none p-0"><i class="bi bi-trash3"></i></button></form><div class="d-flex justify-content-between align-items-start mb-1"><span class="fw-bold text-dark">{{ g.name }}</span></div><div class="d-flex justify-content-between align-items-end mb-1"><span class="fs-6 fw-bold text-success">{{ g.current_amount | rupiah }}</span><span class="text-muted" style="font-size: 0.65rem;">dari {{ g.target_amount | rupiah }}</span></div>{% set progress = (g.current_amount / g.target_amount * 100) | int if g.target_amount > 0 else 0 %}<div class="progress" style="height: 6px; border-radius: 3px;"><div class="progress-bar {{ 'bg-success' if progress >= 100 else 'bg-dark' }}" style="width: {{ progress if progress <= 100 else 100 }}%;"></div></div></div>{% else %}<div class="text-center py-4 text-muted small border rounded-4 border-dashed">Belum ada target tabungan aktif.</div>{% endfor %}</div></div></div>
    <div class="col-md-8"><div class="card-custom bg-white shadow-none h-100 p-4"><h5 class="fw-medium mb-4">Aset Aktif Dimiliki (Holdings)</h5><div class="row g-3">{% for h in active_holdings %}<div class="col-md-6"><div class="border rounded-4 p-3 d-flex justify-content-between align-items-center" style="background: var(--bg-inner);"><div><span class="badge bg-white text-dark border mb-2">{{ h.port_name }}</span><h5 class="fw-bold m-0 text-dark">{{ h.asset_name }}</h5><span class="text-muted small">{{ h.asset_type }}</span></div><div class="text-end"><h5 class="fw-bold m-0 text-dark">{{ h.modal | rupiah }}</h5><span class="text-muted small fw-medium">{{ h.qty | qty(h.asset_type) }}</span></div></div></div>{% else %}<div class="col-12 text-center py-5 text-muted">Belum ada aset investasi yang tercatat.<br>Klik tombol <b>Beli/Jual Aset</b> di bawah untuk memulai.</div>{% endfor %}</div></div></div>
</div>

<h5 class="fw-medium mb-3">Riwayat Transaksi Aset & Goals</h5>
<div class="bg-white p-3 mb-4 shadow-sm" style="border-radius: 20px;"><form method="GET" action="/portfolios" class="row g-2 align-items-end"><div class="col-md-3"><label class="form-label small text-muted mb-1">Pencarian Aset/Tujuan</label><input type="text" name="search" class="form-control form-control-sm form-control-custom" placeholder="Ketik nama..." value="{{ filters.search }}"></div><div class="col-md-2"><label class="form-label small text-muted mb-1">Periode</label><input type="month" name="period" class="form-control form-control-sm form-control-custom" value="{{ filters.period }}"></div><div class="col-md-2"><label class="form-label small text-muted mb-1">Akun</label><select name="account" class="form-select form-select-sm form-select-custom"><option value="">Semua Akun</option>{% for a in accounts %}<option value="{{ a }}" {% if filters.account == a %}selected{% endif %}>{{ a }}</option>{% endfor %}</select></div><div class="col-md-2"><label class="form-label small text-muted mb-1">Platform</label><select name="platform" class="form-select form-select-sm form-select-custom"><option value="">Semua</option>{% for p in portfolios %}<option value="{{ p.id }}" {% if filters.platform == p.id|string %}selected{% endif %}>{{ p.name }}</option>{% endfor %}</select></div><div class="col-md-2"><label class="form-label small text-muted mb-1">Jenis Aksi</label><select name="type" class="form-select form-select-sm form-select-custom"><option value="">Semua</option><option value="Pengeluaran" {% if filters.type == 'Pengeluaran' %}selected{% endif %}>Beli</option><option value="Pemasukan" {% if filters.type == 'Pemasukan' %}selected{% endif %}>Jual</option></select></div><div class="col-md-1"><button type="submit" class="btn btn-dark-custom w-100" style="border-radius: 20px; padding: 0.35rem;"><i class="bi bi-funnel"></i></button></div></form></div>
<div class="d-flex justify-content-end align-items-center mb-3"><div class="d-flex gap-2"><button type="button" id="btnEditInvSelected" class="btn btn-custom bg-white border text-dark" style="padding: 0.4rem 1rem; font-size: 0.85rem;"><i class="bi bi-pencil-square me-1"></i> Edit Terpilih</button><button type="button" id="btnDeleteInvSelected" class="btn btn-custom bg-white border text-danger" style="padding: 0.4rem 1rem; font-size: 0.85rem;"><i class="bi bi-trash3 me-1"></i> Hapus Terpilih</button><button type="button" class="btn btn-custom bg-white border text-dark" data-bs-toggle="modal" data-bs-target="#platformModal" style="padding: 0.4rem 1rem; font-size: 0.85rem;"><i class="bi bi-grid me-1"></i> Kelola Platform</button><button type="button" class="btn btn-custom btn-dark-custom" data-bs-toggle="modal" data-bs-target="#addInvestModal" style="padding: 0.4rem 1rem; font-size: 0.85rem;"><i class="bi bi-plus-lg me-1"></i> Beli/Jual Aset</button></div></div>
<form id="bulkActionFormInv" method="POST" action="/portfolios/bulk_action"><div class="table-responsive">
    <table class="table-modern" id="invTable">
        <thead>
            <tr>
                <th style="width: 50px; text-align: center;"><input class="form-check-input" type="checkbox" id="selectAllCheckboxInv" style="border-radius: 4px; border-color: rgba(0,0,0,0.2); cursor: pointer;"></th>
                <th class="sortable" onclick="sortTable('invTable', 1)">Tanggal <i class="bi bi-chevron-expand sort-icon opacity-50 ms-1"></i></th>
                <th class="sortable" onclick="sortTable('invTable', 2)">Platform / Tujuan <i class="bi bi-chevron-expand sort-icon opacity-50 ms-1"></i></th>
                <th class="sortable" onclick="sortTable('invTable', 3)">Nama Aset <i class="bi bi-chevron-expand sort-icon opacity-50 ms-1"></i></th>
                <th class="sortable" onclick="sortTable('invTable', 4)">Kuantitas <i class="bi bi-chevron-expand sort-icon opacity-50 ms-1"></i></th>
                <th class="sortable" onclick="sortTable('invTable', 5)">Aksi <i class="bi bi-chevron-expand sort-icon opacity-50 ms-1"></i></th>
                <th class="sortable text-end" onclick="sortTable('invTable', 6)">Total (Rp) <i class="bi bi-chevron-expand sort-icon opacity-50 ms-1"></i></th>
            </tr>
        </thead>
        <tbody>
            {% for t in inv_tx %}
            <tr>
                <td class="text-center"><input class="form-check-input inv-checkbox" type="checkbox" name="tx_ids" value="{{ t.id }}" data-tgl="{{ t.tgl }}" data-type="{{ t.type }}" data-pid="{{ t.portfolio_id or '' }}" data-gid="{{ t.goal_id or '' }}" data-atype="{{ t.asset_type or '' }}" data-aname="{{ t.asset_name or '' }}" data-qty="{{ t.quantity or '' }}" data-nom="{{ t.nominal | int }}" data-acc="{{ t.account }}" style="border-radius: 4px; border-color: rgba(0,0,0,0.2); cursor: pointer;"></td>
                <td class="text-dark fw-medium">{{ t.tgl }}</td>
                <td><span class="badge bg-light text-dark border px-3 py-2">{{ t.port_name or 'Goal (Tabungan)' }}</span></td>
                <td><div class="fw-bold text-dark">{{ t.asset_name or t.goal_name or t.description }}</div><div class="small text-muted">{{ t.asset_type or 'Goal Tracking' }}</div></td>
                <td class="text-muted fw-medium">{{ t.quantity | qty(t.asset_type) if t.asset_type else '-' }}</td>
                <td><span class="badge border text-dark fw-medium bg-white" style="border-radius: 20px; padding: 0.45em 0.85em;"><span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background-color: {{ '#303030' if t.type == 'Pengeluaran' else '#10B981' }}; margin-right: 6px; vertical-align: middle;"></span>{{ 'Beli' if t.type == 'Pengeluaran' else 'Jual' }}</span></td>
                <td class="fw-semibold text-dark fs-6 text-end">{{ t.nominal | rupiah }}</td>
            </tr>
            {% else %}
            <tr><td colspan="7" class="text-center py-5 bg-white rounded-4 text-muted">Belum ada riwayat investasi atau tabungan pada filter ini.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div></form>

<div class="modal fade" id="deleteConfirmModalInv" tabindex="-1"><div class="modal-dialog modal-dialog-centered"><div class="modal-content p-3 border-0" style="border-radius: 30px;"><div class="modal-body text-center"><i class="bi bi-trash3 text-danger" style="font-size: 3rem;"></i><h4 class="mt-3 text-dark fw-semibold">Hapus Riwayat Aset?</h4><p class="text-muted" id="deleteModalTextInv">Anda yakin ingin menghapus transaksi yang dipilih?</p><div class="d-flex gap-2 mt-4 justify-content-center"><button type="button" class="btn btn-custom bg-light text-dark border px-4" data-bs-dismiss="modal">Batal</button><button type="button" class="btn btn-custom btn-danger px-4" id="confirmDeleteBtnInv">Ya, Hapus</button></div></div></div></div></div>
<div class="modal fade" id="addInvestModal"><div class="modal-dialog modal-dialog-centered"><div class="modal-content"><form action="/portfolios/transaction" method="POST"><div class="modal-header border-0"><h5 class="modal-title">Beli/Jual Aset & Nabung</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><input type="date" name="tgl" class="form-control form-control-custom mb-3" required value="{{ today }}"><div class="row g-2 mb-3"><div class="col-6"><select name="type" class="form-select form-select-custom" required><option value="Pengeluaran">Beli</option><option value="Pemasukan">Jual</option></select></div><div class="col-6"><select name="portfolio_id" class="form-select form-select-custom"><option value="">-- Platform --</option>{% for p in portfolios %}<option value="{{ p.id }}">{{ p.name }}</option>{% endfor %}</select></div></div><div class="alert bg-light border border-dashed rounded-4 p-3 mb-3"><label class="form-label small fw-bold text-dark mb-2">Tautkan ke Target Tabungan (Opsional)</label><select name="goal_id" class="form-select form-select-sm form-select-custom border-0 shadow-sm" style="border-radius: 15px;"><option value="">-- Tidak ditautkan ke Goal --</option>{% for g in goals %}<option value="{{ g.id }}">Goal: {{ g.name }} (Sisa: {{ (g.target_amount - g.current_amount) | rupiah }})</option>{% endfor %}</select></div><select name="asset_type" id="assetType" class="form-select form-select-custom mb-3"><option value="">Pilih Jenis Investasi...</option><option value="Saham">Saham</option><option value="Reksa Dana">Reksa Dana</option><option value="Emas">Emas</option><option value="Kripto">Kripto</option><option value="Lainnya">Lainnya / Kas Simpanan</option></select><input type="text" name="asset_name" class="form-control form-control-custom mb-3" placeholder="Nama Aset / Judul Simpanan"><input type="number" step="any" name="quantity" id="qtyInput" class="form-control form-control-custom mb-3" placeholder="Kuantitas (Isi 1 jika berupa Kas)"><div class="row g-2 mb-3"><div class="col-6"><input type="number" step="any" name="nominal" class="form-control form-control-custom" placeholder="Total Nominal (Rp)" required></div><div class="col-6"><select name="account" class="form-select form-select-custom" required><option value="">Pilih Akun Bank...</option>{% for acc in accounts %}<option value="{{ acc }}">{{ acc }}</option>{% endfor %}</select></div></div></div><div class="modal-footer border-0"><button type="submit" class="btn btn-yellow w-100 btn-custom">Simpan Transaksi</button></div></form></div></div></div>
<div class="modal fade" id="editInvestModal"><div class="modal-dialog modal-dialog-centered"><div class="modal-content"><form action="/portfolios/edit" method="POST"><input type="hidden" name="tx_id" id="edit_inv_tx_id"><div class="modal-header border-0"><h5 class="modal-title">Edit Riwayat Aset & Goal</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><div class="alert bg-light border-0 small mb-3 text-muted">Perubahan nilai nominal akan diupdate ke saldo Goal secara otomatis.</div><input type="date" name="tgl" id="edit_inv_tgl" class="form-control form-control-custom mb-3" required><div class="row g-2 mb-3"><div class="col-6"><select name="type" id="edit_inv_type" class="form-select form-select-custom" required><option value="Pengeluaran">Beli</option><option value="Pemasukan">Jual</option></select></div><div class="col-6"><select name="portfolio_id" id="edit_inv_pid" class="form-select form-select-custom"><option value="">-- Platform --</option>{% for p in portfolios %}<option value="{{ p.id }}">{{ p.name }}</option>{% endfor %}</select></div></div><div class="alert bg-light border border-dashed rounded-4 p-3 mb-3"><label class="form-label small fw-bold text-dark mb-2">Tautkan ke Target Tabungan</label><select name="goal_id" id="edit_inv_gid" class="form-select form-select-sm form-select-custom border-0 shadow-sm" style="border-radius: 15px;"><option value="">-- Tidak ditautkan ke Goal --</option>{% for g in goals %}<option value="{{ g.id }}">Goal: {{ g.name }}</option>{% endfor %}</select></div><select name="asset_type" id="edit_inv_atype" class="form-select form-select-custom mb-3"><option value="">Pilih Jenis Investasi...</option><option value="Saham">Saham</option><option value="Reksa Dana">Reksa Dana</option><option value="Emas">Emas</option><option value="Kripto">Kripto</option><option value="Lainnya">Lainnya / Kas</option></select><input type="text" name="asset_name" id="edit_inv_aname" class="form-control form-control-custom mb-3" placeholder="Nama Aset / Judul"><input type="number" step="any" name="quantity" id="edit_inv_qty" class="form-control form-control-custom mb-3" placeholder="Kuantitas (Isi 1 jika Kas)"><div class="row g-2 mb-3"><div class="col-6"><input type="number" step="any" name="nominal" id="edit_inv_nom" class="form-control form-control-custom" placeholder="Total Nominal (Rp)" required></div><div class="col-6"><select name="account" id="edit_inv_acc" class="form-select form-select-custom" required><option value="">Pilih Akun Bank...</option>{% for acc in accounts %}<option value="{{ acc }}">{{ acc }}</option>{% endfor %}</select></div></div></div><div class="modal-footer border-0"><button type="submit" class="btn btn-yellow w-100 btn-custom">Simpan Perubahan</button></div></form></div></div></div>
<div class="modal fade" id="addGoalModal"><div class="modal-dialog modal-dialog-centered"><div class="modal-content"><form action="/goals/add" method="POST"><div class="modal-header border-0"><h5 class="modal-title">Buat Target Tabungan</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><input type="text" name="name" class="form-control form-control-custom mb-3" placeholder="Nama Goal (Cth: Dana Darurat)" required><input type="number" step="any" name="target_amount" class="form-control form-control-custom mb-3" placeholder="Target Nominal" required><input type="date" name="deadline" class="form-control form-control-custom mb-3" required></div><div class="modal-footer border-0"><button type="submit" class="btn btn-yellow w-100 btn-custom">Buat Target</button></div></form></div></div></div>
<div class="modal fade" id="platformModal"><div class="modal-dialog modal-dialog-centered"><div class="modal-content"><div class="modal-header border-0"><h5 class="modal-title">Kelola Platform</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><form action="/portfolios/add" method="POST" class="mb-4 d-flex gap-2"><input type="text" name="name" class="form-control form-control-custom" placeholder="Nama platform baru..." required><button type="submit" class="btn btn-dark-custom btn-custom"><i class="bi bi-plus-lg"></i></button></form><div class="list-group">{% for p in portfolios %}<div class="list-group-item border-0 d-flex justify-content-between align-items-center px-0 py-2"><span class="fw-medium text-dark"><i class="bi bi-grid me-2 text-muted"></i> {{ p.name }}</span><form action="/portfolios/delete/{{ p.id }}" method="POST" class="m-0"><button type="submit" class="btn btn-sm text-danger shadow-none p-0"><i class="bi bi-trash3"></i></button></form></div>{% endfor %}</div></div></div></div></div>
<div class="modal fade" id="accountModal"><div class="modal-dialog modal-dialog-centered"><div class="modal-content"><div class="modal-header border-0"><h5 class="modal-title">Kelola Akun / Dompet</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><form action="/accounts/add" method="POST" class="mb-4 d-flex gap-2"><input type="text" name="name" class="form-control form-control-custom" placeholder="Nama Akun baru..." required><button type="submit" class="btn btn-dark-custom btn-custom"><i class="bi bi-plus-lg"></i></button></form><div class="list-group">{% for a in account_objects %}<div class="list-group-item border-0 d-flex justify-content-between align-items-center px-0 py-2"><span class="fw-medium text-dark"><i class="bi bi-wallet2 me-2 text-muted"></i> {{ a.name }}</span><form action="/accounts/delete/{{ a.id }}" method="POST" class="m-0"><button type="submit" class="btn btn-sm text-danger shadow-none p-0"><i class="bi bi-trash3"></i></button></form></div>{% endfor %}</div></div></div></div></div>

<script>
    document.addEventListener('DOMContentLoaded', () => {
        const setupAssetTypeListener = (dropdownId, inputId) => { document.getElementById(dropdownId)?.addEventListener('change', function() { const qtyInput = document.getElementById(inputId); if(this.value === 'Saham') qtyInput.placeholder = 'Kuantitas (Berapa Lot?)'; else if(this.value === 'Emas') qtyInput.placeholder = 'Kuantitas (Berapa Gram?)'; else if(this.value === 'Kripto') qtyInput.placeholder = 'Kuantitas (Berapa Koin?)'; else if(this.value === 'Reksa Dana') qtyInput.placeholder = 'Kuantitas (Berapa Unit?)'; else qtyInput.placeholder = 'Kuantitas (Isi 1 jika Kas)'; }); };
        setupAssetTypeListener('assetType', 'qtyInput'); setupAssetTypeListener('edit_inv_atype', 'edit_inv_qty');
        document.getElementById('selectAllCheckboxInv')?.addEventListener('change', (e) => { document.querySelectorAll('.inv-checkbox').forEach(cb => cb.checked = e.target.checked); });
        document.getElementById('btnEditInvSelected')?.addEventListener('click', () => { const chks = document.querySelectorAll('.inv-checkbox:checked'); if(chks.length !== 1) return showToast('Pilih TEPAT 1 riwayat aset untuk diedit!', 'warning'); const chk = chks[0]; document.getElementById('edit_inv_tx_id').value = chk.value; document.getElementById('edit_inv_tgl').value = chk.dataset.tgl; document.getElementById('edit_inv_type').value = chk.dataset.type; document.getElementById('edit_inv_pid').value = chk.dataset.pid; document.getElementById('edit_inv_gid').value = chk.dataset.gid; document.getElementById('edit_inv_atype').value = chk.dataset.atype; document.getElementById('edit_inv_atype').dispatchEvent(new Event('change')); document.getElementById('edit_inv_aname').value = chk.dataset.aname; document.getElementById('edit_inv_qty').value = chk.dataset.qty; document.getElementById('edit_inv_nom').value = chk.dataset.nom; document.getElementById('edit_inv_acc').value = chk.dataset.acc; new bootstrap.Modal(document.getElementById('editInvestModal')).show(); });
        document.getElementById('btnDeleteInvSelected')?.addEventListener('click', () => { const chks = document.querySelectorAll('.inv-checkbox:checked'); if(chks.length === 0) { showToast('Pilih minimal 1 riwayat aset untuk dihapus.', 'danger'); return; } document.getElementById('deleteModalTextInv').innerText = `Anda yakin ingin menghapus ${chks.length} riwayat aset/tabungan terpilih? Saldo yang terkumpul di Goal terkait akan disesuaikan kembali secara otomatis.`; new bootstrap.Modal(document.getElementById('deleteConfirmModalInv')).show(); });
        document.getElementById('confirmDeleteBtnInv')?.addEventListener('click', () => { const form = document.getElementById('bulkActionFormInv'); const actionInput = document.createElement('input'); actionInput.type = 'hidden'; actionInput.name = 'action'; actionInput.value = 'delete'; form.appendChild(actionInput); form.submit(); });
    });
</script>
"""

HTML_BUDGETS = """
<div class="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-3"><h1 class="fw-light mb-0 title-huge text-dark">Anggaran Bulanan</h1><form method="GET" action="/budgets" class="d-flex gap-2 m-0"><input type="month" name="period" class="form-control form-control-custom bg-white border shadow-sm fw-medium" value="{{ curr_period }}" onchange="this.form.submit()"><button type="button" class="btn btn-custom btn-dark-custom text-nowrap" data-bs-toggle="modal" data-bs-target="#addBudgetModal"><i class="bi bi-pie-chart"></i> Atur Anggaran</button></form></div>
<div class="row g-4 mb-5">
    <div class="col-md-8"><div class="card-custom bg-white p-4 h-100"><h5 class="fw-medium text-dark mb-4"><i class="bi bi-bar-chart-steps text-warning me-2" style="color: var(--accent-yellow) !important;"></i>Realisasi Anggaran vs Batas</h5><div style="height: 350px; position: relative;"><canvas id="budgetBarChart"></canvas></div></div></div>
    <div class="col-md-4 d-flex flex-column gap-4">
        <div class="card-custom p-4 border" style="background: var(--bg-inner);"><h5 class="fw-bold mb-3"><i class="bi bi-lightbulb text-warning me-1"></i> Smart Insights</h5><div class="mb-3"><span class="d-block small text-muted fw-semibold">Sisa Hari Bulan Terpilih</span><div class="fs-4 fw-bold text-dark">{{ days_left }} Hari</div></div><div class="p-3 bg-white rounded-4 border shadow-sm"><span class="d-block small text-muted fw-semibold mb-1">Batas Aman Pengeluaran Harian</span>{% if budgets|length == 0 %}<h4 class="fw-bold text-muted m-0">Belum Diatur</h4>{% elif safe_daily_budget > 0 %}<h4 class="fw-bold text-success m-0">{{ safe_daily_budget | rupiah }} <span class="small text-muted fw-normal" style="font-size: 0.8rem;">/hari</span></h4>{% else %}<h4 class="fw-bold text-danger m-0">Anggaran Habis!</h4>{% endif %}</div></div>
        <div class="card-custom bg-white p-4 flex-grow-1 overflow-auto custom-scrollbar" style="max-height: 300px;"><h6 class="fw-bold mb-3 text-muted">Daftar Anggaran</h6><div class="d-flex flex-column gap-3">{% for b in budgets %}<div class="p-3 border rounded-4 position-relative" style="background: var(--bg-inner);"><form action="/budgets/delete/{{ b.id }}" method="POST" class="position-absolute top-0 end-0 m-2"><button type="submit" class="btn btn-sm text-danger shadow-none p-0"><i class="bi bi-trash3"></i></button></form><div class="d-flex align-items-center mb-1 gap-2"><span class="badge bg-white text-dark border px-2 py-1"><i class="bi bi-tag me-1"></i> {{ b.cat_name }}</span></div><div class="d-flex justify-content-between align-items-end mb-1 mt-2"><span class="fs-6 fw-bold {{ 'text-danger' if b.spent > b.amount else 'text-dark' }}">{{ b.spent | rupiah }}</span><span class="text-muted" style="font-size: 0.65rem;">Batas: {{ b.amount | rupiah }}</span></div>{% set pct = (b.spent / b.amount * 100) | int if b.amount > 0 else 0 %}<div class="progress" style="height: 5px; border-radius: 3px;"><div class="progress-bar {{ 'bg-danger' if pct > 100 else 'bg-warning' }}" style="width: {{ pct if pct <= 100 else 100 }}%;"></div></div></div>{% else %}<div class="text-center py-4 text-muted small border rounded-4 border-dashed">Belum ada anggaran bulanan pada bulan ini.</div>{% endfor %}</div></div>
    </div>
</div>
<div class="modal fade" id="addBudgetModal"><div class="modal-dialog modal-dialog-centered"><div class="modal-content"><form action="/budgets/add" method="POST"><div class="modal-header border-0"><h5 class="modal-title">Set Anggaran Bulanan</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><input type="hidden" name="period" value="{{ curr_period }}"><select name="category_id" class="form-select form-select-custom mb-3" required><option value="">Pilih Kategori Pengeluaran...</option>{% for c in categories %}{% if c.type == 'Pengeluaran' %}<option value="{{ c.id }}">{{ c.name }}</option>{% endif %}{% endfor %}</select><input type="number" step="any" name="amount" class="form-control form-control-custom mb-3" placeholder="Batas Pengeluaran (Rp)" required></div><div class="modal-footer border-0"><button type="submit" class="btn btn-dark-custom w-100 btn-custom">Simpan Anggaran</button></div></form></div></div></div>
<script>
    new Chart(document.getElementById('budgetBarChart').getContext('2d'), { type: 'bar', data: { labels: {{ budget_labels | safe }}, datasets: [ { label: 'Terpakai', data: {{ budget_spent | safe }}, backgroundColor: '#303030', borderRadius: 6, barPercentage: 0.7, categoryPercentage: 0.8 }, { label: 'Batas Maksimal', data: {{ budget_limits | safe }}, backgroundColor: '#FFD861', borderRadius: 6, barPercentage: 0.7, categoryPercentage: 0.8 } ] }, options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top', labels: { boxWidth: 12, font: { family: 'Outfit', size: 12 } } }, tooltip: { backgroundColor: '#303030', titleFont: { family: 'Outfit', size: 13 }, bodyFont: { family: 'Outfit', size: 12 }, padding: 10, cornerRadius: 10 } }, scales: { x: { min: 0, grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { font: { family: 'Outfit' }, callback: function(val) { return 'Rp' + (val >= 1000000 ? (val/1000000) + 'jt' : val); } } }, y: { grid: { display: false }, ticks: { font: { family: 'Outfit', weight: '500' } } } } } });
</script>
"""

HTML_REPORTS = """
<div class="d-flex justify-content-between align-items-center mb-4"><h1 class="fw-light mb-0 title-huge text-dark">Buku Besar Akuntansi</h1><form method="GET" action="/reports" class="d-flex gap-2 m-0"><input type="month" name="month" class="form-control form-control-custom" value="{{ selected_month }}" onchange="this.form.submit()"><a href="/export/pdf?month={{ selected_month }}" class="btn btn-yellow btn-custom text-nowrap"><i class="bi bi-file-pdf"></i> PDF</a></form></div>
<div class="row g-4 mb-4"><div class="col-md-4"><div class="card-custom bg-white p-4"><h6 class="text-muted">Kas Masuk (Debit)</h6><h3 class="text-success">+{{ total_debit | rupiah }}</h3></div></div><div class="col-md-4"><div class="card-custom bg-white p-4"><h6 class="text-muted">Kas Keluar (Kredit)</h6><h3 class="text-danger">-{{ total_kredit | rupiah }}</h3></div></div><div class="col-md-4"><div class="card-custom card-dark p-4"><h6 class="text-white opacity-75">Net Cashflow</h6><h3 class="text-white">{{ (total_debit - total_kredit) | rupiah }}</h3></div></div></div>
<div class="card-custom bg-white p-4 mb-4" style="border-radius: 20px;"><div class="table-responsive"><table class="table-modern"><thead><tr><th>Tanggal</th><th>Akun Bank</th><th>Keterangan & Pos</th><th class="text-end">Pemasukan (Debit)</th><th class="text-end">Pengeluaran (Kredit)</th><th class="text-end">Saldo Berjalan</th></tr></thead><tbody>{% for row in ledger %}<tr><td class="text-muted">{{ row.tgl }}</td><td><span class="badge bg-light text-dark border">{{ row.account }}</span></td><td><div class="fw-medium text-dark">{{ row.desc }}</div><div class="small text-muted">{{ row.pos }}</div></td><td class="text-end text-success fw-medium">{{ row.debit | rupiah if row.debit > 0 else '-' }}</td><td class="text-end text-danger fw-medium">{{ row.kredit | rupiah if row.kredit > 0 else '-' }}</td><td class="text-end text-dark fw-bold">{{ row.saldo | rupiah }}</td></tr>{% else %}<tr><td colspan="6" class="text-center py-4 text-muted">Belum ada entri jurnal pada bulan ini.</td></tr>{% endfor %}</tbody></table></div></div>
"""

TPL_LOGIN_FULL = TPL_AUTH.replace('<!-- CONTENT_AUTH_PLACEHOLDER -->', HTML_LOGIN).replace('{{ title }}', 'Login')
TPL_REGISTER_FULL = TPL_AUTH.replace('<!-- CONTENT_AUTH_PLACEHOLDER -->', HTML_REGISTER).replace('{{ title }}', 'Daftar Akun')
TPL_DASHBOARD = TPL_BASE.replace('<!-- CONTENT_PLACEHOLDER -->', HTML_DASHBOARD)
TPL_TRANSACTIONS = TPL_BASE.replace('<!-- CONTENT_PLACEHOLDER -->', HTML_TRANSACTIONS)
TPL_PORTFOLIOS = TPL_BASE.replace('<!-- CONTENT_PLACEHOLDER -->', HTML_PORTFOLIOS)
TPL_BUDGETS = TPL_BASE.replace('<!-- CONTENT_PLACEHOLDER -->', HTML_BUDGETS)
TPL_REPORTS = TPL_BASE.replace('<!-- CONTENT_PLACEHOLDER -->', HTML_REPORTS)
