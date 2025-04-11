# Auto Reply Bot for Trendyol Reviews

Bu script, Trendyol'daki restoran yorumlarına otomatik olarak yanıt vermek için Telegram botu kullanır. Kullanıcı yorumlarını alır, Google Gemini API'si ile uygun yanıtlar oluşturur ve Telegram üzerinden onay alarak Trendyol API'sine yanıt gönderir.

## Gereksinimler

Scriptin çalışabilmesi için aşağıdaki API anahtarlarına ve ayarlara ihtiyacınız olacak:

### 1. **Telegram Bot API Anahtarı (BOT_TOKEN)**

Telegram botu ile etkileşimde bulunabilmek için bir bot oluşturmanız gerekecek.

- **Nasıl alınır?**
  - Telegram'da [BotFather](https://core.telegram.org/bots#botfather) botuna yazın.
  - `/newbot` komutunu girin ve botunuzu oluşturun.
  - Bot oluşturduktan sonra size bir **bot token** verilecektir. Bu token'ı scriptteki `BOT_TOKEN` alanına yerleştirmeniz gerekecek.

### 2. **Telegram Chat ID (CHAT_ID)**

Telegram botu üzerinden mesaj göndermek için chat ID'yi bilmeniz gerekiyor. Bu, mesajların nereye gönderileceğini belirler.

- **Nasıl alınır?**
  - Botunuzla bir sohbet başlatın ve botu bir grup sohbetine ekleyin.
  - Botu kullanarak bir mesaj gönderin ve chat ID'yi almak için aşağıdaki URL'yi tarayıcınızda açın:
    ```
    https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
    ```
    - `<YOUR_BOT_TOKEN>` yerine Telegram botunuzun token'ını yazın.
    - JSON yanıtında `chat` kısmında `id` alanına bakarak chat ID'nizi alabilirsiniz.

### 3. **Trendyol GO API Anahtarları (API_KEY ve API_SECRET)**

Trendyol GO API'sine erişebilmek için bir **API_KEY** ve **API_SECRET** gereklidir. Bu, API'ye kimlik doğrulaması yapabilmek için kullanılır.

- **Nasıl alınır?**
  - Satıcı Paneli>Hesap Bilgilerim>Entegrasyon Bilgileri.
  - Bu API anahtarlarını aldıktan sonra, scriptteki `API_KEY` ve `API_SECRET` alanlarına bu değerleri yerleştirebilirsiniz.

### 4. **Google Gemini API Anahtarı (GEMINI_API_KEY)**

Yorumları işlemek ve cevaplar oluşturmak için Google Gemini API'sini kullanmanız gerekecek. Bu API, yazılı içerik oluşturma için kullanılır.

- **Nasıl alınır?**
  - Google Gemini API'ye erişmek için bir Google Cloud hesabınızın olması gerekiyor.
  - [Google Cloud Console](https://console.cloud.google.com/) üzerinden bir proje oluşturun ve Gemini API'yi etkinleştirin.
  - API anahtarını alıp, scriptteki `GEMINI_API_KEY` alanına yerleştirebilirsiniz.

### 5. **Trendyol API URL**

Trendyol API'sine veri göndermek için doğru API URL'sine ihtiyacınız olacak. Bu URL, ürün ve yorumlarla etkileşime geçmek için kullanılır.

- **Nasıl Scripte Eklenir?**
  - https://api.tgoapis.com/integrator/review/meal/suppliers/RESTORANİD/stores/ŞUBEİD/reviews/filter
  - Restoran ID ve Şube ID kısmını doldurup scripte ekleyebilirsiniz.

---

## Yükleme ve Başlatma

### Gerekli Kütüphaneler

Aşağıdaki komutlarla gerekli Python kütüphanelerini yükleyebilirsiniz:

```bash
pip install requests base64 json time threading flask prettytable
```

### Scripti Çalıştırın
Scripti çalıştırmadan önce, gerekli tüm ayarları yapmış olduğunuzdan emin olun. Ardından aşağıdaki komut ile scripti çalıştırabilirsiniz:

```bash
python auto_reply.py
```

### Scriptin Çalışma Prensibi
	Yorumları Çekme: Script, Trendyol API’sinden yorumları çeker.
	Yanıt Üretme: Google Gemini API’si aracılığıyla yorumlar için uygun cevaplar oluşturulur.
	Telegram Onayı: Telegram botu üzerinden bu yorumlar size iletilir. Her yorum için “onay ver” veya “görmezden gel” seçenekleri sunulur.
	Yanıt Gönderme: Onay verdiğiniz yorumlar Trendyol API’sine gönderilir ve yanıt verilir.

Script her 20 dakikada bir Trendyol API’sini kontrol eder ve yeni yorumları inceler. Yorumlar için uygun yanıtlar oluşturur ve Telegram botu üzerinden size iletir.

### Dikkat Edilmesi Gerekenler
 API Anahtarları: Scriptin düzgün çalışabilmesi için doğru API anahtarlarını ve bilgileri girdiğinizden emin olun.
	Kütüphane Yüklemeleri: Python kütüphanelerinin doğru şekilde yüklendiğinden emin olun.
	Zamanlama: Script her 20 dakikada bir yorumları kontrol eder. Eğer daha sık aralıklarla çalışmasını istiyorsanız, time.sleep(1200) değerini değiştirebilirsiniz.

 - Başka sorularınız olursa, lütfen iletişime geçin. @berkakahs
