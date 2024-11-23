import os
import binascii
import sys

sys.stdout.reconfigure(encoding='utf-8')

def leer_archivo_gb(ruta_archivo):
    """Lee un archivo .gb y devuelve su contenido en bytes."""
    try:
        with open(ruta_archivo, "rb") as archivo:
            datos = archivo.read()
        return datos
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no se encontró.", file=sys.stderr)
        return None

def extraer_encabezado(datos):
    """Extrae el encabezado del archivo .gb."""
    return datos[0x0100:0x0150]

def obtener_nombre_juego(datos):
    """Obtiene el nombre del juego del encabezado."""
    nombre_bytes = datos[0x0134:0x0144]
    try:
        nombre = nombre_bytes.decode("ascii").strip("\0")
    except UnicodeDecodeError:
        nombre = "Nombre no legible"
    return nombre

def identificar_cartucho(datos):
    """Identifica el tipo de cartucho basado en los datos del encabezado."""
    tipos_cartucho = {
        0x00: "ROM Only",
        0x01: "MBC1",
        0x02: "MBC1 + RAM",
        0x03: "MBC1 + RAM + Battery",
        0x05: "MBC2",
        0x06: "MBC2 + Battery",
        0x08: "ROM + RAM",
        0x09: "ROM + RAM + Battery",
        0x0B: "MMM01",
        0x0C: "MMM01 + RAM",
        0x0D: "MMM01 + RAM + Battery",
        0x0F: "MBC3 + Timer + Battery",
        0x10: "MBC3 + Timer + RAM + Battery",
        0x11: "MBC3",
        0x12: "MBC3 + RAM",
        0x13: "MBC3 + RAM + Battery",
        0x19: "MBC5",
        0x1A: "MBC5 + RAM",
        0x1B: "MBC5 + RAM + Battery",
        0x1C: "MBC5 + Rumble",
        0x1D: "MBC5 + Rumble + RAM",
        0x1E: "MBC5 + Rumble + RAM + Battery",
        0x20: "MBC6",
        0x22: "MBC7 + Sensor + Rumble + RAM + Battery",
    }
    tipo = datos[0x0147]
    return tipos_cartucho.get(tipo, "Desconocido")

def obtener_tamanos_rom_ram(datos):
    """Obtiene el tamaño de la ROM y RAM basándose en el encabezado."""
    tamanos_rom = [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
    tamanos_ram = [0, 2, 8, 32, 128, 64]  # Tamaño en KB

    indice_rom = datos[0x0148]
    tamano_rom = tamanos_rom[indice_rom] if indice_rom < len(tamanos_rom) else "Desconocido"

    indice_ram = datos[0x0149]
    tamano_ram = tamanos_ram[indice_ram] if indice_ram < len(tamanos_ram) else "Desconocido"

    return tamano_rom, tamano_ram

def extraer_rom_completa(datos):
    """Extrae toda la ROM en formato hexadecimal."""
    return binascii.hexlify(datos).decode("utf-8")

def extraer_sonidos(datos):
    """Extrae una sección de la ROM que podría contener los sonidos."""
    # Este es un ejemplo, la sección de sonidos dependerá del juego
    # En muchos juegos de Game Boy, los sonidos se encuentran en una región específica de la ROM.
    # Usualmente, los sonidos están en direcciones altas de la ROM, como de 0xA000 a 0xBFFF
    # En este ejemplo, tomamos un segmento arbitrario como ejemplo de sonidos (puede variar).
    
    inicio_sonidos = 0xA000
    fin_sonidos = 0xBFFF
    sonidos = datos[inicio_sonidos:fin_sonidos]
    
    return sonidos

def guardar_hexadecimal(datos):
    """Guarda el contenido completo de la ROM en formato hexadecimal en dos archivos."""
    # Guardar en 'juego.txt' con el formato original
    with open('juego.txt', 'w') as f:
        print("---- Análisis completo del archivo .gb ----", file=f)
    
        # Encabezado
        encabezado = extraer_encabezado(datos)
        print("\nEncabezado (hex):", file=f)
        print(binascii.hexlify(encabezado).decode("utf-8"), file=f)
    
        # Nombre del juego
        nombre_juego = obtener_nombre_juego(datos)
        print(f"\nNombre del juego: {nombre_juego}", file=f)
    
        # Tipo de cartucho
        tipo_cartucho = identificar_cartucho(datos)
        print(f"Tipo de cartucho: {tipo_cartucho}", file=f)
    
        # Tamaño de ROM y RAM
        tamano_rom, tamano_ram = obtener_tamanos_rom_ram(datos)
        print(f"Tamaño de ROM: {tamano_rom} KB", file=f)
        print(f"Tamaño de RAM: {tamano_ram} KB", file=f)
    
        # ROM completa
        print("\nROM completa:", file=f)
        print(extraer_rom_completa(datos), file=f)
    
    # Guardar en 'juego_hex.txt' con el formato '0x0000 : ...'
    with open('juego_hex.txt', 'w') as hex_output:
        nombre_juego = obtener_nombre_juego(datos)
        hex_output.write(f"Nombre del juego: {nombre_juego}\n\n")
        
        # Escribir el archivo completo en formato '0x0000 : ...'
        for i in range(0, len(datos), 16):
            hex_line = " ".join(f"{byte:02X}" for byte in datos[i:i+16])
            hex_output.write(f"0x{i:04X} : {hex_line}\n")
    
    # Extraer sonidos y guardarlos
    sonidos = extraer_sonidos(datos)
    with open('sonidos.txt', 'w') as sonido_output:
        sonido_output.write("---- Sonidos del juego ----\n")
        sonido_output.write(binascii.hexlify(sonidos).decode("utf-8"))
    
    print("El contenido hexadecimal ha sido guardado en 'juego_hex.txt', 'juego.txt', y 'sonidos.txt'.")

def analizar_archivo_gb(ruta_archivo):
    """Analiza un archivo .gb y muestra su información completa."""
    datos = leer_archivo_gb(ruta_archivo)
    if datos is None:
        return
    
    # Guardar el contenido en los tres archivos de salida
    guardar_hexadecimal(datos)

# Ruta del archivo
ruta = "b.gb"  # Cambia esto por la ruta a tu archivo .gb
if os.path.isfile(ruta):
    analizar_archivo_gb(ruta)
else:
    print(f"El archivo '{ruta}' no existe.", file=sys.stderr)
