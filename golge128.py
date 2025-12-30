import struct

# --- GÖLGE-128 (Shadow-128) Şifreleme Algoritması ---
# Blok Boyutu: 128 bit (16 Byte) [cite: 17]
# Tur Sayısı: 10 [cite: 15]

def main():
    print("--- GÖLGE-128 (Shadow-128) Şifreleme Algoritması ---")

    # 1. GİRİŞ AL [cite: 19, 21]
    # 16 Byte'lık (128 bit) örnek veri ve anahtar
    acik_metin = b"HocaOdevVerdi123"  # Tam 16 karakter
    ana_anahtar = b"GizliAnahtar2025" # Tam 16 karakter

    print(f"\nAçık Metin (Plaintext): {acik_metin.decode('utf-8')}")
    print(f"Hex Hali: {acik_metin.hex().upper()}")

    # Şifreleme İşlemi
    sifreli_metin = sifrele(acik_metin, ana_anahtar)

    print(f"\nŞifreli Metin (Ciphertext):")
    print(f"{sifreli_metin.hex().upper()}")

def sifrele(veri, anahtar):
    """
    Raporun 3. maddesindeki akış şemasını uygular.
    """
    # Veriyi byte dizisine (mutable) çevir
    state = bytearray(veri)
    
    # HAZIRLIK AŞAMASI: Anahtar Genişletme [cite: 22]
    tur_anahtarlari = anahtar_genislet(anahtar)

    # DÖNGÜ (10 Tur) [cite: 15]
    for i in range(10):
        # 1. ADIM: Anahtar Karıştırma (AddRoundKey) [cite: 42]
        # Veri = Veri XOR RK[i]
        state = add_round_key(state, tur_anahtarlari[i])

        # 2. ADIM: İkame İşlemi (SubBytes) [cite: 29, 43]
        # Formül: S(b) = (b * 5 + 13) mod 256
        state = sub_bytes(state)

        # 3. ADIM: Permütasyon (ShiftRows) [cite: 32, 44]
        # Satırları sola kaydır
        state = shift_rows(state)

    return bytes(state)

# --- MATEMATİKSEL FONKSİYONLAR ---

def anahtar_genislet(ana_anahtar):
    """
    Raporun 23-25. maddelerine göre 10 adet tur anahtarı üretir.
    Formül: Ki = (Ki-1 << 3) XOR Sabit
    """
    anahtarlar = []
    # İşlemleri kolay yapmak için anahtarı devasa bir sayıya (int) çeviriyoruz
    suanki_anahtar_int = int.from_bytes(ana_anahtar, byteorder='big')

    for i in range(10):
        # 1. Sola Dairesel Kaydır (3 bit) [cite: 25]
        # Python'da 128-bit rotate işlemi:
        suanki_anahtar_int = ((suanki_anahtar_int << 3) | (suanki_anahtar_int >> (128 - 3))) & ((1 << 128) - 1)
        
        # Sayıyı tekrar byte dizisine çevir
        yeni_anahtar = bytearray(suanki_anahtar_int.to_bytes(16, byteorder='big'))

        # 2. XOR Sabiti (Sabit olarak tur sayısını 'i+1' kullandık) [cite: 24]
        for j in range(16):
            yeni_anahtar[j] ^= (i + 1)
        
        anahtarlar.append(yeni_anahtar)
        
        # Bir sonraki tur için int halini güncelle
        suanki_anahtar_int = int.from_bytes(yeni_anahtar, byteorder='big')

    return anahtarlar

def sub_bytes(state):
    """
    Rapor Madde 29: S(b) = (b * 5 + 13) mod 256
    """
    for i in range(len(state)):
        val = state[i]
        # Doğrusal olmayan dönüşüm
        state[i] = (val * 5 + 13) % 256
    return state

def shift_rows(state):
    """
    Rapor Madde 32-36: Matris satır kaydırma işlemleri.
    Veri 16 elemanlı düz bir dizi ama 4x4 matris gibi davranıyoruz.
    """
    # Python'da 'slice' (dilimleme) ile kaydırma çok kolaydır.
    # 1. Satır (0-3): Sabit [cite: 33]
    row0 = state[0:4]
    
    # 2. Satır (4-7): 1 Sola [cite: 34] -> [4,5,6,7] yerine [5,6,7,4]
    row1 = state[4:8]
    row1 = row1[1:] + row1[:1]
    
    # 3. Satır (8-11): 2 Sola [cite: 35] -> [8,9,10,11] yerine [10,11,8,9]
    row2 = state[8:12]
    row2 = row2[2:] + row2[:2]
    
    # 4. Satır (12-15): 3 Sola [cite: 36] -> [12,13,14,15] yerine [15,12,13,14]
    row3 = state[12:16]
    row3 = row3[3:] + row3[:3]
    
    # Tekrar birleştir
    return row0 + row1 + row2 + row3

def add_round_key(state, anahtar):
    """
    Rapor Madde 42: Veri XOR Anahtar
    """
    for i in range(len(state)):
        state[i] ^= anahtar[i]
    return state

if __name__ == "__main__":
    main()
