import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

import '../webview/migration_webview_controller.dart';

class TrainingWebViewScreen extends StatefulWidget {
  const TrainingWebViewScreen({super.key});

  @override
  State<TrainingWebViewScreen> createState() => _TrainingWebViewScreenState();
}

class _TrainingWebViewScreenState extends State<TrainingWebViewScreen> {
  late final WebViewController _controller;
  var _progress = 0;
  var _canGoBack = false;
  String? _message;

  @override
  void initState() {
    super.initState();
    _controller = buildMigrationWebViewController(
      onProgress: (value) {
        if (mounted) setState(() => _progress = value);
      },
      onPageStarted: () {
        if (mounted) setState(() => _message = null);
      },
      onPageFinished: () async {
        final canGoBack = await _controller.canGoBack();
        if (mounted) setState(() => _canGoBack = canGoBack);
      },
      onBlocked: (rawUrl) {
        final host = Uri.tryParse(rawUrl)?.host;
        if (mounted) {
          setState(
            () => _message =
                'Navigasi eksternal diblokir: '
                '${host == null || host.isEmpty ? rawUrl : host}',
          );
        }
      },
      onMainFrameError: () {
        if (mounted) {
          setState(() => _message = 'Konten gagal dimuat. Coba reload.');
        }
      },
    );
  }

  @override
  Widget build(BuildContext context) => Column(
    children: [
      Material(
        color: Colors.white,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(12, 10, 12, 10),
          child: Row(
            children: [
              const Icon(Icons.verified_user_outlined, size: 20),
              const SizedBox(width: 8),
              const Expanded(
                child: Text(
                  'presisirencar.com • HTTPS allowlist • external blocked',
                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
                ),
              ),
              IconButton(
                tooltip: 'Kembali di WebView',
                onPressed: _canGoBack ? _controller.goBack : null,
                icon: const Icon(Icons.arrow_back),
              ),
              IconButton(
                tooltip: 'Reload',
                onPressed: _controller.reload,
                icon: const Icon(Icons.refresh),
              ),
            ],
          ),
        ),
      ),
      if (_progress < 100) LinearProgressIndicator(value: _progress / 100),
      if (_message != null)
        Container(
          width: double.infinity,
          color: Theme.of(context).colorScheme.errorContainer,
          padding: const EdgeInsets.all(10),
          child: Text(_message!, textAlign: TextAlign.center),
        ),
      Expanded(child: WebViewWidget(controller: _controller)),
    ],
  );
}
