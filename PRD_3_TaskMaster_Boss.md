# PRD: TaskMaster Boss

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
Karyawan sering lupa atau menunda tugas harian, dan aplikasi to-do biasa terasa hambar sehingga ditinggalkan setelah beberapa hari. Tidak ada umpan balik yang membuat menyelesaikan tugas terasa "ada reaksinya".

### 1.2 Objective
Membangun MVP to-do list **offline** yang:
1. Menyimpan sesi karyawan (login email, token tersimpan, logout di halaman Profile).
2. Mendukung tambah tugas, tandai selesai, dan hapus.
3. Menampilkan "AI Boss Evaluator" (mock): komentar acak bernada bos cerewet lewat Snackbar setiap tugas selesai.

### 1.3 Hipotesis
Jika menyelesaikan tugas memicu komentar lucu yang bervariasi, pengguna lebih terdorong membuka aplikasi lagi, tanpa menambah langkah ekstra.

---

## 2. Success Metrics

> Tanpa backend/analytics. Semua metrik diukur lewat skrip uji, unit test, dan usability test kecil. Target berlaku untuk v0.1.0.

| # | Tujuan | Metrik | Target | Cara Ukur |
|---|--------|--------|--------|-----------|
| M1 | Alur inti mudah | Penguji menyelesaikan login → tambah tugas → centang → hapus → logout tanpa bantuan | ≥ 4 dari 5 | Usability test |
| M2 | Aktivasi cepat | Waktu dari login sukses sampai tugas pertama tersimpan | ≤ 15 detik (median) | Stopwatch |
| M3 | Respons bos konsisten | Snackbar muncul pada transisi belum → selesai | 100%; 0 kali pada pembatalan centang | Widget test |
| M4 | Variasi komentar | Komentar identik berturut-turut | 0 pada 50 pemicu simulasi | Unit test `BossEvaluator` |
| M5 | Sesi bertahan | Login terjaga setelah force-close; terhapus setelah Logout | 100% | Uji manual 3 percobaan |
| M6 | Data bertahan | Tugas dan status centang utuh setelah restart | 100% | Uji manual |
| M7 | Kualitas teknis | `flutter analyze` / cakupan domain / start dingin | 0 isu / ≥ 80% / ≤ 2 dtk | `flutter test --coverage`, DevTools |

**Counter-metric:** komentar bos tidak boleh menghalangi aksi berikutnya (tidak ada dialog modal; Snackbar tidak menumpuk).

---

## 3. Target Audience & Personas

### Persona Utama: Nadia (26), staf administrasi kantor
- **Konteks:** banyak tugas kecil per hari dari beberapa atasan; sering lupa.
- **Tujuan:** daftar tugas yang bisa diisi cepat dan dicoret dengan rasa puas.
- **Frustrasi:** to-do app biasa membosankan; fitur kompleks (prioritas, label) tidak dipakai.
- **Perilaku:** membuka aplikasi 3–5 kali sehari; suka humor kantor.
- **Kutipan:** "Kalau selesai ada yang ngomentarin, kan jadi lucu."

### Stakeholder: Developer/Reviewer
Menilai arsitektur, Riverpod, dan pemisahan logika komentar dari UI.

---

## 4. Functional Requirements (MoSCoW)

**Aturan prioritisasi**
- **Must:** tanpa ini journey utama gagal atau data/sesi tidak benar. Blocker rilis.
- **Should:** penting tetapi ada workaround; masuk v0.1.0 jika jadwal cukup, jika tidak ke v0.2.
- **Could:** nilai tambah kecil; default v0.2+.
- **Won't (rilis ini):** disepakati tidak dikerjakan sekarang.
- Must tidak melebihi sekitar 60% dari total effort.

