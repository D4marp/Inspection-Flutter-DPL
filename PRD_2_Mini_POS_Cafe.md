# PRD: Mini POS Cafe

| | |
|---|---|
| **Versi** | 1.0 (MVP) |
| **Status** | Draft untuk review |
| **Tanggal** | 13 Okt 2026 |
| **Platform** | Flutter (Android & iOS), offline penuh |
| **Prioritisasi** | MoSCoW (aturan di bagian 4) |
| **Stack wajib** | flutter_riverpod, shared_preferences, Clean Architecture |

---

## 1. Objective & Problem Statement

### 1.1 Problem Statement
Kasir atau barista di kafe kecil sering menghitung pesanan dengan kalkulator atau catatan kertas. Saat ramai, total bisa salah, riwayat penjualan tidak tercatat rapi, dan kesempatan menawarkan produk tambahan (upsell) terlewat.

### 1.2 Objective
Membangun MVP kasir **offline** yang:
1. Menghitung total pesanan dengan benar dari keranjang.
2. Menyimpan riwayat transaksi di perangkat.
3. Menampilkan "AI Promo Suggester" (mock) berupa saran produk tambahan acak dari data lokal saat tombol Bayar ditekan.

### 1.3 Hipotesis
Jika menambah item, mengubah qty, dan membayar bisa dilakukan dalam beberapa tap, kasir akan memakai aplikasi ini di jam sibuk. Saran upsell di titik bayar meningkatkan peluang penawaran tambahan tanpa memperlambat transaksi.

---

## 2. Success Metrics

> Tanpa backend/analytics. Semua metrik diukur lewat skrip uji, unit test, dan usability test kecil. Target berlaku untuk v0.1.0.

| # | Tujuan | Metrik | Target | Cara Ukur |
|---|--------|--------|--------|-----------|
| M1 | Hitungan benar | Total keranjang sama dengan hitungan manual pada kasus uji | 100% pada ≥ 20 kasus | Unit test `CartCalculator` |
| M2 | Transaksi cepat | Waktu membuat pesanan 3 item sampai tersimpan (menu sudah ada) | ≤ 30 detik (median) | Stopwatch pada usability test 5 penguji |
| M3 | Alur inti mudah | Penguji menyelesaikan login → tambah menu → isi keranjang → bayar → lihat riwayat tanpa bantuan | ≥ 4 dari 5 | Usability test |
| M4 | Saran upsell muncul | Dialog AI muncul pada Bayar bila ada kandidat | 100% | Unit + widget test |
| M5 | Tidak ada transaksi ganda | Double-tap Bayar menghasilkan transaksi | Tepat 1 | Widget test |
| M6 | Data bertahan | Riwayat, menu, dan sesi utuh setelah force-close | 100% pada 3 percobaan | Uji manual |
| M7 | Kualitas teknis | `flutter analyze` / cakupan domain / start dingin | 0 isu / ≥ 80% / ≤ 2 dtk | `flutter test --coverage`, DevTools |

**Counter-metric:** penambahan dialog AI tidak boleh menambah lebih dari 1 tap pada alur bayar.

---

## 3. Target Audience & Personas

### Persona Utama: Dimas (24), barista paruh waktu
- **Konteks:** kafe kecil 1–2 staf; jam sibuk pagi dan sore; satu tangan sering memegang gelas.
- **Tujuan:** mencatat pesanan cepat, total tidak salah, tidak mengulang ketik.
- **Frustrasi:** kalkulator dan kertas lambat; lupa menawarkan tambahan; tidak ada rekap.
- **Perilaku:** mengetik cepat dengan jempol; butuh tombol besar dan alur pendek.
- **Kutipan:** "Pokoknya totalnya jangan sampai salah, antrean udah panjang."

### Persona Sekunder: Bu Sari (45), pemilik kafe
Ingin melihat riwayat transaksi sederhana di akhir hari. Tidak mengoperasikan kasir.

### Stakeholder: Developer/Reviewer
Menilai arsitektur, Riverpod, dan kemudahan pengujian logika keranjang.

---

## 4. Functional Requirements (MoSCoW)

**Aturan prioritisasi**
- **Must:** tanpa ini journey utama gagal, atau ada risiko kesalahan uang/integritas data. Blocker rilis.
- **Should:** penting tetapi ada workaround; masuk v0.1.0 jika jadwal cukup, jika tidak ke v0.2.
- **Could:** nilai tambah kecil; default v0.2+.
- **Won't (rilis ini):** disepakati tidak dikerjakan sekarang.
- Must tidak melebihi sekitar 60% dari total effort.

