# PRD: Stock Ninja

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
Stok barang di gudang kecil atau kebutuhan bulanan anak kos (sabun, mi instan) sering dicatat seadanya. Akibatnya barang habis tanpa disadari, dan baru ketahuan saat dibutuhkan.

### 1.2 Objective
Membangun MVP pencatat stok **offline** yang:
1. Hanya bisa diakses admin yang sudah login (token wajib, tanpa token selalu ke Login).
2. Mendukung tambah barang, ubah stok (tambah/kurang), dan hapus barang.
3. Menampilkan "AI Restock Predictor" (mock): kartu peringatan otomatis untuk barang dengan stok di bawah 5.

### 1.3 Hipotesis
Jika peringatan stok menipis muncul otomatis di halaman utama, admin dapat restock lebih awal tanpa harus memeriksa tiap barang.

---

## 2. Success Metrics

> Tanpa backend/analytics. Semua metrik diukur lewat skrip uji, unit test, dan usability test kecil. Target berlaku untuk v0.1.0.

| # | Tujuan | Metrik | Target | Cara Ukur |
|---|--------|--------|--------|-----------|
| M1 | Alur inti mudah | Penguji menyelesaikan login → tambah barang → ubah stok → hapus tanpa bantuan | ≥ 4 dari 5 | Usability test |
| M2 | Ubah stok cepat | Tap yang dibutuhkan untuk mengubah stok ±1 | ≤ 1 tap | Pengamatan UI |
| M3 | Peringatan akurat | Aturan stok < 5 benar pada kasus batas | 100% (stok 0, 1, 4 → peringatan; 5, 6 → tidak) | Unit test `RestockPredictor` |
| M4 | Peringatan responsif | Kartu muncul/hilang otomatis setelah stok berubah | ≤ 100 ms, tanpa refresh manual | Widget test |
| M5 | Akses terkunci | Akses halaman stok tanpa token | 0 kasus lolos | Widget test route guard |
| M6 | Data bertahan | Barang dan sesi utuh setelah force-close | 100% pada 3 percobaan | Uji manual |
| M7 | Kualitas teknis | `flutter analyze` / cakupan domain / start dingin | 0 isu / ≥ 80% / ≤ 2 dtk | `flutter test --coverage`, DevTools |

**Counter-metric:** stok tidak pernah bernilai negatif dalam kondisi apa pun.

---

## 3. Target Audience & Personas

### Persona Utama: Pak Hendra (35), admin gudang toko kelontong
- **Konteks:** mencatat barang masuk/keluar; sering berpindah antar rak sambil memegang ponsel.
- **Tujuan:** tahu barang mana yang hampir habis tanpa menghitung ulang semua.
- **Frustrasi:** catatan kertas hilang atau tidak update; baru sadar kehabisan saat pelanggan menanyakan.
- **Perilaku:** mengubah stok berkali-kali sehari; butuh +/− cepat.
- **Kutipan:** "Kasih tahu saja mana yang mau habis, saya yang belanja."

### Persona Sekunder: Salsa (20), anak kos
Memakai aplikasi untuk stok bulanan (sabun, mi instan). Alur sama, skala kecil.

### Stakeholder: Developer/Reviewer
Menilai arsitektur, Riverpod, route guard, dan logika peringatan yang terpisah dari UI.

---

## 4. Functional Requirements (MoSCoW)

**Aturan prioritisasi**
- **Must:** tanpa ini journey utama gagal, atau ada risiko data stok salah/akses tak sah. Blocker rilis.
- **Should:** penting tetapi ada workaround; masuk v0.1.0 jika jadwal cukup, jika tidak ke v0.2.
- **Could:** nilai tambah kecil; default v0.2+.
- **Won't (rilis ini):** disepakati tidak dikerjakan sekarang.
- Must tidak melebihi sekitar 60% dari total effort.

**Keputusan desain:** ambang stok menipis **tetap 5** dan berlaku untuk semua barang; stok adalah integer ≥ 0 dengan batas atas 99.999.

