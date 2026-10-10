enum InspectionCondition { good, needsAction }

extension InspectionConditionX on InspectionCondition {
  String get value => switch (this) {
    InspectionCondition.good => 'good',
    InspectionCondition.needsAction => 'needs_action',
  };

  String get label => switch (this) {
    InspectionCondition.good => 'Baik',
    InspectionCondition.needsAction => 'Perlu tindak lanjut',
  };
}

class Inspection {
  const Inspection({
    required this.id,
    required this.assetCode,
    required this.location,
    required this.condition,
    required this.note,
    required this.createdAt,
  });

  final String id;
  final String assetCode;
  final String location;
  final InspectionCondition condition;
  final String note;
  final DateTime createdAt;
}

List<Inspection> demoInspections() => [
  Inspection(
    id: 'seed-1',
    assetCode: 'PMP-001',
    location: 'Workshop A',
    condition: InspectionCondition.good,
    note: 'Kondisi normal dan siap digunakan.',
    createdAt: DateTime.utc(2026, 10, 3, 1),
  ),
  Inspection(
    id: 'seed-2',
    assetCode: 'PMP-002',
    location: 'Dermaga Utara',
    condition: InspectionCondition.needsAction,
    note: 'Getaran motor perlu diperiksa oleh tim mekanik.',
    createdAt: DateTime.utc(2026, 10, 3, 1, 5),
  ),
  Inspection(
    id: 'seed-3',
    assetCode: 'GEN-003',
    location: 'Gudang Peralatan',
    condition: InspectionCondition.good,
    note: 'Pemeriksaan rutin selesai.',
    createdAt: DateTime.utc(2026, 10, 3, 1, 10),
  ),
];
