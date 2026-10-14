# PRD: Secret Diary

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
Orang yang menulis jurnal pribadi di ponsel sering khawatir tulisannya terbaca orang lain, misalnya teman yang meminjam ponsel atau teman sekamar kos. Aplikasi catatan bawaan tidak punya gerbang akses khusus, sedangkan aplikasi jurnal populer terlalu rumit untuk sekadar menulis cepat.

### 1.2 Objective
Membangun MVP jurnal harian **offline** yang:
1. Hanya bisa diakses setelah login Username + PIN.
2. Mendukung menulis, membaca, dan menghapus catatan.
3. Memberi "Mock AI Mood Scanner" yang menambahkan emoji mood pada judul secara otomatis, tanpa AI sungguhan.

### 1.3 Hipotesis
Jika pengguna bisa login, menulis catatan pertama, dan melihatnya kembali dalam kurang dari 1 menit, maka alur inti sudah cukup sederhana untuk dipakai harian. Emoji mood otomatis menambah nilai tanpa langkah ekstra.

---

## 2. Success Metrics

> Aplikasi tidak memakai backend atau analytics. Semua metrik diukur lewat skrip uji manual, widget/unit test, dan DevTools. Target ini berlaku untuk rilis v0.1.0.

| # | Tujuan | Metrik | Target | Cara Ukur |
|---|--------|--------|--------|-----------|
| M1 | Alur inti mudah | Penguji menyelesaikan journey login → tulis → baca → hapus tanpa bantuan | ≥ 4 dari 5 penguji | Usability test 5 orang dengan skrip tertulis |
| M2 | Aktivasi cepat | Waktu dari layar Login sukses sampai catatan pertama tersimpan | ≤ 60 detik (median) | Stopwatch pada usability test |
| M3 | Akses terkunci | Akses ke daftar catatan tanpa token | 0 kasus lolos | Widget test route guard |
| M4 | Mood akurat sesuai aturan | Test case tabel mood lulus | 100% (≥ 12 kasus) | Unit test `MoodScanner` |
| M5 | Data tidak hilang | Catatan dan sesi utuh setelah force-close | 100% pada 3 kali percobaan | Skrip uji manual |
| M6 | Kualitas teknis | `flutter analyze` / cakupan domain / start dingin | 0 isu / ≥ 80% / ≤ 2 dtk | CI lokal, `flutter test --coverage`, DevTools profile mode |
| M7 | Stabil | Crash dalam sesi eksplorasi 30 menit | 0 | Sesi uji manual |

**Counter-metric (jangan dikorbankan):** kecepatan menulis tidak boleh turun karena validasi atau animasi. Dari tap "Tulis" sampai kolom judul fokus ≤ 1 detik.

---

## 3. Target Audience & Personas

### Persona Utama: Rani (21), mahasiswi dan anak kos
- **Konteks:** berbagi ruang dengan teman kos; sering meminjamkan ponsel untuk hal sepele.
- **Tujuan:** menulis curhat singkat malam hari tanpa ribet; yakin tulisannya tidak terbaca sembarang orang.
- **Frustrasi:** aplikasi catatan biasa terbuka bagi siapa saja; aplikasi jurnal besar penuh fitur yang tidak ia butuhkan.
- **Perilaku:** menulis 1–2 kali sehari, 3–10 kalimat, tidak peduli fitur lanjutan.
- **Kutipan:** "Aku cuma mau nulis, terus yakin nggak ada yang bisa buka."

### Stakeholder Sekunder: Developer/Reviewer
Mengevaluasi kebersihan arsitektur, penggunaan Riverpod, dan kemudahan pengujian. Tidak memakai aplikasi sebagai pengguna akhir.

**Di luar target MVP:** pengguna yang butuh enkripsi sungguhan atau sinkronisasi antar perangkat.

---

## 4. Functional Requirements (MoSCoW)

**Aturan prioritisasi yang dipakai**
- **Must:** tanpa ini journey utama gagal, atau ada risiko kehilangan data/keamanan dasar. Blocker rilis.
- **Should:** penting tetapi ada workaround; dikerjakan di v0.1.0 jika jadwal cukup, jika tidak masuk v0.2.
- **Could:** nilai tambah kecil, dikerjakan hanya jika ada sisa waktu; default v0.2+.
- **Won't (rilis ini):** disepakati tidak dikerjakan sekarang. Bukan berarti tidak akan pernah.
- Batas sehat: Must tidak melebihi sekitar 60% dari total effort agar ada ruang cadangan.

