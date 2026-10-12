import 'dart:ui';

import 'package:flutter/foundation.dart';
import 'package:webview_flutter/webview_flutter.dart';

import 'navigation_policy.dart';

const trainingWebsiteUrl = 'https://www.presisirencar.com/';

WebViewController buildMigrationWebViewController({
  required ValueChanged<int> onProgress,
  required ValueChanged<String> onBlocked,
  required VoidCallback onMainFrameError,
  required VoidCallback onPageStarted,
  required VoidCallback onPageFinished,
}) {
  return WebViewController()
    ..setJavaScriptMode(JavaScriptMode.unrestricted)
    ..setBackgroundColor(const Color(0xfff7f8fb))
    ..setNavigationDelegate(
      NavigationDelegate(
        onProgress: onProgress,
        onPageStarted: (_) => onPageStarted(),
        onPageFinished: (_) => onPageFinished(),
        onNavigationRequest: (request) {
          if (TrainingNavigationPolicy.allows(request.url)) {
            return NavigationDecision.navigate;
          }
          onBlocked(request.url);
          return NavigationDecision.prevent;
        },
        onWebResourceError: (error) {
          if (error.isForMainFrame != false) onMainFrameError();
        },
      ),
    )
    ..loadRequest(Uri.parse(trainingWebsiteUrl));
}