| ID | Requirement | Prioritas | Catatan / Alasan | Story |
|----|-------------|-----------|------------------|-------|
| **Autentikasi** | | | | |
| FR-S01 | Login Admin Gudang: Username + Password (konstanta `admin` / `admin123`) | **Must** | Syarat skenario auth | US-S01 |
| FR-S02 | Simpan `admin_token` ke SharedPreferences | **Must** | Syarat skenario auth | US-S01 |
| FR-S03 | **Route guard:** tanpa token, semua halaman selain Login dialihkan ke Login | **Must** | Syarat eksplisit brief | US-S02 |
| FR-S04 | Logout menghapus token → otomatis ke Login | **Must** | Siklus sesi lengkap | US-S02 |
| FR-S05 | Ganti password, multi-admin | Won't | Auth demo lokal | - |
| **Barang** | | | | |
| FR-S06 | Tambah barang (nama wajib, stok awal integer 0–99.999) | **Must** | Inti produk | US-S03 |
| FR-S07 | Daftar barang (nama + stok) dengan empty state | **Must** | Inti produk | US-S04 |
| FR-S08 | Ubah stok dengan tombol + dan −; stok tidak boleh < 0 | **Must** | Inti produk | US-S05 |
| FR-S09 | Hapus barang dengan konfirmasi | **Must** | Hapus tidak bisa dibatalkan | US-S06 |
| FR-S10 | Set jumlah stok langsung via dialog angka | Should | Berguna saat stok opname | US-S05 |
| FR-S11 | Cegah nama barang duplikat (tidak peka huruf besar/kecil, trim) | Should | Hindari data ganda | US-S03 |
| FR-S12 | Penanda teks "Menipis" pada barang dengan stok < 5 (bukan hanya warna) | Should | Aksesibilitas | US-S07 |
| FR-S13 | Urutkan barang menipis di atas | Could | Memudahkan fokus | US-S07 |
| **Mock AI Restock** | | | | |
| FR-S14 | Kartu peringatan otomatis untuk setiap barang dengan stok < 5, di atas daftar, update real-time | **Must** | Pembeda produk, syarat brief | US-S07 |
| FR-S15 | Template teks utama: "AI mendeteksi krisis {nama}! Sisa stok: {n}. Segera pergi ke minimarket sebelum kelaparan." | **Must** | Syarat brief | US-S07 |
| FR-S16 | Template khusus stok 0: "AI mendeteksi {nama} HABIS! Segera restock." | Should | Membedakan urgensi | US-S07 |
| FR-S17 | Kartu hilang saat tidak ada barang menipis | **Must** | Hindari kartu kosong | US-S07 |
| FR-S18 | Riwayat mutasi, kategori/satuan, barcode, ambang yang bisa diatur, notifikasi push, ekspor | Won't | Di luar MVP | - |

---

## 5. Critical User Journeys & User Stories

### 5.1 Critical User Journeys

**CUJ-1: Menyiapkan stok dan melihat peringatan pertama** (journey utama, M1)
1. Buka aplikasi → Login → `admin` / `admin123` → Masuk.
2. Empty state → tambah "Mie Instan" stok 8, "Sabun" stok 3.
3. Daftar tampil; kartu peringatan muncul untuk Sabun: "AI mendeteksi krisis Sabun! Sisa stok: 3. …"
4. Tap + pada Sabun sampai stok 5 → kartu Sabun hilang.
5. *Jalur gagal:* nama kosong → pesan validasi.

**CUJ-2: Pemakaian harian**
1. Tap − pada Mie Instan → stok 7, 6, 5, 4 → kartu peringatan Mie Instan muncul saat stok 4.
2. Stok 0: tombol − nonaktif; pesan "HABIS" (Should).

**CUJ-3: Akses tanpa sesi**
1. Token terhapus (logout) → aplikasi selalu menampilkan Login, back tidak membuka halaman stok.

### 5.2 User Stories

| ID | Story | FR |
|----|-------|----|
| US-S01 | Sebagai admin gudang, saya ingin login dan sesi saya tersimpan, agar tidak mengulang login. | S01, S02 |
| US-S02 | Sebagai admin, saya ingin halaman stok tidak bisa dibuka tanpa login, dan bisa logout, agar data aman. | S03, S04 |
| US-S03 | Sebagai admin, saya ingin menambah barang baru tanpa duplikat, agar data bersih. | S06, S11 |
| US-S04 | Sebagai admin, saya ingin melihat semua barang beserta stoknya, agar tahu kondisi gudang. | S07 |
| US-S05 | Sebagai admin, saya ingin menambah atau mengurangi stok dengan cepat, agar pencatatan sesuai kondisi nyata. | S08, S10 |
| US-S06 | Sebagai admin, saya ingin menghapus barang yang sudah tidak dijual, agar daftar relevan. | S09 |
| US-S07 | Sebagai admin, saya ingin diperingatkan otomatis saat stok menipis, agar bisa restock sebelum habis. | S12–S17 |

---

## 6. Acceptance Criteria