**Keputusan desain yang memengaruhi requirement**
- Harga disimpan sebagai **integer rupiah** (tanpa desimal) untuk menghindari galat floating-point.
- Transaksi menyimpan **snapshot** nama dan harga satuan saat dijual, sehingga menghapus menu tidak mengubah riwayat.
- Peran Barista/Kasir hanya **label** yang dicatat pada transaksi; belum ada perbedaan hak akses.

| ID | Requirement | Prioritas | Catatan / Alasan | Story |
|----|-------------|-----------|------------------|-------|
| **Autentikasi** | | | | |
| FR-P01 | Login memilih peran (Barista/Kasir) + PIN 4 digit (PIN `1234`) | **Must** | Syarat skenario auth | US-P01 |
| FR-P02 | Simpan `cashier_session_token` + peran; sesi bertahan setelah restart | **Must** | Syarat skenario auth | US-P01 |
| FR-P03 | Logout menghapus token | **Must** | Siklus sesi lengkap | US-P02 |
| FR-P04 | Tampilkan peran aktif di app bar | Should | Kejelasan siapa yang bertugas | US-P02 |
| FR-P05 | Hak akses berbeda per peran | Won't | Peran hanya label di MVP | - |
| **Menu** | | | | |
| FR-P06 | Tambah menu (nama wajib, harga integer > 0 dan ≤ 9.999.999) | **Must** | Tanpa data awal, menu harus bisa dibuat | US-P03 |
| FR-P07 | Daftar menu dengan empty state | **Must** | Dasar pembuatan pesanan | US-P03 |
| FR-P08 | Hapus menu (dengan konfirmasi) | Should | Koreksi salah ketik; riwayat aman karena snapshot | US-P03 |
| FR-P09 | Edit menu | Could | Alternatif hapus lalu tambah ulang | US-P03 |
| **Keranjang** | | | | |
| FR-P10 | Tap menu menambah ke keranjang; tap lagi menambah qty | **Must** | Inti produk | US-P04 |
| FR-P11 | Tombol +/− qty; qty 0 menghapus item | **Must** | Koreksi pesanan | US-P04 |
| FR-P12 | Hapus item dari keranjang | **Must** | CRUD yang diminta | US-P04 |
| FR-P13 | Total = Σ(harga × qty), format `Rp15.000`, update langsung | **Must** | Inti produk | US-P05 |
| FR-P14 | Kosongkan seluruh keranjang | Should | Mempercepat pembatalan pesanan | US-P04 |
| FR-P15 | Keranjang tersimpan saat aplikasi ditutup | Could | Lihat risiko R4 | - |
| **Pembayaran** | | | | |
| FR-P16 | Tombol Bayar nonaktif bila keranjang kosong | **Must** | Cegah transaksi kosong | US-P06 |
| FR-P17 | Mock AI Promo Suggester pada Bayar (aturan bagian 6) | **Must** | Pembeda produk dan syarat brief | US-P07 |
| FR-P18 | Konfirmasi bayar → simpan transaksi → kosongkan keranjang | **Must** | Inti produk | US-P06 |
| FR-P19 | Cegah transaksi ganda saat tombol ditekan berulang | **Must** | Integritas data uang | US-P06 |
| FR-P20 | Input uang diterima dan hitung kembalian | Could | Kebutuhan wajar kasir tunai; ditunda agar MVP kecil | - |
| **Riwayat** | | | | |
| FR-P21 | Daftar riwayat (waktu, ringkasan item, total), terbaru di atas, disimpan di SharedPreferences | **Must** | Syarat brief | US-P08 |
| FR-P22 | Riwayat menyimpan snapshot nama, harga satuan, qty, total, peran | **Must** | Integritas data | US-P08 |
| FR-P23 | Detail transaksi | Should | Verifikasi rincian | US-P08 |
| FR-P24 | Empty state riwayat | **Must** | Mulai tanpa data | US-P08 |
| FR-P25 | Metode pembayaran, diskon, cetak struk, laporan harian, stok, multi-cabang | Won't | Di luar MVP | - |

---

## 5. Critical User Journeys & User Stories

### 5.1 Critical User Journeys

