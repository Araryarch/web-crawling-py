
# Deployment Guide (Vercel)

Project ini sudah dikonfigurasi agar siap dideploy ke **Vercel**.

## Cara Deploy (Recommended)

1. **Install Vercel CLI** (jika belum punya):
   ```bash
   npm install -g vercel
   ```

2. **Login ke Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   Jalankan command berikut di root folder project:
   ```bash
   vercel
   ```
   Ikuti langkah-langkah di terminal (tekan Enter untuk default).

4. **Environment Variables**:
   Jika ingin mengubah konfigurasi di production, atur Environment Variables di Dashboard Vercel (Settings > Environment Variables):
   - `FLASK_ENV`: production
   - `CRAWLER_TIMEOUT`: 10
   - `CRAWLER_MAX_PAGES`: 100
   - dll (sesuai `.env.example`)

## Struktur Deployment
- `vercel.json`: Konfigurasi routing agar traffic diarahkan ke `run.py`.
- `run.py`: Entry point aplikasi Flask. Vercel akan mencari object `app` di sini.
