#!/usr/bin/env python3
"""Build Day 3 deck: Kotlin migration PRD, Agent Skill, and bounded WebView."""

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
    slide = d.base_slide(prs, section, title, n, TOTAL, 3)
    for i, (heading, items, icon, accent) in enumerate(cards):
        d.add_card(slide, Inches(0.62 + i * 4.16), Inches(1.30), Inches(3.78), Inches(4.95), heading, items, icon=icon, accent=accent, body_size=13)
    if bottom:
        d.add_text(slide, bottom, Inches(0.85), Inches(6.52), Inches(11.65), Inches(0.28), size=14, color=d.BLUE, bold=True, align=PP_ALIGN.CENTER)
    return slide


def two_cards(prs, n, section, title, left, right, bottom=None):
    slide = d.base_slide(prs, section, title, n, TOTAL, 3)
    d.add_card(slide, Inches(0.62), Inches(1.30), Inches(5.86), Inches(4.95), left[0], left[1], icon=left[2], accent=left[3], body_size=14)
    d.add_card(slide, Inches(6.82), Inches(1.30), Inches(5.88), Inches(4.95), right[0], right[1], icon=right[2], accent=right[3], body_size=14)
    if bottom:
        d.add_text(slide, bottom, Inches(0.85), Inches(6.52), Inches(11.65), Inches(0.28), size=14, color=d.BLUE, bold=True, align=PP_ALIGN.CENTER)
    return slide