| ID | Requirement | Prioritas | Catatan / Alasan | Story |
|----|-------------|-----------|------------------|-------|
| **Autentikasi** | | | | |
| FR-D01 | Login dengan Username + PIN 4 digit (kredensial konstanta `admin` / `1234`) | **Must** | Pintu masuk seluruh aplikasi | US-D01 |
| FR-D02 | Validasi input; pesan error generik "Username atau PIN salah" (tidak menyebut kolom mana yang salah) | **Must** | Praktik keamanan dasar | US-D01 |
| FR-D03 | Simpan `auth_token` di SharedPreferences; auto-login saat aplikasi dibuka ulang | **Must** | Syarat skenario auth | US-D02 |
| FR-D04 | Logout menghapus token dan kembali ke Login | **Must** | Siklus sesi harus lengkap | US-D03 |
| FR-D05 | Kunci sementara 30 detik setelah 5 kali PIN salah | Could | PIN 4 digit mudah ditebak; nilai terbatas karena data tidak terenkripsi | US-D01 |
| **Catatan** | | | | |
| FR-D06 | Tulis catatan baru (judul + isi, keduanya wajib) | **Must** | Inti produk | US-D04 |
| FR-D07 | Daftar catatan, terbaru di atas; tampil judul, tanggal, cuplikan isi 2 baris | **Must** | Inti produk | US-D05 |
| FR-D08 | Halaman detail catatan | **Must** | Membaca penuh | US-D05 |
| FR-D09 | Hapus catatan dengan dialog konfirmasi | **Must** | Hapus tidak bisa dibatalkan → konfirmasi wajib | US-D06 |
| FR-D10 | Empty state pada daftar catatan (ikon, teks, tombol "Tulis catatan") | **Must** | Aplikasi mulai tanpa data | US-D05 |
| FR-D11 | Mock AI Mood Scanner (aturan di bagian 6) | **Must** | Pembeda produk dan syarat brief | US-D07 |
| FR-D12 | Batas panjang: judul ≤ 80, isi ≤ 5.000 karakter, dengan penghitung | Should | Mencegah data membengkak di SharedPreferences | US-D04 |
| FR-D13 | Umpan balik "Catatan disimpan" via Snackbar | Should | Konfirmasi aksi | US-D04 |
| FR-D14 | Simpan draft otomatis jika form ditutup sebelum disimpan | Could | Mencegah tulisan hilang | US-D04 |
| FR-D15 | Tema gelap | Could | Kenyamanan malam hari | - |
| FR-D16 | Edit catatan | Won't | Di luar CRUD yang diminta (tulis, baca, hapus) | - |
| FR-D17 | Pencarian catatan | Won't | Belum dibutuhkan pada volume kecil | - |
| FR-D18 | Ganti PIN / registrasi akun | Won't | Auth hanya demo lokal | - |
| FR-D19 | Biometrik | Won't | Butuh plugin dan pengujian perangkat | - |
| FR-D20 | Enkripsi catatan at-rest | Won't | Lihat risiko R1; prioritas pertama pasca-MVP | - |
| FR-D21 | Penanganan negasi pada Mood Scanner ("tidak senang") | Won't | Batasan mock yang disetujui (R3) | - |

---

## 5. Critical User Journeys & User Stories

### 5.1 Critical User Journeys

**CUJ-1: Pertama kali menulis catatan** (journey utama, ukuran M1 dan M2)
1. Pengguna membuka aplikasi → Login.
2. Mengisi `admin` + `1234` → tap Masuk.
3. Melihat empty state → tap "Tulis catatan".
4. Mengisi judul dan isi (mis. "Hari ini aku senang sekali") → tap Simpan.
5. Kembali ke daftar; judul tampil `😄 …`.
6. *Jalur gagal:* PIN salah → error generik, form tetap terisi username, PIN dikosongkan.

**CUJ-2: Kembali membaca** 
1. Buka aplikasi → langsung ke daftar (token ada).
2. Tap catatan → detail.