**AC-S01 Login & token (FR-S01, S02)**
- Given belum login, When `admin` / `admin123` lalu Masuk, Then `admin_token` tersimpan dan Daftar Stok tampil.
- Given kredensial salah atau kolom kosong, Then muncul pesan error dan tidak ada token tersimpan.

**AC-S02 Route guard & logout (FR-S03, S04)**
- Given tidak ada token, When aplikasi dibuka atau route lain diminta, Then Login tampil.
- Given sudah login, When force-close lalu buka kembali, Then langsung ke Daftar Stok.
- Given tap Logout, Then token terhapus, Login tampil, dan back tidak membuka halaman stok.

**AC-S03 Tambah barang (FR-S06, S11)**
- Given nama kosong atau stok bukan integer 0–99.999, Then muncul validasi dan barang tidak tersimpan.
- Given nama valid dan stok valid, Then barang muncul di daftar dan bertahan setelah restart.
- Given nama sudah ada ("mie instan" vs "Mie Instan"), Then muncul "Barang sudah ada" (Should).

**AC-S04 Daftar (FR-S07, S12)**
- Given belum ada barang, Then empty state dengan tombol "Tambah barang".
- Given stok < 5, Then baris diberi teks "Menipis".

**AC-S05 Ubah stok (FR-S08, S10)**
- Given tap +, Then stok bertambah 1 dan tersimpan.
- Given tap −, Then stok berkurang 1; pada stok 0 tombol − nonaktif dan stok tidak pernah negatif.
- Given dialog angka diisi 12 (Should), Then stok menjadi 12; input negatif ditolak.

**AC-S06 Hapus (FR-S09)**
- Given tap hapus, Then dialog "Hapus {nama}?" dengan Batal dan Hapus.
- Given Batal, Then barang tetap ada. Given Hapus, Then barang hilang dari daftar dan storage.

**AC-S07 Mock AI Restock Predictor (FR-S14–S17)**
- Barang menipis = `stok < 5`.

| Stok | Kartu peringatan | Teks |
|------|------------------|------|
| 6 | Tidak | - |
| 5 | Tidak | - |
| 4 | Ya | "AI mendeteksi krisis Mie Instan! Sisa stok: 4. Segera pergi ke minimarket sebelum kelaparan." |
| 2 | Ya | "… Sisa stok: 2. …" |
| 0 | Ya | "AI mendeteksi Mie Instan HABIS! Segera restock." (Should; jika belum, memakai teks utama) |
- Satu kartu per barang menipis, di atas daftar.
- Given stok berubah, Then kartu muncul/hilang otomatis tanpa refresh manual.
- Given tidak ada barang menipis, Then area kartu tidak tampil.
- Kartu memakai warna solid (border + latar polos), tanpa gradient.

---

## 7. Out of Scope

- Riwayat mutasi stok, laporan, ekspor.
- Satuan, kategori, barcode/scan, foto barang.
- Ambang stok yang bisa diatur per barang.
- Notifikasi push, widget layar utama.
- Multi-admin, ganti password, sinkronisasi cloud.
- AI sungguhan atau prediksi berbasis tren pemakaian.

---

## 8. Non-Functional Requirements

| Kategori | Requirement | Target | Verifikasi |
|----------|-------------|--------|------------|
| Performa | Start dingin | ≤ 2 detik | DevTools |
| Performa | Tap +/− → UI dan kartu ter-update | ≤ 100 ms | Widget test / manual |
| Performa | 1.000 barang | Scroll ≥ 55 fps | DevTools |
| Keandalan | Data dan sesi bertahan setelah force-close | 100% | Uji manual |
| Keandalan | Stok tidak pernah negatif | 100% | Unit test `AdjustStock` |
| Keandalan | JSON rusak | Tidak crash; daftar kosong + pesan | Unit test datasource |
| Keamanan & privasi | Data lokal; tanpa permission INTERNET; tanpa log kredensial | Terpenuhi | Cek manifest, review |
| Keamanan | Route guard berbasis state; kredensial konstanta bukan batas keamanan nyata | Didokumentasikan | Widget test + review |
| Aksesibilitas | Target sentuh ≥ 48 dp; kontras ≥ 4,5:1; teks 1,5× tanpa overflow; status "Menipis" tidak hanya lewat warna; tombol ± berlabel semantik | Terpenuhi | Uji manual |
| Kompatibilitas | Android API 24+, iOS 13+; potret; ≥ 360 dp | Terpenuhi | Emulator |
| Lokalisasi | Bahasa Indonesia | Terpenuhi | Review |
| Maintainability | `analyze` 0 isu; aturan layer ditaati | Terpenuhi | Lint + review |
| Testabilitas | Cakupan `domain` ≥ 80% | ≥ 80% | `flutter test --coverage` |

