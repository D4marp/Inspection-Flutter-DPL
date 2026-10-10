import 'package:flutter/material.dart';

import '../models/inspection.dart';
import '../validation.dart';

class InspectionFormScreen extends StatefulWidget {
  const InspectionFormScreen({super.key});

  @override
  State<InspectionFormScreen> createState() => _InspectionFormScreenState();
}

class _InspectionFormScreenState extends State<InspectionFormScreen> {
  final _formKey = GlobalKey<FormState>();
  final _asset = TextEditingController();
  final _location = TextEditingController();
  final _note = TextEditingController();
  InspectionCondition _condition = InspectionCondition.good;

  @override
  void dispose() {
    _asset.dispose();
    _location.dispose();
    _note.dispose();
    super.dispose();
  }

  void _save() {
    FocusScope.of(context).unfocus();
    if (!(_formKey.currentState?.validate() ?? false)) return;
    final now = DateTime.now().toUtc();
    Navigator.of(context).pop(
      Inspection(
        id: 'local-${now.microsecondsSinceEpoch}',
        assetCode: _asset.text.trim(),
        location: _location.text.trim(),
        condition: _condition,
        note: _note.text.trim(),
        createdAt: now,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Tambah inspeksi')),
      body: SafeArea(
        child: Form(
          key: _formKey,
          child: ListView(
            padding: const EdgeInsets.all(20),
            children: [
              TextFormField(
                key: const Key('assetField'),
                controller: _asset,
                maxLength: 30,
                textInputAction: TextInputAction.next,
                decoration: const InputDecoration(labelText: 'Kode aset'),
                validator: (value) => validateRequired(value, 'Kode aset'),
              ),
              const SizedBox(height: 16),
              TextFormField(
                key: const Key('locationField'),
                controller: _location,
                maxLength: 80,
                textInputAction: TextInputAction.next,
                decoration: const InputDecoration(labelText: 'Lokasi'),
                validator: (value) => validateRequired(value, 'Lokasi'),
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<InspectionCondition>(
                initialValue: _condition,
                decoration: const InputDecoration(labelText: 'Kondisi'),
                items: InspectionCondition.values
                    .map(
                      (value) => DropdownMenuItem(
                        value: value,
                        child: Text(value.label),
                      ),
                    )
                    .toList(),
                onChanged: (value) {
                  if (value != null) setState(() => _condition = value);
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                key: const Key('noteField'),
                controller: _note,
                minLines: 3,
                maxLines: 5,
                maxLength: 500,
                decoration: const InputDecoration(labelText: 'Catatan'),
                validator: (value) => validateNote(
                  _condition == InspectionCondition.needsAction,
                  value,
                ),
              ),
              const SizedBox(height: 8),
              FilledButton.icon(
                key: const Key('saveButton'),
                onPressed: _save,
                icon: const Icon(Icons.save_outlined),
                label: const Text('Simpan inspeksi'),
              ),
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text('Batal'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