| ID | Requirement | Prioritas | Catatan / Alasan | Story |
|----|-------------|-----------|------------------|-------|
| **Autentikasi** | | | | |
| FR-T01 | Login dengan Email (tanpa password) | **Must** | Syarat skenario auth | US-T01 |
| FR-T02 | Validasi format email (mis. `nama@domain.tld`); email dinormalisasi (trim, huruf kecil) | **Must** | Cegah input asal | US-T01 |
| FR-T03 | Simpan `employee_token` + email; auto-login saat aplikasi dibuka ulang | **Must** | Syarat: sesi tidak hilang saat aplikasi ditutup | US-T02 |
| FR-T04 | Halaman Profile menampilkan email + tombol Logout yang menghapus token | **Must** | Syarat brief | US-T03 |
| FR-T05 | Verifikasi email / password | Won't | Auth demo lokal | - |
| **Tugas** | | | | |
| FR-T06 | Tambah tugas (judul wajib, tidak boleh hanya spasi) | **Must** | Inti produk | US-T04 |
| FR-T07 | Daftar tugas: belum selesai di atas, selesai di bawah (judul dicoret) | **Must** | Inti produk | US-T05 |
| FR-T08 | Tandai selesai lewat checkbox (toggle); status tersimpan | **Must** | Inti produk | US-T06 |
| FR-T09 | Hapus tugas (swipe atau ikon) | **Must** | CRUD yang diminta | US-T07 |
| FR-T10 | Empty state pada daftar tugas | **Must** | Mulai tanpa data | US-T05 |
| FR-T11 | Batas judul 120 karakter | Should | Cegah layout rusak | US-T04 |
| FR-T12 | Hapus tanpa konfirmasi, tetapi ada "Urungkan" di Snackbar | Could | Aksi ringan; ganti konfirmasi dengan undo | US-T07 |
| FR-T13 | Penghitung "X dari Y selesai" | Could | Rasa progres | US-T05 |
| **Mock AI Boss** | | | | |
| FR-T14 | Snackbar komentar acak dari `List<String>` (≥ 6) saat transisi belum → selesai; tidak muncul saat centang dibatalkan | **Must** | Pembeda produk, syarat brief | US-T08 |
| FR-T15 | Komentar tidak sama dengan komentar sebelumnya | Should | Terasa "hidup" | US-T08 |
| FR-T16 | Snackbar baru menggantikan yang lama (tidak menumpuk) | Should | Centang cepat beruntun | US-T08 |
| FR-T17 | Edit judul, deadline, prioritas, kategori, notifikasi, sinkronisasi | Won't | Di luar MVP | - |

---

## 5. Critical User Journeys & User Stories

### 5.1 Critical User Journeys

**CUJ-1: Hari pertama kerja** (journey utama, M1 dan M2)
1. Buka aplikasi → Login → isi `nadia@kantor.com` → Masuk.
2. Empty state → tap "Tambah tugas" → "Kirim laporan" → Simpan.
3. Centang tugas → Snackbar: "Bagus, tapi gajimu tetap sama."
4. *Jalur gagal:* email tidak valid → pesan "Format email tidak valid".

**CUJ-2: Kembali ke aplikasi**
1. Buka aplikasi → langsung ke daftar tugas (token ada).
2. Hapus satu tugas lama.

**CUJ-3: Pergantian akun**
1. Tab Profile → email tampil → Logout → Login.
2. Back tidak mengembalikan ke daftar tugas.

### 5.2 User Stories

| ID | Story | FR |
|----|-------|----|
| US-T01 | Sebagai karyawan, saya ingin masuk dengan email, agar tugas saya terasa pribadi. | T01, T02 |
| US-T02 | Sebagai karyawan, saya ingin tetap login setelah menutup aplikasi, agar tidak mengulang login. | T03 |
| US-T03 | Sebagai karyawan, saya ingin logout dari halaman Profile, agar bisa ganti akun atau mengamankan perangkat. | T04 |
| US-T04 | Sebagai karyawan, saya ingin menambah tugas dengan cepat, agar tidak lupa. | T06, T11 |
| US-T05 | Sebagai karyawan, saya ingin melihat tugas aktif lebih dulu dari yang selesai, agar fokus pada yang belum dikerjakan. | T07, T10, T13 |
| US-T06 | Sebagai karyawan, saya ingin mencentang tugas yang selesai, agar progres jelas. | T08 |
| US-T07 | Sebagai karyawan, saya ingin menghapus tugas yang tidak relevan, agar daftar tetap rapi. | T09, T12 |
| US-T08 | Sebagai karyawan, saya ingin komentar bos saat tugas selesai, agar menyelesaikan tugas terasa menyenangkan. | T14–T16 |

---

## 6. Acceptance Criteria