def lab(prs, n, title, tasks, evidence, stretch, duration):
    slide = d.base_slide(prs, "PRAKTIK", title, n, TOTAL, 3)
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

    s = d.add_cover(prs, 3, "Flutter WebView &\nKotlin Migration Lab", "PRD vertical slice, Agent Skill, WebView boundary, dan evidence migrasi yang dapat direview.", ["PRD", "KOTLIN → FLUTTER", "WEBVIEW", "AGENT SKILL"], background, TOTAL)
    notes(s, "08.30–08.35", 5, "Menyepakati hasil Hari 3.", "Preview empat tab Migration Lab dan artefak handover.", "Apa beda rewrite dan vertical slice?", "Project Hari 3.")
    n += 1

    s = d.add_outcome_slide(prs, 3, n, TOTAL, "Outcome yang harus dapat dibuktikan", [
        ("Behavior map", ["Legacy evidence", "Unknown list"], "B", d.CYAN),
        ("PRD slice", ["AC + evidence", "Out of scope"], "P", d.BLUE),
        ("Bounded WebView", ["Situs latihan", "HTTPS allowlist"], "W", d.GOLD),
        ("Agent Skill", ["Repeatable flow", "Human gate"], "A", d.GREEN),
    ])
    notes(s, "08.35–08.45", 10, "Menentukan evidence.", "Minta peserta membedakan code, parity, security, dan build evidence.", "Mana yang tetap perlu device test?", "PRD Hari 3.")
    n += 1

    s = d.add_agenda_slide(prs, 3, n, TOTAL, [
        ("08.30", "Inventory legacy", "Behavior, state, navigation, unknown"),
        ("09.15", "PRD vertical slice", "Acceptance → evidence matrix"),
        ("10.15", "Kotlin → Flutter", "UI, state, data, lifecycle mapping"),
        ("11.15", "Agent Skill", "Context, prompt, review gate"),
        ("13.00", "WebView & lab", "Bounded implementation, tests, build"),
    ])
    notes(s, "08.45–08.50", 5, "Menjelaskan alokasi 6,5 jam.", "Tandai empat challenge dan checkpoint.", "Blok mana tidak boleh dilewati?", "Rundown Hari 3.")
    n += 1

    s = three_cards(prs, n, "ORIENTASI", "Masalah migrasi bukan sekadar syntax", [
        ("Behavior loss", ["Hidden state", "Back behavior", "Error path", "Side effect"], "1", d.RED),
        ("Contract drift", ["Endpoint berubah", "DTO diasumsikan", "Storage beda", "Unknown disamarkan"], "2", d.GOLD),
        ("False done", ["UI terlihat", "No parity", "No device test", "No gap register"], "3", d.CYAN),
    ], "Migrasi selesai ketika outcome terukur setara—bukan ketika screen baru tampak mirip.")
    notes(s, "08.50–09.00", 10, "Membangun migration mindset.", "Gunakan satu contoh behavior tersembunyi dari app Kotlin.", "Apa yang screenshot tidak buktikan?", "Migration PRD.")
    n += 1

    s = d.add_section_slide(prs, 3, n, TOTAL, "01", "Inventory legacy Kotlin", "Baca seperlunya, catat perilaku teramati, dan pisahkan fakta dari unknown.", ["Pilih slice", "Trace behavior", "Buat evidence"])
    notes(s, "09.00–09.02", 2, "Membuka inventory.", "Mulai dari user flow, bukan folder demi folder.", "Apa entry point slice?", "Legacy sample.")
    n += 1

    s = three_cards(prs, n, "INVENTORY", "File minimum untuk satu slice", [
        ("Presentation", ["Activity/Fragment", "XML/RecyclerView", "Navigation graph", "Permission"], "UI", d.CYAN),
        ("State", ["ViewModel", "LiveData/Flow", "Saved state", "Lifecycle"], "S", d.BLUE),
        ("Data", ["Retrofit/DTO", "Repository", "Database/prefs", "Tests"], "D", d.GOLD),
    ], "Ambil hanya file yang memengaruhi behavior slice; context berlebih menambah noise dan risiko.")
    notes(s, "09.02–09.15", 13, "Memilih source relevan.", "Minta peserta menandai entry, state owner, dan side effect.", "File mana hanya dekorasi?", "Legacy inventory.")
    n += 1

    s = d.base_slide(prs, "TRACE", "Trace behavior dari trigger sampai evidence", n, TOTAL, 3)
    d.add_flow(s, ["User trigger", "UI state", "ViewModel", "Repository", "Effect/result"], Inches(0.62), Inches(1.45), Inches(12.08), descriptions=["tap/open", "loading/error", "intent", "API/storage", "navigation/data"])
    d.add_card(s, Inches(0.62), Inches(3.62), Inches(5.85), Inches(2.52), "Catat", ["Input/output", "State transition", "Error path", "Back/restart"], icon="+", accent=d.GREEN, body_size=13)
    d.add_card(s, Inches(6.82), Inches(3.62), Inches(5.88), Inches(2.52), "Jangan simpulkan", ["Nama class = contract", "No test = no behavior", "UI sama = parity", "Agent tahu domain"], icon="—", accent=d.RED, body_size=13)
    notes(s, "09.15–09.28", 13, "Membuat behavior trace.", "Trace tap item sampai detail dan kembali.", "Di mana request dapat terulang?", "Behavior map.")
    n += 1

    s = two_cards(prs, n, "SOURCE OF TRUTH", "Fakta, inference, dan unknown", ("Fakta", ["Contract disetujui", "Test hijau", "Observed behavior", "Product decision"], "F", d.GREEN), ("Unknown / inference", ["Label asumsi", "Cari evidence", "Tanya owner", "Block bila material"], "?", d.GOLD), "Unknown yang dicatat lebih aman daripada contract yang dikarang.")
    notes(s, "09.28–09.40", 12, "Memisahkan evidence.", "Tandai tiap temuan F/I/U.", "Kapan unknown memblokir implementasi?", "Trace worksheet.")
    n += 1

    s = d.base_slide(prs, "SLICE", "Vertical slice menjaga migrasi tetap selesai", n, TOTAL, 3)
    d.add_flow(s, ["List trigger", "GET contract", "List state", "Detail route", "Parity evidence"], Inches(0.62), Inches(1.45), Inches(12.08), descriptions=["entry", "unchanged", "all states", "stable ID", "AC + test"])
    d.add_card(s, Inches(0.62), Inches(3.62), Inches(5.85), Inches(2.52), "Masuk slice", ["One user outcome", "UI + state + data", "Failure path", "Reviewable diff"], icon="IN", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(6.82), Inches(3.62), Inches(5.88), Inches(2.52), "Di luar slice", ["All screens", "API contract rewrite", "New auth", "Broad refactor"], icon="OUT", accent=d.RED, body_size=13)
    notes(s, "09.40–09.50", 10, "Memotong scope.", "Pilih list→detail sebagai slice kelas.", "Apa dependency minimum slice?", "PRD slice.")
    n += 1

    s = lab(prs, n, "Lab 1 — legacy behavior map", ["Pilih daftar→detail", "Temukan source Kotlin/XML", "Trace state + data", "Catat back/restart", "Tandai F/I/U", "Buat unknown list"], ["1-page map", "Source references", "No invented behavior"], ["Trace error/offline", "Bandingkan dua implementation"], "45 MENIT")
    notes(s, "09.50–10.35", 45, "Membuat behavior map.", "Review berpasangan dengan pertanyaan evidence.", "Temuan mana masih unknown?", "Behavior map template.")
    n += 1

    s = d.add_section_slide(prs, 3, n, TOTAL, "02", "PRD untuk migrasi", "Ubah behavior menjadi acceptance yang dapat dinilai dan ditelusuri.", ["Define outcome", "Write AC", "Map evidence"])
    notes(s, "10.35–10.37", 2, "Membuka PRD.", "Hubungkan behavior map ke keputusan produk.", "Siapa menyetujui parity?", "PRD Hari 3.")
    n += 1

    s = three_cards(prs, n, "PRD", "Anatomi PRD slice yang bisa dieksekusi", [
        ("Why", ["Problem", "User outcome", "Source of truth", "Risk"], "W", d.CYAN),
        ("What", ["In scope", "Out of scope", "Dependencies", "Constraints"], "T", d.BLUE),
        ("Proof", ["Acceptance", "Evidence", "Owner", "Next slice"], "P", d.GOLD),
    ], "PRD bukan dokumentasi setelah coding; PRD adalah batas keputusan sebelum patch.")
    notes(s, "10.37–10.50", 13, "Menulis PRD minimum.", "Buka PRD_MIGRASI_KOTLIN.md.", "Bagian mana mengurangi scope creep?", "Project PRD.")
    n += 1

    s = two_cards(prs, n, "ACCEPTANCE", "Acceptance harus observable", ("Baik", ["Given/when/then", "Status terlihat", "ID/contract eksplisit", "Pass/fail jelas"], "✓", d.GREEN), ("Lemah", ["UI modern", "Mirip Kotlin", "Lebih cepat", "Berfungsi baik"], "×", d.RED), "Jika reviewer masih perlu menebak, acceptance belum cukup spesifik.")
    notes(s, "10.50–11.02", 12, "Memperbaiki AC.", "Ubah satu kalimat lemah menjadi skenario terukur.", "Bukti apa yang dibutuhkan AC?", "PRD acceptance.")
    n += 1

    s = d.base_slide(prs, "TRACEABILITY", "Satu garis dari behavior sampai evidence", n, TOTAL, 3)
    d.add_table(s, ["Legacy behavior", "PRD AC", "Flutter target", "Evidence"], [
        ["Tap item ID 42", "AC2", "detail route 42", "widget test"],
        ["Load gagal", "AC3", "error + retry", "fake repository"],
        ["Back preserves list", "AC4", "Navigator pop", "smoke test"],
        ["External URL denied", "WV3", "NavigationDelegate", "device demo"],
    ], Inches(0.52), Inches(1.38), Inches(12.28), Inches(4.72), widths=[Inches(3.0), Inches(1.45), Inches(3.65), Inches(4.18)], font_size=13)
    d.add_text(s, "Traceability membuat review agent output dan parity lebih objektif.", Inches(0.9), Inches(6.42), Inches(11.5), Inches(0.30), size=14, color=d.BLUE, bold=True, align=PP_ALIGN.CENTER)
    notes(s, "11.02–11.15", 13, "Membangun matriks.", "Isi satu baris dari hasil lab.", "AC mana belum punya evidence?", "Traceability matrix.")
    n += 1

    s = three_cards(prs, n, "RISK", "Risiko dan keputusan sebelum coding", [
        ("Product", ["Parity ambiguity", "Scope growth", "Owner absent", "Rollout"], "P", d.GOLD),
        ("Technical", ["Lifecycle", "API drift", "Back/session", "Platform plugin"], "T", d.CYAN),
        ("Security", ["WebView origin", "JS bridge", "Secret", "PII in prompt"], "S", d.RED),
    ], "Risiko material tanpa owner bukan detail implementasi—itu blocker keputusan.")
    notes(s, "11.15–11.27", 12, "Mengidentifikasi risiko.", "Beri owner dan mitigation pada tiga risiko.", "Risiko mana harus diputus sebelum agent bekerja?", "Risk register.")
    n += 1

    s = lab(prs, n, "Challenge 1 — tulis PRD slice", ["Tulis problem + outcome", "Tetapkan source of truth", "Batasi in/out scope", "Tulis 5+ AC", "Map AC ke evidence", "Tambahkan risk/owner"], ["Reviewer dapat pass/fail", "No vague AC", "Unknown tetap terlihat"], ["Tambah rollout/rollback", "Review silang tim"], "45 MENIT")
    notes(s, "11.27–12.12", 45, "Menyelesaikan PRD.", "Gunakan peer review; trainer hanya mengklarifikasi contract.", "AC mana masih ambigu?", "PRD Hari 3.")
    n += 1

    s = d.add_section_slide(prs, 3, n, TOTAL, "03", "Kotlin → Flutter mapping", "Petakan responsibility dan lifecycle; jangan menyalin class satu banding satu.", ["Map UI", "Map state/data", "Preserve behavior"])
    notes(s, "13.00–13.02", 2, "Membuka mapping.", "Bandingkan architecture sebagai responsibility.", "Apa yang harus tetap sama?", "Migration map.")
    n += 1

    s = d.base_slide(prs, "UI MAP", "Activity / Fragment / XML → route dan widget tree", n, TOTAL, 3)
    d.add_table(s, ["Kotlin", "Flutter", "Yang diperiksa"], [
        ["Activity/Fragment", "Screen + route", "entry, back, lifecycle"],
        ["XML layout", "Widget tree", "constraints, semantics"],
        ["RecyclerView", "ListView.builder", "key, lazy build"],
        ["ViewBinding", "typed widget refs/state", "ownership/dispose"],
    ], Inches(0.62), Inches(1.35), Inches(12.08), Inches(4.95), widths=[Inches(3.2), Inches(3.7), Inches(5.18)], font_size=13)
    d.add_text(s, "Targetnya behavior parity—bukan class parity.", Inches(0.9), Inches(6.52), Inches(11.5), Inches(0.28), size=14, color=d.BLUE, bold=True, align=PP_ALIGN.CENTER)
    notes(s, "13.02–13.15", 13, "Memetakan presentation layer.", "Trace list screen source Hari 3.", "Di mana stable ID dipakai?", "Flutter target.")
    n += 1

    s = two_cards(prs, n, "STATE", "ViewModel/LiveData → state owner yang eksplisit", ("Legacy", ["ViewModel", "LiveData/Flow", "SavedStateHandle", "Coroutine scope"], "K", d.BLUE), ("Flutter", ["Controller/state", "Stream/Notifier", "Route state", "mounted/dispose"], "F", d.CYAN), "Pilih mekanisme sesuai kebutuhan; jangan menambah state library hanya agar mapping terlihat modern.")
    notes(s, "13.15–13.28", 13, "Memetakan state/lifecycle.", "Tentukan kapan load, refresh, dan dispose.", "State apa harus survive restart?", "State mapping.")
    n += 1

    s = d.base_slide(prs, "DATA", "Retrofit → ApiClient tanpa contract drift", n, TOTAL, 3)
    d.add_flow(s, ["Retrofit annotation", "HTTP contract", "ApiClient", "Repository", "Typed model"], Inches(0.62), Inches(1.45), Inches(12.08), descriptions=["observed", "source of truth", "method/status", "policy", "strict mapping"])
    d.add_card(s, Inches(0.62), Inches(3.62), Inches(5.85), Inches(2.52), "Preserve", ["Path/method", "Headers/auth", "Payload/nullability", "Error semantics"], icon="=", accent=d.GREEN, body_size=13)
    d.add_card(s, Inches(6.82), Inches(3.62), Inches(5.88), Inches(2.52), "Escalate", ["Ambiguous field", "Undocumented status", "Legacy workaround", "PII/logging"], icon="!", accent=d.GOLD, body_size=13)
    notes(s, "13.28–13.41", 13, "Menjaga API contract.", "Bandingkan OpenAPI dan model target.", "Perbedaan mana bug versus product decision?", "OpenAPI.")
    n += 1

    s = three_cards(prs, n, "LIFECYCLE", "Navigation, storage, dan platform boundary", [
        ("Navigation", ["Back result", "Deep link", "Stable ID", "Duplicate route"], "N", d.CYAN),
        ("Storage", ["Session", "Cache", "Logout cleanup", "Migration version"], "S", d.BLUE),
        ("Platform", ["Permission", "Plugin", "Activity loss", "Device test"], "P", d.GOLD),
    ], "Hal kecil pada lifecycle sering menjadi parity gap terbesar.")
    notes(s, "13.41–13.54", 13, "Memetakan boundary.", "Gunakan PhotoPanel sebagai contoh plugin lifecycle.", "Apa yang widget test tidak buktikan?", "Day3 source.")
    n += 1

    s = two_cards(prs, n, "ANTI-PATTERN", "Hindari dua ekstrem migrasi", ("Copy architecture", ["Satu class = satu class", "XML diterjemahkan literal", "Legacy debt ikut", "No Flutter idiom"], "C", d.RED), ("Rewrite tanpa evidence", ["Contract berubah", "Hidden behavior hilang", "Scope tak terkendali", "No parity proof"], "R", d.RED), "Responsibility dipetakan; struktur target dipilih secara sadar dan dibuktikan.")
    notes(s, "13.54–14.06", 12, "Mengenali anti-pattern.", "Review satu mapping yang terlalu literal.", "Apa keputusan target yang harus didokumentasikan?", "Migration review.")
    n += 1

    s = lab(prs, n, "Lab 2 — architecture mapping", ["Map UI/navigation", "Map state/lifecycle", "Map Retrofit/repository", "Map storage/session", "Tandai parity risk", "Pilih target files"], ["1 map per layer", "Contract unchanged", "Risiko punya owner"], ["Buat sequence diagram", "Tambah rollback plan"], "60 MENIT")
    notes(s, "14.06–15.06", 60, "Menyelesaikan mapping.", "Review target files sebelum patch.", "Responsibility mana belum punya owner?", "Migration map.")
    n += 1

    s = d.add_section_slide(prs, 3, n, TOTAL, "04", "Agent Skill", "Kemas workflow migrasi sebagai instruksi reusable, bukan prompt sekali pakai.", ["Discover skill", "Prepare context", "Review evidence"])
    notes(s, "Agent", 2, "Membuka Agent Skill.", "Tunjukkan file skill nyata pada repo.", "Apa yang skill standardisasi?", "SKILL.md.")
    n += 1

    s = d.base_slide(prs, "AGENT SKILL", "Skill nyata di dalam repository", n, TOTAL, 3)
    d.add_code(s, ".agents/skills/\n  migrate-kotlin-slice/\n    SKILL.md\n\n---\nname: migrate-kotlin-slice\ndescription: Migrate one Kotlin slice\n---\n\n# Workflow\n1. Read PRD + source\n2. List facts + unknowns\n3. Map AC → file/test\n4. Patch one small slice\n5. Verify and report gaps", Inches(0.60), Inches(1.20), Inches(6.45), Inches(5.55), label="SKILL.md", highlight="ONE SLICE • HUMAN REVIEW", size=11.5)
    d.add_card(s, Inches(7.38), Inches(1.20), Inches(5.33), Inches(2.48), "Membakukan", ["Input minimum", "Urutan kerja", "Guardrail", "Output/evidence"], icon="S", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(7.38), Inches(3.95), Inches(5.33), Inches(2.80), "Tidak menggantikan", ["PRD approval", "Domain owner", "Diff review", "Device test"], icon="H", accent=d.GOLD, body_size=13)
    notes(s, "Agent", 15, "Memahami skill structure.", "Buka SKILL.md dan validasi frontmatter.", "Apa beda skill dan prompt?", "OpenCode skills docs.")
    n += 1

    s = three_cards(prs, n, "CONTEXT", "Context pack minimum dan aman", [
        ("Include", ["PRD slice", "Relevant Kotlin/XML", "OpenAPI", "Target + tests"], "+", d.GREEN),
        ("Exclude", [".env/key/token", "Keystore", "User dump", "Unrelated repo"], "—", d.RED),
        ("Annotate", ["Source of truth", "Unknown", "Constraints", "Expected evidence"], "i", d.CYAN),
    ], "Context hygiene meningkatkan akurasi sekaligus menurunkan security exposure.")
    notes(s, "Agent", 13, "Menyiapkan context.", "Sanitasi file sebelum prompt.", "File mana tidak perlu agent lihat?", "AI playbook.")
    n += 1

    s = two_cards(prs, n, "PROMPT", "Prompt mengikat agent ke PRD", ("Berikan", ["Goal satu slice", "Source of truth", "Target files", "Acceptance/evidence", "Commands"], "+", d.GREEN), ("Larangan", ["No invented contract", "No secret", "No broad rewrite", "No host/bridge expansion", "No fake tests"], "—", d.RED), "Minta plan dan unknown sebelum mengizinkan patch.")
    notes(s, "Agent", 13, "Menulis prompt terkontrol.", "Gunakan contoh pada screen Agent Skill.", "Constraint mana mencegah WebView melebar?", "AI playbook.")
    n += 1

    s = d.base_slide(prs, "HUMAN GATE", "Agent output harus melewati review manusia", n, TOTAL, 3)
    d.add_flow(s, ["Read-only summary", "Plan", "Patch", "Diff review", "Evidence"], Inches(0.62), Inches(1.45), Inches(12.08), descriptions=["facts/unknown", "AC mapping", "small", "contract/security", "commands + gaps"])
    d.add_card(s, Inches(0.62), Inches(3.62), Inches(5.85), Inches(2.52), "Reject jika", ["Endpoint dikarang", "Scope melebar", "Secret tampil", "Tests tidak dijalankan"], icon="×", accent=d.RED, body_size=13)
    d.add_card(s, Inches(6.82), Inches(3.62), Inches(5.88), Inches(2.52), "Accept jika", ["AC trace jelas", "Patch reviewable", "Gate hijau", "Gap jujur"], icon="✓", accent=d.GREEN, body_size=13)
    notes(s, "Agent", 13, "Menetapkan approval flow.", "Simulasikan output agent yang perlu ditolak.", "Siapa bertanggung jawab atas merge?", "Review checklist.")
    n += 1

    s = lab(prs, n, "Lab 3 — jalankan Agent Skill", ["Pastikan skill terdeteksi", "Berikan context minimum", "Minta facts/unknown", "Review plan", "Izinkan patch kecil", "Review diff + tests"], ["Skill path nyata", "No secret", "AC/evidence report"], ["Tambah test failure", "Peer-review agent output"], "45 MENIT")
    notes(s, "Agent", 45, "Memakai skill.", "Trainer mengaudit diff dan klaim test.", "Agent mengarang apa?", "migrate-kotlin-slice skill.")
    n += 1

    s = d.add_section_slide(prs, 3, n, TOTAL, "05", "Bounded WebView", "Gunakan WebView sebagai surface terdefinisi dengan origin, navigation, session, dan security policy.", ["Create controller", "Load training site", "Block external"])
    notes(s, "WebView", 2, "Membuka WebView.", "Tegaskan satu situs HTTPS, exact-host allowlist, dan tanpa JS bridge.", "Mengapa WebView bukan shortcut migrasi?", "WebView source.")
    n += 1

    s = d.base_slide(prs, "WEBVIEW", "Pisahkan policy, controller, dan screen", n, TOTAL, 3)
    d.add_code(s, "lib/src/\n├── webview/\n│   ├── navigation_policy.dart\n│   └── migration_webview_controller.dart\n└── screens/\n    └── training_webview_screen.dart\n\nURL:\nhttps://www.presisirencar.com/", Inches(0.60), Inches(1.25), Inches(6.25), Inches(5.48), label="SOURCE TREE", highlight="POLICY • BEHAVIOR • UI", size=13.2)
    d.add_card(s, Inches(7.18), Inches(1.25), Inches(5.53), Inches(2.42), "Bisa diuji cepat", ["Policy: unit test", "Screen: widget state", "Controller: device smoke"], icon="T", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(7.18), Inches(3.95), Inches(5.53), Inches(2.78), "Ownership jelas", ["Policy memilih URL", "Controller mengatur WebView", "Screen render progress/error"], icon="O", accent=d.GOLD, body_size=13)
    notes(s, "WebView", 15, "Mengenalkan struktur WebView modular.", "Buka tiga file satu per satu, dimulai dari policy yang paling kecil.", "Bagian mana dapat diuji tanpa device?", "lib/src/webview + TrainingWebViewScreen.")
    n += 1

    s = d.base_slide(prs, "CONTROLLER", "Controller: satu URL, state jelas", n, TOTAL, 3)
    d.add_code(s, "const trainingWebsiteUrl =\n  'https://www.presisirencar.com/';\n\nreturn WebViewController()\n  ..setJavaScriptMode(\n    JavaScriptMode.unrestricted,\n  )\n  ..setNavigationDelegate(\n    NavigationDelegate(\n      onProgress: onProgress,\n      onNavigationRequest: decide,\n      onWebResourceError: handleError,\n    ),\n  )\n  ..loadRequest(\n    Uri.parse(trainingWebsiteUrl),\n  );", Inches(0.60), Inches(1.18), Inches(7.15), Inches(5.60), label="migration_webview_controller.dart", highlight="ONE URL • NO JS BRIDGE", size=11.3)
    d.add_card(s, Inches(8.05), Inches(1.25), Inches(4.66), Inches(2.42), "Keputusan", ["HTTPS only", "JS untuk Next.js", "No JS bridge"], icon="L", accent=d.CYAN, body_size=13)
    d.add_card(s, Inches(8.05), Inches(3.95), Inches(4.66), Inches(2.78), "States", ["Progress", "Main-frame error", "Reload", "Blocked URL"], icon="S", accent=d.GOLD, body_size=13)
    notes(s, "WebView", 13, "Membedah controller factory.", "Buka migration_webview_controller.dart lalu cocokkan callback ke screen.", "Apa yang berubah bila URL remote?", "webview_flutter controller API.")
    n += 1

    s = d.base_slide(prs, "POLICY", "Default deny: HTTPS + exact host", n, TOTAL, 3)
    d.add_code(s, "static const allowedHosts = {\n  'presisirencar.com',\n  'www.presisirencar.com',\n};\n\nstatic bool allows(String rawUrl) {\n  if (rawUrl == 'about:blank') return true;\n  final uri = Uri.tryParse(rawUrl);\n  return uri != null &&\n      uri.scheme == 'https' &&\n      allowedHosts.contains(\n        uri.host.toLowerCase(),\n      );\n}\n\n// http, file, javascript, external → false", Inches(0.60), Inches(1.25), Inches(7.15), Inches(5.48), label="navigation_policy.dart", highlight="PURE FUNCTION • UNIT TEST", size=10.8)
    d.add_card(s, Inches(8.05), Inches(1.25), Inches(4.66), Inches(2.42), "Baseline lab", ["2 exact hosts", "External prevent", "No JavaScript bridge"], icon="✓", accent=d.GREEN, body_size=13)
    d.add_card(s, Inches(8.05), Inches(3.95), Inches(4.66), Inches(2.78), "Test negatif", ["HTTP", "Fake subdomain", "file/javascript"], icon="!", accent=d.RED, body_size=13)
    notes(s, "WebView", 15, "Membedah policy default-deny.", "Jalankan unit test untuk dua host, HTTP, fake subdomain, file, dan javascript.", "Mengapa pencocokan string URL berbahaya?", "navigation_policy.dart + WebView security.")
    n += 1

    s = three_cards(prs, n, "LIFECYCLE", "Back, session, dan failure harus eksplisit", [
        ("Back", ["canGoBack", "Navigator pop", "No trap", "Deep link"], "B", d.CYAN),
        ("Session", ["Cookie owner", "Logout cleanup", "Expiry", "SSO policy"], "S", d.GOLD),
        ("Failure", ["TLS", "Offline", "Render crash", "Retry/report"], "F", d.RED),
    ], "WebView yang memuat halaman belum berarti journey pengguna selesai.")
    notes(s, "WebView", 12, "Mendesain lifecycle.", "Diskusikan Android back pada history kosong/berisi.", "Apa yang dibersihkan saat logout?", "WebView PRD.")
    n += 1

    s = lab(prs, n, "Lab 4 — WebView boundary", ["Load presisirencar.com", "Show progress/error", "Apply HTTPS allowlist", "Block external URL", "Add reload", "Define back behavior"], ["Site tampil", "External denied", "No key/bridge"], ["Test fake subdomain", "Document session policy"], "60 MENIT")
    notes(s, "WebView", 60, "Mengimplementasikan WebView aman.", "Uji pada emulator/device karena platform view.", "Evidence mana manual?", "TrainingWebViewScreen.")
    n += 1

    s = d.base_slide(prs, "TEST", "Portfolio test mengikuti risiko migrasi", n, TOTAL, 3)
    d.add_table(s, ["Level", "Membuktikan", "Contoh"], [
        ["Unit", "mapping/validator", "DTO, rule"],
        ["Widget", "screen state/navigation", "PRD/skill UI"],
        ["Contract", "HTTP parity", "OpenAPI fixtures"],
        ["Device", "WebView/plugin/back", "external denied"],
        ["Build", "toolchain integration", "APK debug"],
    ], Inches(0.62), Inches(1.35), Inches(12.08), Inches(4.95), widths=[Inches(2.4), Inches(4.3), Inches(5.38)], font_size=13)
    d.add_text(s, "Satu jenis test tidak membuktikan seluruh vertical slice.", Inches(0.9), Inches(6.52), Inches(11.5), Inches(0.28), size=14, color=d.BLUE, bold=True, align=PP_ALIGN.CENTER)
    notes(s, "Quality", 13, "Memilih test sesuai risiko.", "Map setiap AC ke satu evidence minimal.", "Apa yang butuh device?", "Test matrix.")
    n += 1

    s = d.base_slide(prs, "QUALITY GATE", "Format, analyze, test, build, review gap", n, TOTAL, 3)
    d.add_code(s, "cd flutter_projects/\n  hari_3_dpl_inspection_release\n\nfvm dart format --output=none \\\n  --set-exit-if-changed lib test\nfvm flutter analyze\nfvm flutter test\nfvm flutter build apk --debug\n\n# then: device smoke + git diff", Inches(0.60), Inches(1.25), Inches(7.05), Inches(5.48), label="GATE", highlight="EVIDENCE, NOT CLAIM", size=11)
    d.add_card(s, Inches(7.95), Inches(1.25), Inches(4.76), Inches(2.42), "Automated", ["Format", "Analyze", "3+ tests", "APK build"], icon="A", accent=d.GREEN, body_size=13)
    d.add_card(s, Inches(7.95), Inches(3.95), Inches(4.76), Inches(2.78), "Human/device", ["Parity review", "WebView block", "Back/plugin", "Gap register"], icon="H", accent=d.GOLD, body_size=13)
    notes(s, "Quality", 15, "Menjalankan gate.", "Simpan output tanpa secret.", "Apa yang tetap belum terbukti?", "Project README.")
    n += 1

    s = d.base_slide(prs, "CHALLENGE", "Rubrik demo migrasi 8 menit", n, TOTAL, 3)
    d.add_table(s, ["Menit", "Demo", "Evidence"], [
        ["1", "Behavior map", "facts + unknown"],
        ["2", "PRD traceability", "AC → file/test"],
        ["2", "WebView", "site + external denied"],
        ["1", "Agent Skill", "path + guardrail"],
        ["1", "Target slice", "list/detail parity"],
        ["1", "Gate + gap", "tests/build/next"],
    ], Inches(0.62), Inches(1.35), Inches(12.08), Inches(4.95), widths=[Inches(1.4), Inches(4.3), Inches(6.38)], font_size=13)
    d.add_text(s, "Core harus lulus sebelum stretch: session/login, bridge, atau slice kedua.", Inches(0.9), Inches(6.52), Inches(11.5), Inches(0.28), size=14, color=d.BLUE, bold=True, align=PP_ALIGN.CENTER)
    notes(s, "Demo", 30, "Menilai hasil Hari 3.", "Gunakan rubrik dan minta satu risiko yang belum selesai.", "Apakah parity terbukti?", "Day3 rubric.")
    n += 1

    s = d.base_slide(prs, "CLOSING", "Trace behavior. Bound the surface. Prove the migration.", n, TOTAL, 3, bg=d.NAVY)
    d.add_text(s, "day-3", Inches(0.72), Inches(1.15), Inches(4.2), Inches(0.85), size=54, color=d.CYAN, bold=True, font=d.FONT_DISPLAY)
    d.add_text(s, "PRD → Agent Skill → WebView → Evidence", Inches(0.75), Inches(2.08), Inches(7.0), Inches(0.46), size=25, color=d.WHITE, bold=True)
    d.add_code(s, "fvm flutter analyze\nfvm flutter test\nfvm flutter build apk --debug\n\ngit diff --check\n# attach PRD, evidence, gap register", Inches(0.75), Inches(2.82), Inches(6.15), Inches(3.12), label="FINAL CHECKPOINT", size=11.2)
    d.add_card(s, Inches(7.25), Inches(1.15), Inches(5.38), Inches(4.79), "Handover", ["Behavior map", "PRD + traceability", "Agent Skill", "WebView policy", "Tests/build + gaps"], icon="✓", accent=d.CYAN, fill=d.NAVY_2, body_size=14)
    d.add_text(s, "Rujukan: docs.flutter.dev • pub.dev/webview_flutter • opencode.ai/docs", Inches(0.75), Inches(6.52), Inches(11.85), Inches(0.28), size=10, color=d.CYAN_2, align=PP_ALIGN.CENTER)
    d.add_text(s, f"{n:02d} / {TOTAL:02d}", Inches(11.62), Inches(6.90), Inches(0.95), Inches(0.22), size=10, color=d.CYAN_2, bold=True, align=PP_ALIGN.RIGHT)
    notes(s, "Closing", 5, "Menutup program.", "Minta tiap tim menyebut next slice dan blocker.", "Bukti apa yang paling mengubah keputusan?", "Day3 handover.")

    assert len(prs.slides) == TOTAL, (len(prs.slides), TOTAL)
    out = ROOT / "Hari_3_Flutter_Professional.pptx"
    prs.save(out)
    shutil.copy2(out, ROOT / "PPT_Training" / "Hari_3_Testing_Performance_Release_Android.pptx")
    shutil.copy2(out, ROOT / "PPT_Training" / "Hari_3_AI_Agent_WebView_Migrasi_Kotlin.pptx")
    return out


def main():
    original = ROOT / "Hari_3_Flutter_Professional.pptx"
    backup = ROOT / "Hari_3_Flutter_Professional_sebelum_AI_WebView.pptx"
    if original.exists() and not backup.exists():
        shutil.copy2(original, backup)
    with tempfile.TemporaryDirectory(prefix="dpl-day3-ai-webview-") as temp_name:
        background = d.prepare_cover_background(Path(temp_name))
        out = build(background)
    print(f"Built {out}")
    print(f"Slides: {TOTAL}; backup: {backup.name}")


if __name__ == "__main__":
    main()
