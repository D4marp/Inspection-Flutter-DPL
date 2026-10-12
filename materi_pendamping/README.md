# Paket Training Flutter 3 Hari — Proyek Lengkap + iPhone 16

**Trainer dan Pembuat Buku: Damar Galih Aji Pradana, S.Tr.Kom.**

Paket untuk tim developer PT. Dok Pantai Lamongan yang sudah mengenal Kotlin.
Praktik kelas dijalankan pada iPhone 16 Simulator yang lebih ringan daripada
varian Pro/Pro Max. Source Android tetap dibuat untuk kebutuhan build lanjutan.

## Toolchain yang dikunci

- Flutter 3.44.8 stable
- Dart 3.12.2
- DevTools 2.57.0
- Xcode 26.5
- Simulator: iPhone 16, iOS 18.0

Setiap proyek mempunyai `.fvmrc` dan `pubspec.lock`. Gunakan FVM agar laptop
peserta dan CI memakai versi yang sama:

```sh
fvm install 3.44.8
fvm flutter --version
```

## Tiga proyek hasil `flutter create`

| Hari | Folder | Hasil utama |
|---|---|---|
| 1 | `../flutter_projects/hari_1_dpl_inspection` | UI, form, navigation, state lokal |
| 2 | `../flutter_projects/hari_2_dpl_inspection_api` | UI foundation, full CRUD, image/file picker, OpenCode setup |
| 3 | `../flutter_projects/hari_3_dpl_inspection_release` | PRD migrasi Kotlin, WebView, Agent Skill, quality gate |

Semua folder adalah proyek mandiri hasil
`flutter create --platforms=android,ios`. Masing-masing memiliki README, test,
konfigurasi platform, lockfile, dan instruksi GitHub. Karena mandiri, setiap
folder dapat menjadi repository GitHub terpisah.

## Hari 1 — UI dan form

```sh
cd ../flutter_projects/hari_1_dpl_inspection
fvm flutter pub get
fvm flutter analyze
fvm flutter test
fvm flutter run -d "iPhone 16"
```

Proyek mencakup model, validator, daftar/detail/form, loading, empty state,
error/retry, theme, komponen reusable, dan widget test.

![Aplikasi Hari 1 pada iPhone 16](../flutter_projects/hari_1_dpl_inspection/screenshots/hari_1_daftar.png)

## Hari 2 — UI, full CRUD, picker, dan OpenCode

Proyek mempunyai tiga tab: CRUD API, UI Dasar, dan AI Setup. Jalur utama memakai
JSONPlaceholder public API; peserta mengerjakan GET, POST, PUT, DELETE, mapper,
failure state, picker, serta setup OpenCode tanpa API key di Flutter.

```sh
cd flutter_projects/hari_2_dpl_inspection_api
fvm flutter pub get
fvm flutter run -d "iPhone 16"
```

Trainer memverifikasi GET, POST, PUT, dan DELETE terhadap
`https://jsonplaceholder.typicode.com/posts`. Write hanya simulasi dan tidak
persisten; banner aplikasi serta materi menjelaskan batas ini.

```sh
curl 'https://jsonplaceholder.typicode.com/posts?_limit=2'
```

Tutorial pembuatan per file berada di
`../flutter_projects/hari_2_dpl_inspection_api/docs/JSONPLACEHOLDER_PER_FILE.md`.
Jika internet kelas gagal, gunakan response fixture melalui `MockClient`; mock
lama `/inspections` tidak kompatibel dengan adapter `/posts` yang baru.

Tidak ada login/API key untuk JSONPlaceholder. File yang dipilih pada form hanya
preview/metadata lokal dan belum di-upload.

![Aplikasi Hari 2 mengambil data API](../flutter_projects/hari_2_dpl_inspection_api/screenshots/hari_2_api.png)

## Hari 3 — Flutter WebView dan migrasi Kotlin berbasis PRD

```sh
cd flutter_projects/hari_3_dpl_inspection_release
fvm flutter pub get
fvm flutter analyze
fvm flutter test
fvm flutter run -d "iPhone 16"
```

App Migration Lab mempunyai tab PRD, WebView, target Flutter, dan Agent Skill.
WebView membuka `https://www.presisirencar.com/` dengan exact-host HTTPS
allowlist. Tautan eksternal diblokir dan JavaScript aktif tanpa JavaScript
bridge. Skill proyek berada di
`.agents/skills/migrate-kotlin-slice/SKILL.md`; foto lokal tetap tersedia pada
target detail sebagai contoh native plugin/lifecycle.

![Aplikasi Hari 3 dengan panel foto](../flutter_projects/hari_3_dpl_inspection_release/screenshots/hari_3_foto.png)

## Push GitHub per hari

Jalankan dari folder proyek yang ingin dipush:

```sh
git init
git add .
git commit -m "Complete Flutter training checkpoint"
git branch -M main
git remote add origin https://github.com/USERNAME/NAMA-REPO.git
git push -u origin main
```

Jangan commit token, `.env`, password, keystore, atau data operasional.

## Status verifikasi

Ketiga proyek sudah dijalankan dengan Flutter 3.44.8 pada iPhone 16 Simulator.
Semuanya lulus `flutter analyze` dan `flutter test`. Screenshot di atas diambil
langsung dari simulator 1179×2556; Hari 2 diverifikasi bersama mock API aktif.
Contoh tetap merupakan aplikasi training, bukan aplikasi production.
