# PRD Slice — Migrasi Daftar dan Detail Inspeksi

## Problem

Aplikasi lama Android Kotlin memiliki alur daftar dan detail inspeksi. Tim perlu
memindahkan alur itu ke Flutter tanpa mengubah contract API, navigation outcome,
atau penanganan state pengguna.

## User outcome

Petugas dapat membuka daftar inspeksi, memahami kondisi tiap aset, membuka
detail, kembali ke daftar yang sama, dan melihat loading/empty/error secara jelas.

## Traceability awal

| Legacy Kotlin | Target Flutter | Evidence |
|---|---|---|
| Activity/Fragment | Screen/route | widget test + demo |
| XML layout | Widget tree | narrow-screen review |
| ViewModel state | Controller/state object | unit/widget test |
| Retrofit service | ApiClient/Repository | contract test |
| SharedPreferences | explicit storage policy | restart/logout test |

## Acceptance criteria

- AC1: daftar menampilkan kode, lokasi, dan kondisi sesuai contract.
- AC2: tap item membuka detail untuk ID yang sama.
- AC3: loading, empty, dan error/retry dapat dibedakan.
- AC4: back kembali ke daftar tanpa membuat request ganda yang tidak perlu.
- AC5: source Flutter lolos format, analyze, dan test.
- AC6: setiap gap parity memiliki owner dan next action.

## WebView acceptance

- WV1: `https://www.presisirencar.com/` dapat dibuka dengan loading/error state.
- WV2: JavaScript aktif hanya untuk interaksi situs; JavaScript bridge tidak ada.
- WV3: hanya HTTPS ke `presisirencar.com` dan `www.presisirencar.com` yang diizinkan.
- WV4: provider API key tidak berada di asset atau bundle aplikasi.
- WV5: perubahan origin, scheme, bridge, atau session wajib melalui review PRD.

## Out of scope

Rewrite seluruh aplikasi, perubahan schema backend, autentikasi baru, JavaScript
bridge produksi, upload foto, dan distribusi store.

## Definition of done

PRD, patch Flutter, Agent Skill, hasil `flutter analyze`, hasil `flutter test`,
smoke test WebView pada device/emulator, dan daftar gap tersedia untuk review.
