import struct

# --- GÖLGE-128 (Shadow-128) Şifreleme Algoritması ---
# Föy Uyumluluğu: Aşama 2 (Kodlama ve Test)

# --- MATEMATİKSEL SABİTLER ---
# İkame ters işlemi için: 5 * 205 = 1025 = 1 (mod 256)
# Yani 5'in mod 256'ya göre tersi 205'tir.
INV_MULT = 205 

def anahtar_uret(parola):
    """
    FÖY İSTERİ 1: Anahtar_Uret(parola)
    Girilen parolayı 128-bit (16 byte) anahtara tamamlar veya kırpar.
    """
    parola_bytes = parola.encode('utf-8')
    if len(parola_bytes) < 16:
        # 16 byte'a tamamla (Padding)
        return parola_bytes + b'\x00' * (16 - len(parola_bytes))
    return parola_bytes[:16] # İlk 16 byte'ı al

def anahtar_genislet(ana_anahtar):
    """
    Yardımcı Fonksiyon: 10 Tur anahtarı üretir.
    """
    anahtarlar = []
    su_anki = int.from_bytes(ana_anahtar, byteorder='big')

    for i in range(10):
        # Sola 3 bit kaydır (Rotate)
        su_anki = ((su_anki << 3) | (su_anki >> (128 - 3))) & ((1 << 128) - 1)
        
        yeni_anahtar = bytearray(su_anki.to_bytes(16, byteorder='big'))
        # XOR Sabiti (i+1)
        for j in range(16):
            yeni_anahtar[j] ^= (i + 1)
        
        anahtarlar.append(yeni_anahtar)
        su_anki = int.from_bytes(yeni_anahtar, byteorder='big')
    return anahtarlar

# --- ŞİFRELEME FONKSİYONLARI ---

def sifrele(duz_metin, anahtar):
    """
    FÖY İSTERİ 2: Sifrele(duz_metin, anahtar)
    """
    # Blok boyutuna (16 byte) tamamla (Basit Zero Padding)
    while len(duz_metin) % 16 != 0:
        duz_metin += b'\x00'
    
    state = bytearray(duz_metin)
    tur_anahtarlari = anahtar_genislet(anahtar)

    # 10 Tur İşlemi
    for i in range(10):
        # 1. AddRoundKey
        for j in range(16): state[j] ^= tur_anahtarlari[i][j]
        
        # 2. SubBytes: (x * 5 + 13) % 256
        for j in range(16): state[j] = (state[j] * 5 + 13) % 256
        
        # 3. ShiftRows (Sola Kaydır)
        # 1. Satır sabit, 2. Satır 1 sola, 3. Satır 2 sola, 4. Satır 3 sola
        s = state # Kısaltma
        # Row 1 (Index 4-7)
        state[4:8] = s[5:8] + s[4:5]
        # Row 2 (Index 8-11)
        state[8:12] = s[10:12] + s[8:10]
        # Row 3 (Index 12-15)
        state[12:16] = s[15:16] + s[12:15]

    return bytes(state)

# --- DEŞİFRELEME FONKSİYONLARI ---

def desifrele(sifreli_metin, anahtar):
    """
    FÖY İSTERİ 3: Desifrele(sifreli_metin, anahtar)
    Şifreleme işlemlerinin TAM TERSİNİ ters sırayla uygular.
    """
    state = bytearray(sifreli_metin)
    tur_anahtarlari = anahtar_genislet(anahtar)

    # İşlemleri tersten yapıyoruz (Round 9'dan 0'a)
    for i in range(9, -1, -1):
        # 1. Inverse ShiftRows (Sağa Kaydır)
        # Sola kaydırmanın tersi sağa kaydırmadır
        s = state[:] # Kopya al
        # Row 1 (Index 4-7): 1 Sağa -> [7,4,5,6]
        state[4:8] = s[7:8] + s[4:7]
        # Row 2 (Index 8-11): 2 Sağa -> [10,11,8,9]
        state[8:12] = s[10:12] + s[8:10]
        # Row 3 (Index 12-15): 3 Sağa -> [13,14,15,12]
        state[12:16] = s[13:16] + s[12:13]

        # 2. Inverse SubBytes
        # Şifrelerken: y = (x * 5 + 13) % 256
        # Çözerken:    x = (y - 13) * 205 % 256
        for j in range(16):
            val = (state[j] - 13) % 256
            state[j] = (val * INV_MULT) % 256

        # 3. Inverse AddRoundKey (XOR'un tersi yine XOR'dur)
        for j in range(16): state[j] ^= tur_anahtarlari[i][j]

    return bytes(state).rstrip(b'\x00') # Padding'i temizle

# --- TEST VE DOĞRULAMA (2.2) ---

def testleri_calistir():
    print("\n--- AŞAMA 2.2: TEST VE DOĞRULAMA ---")
    
    # SENARYO 1: BASİT DOĞRULAMA
    print("\n[TEST 1] Basit Şifreleme/Deşifreleme Doğrulaması")
    parola = "GizliAnahtar"
    mesaj = b"HocaOdevVerdi"
    
    anahtar = anahtar_uret(parola)
    sifreli = sifrele(mesaj, anahtar)
    cozulmus = desifrele(sifreli, anahtar)
    
    print(f"Orijinal: {mesaj}")
    print(f"Şifreli (Hex): {sifreli.hex().upper()}")
    print(f"Çözülmüş: {cozulmus}")
    
    if mesaj == cozulmus:
        print("SONUÇ: ✅ BAŞARILI (Metin başarıyla geri döndürüldü)")
    else:
        print("SONUÇ: ❌ BAŞARISIZ")

    # SENARYO 2: ANAHTAR HASSASİYETİ (ÇIĞ ETKİSİ)
    print("\n[TEST 2] Anahtar Hassasiyeti (Çığ Etkisi)")
    print("Amaç: Anahtardaki 1 bitlik değişimin şifreli metni tamamen değiştirdiğini kanıtlamak.")
    
    # 1. Durum: Normal Anahtar
    anahtar1 = anahtar_uret("A") # Hex: 41 00 ...
    c1 = sifrele(b"TestMesaji123456", anahtar1)
    
    # 2. Durum: Anahtarın sadece son bitini değiştir
    # "A" (01000001) yerine "C" (01000011) kullanalım. Çok küçük fark.
    anahtar2 = anahtar_uret("C") 
    c2 = sifrele(b"TestMesaji123456", anahtar2)
    
    print(f"Anahtar 1 Şifreli: {c1.hex().upper()}")
    print(f"Anahtar 2 Şifreli: {c2.hex().upper()}")
    
    # Farklılık Analizi
    farkli_byte_sayisi = sum(1 for a, b in zip(c1, c2) if a != b)
    print(f"Değişen Byte Sayısı: {farkli_byte_sayisi} / 16")
    
    if farkli_byte_sayisi > 8: # %50'den fazla değişim iyi bir çığ etkisidir
        print("SONUÇ: ✅ BAŞARILI (Yüksek Çığ Etkisi Gözlemlendi)")
    else:
        print("SONUÇ: ⚠️ ZAYIF (Benzerlikler var)")

if __name__ == "__main__":
    testleri_calistir()