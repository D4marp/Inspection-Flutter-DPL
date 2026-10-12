#!/usr/bin/env python3
"""Build Day 2 deck: UI foundations, open CRUD API, pickers, and OpenCode AI setup."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches

import build_professional_decks as d


ROOT = Path(__file__).resolve().parents[1]
TOTAL = 39


def notes(slide, session, minutes, objective, delivery, question, reference):
    d.add_notes(slide, session, minutes, objective, delivery, question, reference)


def three_cards(prs, n, section, title, cards, bottom=None):
    slide = d.base_slide(prs, section, title, n, TOTAL, 2)
    for i, (heading, items, icon, accent) in enumerate(cards):
        d.add_card(slide, Inches(0.62 + i * 4.16), Inches(1.30), Inches(3.78), Inches(4.95), heading, items, icon=icon, accent=accent, body_size=13)
    if bottom:
        d.add_text(slide, bottom, Inches(0.85), Inches(6.52), Inches(11.65), Inches(0.28), size=14, color=d.BLUE, bold=True, align=PP_ALIGN.CENTER)
    return slide


def two_cards(prs, n, section, title, left, right, bottom=None):
    slide = d.base_slide(prs, section, title, n, TOTAL, 2)
    d.add_card(slide, Inches(0.62), Inches(1.30), Inches(5.86), Inches(4.95), left[0], left[1], icon=left[2], accent=left[3], body_size=14)
    d.add_card(slide, Inches(6.82), Inches(1.30), Inches(5.88), Inches(4.95), right[0], right[1], icon=right[2], accent=right[3], body_size=14)
    if bottom:
        d.add_text(slide, bottom, Inches(0.85), Inches(6.52), Inches(11.65), Inches(0.28), size=14, color=d.BLUE, bold=True, align=PP_ALIGN.CENTER)
    return slide


def lab(prs, n, title, tasks, evidence, stretch, duration):
    slide = d.base_slide(prs, "PRAKTIK", title, n, TOTAL, 2)
    d.add_card(slide, Inches(0.60), Inches(1.25), Inches(7.35), Inches(5.45), "Tugas inti", tasks, icon="LAB", accent=d.CYAN, body_size=14)
    d.add_card(slide, Inches(8.28), Inches(1.25), Inches(4.43), Inches(2.45), "Evidence / DoD", evidence, icon="✓", accent=d.GREEN, body_size=12)
    d.add_card(slide, Inches(8.28), Inches(4.00), Inches(4.43), Inches(2.70), "Stretch challenge", stretch, icon="+", accent=d.GOLD, body_size=12)
    d.add_pill(slide, duration, Inches(10.55), Inches(0.98), Inches(1.82), fill=d.NAVY_2, color=d.CYAN_2, size=9)
    return slide


def build(background: Path) -> Path:
    prs = Presentation()
    prs.slide_width = d.SW
    prs.slide_height = d.SH
    n = 1

    s = d.add_cover(prs, 2, "Flutter UI, CRUD & AI\nDeveloper Workflow", "Scaffold sampai Form, CRUD end-to-end, image/file picker, dan setup OpenCode yang aman.", ["UI", "CRUD", "PICKER", "OPENCODE"], background, TOTAL)
    notes(s, "08.30–08.35", 5, "Menyepakati target Hari 2.", "Tunjukkan tiga tab dan banner simulasi JSONPlaceholder.", "Apa beda response sukses dan persistence?", "Project Hari 2.")
    n += 1

    s = d.add_outcome_slide(prs, 2, n, TOTAL, "Outcome yang harus dapat didemokan", [
        ("UI foundations", ["Scaffold/AppBar", "Row/Column/Form"], "U", d.CYAN),
        ("Public CRUD", ["GET/POST/PUT/DELETE", "Mapper + tests"], "C", d.BLUE),
        ("Picker boundary", ["Image preview", "File metadata"], "P", d.GOLD),
        ("AI setup", ["OpenCode connected", "No key in Flutter"], "A", d.GREEN),
    ])
    notes(s, "08.35–08.45", 10, "Menentukan evidence.", "Minta peserta membedakan UI demo, network evidence, dan secret hygiene.", "Mana yang perlu device test?", "PRD Hari 2.")
    n += 1

    s = d.add_agenda_slide(prs, 2, n, TOTAL, [
        ("08.30", "UI composition", "Scaffold, AppBar, Row, Column, Form"),
        ("10.15", "Public CRUD API", "JSONPlaceholder, mapper, GET/POST/PUT/DELETE"),
        ("13.00", "Image & file picker", "Preview, metadata, lifecycle, scope"),
        ("14.45", "OpenCode & API key", "Install, connect, model, secret boundary"),
        ("16.00", "Challenge & gate", "Tests, demo rubric, handover"),
    ])
    notes(s, "08.45–08.50", 5, "Menjelaskan alokasi 6,5 jam.", "Tandai empat lab dan waktu challenge.", "Checkpoint mana tidak boleh dilewati?", "Rundown Hari 2.")
    n += 1

    s = three_cards(prs, n, "ORIENTASI", "Input Hari 1 → target Hari 2", [
        ("Sudah ada", ["Model Dart", "List/detail", "Local form", "Navigation"], "1", d.CYAN),
        ("Ditambahkan", ["Layered API", "Full CRUD", "Plugin picker", "AI developer tool"], "2", d.BLUE),
        ("Tetap dijaga", ["Validation", "Error state", "No secret", "Reproducible build"], "✓", d.GREEN),
    ], "Hari 2 menghubungkan UI ke contract nyata tanpa mencampur secret atau infrastructure ke widget.")
    notes(s, "08.50–09.00", 10, "Memastikan baseline Hari 1.", "Jalankan smoke list/detail/form lokal sebelum refactor.", "Bagian mana harus tetap bekerja?", "Checkpoint day-1.")
    n += 1

    s = d.add_section_slide(prs, 2, n, TOTAL, "01", "Flutter UI foundations", "Pahami ownership layout dan form sebelum menghubungkannya ke network atau agent.", ["Bangun page shell", "Atur constraints", "Validasi form"])
    notes(s, "09.00–09.02", 2, "Membuka UI foundations.", "Gunakan source aktif, bukan widget terpisah yang tidak dipakai.", "Siapa pemilik state form?", "Flutter widget fundamentals.")
    n += 1

    s = d.base_slide(prs, "UI", "Scaffold adalah shell satu screen", n, TOTAL, 2)
    d.add_flow(s, ["MaterialApp", "Scaffold", "AppBar", "Body", "FAB / NavBar"], Inches(0.62), Inches(1.45), Inches(12.08), descriptions=["theme + route", "page ownership", "title/actions", "main content", "primary/nav intent"])
    d.add_card(s, Inches(0.62), Inches(3.62), Inches(5.85), Inches(2.52), "Scaffold mengelola", ["App bar", "Body/safe area", "Snackbar", "FAB/bottom navigation"], icon="S", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(6.82), Inches(3.62), Inches(5.88), Inches(2.52), "Jangan lakukan", ["Scaffold bertumpuk tanpa alasan", "Request dari build", "Global BuildContext", "Business rule di widget"], icon="×", accent=d.RED, body_size=13)
    notes(s, "09.02–09.15", 13, "Memahami struktur halaman.", "Trace HomeScreen dari MaterialApp hingga FAB.", "Kapan nested Scaffold masuk akal?", "HomeScreen source.")
    n += 1

    s = two_cards(prs, n, "UI", "AppBar: konteks dan aksi yang konsisten", ("Context", ["Judul screen", "Subtitle modul/hari", "Back navigation", "Public demo label"], "C", d.CYAN), ("Actions", ["Refresh hanya di CRUD", "No fake login", "Tooltip", "Disabled saat loading"], "A", d.GOLD), "AppBar tidak menjadi tempat menaruh semua action aplikasi.")
    notes(s, "09.15–09.28", 13, "Mendesain AppBar yang jelas.", "Bandingkan action yang berubah sesuai tab aktif.", "Mengapa refresh tidak muncul di AI Setup?", "Material AppBar.")
    n += 1

    s = d.base_slide(prs, "LAYOUT", "Row dan Column bekerja di dalam constraints", n, TOTAL, 2)
    d.add_table(s, ["Widget", "Main axis", "Risiko", "Countermeasure"], [
        ["Row", "horizontal", "overflow teks", "Expanded/Flexible/Wrap"],
        ["Column", "vertical", "tinggi tak terbatas", "scroll/Expanded"],
        ["ListView", "vertical scroll", "nested scroll", "satu owner scroll"],
        ["Wrap", "flow baris", "urutan visual", "spacing/runSpacing"],
    ], Inches(0.72), Inches(1.42), Inches(11.90), Inches(4.65), widths=[Inches(2.1), Inches(2.25), Inches(3.45), Inches(4.1)], font_size=13)
    d.add_text(s, "Layout Flutter adalah negosiasi constraints: parent memberi batas, child memilih ukuran.", Inches(0.9), Inches(6.42), Inches(11.5), Inches(0.30), size=14, color=d.BLUE, bold=True, align=PP_ALIGN.CENTER)
    notes(s, "09.28–09.43", 15, "Mencegah overflow.", "Gunakan tiga concept card dan kecilkan viewport.", "Mengapa Row di dalam ListView masih bisa overflow?", "Flutter layout constraints.")
    n += 1

    s = d.base_slide(prs, "FORM", "Form mengumpulkan, memvalidasi, lalu mengirim intent", n, TOTAL, 2)
    d.add_code(s, "final formKey = GlobalKey<FormState>();\n\nForm(\n  key: formKey,\n  child: Column(children: [\n    TextFormField(\n      controller: assetController,\n      validator: validateAsset,\n    ),\n    FilledButton(\n      onPressed: submitting ? null : save,\n      child: const Text('Create'),\n    ),\n  ]),\n);", Inches(0.60), Inches(1.25), Inches(6.62), Inches(5.50), label="DART", highlight="VALIDATE BEFORE API", size=11)
    d.add_card(s, Inches(7.52), Inches(1.25), Inches(5.19), Inches(2.42), "Ownership", ["Controller dibuat/dispose", "Form key lokal", "Submit guard"], icon="O", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(7.52), Inches(3.95), Inches(5.19), Inches(2.80), "Validation", ["Client untuk UX", "Server tetap authoritative", "Field error dipetakan", "Input dipertahankan saat gagal"], icon="V", accent=d.GOLD, body_size=13)
    notes(s, "09.43–10.00", 17, "Membuat form deterministik.", "Demo submit kosong, valid, dan double tap.", "Mengapa client validation tidak menggantikan server?", "InspectionFormScreen.")
    n += 1

    s = lab(prs, n, "Lab 1 — compose UI yang responsive", ["Buat Scaffold + AppBar", "Gunakan Row untuk tiga summary card", "Gunakan Column di dalam Card", "Tambahkan Form + validator", "Uji viewport sempit", "Pastikan controller di-dispose"], ["Tidak overflow", "Error form terlihat", "Submit valid mengubah state"], ["Ubah Row menjadi Wrap", "Tambahkan keyboard-safe scroll"], "60 MENIT")
    notes(s, "10.15–11.15", 60, "Menyusun UI foundation.", "Pair work dengan review constraints pada menit 30.", "Widget mana memiliki scroll?", "UiFoundationScreen.")
    n += 1

    s = d.add_section_slide(prs, 2, n, TOTAL, "02", "JSONPlaceholder public CRUD", "Gunakan API publik open-source dan pisahkan schema eksternal melalui mapper yang dapat diuji.", ["Verifikasi endpoint", "Buat mapper", "Jelaskan simulasi"])
    notes(s, "11.15–11.17", 2, "Membuka sesi API.", "Buka endpoint /posts dan source JSONPlaceholder.", "Apa beda simulated write dan persistence?", "jsonplaceholder.typicode.com.")
    n += 1

    s = three_cards(prs, n, "API", "JSONPlaceholder: publik, open-source, tanpa setup", [
        ("Access", ["HTTPS public", "No account", "No API key", "CORS"], "A", d.CYAN),
        ("Contract", ["/posts", "GET/POST/PUT/DELETE", "JSON", "Known status"], "C", d.BLUE),
        ("Boundary", ["Write simulated", "No persistence", "Reset on refresh", "Training only"], "S", d.GOLD),
    ], "Response sukses cukup untuk latihan state—tetapi bukan bukti data tersimpan.")
    notes(s, "11.17–11.30", 13, "Mengenali public API.", "Baca guide dan source MIT JSONPlaceholder.", "Mengapa banner simulasi wajib?", "JSONPlaceholder guide.")
    n += 1

    s = d.base_slide(prs, "SETUP", "Verifikasi public API sebelum Flutter", n, TOTAL, 2)
    d.add_code(s, "BASE=https://jsonplaceholder.typicode.com\n\ncurl \"$BASE/posts?_limit=2\"\n\ncurl -X POST \"$BASE/posts\" \\\n  -H 'Content-Type: application/json' \\\n  -d '{\"title\":\"PMP-900\",\n       \"body\":\"Simulasi\",\n       \"userId\":1}'", Inches(0.60), Inches(1.25), Inches(7.05), Inches(5.48), label="TERMINAL", size=11.2)
    d.add_card(s, Inches(7.95), Inches(1.25), Inches(4.76), Inches(2.42), "Checkpoint", ["GET 200", "POST 201 + id 101", "HTTPS reachable"], icon="✓", accent=d.GREEN, body_size=13)
    d.add_card(s, Inches(7.95), Inches(3.95), Inches(4.76), Inches(2.78), "Default", ["No local server", "No login", "No API key", "Internet required"], icon="URL", accent=d.CYAN, body_size=13)
    notes(s, "11.30–11.43", 13, "Memverifikasi API publik.", "Jalankan curl dan simpan status, bukan credential.", "Apa fallback automated test?", "Per-file tutorial.")
    n += 1

    s = d.base_slide(prs, "STRUCTURE", "Empat operasi, empat file yang bisa dibedah", n, TOTAL, 2)
    d.add_code(s, "lib/src/data/crud/\n\n├── read_inspections.dart\n├── create_inspection.dart\n├── update_inspection.dart\n└── delete_inspection.dart\n\napi_client.dart  // facade", Inches(0.60), Inches(1.25), Inches(6.25), Inches(5.48), label="SOURCE TREE", highlight="ONE INTENT • ONE FILE", size=14)
    d.add_card(s, Inches(7.18), Inches(1.25), Inches(5.53), Inches(2.42), "Urutan bedah", ["1  Read + mapper", "2  Create + payload", "3  Update + stable ID", "4  Delete + confirmation"], icon="4", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(7.18), Inches(3.95), Inches(5.53), Inches(2.78), "Shared helper", ["ApiException", "JsonResponseDecoder", "10-second timeout", "MockClient seam"], icon="S", accent=d.GOLD, body_size=13)
    notes(s, "11.43–11.55", 12, "Mengenalkan struktur CRUD modular.", "Buka empat file secara berurutan; jangan tampilkan seluruh project sekaligus.", "Apa yang layak menjadi helper bersama?", "data/crud + per-file tutorial.")
    n += 1

    s = d.base_slide(prs, "READ", "01 • ReadInspections — GET dan mapping", n, TOTAL, 2)
    d.add_code(s, "Future<List<Inspection>> call() async {\n  final response = await client.get(\n    Uri.parse(\n      '$baseUrl/posts?_limit=20',\n    ),\n  );\n  final posts = JsonResponseDecoder.list(\n    response, expectedStatus: 200,\n  );\n  return posts\n      .map(JsonPlaceholderMapper.fromPost)\n      .toList();\n}", Inches(0.60), Inches(1.20), Inches(7.15), Inches(5.58), label="read_inspections.dart", highlight="GET → LIST → DOMAIN", size=12.4)
    d.add_card(s, Inches(8.05), Inches(1.25), Inches(4.66), Inches(2.42), "Bedah 3 titik", ["URL + query", "Expected 200", "Post → Inspection"], icon="R", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(8.05), Inches(3.95), Inches(4.66), Inches(2.78), "Failure", ["Timeout di boundary", "Invalid JSON typed", "Repository boleh fallback cache"], icon="!", accent=d.RED, body_size=13)
    notes(s, "11.55–12.08", 13, "Membedah operasi Read.", "Buka hanya read_inspections.dart, lalu jalankan test GET.", "Failure mana boleh memakai cache?", "data/crud/read_inspections.dart.")
    n += 1

    s = d.base_slide(prs, "CREATE", "02 • CreateInspection — POST dan payload", n, TOTAL, 2)
    d.add_code(s, "Future<Inspection> call(fields) async {\n  final response = await client.post(\n    Uri.parse('$baseUrl/posts'),\n    headers: const {\n      'Content-Type': 'application/json',\n    },\n    body: jsonEncode(\n      JsonPlaceholderMapper.toPost(fields),\n    ),\n  );\n  final post = JsonResponseDecoder.object(\n    response, expectedStatus: 201,\n  );\n  return JsonPlaceholderMapper.fromPost(post);\n}", Inches(0.60), Inches(1.18), Inches(7.15), Inches(5.60), label="create_inspection.dart", highlight="POST → 201 • SIMULATED", size=11.7)
    d.add_card(s, Inches(7.62), Inches(1.25), Inches(5.09), Inches(2.42), "Before request", ["Form valid", "No double submit", "JSON contract exact"], icon="B", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(7.62), Inches(3.95), Inches(5.09), Inches(2.78), "After request", ["Map response", "Insert local state", "Show SIMULATED", "Reset removes it"], icon="A", accent=d.GOLD, body_size=13)
    notes(s, "13.00–13.13", 13, "Membedah operasi Create.", "Buka create_inspection.dart, inspect payload, lalu refresh untuk membuktikan simulasi.", "Apa evidence persistence nyata?", "data/crud/create_inspection.dart.")
    n += 1

    s = d.base_slide(prs, "UPDATE", "03 • UpdateInspection — PUT dengan stable ID", n, TOTAL, 2)
    d.add_code(s, "Future<Inspection> call(\n  String id, Map<String, dynamic> fields,\n) async {\n  final response = await client.put(\n    Uri.parse('$baseUrl/posts/$id'),\n    headers: const {\n      'Content-Type': 'application/json',\n    },\n    body: jsonEncode(\n      JsonPlaceholderMapper.toPost(fields, id: id),\n    ),\n  );\n  final post = JsonResponseDecoder.object(\n    response, expectedStatus: 200,\n  );\n  return JsonPlaceholderMapper.fromPost(post);\n}", Inches(0.60), Inches(1.12), Inches(7.15), Inches(5.66), label="update_inspection.dart", highlight="PATH ID = PAYLOAD ID", size=10.9)
    d.add_card(s, Inches(8.05), Inches(1.25), Inches(4.66), Inches(2.42), "Before PUT", ["Prefill form", "Validate full body", "Keep stable ID"], icon="B", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(8.05), Inches(3.95), Inches(4.66), Inches(2.78), "After 200", ["Map server result", "Replace same ID", "Preserve list order"], icon="A", accent=d.GOLD, body_size=13)
    notes(s, "13.13–13.26", 13, "Membedah operasi Update.", "Buka update_inspection.dart dan cocokkan ID path dengan payload.", "Mengapa response server mengganti model lokal?", "data/crud/update_inspection.dart.")
    n += 1

    s = d.base_slide(prs, "DELETE", "04 • DeleteInspection — DELETE tanpa model response", n, TOTAL, 2)
    d.add_code(s, "Future<void> call(String id) async {\n  final response = await client.delete(\n    Uri.parse('$baseUrl/posts/$id'),\n  );\n\n  JsonResponseDecoder.empty(\n    response,\n    expectedStatuses: const {200, 204},\n  );\n}\n\n// Controller removes the local item\n// only after this Future succeeds.", Inches(0.60), Inches(1.25), Inches(7.15), Inches(5.48), label="delete_inspection.dart", highlight="DELETE → 200 / 204", size=12.1)
    d.add_card(s, Inches(7.62), Inches(1.25), Inches(5.09), Inches(2.42), "Protect user", ["Name target", "Cancel default", "Disable while request"], icon="P", accent=d.RED, body_size=13)
    d.add_card(s, Inches(7.62), Inches(3.95), Inches(5.09), Inches(2.78), "Handle result", ["200 accepted", "Remove local item", "Banner remains", "Reset restores"], icon="R", accent=d.GREEN, body_size=13)
    notes(s, "13.26–13.39", 13, "Membedah operasi Delete.", "Buka delete_inspection.dart; confirmation tetap concern UI.", "Kapan optimistic delete layak?", "data/crud/delete_inspection.dart.")
    n += 1

    s = d.base_slide(prs, "FACADE", "ApiClient menjaga pemanggilan tetap sederhana", n, TOTAL, 2)
    d.add_code(s, "Future<List<Inspection>> fetchInspections()\n  => read();\n\nFuture<Inspection> createInspection(fields)\n  => create(fields);\n\nFuture<Inspection> updateInspection(id, fields)\n  => update(id, fields);\n\nFuture<void> deleteInspection(id)\n  => delete(id);", Inches(0.60), Inches(1.25), Inches(6.25), Inches(5.48), label="api_client.dart", highlight="FACADE → 4 OPERATIONS", size=13)
    d.add_card(s, Inches(7.18), Inches(1.25), Inches(5.53), Inches(2.42), "Aplikasi memanggil", ["Repository → facade", "Nama intent jelas", "UI tidak tahu HTTP"], icon="A", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(7.18), Inches(3.95), Inches(5.53), Inches(2.78), "Trainer dapat membuka", ["Satu operation file", "Satu MockClient test", "Satu failure scenario"], icon="T", accent=d.GOLD, body_size=13)
    notes(s, "13.39–13.52", 13, "Menjelaskan facade.", "Bandingkan pemanggilan repository dengan isi empat operation file.", "Mengapa facade tidak menjadi god object?", "api_client.dart + data/crud.")
    n += 1

    s = two_cards(prs, n, "SECURITY", "Public API bukan tempat menaruh API key AI", ("JSONPlaceholder", ["No login", "No key", "Public demo data", "HTTPS"], "P", d.CYAN), ("AI provider key", ["Milik tool developer", "Tidak pernah di Flutter", "Quota + rotation", "Redact dari log/prompt"], "K", d.RED), "Endpoint publik dan provider credential mempunyai threat model yang berbeda.")
    notes(s, "13.52–14.05", 13, "Membedakan public API dan secret.", "Pastikan tidak ada fake login atau key di app.", "Mengapa APK tidak dapat menyimpan secret?", "Security baseline.")
    n += 1

    s = three_cards(prs, n, "STATE", "CRUD perlu state dan failure yang eksplisit", [
        ("Read", ["loading", "data/empty", "cached", "error/retry"], "R", d.CYAN),
        ("Write", ["submitting", "success", "simulated", "reset behavior"], "W", d.GOLD),
        ("Delete", ["confirm", "deleting", "200", "local removal"], "D", d.RED),
    ], "Satu bool global tidak cukup menjelaskan semua operasi bersamaan.")
    notes(s, "14.05–14.18", 13, "Memetakan UI state ke operasi.", "Fake 500, timeout, dan invalid JSON melalui MockClient.", "Apa yang terjadi pada write setelah refresh?", "InspectionController.")
    n += 1

    s = lab(prs, n, "Lab 2 — CRUD simulasi end-to-end", ["Curl public /posts", "GET + mapper", "POST simulated", "PUT record terpilih", "DELETE + confirmation", "Reset membuktikan no persistence"], ["Empat method berhasil", "Banner terlihat", "MockClient tests hijau"], ["Tambah badge SIMULATED", "Map /todos tanpa ubah UI"], "90 MENIT")
    notes(s, "14.18–15.48", 90, "Menyelesaikan CRUD simulasi.", "Checkpoint per file: mapper, client, repository, controller, UI.", "Di mana persistence berhenti?", "JSONPLACEHOLDER_PER_FILE.md.")
    n += 1

    s = d.add_section_slide(prs, 2, n, TOTAL, "03", "Image & file picker", "Plugin mengakses capability platform; UI harus menjelaskan apakah file hanya preview atau benar-benar di-upload.", ["Pilih plugin", "Kelola lifecycle", "Jaga scope data"])
    notes(s, "Picker", 2, "Membuka sesi picker.", "Bedakan gambar dan file generik serta batas upload.", "Apa yang pengguna kira terjadi setelah memilih file?", "image_picker/file_picker.")
    n += 1

    s = d.base_slide(prs, "DECISION", "Image picker atau file picker?", n, TOTAL, 2)
    d.add_table(s, ["Kebutuhan", "Gunakan", "Output latihan"], [
        ["Galeri/camera image", "image_picker", "XFile + preview"],
        ["PDF/dokumen/file umum", "file_picker", "PlatformFile + metadata"],
        ["Upload server", "HTTP multipart/storage SDK", "out of scope"],
        ["Persist local", "app documents directory", "out of scope"],
    ], Inches(0.72), Inches(1.42), Inches(11.90), Inches(4.65), widths=[Inches(4.0), Inches(3.15), Inches(4.75)], font_size=13)
    d.add_text(s, "Pilih plugin berdasarkan capability dan contract—bukan popularitas package.", Inches(0.9), Inches(6.42), Inches(11.5), Inches(0.30), size=14, color=d.BLUE, bold=True, align=PP_ALIGN.CENTER)
    notes(s, "Picker", 12, "Memilih picker sesuai kebutuhan.", "Minta peserta mengklasifikasikan foto inspeksi dan PDF sertifikat.", "Kapan satu form memerlukan keduanya?", "pubspec Hari 2.")
    n += 1

    s = d.base_slide(prs, "IMAGE", "Image picker: cancel bukan error", n, TOTAL, 2)
    d.add_code(s, "final selected = await ImagePicker().pickImage(\n  source: ImageSource.gallery,\n  maxWidth: 1600,\n  imageQuality: 82,\n);\n\nif (!mounted || selected == null) return;\nsetState(() {\n  image = selected;\n  file = null;\n});", Inches(0.60), Inches(1.25), Inches(6.72), Inches(5.48), label="DART", highlight="XFILE", size=11.5)
    d.add_card(s, Inches(7.62), Inches(1.25), Inches(5.09), Inches(2.42), "Configuration", ["iOS usage description", "Android plugin setup", "Physical device for camera"], icon="C", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(7.62), Inches(3.95), Inches(5.09), Inches(2.78), "UX", ["Cancel keeps state", "Preview bounded", "Clear action", "Error is actionable"], icon="U", accent=d.GOLD, body_size=13)
    notes(s, "Picker", 13, "Menggunakan image_picker.", "Demo gallery, cancel, dan clear.", "Mengapa cancel tidak perlu snackbar merah?", "InspectionFormScreen.")
    n += 1

    s = d.base_slide(prs, "FILE", "File picker: API versi terbaru dan metadata", n, TOTAL, 2)
    d.add_code(s, "final selected = await FilePicker.pickFile();\nif (!mounted || selected == null) return;\n\nsetState(() {\n  file = selected;\n  image = null;\n});\n\nfinal name = selected.name;\nfinal bytes = selected.lengthSync();", Inches(0.60), Inches(1.25), Inches(6.72), Inches(5.48), label="DART", highlight="FILE_PICKER 13", size=11.5)
    d.add_card(s, Inches(7.62), Inches(1.25), Inches(5.09), Inches(2.42), "Perhatikan versi", ["Baca installed package", "API dapat berubah", "Lockfile disimpan"], icon="V", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(7.62), Inches(3.95), Inches(5.09), Inches(2.78), "Metadata", ["Name", "URI/path mungkin null", "Size mungkin unknown", "Jangan baca file besar sekaligus"], icon="M", accent=d.GOLD, body_size=13)
    notes(s, "Picker", 13, "Menggunakan file_picker terbaru.", "Tekankan perubahan API menjadi static pickFile dan lengthSync nullable.", "Mengapa path tidak selalu tersedia?", "file_picker installed source.")
    n += 1

    s = three_cards(prs, n, "SCOPE", "Selected ≠ persisted ≠ uploaded", [
        ("Selected", ["State lokal", "Preview/name", "Dapat hilang", "Belum server"], "1", d.CYAN),
        ("Persisted", ["Copy storage", "Metadata", "Cleanup", "Privacy"], "2", d.BLUE),
        ("Uploaded", ["Multipart/presigned", "Progress", "Retry/idempotency", "Retention"], "3", d.GOLD),
    ], "UI Hari 2 secara eksplisit menyatakan lampiran belum di-upload.")
    notes(s, "Picker", 12, "Menjaga ekspektasi data.", "Minta peserta menulis label status lampiran.", "Bukti apa yang menunjukkan upload berhasil?", "Picker boundary.")
    n += 1

    s = three_cards(prs, n, "LIFECYCLE", "Picker failure, privacy, dan ownership", [
        ("Lifecycle", ["mounted check", "single active pick", "cancel safe", "dispose owner"], "L", d.CYAN),
        ("Privacy", ["minimum access", "no production photo", "no logging path", "clear policy"], "P", d.RED),
        ("Performance", ["Resize image", "bounded preview", "stream large file", "no bytes in state"], "F", d.GOLD),
    ], "Plugin success di simulator belum membuktikan permission dan device behavior.")
    notes(s, "Picker", 12, "Menangani risiko plugin.", "Uji cancel dan pilih file besar secara terkontrol.", "Apa yang masih perlu physical device?", "Plugin docs.")
    n += 1

    s = lab(prs, n, "Lab 3 — image & file picker", ["Pasang dua package", "Tambahkan iOS usage description", "Pilih image + preview", "Pilih file + metadata", "Cancel dan clear aman", "Label 'belum di-upload' terlihat"], ["No crash", "Tidak ada file bytes di API", "Analyzer/test hijau"], ["Batasi extension/size", "Buat adapter picker yang dapat di-fake"], "60 MENIT")
    notes(s, "Picker", 60, "Mengintegrasikan picker.", "Gunakan form create/update yang sama.", "State apa yang bertahan setelah kembali dari picker?", "Form Hari 2.")
    n += 1

    s = d.add_section_slide(prs, 2, n, TOTAL, "04", "OpenCode & API key AI", "AI coding agent membantu membaca dan mengubah repository; secret dan keputusan engineering tetap dikendalikan manusia.", ["Install & connect", "Protect API key", "Review output"])
    notes(s, "AI", 2, "Membuka sesi OpenCode.", "Tegaskan OpenCode adalah tool developer, bukan fitur Flutter.", "Di mana API key seharusnya berada?", "OpenCode official docs.")
    n += 1

    s = d.base_slide(prs, "INSTALL", "Install OpenCode—pin jalur major untuk kelas", n, TOTAL, 2)
    d.add_code(s, "# OpenCode 1 stable\ncurl -fsSL https://opencode.ai/install | bash\n\n# atau macOS/Linux Homebrew\nbrew install anomalyco/tap/opencode\n\n# atau Node.js\nnpm install -g opencode-ai\n\n# verify\nopencode --version", Inches(0.60), Inches(1.25), Inches(7.05), Inches(5.48), label="TERMINAL", highlight="CHECK OFFICIAL DOCS", size=11)
    d.add_card(s, Inches(7.95), Inches(1.25), Inches(4.76), Inches(2.42), "Sebelum kelas", ["Pilih major version", "Dry-run installer", "Catat version"], icon="P", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(7.95), Inches(3.95), Inches(4.76), Inches(2.78), "Windows", ["WSL recommended", "Work in project folder", "Verify terminal access", "No admin improvisation"], icon="W", accent=d.GOLD, body_size=13)
    notes(s, "AI", 15, "Memasang OpenCode reproducibly.", "Pilih satu installer yang disetujui organisasi.", "Mengapa major version perlu dipin?", "opencode.ai/docs.")
    n += 1

    s = d.base_slide(prs, "CONNECT", "Hubungkan provider, model, lalu init project", n, TOTAL, 2)
    d.add_flow(s, ["opencode", "/connect", "/models", "/init", "Read-only ask"], Inches(0.62), Inches(1.45), Inches(12.08), descriptions=["project root", "enter key privately", "approved model", "review AGENTS.md", "inspect first"])
    d.add_card(s, Inches(0.62), Inches(3.62), Inches(5.85), Inches(2.52), "Checkpoint", ["Version printed", "Provider connected", "Model selectable", "AGENTS.md reviewed"], icon="✓", accent=d.GREEN, body_size=13)
    d.add_card(s, Inches(6.82), Inches(3.62), Inches(5.88), Inches(2.52), "Governance", ["Training account", "Quota/budget", "Retention policy", "Revoke procedure"], icon="G", accent=d.GOLD, body_size=13)
    notes(s, "AI", 15, "Menghubungkan provider.", "Peserta tidak menampilkan key pada projector.", "Siapa owner key training?", "OpenCode providers docs.")
    n += 1

    s = d.base_slide(prs, "SECURITY", "API key tidak boleh masuk Flutter", n, TOTAL, 2)
    d.add_table(s, ["Lokasi", "Aman?", "Alasan / alternatif"], [
        ["Dart constant", "Tidak", "Mudah diekstrak dari app"],
        ["--dart-define", "Tidak untuk secret", "Nilai masuk build"],
        ["Asset/.env bundled", "Tidak", "Terkirim ke pengguna"],
        ["OpenCode /connect", "Tool credential", "Untuk developer workstation"],
        ["Runtime AI production", "Di luar scope", "Butuh arsitektur terpisah"],
    ], Inches(0.62), Inches(1.35), Inches(12.08), Inches(4.95), widths=[Inches(3.4), Inches(2.1), Inches(6.58)], font_size=13)
    d.add_text(s, "Obfuscation menyulitkan pembacaan; tidak mengubah client menjadi secret store.", Inches(0.9), Inches(6.52), Inches(11.5), Inches(0.28), size=14, color=d.RED, bold=True, align=PP_ALIGN.CENTER)
    notes(s, "AI", 15, "Menetapkan secret boundary.", "Minta peserta menemukan lokasi key yang salah dari contoh.", "Apa yang dilakukan bila key ter-commit?", "AI setup doc.")
    n += 1

    s = d.base_slide(prs, "WORKFLOW", "Gunakan agent untuk memahami repo sebelum edit", n, TOTAL, 2)
    d.add_flow(s, ["Ask", "Inspect", "Plan", "Patch", "Verify"], Inches(0.62), Inches(1.45), Inches(12.08), descriptions=["goal + scope", "source + contract", "small steps", "reviewable diff", "format/test/diff"])
    d.add_card(s, Inches(0.62), Inches(3.62), Inches(5.85), Inches(2.52), "Prompt awal", ["Ringkas lib/src", "Temukan CRUD boundaries", "Jangan edit", "Daftar unknown"], icon="P", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(6.82), Inches(3.62), Inches(5.88), Inches(2.52), "Human checkpoint", ["Summary benar", "Scope disetujui", "Diff dibaca", "Tests benar-benar lulus"], icon="H", accent=d.GREEN, body_size=13)
    notes(s, "AI", 15, "Memakai agent secara bertahap.", "Mulai prompt read-only lalu lihat git diff.", "Mengapa summary diperiksa sebelum patch?", "OpenCode workflow.")
    n += 1

    s = two_cards(prs, n, "PROMPT", "Prompt yang membantu, bukan mengambil alih", ("Berikan", ["Goal dan scope", "Files/context", "Acceptance criteria", "Commands", "Output format"], "+", d.GREEN), ("Larangan", ["No secret", "No invented API", "No rewrite massal", "No silent dependency", "No fake test claim"], "—", d.RED), "Agent mempercepat pekerjaan; contract dan keputusan tetap milik tim.")
    notes(s, "AI", 13, "Menulis prompt berkualitas.", "Minta agent menambahkan test untuk satu CRUD failure.", "Constraint mana mencegah scope creep?", "Prompt checklist.")
    n += 1

    s = lab(prs, n, "Lab 4 — OpenCode setup & read-only review", ["Install dan cek version", "Jalankan /connect tanpa menampilkan key", "Pilih model melalui /models", "Jalankan /init; review AGENTS.md", "Minta ringkasan + peta CRUD", "Pastikan tidak ada edit/secret lain"], ["Provider connected", "AGENTS.md direview", "Summary benar; no secret"], ["Minta test plan", "Review satu patch kecil dengan approval"], "45 MENIT")
    notes(s, "AI", 45, "Mengaktifkan AI workflow aman.", "Trainer memeriksa AGENTS.md, secret hygiene, dan git diff.", "Apakah agent mengarang endpoint?", "OPENCODE_AI_SETUP.md.")
    n += 1

    s = d.base_slide(prs, "QUALITY GATE", "Semua layer harus hijau", n, TOTAL, 2)
    d.add_code(s, "# Flutter\nfvm dart format --output=none \\\n  --set-exit-if-changed lib test\nfvm flutter analyze\nfvm flutter test\nfvm flutter build apk --debug\n\n# Public API smoke\ncurl 'https://jsonplaceholder.typicode.com/posts?_limit=1'", Inches(0.60), Inches(1.25), Inches(7.05), Inches(5.48), label="GATE", highlight="APP + PUBLIC CONTRACT", size=11.1)
    d.add_card(s, Inches(7.95), Inches(1.25), Inches(4.76), Inches(2.42), "Evidence", ["8 Flutter tests", "4 HTTP status", "Simulated CRUD demo"], icon="E", accent=d.GREEN, body_size=13)
    d.add_card(s, Inches(7.95), Inches(3.95), Inches(4.76), Inches(2.78), "Manual", ["Picker cancel", "Device permission", "No secret in diff", "API key not in app"], icon="M", accent=d.GOLD, body_size=13)
    notes(s, "Gate", 15, "Menjalankan gate lintas layer.", "Bedakan automated dan manual evidence.", "Apa yang belum dibuktikan test?", "Project READMEs.")
    n += 1

    s = d.base_slide(prs, "CHALLENGE", "Tantangan dan rubrik demo", n, TOTAL, 2)
    d.add_table(s, ["Level", "Challenge", "Evidence"], [
        ["Core", "UI + full CRUD + picker + AI setup", "demo + tests"],
        ["Bronze", "Search/filter dan empty/error", "state evidence"],
        ["Silver", "Picker adapter + fake", "unit/widget test"],
        ["Gold", "Attachment upload PRD", "contract + threat model"],
        ["Platinum", "Agent review skill", "SKILL.md + peer review"],
    ], Inches(0.62), Inches(1.35), Inches(12.08), Inches(4.95), widths=[Inches(2.0), Inches(6.0), Inches(4.08)], font_size=13)
    d.add_text(s, "Demo 7 menit: UI 1 • CRUD 3 • picker 1 • AI security 1 • evidence 1.", Inches(0.9), Inches(6.52), Inches(11.5), Inches(0.28), size=14, color=d.BLUE, bold=True, align=PP_ALIGN.CENTER)
    notes(s, "Demo", 30, "Menilai hasil Hari 2.", "Naik challenge hanya setelah Core lulus.", "Bagian mana belum punya evidence?", "Day2 rubric.")
    n += 1

    s = d.base_slide(prs, "CLOSING", "Build the UI. Respect the contract. Protect the key.", n, TOTAL, 2, bg=d.NAVY)
    d.add_text(s, "day-2", Inches(0.72), Inches(1.15), Inches(4.2), Inches(0.85), size=54, color=d.CYAN, bold=True, font=d.FONT_DISPLAY)
    d.add_text(s, "UI → CRUD → Picker → AI workflow", Inches(0.75), Inches(2.08), Inches(7.0), Inches(0.46), size=25, color=d.WHITE, bold=True)
    d.add_code(s, "fvm flutter analyze\nfvm flutter test\nfvm flutter build apk --debug\n\ngit diff --check\ngit commit -m \"Use JSONPlaceholder CRUD simulation\"", Inches(0.75), Inches(2.82), Inches(6.15), Inches(3.12), label="FINAL CHECKPOINT", size=11.2)
    d.add_card(s, Inches(7.25), Inches(1.15), Inches(5.38), Inches(4.79), "Bawa ke Hari 3", ["Flutter UI structure", "CRUD contract", "Picker boundary", "OpenCode connected", "Secret discipline"], icon="✓", accent=d.CYAN, fill=d.NAVY_2, body_size=14)
    d.add_text(s, "Rujukan: docs.flutter.dev • jsonplaceholder.typicode.com • opencode.ai/docs • pub.dev", Inches(0.75), Inches(6.52), Inches(11.85), Inches(0.28), size=10, color=d.CYAN_2, align=PP_ALIGN.CENTER)
    d.add_text(s, f"{n:02d} / {TOTAL:02d}", Inches(11.62), Inches(6.90), Inches(0.95), Inches(0.22), size=10, color=d.CYAN_2, bold=True, align=PP_ALIGN.RIGHT)
    notes(s, "Closing", 5, "Menutup dengan checkpoint.", "Minta peserta menyebut satu contract dan satu secret boundary.", "Apa fondasi yang dipakai untuk migrasi Hari 3?", "Flutter/OpenCode official docs.")

    assert len(prs.slides) == TOTAL, (len(prs.slides), TOTAL)
    out = ROOT / "Hari_2_Flutter_Professional.pptx"
    prs.save(out)
    shutil.copy2(out, ROOT / "PPT_Training" / "Hari_2_Architecture_API_State_Storage.pptx")
    shutil.copy2(out, ROOT / "PPT_Training" / "Hari_2_UI_CRUD_OpenCode_Picker.pptx")
    return out


def main():
    original = ROOT / "Hari_2_Flutter_Professional.pptx"
    backup = ROOT / "Hari_2_Flutter_Professional_sebelum_CRUD_AI_Picker.pptx"
    if original.exists() and not backup.exists():
        shutil.copy2(original, backup)
    with tempfile.TemporaryDirectory(prefix="dpl-day2-crud-ai-") as temp_name:
        background = d.prepare_cover_background(Path(temp_name))
        out = build(background)
    print(f"Built {out}")
    print(f"Slides: {TOTAL}; backup: {backup.name}")


if __name__ == "__main__":
    main()
