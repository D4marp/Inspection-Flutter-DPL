# DPL Migration Lab — Hari 3

Proyek Flutter untuk belajar memigrasikan satu vertical slice aplikasi Android
Kotlin ke Flutter berdasarkan PRD. Demo menyatukan empat area:

1. PRD migrasi dan acceptance criteria.
2. WebView situs latihan yang dibatasi host.
3. Target Flutter daftar/detail inspeksi dan foto lokal.
4. Agent Skill `migrate-kotlin-slice` untuk workflow migrasi yang repeatable.

## Toolchain

- Flutter 3.44.8 stable; Dart 3.12.2
- `webview_flutter` 4.14.1
- `image_picker` dan `shared_preferences`
- Android dan iOS tersedia dari hasil `flutter create`

## Menjalankan dan memverifikasi

```sh
fvm flutter pub get
fvm dart format --output=none --set-exit-if-changed lib test
fvm flutter analyze
fvm flutter test
fvm flutter run
```

Build verifikasi Android:

```sh
fvm flutter build apk --debug
```

## WebView boundary

WebView membuka `https://www.presisirencar.com/`. JavaScript diaktifkan karena
situs latihan memakai interaksi Next.js, tetapi tidak ada JavaScript bridge ke
Flutter. `NavigationDelegate` hanya mengizinkan HTTPS ke `presisirencar.com`
dan `www.presisirencar.com`; HTTP, subdomain palsu, scheme lain, serta tautan
eksternal diblokir.

Source WebView dipisah agar mudah dibedah:

```text
lib/src/webview/navigation_policy.dart
lib/src/webview/migration_webview_controller.dart
lib/src/screens/training_webview_screen.dart
```

Policy URL dapat diuji tanpa platform view, controller memegang URL dan
konfigurasi security/lifecycle, dan screen hanya merender progress, error,
back, reload, serta WebView.

Jika origin berubah, revisi PRD, allowlist, session, TLS, file upload/download,
dan logout sebelum mengubah kode. Jangan pernah menyisipkan API key provider AI
ke Flutter, HTML, JavaScript, URL, atau asset aplikasi.

## Agent Skill

Skill proyek berada di:

```text
.agents/skills/migrate-kotlin-slice/SKILL.md
```

OpenCode dapat menemukan skill dari folder `.agents/skills`. Minta agent
memakai `migrate-kotlin-slice`, lalu berikan PRD slice, source Kotlin/XML yang
relevan, contract API, target file Flutter, dan test yang sudah ada.

Contoh prompt:

```text
Gunakan skill migrate-kotlin-slice. Migrasikan alur daftar-detail dari legacy
Kotlin sesuai PRD. Tunjukkan traceability AC, patch kecil, hasil analyze/test,
dan gap yang tersisa.
```

Panduan praktik lebih lengkap ada pada [docs/AI_AGENT_PLAYBOOK.md](docs/AI_AGENT_PLAYBOOK.md)
dan [docs/PRD_MIGRASI_KOTLIN.md](docs/PRD_MIGRASI_KOTLIN.md).

## Batas demo

Foto hanya preview lokal. WebView bukan bridge produksi. Source legacy Kotlin
tidak disertakan sehingga peserta memakai contoh/fixture yang diberikan trainer.
Build release, signing, dan deployment backend tetap menjadi quality gate
terpisah.
