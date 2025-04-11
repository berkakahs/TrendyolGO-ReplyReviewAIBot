# Telegram Yorum Cevap Botu

Bu Python scripti, Trendyol API'si üzerinden restoran yorumlarını alır, her bir yoruma uygun bir cevap oluşturur ve Telegram botu üzerinden onay almanızı sağlar. Onayladığınız yorumlar, Trendyol API'sine gönderilir.

## Özellikler

- Trendyol API'si üzerinden restoran yorumlarını alır.
- Gemini API'si ile yorumlara uygun cevaplar oluşturur.
- Telegram botu ile her bir yoruma cevap oluşturulup onaylanmasını bekler.
- Onaylanan yorumlar Trendyol API'sine gönderilir.

## Kurulum

### Gereksinimler

- Python 3.6 ve üzeri
- `requests`, `flask`, `prettytable` gibi Python kütüphaneleri

### Gerekli Kütüphaneleri Yükleme

Aşağıdaki komutları kullanarak gerekli Python kütüphanelerini yükleyin:

```bash
pip install requests flask prettytable