**AC-T01 Login (FR-T01, T02)**
- Given belum login, When memasukkan email valid lalu Masuk, Then `employee_token` dan email tersimpan, dan Daftar Tugas tampil.
- Given email kosong atau tidak valid, Then muncul "Format email tidak valid" dan tidak ada token tersimpan.

| Input | Valid? |
|-------|--------|
| `nadia@kantor.com` | Ya |
| `  Nadia@Kantor.com ` | Ya (disimpan `nadia@kantor.com`) |
| `nadia@kantor` | Tidak |
| `nadia.kantor.com` | Tidak |
| (kosong) | Tidak |

**AC-T02 Sesi bertahan (FR-T03)**
- Given sudah login, When force-close lalu buka kembali, Then langsung ke Daftar Tugas.

**AC-T03 Profile & Logout (FR-T04)**
- Given membuka Profile, Then email aktif tampil.
- Given tap Logout, Then token dan email terhapus, Login tampil, dan back tidak membuka Daftar Tugas.
- Given aplikasi dibuka ulang setelah Logout, Then Login tampil.

**AC-T04 Tambah tugas (FR-T06, T11)**
- Given judul kosong atau hanya spasi, Then muncul "Judul wajib diisi" dan tugas tidak tersimpan.
- Given judul valid, Then tugas muncul di bagian belum selesai dan bertahan setelah restart.

**AC-T05 Daftar (FR-T07, T10)**
- Given ada tugas campuran, Then belum selesai di atas dan selesai di bawah dengan judul dicoret.
- Given belum ada tugas, Then empty state tampil.

**AC-T06 Toggle (FR-T08)**
- Given centang tugas, Then `isDone = true`, tugas pindah ke bagian selesai, dan status tersimpan.
- Given hapus centang, Then `isDone = false` dan tugas kembali ke bagian belum selesai.

**AC-T07 Hapus (FR-T09)**
- Given swipe atau tap hapus, Then tugas hilang dari daftar dan dari storage.

**AC-T08 Mock AI Boss Evaluator (FR-T14–T16)**
- Given tugas belum selesai, When dicentang, Then Snackbar tampil ≤ 3 detik dengan satu komentar dari list.
- Given tugas selesai, When centang dibatalkan, Then **tidak ada** Snackbar.
- Given dua tugas dicentang berurutan cepat, Then Snackbar pertama diganti Snackbar kedua (Should).
- Given 50 pemicu berurutan, Then tidak ada dua komentar identik berurutan (Should).
- List komentar berisi minimal 6 string; contoh:
  - "Bagus, tapi gajimu tetap sama."
  - "Akhirnya selesai juga, saya kira kamu ketiduran."
  - "Hmm, standar. Lanjut tugas berikutnya."
  - "Cepat juga. Pasti tugasnya terlalu gampang."
  - "Selesai? Bagus. Sekarang ada 3 tugas lagi."
  - "Saya tidak bilang bagus, saya bilang selesai."
- Panduan konten: sindiran ringan soal pekerjaan, **tidak** menyinggung fisik, SARA, atau pribadi.

---

## 7. Out of Scope

- Edit judul, deadline, prioritas, kategori/label, subtugas.
- Notifikasi pengingat, widget layar utama.
- Password, verifikasi email, multi-user, sinkronisasi cloud.
- AI sungguhan atau personalisasi komentar.
- Statistik produktivitas dan laporan.

---

## 8. Non-Functional Requirements

| Kategori | Requirement | Target | Verifikasi |
|----------|-------------|--------|------------|
| Performa | Start dingin | ≤ 2 detik | DevTools |
| Performa | Toggle centang → UI ter-update | ≤ 100 ms | Widget test / manual |
| Performa | Daftar 1.000 tugas | Scroll ≥ 55 fps | DevTools |
| Keandalan | Data dan sesi bertahan setelah force-close | 100% | Uji manual |
| Keandalan | JSON rusak | Tidak crash; daftar kosong + pesan | Unit test datasource |
| Keamanan & privasi | Data lokal; tanpa permission INTERNET; tidak ada log email | Terpenuhi | Cek manifest, review |
| Keamanan | Token lokal bukan autentikasi nyata; didokumentasikan sebagai identifikasi sesi | Didokumentasikan | Review |
| Konten | Daftar komentar bebas konten ofensif | Terpenuhi | Review manual |
| Aksesibilitas | Target sentuh ≥ 48 dp; kontras ≥ 4,5:1; teks 1,5× tanpa overflow; Snackbar terbaca pembaca layar; checkbox berlabel judul tugas | Terpenuhi | Uji manual |
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
- A1: Satu pengguna per perangkat; login ulang dengan email berbeda menimpa sesi, **bukan** memisahkan data per akun (lihat R3).
- A2: Token dibuat lokal (mis. UUID/timestamp); tidak divalidasi server.
- A3: Email tidak diverifikasi.
- A4: Bahasa Indonesia; komentar bos hanya dari daftar bawaan.

