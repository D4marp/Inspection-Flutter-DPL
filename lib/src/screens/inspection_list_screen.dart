import 'package:flutter/material.dart';

import '../models/inspection.dart';
import '../widgets/status_badge.dart';
import 'inspection_detail_screen.dart';
import 'inspection_form_screen.dart';

class InspectionListScreen extends StatefulWidget {
  const InspectionListScreen({super.key});

  @override
  State<InspectionListScreen> createState() => _InspectionListScreenState();
}

class _InspectionListScreenState extends State<InspectionListScreen> {
  List<Inspection> _items = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load({bool fail = false}) async {
    setState(() {
      _loading = true;
      _error = null;
    });
    await Future<void>.delayed(const Duration(milliseconds: 500));
    if (!mounted) return;
    setState(() {
      _loading = false;
      if (fail) {
        _error = 'Data gagal dimuat. Periksa koneksi lalu coba lagi.';
      } else {
        _items = demoInspections();
      }
    });
  }

  Future<void> _add() async {
    final created = await Navigator.of(context).push<Inspection>(
      MaterialPageRoute(builder: (_) => const InspectionFormScreen()),
    );
    if (!mounted || created == null) return;
    setState(() => _items = [created, ..._items]);
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Inspeksi berhasil ditambahkan')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('DPL Inspection'),
        actions: [
          PopupMenuButton<String>(
            enabled: !_loading,
            tooltip: 'Skenario demo',
            onSelected: (value) {
              if (value == 'empty') setState(() => _items = []);
              if (value == 'error') _load(fail: true);
              if (value == 'reload') _load();
            },
            itemBuilder: (_) => const [
              PopupMenuItem(value: 'empty', child: Text('Demo kosong')),
              PopupMenuItem(value: 'error', child: Text('Demo error')),
              PopupMenuItem(value: 'reload', child: Text('Muat ulang demo')),
            ],
          ),
        ],
      ),
      body: SafeArea(child: _buildBody()),
      floatingActionButton: _loading || _error != null
          ? null
          : FloatingActionButton.extended(
              onPressed: _add,
              icon: const Icon(Icons.add),
              label: const Text('Tambah'),
            ),
    );
  }

  Widget _buildBody() {
    if (_loading) {
      return const Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            CircularProgressIndicator(),
            SizedBox(height: 16),
            Text('Memuat inspeksi…'),
          ],
        ),
      );
    }
    if (_error != null) {
      return _MessageState(
        icon: Icons.cloud_off_outlined,
        title: 'Tidak dapat memuat data',
        message: _error!,
        buttonLabel: 'Coba lagi',
        onPressed: _load,
      );
    }
    if (_items.isEmpty) {
      return _MessageState(
        icon: Icons.assignment_outlined,
        title: 'Belum ada inspeksi',
        message: 'Tambahkan inspeksi pertama untuk memulai.',
        buttonLabel: 'Tambah inspeksi',
        onPressed: _add,
      );
    }
    return RefreshIndicator(
      onRefresh: _load,
      child: ListView.separated(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 96),
        itemCount: _items.length,
        separatorBuilder: (_, _) => const SizedBox(height: 8),
        itemBuilder: (context, index) {
          final item = _items[index];
          return Card(
            key: ValueKey(item.id),
            child: ListTile(
              contentPadding: const EdgeInsets.all(16),
              title: Text(
                item.assetCode,
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
              subtitle: Padding(
                padding: const EdgeInsets.only(top: 6),
                child: Text(item.location),
              ),
              trailing: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 150),
                child: StatusBadge(condition: item.condition),
              ),
              onTap: () => Navigator.of(context).push<void>(
                MaterialPageRoute(
                  builder: (_) => InspectionDetailScreen(item: item),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

class _MessageState extends StatelessWidget {
  const _MessageState({
    required this.icon,
    required this.title,
    required this.message,
    required this.buttonLabel,
    required this.onPressed,
  });

  final IconData icon;
  final String title;
  final String message;
  final String buttonLabel;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) => Center(
    child: Padding(
      padding: const EdgeInsets.all(32),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 56, color: Theme.of(context).colorScheme.primary),
          const SizedBox(height: 16),
          Text(
            title,
            style: Theme.of(context).textTheme.titleLarge,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),
          Text(message, textAlign: TextAlign.center),
          const SizedBox(height: 20),
          FilledButton(onPressed: onPressed, child: Text(buttonLabel)),
        ],
      ),
    ),
  );
}