---

## 9. Dependencies, Assumptions & Risks

### 9.1 Dependencies
| Jenis | Item | Keterangan |
|-------|------|------------|
| Paket runtime | `flutter_riverpod`, `shared_preferences` | State dan penyimpanan |
| Paket dev | `flutter_test`, `mocktail`, `flutter_lints` | Pengujian dan lint |
| Layanan eksternal | Tidak ada | Offline penuh |

### 9.2 Assumptions
- A1: Satu admin, satu perangkat.
- A2: Kredensial tetap (`admin` / `admin123`); autentikasi demo.
- A3: Stok bilangan bulat tanpa satuan.
- A4: Ambang "menipis" berlaku sama untuk semua barang.
- A5: Perubahan stok tidak dicatat sebagai riwayat.

### 9.3 Risks
| ID | Risiko | Peluang | Dampak | Mitigasi |
|----|--------|---------|--------|----------|
| R1 | Ambang 5 tidak cocok untuk semua barang (mis. beras vs sabun) | Tinggi | Sedang | Diterima di MVP; ambang per barang di roadmap v0.2 |
| R2 | Tanpa riwayat mutasi, salah ketuk tidak bisa ditelusuri | Sedang | Sedang | Dicatat sebagai keterbatasan; riwayat di v0.3 |
| R3 | Route guard bocor lewat navigasi back/deep link | Rendah | Tinggi | Guard di level root berbasis `authNotifierProvider`; widget test M5 |
| R4 | Nama duplikat membuat data ganda | Sedang | Rendah | FR-S11 (Should) |
| R5 | Teks "sebelum kelaparan" kurang cocok untuk barang non-makanan | Sedang | Rendah | Diterima karena teks mengikuti brief; opsi: template netral di v0.2 |
| R6 | SharedPreferences kurang cocok untuk data besar | Sedang | Sedang | Repository abstrak; migrasi ke SQLite saat perlu |
| R7 | Scope creep (kategori, satuan) | Sedang | Sedang | Daftar Won't dibekukan |

### 9.4 Pertanyaan Terbuka
- Haruskah daftar otomatis diurutkan menipis dahulu? (default MVP: urutan input; FR-S13 Could)

---

## 10. Design & UX

### 10.1 Prinsip
- Peringatan terlihat tanpa scroll; kartu selalu di atas daftar.
- Ubah stok sekali tap; tombol ± besar.
- Warna **solid**, **tanpa gradient**, tanpa glassmorphism/neon/shadow berlebihan. Status tidak bergantung pada warna saja.

### 10.2 Peta Navigasi
```
(tanpa token) ──> Login ──(sukses)──> Daftar Stok ──> Tambah Barang ──> Daftar Stok
                                          │
Logout (ikon app bar) ────────────────────┘──> Login
```

### 10.3 Spesifikasi Layar
| Layar | Elemen utama | State |
|-------|--------------|-------|
| Login | Judul, kolom Username, kolom Password, tombol Masuk, teks error | idle, error validasi, error kredensial, loading |
| Daftar Stok | Kartu peringatan (0..n), daftar `StockTile` (nama, stok, −, +, hapus), FAB tambah | loading, empty, terisi, ada peringatan |
| Tambah Barang | Kolom nama, kolom stok awal, tombol Simpan | idle, error validasi, duplikat |
| Dialog Hapus | Teks konfirmasi, Batal / Hapus | muncul |

### 10.4 Wireframe Daftar Stok
```
┌──────────────────────────────┐
│ Stok Gudang            [⎋]   │
├──────────────────────────────┤
│ ┌──────────────────────────┐ │
│ │ AI mendeteksi krisis Mie │ │
│ │ Instan! Sisa stok: 2.    │ │
│ │ Segera pergi ke ...      │ │
│ └──────────────────────────┘ │
├──────────────────────────────┤
│ Mie Instan  · Menipis        │
│   [−]   2   [+]        [🗑]  │
├──────────────────────────────┤
│ Sabun                        │
│   [−]   8   [+]        [🗑]  │
│                       [ + ]  │
└──────────────────────────────┘
```

### 10.5 Design Token (solid)
| Token | Nilai |
|-------|-------|
| Latar | `#FFFFFF` |
| Permukaan | `#F4F5F2` |
| Teks utama / sekunder | `#1B1C1A` / `#5A5D55` |
| Aksen tunggal | `#1F6F5B` |
| Peringatan (border kartu / teks) | `#B3261E` |
| Latar kartu peringatan | `#FDECEA` (solid) |
| Border | `#D8DAD3`, 1 px |
| Tipografi | Default Material; 20 / 16 / 12; stok 20 tebal |
| Spasi | Grid 8 dp; gutter 16 dp |
| Radius | 8 dp |