### 9.3 Risks
| ID | Risiko | Peluang | Dampak | Mitigasi |
|----|--------|---------|--------|----------|
| R1 | Komentar "roasting" dianggap menyinggung | Sedang | Sedang | Panduan konten; tinjau seluruh string sebelum rilis |
| R2 | Pengguna mengira email/token adalah autentikasi aman | Sedang | Rendah | Dokumentasikan sebagai identifikasi sesi lokal |
| R3 | Ganti akun menampilkan tugas akun sebelumnya | Sedang | Sedang | Pada MVP data tugas bersifat global per perangkat; dicatat di backlog (data per email) |
| R4 | Snackbar menumpuk saat centang beruntun | Tinggi | Rendah | FR-T16 (ganti Snackbar lama) |
| R5 | Komentar terasa repetitif | Sedang | Rendah | FR-T15; perluas daftar di v0.2 |
| R6 | Hapus tanpa konfirmasi menyebabkan salah hapus | Sedang | Rendah | Pilihan: FR-T12 (Urungkan) |
| R7 | Scope creep (deadline, notifikasi) | Sedang | Sedang | Daftar Won't dibekukan |

### 9.4 Pertanyaan Terbuka
- Perlukah Logout menghapus data tugas? (default MVP: tidak; tugas tetap tersimpan)

---

## 10. Design & UX

### 10.1 Prinsip
- Ringan dan cepat: tambah tugas dalam 2–3 tap.
- Humor ada di teks komentar, **bukan** di dekorasi visual.
- Warna **solid**, **tanpa gradient**, tanpa glassmorphism/neon/shadow berlebihan.

### 10.2 Peta Navigasi
```
Login ──> Shell (bottom nav)
            ├─ Tugas  (daftar + tambah tugas via bottom sheet)
            └─ Profile (email + Logout) ──> Login
```

### 10.3 Spesifikasi Layar
| Layar | Elemen utama | State |
|-------|--------------|-------|
| Login | Judul, kolom Email, tombol Masuk, teks error | idle, error validasi, loading |
| Tugas | Daftar `TaskTile` (checkbox + judul), seksi "Belum selesai"/"Selesai", FAB tambah | loading, empty, terisi |
| Tambah Tugas | Bottom sheet: kolom judul, tombol Simpan | idle, error validasi |
| Profile | Email, tombol Logout | normal |
| Snackbar Bos | Satu baris teks komentar, 3 detik | muncul / diganti |

### 10.4 Wireframe Daftar Tugas
```
┌──────────────────────────────┐
│ Tugas                        │
├──────────────────────────────┤
│ BELUM SELESAI                │
│ [ ] Kirim laporan mingguan   │
│ [ ] Balas email klien        │
│ SELESAI                      │
│ [x] ~~Rapat pagi~~           │
│                       [ + ]  │
│ ┌──────────────────────────┐ │
│ │ Bagus, tapi gajimu tetap │ │
│ │ sama.                    │ │
│ └──────────────────────────┘ │
├──────────────────────────────┤
│   Tugas   │   Profile        │
└──────────────────────────────┘
```

### 10.5 Design Token (solid)
| Token | Nilai |
|-------|-------|
| Latar | `#FFFFFF` |
| Permukaan | `#F4F6F8` |
| Teks utama / sekunder | `#1A1C1E` / `#5B6168` |
| Aksen tunggal | `#0F5CA8` |
| Error | `#B3261E` |
| Border | `#D5DAE0`, 1 px |
| Tipografi | Default Material; 20 / 16 / 12; teks selesai dicoret + warna sekunder |
| Spasi | Grid 8 dp; gutter 16 dp |
| Radius | 8 dp |

