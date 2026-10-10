import 'package:flutter/material.dart';

import 'screens/inspection_list_screen.dart';

class DplInspectionApp extends StatelessWidget {
  const DplInspectionApp({super.key});

  @override
  Widget build(BuildContext context) {
    const seed = Color(0xff006a60);
    return MaterialApp(
      title: 'DPL Inspection',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: seed),
        useMaterial3: true,
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(),
          alignLabelWithHint: true,
        ),
      ),
      home: const InspectionListScreen(),
    );
  }
}