**CUJ-3: Hapus dan keluar**
1. Dari detail → tap hapus → dialog konfirmasi → Hapus.
2. Kembali ke daftar tanpa catatan itu.
3. Tap Logout → Login; tombol back tidak bisa kembali ke daftar.

### 5.2 User Stories

| ID | Story | FR |
|----|-------|----|
| US-D01 | Sebagai pemilik jurnal, saya ingin masuk dengan username dan PIN, agar orang lain tidak bisa membuka catatan saya. | D01, D02, D05 |
| US-D02 | Sebagai pemilik, saya ingin tetap login setelah menutup aplikasi, agar tidak mengetik PIN setiap kali. | D03 |
| US-D03 | Sebagai pemilik, saya ingin keluar dari akun, agar ponsel aman saat dipinjamkan. | D04 |
| US-D04 | Sebagai pemilik, saya ingin menulis catatan dengan cepat, agar kebiasaan menulis tidak terganggu. | D06, D12, D13, D14 |
| US-D05 | Sebagai pemilik, saya ingin melihat daftar dan isi catatan, agar bisa mengingat kembali kejadian lama. | D07, D08, D10 |
| US-D06 | Sebagai pemilik, saya ingin menghapus catatan dengan aman, agar tidak terhapus karena salah tap. | D09 |
| US-D07 | Sebagai pemilik, saya ingin judul diberi emoji mood otomatis, agar suasana hati terlihat sekilas di daftar. | D11 |

---

## 6. Acceptance Criteria

Format: Given / When / Then.

**AC-D01 Login berhasil (FR-D01, D03)**
- Given belum ada token, When pengguna memasukkan `admin` dan `1234` lalu tap Masuk, Then `auth_token` tersimpan di SharedPreferences dan pengguna masuk ke Daftar Catatan.

**AC-D02 Login gagal (FR-D02)**
- Given kredensial salah (username atau PIN), When tap Masuk, Then muncul "Username atau PIN salah", tidak ada token tersimpan, dan PIN dikosongkan.
- Given kolom kosong atau PIN bukan 4 digit angka, When tap Masuk, Then muncul pesan validasi per kolom dan tidak ada pengecekan kredensial.

**AC-D03 Sesi bertahan (FR-D03)**
- Given sudah login, When aplikasi di-force-close lalu dibuka, Then pengguna langsung ke Daftar Catatan tanpa melihat Login (kecuali kilasan loading ≤ 500 ms).

**AC-D04 Logout (FR-D04)**
- Given sudah login, When tap Logout, Then token terhapus, layar Login tampil, dan tombol back tidak membuka Daftar Catatan.

**AC-D05 Tulis catatan (FR-D06, D12)**
- Given form kosong, When tap Simpan, Then kedua kolom menampilkan "Wajib diisi" dan tidak ada catatan baru.
- Given judul dan isi valid, When tap Simpan, Then catatan tersimpan dengan id unik dan `createdAt` saat ini, dan pengguna kembali ke daftar.
- Given judul lebih dari 80 karakter, Then input tidak menerima karakter berikutnya (Should).

**AC-D06 Daftar (FR-D07, D10)**
- Given ada beberapa catatan, Then urutan dari `createdAt` terbaru ke terlama.
- Given belum ada catatan, Then empty state dan tombol "Tulis catatan" tampil.

**AC-D07 Detail (FR-D08)**
- Given tap sebuah catatan, Then detail menampilkan judul lengkap, tanggal-waktu, dan isi penuh dengan teks yang bisa digulir.

**AC-D08 Hapus (FR-D09)**
- Given tap hapus, Then dialog "Hapus catatan ini?" dengan tombol Batal dan Hapus.
- Given tap Batal, Then catatan tetap ada. Given tap Hapus, Then catatan hilang dari daftar dan dari SharedPreferences.

**AC-D09 Mock AI Mood Scanner (FR-D11)**
Teks diperiksa = judul + isi, huruf kecil. Aturan if-else berurutan:
1. Mengandung `senang` atau `bahagia` → awalan `😄 ` pada judul.
2. Else mengandung `sedih` atau `marah` → awalan `😢 `.
3. Else → judul tidak berubah.

