abstract final class TrainingNavigationPolicy {
  static const allowedHosts = <String>{
    'presisirencar.com',
    'www.presisirencar.com',
  };

  static bool allows(String rawUrl) {
    if (rawUrl == 'about:blank') return true;
    final uri = Uri.tryParse(rawUrl);
    return uri != null &&
        uri.scheme == 'https' &&
        allowedHosts.contains(uri.host.toLowerCase());
  }
}
