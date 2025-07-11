import 'dart:html' as html;
import 'dart:ui' as ui; // Platform görünüm kaydı için gerekli
import 'package:flutter/material.dart';

void main() {
  setupHtml(); // HTML elementini kaydetmeden önce çağırıyoruz
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  final String streamUrl = 'http://localhost:5000/video_feed'; // MJPEG akış URL'niz

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MJPEG Viewer',
      home: Scaffold(
        appBar: AppBar(
          title: const Text('🎥 Live Camera Stream'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('RTSP MJPEG Stream', style: TextStyle(fontSize: 20)),
              const SizedBox(height: 20),
              SizedBox(
                width: 640,
                height: 480,
                child: HtmlElementView(viewType: 'imgElement'), // Kayıtlı görünüm türünü kullanıyoruz
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// <img> elementini oluşturup yapılandıran fonksiyon
void setupHtml() {
  ui.platformViewRegistry.registerViewFactory(
    'imgElement', // HtmlElementView ile eşleşen görünüm türü
        (int viewId) {
      final imgElement = html.ImageElement(src: 'http://localhost:5000/video_feed');
      imgElement.style.width = '640px';
      imgElement.style.height = '480px';
      // Hata ayıklama için opsiyonel hata dinleyicisi
      imgElement.onError.listen((event) {
        print('Akış yüklenirken hata oluştu: $event');
      });
      return imgElement;
    },
  );
  print('Görünüm fabrikası "imgElement" için başarıyla kaydedildi.');
}