import 'package:dpl_inspection_day_1/src/validation.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('good condition allows an empty note', () {
    expect(validateNote(false, ''), isNull);
  });

  test('needs action requires a descriptive note', () {
    expect(validateNote(true, 'cek'), isNotNull);
    expect(validateNote(true, 'Motor bergetar tinggi'), isNull);
  });

  test('required values are trimmed', () {
    expect(validateRequired('   ', 'Lokasi'), 'Lokasi wajib diisi');
  });
}