| # | Judul | Isi | Hasil judul |
|---|-------|-----|-------------|
| 1 | Hari ini | Aku senang | 😄 Hari ini |
| 2 | Hari ini | Aku BAHAGIA | 😄 Hari ini |
| 3 | Senang | biasa | 😄 Senang |
| 4 | Kabar | Aku sedih | 😢 Kabar |
| 5 | Kabar | Dia marah | 😢 Kabar |
| 6 | Marah | biasa | 😢 Marah |
| 7 | Hari ini | senang tapi sedih | 😄 Hari ini |
| 8 | Hari ini | marah lalu bahagia | 😄 Hari ini |
| 9 | Hari ini | biasa saja | Hari ini |
| 10 | Hari ini | kesenangan | 😄 Hari ini |
| 11 | Hari ini | (isi lain) tanpa kata kunci | Hari ini |
| 12 | 😄 Sudah | senang | 😄 Sudah (tidak ganda) |

- Emoji disimpan bersama judul di data, bukan hanya tampilan.
- Baris 10 (substring) dan keterbatasan negasi ("tidak senang" → 😄) adalah **perilaku yang diketahui dan disetujui** untuk mock ini.

---

## 7. Out of Scope

Tidak dikerjakan pada v0.1.0 (lihat tabel Won't di bagian 4):
- Edit catatan, pencarian, kategori/tag, lampiran foto.
- Ganti PIN, registrasi, lupa PIN, multi-akun.
- Biometrik, enkripsi at-rest, backup/ekspor, sinkronisasi cloud.
- Analisis sentimen sungguhan, penanganan negasi, bahasa selain Indonesia.
- Notifikasi pengingat menulis.

---

## 8. Non-Functional Requirements

| Kategori | Requirement | Target | Verifikasi |
|----------|-------------|--------|------------|
| Performa | Start dingin | ≤ 2 detik (perangkat menengah, profile mode) | DevTools |
| Performa | Scroll daftar 500 catatan | ≥ 55 fps, tanpa jank terlihat | DevTools |
| Performa | Simpan/hapus catatan | ≤ 200 ms | Pengukuran lokal |
| Keandalan | Data bertahan setelah force-close | 100% | Uji manual |
| Keandalan | JSON rusak di storage | Tidak crash; tampil daftar kosong + pesan error | Unit test datasource |
| Keamanan & privasi | Data hanya di perangkat; tanpa permission INTERNET pada rilis | Terpenuhi | Cek manifest |
| Keamanan & privasi | Tidak ada log berisi PIN atau isi catatan | Terpenuhi | Code review |
| Keamanan & privasi | Pesan tidak mengklaim "terenkripsi" | Terpenuhi | Review copy |
| Aksesibilitas | Target sentuh ≥ 48 dp; kontras teks ≥ 4,5:1; teks skala 1,5× tanpa overflow; label semantik pada ikon | Terpenuhi | Uji manual + Flutter semantics |
| Kompatibilitas | Android API 24+, iOS 13+; potret; lebar ≥ 360 dp | Terpenuhi | Uji emulator |
| Lokalisasi | Bahasa Indonesia; tanggal `13 Okt 2026, 17.33` | Terpenuhi | Review |
| Maintainability | `flutter analyze` 0 isu; tidak ada impor `flutter`/`data` yang melanggar aturan layer | Terpenuhi | Lint + review |
| Testabilitas | Cakupan `domain` ≥ 80% | ≥ 80% | `flutter test --coverage` |

---

## 9. Dependencies, Assumptions & Risks

### 9.1 Dependencies
| Jenis | Item | Keterangan |
|-------|------|------------|
| Paket runtime | `flutter_riverpod`, `shared_preferences`, `intl` | State, penyimpanan, format tanggal |
| Paket dev | `flutter_test`, `mocktail`, `flutter_lints` | Pengujian dan lint |
| Layanan eksternal | Tidak ada | Offline penuh |
| Tim/aset | Tidak ada desainer; UI mengikuti spesifikasi bagian 10 | |

### 9.2 Assumptions
- A1: Satu pengguna, satu perangkat.
- A2: Kredensial tetap (`admin`/`1234`); ini autentikasi demo, bukan batas keamanan.
- A3: Perangkat tidak di-root dan pengguna tidak membuka storage aplikasi.
- A4: Teks catatan hanya plain text, bahasa Indonesia.
- A5: Kehilangan data karena uninstall atau clear data dapat diterima pada MVP.

### 9.3 Risks
| ID | Risiko | Peluang | Dampak | Mitigasi |
|----|--------|---------|--------|----------|
| R1 | Nama "Secret" menyiratkan keamanan, padahal catatan tersimpan sebagai teks biasa di SharedPreferences | Tinggi | Tinggi | Jangan klaim enkripsi di UI; jadikan FR-D20 prioritas pertama v0.2 (kunci di `flutter_secure_storage` + penyimpanan terenkripsi) |
| R2 | PIN di-hardcode dan 4 digit mudah ditebak | Tinggi | Rendah (MVP) | Dilabeli autentikasi demo; FR-D05 sebagai pengaman ringan |
| R3 | Scanner salah pada negasi/substring ("tidak senang" → 😄) | Tinggi | Rendah | Perilaku didokumentasikan di AC-D09; FR-D21 ditunda |
| R4 | Semua catatan dalam satu string JSON bisa lambat bila jumlahnya besar | Sedang | Sedang | Batas panjang (FR-D12); repository abstrak memudahkan ganti ke SQLite/Isar |
| R5 | Scope creep (edit, pencarian) | Sedang | Sedang | Daftar Won't dibekukan; permintaan baru masuk backlog v0.2 |
| R6 | Clean Architecture terasa berat untuk aplikasi kecil | Sedang | Rendah | Usecase dijaga tipis; biaya diterima karena tujuan juga latihan arsitektur |
| R7 | Data hilang saat uninstall/clear data | Tinggi | Sedang | Diterima di MVP; backup/ekspor di roadmap |

### 9.4 Pertanyaan Terbuka
- Perlukah catatan diberi batas jumlah total? (default: tidak)
- Haruskah emoji bisa dimatikan? (default: tidak untuk MVP)

---

## 10. Design & UX

### 10.1 Prinsip
- Cepat menulis: sedikit langkah, keyboard langsung muncul.
- Tenang dan polos: warna **solid**, **tanpa gradient**, tanpa glassmorphism/neon/shadow berlebihan.
- Teks singkat, jelas, bahasa Indonesia sehari-hari. Emoji hanya untuk fitur mood.

### 10.2 Peta Navigasi
```
Login ──(sukses)──> Daftar Catatan ──> Detail Catatan ──(hapus)──> Daftar
                         │
                         └──> Tulis Catatan ──(simpan)──> Daftar
Logout (ikon app bar) ──> Login
```

### 10.3 Spesifikasi Layar
| Layar | Elemen utama | State |
|-------|--------------|-------|
| Login | Judul, kolom Username, kolom PIN (obscure, numerik, maks 4), tombol Masuk, teks error | idle, error validasi, error kredensial, loading singkat |
| Daftar Catatan | App bar + ikon Logout, daftar `NoteTile` (judul, tanggal, 2 baris isi), FAB "Tulis" | loading, empty, terisi, error baca |
| Tulis Catatan | Kolom Judul, kolom Isi (multiline), penghitung, tombol Simpan | idle, error validasi, menyimpan |
| Detail Catatan | Judul, tanggal, isi, ikon hapus | normal, dialog konfirmasi |

### 10.4 Wireframe Daftar Catatan
```
┌──────────────────────────────┐
│ Catatanku              [⎋]   │
├──────────────────────────────┤
│ 😄 Hari ini                   │
│ 13 Okt 2026, 17.33            │
│ Aku senang sekali karena ...  │
├──────────────────────────────┤
│ 😢 Kabar buruk                │
│ 12 Okt 2026, 21.05            │
│ Hari ini berat ...            │
│                        [ + ] │
└──────────────────────────────┘
```

### 10.5 Design Token (solid)
| Token | Nilai |
|-------|-------|
| Latar | `#FFFFFF` |
| Permukaan | `#F5F5F4` |
| Teks utama / sekunder | `#1C1B1F` / `#5F5E5A` |
| Aksen tunggal | `#2F5D50` |
| Error | `#B3261E` |
| Border | `#D9D8D4`, 1 px |
| Tipografi | Default Material; 20 (judul), 16 (isi), 12 (keterangan) |
| Spasi | Grid 8 dp; gutter 16 dp |
| Radius | 8 dp |

### 10.6 Microcopy
- Empty state: "Belum ada catatan." + tombol "Tulis catatan".
- Error login: "Username atau PIN salah."
- Konfirmasi hapus: "Hapus catatan ini? Tindakan ini tidak bisa dibatalkan."
- Setelah simpan: "Catatan disimpan."

### 10.7 Checklist Anti "AI Slop"
- [ ] Tidak ada gradient di mana pun.
- [ ] Hanya satu warna aksen.
- [ ] Tidak ada ilustrasi/ikon dekoratif tanpa fungsi.
- [ ] Tidak ada kalimat promosi atau slogan.
- [ ] Komponen Material standar dengan penyesuaian tema minimal.

---

## 11. Release & Milestone Planning

Estimasi untuk satu developer, hari kerja efektif. Urutan milestone juga menjadi urutan prioritas di dalam kategori Must.

| Milestone | Cakupan | Estimasi | Exit Criteria |
|-----------|---------|----------|---------------|
| M0 Setup | Proyek, struktur folder, tema, `ProviderScope`, lint | 0,5 hari | App kosong jalan; `analyze` bersih |
| M1 Auth | FR-D01–D04 + route guard | 1 hari | AC-D01–D04 lulus; test `Login` lulus |
| M2 Catatan | FR-D06–D10 | 1,5 hari | AC-D05–D08 lulus; data bertahan |
| M3 Mood Scanner | FR-D11 | 0,5 hari | 12 kasus AC-D09 lulus |
| M4 Hardening & Rilis | Should (D12, D13), usability test, bugfix, build | 1 hari | Metrik M1–M7 terpenuhi |
| **Total** | | **≈ 4,5 hari** | **Rilis v0.1.0** |

**Strategi rilis:** APK/IPA sideload untuk penguji internal (5 orang); tanpa store release pada MVP.

**Checklist rilis v0.1.0**
- [ ] Semua Must lulus AC.
- [ ] Metrik M1–M7 tercatat.
- [ ] Tidak ada bug severity tinggi terbuka.
- [ ] Tidak ada gradient; copy tidak mengklaim enkripsi.

**Roadmap pasca-MVP**
- v0.2: FR-D20 (enkripsi), FR-D14 (draft), FR-D05 (kunci sementara), edit catatan, tema gelap.
- v0.3: pencarian, ekspor/backup, biometrik.

---

## Lampiran A: Ringkasan Arsitektur Teknis (Clean Architecture)

**Aturan dependensi:** `presentation → domain ← data`
- `domain`: Dart murni, tanpa impor `flutter`, `shared_preferences`, atau `riverpod`.
- `presentation`: hanya bergantung pada `domain`; tidak mengimpor `data`.
- `data`: mengimplementasikan interface repository dari `domain`.
- DI hanya lewat provider Riverpod.

```
lib/
  main.dart
  core/ (error/, storage/prefs_provider.dart, theme/, utils/)
  features/
    auth/
      domain/ (entities/session.dart, repositories/auth_repository.dart,
               usecases/{login,logout,get_session}.dart)
      data/   (datasources/auth_local_datasource.dart,
               repositories/auth_repository_impl.dart)
      presentation/ (providers/, screens/login_screen.dart)
    notes/
      domain/ (entities/note.dart, repositories/note_repository.dart,
               services/mood_scanner.dart,
               usecases/{get_notes,add_note,delete_note}.dart)
      data/   (models/note_model.dart, datasources/note_local_datasource.dart,
               repositories/note_repository_impl.dart)
      presentation/ (providers/, screens/, widgets/note_tile.dart)
```

**Kontrak inti**
```dart
class Note { final String id, title, content; final DateTime createdAt; }
abstract class NoteRepository {
  Future<List<Note>> getNotes();
  Future<void> addNote(Note note);
  Future<void> deleteNote(String id);
}
class MoodScanner { String apply(String title, String content); } // pure
```

**Alur provider:** `sharedPreferencesProvider` → datasource → repository (tipe interface) → usecase → `notesNotifierProvider` (AsyncNotifier). `authNotifierProvider` menentukan layar awal.

**Pemetaan requirement → usecase:** D01/D02 `Login`; D03 `GetSession`; D04 `Logout`; D06 `AddNote` (memanggil `MoodScanner`); D07 `GetNotes`; D09 `DeleteNote`.
