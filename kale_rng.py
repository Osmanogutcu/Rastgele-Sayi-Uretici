import time
import math

class KaleRNG:
    def __init__(self, seed=None):
        if seed is None:
            # Seed verilmezse şimdiki zamanı kullan (Tamamen rastgelelik için)
            self.state = int(time.time() * 1000)
        else:
            self.state = seed
        
        # LCG Algoritması Sabitleri (Kaliteli rastgelelik için seçildi)
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32

    def sonraki_sayi(self):
        """0 ile 2^32 arasında rastgele bir tam sayı üretir."""
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def sonraki_bit(self):
        """0 veya 1 üretir (İstatistiksel kalite için 30. biti alıyoruz)"""
        raw = self.sonraki_sayi()
        # Sayının ortasındaki bitleri almak daha kalitelidir
        # 30. biti çekiyoruz (0 veya 1 döner)
        return (raw >> 30) & 1

    def bit_dizisi_uret(self, uzunluk):
        """İstenen uzunlukta 0 ve 1 listesi üretir"""
        return [self.sonraki_bit() for _ in range(uzunluk)]

# --- İSTATİSTİKSEL TESTLER ---

def ki_kare_testi(bitler):
    """
    Amaç: 0 ve 1'lerin sayısı birbirine yakın mı?
    """
    n = len(bitler)
    beklenen = n / 2
    sayac_0 = bitler.count(0)
    sayac_1 = bitler.count(1)
    
    # Ki-Kare Formülü: (Gözlenen - Beklenen)^2 / Beklenen
    chi_square = ((sayac_0 - beklenen)**2 / beklenen) + ((sayac_1 - beklenen)**2 / beklenen)
    
    print(f"\n[1] Kİ-KARE TESTİ (Chi-Square)")
    print(f"    Toplam Bit: {n}")
    print(f"    0 Sayısı: {sayac_0} | 1 Sayısı: {sayac_1}")
    print(f"    Hesaplanan Değer: {chi_square:.4f}")
    
    # Serbestlik derecesi 1, güven aralığı %95 için kritik değer 3.841
    if chi_square < 3.841:
        print("    SONUÇ: ✅ BAŞARILI (0 ve 1 dağılımı dengeli)")
        return True
    else:
        print("    SONUÇ: ❌ BAŞARISIZ (Denge bozuk)")
        return False

def mislin_testi(bitler):
    """
    Runs Test (Seriler Testi): 0'lar ve 1'ler ne sıklıkla değişiyor?
    Örn: 0000011111 (Kötü) vs 01010101 (Kötü) vs 00110101 (İyi)
    """
    n = len(bitler)
    n0 = bitler.count(0)
    n1 = bitler.count(1)
    
    # Seri (Run) sayısını bul
    runs = 1
    for i in range(len(bitler) - 1):
        if bitler[i] != bitler[i+1]:
            runs += 1
            
    # Beklenen seri sayısı ve standart sapma formülleri
    beklenen_runs = ((2 * n0 * n1) / n) + 1
    varyans = (2 * n0 * n1 * (2 * n0 * n1 - n)) / (n**2 * (n - 1))
    standart_sapma = math.sqrt(varyans)
    
    # Z Skoru
    z = (runs - beklenen_runs) / standart_sapma
    
    print(f"\n[2] MİSLİN (RUNS) TESTİ")
    print(f"    Seri Sayısı (Runs): {runs}")
    print(f"    Beklenen Seri: {beklenen_runs:.2f}")
    print(f"    Z-Skoru: {z:.4f}")
    
    # Z skoru -1.96 ile +1.96 arasındaysa (%95 güven) başarılıdır
    if -1.96 < z < 1.96:
        print("    SONUÇ: ✅ BAŞARILI (Rastgelelik akışı doğal)")
        return True
    else:
        print("    SONUÇ: ❌ BAŞARISIZ (Örüntü tespit edildi)")
        return False

# --- ANA PROGRAM ---
if __name__ == "__main__":
    print("--- KALE-RSÜ (Rastgele Sayı Üreteci) ---")
    
    # 1. Algoritmayı Başlat
    rng = KaleRNG() # Otomatik seed (zaman)
    
    # 2. 1000 tane bit üret (Hocaya göstermek için ideal sayı)
    print("Veri üretiliyor (1000 bit)...")
    bit_dizisi = rng.bit_dizisi_uret(1000)
    
    # 3. İlk 50 bitini ekrana yazdır (Örnek çıktı)
    print(f"\nÜretilen İlk 50 Bit: {bit_dizisi[:50]}")
    
    # 4. Testleri Uygula
    t1 = ki_kare_testi(bit_dizisi)
    t2 = mislin_testi(bit_dizisi)
    
    if t1 and t2:
        print("\n🏆 GENEL SONUÇ: ALGORİTMA GÜVENİLİR VE RASTGELE.")
    else:
        print("\n⚠️ GENEL SONUÇ: ALGORİTMA REVİZE EDİLMELİ.")
