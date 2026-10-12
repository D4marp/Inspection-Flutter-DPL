import 'package:flutter/material.dart';

class MigrationPrdScreen extends StatelessWidget {
  const MigrationPrdScreen({super.key});

  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.all(16),
    children: [
      _HeroCard(),
      const SizedBox(height: 16),
      Text('Slice pertama', style: Theme.of(context).textTheme.titleLarge),
      const SizedBox(height: 10),
      const _SectionCard(
        icon: Icons.flag_outlined,
        title: 'Tujuan produk',
        body:
            'Memigrasikan alur daftar → detail inspeksi dari Android Kotlin ke Flutter tanpa mengubah kontrak API atau perilaku bisnis.',
      ),
      const SizedBox(height: 10),
      const _SectionCard(
        icon: Icons.compare_arrows,
        title: 'Pemetaan artefak',
        body:
            'Activity/Fragment → Screen • XML → Widget tree • ViewModel → Controller • Retrofit → ApiClient/Repository • SharedPreferences → storage policy.',
      ),
      const SizedBox(height: 10),
      const _SectionCard(
        icon: Icons.rule_folder_outlined,
        title: 'Acceptance criteria',
        body:
            'AC1 daftar dan detail setara • AC2 loading/empty/error terlihat • AC3 back navigation konsisten • AC4 test otomatis hijau • AC5 keputusan dan gap dicatat.',
      ),
      const SizedBox(height: 10),
      const _SectionCard(
        icon: Icons.block_outlined,
        title: 'Di luar scope slice',
        body:
            'Rewrite seluruh aplikasi, perubahan kontrak API, autentikasi baru, JavaScript bridge produksi, dan keputusan arsitektur tanpa bukti dari app Kotlin.',
      ),
      const SizedBox(height: 18),
      _Checklist(),
    ],
  );
}

class _HeroCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(colors: [colors.primary, colors.secondary]),
        borderRadius: BorderRadius.circular(24),
      ),
      child: const Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(Icons.route, color: Colors.white, size: 30),
          SizedBox(height: 14),
          Text(
            'Migrate by vertical slice',
            style: TextStyle(
              color: Colors.white,
              fontSize: 24,
              fontWeight: FontWeight.w800,
            ),
          ),
          SizedBox(height: 8),
          Text(
            'Trace perilaku Kotlin, tulis acceptance, implementasikan satu alur Flutter, lalu buktikan parity.',
            style: TextStyle(color: Colors.white, height: 1.45),
          ),
        ],
      ),
    );
  }
}

class _SectionCard extends StatelessWidget {
  const _SectionCard({
    required this.icon,
    required this.title,
    required this.body,
  });

  final IconData icon;
  final String title;
  final String body;

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: Theme.of(context).colorScheme.secondary),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 6),
                Text(body, style: const TextStyle(height: 1.45)),
              ],
            ),
          ),
        ],
      ),
    ),
  );
}

class _Checklist extends StatelessWidget {
  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Evidence minimum',
            style: Theme.of(
              context,
            ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 10),
          for (final item in const [
            'Screenshot perilaku lama dan target Flutter',
            'Traceability PRD → test → commit',
            'flutter analyze dan flutter test lulus',
            'Daftar gap, risiko, owner, dan next slice',
          ])
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(
                    Icons.check_circle,
                    size: 18,
                    color: Color(0xff0f8b8d),
                  ),
                  const SizedBox(width: 8),
                  Expanded(child: Text(item)),
                ],
              ),
            ),
        ],
      ),
    ),
  );
}
