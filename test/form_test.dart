import 'package:dpl_inspection_day_1/src/screens/inspection_form_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('empty form reports required fields', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: InspectionFormScreen()));
    await tester.ensureVisible(find.byKey(const Key('saveButton')));
    await tester.tap(find.byKey(const Key('saveButton')));
    await tester.pump();

    expect(find.text('Kode aset wajib diisi'), findsOneWidget);
    expect(find.text('Lokasi wajib diisi'), findsOneWidget);
  });
}
