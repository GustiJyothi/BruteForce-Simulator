# 🔐 Brute Force Login Simulator

Simulasi realistis untuk mempelajari dan menguji keamanan sistem login terhadap serangan brute force. Lengkap dengan fitur captcha, rate limiting, user-agent simulation, dan mode challenge. Cocok untuk edukasi, pentest lab, maupun demonstrasi keamanan siber.

---

## 🎯 Fitur Utama

- 🔐 **Manual Login** — Uji login dengan input user-pass secara langsung.
- 🤖 **Brute Force Otomatis** — Coba kombinasi dari wordlist terhadap seluruh akun yang ada.
- 🔁 **Rate Limiting Cerdas** — Dilengkapi dengan algoritma exponential backoff dan lockout.
- 🧠 **Captcha Challenge** — Captcha aktif otomatis setelah gagal 3x untuk mencegah spam.
- 📶 **User-Agent Simulation** — Simulasi berbagai perangkat & browser.
- 🐢 **Auto Delay Randomized** — Tambahkan jeda otomatis agar lebih mirip trafik asli.
- 🎮 **Mode Challenge** — Buat akun acak dengan password rahasia untuk tantangan eksploitasi!
- 📊 **Progress Bar & Statistik** — Visualisasi proses brute force secara real-time.
- 📝 **Log Lengkap** — Semua percobaan login dicatat rapi dengan status dan user-agent.

---

## 🚀 Instalasi & Menjalankan

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/GustiJyothi/BruteForce-Simulator.git
   cd BruteForce-Simulator
   ```

2. **Jalankan script:**
   ```bash
   python login_simulator.py 
   ```

   > ✅ Pastikan Python 3 sudah terinstal. Script ini tidak membutuhkan dependensi eksternal apa pun.

---

## 🖥️ Tampilan Menu

```
==============================================
Brute Force Login Simulator - Interactive Menu
==============================================
1. Manual Login
2. Brute Force Otomatis (wordlist)
3. Toggle Captcha (Currently: ON/OFF)
4. Toggle Progress Bar & Statistik (Currently: ON/OFF)
5. Toggle User-Agent Simulation (Currently: ON/OFF)
6. Toggle Auto Delay (Currently: ON/OFF)
7. Mode Challenge (Random User/Pass)
8. Keluar
```

---

## 🧪 Contoh Skema Penggunaan

- 🔍 **Menguji keamanan sistem login lokal.**
- 📚 **Simulasi edukasi dalam pelatihan keamanan siber.**
- 🔒 **Melatih tim Blue Team dalam membaca log & mendeteksi brute force.**

---

## 🧾 Format Log Output

Semua aktivitas login disimpan dalam file `bruteforce_sim_log.txt`, contoh:
```
2025-06-08 17:12:33 | admin:123456 | FAIL | UA: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
2025-06-08 17:12:35 | admin:Passw0rd! | SUCCESS | UA: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
```

---

## ⚠️ Disclaimer

> ⚠️ Proyek ini hanya untuk edukasi dan penggunaan di lingkungan aman atau lab pribadi. Dilarang keras menggunakan ini untuk menyerang sistem nyata tanpa izin tertulis.

---
