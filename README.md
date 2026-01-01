# Rastgele-Sayi-Uretici
# 🎲 KALE-RSÜ (Rastgele Sayı Üreteci)

Bu proje, kriptografik ve istatistiksel standartlara uygun, Python tabanlı bir Sözde Rastgele Sayı Üreteci (PRNG) algoritmasıdır.

## ⚙️ Algoritmanın Mantığı
Algoritma, **Doğrusal Benzeşim Yöntemi (Linear Congruential Generator - LCG)** temel alınarak tasarlanmıştır.

1.  **Tohum (Seed):** Başlangıç değeri olarak sistem saati (milisaniye cinsinden) alınır. Bu, her çalıştırmada tamamen farklı sonuçlar üretilmesini sağlar.
2.  **Matematiksel Dönüşüm:** Her adımda şu formül uygulanır:
    $$X_{n+1} = (a \cdot X_n + c) \mod m$$
    * $a = 1664525$
    * $c = 1013904223$
    * $m = 2^{32}$
3.  **Bit Çıkarma:** Üretilen büyük tam sayıların en yüksek anlamlı bitleri (MSB) daha rastgele olduğu için, sayının 30. biti çekilerek `0` veya `1` elde edilir.

---

## 📝 Sözde Kod (Pseudocode)
-
BAŞLA
    GİRDİ: Seed (Yoksa Sistem Saatini Al)
    SABİTLER: a = 1664525, c = 1013904223, m = 2^32
    DEĞİŞKEN: State = Seed

    FONKSİYON Sonraki_Bit():
        State = (a * State + c) MOD m
        Bit = (State SAĞA KAYDIR 30) VE 1
        DÖNDÜR Bit

    DÖNGÜ (1000 Kez):
        Bit Listesine Ekle(Sonraki_Bit())
    
    FONKSİYON Testler(Bit_Listesi):
        Ki-Kare Testi Uygula
        Mislin (Runs) Testi Uygula
        Sonuçları Yazdır
BİTİR

## 🔄 Algoritma Akış Şeması
-
    %% Akış Diyagramı
    A([BAŞLA]):::siyahYazi --> B[/Giriş: Sistem Saati / Seed/]:::siyahYazi
    B --> C[LCG Formülü Uygula:<br/>State = a * State + c MOD m]:::siyahYazi
    C --> D[Bit Çıkarma:<br/>Sayının 30. Bitini Al]:::siyahYazi
    D --> E[Listeye Ekle]:::siyahYazi
    E --> F{1000 Bit Oldu mu?}:::siyahYazi
    
    %% Karar Okları
    F -- Hayır --> C
    F -- Evet --> G[İstatistiksel Testleri Başlat]:::siyahYazi
    
    G --> H[Ki-Kare Testi Hesapla]:::siyahYazi
    H --> I[Mislin / Runs Testi Hesapla]:::siyahYazi
    I --> J{Testler Geçti mi?}:::siyahYazi
    
    %% Sonuç Okları
    J -- Evet --> K[/Çıktı: BAŞARILI/]:::siyahYazi
    J -- Hayır --> L[/Çıktı: BAŞARISIZ/]:::siyahYazi
    
    K --> M([BİTİR]):::siyahYazi
    L --> M
Geliştirici isim:Osmnan Kerim Ögütçü
