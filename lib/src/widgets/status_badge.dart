import 'package:flutter/material.dart';

import '../models/inspection.dart';

class StatusBadge extends StatelessWidget {
  const StatusBadge({super.key, required this.condition});

  final InspectionCondition condition;

  @override
  Widget build(BuildContext context) {
    final good = condition == InspectionCondition.good;
    final colors = Theme.of(context).colorScheme;
    return Semantics(
      label: 'Kondisi ${condition.label}',
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
        decoration: BoxDecoration(
          color: good ? colors.primaryContainer : colors.errorContainer,
          borderRadius: BorderRadius.circular(999),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              good ? Icons.check_circle_outline : Icons.warning_amber_rounded,
              size: 16,
              color: good ? colors.onPrimaryContainer : colors.onErrorContainer,
            ),
            const SizedBox(width: 6),
            Flexible(
              child: Text(
                condition.label,
                overflow: TextOverflow.ellipsis,
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                  color: good
                      ? colors.onPrimaryContainer
                      : colors.onErrorContainer,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