### 10.6 Microcopy
- Empty: "Belum ada tugas. Bos belum punya bahan komentar."
- Error email: "Format email tidak valid."
- Judul kosong: "Judul wajib diisi."

### 10.7 Checklist Anti "AI Slop"
- [ ] Tidak ada gradient.
- [ ] Satu warna aksen.
- [ ] Tidak ada avatar/maskot bos dekoratif; humor hanya lewat teks.
- [ ] Snackbar memakai komponen standar.
- [ ] Tidak ada slogan motivasi generik.

---

## 11. Release & Milestone Planning

Estimasi satu developer, hari kerja efektif. Urutan milestone = urutan prioritas di dalam Must.

| Milestone | Cakupan | Estimasi | Exit Criteria |
|-----------|---------|----------|---------------|
| M0 Setup | Proyek, struktur, tema, `ProviderScope`, lint | 0,5 hari | App kosong jalan; `analyze` bersih |
| M1 Auth & Profile | FR-T01–T04 | 1 hari | AC-T01–T03 lulus |
| M2 Tugas | FR-T06–T10 | 1 hari | AC-T04–T07 lulus |
| M3 Boss Evaluator | FR-T14 (+ T15, T16) | 0,5 hari | AC-T08 lulus |
| M4 Hardening & Rilis | Should (T11, T15, T16), usability test, bugfix, build | 1 hari | Metrik M1–M7 terpenuhi |
| **Total** | | **≈ 4 hari** | **Rilis v0.1.0** |

**Strategi rilis:** APK/IPA sideload untuk 5 penguji; tanpa rilis store.

**Checklist rilis v0.1.0**
- [ ] Semua Must lulus AC.
- [ ] Metrik M1–M7 tercatat.
- [ ] Seluruh komentar bos lolos tinjauan konten.
- [ ] Tidak ada gradient.

**Roadmap pasca-MVP**
- v0.2: tugas per akun email, "Urungkan" hapus (T12), penghitung progres (T13), perluasan daftar komentar.
- v0.3: edit tugas, deadline, notifikasi.

---

## Lampiran A: Ringkasan Arsitektur Teknis (Clean Architecture)

**Aturan dependensi:** `presentation → domain ← data`
- `domain`: Dart murni (tanpa `flutter`, `shared_preferences`, `riverpod`).
- `presentation`: hanya bergantung pada `domain`; tampilan Snackbar ada di layer ini.
- `data`: mengimplementasikan interface repository.
- DI hanya lewat provider Riverpod.

```
lib/
  core/ (error/, storage/, theme/, utils/)
  features/
    auth/   domain/ (session, auth_repository, usecases login/logout/get_session)
            data/ (auth_local_datasource, auth_repository_impl)
            presentation/ (login_screen, profile_screen, providers)
    tasks/  domain/ (task, task_repository, services/boss_evaluator,
                     usecases get/add/toggle/delete)
            data/ (task_model, task_local_datasource, task_repository_impl)
            presentation/ (task_list_screen, widgets, providers)
```

**Kontrak inti**
```dart
class Task { final String id, title; final bool isDone; final DateTime createdAt; }
class Session { final String token, email; }
abstract class TaskRepository {
  Future<List<Task>> getTasks();
  Future<void> saveTasks(List<Task> tasks);
}
class BossEvaluator {
  BossEvaluator({Random? random});
  String nextComment(); // acak, tidak sama dengan komentar sebelumnya
}
```

**Alur provider:** `sharedPreferencesProvider` → datasource → repository → usecase → `tasksNotifierProvider` (AsyncNotifier). `authNotifierProvider` menentukan layar awal. `bossEvaluatorProvider` menyediakan komentar.

**Pemicu Snackbar:** UI memanggil `toggle(id)`; usecase `ToggleTask` mengembalikan status baru. Jika hasilnya "baru selesai", UI memanggil `bossEvaluator.nextComment()` dan menampilkan Snackbar. Domain tidak menyentuh UI.

**Pemetaan requirement → usecase/service:** T01/T02 `Login`; T03 `GetSession`; T04 `Logout`; T06 `AddTask`; T07 `GetTasks`; T08 `ToggleTask`; T09 `DeleteTask`; T14/T15 `BossEvaluator`.
