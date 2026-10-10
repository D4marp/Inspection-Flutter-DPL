import 'package:flutter/material.dart';

import '../models/inspection.dart';
import '../widgets/status_badge.dart';

class InspectionDetailScreen extends StatelessWidget {
  const InspectionDetailScreen({super.key, required this.item});

  final Inspection item;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Detail inspeksi')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            Text(
              item.assetCode,
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 8),
            Align(
              alignment: Alignment.centerLeft,
              child: StatusBadge(condition: item.condition),
            ),
            const SizedBox(height: 24),
            _DetailRow(
              icon: Icons.place_outlined,
              label: 'Lokasi',
              value: item.location,
            ),
            _DetailRow(
              icon: Icons.schedule_outlined,
              label: 'Waktu',
              value: item.createdAt.toLocal().toString(),
            ),
            _DetailRow(
              icon: Icons.notes_outlined,
              label: 'Catatan',
              value: item.note.isEmpty ? 'Tanpa catatan' : item.note,
            ),
            _DetailRow(icon: Icons.tag_outlined, label: 'ID', value: item.id),
          ],
        ),
      ),
    );
  }
}

class _DetailRow extends StatelessWidget {
  const _DetailRow({
    required this.icon,
    required this.label,
    required this.value,
  });

  final IconData icon;
  final String label;
  final String value;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 20),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label, style: Theme.of(context).textTheme.labelLarge),
              const SizedBox(height: 4),
              Text(value),
            ],
          ),
        ),
      ],
    ),
  );
}