**CUJ-1: Memulai shift dan membuat pesanan pertama** (journey utama, M2 dan M3)
1. Buka aplikasi → Login → pilih peran Kasir, PIN `1234`.
2. Tab Menu masih kosong → tambah "Kopi Susu" Rp18.000 dan "Donat Cokelat" Rp10.000.
3. Tab Kasir: tap "Kopi Susu" dua kali → qty 2; total Rp36.000.
4. Tap Bayar → dialog AI: "Tawarkan Donat Cokelat seharga Rp10.000…" → Lanjut Bayar.
5. Konfirmasi → transaksi tersimpan, keranjang kosong, notifikasi singkat "Transaksi tersimpan".
6. *Jalur gagal:* keranjang kosong → tombol Bayar nonaktif.

**CUJ-2: Koreksi pesanan**
1. Keranjang berisi 3 item → kurangi qty, hapus satu item, total ikut berubah.
2. Atau Kosongkan keranjang (Should).

**CUJ-3: Memeriksa riwayat**
1. Tab Riwayat → daftar terbaru di atas → tap item → detail (Should).

### 5.2 User Stories

| ID | Story | FR |
|----|-------|----|
| US-P01 | Sebagai kasir, saya ingin login dengan peran dan PIN dan tetap login saat aplikasi dibuka ulang, agar tidak mengulang di tengah antrean. | P01, P02 |
| US-P02 | Sebagai kasir, saya ingin logout dan melihat peran saya, agar pergantian shift jelas. | P03, P04 |
| US-P03 | Sebagai kasir, saya ingin menambah dan menghapus menu, agar daftar jualan sesuai kondisi kafe. | P06–P09 |
| US-P04 | Sebagai kasir, saya ingin menambah, mengubah qty, dan menghapus item di keranjang, agar pesanan sesuai permintaan pelanggan. | P10–P12, P14 |
| US-P05 | Sebagai kasir, saya ingin total harga tampil langsung, agar tidak salah hitung. | P13 |
| US-P06 | Sebagai kasir, saya ingin membayar dan menyimpan transaksi dengan aman, agar tidak tercatat dua kali. | P16, P18, P19 |
| US-P07 | Sebagai kasir, saya ingin saran produk tambahan saat bayar, agar bisa menawarkannya kepada pelanggan. | P17 |
| US-P08 | Sebagai kasir/pemilik, saya ingin melihat riwayat transaksi, agar bisa merekap penjualan. | P21–P24 |

---

## 6. Acceptance Criteria

**AC-P01 Login & sesi (FR-P01–P03)**
- Given belum login, When pilih peran dan PIN `1234` lalu Masuk, Then `cashier_session_token` dan peran tersimpan, dan layar Kasir tampil.
- Given PIN salah atau bukan 4 digit, Then muncul pesan error dan tidak ada token tersimpan.
- Given sudah login, When aplikasi di-force-close lalu dibuka, Then langsung masuk layar Kasir.
- Given tap Logout, Then token terhapus dan Login tampil.

**AC-P02 Tambah menu (FR-P06, P07)**
- Given nama kosong atau harga ≤ 0 atau bukan angka, Then muncul validasi dan menu tidak tersimpan.
- Given nama dan harga valid, Then menu muncul di daftar dan bertahan setelah restart.
- Given belum ada menu, Then empty state dengan tombol "Tambah menu".

**AC-P03 Keranjang (FR-P10–P12)**
- Given tap menu yang belum ada di keranjang, Then item masuk dengan qty 1.
- Given tap menu yang sama, Then qty bertambah 1.
- Given tap − pada qty 1, Then item terhapus dari keranjang.
- Given tap hapus pada item, Then item hilang tanpa memengaruhi item lain.

**AC-P04 Total (FR-P13)**

| Keranjang | Total |
|-----------|-------|
| Kosong | Rp0 |
| 1 × Rp18.000 | Rp18.000 |
| 2 × Rp18.000 + 1 × Rp10.000 | Rp46.000 |
| 3 × Rp7.500 | Rp22.500 |
| Item dihapus → sisa 1 × Rp10.000 | Rp10.000 |
- Format ribuan memakai titik; tanpa desimal; prefiks `Rp`.