### 10.6 Microcopy
- Empty: "Belum ada barang. Tambahkan barang pertama."
- Duplikat: "Barang sudah ada."
- Hapus: "Hapus {nama}? Tindakan ini tidak bisa dibatalkan."

### 10.7 Checklist Anti "AI Slop"
- [ ] Tidak ada gradient (termasuk pada kartu peringatan).
- [ ] Satu aksen + satu warna peringatan solid.
- [ ] Kartu "AI" memakai komponen Card standar, tanpa ikon robot atau efek berkilau.
- [ ] Teks peringatan mengikuti template; tidak ada slogan tambahan.

---

## 11. Release & Milestone Planning

Estimasi satu developer, hari kerja efektif. Urutan milestone = urutan prioritas di dalam Must.

| Milestone | Cakupan | Estimasi | Exit Criteria |
|-----------|---------|----------|---------------|
| M0 Setup | Proyek, struktur, tema, `ProviderScope`, lint | 0,5 hari | App kosong jalan; `analyze` bersih |
| M1 Auth & Guard | FR-S01–S04 | 1 hari | AC-S01, AC-S02 lulus; widget test guard lulus |
| M2 Barang | FR-S06–S09 | 1,5 hari | AC-S03–S06 lulus |
| M3 Restock Predictor | FR-S14, S15, S17 | 0,75 hari | AC-S07 lulus (kasus batas 0, 4, 5) |
| M4 Hardening & Rilis | Should (S10, S11, S12, S16), usability test, bugfix, build | 1 hari | Metrik M1–M7 terpenuhi |
| **Total** | | **≈ 4,75 hari** | **Rilis v0.1.0** |

**Strategi rilis:** APK/IPA sideload untuk 5 penguji; tanpa rilis store.

**Checklist rilis v0.1.0**
- [ ] Semua Must lulus AC.
- [ ] Metrik M1–M7 tercatat.
- [ ] Uji batas stok (0, 4, 5) lulus.
- [ ] Tidak ada gradient.

**Roadmap pasca-MVP**
- v0.2: urut menipis di atas (S13), ambang per barang, template peringatan netral.
- v0.3: riwayat mutasi, satuan/kategori, ekspor.

---

## Lampiran A: Ringkasan Arsitektur Teknis (Clean Architecture)

**Aturan dependensi:** `presentation → domain ← data`
- `domain`: Dart murni (tanpa `flutter`, `shared_preferences`, `riverpod`).
- `presentation`: hanya bergantung pada `domain`.
- `data`: mengimplementasikan interface repository.
- DI hanya lewat provider Riverpod.

```
lib/
  main.dart            // route guard dari authNotifierProvider
  core/ (error/, storage/, theme/, utils/)
  features/
    auth/   domain/ (session, auth_repository, usecases login/logout/get_session)
            data/ (auth_local_datasource, auth_repository_impl)
            presentation/ (login_screen, providers)
    stock/  domain/ (stock_item, stock_repository, services/restock_predictor,
                     usecases get/add/adjust/set_quantity/delete)
            data/ (stock_item_model, stock_local_datasource, stock_repository_impl)
            presentation/ (stock_list_screen, add_item_screen,
                           widgets/{stock_tile,restock_alert_card}, providers)
```

**Kontrak inti**
```dart
class StockItem { final String id, name; final int quantity; }
abstract class StockRepository {
  Future<List<StockItem>> getItems();
  Future<void> saveItems(List<StockItem> items);
}
class RestockPredictor {
  static const threshold = 5;
  List<StockItem> lowStock(List<StockItem> items); // quantity < threshold
  String message(StockItem item);
}
```

**Alur provider:** `sharedPreferencesProvider` → datasource → repository → usecase → `stockNotifierProvider` (AsyncNotifier). `lowStockProvider` = turunan dari `stockNotifierProvider` lewat `RestockPredictor`, sehingga kartu otomatis ter-update. `authNotifierProvider` memutuskan Login vs Daftar Stok (route guard).

**Pemetaan requirement → usecase/service:** S01/S02 `Login`; S03 `GetSession` + guard; S04 `Logout`; S06/S11 `AddItem`; S08 `AdjustStock`; S10 `SetQuantity`; S09 `DeleteItem`; S14–S17 `RestockPredictor`.
