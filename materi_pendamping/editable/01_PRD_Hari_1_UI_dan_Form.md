# PRD Hari 1 UI dan Form Inspeksi
**Product Requirements Document | DPL Inspection Training | Versi latihan 0.1**

**Trainer dan Pembuat Buku: Damar Galih Aji Pradana, S.Tr.Kom.**

## Tujuan dan konteks
Menghasilkan prototipe Flutter yang memungkinkan pengguna melihat daftar inspeksi, membuka detail, dan menambah catatan dengan validasi. Hari 1 memakai data lokal dalam memori agar peserta dapat memusatkan perhatian pada Dart, widget, navigation, dan state. Ini kasus pelatihan, bukan proses inspeksi DPL yang telah disahkan.

**Pengguna utama:** petugas inspeksi simulasi. **Pemilik hasil latihan:** tim developer peserta. **Reviewer:** trainer bersama PIC developer. Tidak ada autentikasi nyata, layanan API, role supervisor, atau approval pada checkpoint ini.

## User stories
- Sebagai petugas, saya ingin melihat daftar inspeksi agar mengetahui catatan yang tersedia.
- Sebagai petugas, saya ingin melihat detail agar dapat membaca kondisi aset dan catatan.
- Sebagai petugas, saya ingin membuat catatan baru agar hasil pemeriksaan muncul di daftar.
- Sebagai petugas, saya ingin mendapat pesan validasi agar data wajib tidak kosong.

## Kebutuhan fungsional
| ID | Persyaratan inti | Perilaku yang diharapkan |
|---|---|---|
| D1-01 | Daftar inspeksi | Minimal 3 dummy record; kode aset, lokasi, kondisi |
| D1-02 | Detail | Semua field record dipilih ditampilkan tanpa tertukar |
| D1-03 | Form tambah | Kode aset, lokasi, kondisi, catatan; tombol simpan |
| D1-04 | Validasi | Kode/lokasi trim tidak kosong; kondisi wajib |
| D1-05 | Aturan temuan | Kondisi Perlu tindak lanjut mewajibkan catatan >= 10 karakter setelah trim |
| D1-06 | Simpan lokal | Record baru mendapat ID unik dan waktu UTC lalu tampil di daftar |
| D1-07 | Navigasi | Kembali dari detail/form; batal form tidak menyimpan |
| D1-08 | State UI | Loading simulasi, success, empty dan error dengan retry |

**Prioritas tambahan:** filter kondisi, search lokal, theme dan reusable widget. Tambahan hanya setelah D1-01 sampai D1-08 lulus.

<!-- PAGE -->
## Data dan aturan tampilan
| Field | Tipe dan contoh | Aturan |
|---|---|---|
| id | String; local-001 | Unik; tidak dapat diedit pengguna |
| assetCode | String; PMP-001 | Wajib; trim; maksimal 30 karakter |
| location | String; Workshop A | Wajib; trim; maksimal 80 karakter |
| condition | String; good / needs_action | UI menampilkan Baik / Perlu tindak lanjut |
| note | String; Ada getaran pada motor | Maksimal 500 karakter; temuan minimal 10 |
| createdAt | DateTime UTC | Dibuat sistem; tampil sebagai waktu lokal perangkat |

**Layout:** daftar berupa ListView.builder. Detail dan form dapat di-scroll. Ukuran uji 360 x 800 logical pixels dan landscape emulator. Peserta boleh memakai Material design bawaan; target hari 1 adalah alur yang bekerja dan keterbacaan.

## Alur layar
1. Aplikasi membuka daftar dan menampilkan loading simulasi, kemudian data dummy.
2. Pengguna memilih sebuah record untuk membuka detail, lalu kembali ke daftar.
3. Tombol tambah membuka form. Simpan menjalankan validator seluruh field.
4. Form valid menghasilkan record dan kembali ke daftar. Form batal tidak menghasilkan record.
5. Daftar kosong menampilkan pesan dan tombol tambah. Error simulasi menampilkan pesan dan retry.

## Kebutuhan nonfungsional
- UI tidak overflow pada dua orientasi uji dan input tetap terjangkau ketika keyboard terbuka.
- FormController di-dispose; tidak ada setState setelah widget dilepas.
- Model memiliki tipe eksplisit, menggunakan null safety; tidak memakai dynamic untuk seluruh aplikasi.
- Data hari 1 boleh hilang setelah aplikasi ditutup. Persistence adalah scope hari 2.
- Label field dan pesan error jelas. Warna bukan satu-satunya penanda kondisi.

## Batas scope
Login, REST API, database, token, foto, push notification, GPS, signing, dan store upload belum termasuk hasil hari 1. Fitur bisnis seperti scheduling inspeksi, escalation, dan approval supervisor tidak dikembangkan dalam kelas ini.

## Dependensi dan risiko
Flutter 3.44.8, Xcode, dan iPhone 16 Simulator iOS 18.0 sudah siap. Jika environment peserta bermasalah, trainer memberi checkpoint proyek lengkap; peserta tetap harus mendemonstrasikan perubahan sendiri. Desain final dan SOP inspeksi DPL belum menjadi input latihan.

<!-- PAGE -->
## Acceptance criteria hari 1
| ID | Skenario uji | Kriteria lulus |
|---|---|---|
| AC1 | Buka aplikasi | Loading lalu >= 3 dummy record tampil |
| AC2 | Pilih record kedua | Detail cocok dengan id record kedua |
| AC3 | Simpan kode aset berisi spasi saja | Pesan error; daftar tidak berubah |
| AC4 | Kondisi needs_action dengan catatan pendek | Simpan ditolak dan aturan dijelaskan |
| AC5 | Simpan data valid dua kali | Dua record berbeda dengan ID unik |
| AC6 | Isi form lalu tekan batal | Tidak ada record baru |
| AC7 | Set daftar kosong dan error simulasi | Empty dan error tampil; retry memulihkan daftar |
| AC8 | Buka form dan keyboard pada layar sempit | Field/tombol dapat diakses; tidak ada overflow |

## Definition of done
- D1-01 sampai D1-08 dan seluruh acceptance criteria lulus.
- Source proyek disimpan di Git dengan README singkat dan tag day-1.
- Peserta menyerahkan screenshot daftar, detail, form invalid, serta form valid.
- Peserta dapat menjelaskan pilihan StatelessWidget/StatefulWidget dan asal data daftar.
- Temuan review dicatat dengan status, bukti, dan aksi perbaikan; trainer menandai checkpoint dapat dilanjutkan.

## Cara review dalam 30 menit terakhir
Per pasangan, demo 4 menit: daftar-detail, form invalid, form valid, dan error/retry. Trainer memeriksa alur utama dan memilih satu skenario tambahan. Peserta melakukan commit final, menyimpan bukti, lalu menuliskan satu kendala yang harus ditangani sebelum hari 2.

## Pertanyaan yang sengaja terbuka
Sebelum dipakai sebagai aplikasi DPL nyata, PIC perlu menentukan master aset, definisi kondisi, hak akses, SOP foto, retensi data, dan kebutuhan approval. Jawaban tidak diperlukan untuk data dummy kelas, tetapi wajib untuk pengembangan operasional.
