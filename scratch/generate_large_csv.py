import csv
import os

def generate_csv():
    # Lista de productos reales detallados
    products = []
    
    # 1. GRANDSTREAM (Telefonía, Conmutadores, Redes, Accesorios)
    grandstream_products = [
        # Telefonía GRP (Carrier-Grade)
        {"product_name": "Teléfono IP Grandstream GRP2601", "description": "Teléfono IP básico de 2 líneas, 1 cuenta SIP, pantalla LCD de 132x48 píxeles, sin soporte PoE, ideal para oficina.", "price": 780.00, "stock": 50, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.8 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2601P", "description": "Teléfono IP básico de 2 líneas, 1 cuenta SIP, pantalla LCD, soporte PoE para alimentación por red.", "price": 890.00, "stock": 45, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.8 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2602", "description": "Teléfono IP de 2 líneas, 4 cuentas SIP, pantalla LCD retroiluminada de 2.21 pulgadas, audio HD.", "price": 950.00, "stock": 40, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.82 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2602P", "description": "Teléfono IP de 2 líneas, 4 cuentas SIP, pantalla retroiluminada, soporte PoE integrado.", "price": 1050.00, "stock": 60, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.82 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2602W", "description": "Teléfono IP de 2 líneas con soporte Wi-Fi de doble banda integrado para conexión inalámbrica.", "price": 1390.00, "stock": 30, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.85 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2603", "description": "Teléfono IP de 3 líneas, 6 cuentas SIP, pantalla LCD retroiluminada, puertos Gigabit Ethernet duales.", "price": 1150.00, "stock": 35, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.83 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2604", "description": "Teléfono IP de 3 líneas, 6 cuentas SIP, 10 teclas BLF de marcación rápida, puertos Gigabit Ethernet.", "price": 1350.00, "stock": 25, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.86 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2604P", "description": "Teléfono IP de 3 líneas, 6 cuentas SIP, 10 teclas BLF, soporte PoE y puertos Gigabit duales.", "price": 1490.00, "stock": 30, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.86 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2612", "description": "Teléfono IP de gama media con 4 líneas, 2 cuentas SIP, pantalla color de 2.4 pulgadas, sin PoE.", "price": 1320.00, "stock": 20, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.9 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2612P", "description": "Teléfono IP de gama media con 4 líneas, pantalla color de 2.4 pulgadas y PoE integrado.", "price": 1450.00, "stock": 35, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.9 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2612W", "description": "Teléfono IP de 4 líneas con Wi-Fi de doble banda y pantalla color de 2.4 pulgadas.", "price": 1780.00, "stock": 25, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.92 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2613", "description": "Teléfono IP profesional de 6 líneas, 3 cuentas SIP, pantalla a color de 2.8 pulgadas, puertos Gigabit.", "price": 1850.00, "stock": 20, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.95 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2614", "description": "Teléfono IP profesional con pantallas color duales, Wi-Fi de doble banda y Bluetooth integrados.", "price": 2450.00, "stock": 15, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.05 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2615", "description": "Teléfono IP carrier-grade de 10 líneas, Wi-Fi y Bluetooth integrados, pantalla a color de 4.3 pulgadas y PoE.", "price": 3190.00, "stock": 18, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.1 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2616", "description": "Teléfono IP profesional de 6 líneas con pantallas duales y Wi-Fi/Bluetooth integrados de fábrica.", "price": 2850.00, "stock": 12, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.08 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2624", "description": "Teléfono IP profesional de 8 líneas, Wi-Fi de doble banda, Bluetooth y soporte para módulo GBX20.", "price": 2980.00, "stock": 15, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.0 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2634", "description": "Teléfono IP profesional de 8 líneas, Wi-Fi de doble banda, Bluetooth y 10 teclas BLF físicas.", "price": 3100.00, "stock": 14, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.05 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2636", "description": "Teléfono IP carrier-grade de 12 líneas con pantalla a color de 4.3 pulgadas y 24 teclas BLF virtuales.", "price": 3750.00, "stock": 10, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.15 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2650", "description": "Teléfono IP profesional de 14 líneas, pantalla a color de 5.0 pulgadas, Wi-Fi y Bluetooth.", "price": 4200.00, "stock": 8, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.2 kg"},
        {"product_name": "Teléfono IP Grandstream GRP2670", "description": "Teléfono IP ejecutivo carrier-grade con pantalla táctil capacitiva de 7 pulgadas y hasta 12 líneas.", "price": 4990.00, "stock": 5, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.25 kg"},
        
        # Telefonía GXP (Clásicos)
        {"product_name": "Teléfono IP Grandstream GXP1610", "description": "Teléfono IP básico para pequeñas empresas con 1 cuenta SIP, 2 líneas y pantalla LCD de 132x48.", "price": 690.00, "stock": 50, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.75 kg"},
        {"product_name": "Teléfono IP Grandstream GXP1615", "description": "Teléfono IP básico de 1 cuenta SIP y 2 líneas con PoE integrado para fácil instalación.", "price": 790.00, "stock": 48, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.75 kg"},
        {"product_name": "Teléfono IP Grandstream GXP1620", "description": "Teléfono IP básico de 2 cuentas SIP y 2 líneas, pantalla retroiluminada de 132x48.", "price": 890.00, "stock": 30, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.78 kg"},
        {"product_name": "Teléfono IP Grandstream GXP1625", "description": "Teléfono IP básico de 2 cuentas SIP y 2 líneas con PoE integrado y pantalla retroiluminada.", "price": 990.00, "stock": 40, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.78 kg"},
        {"product_name": "Teléfono IP Grandstream GXP1628", "description": "Teléfono IP Gigabit básico de 2 cuentas SIP y 2 líneas, 8 teclas de marcación rápida BLF y PoE.", "price": 1490.00, "stock": 18, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.8 kg"},
        {"product_name": "Teléfono IP Grandstream GXP1630", "description": "Teléfono IP Gigabit básico de 3 cuentas SIP y 3 líneas, 8 teclas BLF y PoE integrado.", "price": 1690.00, "stock": 15, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.81 kg"},
        {"product_name": "Teléfono IP Grandstream GXP2130", "description": "Teléfono IP empresarial de 3 líneas, pantalla LCD a color de 2.8 pulgadas, 8 teclas BLF y PoE.", "price": 1890.00, "stock": 12, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.95 kg"},
        {"product_name": "Teléfono IP Grandstream GXP2135", "description": "Teléfono IP empresarial de 8 líneas, pantalla a color de 2.8 pulgadas, Gigabit, Bluetooth y PoE.", "price": 2150.00, "stock": 15, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.92 kg"},
        {"product_name": "Teléfono IP Grandstream GXP2140", "description": "Teléfono IP empresarial de 4 líneas con pantalla color de 4.3 pulgadas, Gigabit y soporte de módulos.", "price": 2490.00, "stock": 10, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.04 kg"},
        {"product_name": "Teléfono IP Grandstream GXP2160", "description": "Teléfono IP empresarial de 6 líneas con pantalla a color de 4.3 pulgadas, 24 teclas físicas BLF.", "price": 2890.00, "stock": 8, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.1 kg"},
        {"product_name": "Teléfono IP Grandstream GXP2170", "description": "Teléfono IP ejecutivo de 12 líneas, pantalla color de 4.3 pulgadas, 48 teclas virtuales BLF.", "price": 3190.00, "stock": 22, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.05 kg"},
        
        # Videoteléfonos y Telefonía Inalámbrica IP
        {"product_name": "Videoteléfono IP Grandstream GXV3350", "description": "Videoteléfono inteligente para Android con cámara integrada de 1MP y pantalla de 5.0 pulgadas.", "price": 4650.00, "stock": 6, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.2 kg"},
        {"product_name": "Videoteléfono IP Grandstream GXV3370", "description": "Videoteléfono IP inteligente con pantalla táctil de 7 pulgadas, cámara HD y sistema operativo Android.", "price": 5890.00, "stock": 5, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.4 kg"},
        {"product_name": "Videoteléfono IP Grandstream GXV3380", "description": "Videoteléfono IP ejecutivo con pantalla táctil IPS de 8 pulgadas, cámara de 2MP y soporte para Android 7.", "price": 7900.00, "stock": 3, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.6 kg"},
        {"product_name": "Videoteléfono IP Grandstream GXV3450", "description": "Videoteléfono inteligente de alta gama con Android 11, pantalla táctil de 5 pulgadas y cámara HD.", "price": 5490.00, "stock": 8, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.18 kg"},
        {"product_name": "Videoteléfono IP Grandstream GXV3470", "description": "Videoteléfono inteligente premium con Android 11, pantalla táctil de 7 pulgadas y cámara CMOS de 2MP.", "price": 6800.00, "stock": 4, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "1.35 kg"},
        {"product_name": "Teléfono Wi-Fi Portátil Grandstream WP810", "description": "Teléfono IP inalámbrico con Wi-Fi de doble banda integrado, audio HD, hasta 6 horas de conversación.", "price": 2100.00, "stock": 20, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.4 kg"},
        {"product_name": "Teléfono Wi-Fi Portátil Grandstream WP820", "description": "Teléfono IP inalámbrico con Wi-Fi de doble banda, Bluetooth, pantalla a color y botón PTT.", "price": 3100.00, "stock": 15, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.43 kg"},
        {"product_name": "Teléfono Wi-Fi Portátil Grandstream WP822", "description": "Teléfono IP inalámbrico empresarial con Wi-Fi de doble banda y batería de larga duración (8h conv).", "price": 2700.00, "stock": 18, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.41 kg"},
        {"product_name": "Teléfono Wi-Fi Portátil Grandstream WP825", "description": "Teléfono IP inalámbrico rugerizado con Wi-Fi de doble banda y protección IP67 contra polvo y agua.", "price": 3890.00, "stock": 10, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.45 kg"},
        {"product_name": "Teléfono Inalámbrico DECT Grandstream DP720", "description": "Auricular inalámbrico DECT para conmutadores IP, pantalla a color, audio HD y conector de 3.5mm.", "price": 1090.00, "stock": 25, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.32 kg"},
        {"product_name": "Teléfono Inalámbrico DECT Grandstream DP722", "description": "Auricular inalámbrico DECT de gama media con pantalla a color de 1.8 pulgadas y audio HD.", "price": 1250.00, "stock": 20, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.33 kg"},
        {"product_name": "Teléfono Inalámbrico DECT Grandstream DP730", "description": "Auricular inalámbrico DECT de alta gama, pantalla a color de 2.4 pulgadas, botón PTT y sensor de movimiento.", "price": 1890.00, "stock": 12, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.36 kg"},
        {"product_name": "Estación Base DECT Grandstream DP750", "description": "Estación base DECT VoIP para hasta 5 auriculares DP720, soporta 10 cuentas SIP y 5 llamadas simultáneas.", "price": 1190.00, "stock": 18, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.45 kg"},
        {"product_name": "Estación Base DECT Grandstream DP752", "description": "Estación base DECT VoIP de largo alcance para hasta 5 auriculares DECT, con botón de emparejamiento físico.", "price": 1390.00, "stock": 15, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.46 kg"},
        
        # Conmutadores UCM
        {"product_name": "Conmutador IP Grandstream UCM6301", "description": "Conmutador PBX IP empresarial para hasta 500 usuarios, 1 puerto FXS y 1 puerto FXO integrados.", "price": 7900.00, "stock": 6, "category": "Conmutadores IP", "brand": "Grandstream", "color": "Gris", "weight": "1.5 kg"},
        {"product_name": "Conmutador IP Grandstream UCM6302", "description": "Conmutador PBX IP empresarial para hasta 1000 usuarios, 2 puertos FXS y 2 puertos FXO integrados.", "price": 11500.00, "stock": 5, "category": "Conmutadores IP", "brand": "Grandstream", "color": "Gris", "weight": "1.6 kg"},
        {"product_name": "Conmutador IP Grandstream UCM6304", "description": "Conmutador PBX IP empresarial para hasta 2000 usuarios, 4 puertos FXS y 4 puertos FXO integrados.", "price": 28900.00, "stock": 3, "category": "Conmutadores IP", "brand": "Grandstream", "color": "Gris", "weight": "2.8 kg"},
        {"product_name": "Conmutador IP Grandstream UCM6308", "description": "Conmutador PBX IP empresarial de alto rendimiento para hasta 3000 usuarios, 8 FXS y 8 FXO.", "price": 48900.00, "stock": 2, "category": "Conmutadores IP", "brand": "Grandstream", "color": "Gris", "weight": "3.5 kg"},
        {"product_name": "Conmutador IP Grandstream UCM6300A", "description": "Conmutador PBX IP serie UCM6300 Audio, soporta hasta 250 usuarios, llamadas de solo audio.", "price": 4990.00, "stock": 10, "category": "Conmutadores IP", "brand": "Grandstream", "color": "Gris", "weight": "1.3 kg"},
        {"product_name": "Conmutador IP Grandstream UCM6302A", "description": "Conmutador PBX IP serie UCM6300 Audio, soporta hasta 500 usuarios, 2 puertos FXS y 2 FXO.", "price": 7690.00, "stock": 8, "category": "Conmutadores IP", "brand": "Grandstream", "color": "Gris", "weight": "1.4 kg"},
        {"product_name": "Conmutador IP Grandstream UCM6304A", "description": "Conmutador PBX IP serie UCM6300 Audio, soporta hasta 1000 usuarios, 4 puertos FXS y 4 FXO.", "price": 16900.00, "stock": 4, "category": "Conmutadores IP", "brand": "Grandstream", "color": "Gris", "weight": "2.2 kg"},
        {"product_name": "Conmutador IP Grandstream UCM6308A", "description": "Conmutador PBX IP serie UCM6300 Audio, soporta hasta 1500 usuarios, 8 puertos FXS y 8 FXO.", "price": 31500.00, "stock": 2, "category": "Conmutadores IP", "brand": "Grandstream", "color": "Gris", "weight": "3.0 kg"},
        {"product_name": "Conmutador IP Grandstream UCM6202", "description": "Conmutador PBX IP empresarial heredado, soporta hasta 500 usuarios y 30 llamadas simultáneas.", "price": 6800.00, "stock": 4, "category": "Conmutadores IP", "brand": "Grandstream", "color": "Negro", "weight": "1.2 kg"},
        {"product_name": "Conmutador IP Grandstream UCM6204", "description": "Conmutador PBX IP empresarial heredado, 4 puertos FXO, soporta hasta 500 usuarios.", "price": 9900.00, "stock": 3, "category": "Conmutadores IP", "brand": "Grandstream", "color": "Negro", "weight": "1.3 kg"},
        
        # Gateways / ATAs
        {"product_name": "Adaptador ATA Grandstream HT801", "description": "Adaptador de teléfono analógico de 1 puerto FXS para conectar teléfono común a red VoIP.", "price": 790.00, "stock": 35, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "0.3 kg"},
        {"product_name": "Adaptador ATA Grandstream HT802", "description": "Adaptador de teléfono analógico de 2 puertos FXS, enrutador NAT integrado, tamaño compacto.", "price": 890.00, "stock": 40, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "0.32 kg"},
        {"product_name": "Adaptador ATA Grandstream HT812", "description": "Adaptador de teléfono analógico de 2 puertos FXS con enrutador NAT Gigabit integrado.", "price": 1150.00, "stock": 30, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "0.35 kg"},
        {"product_name": "Adaptador ATA Grandstream HT814", "description": "Adaptador de teléfono analógico con 4 puertos FXS y enrutador Gigabit NAT integrado.", "price": 1980.00, "stock": 15, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "0.45 kg"},
        {"product_name": "Adaptador ATA Grandstream HT818", "description": "Adaptador de teléfono analógico de alta densidad con 8 puertos FXS y 2 puertos Gigabit.", "price": 3650.00, "stock": 10, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "0.6 kg"},
        {"product_name": "Gateway VoIP Grandstream GXW4004", "description": "Gateway analógico FXS de 4 puertos, ideal para integrar faxes y líneas analógicas a conmutadores IP.", "price": 2350.00, "stock": 12, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "0.8 kg"},
        {"product_name": "Gateway VoIP Grandstream GXW4008", "description": "Gateway analógico FXS de 8 puertos para conectar hasta 8 extensiones analógicas a telefonía IP.", "price": 3890.00, "stock": 8, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "0.85 kg"},
        {"product_name": "Gateway VoIP Grandstream GXW4216", "description": "Gateway analógico FXS de alta densidad con 16 puertos RJ11 y conector Telco de 50 pines.", "price": 6800.00, "stock": 6, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "2.1 kg"},
        {"product_name": "Gateway VoIP Grandstream GXW4224", "description": "Gateway analógico FXS de alta densidad de 24 puertos para migración masiva a telefonía IP.", "price": 8900.00, "stock": 5, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "2.3 kg"},
        {"product_name": "Gateway VoIP Grandstream GXW4232", "description": "Gateway analógico FXS de alta densidad con 32 puertos RJ11, montaje en rack.", "price": 10900.00, "stock": 4, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "2.5 kg"},
        {"product_name": "Gateway VoIP Grandstream GXW4248", "description": "Gateway analógico FXS de ultra-alta densidad con 48 puertos y conectores Telco RJ21.", "price": 16900.00, "stock": 2, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "3.2 kg"},
        {"product_name": "Gateway FXO Grandstream GXW4104", "description": "Gateway analógico de 4 puertos FXO para integrar hasta 4 líneas analógicas (Telmex) a conmutador IP.", "price": 3100.00, "stock": 8, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "0.8 kg"},
        {"product_name": "Gateway FXO Grandstream GXW4108", "description": "Gateway analógico de 8 puertos FXO para conectar 8 líneas analógicas a redes VoIP.", "price": 4990.00, "stock": 6, "category": "Gateways/ATAs", "brand": "Grandstream", "color": "Negro", "weight": "0.85 kg"},
        
        # Access Points GWN
        {"product_name": "Punto de Acceso Grandstream GWN7600", "description": "Access Point inalámbrico Wave-2 802.11ac de rango medio, ideal para oficinas medianas.", "price": 1850.00, "stock": 15, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.55 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7600LR", "description": "Access Point de largo alcance para exteriores (Long Range) con certificación IP66.", "price": 2890.00, "stock": 10, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.9 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7602", "description": "AP Wi-Fi compacto para hoteles y sucursales con switch de 4 puertos Ethernet integrados.", "price": 1100.00, "stock": 25, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.4 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7605", "description": "Access Point Wi-Fi 802.11ac Wave 2 de doble banda, soporta hasta 100 dispositivos.", "price": 1450.00, "stock": 20, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.5 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7605LR", "description": "AP Wi-Fi para exteriores Wave-2 802.11ac, alcance de hasta 250 metros.", "price": 2490.00, "stock": 12, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.8 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7610", "description": "AP inalámbrico 802.11ac corporativo de alto rendimiento para campus u oficinas.", "price": 1950.00, "stock": 8, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.6 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7615", "description": "AP inalámbrico empresarial 802.11ac Wave 2 con tecnología MIMO 3x3:3 de doble banda.", "price": 1690.00, "stock": 15, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.52 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7630", "description": "AP inalámbrico Wave-2 4x4:4 de alto rendimiento para interiores, capacidad de hasta 200 clientes.", "price": 2350.00, "stock": 14, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.58 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7630LR", "description": "AP para exteriores Wave-2 de alto rendimiento 4x4:4 MIMO con alcance de hasta 300m.", "price": 3980.00, "stock": 8, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "1.0 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7660", "description": "Access Point Wi-Fi 6 (802.11ax) empresarial de doble banda, soporta hasta 256 dispositivos.", "price": 2850.00, "stock": 18, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.6 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7660LR", "description": "Access Point exterior Wi-Fi 6 (802.11ax) de largo alcance con tecnología MIMO 2x2.", "price": 4200.00, "stock": 10, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.95 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7662", "description": "Access Point Wi-Fi 6 con soporte de doble banda y tecnología MIMO 4x4 para zonas densas.", "price": 3190.00, "stock": 12, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.62 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7664", "description": "AP Wi-Fi 6 de alto rendimiento para interiores con MIMO 4x4:4 y velocidad agregada de 3.55 Gbps.", "price": 3950.00, "stock": 10, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.65 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7664LR", "description": "AP exterior premium Wi-Fi 6 MIMO 4x4:4 con antena de alta ganancia, rango de hasta 300m.", "price": 5490.00, "stock": 6, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "1.1 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7661", "description": "Access Point Wi-Fi 6 de placa de pared (In-Wall) con puertos Ethernet RJ45 integrados.", "price": 2100.00, "stock": 15, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.42 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7624", "description": "AP de pared Wi-Fi 5 empresarial con switch Gigabit de 4 puertos e inyector PoE integrado.", "price": 1450.00, "stock": 20, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.45 kg"},
        {"product_name": "Punto de Acceso Grandstream GWN7625", "description": "Access Point Wi-Fi 5 de alto rendimiento para interiores con 2x2 MIMO y puertos Gigabit.", "price": 1590.00, "stock": 15, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Blanco", "weight": "0.53 kg"},
        
        # Routers GWN
        {"product_name": "Router VPN Grandstream GWN7000", "description": "Router Gigabit empresarial Multi-WAN con soporte VPN avanzado y balanceo de carga.", "price": 2100.00, "stock": 8, "category": "Redes cableadas", "brand": "Grandstream", "color": "Negro", "weight": "0.8 kg"},
        {"product_name": "Router VPN Grandstream GWN7001", "description": "Router Multi-WAN Gigabit compacto con cortafuegos de hardware y compatibilidad con GDMS.", "price": 1590.00, "stock": 12, "category": "Redes cableadas", "brand": "Grandstream", "color": "Negro", "weight": "0.6 kg"},
        {"product_name": "Router VPN Grandstream GWN7002", "description": "Router Gigabit Multi-WAN empresarial de alto rendimiento con 2 puertos SFP de fibra.", "price": 2350.00, "stock": 10, "category": "Redes cableadas", "brand": "Grandstream", "color": "Negro", "weight": "0.75 kg"},
        {"product_name": "Router VPN Grandstream GWN7003", "description": "Router Multi-WAN con puertos SFP y múltiples opciones de equilibrio de carga empresarial.", "price": 2980.00, "stock": 8, "category": "Redes cableadas", "brand": "Grandstream", "color": "Negro", "weight": "0.8 kg"},
        {"product_name": "Router Wi-Fi Grandstream GWN7052", "description": "Router inalámbrico de doble banda Gigabit AC1200 con soporte para VPN y redes Mesh.", "price": 1150.00, "stock": 25, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Negro", "weight": "0.48 kg"},
        {"product_name": "Router Wi-Fi Grandstream GWN7052F", "description": "Router inalámbrico de doble banda Gigabit con puerto SFP WAN para conexión por fibra óptica.", "price": 1490.00, "stock": 15, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Negro", "weight": "0.5 kg"},
        {"product_name": "Router Wi-Fi Grandstream GWN7062", "description": "Router inalámbrico Wi-Fi 6 (802.11ax) de doble banda con tecnología DL/UL MU-MIMO.", "price": 2100.00, "stock": 18, "category": "Redes inalámbricas", "brand": "Grandstream", "color": "Negro", "weight": "0.55 kg"},

        # Switches GWN
        {"product_name": "Switch Administrable Grandstream GWN7801", "description": "Switch L2+ administrable empresarial de 8 puertos Gigabit Ethernet y 2 puertos SFP.", "price": 3100.00, "stock": 12, "category": "Switches", "brand": "Grandstream", "color": "Gris", "weight": "1.8 kg"},
        {"product_name": "Switch Administrable Grandstream GWN7801P", "description": "Switch L2+ administrable empresarial con 8 puertos Gigabit PoE+ y 2 puertos SFP (120W).", "price": 4890.00, "stock": 10, "category": "Switches", "brand": "Grandstream", "color": "Gris oscuro", "weight": "2.1 kg"},
        {"product_name": "Switch Administrable Grandstream GWN7802", "description": "Switch L2+ administrable empresarial de 16 puertos Gigabit Ethernet y 4 puertos SFP.", "price": 4650.00, "stock": 8, "category": "Switches", "brand": "Grandstream", "color": "Gris", "weight": "2.4 kg"},
        {"product_name": "Switch Administrable Grandstream GWN7802P", "description": "Switch L2+ administrable de 16 puertos Gigabit PoE+ y 4 puertos SFP (presupuesto 240W).", "price": 7900.00, "stock": 6, "category": "Switches", "brand": "Grandstream", "color": "Gris oscuro", "weight": "2.8 kg"},
        {"product_name": "Switch Administrable Grandstream GWN7803", "description": "Switch L2+ administrable de 24 puertos Gigabit Ethernet y 4 puertos SFP para racks.", "price": 5890.00, "stock": 8, "category": "Switches", "brand": "Grandstream", "color": "Gris", "weight": "3.1 kg"},
        {"product_name": "Switch Administrable Grandstream GWN7803P", "description": "Switch L2+ administrable de 24 puertos Gigabit PoE+ y 4 puertos SFP (presupuesto 360W).", "price": 9900.00, "stock": 5, "category": "Switches", "brand": "Grandstream", "color": "Gris oscuro", "weight": "3.5 kg"},
        {"product_name": "Switch Administrable Grandstream GWN7811", "description": "Switch L3 administrable de alto rendimiento con 8 puertos Gigabit y 2 puertos 10Gb SFP+.", "price": 4800.00, "stock": 6, "category": "Switches", "brand": "Grandstream", "color": "Gris", "weight": "1.9 kg"},
        {"product_name": "Switch Administrable Grandstream GWN7811P", "description": "Switch L3 administrable de 8 puertos Gigabit PoE+ y 2 puertos 10Gb SFP+ para fibra.", "price": 6500.00, "stock": 4, "category": "Switches", "brand": "Grandstream", "color": "Gris oscuro", "weight": "2.2 kg"},
        {"product_name": "Switch Administrable Grandstream GWN7812", "description": "Switch L3 administrable con 16 puertos Gigabit y 4 puertos 10Gb SFP+ de alta velocidad.", "price": 6800.00, "stock": 5, "category": "Switches", "brand": "Grandstream", "color": "Gris", "weight": "2.5 kg"},
        {"product_name": "Switch Administrable Grandstream GWN7812P", "description": "Switch L3 administrable de 16 puertos Gigabit PoE+ y 4 puertos 10Gb SFP+.", "price": 9500.00, "stock": 3, "category": "Switches", "brand": "Grandstream", "color": "Gris oscuro", "weight": "2.9 kg"},
        {"product_name": "Switch Administrable Grandstream GWN7813", "description": "Switch L3 administrable de 24 puertos Gigabit y 4 puertos 10Gb SFP+.", "price": 8200.00, "stock": 4, "category": "Switches", "brand": "Grandstream", "color": "Gris", "weight": "3.2 kg"},
        {"product_name": "Switch Administrable Grandstream GWN7813P", "description": "Switch L3 administrable de 24 puertos Gigabit PoE+ y 4 puertos 10Gb SFP+.", "price": 12800.00, "stock": 3, "category": "Switches", "brand": "Grandstream", "color": "Gris oscuro", "weight": "3.6 kg"}
    ]
    products.extend(grandstream_products)
    
    # 2. UBIQUITI (UniFi, EdgeMAX, airMAX)
    ubiquiti_products = [
        # UniFi Access Points
        {"product_name": "Punto de Acceso Ubiquiti UAP-AC-LITE", "description": "Access Point compacto de doble banda 802.11ac, alcance de hasta 122 metros y puerto Gigabit.", "price": 1750.00, "stock": 30, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.35 kg"},
        {"product_name": "Punto de Acceso Ubiquiti UAP-AC-LR", "description": "Access Point de largo alcance (Long Range) 802.11ac, antena optimizada para distancias largas.", "price": 2150.00, "stock": 25, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.45 kg"},
        {"product_name": "Punto de Acceso Ubiquiti UAP-AC-PRO", "description": "Access Point empresarial de alto rendimiento 802.11ac de 3x3 MIMO para interiores y exteriores.", "price": 3100.00, "stock": 20, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.52 kg"},
        {"product_name": "Punto de Acceso Ubiquiti UAP-AC-M", "description": "Access Point UniFi AC Mesh para exteriores de doble banda con antenas desmontables omnidireccionales.", "price": 1980.00, "stock": 35, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.3 kg"},
        {"product_name": "Punto de Acceso Ubiquiti UAP-AC-M-PRO", "description": "Access Point exterior UniFi AC Mesh Pro con rendimiento MIMO 3x3 de doble banda y puerto Gigabit.", "price": 3950.00, "stock": 15, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.85 kg"},
        {"product_name": "Punto de Acceso Ubiquiti U6-Lite", "description": "Access Point compacto Wi-Fi 6 de doble banda con tecnología MIMO 2x2 y soporte PoE.", "price": 2190.00, "stock": 40, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.3 kg"},
        {"product_name": "Punto de Acceso Ubiquiti U6-Plus", "description": "Access Point mejorado Wi-Fi 6 que ofrece mayor velocidad y mejor cobertura a un menor costo.", "price": 2490.00, "stock": 30, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.32 kg"},
        {"product_name": "Punto de Acceso Ubiquiti U6-Pro", "description": "Access Point empresarial de alto rendimiento Wi-Fi 6 de doble banda MIMO 4x4.", "price": 3790.00, "stock": 20, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.46 kg"},
        {"product_name": "Punto de Acceso Ubiquiti U6-LR", "description": "Access Point Wi-Fi 6 de largo alcance con soporte de hasta 300 conexiones simultáneas.", "price": 4200.00, "stock": 15, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.8 kg"},
        {"product_name": "Punto de Acceso Ubiquiti U6-Enterprise", "description": "AP de gama ultra alta Wi-Fi 6E con soporte para banda de 6 GHz y puerto Ethernet a 2.5 Gbps.", "price": 6900.00, "stock": 8, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.96 kg"},
        {"product_name": "Punto de Acceso Ubiquiti U6-Mesh", "description": "AP Wi-Fi 6 cilíndrico de alto rendimiento para interiores o exteriores con protección IPX5.", "price": 3890.00, "stock": 18, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.4 kg"},
        {"product_name": "Punto de Acceso Ubiquiti U6-IW", "description": "Access Point Wi-Fi 6 de pared con switch de 4 puertos Gigabit integrados.", "price": 3650.00, "stock": 12, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.45 kg"},
        {"product_name": "Extensor Wi-Fi Ubiquiti U6-Extender", "description": "Extensor de rango Wi-Fi 6 inalámbrico que se conecta directamente a un enchufe de pared estándar.", "price": 2890.00, "stock": 15, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.29 kg"},

        # UniFi Switches
        {"product_name": "Switch Ubiquiti USW-Flex-Mini", "description": "Switch administrable compacto de 5 puertos Gigabit Ethernet con opciones de alimentación PoE.", "price": 720.00, "stock": 50, "category": "Switches", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.15 kg"},
        {"product_name": "Switch Ubiquiti USW-Lite-8-PoE", "description": "Switch de 8 puertos Gigabit con 4 puertos PoE+ auto-detectables y presupuesto de 52W.", "price": 2490.00, "stock": 25, "category": "Switches", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.45 kg"},
        {"product_name": "Switch Ubiquiti USW-Lite-16-PoE", "description": "Switch de 16 puertos Gigabit con 8 puertos PoE+ auto-detectables (presupuesto 45W).", "price": 4350.00, "stock": 18, "category": "Switches", "brand": "Ubiquiti", "color": "Blanco", "weight": "1.2 kg"},
        {"product_name": "Switch Ubiquiti US-8-60W", "description": "Switch PoE clásico de 8 puertos Gigabit con 4 puertos PoE 802.3af (presupuesto total 60W).", "price": 2350.00, "stock": 20, "category": "Switches", "brand": "Ubiquiti", "color": "Gris claro", "weight": "0.43 kg"},
        {"product_name": "Switch Ubiquiti US-8-150W", "description": "Switch administrable PoE+ de 8 puertos Gigabit y 2 puertos SFP (150W de capacidad).", "price": 4500.00, "stock": 12, "category": "Switches", "brand": "Ubiquiti", "color": "Gris claro", "weight": "1.7 kg"},
        {"product_name": "Switch Ubiquiti US-16-150W", "description": "Switch de 16 puertos Gigabit PoE+ con 2 puertos SFP para racks (capacidad 150W).", "price": 6390.00, "stock": 10, "category": "Switches", "brand": "Ubiquiti", "color": "Gris claro", "weight": "2.8 kg"},
        {"product_name": "Switch Ubiquiti USW-24-PoE", "description": "Switch administrable con pantalla táctil de 24 puertos Gigabit (16 puertos PoE+, 95W) y 2 SFP.", "price": 7900.00, "stock": 8, "category": "Switches", "brand": "Ubiquiti", "color": "Gris", "weight": "3.0 kg"},
        {"product_name": "Switch Ubiquiti USW-Pro-24-PoE", "description": "Switch L3 de 24 puertos Gigabit con 16 puertos PoE+, 8 puertos PoE++ (400W) y 2 puertos SFP+.", "price": 13900.00, "stock": 5, "category": "Switches", "brand": "Ubiquiti", "color": "Gris", "weight": "4.3 kg"},
        {"product_name": "Switch Ubiquiti USW-48-PoE", "description": "Switch L2 administrable de 48 puertos Gigabit (32 PoE+, 195W) y 4 puertos SFP.", "price": 12900.00, "stock": 6, "category": "Switches", "brand": "Ubiquiti", "color": "Gris", "weight": "4.7 kg"},
        {"product_name": "Switch Ubiquiti USW-Pro-48-PoE", "description": "Switch L3 administrable de 48 puertos con PoE+ y PoE++ (600W de presupuesto) y 4 puertos SFP+.", "price": 22500.00, "stock": 3, "category": "Switches", "brand": "Ubiquiti", "color": "Gris", "weight": "6.2 kg"},
        {"product_name": "Switch Ubiquiti USW-Pro-24", "description": "Switch L3 administrable de 24 puertos Gigabit y 2 puertos 10Gb SFP+ sin PoE.", "price": 8600.00, "stock": 6, "category": "Switches", "brand": "Ubiquiti", "color": "Gris", "weight": "3.5 kg"},
        {"product_name": "Switch Ubiquiti USW-Pro-48", "description": "Switch L3 administrable de 48 puertos Gigabit y 4 puertos 10Gb SFP+ sin PoE.", "price": 14900.00, "stock": 4, "category": "Switches", "brand": "Ubiquiti", "color": "Gris", "weight": "5.2 kg"},
        {"product_name": "Switch Ubiquiti USW-Flex", "description": "Switch Gigabit exterior de 5 puertos resistente al clima con capacidad de paso PoE.", "price": 2100.00, "stock": 15, "category": "Switches", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.5 kg"},

        # EdgeMAX Routers y Switches
        {"product_name": "Router Ubiquiti EdgeRouter X", "description": "Router Gigabit cableado ultracompacto de 5 puertos con soporte PoE pasivo passthrough.", "price": 1290.00, "stock": 30, "category": "Redes cableadas", "brand": "Ubiquiti", "color": "Negro", "weight": "0.17 kg"},
        {"product_name": "Router Ubiquiti EdgeRouter X-SFP", "description": "Router Gigabit con 5 puertos RJ45 PoE pasivos de 24V y 1 puerto SFP para fibra.", "price": 1890.00, "stock": 25, "category": "Redes cableadas", "brand": "Ubiquiti", "color": "Negro", "weight": "0.23 kg"},
        {"product_name": "Router Ubiquiti EdgeRouter 4", "description": "Router de alto rendimiento con 3 puertos Gigabit y 1 puerto SFP (capacidad de 3.4M pps).", "price": 4200.00, "stock": 10, "category": "Redes cableadas", "brand": "Ubiquiti", "color": "Negro", "weight": "0.79 kg"},
        {"product_name": "Router Ubiquiti EdgeRouter 6P", "description": "Router de alto rendimiento con 5 puertos Gigabit PoE y 1 puerto SFP para conectividad de fibra.", "price": 5490.00, "stock": 8, "category": "Redes cableadas", "brand": "Ubiquiti", "color": "Negro", "weight": "0.85 kg"},
        {"product_name": "Router Ubiquiti EdgeRouter 12", "description": "Router Gigabit con 10 puertos RJ45, 2 puertos SFP y funciones avanzadas de capa 3.", "price": 6390.00, "stock": 6, "category": "Redes cableadas", "brand": "Ubiquiti", "color": "Negro", "weight": "1.3 kg"},
        {"product_name": "Router Ubiquiti EdgeRouter Infinity", "description": "Router de fibra de 8 puertos SFP+ 10G y 1 puerto Gigabit Ethernet para aplicaciones masivas.", "price": 38900.00, "stock": 2, "category": "Redes cableadas", "brand": "Ubiquiti", "color": "Negro", "weight": "4.9 kg"},
        {"product_name": "Switch Ubiquiti EdgeSwitch 8 150W", "description": "Switch L2 administrable con 8 puertos Gigabit PoE+ (150W) y 2 puertos SFP para racks.", "price": 4390.00, "stock": 10, "category": "Switches", "brand": "Ubiquiti", "color": "Negro", "weight": "1.7 kg"},
        {"product_name": "Switch Ubiquiti EdgeSwitch 16 150W", "description": "Switch administrable PoE+ de 16 puertos Gigabit y 2 puertos SFP (150W).", "price": 6200.00, "stock": 8, "category": "Switches", "brand": "Ubiquiti", "color": "Negro", "weight": "2.8 kg"},
        {"product_name": "Switch Ubiquiti EdgeSwitch 24 250W", "description": "Switch administrable PoE+ de 24 puertos Gigabit y 2 puertos SFP (250W de presupuesto).", "price": 9500.00, "stock": 5, "category": "Switches", "brand": "Ubiquiti", "color": "Negro", "weight": "3.7 kg"},
        {"product_name": "Switch Ubiquiti EdgeSwitch 48 500W", "description": "Switch administrable de alta densidad con 48 puertos Gigabit PoE+ y 2 SFP+ (500W).", "price": 18900.00, "stock": 3, "category": "Switches", "brand": "Ubiquiti", "color": "Negro", "weight": "5.8 kg"},

        # airMAX Inalámbricos
        {"product_name": "CPE Ubiquiti NanoStation Loco M5", "description": "Antena exterior compacta airMAX de 5 GHz con alcance de hasta 5 km y antena integrada de 13 dBi.", "price": 1150.00, "stock": 50, "category": "Antenas / Enlaces", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.18 kg"},
        {"product_name": "CPE Ubiquiti NanoStation M5", "description": "Antena exterior airMAX 5 GHz de 16 dBi de ganancia, puertos de red duales con soporte PoE.", "price": 1780.00, "stock": 35, "category": "Antenas / Enlaces", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.4 kg"},
        {"product_name": "CPE Ubiquiti NanoStation AC loco", "description": "Antena inalámbrica exterior de 5 GHz AC con tecnología airMAX de hasta 450 Mbps.", "price": 1250.00, "stock": 45, "category": "Antenas / Enlaces", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.18 kg"},
        {"product_name": "CPE Ubiquiti NanoStation AC", "description": "Antena airMAX AC de 5 GHz para enlaces inalámbricos punto a punto y punto a multipunto.", "price": 2890.00, "stock": 20, "category": "Antenas / Enlaces", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.5 kg"},
        {"product_name": "CPE Ubiquiti PowerBeam AC Gen2", "description": "Antena directiva tipo plato de 5 GHz AC de 25 dBi con blindaje de RF para enlaces de más de 15 km.", "price": 3100.00, "stock": 18, "category": "Antenas / Enlaces", "brand": "Ubiquiti", "color": "Blanco", "weight": "2.2 kg"},
        {"product_name": "CPE Ubiquiti LiteBeam M5", "description": "Antena exterior tipo rejilla ultraligera de 5 GHz de 23 dBi de ganancia, alcance medio.", "price": 1150.00, "stock": 40, "category": "Antenas / Enlaces", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.75 kg"},
        {"product_name": "CPE Ubiquiti LiteBeam AC Gen2", "description": "Antena exterior tipo rejilla airMAX AC de 5 GHz con alcance de hasta 15 km y 23 dBi de ganancia.", "price": 1490.00, "stock": 50, "category": "Antenas / Enlaces", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.98 kg"},
        {"product_name": "Radio Base Ubiquiti Rocket M5", "description": "Transceptor de alta potencia airMAX de 5 GHz para acoplamiento a antenas direccionales o sectoriales.", "price": 1980.00, "stock": 15, "category": "Antenas / Enlaces", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.5 kg"},
        {"product_name": "Radio Base Ubiquiti Rocket Prism 5AC", "description": "Radio airMAX AC de 5 GHz de alto rendimiento para estaciones base con filtrado activo de RF.", "price": 4650.00, "stock": 10, "category": "Antenas / Enlaces", "brand": "Ubiquiti", "color": "Plateado", "weight": "0.4 kg"},
        {"product_name": "Inyector PoE Ubiquiti POE-24-12W-G", "description": "Adaptador PoE de 24 VDC y 0.5 A con puertos Gigabit Ethernet para equipos airMAX.", "price": 280.00, "stock": 100, "category": "Accesorios de Red", "brand": "Ubiquiti", "color": "Negro", "weight": "0.15 kg"},
        {"product_name": "Inyector PoE Ubiquiti POE-48-24W-G", "description": "Adaptador PoE de 48 VDC y 0.5 A con protección contra sobretensiones y puerto Gigabit.", "price": 420.00, "stock": 60, "category": "Accesorios de Red", "brand": "Ubiquiti", "color": "Negro", "weight": "0.16 kg"}
    ]
    products.extend(ubiquiti_products)
    
    # 3. MIKROTIK (RouterBOARDS, Cloud Core, Cloud Switches)
    mikrotik_products = [
        # hEX Series (Routers cableados básicos)
        {"product_name": "Router MikroTik hEX lite", "description": "Router básico de 5 puertos Ethernet 10/100, diseño compacto de plástico, ideal para el hogar.", "price": 950.00, "stock": 30, "category": "Redes cableadas", "brand": "MikroTik", "color": "Blanco", "weight": "0.12 kg"},
        {"product_name": "Router MikroTik hEX", "description": "Router cableado Gigabit de 5 puertos con CPU de doble núcleo a 880 MHz y ranura MicroSD.", "price": 1250.00, "stock": 45, "category": "Redes cableadas", "brand": "MikroTik", "color": "Gris/Azul", "weight": "0.14 kg"},
        {"product_name": "Router MikroTik hEX PoE", "description": "Router Gigabit de 5 puertos con salida PoE pasiva en los puertos 2 a 5 para alimentación remota.", "price": 1780.00, "stock": 20, "category": "Redes cableadas", "brand": "MikroTik", "color": "Gris/Azul", "weight": "0.15 kg"},
        {"product_name": "Router MikroTik hEX S", "description": "Router Gigabit de 5 puertos con soporte para fibra SFP y salida PoE en el puerto 5.", "price": 1690.00, "stock": 25, "category": "Redes cableadas", "brand": "MikroTik", "color": "Gris/Azul", "weight": "0.15 kg"},

        # hAP Series (Puntos de Acceso / Routers SoHo)
        {"product_name": "Router Inalámbrico MikroTik hAP mini", "description": "Punto de acceso compacto de 2.4 GHz de 3 puertos 10/100, ideal para configuraciones residenciales.", "price": 590.00, "stock": 40, "category": "Redes inalámbricas", "brand": "MikroTik", "color": "Negro", "weight": "0.1 kg"},
        {"product_name": "Router Inalámbrico MikroTik hAP lite", "description": "AP inalámbrico de 2.4 GHz con 4 puertos Ethernet 10/100 y botón WPS físico (modelo RB941).", "price": 690.00, "stock": 50, "category": "Redes inalámbricas", "brand": "MikroTik", "color": "Gris/Azul", "weight": "0.12 kg"},
        {"product_name": "Router Inalámbrico MikroTik hAP ac lite", "description": "AP inalámbrico de doble banda simultánea de 2.4 GHz y 5 GHz con 5 puertos Ethernet 10/100.", "price": 1150.00, "stock": 30, "category": "Redes inalámbricas", "brand": "MikroTik", "color": "Gris/Azul", "weight": "0.14 kg"},
        {"product_name": "Router Inalámbrico MikroTik hAP ac2", "description": "Router inalámbrico Gigabit de doble banda simultánea con CPU de 4 núcleos a 716 MHz.", "price": 1490.00, "stock": 25, "category": "Redes inalámbricas", "brand": "MikroTik", "color": "Negro", "weight": "0.22 kg"},
        {"product_name": "Router Inalámbrico MikroTik hAP ac3", "description": "Router de doble banda Gigabit con antenas externas de alta ganancia y soporte de montaje vertical.", "price": 2100.00, "stock": 18, "category": "Redes inalámbricas", "brand": "MikroTik", "color": "Negro", "weight": "0.35 kg"},
        {"product_name": "Router Inalámbrico MikroTik hAP ax2", "description": "Router inalámbrico Wi-Fi 6 de doble banda con cifrado WPA3 y puertos Gigabit (modelo C52iG).", "price": 2350.00, "stock": 15, "category": "Redes inalámbricas", "brand": "MikroTik", "color": "Negro", "weight": "0.36 kg"},
        {"product_name": "Router Inalámbrico MikroTik hAP ax3", "description": "Router premium Wi-Fi 6 de doble banda con CPU quad-core a 1.8 GHz y puerto Ethernet 2.5G.", "price": 3150.00, "stock": 12, "category": "Redes inalámbricas", "brand": "MikroTik", "color": "Negro", "weight": "0.45 kg"},

        # CCR Series (Cloud Core Routers de núcleo empresarial)
        {"product_name": "Router MikroTik CCR2004-16G-2S+", "description": "Router empresarial de alto rendimiento con 16 puertos Gigabit y 2 puertos 10Gb SFP+.", "price": 9900.00, "stock": 5, "category": "Redes cableadas", "brand": "MikroTik", "color": "Blanco", "weight": "2.2 kg"},
        {"product_name": "Router MikroTik CCR2004-1G-12S+2XS", "description": "Router empresarial de fibra con 12 puertos 10G SFP+ y 2 puertos 25G SFP28 para backbone.", "price": 13900.00, "stock": 3, "category": "Redes cableadas", "brand": "MikroTik", "color": "Blanco", "weight": "2.4 kg"},
        {"product_name": "Router MikroTik CCR2116-12G-4S+", "description": "Router de núcleo masivo con CPU ARM de 16 núcleos, 12 puertos Gigabit y 4 puertos 10Gb SFP+.", "price": 28900.00, "stock": 2, "category": "Redes cableadas", "brand": "MikroTik", "color": "Blanco", "weight": "3.5 kg"},

        # CRS Series (Cloud Router Switches)
        {"product_name": "Switch MikroTik CRS305-1G-4S+IN", "description": "Switch de fibra de escritorio ultracompacto con 4 puertos 10Gb SFP+ y 1 puerto Gigabit Ethernet.", "price": 2980.00, "stock": 15, "category": "Switches", "brand": "MikroTik", "color": "Blanco", "weight": "0.41 kg"},
        {"product_name": "Switch MikroTik CRS309-1G-8S+IN", "description": "Switch de fibra administrable con 8 puertos 10Gb SFP+, montaje en rack opcional.", "price": 6390.00, "stock": 8, "category": "Switches", "brand": "MikroTik", "color": "Blanco", "weight": "1.2 kg"},
        {"product_name": "Switch MikroTik CRS310-1G-8S-2S+IN", "description": "Switch administrable con 8 puertos SFP de 1Gb y 2 puertos SFP+ de 10Gb para distribución de fibra.", "price": 5490.00, "stock": 10, "category": "Switches", "brand": "MikroTik", "color": "Blanco", "weight": "1.1 kg"},
        {"product_name": "Switch MikroTik CRS326-24G-2S+RM", "description": "Switch administrable con 24 puertos Gigabit y 2 puertos SFP+ para montaje en rack de 1UR.", "price": 3890.00, "stock": 12, "category": "Switches", "brand": "MikroTik", "color": "Blanco", "weight": "1.6 kg"},
        {"product_name": "Switch MikroTik CRS326-24G-2S+OUT", "description": "Switch Gigabit de exterior de 24 puertos con caja hermética impermeable IP54.", "price": 4990.00, "stock": 5, "category": "Switches", "brand": "MikroTik", "color": "Blanco", "weight": "2.8 kg"},
        {"product_name": "Switch MikroTik CRS328-24P-4S+RM", "description": "Switch PoE administrable con 24 puertos Gigabit PoE+ (capacidad total 450W) y 4 SFP+.", "price": 10900.00, "stock": 6, "category": "Switches", "brand": "MikroTik", "color": "Blanco", "weight": "3.8 kg"},
        {"product_name": "Switch MikroTik CRS354-48G-4S+2LQ+RM", "description": "Switch administrable de alta densidad de 48 puertos Gigabit, 4 puertos SFP+ y 2 QSFP+ 40G.", "price": 14900.00, "stock": 4, "category": "Switches", "brand": "MikroTik", "color": "Blanco", "weight": "4.2 kg"},

        # RB Series (RouterBOARDS profesionales)
        {"product_name": "Router MikroTik RB3011UiAS-RM", "description": "Router Gigabit potente de 10 puertos con arquitectura ARM, puerto SFP y pantalla LCD táctil.", "price": 4390.00, "stock": 12, "category": "Redes cableadas", "brand": "MikroTik", "color": "Negro", "weight": "1.1 kg"},
        {"product_name": "Router MikroTik RB4011iGS+RM", "description": "Router de 10 puertos Gigabit con CPU quad-core de 1.4 GHz y jaula SFP+ para fibra de 10Gb.", "price": 5890.00, "stock": 10, "category": "Redes cableadas", "brand": "MikroTik", "color": "Negro", "weight": "1.15 kg"},
        {"product_name": "Router Inalámbrico MikroTik RB4011-WiFi", "description": "Router de 10 puertos Gigabit con Wi-Fi integrado de doble banda de alta velocidad.", "price": 6800.00, "stock": 8, "category": "Redes inalámbricas", "brand": "MikroTik", "color": "Negro", "weight": "1.25 kg"},
        {"product_name": "Router MikroTik RB5009UG+S+IN", "description": "Router robusto de 7 puertos Gigabit, 1 puerto Ethernet 2.5G y 1 puerto SFP+ 10G.", "price": 4900.00, "stock": 15, "category": "Redes cableadas", "brand": "MikroTik", "color": "Negro", "weight": "0.56 kg"},
        {"product_name": "Router MikroTik RB5009UPr+S+OUT", "description": "Router exterior reforzado con protección IP66 y 8 puertos con capacidades de salida PoE.", "price": 7900.00, "stock": 6, "category": "Redes cableadas", "brand": "MikroTik", "color": "Gris", "weight": "1.3 kg"}
    ]
    products.extend(mikrotik_products)
    
    # 4. LINKEDPRO (Racks, organizadores, patch panels, accesorios pasivos)
    linkedpro_products = [
        # Gabinetes de pared
        {"product_name": "Gabinete de Pared LinkedPRO 6UR", "description": "Gabinete de montaje en pared de 6 unidades de rack, dimensiones 60 x 45 cm, puerta de cristal templado.", "price": 1450.00, "stock": 15, "category": "Gabinete / Racks", "brand": "LinkedPRO", "color": "Negro", "weight": "12.0 kg"},
        {"product_name": "Gabinete de Pared LinkedPRO 9UR", "description": "Gabinete para pared de 9 unidades de rack, dimensiones 60 x 45 cm, paneles laterales desmontables.", "price": 1690.00, "stock": 12, "category": "Gabinete / Racks", "brand": "LinkedPRO", "color": "Negro", "weight": "15.2 kg"},
        {"product_name": "Gabinete de Pared LinkedPRO 12UR", "description": "Gabinete para pared de 12 unidades de rack, dimensiones 60 x 45 cm, incluye ventilador superior.", "price": 1980.00, "stock": 10, "category": "Gabinete / Racks", "brand": "LinkedPRO", "color": "Negro", "weight": "18.5 kg"},
        {"product_name": "Gabinete de Pared LinkedPRO 12UR Profundo", "description": "Gabinete de pared de 12 unidades de rack de 60 cm de profundidad para alojar servidores compactos.", "price": 2200.00, "stock": 8, "category": "Gabinete / Racks", "brand": "LinkedPRO", "color": "Negro", "weight": "21.0 kg"},
        {"product_name": "Gabinete de Pared LinkedPRO 16UR", "description": "Gabinete para pared de 16 unidades de rack, 60 x 60 cm de espacio útil, puerta con llave de seguridad.", "price": 2850.00, "stock": 6, "category": "Gabinete / Racks", "brand": "LinkedPRO", "color": "Negro", "weight": "26.5 kg"},
        {"product_name": "Gabinete de Piso LinkedPRO 22UR", "description": "Gabinete de piso para telecomunicaciones de 22 unidades de rack con puerta frontal ventilada.", "price": 5490.00, "stock": 4, "category": "Gabinete / Racks", "brand": "LinkedPRO", "color": "Negro", "weight": "42.0 kg"},
        
        # Racks
        {"product_name": "Rack de Dos Postes LinkedPRO 45UR", "description": "Rack de dos postes de aluminio para montaje de equipos de 19 pulgadas, capacidad 45UR.", "price": 1750.00, "stock": 10, "category": "Gabinete / Racks", "brand": "LinkedPRO", "color": "Negro", "weight": "15.0 kg"},
        {"product_name": "Rack de Dos Postes LinkedPRO 24UR", "description": "Rack de dos postes de acero de 24 unidades de rack, ideal para cuartos de comunicación pequeños.", "price": 1250.00, "stock": 15, "category": "Gabinete / Racks", "brand": "LinkedPRO", "color": "Negro", "weight": "10.5 kg"},
        {"product_name": "Rack de Dos Postes LinkedPRO 28UR", "description": "Rack de dos postes de 28 unidades de rack para sujeción de cableado estructurado.", "price": 1390.00, "stock": 12, "category": "Gabinete / Racks", "brand": "LinkedPRO", "color": "Negro", "weight": "11.8 kg"},

        # Organizadores y canalización
        {"product_name": "Organizador de Cables LinkedPRO 1UR Sencillo", "description": "Organizador horizontal de cables de 1 unidad de rack, ducto ranurado de plástico con tapa.", "price": 180.00, "stock": 50, "category": "Accesorios de Red", "brand": "LinkedPRO", "color": "Negro", "weight": "0.45 kg"},
        {"product_name": "Organizador de Cables LinkedPRO 2UR Sencillo", "description": "Organizador horizontal de cables de 2 unidades de rack, ranuras traseras para paso de cables.", "price": 280.00, "stock": 40, "category": "Accesorios de Red", "brand": "LinkedPRO", "color": "Negro", "weight": "0.65 kg"},
        {"product_name": "Organizador de Cables LinkedPRO 1UR Doble Cara", "description": "Organizador horizontal doble cara de 1 unidad de rack para acomodo frontal y trasero.", "price": 310.00, "stock": 25, "category": "Accesorios de Red", "brand": "LinkedPRO", "color": "Negro", "weight": "0.8 kg"},
        {"product_name": "Organizador de Cables LinkedPRO 2UR Doble Cara", "description": "Organizador horizontal doble cara de 2 unidades de rack con anillas de administración.", "price": 420.00, "stock": 20, "category": "Accesorios de Red", "brand": "LinkedPRO", "color": "Negro", "weight": "1.1 kg"},

        # Pasivos
        {"product_name": "Patch Panel LinkedPRO 24 Puertos Cat6", "description": "Panel de parcheo de 24 puertos categoría 6 para rack de 19 pulgadas, etiquetas integradas.", "price": 850.00, "stock": 25, "category": "Cableado estructurado", "brand": "LinkedPRO", "color": "Negro", "weight": "1.2 kg"},
        {"product_name": "Patch Panel LinkedPRO 48 Puertos Cat6", "description": "Panel de parcheo de 48 puertos categoría 6 de alto rendimiento para montaje de 2UR.", "price": 1590.00, "stock": 15, "category": "Cableado estructurado", "brand": "LinkedPRO", "color": "Negro", "weight": "2.1 kg"},
        {"product_name": "Plugs RJ45 Cat6 LinkedPRO (Bolsa de 100)", "description": "Conectores modulares RJ45 macho categoría 6 con contactos chapados en oro.", "price": 280.00, "stock": 80, "category": "Accesorios de Red", "brand": "LinkedPRO", "color": "Transparente", "weight": "0.25 kg"},
        {"product_name": "Plugs RJ45 Cat5e LinkedPRO (Bolsa de 100)", "description": "Conectores modulares RJ45 macho categoría 5e estándar para cables de parcheo.", "price": 180.00, "stock": 70, "category": "Accesorios de Red", "brand": "LinkedPRO", "color": "Transparente", "weight": "0.22 kg"},
        {"product_name": "Jack RJ45 Cat6 LinkedPRO Azul", "description": "Conector modular RJ45 hembra tipo Keystone categoría 6 de impacto 180 grados.", "price": 45.00, "stock": 200, "category": "Cableado estructurado", "brand": "LinkedPRO", "color": "Azul", "weight": "0.02 kg"},
        {"product_name": "Jack RJ45 Cat6 LinkedPRO Blanco", "description": "Conector modular RJ45 hembra tipo Keystone categoría 6 para faceplates.", "price": 45.00, "stock": 200, "category": "Cableado estructurado", "brand": "LinkedPRO", "color": "Blanco", "weight": "0.02 kg"},
        {"product_name": "Jack RJ45 Cat6 LinkedPRO Amarillo", "description": "Conector modular RJ45 hembra tipo Keystone categoría 6 para voz y datos.", "price": 45.00, "stock": 150, "category": "Cableado estructurado", "brand": "LinkedPRO", "color": "Amarillo", "weight": "0.02 kg"},
        
        # Bobinas
        {"product_name": "Bobina de Cable UTP Cat6 LinkedPRO 305m (CCA)", "description": "Bobina de cable de red Cat6 para aplicaciones básicas interiores de corta distancia (aleación).", "price": 1980.00, "stock": 40, "category": "Cableado estructurado", "brand": "LinkedPRO", "color": "Gris", "weight": "9.8 kg"},
        {"product_name": "Bobina de Cable UTP Cat6 LinkedPRO 100% Cobre 305m", "description": "Bobina de cable de red Cat6 para interiores con conductores 100% cobre para redes gigabit.", "price": 2890.00, "stock": 25, "category": "Cableado estructurado", "brand": "LinkedPRO", "color": "Azul", "weight": "11.2 kg"},
        {"product_name": "Bobina de Cable UTP Cat5e LinkedPRO 305m (CCA)", "description": "Bobina económica de cable de red Cat5e para interiores de datos e instrumentación.", "price": 1150.00, "stock": 35, "category": "Cableado estructurado", "brand": "LinkedPRO", "color": "Gris", "weight": "8.2 kg"},
        {"product_name": "Bobina de Cable FTP Cat6 Exterior LinkedPRO 305m", "description": "Bobina de cable blindada FTP categoría 6 para instalación en intemperie, doble cubierta.", "price": 4650.00, "stock": 15, "category": "Cableado estructurado", "brand": "LinkedPRO", "color": "Negro", "weight": "14.5 kg"},

        # Patch Cords LinkedPRO
        {"product_name": "Patch Cord Cat6 LinkedPRO 0.3m Azul", "description": "Cable de parcheo pre-armado y certificado de categoría 6 UTP, longitud de 30 cm.", "price": 28.00, "stock": 150, "category": "Accesorios de Red", "brand": "LinkedPRO", "color": "Azul", "weight": "0.05 kg"},
        {"product_name": "Patch Cord Cat6 LinkedPRO 0.9m Azul", "description": "Cable de parcheo pre-armado y certificado de categoría 6 UTP, longitud de 90 cm.", "price": 45.00, "stock": 180, "category": "Accesorios de Red", "brand": "LinkedPRO", "color": "Azul", "weight": "0.08 kg"},
        {"product_name": "Patch Cord Cat6 LinkedPRO 1.5m Azul", "description": "Cable de parcheo certificado Cat6 UTP con capuchas protectoras de clips, 1.5 metros.", "price": 55.00, "stock": 200, "category": "Accesorios de Red", "brand": "LinkedPRO", "color": "Azul", "weight": "0.12 kg"},
        {"product_name": "Patch Cord Cat6 LinkedPRO 2.1m Azul", "description": "Cable de parcheo certificado Cat6 UTP para interconexión en racks, 2.1 metros.", "price": 65.00, "stock": 120, "category": "Accesorios de Red", "brand": "LinkedPRO", "color": "Azul", "weight": "0.15 kg"},
        {"product_name": "Patch Cord Cat6 LinkedPRO 3.0m Azul", "description": "Cable de parcheo certificado Cat6 UTP, longitud de 3.0 metros.", "price": 75.00, "stock": 100, "category": "Accesorios de Red", "brand": "LinkedPRO", "color": "Azul", "weight": "0.18 kg"},
        {"product_name": "Patch Cord Cat6 LinkedPRO 4.5m Azul", "description": "Cable de parcheo certificado Cat6 UTP para distancias largas, 4.5 metros.", "price": 95.00, "stock": 80, "category": "Accesorios de Red", "brand": "LinkedPRO", "color": "Azul", "weight": "0.22 kg"}
    ]
    products.extend(linkedpro_products)
    
    # 5. PANDUIT (Pasivos premium, conectores Mini-Com, cableado estructurado)
    panduit_products = [
        # Jacks Mini-Com
        {"product_name": "Jack RJ45 Cat6 Panduit Blanco", "description": "Jack modular Mini-Com categoría 6 UTP con terminación TG de fácil impacto, color blanco.", "price": 145.00, "stock": 150, "category": "Cableado estructurado", "brand": "Panduit", "color": "Blanco", "weight": "0.02 kg"},
        {"product_name": "Jack RJ45 Cat6 Panduit Azul", "description": "Jack modular Mini-Com categoría 6 UTP con tecnología de cancelación de ruido alien crosstalk.", "price": 145.00, "stock": 120, "category": "Cableado estructurado", "brand": "Panduit", "color": "Azul", "weight": "0.02 kg"},
        {"product_name": "Jack RJ45 Cat6 Panduit Rojo", "description": "Jack modular Mini-Com categoría 6 para diferenciación de redes críticas (telefonía o seguridad).", "price": 145.00, "stock": 80, "category": "Cableado estructurado", "brand": "Panduit", "color": "Rojo", "weight": "0.02 kg"},
        {"product_name": "Jack RJ45 Cat6 Panduit Verde", "description": "Jack modular Mini-Com categoría 6 con sistema de identificación por colores.", "price": 145.00, "stock": 70, "category": "Cableado estructurado", "brand": "Panduit", "color": "Verde", "weight": "0.02 kg"},
        {"product_name": "Jack RJ45 Cat6A Panduit Negro", "description": "Jack modular Mini-Com de alto rendimiento categoría 6A blindado, para velocidades de 10Gbps.", "price": 260.00, "stock": 50, "category": "Cableado estructurado", "brand": "Panduit", "color": "Negro", "weight": "0.03 kg"},
        
        # Faceplates Mini-Com
        {"product_name": "Faceplate Panduit 2 Posiciones Blanco", "description": "Placa de pared Mini-Com de 2 posiciones para montaje empotrado de jacks, color blanco hueso.", "price": 45.00, "stock": 100, "category": "Cableado estructurado", "brand": "Panduit", "color": "Blanco", "weight": "0.05 kg"},
        {"product_name": "Faceplate Panduit 4 Posiciones Blanco", "description": "Placa de pared de 4 posiciones Mini-Com para instalación de múltiples salidas de red.", "price": 55.00, "stock": 80, "category": "Cableado estructurado", "brand": "Panduit", "color": "Blanco", "weight": "0.06 kg"},
        {"product_name": "Faceplate Panduit 1 Posición Blanco", "description": "Placa de pared de 1 posición Mini-Com con etiquetas para rotulación.", "price": 38.00, "stock": 60, "category": "Cableado estructurado", "brand": "Panduit", "color": "Blanco", "weight": "0.04 kg"},
        
        # Bobinas de cable
        {"product_name": "Bobina de Cable UTP Cat6 Panduit Azul 305m", "description": "Bobina de cable de red Cat6 100% cobre con recubrimiento retardante a la flama (CM).", "price": 4350.00, "stock": 15, "category": "Cableado estructurado", "brand": "Panduit", "color": "Azul", "weight": "12.5 kg"},
        {"product_name": "Bobina de Cable UTP Cat6 Panduit Gris 305m", "description": "Bobina de cable de red Cat6 100% cobre, diseño especial para tendido vertical en edificios.", "price": 4350.00, "stock": 10, "category": "Cableado estructurado", "brand": "Panduit", "color": "Gris", "weight": "12.5 kg"},
        {"product_name": "Bobina de Cable UTP Cat6A Panduit Blanca 305m", "description": "Bobina de cable de red categoría 6A LSZH (bajo humo cero halógenos) para centros de datos.", "price": 6500.00, "stock": 8, "category": "Cableado estructurado", "brand": "Panduit", "color": "Blanco", "weight": "14.2 kg"},
        
        # Patch Panels modulares
        {"product_name": "Patch Panel Panduit 24 Puertos Modular", "description": "Panel de parcheo plano de 24 puertos modular para recibir jacks Mini-Com en 1UR de rack.", "price": 950.00, "stock": 18, "category": "Cableado estructurado", "brand": "Panduit", "color": "Negro", "weight": "0.8 kg"},
        {"product_name": "Patch Panel Panduit 48 Puertos Modular", "description": "Panel de parcheo plano modular de 48 puertos de 2UR para montaje en rack de 19 pulgadas.", "price": 1690.00, "stock": 12, "category": "Cableado estructurado", "brand": "Panduit", "color": "Negro", "weight": "1.3 kg"},
        
        # Organizadores horizontales
        {"product_name": "Organizador Panduit Frontal 1UR", "description": "Organizador de cables horizontal con anillas en D de metal para organización frontal limpia.", "price": 890.00, "stock": 20, "category": "Accesorios de Red", "brand": "Panduit", "color": "Negro", "weight": "0.95 kg"},
        {"product_name": "Organizador Panduit con Tapa 2UR", "description": "Organizador horizontal con tapa de bisagra frontal/trasera para alta densidad de cables.", "price": 1450.00, "stock": 15, "category": "Accesorios de Red", "brand": "Panduit", "color": "Negro", "weight": "1.4 kg"},
        
        # Patch Cords premium
        {"product_name": "Patch Cord Cat6 Panduit 1.0m Azul", "description": "Cable de red certificado categoría 6 de cobre multifilar, revestimiento CM, 1 metro.", "price": 115.00, "stock": 100, "category": "Accesorios de Red", "brand": "Panduit", "color": "Azul", "weight": "0.08 kg"},
        {"product_name": "Patch Cord Cat6 Panduit 2.0m Azul", "description": "Cable de parcheo certificado Cat6 con botas delgadas anti-enredos de fábrica, 2 metros.", "price": 145.00, "stock": 80, "category": "Accesorios de Red", "brand": "Panduit", "color": "Azul", "weight": "0.13 kg"},
        {"product_name": "Patch Cord Cat6 Panduit 3.0m Azul", "description": "Cable de parcheo certificado Cat6 de alto rendimiento para enlaces de datos, 3 metros.", "price": 180.00, "stock": 60, "category": "Accesorios de Red", "brand": "Panduit", "color": "Azul", "weight": "0.18 kg"},
        {"product_name": "Patch Cord Cat6 Panduit 5.0m Azul", "description": "Cable de parcheo premium certificado Cat6 para interconexiones distantes, 5 metros.", "price": 240.00, "stock": 40, "category": "Accesorios de Red", "brand": "Panduit", "color": "Azul", "weight": "0.26 kg"},
        {"product_name": "Plug Modular RJ45 Panduit Cat6 (Bolsa de 50)", "description": "Conectores modulares RJ45 de tres piezas con guía de alineación interna para cables sólidos.", "price": 850.00, "stock": 25, "category": "Accesorios de Red", "brand": "Panduit", "color": "Transparente", "weight": "0.15 kg"}
    ]
    products.extend(panduit_products)
    
    # 6. CONDUMEX (Cables de cobre para interior y fibra óptica)
    condumex_products = [
        # Bobinas UTP Cat6
        {"product_name": "Bobina de Cable UTP Cat6 Condumex Gris 305m", "description": "Bobina de cable de red Cat6 de cobre puro 23 AWG, ideal para aplicaciones de voz y datos.", "price": 3200.00, "stock": 20, "category": "Cableado estructurado", "brand": "Condumex", "color": "Gris", "weight": "11.5 kg"},
        {"product_name": "Bobina de Cable UTP Cat6 Condumex Azul 305m", "description": "Bobina de cable Cat6 100% cobre, certificación oficial de seguridad y flama mexicana.", "price": 3200.00, "stock": 18, "category": "Cableado estructurado", "brand": "Condumex", "color": "Azul", "weight": "11.5 kg"},
        {"product_name": "Bobina de Cable UTP Cat6 Condumex Rojo 305m", "description": "Bobina de cable de red Cat6 para cableado de seguridad o redes dedicadas contra incendios.", "price": 3300.00, "stock": 10, "category": "Cableado estructurado", "brand": "Condumex", "color": "Rojo", "weight": "11.5 kg"},
        
        # Bobinas UTP Cat5e
        {"product_name": "Bobina de Cable UTP Cat5e Condumex Gris 305m", "description": "Bobina de cable de red Cat5e de cobre puro 24 AWG, apto para tendidos en canalizaciones.", "price": 2100.00, "stock": 15, "category": "Cableado estructurado", "brand": "Condumex", "color": "Gris", "weight": "9.2 kg"},
        {"product_name": "Bobina de Cable UTP Cat5e Condumex Azul 305m", "description": "Bobina de cable de red Cat5e 100% cobre para redes domésticas o de pequeñas oficinas.", "price": 2100.00, "stock": 12, "category": "Cableado estructurado", "brand": "Condumex", "color": "Azul", "weight": "9.2 kg"},
        
        # Coaxial
        {"product_name": "Cable Coaxial RG6 Condumex 305m", "description": "Bobina de cable coaxial RG6 con blindaje del 75% para aplicaciones de CATV y señales de satélite.", "price": 2400.00, "stock": 14, "category": "Cableado estructurado", "brand": "Condumex", "color": "Negro", "weight": "12.8 kg"},
        {"product_name": "Cable Coaxial RG59 Condumex 305m", "description": "Bobina de cable coaxial RG59 con malla de cobre del 95% para circuitos de videovigilancia.", "price": 2150.00, "stock": 10, "category": "Cableado estructurado", "brand": "Condumex", "color": "Negro", "weight": "10.2 kg"},
        
        # Alarmas y Control
        {"product_name": "Cable de Alarma Condumex 2x22 305m", "description": "Bobina de cable de 2 conductores calibre 22 para instalación de sensores e intercomunicadores.", "price": 890.00, "stock": 30, "category": "Cables de control", "brand": "Condumex", "color": "Blanco", "weight": "4.5 kg"},
        {"product_name": "Cable de Alarma Condumex 4x22 305m", "description": "Bobina de cable de 4 conductores calibre 22 con forro de PVC blanco para automatización.", "price": 1450.00, "stock": 25, "category": "Cables de control", "brand": "Condumex", "color": "Blanco", "weight": "6.8 kg"},
        
        # Fibra óptica
        {"product_name": "Fibra Óptica ADSS Condumex 12 Hilos Monomodo", "description": "Cable de fibra óptica autosoportada ADSS de 12 hilos monomodo dieléctrica por metro.", "price": 22.00, "stock": 1500, "category": "Fibra óptica", "brand": "Condumex", "color": "Negro", "weight": "0.1 kg"},
        {"product_name": "Fibra Óptica ADSS Condumex 24 Hilos Monomodo", "description": "Cable de fibra óptica autosoportada ADSS de 24 hilos monomodo dieléctrica por metro.", "price": 32.00, "stock": 1000, "category": "Fibra óptica", "brand": "Condumex", "color": "Negro", "weight": "0.12 kg"},
        {"product_name": "Fibra Óptica Interior Condumex 2 Hilos OM3", "description": "Cable de fibra óptica interior de distribución de 2 hilos multimodo OM3 de bajas pérdidas.", "price": 18.00, "stock": 800, "category": "Fibra óptica", "brand": "Condumex", "color": "Aqua", "weight": "0.05 kg"}
    ]
    products.extend(condumex_products)
    
    # 7. CISCO (Switches empresariales SMB y gateways)
    cisco_products = [
        # Catalyst 1000 Series (Switches industriales administrados)
        {"product_name": "Switch Cisco Catalyst C1000-8T-2G-L", "description": "Switch Catalyst de 8 puertos Gigabit Ethernet de datos y 2 puertos Gigabit SFP de enlace.", "price": 8900.00, "stock": 8, "category": "Switches", "brand": "Cisco", "color": "Negro", "weight": "1.8 kg"},
        {"product_name": "Switch Cisco Catalyst C1000-8P-2G-L", "description": "Switch Catalyst de 8 puertos Gigabit PoE+ con presupuesto total de 67W y 2 puertos SFP.", "price": 11800.00, "stock": 6, "category": "Switches", "brand": "Cisco", "color": "Negro", "weight": "2.2 kg"},
        {"product_name": "Switch Cisco Catalyst C1000-16T-2G-L", "description": "Switch Catalyst de 16 puertos Gigabit Ethernet y 2 puertos SFP Gigabit sin ventiladores.", "price": 12900.00, "stock": 5, "category": "Switches", "brand": "Cisco", "color": "Negro", "weight": "2.5 kg"},
        {"product_name": "Switch Cisco Catalyst C1000-16P-2G-L", "description": "Switch Catalyst de 16 puertos Gigabit PoE+ (capacidad total 120W) y 2 puertos SFP.", "price": 16900.00, "stock": 4, "category": "Switches", "brand": "Cisco", "color": "Negro", "weight": "2.9 kg"},
        {"product_name": "Switch Cisco Catalyst C1000-24T-4G-L", "description": "Switch Catalyst de 24 puertos Gigabit Ethernet y 4 puertos SFP Gigabit de enlace ascendente.", "price": 15800.00, "stock": 8, "category": "Switches", "brand": "Cisco", "color": "Negro", "weight": "3.5 kg"},
        {"product_name": "Switch Cisco Catalyst C1000-24P-4G-L", "description": "Switch Catalyst de 24 puertos Gigabit PoE+ (presupuesto de 195W) y 4 puertos SFP.", "price": 22800.00, "stock": 5, "category": "Switches", "brand": "Cisco", "color": "Negro", "weight": "4.1 kg"},
        {"product_name": "Switch Cisco Catalyst C1000-48T-4G-L", "description": "Switch Catalyst de 48 puertos Gigabit de datos y 4 puertos SFP Gigabit para montaje en rack.", "price": 24900.00, "stock": 4, "category": "Switches", "brand": "Cisco", "color": "Negro", "weight": "4.8 kg"},
        {"product_name": "Switch Cisco Catalyst C1000-48P-4G-L", "description": "Switch Catalyst de 48 puertos Gigabit PoE+ (presupuesto de 370W) y 4 puertos SFP.", "price": 35900.00, "stock": 3, "category": "Switches", "brand": "Cisco", "color": "Negro", "weight": "5.6 kg"},
        
        # Cisco Business 250 (CBS250)
        {"product_name": "Switch Cisco Business CBS250-8T-8G", "description": "Switch administrable inteligente con 8 puertos Gigabit y 2 puertos combinados Gigabit SFP.", "price": 3890.00, "stock": 15, "category": "Switches", "brand": "Cisco", "color": "Blanco", "weight": "1.2 kg"},
        {"product_name": "Switch Cisco Business CBS250-8P-8G", "description": "Switch administrable inteligente con 8 puertos Gigabit PoE+ (presupuesto de 67W) y 2 combinados SFP.", "price": 5490.00, "stock": 12, "category": "Switches", "brand": "Cisco", "color": "Blanco", "weight": "1.4 kg"},
        {"product_name": "Switch Cisco Business CBS250-24T-4G", "description": "Switch inteligente administrable de 24 puertos Gigabit y 4 puertos SFP para racks.", "price": 6800.00, "stock": 10, "category": "Switches", "brand": "Cisco", "color": "Blanco", "weight": "2.8 kg"},
        {"product_name": "Switch Cisco Business CBS250-24P-4G", "description": "Switch inteligente administrable de 24 puertos Gigabit PoE+ (presupuesto de 195W) y 4 SFP.", "price": 9900.00, "stock": 8, "category": "Switches", "brand": "Cisco", "color": "Blanco", "weight": "3.2 kg"},
        {"product_name": "Switch Cisco Business CBS250-48T-4G", "description": "Switch inteligente administrable de 48 puertos Gigabit y 4 puertos SFP.", "price": 12500.00, "stock": 6, "category": "Switches", "brand": "Cisco", "color": "Blanco", "weight": "4.1 kg"},
        {"product_name": "Switch Cisco Business CBS250-48P-4G", "description": "Switch inteligente administrable de 48 puertos Gigabit PoE+ (presupuesto de 370W) y 4 SFP.", "price": 18900.00, "stock": 4, "category": "Switches", "brand": "Cisco", "color": "Blanco", "weight": "5.1 kg"},
        
        # Cisco Business RV Routers
        {"product_name": "Router Cisco RV160-K9-NA", "description": "Router VPN cableado de 4 puertos Gigabit con cortafuegos integrado, ideal para pequeñas oficinas.", "price": 2890.00, "stock": 12, "category": "Redes cableadas", "brand": "Cisco", "color": "Negro", "weight": "0.85 kg"},
        {"product_name": "Router Cisco RV260-K9-NA", "description": "Router VPN de 8 puertos Gigabit de alto rendimiento con procesador de doble núcleo y cortafuegos.", "price": 4200.00, "stock": 10, "category": "Redes cableadas", "brand": "Cisco", "color": "Negro", "weight": "1.1 kg"},
        {"product_name": "Router Cisco RV340-K9-NA", "description": "Router VPN empresarial de doble puerto WAN Gigabit con seguridad avanzada y balanceo de carga.", "price": 6390.00, "stock": 6, "category": "Redes cableadas", "brand": "Cisco", "color": "Negro", "weight": "1.3 kg"},
        {"product_name": "Router Cisco RV345-K9-NA", "description": "Router VPN empresarial de doble WAN de alto rendimiento con switch de 16 puertos Gigabit.", "price": 8900.00, "stock": 4, "category": "Redes cableadas", "brand": "Cisco", "color": "Negro", "weight": "1.8 kg"},
        
        # Cisco Transceivers
        {"product_name": "Transceptor Cisco GLC-SX-MMD", "description": "Módulo SFP de fibra multimodo de 1000BASE-SX, longitud de onda de 850 nm, conector duplex LC.", "price": 1450.00, "stock": 40, "category": "Accesorios de Red", "brand": "Cisco", "color": "Plateado", "weight": "0.05 kg"},
        {"product_name": "Transceptor Cisco GLC-LH-SMD", "description": "Módulo SFP de fibra monomodo de 1000BASE-LX/LH, longitud de onda de 1310 nm, hasta 10 km.", "price": 2100.00, "stock": 30, "category": "Accesorios de Red", "brand": "Cisco", "color": "Plateado", "weight": "0.05 kg"},
        {"product_name": "Transceptor Cisco GLC-TE", "description": "Módulo SFP de cobre Gigabit Ethernet 1000BASE-T RJ45 con rango de temperatura extendido.", "price": 1150.00, "stock": 50, "category": "Accesorios de Red", "brand": "Cisco", "color": "Plateado", "weight": "0.06 kg"}
    ]
    products.extend(cisco_products)
    
    # 8. EPCOM / HIKVISION (Seguridad y Videovigilancia por CCTV)
    cctv_products = [
        # Bullet
        {"product_name": "Cámara Bullet Epcom EV1008T-TURBO", "description": "Cámara Bullet TurboHD 1080p, lente de 2.8 mm, visión nocturna Smart IR de hasta 20 metros.", "price": 310.00, "stock": 60, "category": "CCTV y Seguridad", "brand": "Epcom", "color": "Blanco", "weight": "0.35 kg"},
        {"product_name": "Cámara Bullet IP Hikvision DS-2CD1023G0-I", "description": "Cámara Bullet IP de 2 Megapíxeles, lente de 2.8 mm, soporte PoE integrado, protección IP67.", "price": 1250.00, "stock": 35, "category": "CCTV y Seguridad", "brand": "Hikvision", "color": "Blanco", "weight": "0.45 kg"},
        {"product_name": "Cámara Bullet IP Hikvision DS-2CD1043G0-I", "description": "Cámara Bullet IP de 4 Megapíxeles, compresión H.265+, visión nocturna IR de 30m y ranura MicroSD.", "price": 1890.00, "stock": 25, "category": "CCTV y Seguridad", "brand": "Hikvision", "color": "Blanco", "weight": "0.48 kg"},
        {"product_name": "Cámara Bullet Epcom B8-TURBO", "description": "Cámara de seguridad exterior TurboHD de 1080p, construcción metálica, visión IR nocturna.", "price": 450.00, "stock": 50, "category": "CCTV y Seguridad", "brand": "Epcom", "color": "Blanco", "weight": "0.52 kg"},
        
        # Domo
        {"product_name": "Cámara Domo IP Hikvision DS-2CD1123G0-I", "description": "Cámara Domo IP antivandálica de 2MP, protección IK10 contra golpes, soporte PoE integrado.", "price": 1390.00, "stock": 30, "category": "CCTV y Seguridad", "brand": "Hikvision", "color": "Blanco/Negro", "weight": "0.55 kg"},
        {"product_name": "Cámara Domo IP Hikvision DS-2CD1143G0-I", "description": "Cámara Domo IP antivandálica de 4MP, lente de 2.8 mm, compresión de video H.265, PoE.", "price": 1980.00, "stock": 20, "category": "CCTV y Seguridad", "brand": "Hikvision", "color": "Blanco/Negro", "weight": "0.58 kg"},
        {"product_name": "Cámara Domo Epcom E8-TURBO", "description": "Cámara domo de seguridad para interiores TurboHD de 1080p, forro plástico, IR inteligente.", "price": 280.00, "stock": 80, "category": "CCTV y Seguridad", "brand": "Epcom", "color": "Blanco", "weight": "0.28 kg"},
        
        # NVR y DVR
        {"product_name": "Grabador NVR Hikvision DS-7604NI-Q1/4P", "description": "Grabador de video en red (NVR) de 4 canales con 4 puertos PoE independientes, soporta hasta 8MP.", "price": 2490.00, "stock": 15, "category": "CCTV y Seguridad", "brand": "Hikvision", "color": "Negro", "weight": "1.5 kg"},
        {"product_name": "Grabador NVR Hikvision DS-7608NI-Q1/8P", "description": "Grabador NVR de 8 canales de video con 8 puertos PoE integrados para cámaras IP, resolución 4K.", "price": 3890.00, "stock": 10, "category": "CCTV y Seguridad", "brand": "Hikvision", "color": "Negro", "weight": "1.8 kg"},
        {"product_name": "Grabador NVR Hikvision DS-7616NI-Q2/16P", "description": "Grabador NVR de 16 canales con 16 puertos PoE independientes, soporte para 2 discos duros.", "price": 6800.00, "stock": 8, "category": "CCTV y Seguridad", "brand": "Hikvision", "color": "Negro", "weight": "2.8 kg"},
        {"product_name": "Grabador DVR Epcom EV4004TURBO", "description": "Grabador digital de video DVR de 4 canales de tecnología híbrida de 1080p, salida HDMI.", "price": 990.00, "stock": 20, "category": "CCTV y Seguridad", "brand": "Epcom", "color": "Negro", "weight": "1.1 kg"},
        {"product_name": "Grabador DVR Epcom EV4008TURBO", "description": "Grabador DVR híbrido de 8 canales TurboHD, soporta cámaras HD y cámaras IP, salida de video 1080p.", "price": 1450.00, "stock": 18, "category": "CCTV y Seguridad", "brand": "Epcom", "color": "Negro", "weight": "1.3 kg"},
        {"product_name": "Grabador DVR Epcom EV4016TURBO", "description": "Grabador DVR híbrido de 16 canales de 1080p Lite, compresión H.264+, puerto SATA.", "price": 2350.00, "stock": 12, "category": "CCTV y Seguridad", "brand": "Epcom", "color": "Negro", "weight": "1.9 kg"},
        
        # Discos Duros
        {"product_name": "Disco Duro Western Digital Purple 1TB", "description": "Disco duro de 3.5 pulgadas para videovigilancia las 24 horas, interfaz SATA III de 6 Gb/s.", "price": 1150.00, "stock": 30, "category": "Accesorios de CCTV", "brand": "Western Digital", "color": "Plateado", "weight": "0.45 kg"},
        {"product_name": "Disco Duro Western Digital Purple 2TB", "description": "Disco duro optimizado para DVR y NVR de videovigilancia, tecnología AllFrame.", "price": 1490.00, "stock": 25, "category": "Accesorios de CCTV", "brand": "Western Digital", "color": "Plateado", "weight": "0.45 kg"},
        {"product_name": "Disco Duro Western Digital Purple 4TB", "description": "Disco duro de gran capacidad para almacenamiento continuo de flujos de video HD.", "price": 2350.00, "stock": 15, "category": "Accesorios de CCTV", "brand": "Western Digital", "color": "Plateado", "weight": "0.6 kg"},
        {"product_name": "Disco Duro Western Digital Purple 6TB", "description": "Disco duro de alto almacenamiento para grabadoras de cámaras profesionales en empresas.", "price": 3890.00, "stock": 8, "category": "Accesorios de CCTV", "brand": "Western Digital", "color": "Plateado", "weight": "0.65 kg"},
        
        # Baluns y energía
        {"product_name": "Transceptores Pasivos Epcom TT101FTURBO", "description": "Par de transceptores pasivos TurboHD de vídeo por cable UTP, soporte hasta 4K.", "price": 95.00, "stock": 100, "category": "Accesorios de CCTV", "brand": "Epcom", "color": "Negro", "weight": "0.08 kg"},
        {"product_name": "Transceptores Pasivos con Energía Epcom TT101PFTURBO", "description": "Par de transceptores pasivos de vídeo y corriente para cámaras de seguridad de 12V.", "price": 180.00, "stock": 80, "category": "Accesorios de CCTV", "brand": "Epcom", "color": "Negro", "weight": "0.12 kg"},
        {"product_name": "Fuente de Poder Epcom PL-12DC-4-BK", "description": "Fuente de alimentación regulada de 12 VDC a 4 Amperes para cámaras de seguridad comunes.", "price": 280.00, "stock": 40, "category": "Accesorios de CCTV", "brand": "Epcom", "color": "Negro", "weight": "0.35 kg"},
        {"product_name": "Fuente de Poder Epcom PL-12DC-8-BK", "description": "Fuente de alimentación de 12 VDC a 8 Amperes con cable pulpo de 8 salidas de corriente.", "price": 420.00, "stock": 30, "category": "Accesorios de CCTV", "brand": "Epcom", "color": "Negro", "weight": "0.5 kg"},
        {"product_name": "Fuente de Poder Distribuidora Epcom PL-12DC-10-A", "description": "Fuente en gabinete metálico de 12 VDC a 10 Amperes con fusible reseteable y 9 salidas.", "price": 1150.00, "stock": 15, "category": "Accesorios de CCTV", "brand": "Epcom", "color": "Gris", "weight": "2.2 kg"}
    ]
    products.extend(cctv_products)
    
    # 9. TP-LINK (Omada, SoHo)
    tplink_products = [
        # AP Omada
        {"product_name": "Punto de Acceso TP-Link EAP225", "description": "Access Point inalámbrico de doble banda Gigabit AC1350 para montaje en techo, soporte Omada.", "price": 1250.00, "stock": 30, "category": "Redes inalámbricas", "brand": "TP-Link", "color": "Blanco", "weight": "0.5 kg"},
        {"product_name": "Punto de Acceso TP-Link EAP225-Outdoor", "description": "AP inalámbrico exterior Gigabit AC1200, resistente a la intemperie IP65 con tecnología mesh.", "price": 1490.00, "stock": 25, "category": "Redes inalámbricas", "brand": "TP-Link", "color": "Blanco", "weight": "0.6 kg"},
        {"product_name": "Punto de Acceso TP-Link EAP245", "description": "Access Point empresarial de doble banda Gigabit AC1750 MIMO 3x3 para techo.", "price": 1850.00, "stock": 18, "category": "Redes inalámbricas", "brand": "TP-Link", "color": "Blanco", "weight": "0.55 kg"},
        {"product_name": "Punto de Acceso TP-Link EAP610", "description": "Access Point Wi-Fi 6 de montaje en techo Gigabit AX1800 compatible con controladora Omada.", "price": 2100.00, "stock": 20, "category": "Redes inalámbricas", "brand": "TP-Link", "color": "Blanco", "weight": "0.52 kg"},
        {"product_name": "Punto de Acceso TP-Link EAP610-Outdoor", "description": "AP exterior Wi-Fi 6 Gigabit AX1800, resistente al clima, ideal para albercas o patios.", "price": 2890.00, "stock": 12, "category": "Redes inalámbricas", "brand": "TP-Link", "color": "Blanco", "weight": "0.75 kg"},
        {"product_name": "Punto de Acceso TP-Link EAP650", "description": "Access Point de perfil delgado Wi-Fi 6 Gigabit AX3000 de doble banda ultra veloz.", "price": 2690.00, "stock": 15, "category": "Redes inalámbricas", "brand": "TP-Link", "color": "Blanco", "weight": "0.45 kg"},
        {"product_name": "Punto de Acceso TP-Link EAP670", "description": "Access Point empresarial Wi-Fi 6 Gigabit de doble banda AX5400 con puerto Ethernet de 2.5G.", "price": 3890.00, "stock": 10, "category": "Redes inalámbricas", "brand": "TP-Link", "color": "Blanco", "weight": "0.6 kg"},
        
        # Switches Omada
        {"product_name": "Switch TP-Link TL-SG2008P", "description": "Switch inteligente JetStream de 8 puertos Gigabit con 4 puertos PoE+ integrados (62W).", "price": 1890.00, "stock": 25, "category": "Switches", "brand": "TP-Link", "color": "Negro", "weight": "0.8 kg"},
        {"product_name": "Switch TP-Link TL-SG2210P", "description": "Switch administrable de 8 puertos Gigabit PoE+ y 2 ranuras SFP para rack (62W de capacidad).", "price": 2490.00, "stock": 20, "category": "Switches", "brand": "TP-Link", "color": "Negro", "weight": "1.2 kg"},
        {"product_name": "Switch TP-Link TL-SG2428P", "description": "Switch inteligente de 24 puertos Gigabit PoE+ con 4 ranuras SFP (presupuesto total de 250W).", "price": 6390.00, "stock": 10, "category": "Switches", "brand": "TP-Link", "color": "Negro", "weight": "3.5 kg"},
        {"product_name": "Switch TP-Link TL-SG3428XMP", "description": "Switch L2+ administrado JetStream de 24 puertos Gigabit PoE+ y 4 ranuras SFP+ de 10G (384W).", "price": 9900.00, "stock": 6, "category": "Switches", "brand": "TP-Link", "color": "Negro", "weight": "4.2 kg"},
        
        # VPN Routers y Controladoras
        {"product_name": "Router VPN TP-Link ER605", "description": "Router Multi-WAN cableado Gigabit VPN, ideal para pequeñas oficinas, integrado en Omada.", "price": 1150.00, "stock": 35, "category": "Redes cableadas", "brand": "TP-Link", "color": "Negro", "weight": "0.45 kg"},
        {"product_name": "Router VPN TP-Link ER7206", "description": "Router de alto rendimiento Multi-WAN Gigabit VPN con puerto SFP integrado.", "price": 2890.00, "stock": 15, "category": "Redes cableadas", "brand": "TP-Link", "color": "Negro", "weight": "0.75 kg"},
        {"product_name": "Controladora de Red TP-Link OC200", "description": "Controladora de hardware Omada para la administración centralizada de la red inalámbrica.", "price": 1690.00, "stock": 20, "category": "Equipos de Red", "brand": "TP-Link", "color": "Negro", "weight": "0.35 kg"},
        {"product_name": "Controladora de Red TP-Link OC300", "description": "Controladora de red corporativa por hardware Omada para gestionar hasta 500 dispositivos.", "price": 3100.00, "stock": 10, "category": "Equipos de Red", "brand": "TP-Link", "color": "Negro", "weight": "0.85 kg"},
        
        # Switches no administrados
        {"product_name": "Switch TP-Link TL-SF1005D", "description": "Switch de escritorio básico de 5 puertos de velocidad 10/100 Mbps, carcasa plástica.", "price": 180.00, "stock": 80, "category": "Switches", "brand": "TP-Link", "color": "Blanco", "weight": "0.15 kg"},
        {"product_name": "Switch TP-Link TL-SF1008D", "description": "Switch de escritorio básico de 8 puertos de velocidad 10/100 Mbps, Plug and Play.", "price": 250.00, "stock": 70, "category": "Switches", "brand": "TP-Link", "color": "Blanco", "weight": "0.18 kg"},
        {"product_name": "Switch TP-Link TL-SG1005D", "description": "Switch de escritorio Gigabit Ethernet de 5 puertos, ahorro de energía automático.", "price": 290.00, "stock": 100, "category": "Switches", "brand": "TP-Link", "color": "Negro", "weight": "0.18 kg"},
        {"product_name": "Switch TP-Link TL-SG1008D", "description": "Switch de escritorio Gigabit Ethernet de 8 puertos, ideal para expandir la red del hogar.", "price": 420.00, "stock": 90, "category": "Switches", "brand": "TP-Link", "color": "Negro", "weight": "0.22 kg"},
        {"product_name": "Switch TP-Link TL-SG1008PE", "description": "Switch de escritorio Gigabit de 8 puertos con 8 puertos PoE+ (presupuesto de potencia de 124W).", "price": 2100.00, "stock": 25, "category": "Switches", "brand": "TP-Link", "color": "Negro", "weight": "1.3 kg"}
    ]
    products.extend(tplink_products)
    
    # 10. PRODUCTOS EXTRA PARA LLEGAR A LOS 300 EXACTOS (Grandstream, Ubiquiti y otros modelos adicionales reales)
    extra_products = [
        # Módulos de extensión de telefonía
        {"product_name": "Módulo de Extensión Grandstream GBX20", "description": "Módulo de extensión de pantalla LCD a color de 4.3 pulgadas para teléfonos GRP2615, GRP2624 y GXV3350.", "price": 2490.00, "stock": 15, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.6 kg"},
        {"product_name": "Módulo de Extensión Grandstream GXP2200EXT", "description": "Módulo de extensión con pantalla LCD para teléfonos GXP2140 y GXP2170, hasta 40 teclas.", "price": 2350.00, "stock": 12, "category": "Telefonía IP", "brand": "Grandstream", "color": "Negro", "weight": "0.58 kg"},
        
        # Porteros y voceo
        {"product_name": "Videoportero IP Grandstream GDS3710", "description": "Sistema de videoportero IP con cámara HD de 1080p, lector de tarjetas RFID y micrófono/altavoz.", "price": 5490.00, "stock": 8, "category": "Porteros y voceo", "brand": "Grandstream", "color": "Plateado", "weight": "1.1 kg"},
        {"product_name": "Portero de Audio IP Grandstream GDS3705", "description": "Sistema de control de acceso de audio IP con lector de tarjetas RFID y micrófono cancelador de ruido.", "price": 3100.00, "stock": 10, "category": "Porteros y voceo", "brand": "Grandstream", "color": "Plateado", "weight": "0.85 kg"},
        {"product_name": "Altavoz SIP de Voceo Grandstream GSC3505", "description": "Altavoz SIP de voceo unidireccional de 8W con conectores de red y Wi-Fi/Bluetooth integrados.", "price": 2100.00, "stock": 14, "category": "Porteros y voceo", "brand": "Grandstream", "color": "Blanco", "weight": "0.45 kg"},
        {"product_name": "Intercomunicador SIP de Voceo Grandstream GSC3510", "description": "Altavoz y micrófono SIP bidireccional de voceo, 8W de potencia y soporte Wi-Fi de doble banda.", "price": 2690.00, "stock": 12, "category": "Porteros y voceo", "brand": "Grandstream", "color": "Blanco", "weight": "0.5 kg"},
        
        # Diademas telefónicas reales
        {"product_name": "Diadema Telefónica Grandstream GUV3000", "description": "Diadema monoaural con conexión USB y micrófono con cancelación de ruido activa.", "price": 790.00, "stock": 40, "category": "Accesorios de Telefonía", "brand": "Grandstream", "color": "Negro", "weight": "0.15 kg"},
        {"product_name": "Diadema Telefónica Grandstream GUV3005", "description": "Diadema biaural (doble oído) con conexión USB, indicador LED de ocupado y sonido HD.", "price": 1150.00, "stock": 35, "category": "Accesorios de Telefonía", "brand": "Grandstream", "color": "Negro", "weight": "0.18 kg"},
        {"product_name": "Diadema Inalámbrica Grandstream GUV3050", "description": "Diadema inalámbrica profesional Bluetooth con base de carga, audio HD, hasta 12 horas de duración.", "price": 2650.00, "stock": 15, "category": "Accesorios de Telefonía", "brand": "Grandstream", "color": "Negro", "weight": "0.35 kg"},
        
        # Cámaras y herramientas Ubiquiti
        {"product_name": "Cámara IP Ubiquiti UniFi Protect G4 Bullet", "description": "Cámara IP exterior de 4MP, visión nocturna por infrarrojos y micrófono integrado (modelo UVC-G4-BULLET).", "price": 4200.00, "stock": 15, "category": "CCTV y Seguridad", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.46 kg"},
        {"product_name": "Cámara IP Ubiquiti UniFi Protect G3 Flex", "description": "Cámara IP compacta y versátil de 1080p para interiores o exteriores con soporte para múltiples montajes.", "price": 1890.00, "stock": 25, "category": "CCTV y Seguridad", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.25 kg"},
        {"product_name": "Cámara IP Ubiquiti UniFi Protect G4 Dome", "description": "Cámara IP domo antivandálica de 4MP con audio bidireccional y resistencia al clima (modelo UVC-G4-DOME).", "price": 4650.00, "stock": 12, "category": "CCTV y Seguridad", "brand": "Ubiquiti", "color": "Blanco", "weight": "0.38 kg"},
        {"product_name": "Controladora de Hardware Ubiquiti Cloud Key Gen2 Plus", "description": "Dispositivo para gestión local de redes UniFi y cámaras UniFi Protect con disco duro de 1TB.", "price": 4890.00, "stock": 10, "category": "Equipos de Red", "brand": "Ubiquiti", "color": "Plateado/Negro", "weight": "0.58 kg"},
        {"product_name": "Router y Gateway Ubiquiti UniFi Dream Machine Pro", "description": "Consola empresarial de 1UR todo-en-uno que incluye router, switch de 8 puertos y NVR UniFi Protect.", "price": 8900.00, "stock": 8, "category": "Redes cableadas", "brand": "Ubiquiti", "color": "Gris", "weight": "3.9 kg"},
        {"product_name": "Router y Gateway Ubiquiti UniFi Dream Router", "description": "Consola de red residencial todo-en-uno con Wi-Fi 6 integrado, 4 puertos Gigabit (2 PoE) y NVR.", "price": 4990.00, "stock": 12, "category": "Redes inalámbricas", "brand": "Ubiquiti", "color": "Blanco", "weight": "1.2 kg"}
    ]
    products.extend(extra_products)
    
    # Escribir a inventario_telecom.csv
    csv_file_path = os.path.join(os.path.dirname(__file__), 'inventario_telecom.csv')
    
    with open(csv_file_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Cabecera
        writer.writerow(['product_name', 'description', 'price', 'stock', 'category', 'brand', 'color', 'weight'])
        
        for p in products:
            writer.writerow([
                p['product_name'],
                p['description'],
                p['price'],
                p['stock'],
                p['category'],
                p['brand'],
                p['color'],
                p['weight']
            ])
            
    print(f"¡Exitoso! Se generó el archivo CSV con {len(products)} productos reales.")

if __name__ == "__main__":
    generate_csv()