**AC-P05 Bayar (FR-P16, P18, P19)**
- Given keranjang kosong, Then tombol Bayar nonaktif.
- Given keranjang terisi, When Bayar → (dialog AI jika ada kandidat) → Konfirmasi, Then tepat satu `Transaction` tersimpan dengan snapshot item, total, peran, dan waktu; keranjang kosong.
- Given tombol Konfirmasi ditekan dua kali berturut-turut, Then hanya satu transaksi tersimpan.

**AC-P06 Mock AI Promo Suggester (FR-P17)**
- Kandidat = menu yang **tidak ada** di keranjang.
- Given ada ≥ 1 kandidat, When tap Bayar, Then dialog "AI Recommendation" menampilkan satu kandidat acak: "AI menyarankan: Tawarkan {nama} seharga {harga} sebagai pendamping pesanan ini!"
- Given tidak ada kandidat (semua menu sudah di keranjang atau hanya ada satu menu), Then dialog dilewati dan langsung ke konfirmasi.
- Dialog punya dua tombol: "Lanjut Bayar" dan "Kembali ke Keranjang". Saran **tidak** menambah item otomatis.
- Pemilihan acak bisa diuji dengan `Random` ber-seed.

**AC-P07 Riwayat (FR-P21–P24)**
- Given ada transaksi, Then daftar terbaru di atas dengan waktu, ringkasan item, dan total.
- Given menu dihapus setelah transaksi, Then rincian transaksi lama tetap menampilkan nama dan harga saat itu.
- Given belum ada transaksi, Then empty state tampil.

---

## 7. Out of Scope

- Metode pembayaran, input uang diterima/kembalian (Could), diskon/pajak, struk cetak.
- Stok bahan, laporan harian/mingguan, ekspor.
- Perbedaan hak akses per peran, multi-kasir, multi-cabang.
- Sinkronisasi cloud, integrasi printer/QRIS.
- AI sungguhan (rekomendasi hanya acak dari data lokal).

---

## 8. Non-Functional Requirements

| Kategori | Requirement | Target | Verifikasi |
|----------|-------------|--------|------------|
| Performa | Start dingin | ≤ 2 detik | DevTools |
| Performa | Respons tap menu → total ter-update | ≤ 100 ms | Uji manual / widget test |
| Performa | Riwayat 1.000 transaksi | Scroll ≥ 55 fps | DevTools |
| Keandalan | Data bertahan setelah force-close | 100% | Uji manual |
| Keandalan | Data rusak di storage | Tidak crash; tampil kosong + pesan | Unit test datasource |
| Akurasi | Perhitungan uang | Integer rupiah, tanpa floating-point | Unit test |
| Keamanan & privasi | Data lokal; tanpa permission INTERNET; tanpa log PIN | Terpenuhi | Cek manifest, review |
| Keamanan | Token dan PIN di SharedPreferences/konstanta bukan batas keamanan nyata | Didokumentasikan | Review |
| Aksesibilitas | Target sentuh ≥ 48 dp (tombol kasir ≥ 56 dp); kontras ≥ 4,5:1; teks 1,5× tanpa overflow | Terpenuhi | Uji manual |
| Kompatibilitas | Android API 24+, iOS 13+; potret; lebar ≥ 360 dp | Terpenuhi | Emulator |
| Lokalisasi | Bahasa Indonesia; mata uang `Rp15.000`; tanggal `13 Okt 2026, 17.33` | Terpenuhi | Review |
| Maintainability | `analyze` 0 isu; aturan layer ditaati | Terpenuhi | Lint + review |
| Testabilitas | Cakupan `domain` ≥ 80% | ≥ 80% | `flutter test --coverage` |

---

## 9. Dependencies, Assumptions & Risks

### 9.1 Dependencies
| Jenis | Item | Keterangan |
|-------|------|------------|
| Paket runtime | `flutter_riverpod`, `shared_preferences`, `intl` | State, penyimpanan, format Rupiah/tanggal |
| Paket dev | `flutter_test`, `mocktail`, `flutter_lints` | Pengujian dan lint |
| Layanan eksternal | Tidak ada | Offline penuh |

### 9.2 Assumptions
- A1: Satu perangkat kasir; satu sesi aktif.
- A2: Semua harga dalam Rupiah bulat.
- A3: PIN `1234` tetap; autentikasi demo.
- A4: Kasir mengisi menu sendiri di awal (tanpa data bawaan).
- A5: Keranjang boleh hilang bila aplikasi dimatikan paksa (FR-P15 Could).

