# Paket Training Flutter DPL — 3 Hari

Paket ini berisi materi, PowerPoint, PDF, dan tiga proyek praktik Flutter untuk
pelatihan PT. Dok Pantai Lamongan. Fokus kelas tetap pada Flutter dan API publik
siap pakai, sehingga peserta tidak perlu menyiapkan layanan server sendiri.

## Isi paket

| Hari | Proyek | Fokus |
|---|---|---|
| 1 | `flutter_projects/hari_1_dpl_inspection` | Dart, UI, form, navigation, dan state lokal |
| 2 | `flutter_projects/hari_2_dpl_inspection_api` | Simulasi CRUD API, clean code, image picker, file picker, dan OpenCode |
| 3 | `flutter_projects/hari_3_dpl_inspection_release` | WebView, PRD migrasi Kotlin, Agent Skill, dan quality gate |

Materi presentasi tersedia di root dan folder `PPT_Training`. Versi editable
dan PDF berada di `materi_pendamping`.

## API latihan Hari 2

Hari 2 memakai API publik gratis JSONPlaceholder:

```text
https://jsonplaceholder.typicode.com/posts
```

Tidak ada akun, API key, atau server lokal yang perlu disiapkan. GET
mengambil data publik. POST, PUT, dan DELETE mengembalikan respons simulasi,
tetapi tidak menyimpan perubahan secara permanen. Aplikasi menampilkan batas
ini secara eksplisit agar peserta memahami perbedaan respons sukses dan
persistence.

Tutorial implementasi per file:

```text
flutter_projects/hari_2_dpl_inspection_api/
  docs/JSONPLACEHOLDER_PER_FILE.md
```

## WebView Hari 3

Contoh WebView membuka:

```text
https://www.presisirencar.com/
```

Navigasi dibatasi ke HTTPS dan host `presisirencar.com`/
`www.presisirencar.com`. Tautan eksternal diblokir. JavaScript aktif untuk
interaksi situs, tanpa JavaScript bridge ke Flutter.

## Menjalankan proyek

Contoh untuk Hari 2:

```sh
cd flutter_projects/hari_2_dpl_inspection_api
fvm flutter pub get
fvm flutter analyze
fvm flutter test
fvm flutter run
```

Gunakan langkah yang sama pada folder Hari 1 atau Hari 3. Setiap proyek
memiliki `.fvmrc`, `pubspec.lock`, README, dan test masing-masing.

## Push repository

Script `push-to-repos.sh` di root menyinkronkan tiga repository: repo utama
(paket dan Hari 1), Hari 2, dan Hari 3. Backend tidak termasuk:

```sh
./push-to-repos.sh
```

Pilih target `main`, `day2`, atau `day3` untuk push satu repository, misalnya
`./push-to-repos.sh day2`. Pastikan perubahan repo utama sudah di-commit;
script tidak melakukan force-push dan menolak berjalan saat worktree repo utama
masih memiliki perubahan lokal.

## Keamanan

Jangan commit API key, token, `.env`, keystore, atau data operasional. API key
AI dipakai oleh tool developer melalui mekanisme login/provider, bukan ditanam
di source Flutter atau APK.
