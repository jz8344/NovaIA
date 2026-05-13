from loguru import logger
from database.manager import DatabaseManager


async def seed_database(db: DatabaseManager):
    existing = await db.get_all_extensions()
    if existing:
        logger.info(f"Base de datos ya tiene {len(existing)} extensiones, omitiendo seed")
        return

    logger.info("Insertando datos iniciales de ejemplo...")

    extensions = [
        ("Luis Alfonso García", "104", "Ventas", "luis.garcia@techsolutions.com"),
        ("María Fernanda López", "105", "Soporte Técnico", "maria.lopez@techsolutions.com"),
        ("Carlos Rodríguez", "106", "Desarrollo", "carlos.rodriguez@techsolutions.com"),
        ("Ana Patricia Méndez", "107", "Recursos Humanos", "ana.mendez@techsolutions.com"),
        ("Roberto Sánchez", "108", "Dirección General", "roberto.sanchez@techsolutions.com"),
        ("Gabriela Torres", "109", "Contabilidad", "gabriela.torres@techsolutions.com"),
        ("Soporte Técnico", "200", "Soporte Técnico", "soporte@techsolutions.com"),
        ("Ventas", "201", "Ventas", "ventas@techsolutions.com"),
        ("Recepción", "100", "Administración", "recepcion@techsolutions.com"),
    ]

    for name, ext, dept, email in extensions:
        await db.add_extension(name, ext, dept, email)

    products = [
        ("Laptop ProBook 450", "Laptop empresarial 15.6 pulgadas, i7, 16GB RAM", 18500.00, 15, "Computadoras", "HP", "Plata", "1.7 kg"),
        ("Monitor UltraWide 34", "Monitor curvo 34 pulgadas WQHD", 8900.00, 8, "Monitores", "LG", "Negro", "6.2 kg"),
        ("Monitor Básico 24", "Monitor LED 24 pulgadas Full HD", 3500.00, 20, "Monitores", "Dell", "Negro", "3.5 kg"),
        ("Teléfono IP GXP2170", "Teléfono IP empresarial Grandstream 6 líneas", 3200.00, 25, "Telefonía", "Grandstream", "Negro", "0.9 kg"),
        ("Celular Empresarial A54", "Smartphone corporativo 128GB", 6500.00, 10, "Telefonía", "Samsung", "Gris", "0.2 kg"),
        ("Switch PoE 24 puertos", "Switch gestionable PoE+ 24 puertos Gigabit", 12500.00, 5, "Redes", "Cisco", "Metálico", "2.1 kg"),
        ("Licencia Office 365", "Licencia anual Microsoft 365 Business", 2800.00, 100, "Software", "Microsoft", "N/A", "0 kg"),
        ("Cable UTP Cat6 (305m)", "Bobina cable red categoría 6 certificado", 1850.00, 30, "Cableado", "Belden", "Azul", "12 kg"),
        ("Access Point WiFi 6", "Punto de acceso WiFi 6 para interiores", 4500.00, 12, "Redes", "Ubiquiti", "Blanco", "0.5 kg"),
        ("Teclado Inalámbrico", "Teclado ergonómico bluetooth silencioso", 1200.00, 45, "Periféricos", "Logitech", "Gris Oscuro", "0.8 kg"),
        ("Ratón Óptico Inalámbrico", "Mouse bluetooth de precisión", 800.00, 50, "Periféricos", "Logitech", "Negro", "0.1 kg"),
        ("Servidor Rack 1U", "Servidor de montaje en rack, Xeon 32GB RAM", 45000.00, 3, "Servidores", "Dell", "Metálico", "18 kg"),
    ]

    for name, desc, price, stock, cat, brand, color, weight in products:
        await db.add_inventory_item(name, desc, price, stock, cat, brand, color, weight)

    logger.info("Datos iniciales insertados correctamente")