### 9.3 Risks
| ID | Risiko | Peluang | Dampak | Mitigasi |
|----|--------|---------|--------|----------|
| R1 | Salah hitung karena floating-point | Rendah | Tinggi | Integer rupiah; unit test M1 |
| R2 | Transaksi ganda saat tap berulang | Sedang | Tinggi | FR-P19; tombol dikunci selama proses |
| R3 | Menu dihapus mengubah riwayat lama | Sedang | Tinggi | Snapshot nama dan harga (FR-P22) |
| R4 | Keranjang hilang saat aplikasi mati | Sedang | Sedang | Diterima di MVP; FR-P15 Could |
| R5 | Kasir tidak punya kembalian otomatis sehingga hitung manual | Tinggi | Sedang | Dicatat sebagai backlog teratas v0.2 (FR-P20) |
| R6 | Peran tidak berbeda hak akses bisa disalahpahami | Sedang | Rendah | UI menyebut peran sebagai "Bertugas sebagai"; FR-P05 ditunda |
| R7 | SharedPreferences kurang cocok untuk riwayat besar | Sedang | Sedang | Repository abstrak; migrasi ke SQLite saat perlu |
| R8 | Scope creep (diskon, struk) | Sedang | Sedang | Daftar Won't dibekukan |

### 9.4 Pertanyaan Terbuka
- Perlukah saran AI tidak mengulang kandidat yang sama dua transaksi berturut-turut? (default: tidak)

---

## 10. Design & UX

### 10.1 Prinsip
- Cepat dan satu tangan: tombol besar (≥ 56 dp), area utama di jangkauan jempol.
- Angka jelas: total selalu terlihat, huruf besar, kontras tinggi.
- Warna **solid**, **tanpa gradient**, tanpa glassmorphism/neon/shadow berlebihan.

### 10.2 Peta Navigasi
```
Login ──> Shell (bottom nav)
            ├─ Kasir  (daftar menu + panel keranjang + Bayar)
            ├─ Riwayat ──> Detail Transaksi
            └─ Menu   ──> Tambah Menu
Logout (ikon app bar) ──> Login
```

### 10.3 Spesifikasi Layar
| Layar | Elemen utama | State |
|-------|--------------|-------|
| Login | Dropdown peran, kolom PIN, tombol Masuk | idle, error, loading |
| Kasir | Grid menu (nama + harga), panel keranjang ringkas (jumlah item + total), tombol Bayar; panel keranjang bisa dibuka penuh | menu kosong, keranjang kosong, terisi |
| Dialog AI | Judul "AI Recommendation", teks saran, tombol Lanjut Bayar / Kembali | muncul / dilewati |
| Konfirmasi Bayar | Ringkasan total, tombol Konfirmasi / Batal | idle, memproses |
| Riwayat | List transaksi | kosong, terisi |
| Kelola Menu | Form nama + harga, daftar menu dengan hapus | kosong, terisi, error validasi |

### 10.4 Wireframe Layar Kasir
```
┌──────────────────────────────┐
│ Kasir · Bertugas: Kasir  [⎋] │
├──────────────────────────────┤
│ ┌────────────┐ ┌────────────┐│
│ │ Kopi Susu  │ │ Donat      ││
│ │ Rp18.000   │ │ Rp10.000   ││
│ └────────────┘ └────────────┘│
│                              │
├──────────────────────────────┤
│ Keranjang (3)    Rp46.000    │
│ [      Bayar      ]          │
├──────────────────────────────┤
│  Kasir │ Riwayat │ Menu      │
└──────────────────────────────┘
```

### 10.5 Design Token (solid)
| Token | Nilai |
|-------|-------|
| Latar | `#FFFFFF` |
| Permukaan | `#F6F4F1` |
| Teks utama / sekunder | `#1F1B16` / `#5E564D` |
| Aksen tunggal | `#6B4423` |
| Error | `#B3261E` |
| Border | `#DAD5CE`, 1 px |
| Tipografi | Default Material; 20 (judul), 16 (isi), 24 tebal (total), 12 (keterangan) |
| Spasi | Grid 8 dp; gutter 16 dp |
| Radius | 8 dp |

### 10.6 Microcopy
- Empty menu: "Belum ada menu. Tambahkan menu pertama."
- Keranjang kosong: "Keranjang kosong."
- Sukses: "Transaksi tersimpan."
- Dialog AI: "AI menyarankan: Tawarkan Donat Cokelat seharga Rp10.000 sebagai pendamping pesanan ini!"

