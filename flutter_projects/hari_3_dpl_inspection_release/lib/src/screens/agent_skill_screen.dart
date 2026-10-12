import 'package:flutter/material.dart';

class AgentSkillScreen extends StatelessWidget {
  const AgentSkillScreen({super.key});

  static const skillPath = '.agents/skills/migrate-kotlin-slice/SKILL.md';

  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.all(16),
    children: [
      Card(
        color: Theme.of(context).colorScheme.primary,
        child: const Padding(
          padding: EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(Icons.auto_awesome, color: Color(0xffffd166), size: 32),
              SizedBox(height: 12),
              Text(
                'migrate-kotlin-slice',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                  fontWeight: FontWeight.w800,
                ),
              ),
              SizedBox(height: 8),
              Text(
                'Workflow reusable untuk memindahkan satu vertical slice Kotlin ke Flutter dengan evidence dan guardrail.',
                style: TextStyle(color: Colors.white, height: 1.45),
              ),
            ],
          ),
        ),
      ),
      const SizedBox(height: 14),
      const _InfoTile(
        icon: Icons.folder_open_outlined,
        title: 'Lokasi skill',
        body: skillPath,
      ),
      const _InfoTile(
        icon: Icons.input_outlined,
        title: 'Input wajib',
        body:
            'PRD slice, source Kotlin/XML relevan, contract API, target file Flutter, dan test yang sudah ada.',
      ),
      const _InfoTile(
        icon: Icons.account_tree_outlined,
        title: 'Workflow',
        body:
            'Read → trace behavior → map AC → plan patch kecil → implement → format/analyze/test → report gap.',
      ),
      const _InfoTile(
        icon: Icons.security_outlined,
        title: 'Guardrail',
        body:
            'Jangan invent contract, jangan kirim secret, jangan perluas host/bridge WebView, dan jangan mengklaim test yang belum dijalankan.',
      ),
      const SizedBox(height: 14),
      Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Prompt praktik',
                style: Theme.of(
                  context,
                ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 10),
              const SelectableText(
                'Gunakan skill migrate-kotlin-slice. Migrasikan alur daftar-detail dari legacy Kotlin sesuai PRD. Tunjukkan traceability AC, patch kecil, hasil analyze/test, dan gap yang tersisa.',
                style: TextStyle(fontFamily: 'monospace', height: 1.5),
              ),
            ],
          ),
        ),
      ),
    ],
  );
}

class _InfoTile extends StatelessWidget {
  const _InfoTile({
    required this.icon,
    required this.title,
    required this.body,
  });

  final IconData icon;
  final String title;
  final String body;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Card(
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: Icon(icon, color: Theme.of(context).colorScheme.secondary),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.w700)),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 6),
          child: Text(body, style: const TextStyle(height: 1.4)),
        ),
      ),
    ),
  );
}