### 10.7 Checklist Anti "AI Slop"
- [ ] Tidak ada gradient.
- [ ] Satu warna aksen.
- [ ] Dialog AI memakai komponen dialog standar, tanpa efek berkilau atau ikon robot dekoratif.
- [ ] Tidak ada slogan atau teks promosi.

---

## 11. Release & Milestone Planning

Estimasi satu developer, hari kerja efektif. Urutan milestone = urutan prioritas di dalam Must.

| Milestone | Cakupan | Estimasi | Exit Criteria |
|-----------|---------|----------|---------------|
| M0 Setup | Proyek, struktur, tema, `ProviderScope`, lint | 0,5 hari | App kosong jalan; `analyze` bersih |
| M1 Auth | FR-P01–P03 | 0,75 hari | AC-P01 lulus |
| M2 Menu | FR-P06, P07 | 0,75 hari | AC-P02 lulus |
| M3 Keranjang & Total | FR-P10–P13 | 1 hari | AC-P03, AC-P04 lulus (20 kasus total) |
| M4 Bayar & Riwayat | FR-P16–P19, P21, P22, P24 + Mock AI (P17) | 1,5 hari | AC-P05–P07 lulus |
| M5 Hardening & Rilis | Should (P04, P08, P14, P23), usability test, bugfix, build | 1 hari | Metrik M1–M7 terpenuhi |
| **Total** | | **≈ 5,5 hari** | **Rilis v0.1.0** |

**Strategi rilis:** APK/IPA sideload untuk 5 penguji; tanpa rilis store.

**Checklist rilis v0.1.0**
- [ ] Semua Must lulus AC.
- [ ] Metrik M1–M7 tercatat.
- [ ] Uji double-tap Bayar lulus.
- [ ] Tidak ada gradient.

**Roadmap pasca-MVP**
- v0.2: uang diterima + kembalian (P20), edit menu (P09), keranjang persisten (P15).
- v0.3: laporan harian, ekspor, hak akses per peran, migrasi ke SQLite.

---

## Lampiran A: Ringkasan Arsitektur Teknis (Clean Architecture)

**Aturan dependensi:** `presentation → domain ← data`
- `domain`: Dart murni (tanpa `flutter`, `shared_preferences`, `riverpod`).
- `presentation`: hanya bergantung pada `domain`.
- `data`: mengimplementasikan interface repository.
- DI hanya lewat provider Riverpod.

```
lib/
  core/ (error/, storage/, theme/, utils/{currency_formatter,id_generator}.dart)
  features/
    auth/   domain/ (session, cashier_role, auth_repository, usecases login/logout/get_session)
            data/ (auth_local_datasource, auth_repository_impl)
            presentation/
    menu/   domain/ (menu_item, menu_repository, usecases get/add/delete)
            data/ (menu_item_model, datasource, repository_impl)
            presentation/
    cart/   domain/ (cart_item, services/cart_calculator, services/promo_suggester)
            presentation/   // tanpa layer data: keranjang hanya state di memori
    transactions/
            domain/ (transaction, transaction_item[snapshot], repository, usecases checkout/get)
            data/ (model, datasource, repository_impl)
            presentation/
```

**Kontrak inti**
```dart
class MenuItem { final String id, name; final int price; }
class CartItem { final MenuItem menuItem; final int qty; }
class TransactionItem { final String name; final int unitPrice, qty; } // snapshot
class Transaction {
  final String id; final List<TransactionItem> items;
  final int total; final CashierRole role; final DateTime createdAt;
}
class CartCalculator { int total(List<CartItem> items); }
class PromoSuggester {
  MenuItem? suggest(List<MenuItem> menu, List<CartItem> cart, {Random? random});
}
```

**Alur provider:** `sharedPreferencesProvider` → datasource → repository → usecase → notifier (`menuNotifierProvider`, `transactionsNotifierProvider`, `authNotifierProvider`). `cartNotifierProvider` (Notifier in-memory) → `cartTotalProvider` dan `promoSuggestionProvider` (provider turunan).

**Pemetaan requirement → usecase/service:** P01/P02 `Login`; P06 `AddMenu`; P13 `CartCalculator.total`; P17 `PromoSuggester.suggest`; P18/P19/P22 `Checkout`; P21 `GetTransactions`.
