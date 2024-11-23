class Memory:
    def __init__(self):
        # Inicializa la memoria total de 2 MB (0x200000)
        self.memory = [0] * 0x200000  # 2 MB de memoria total
        
        # Asignación de áreas específicas:
        self.rom_start = 0x0000  # 2 MB para la ROM
        self.rom_end = 0x1FFFFF  # Fin de la ROM (hasta 0x1FFFFF)
        
        self.vram_start = 0x8000  # VRAM: 8 KB
        self.vram_end = 0x9FFF
        
        self.wram_start = 0xC000  # WRAM: 32 KB
        self.wram_end = 0xDFFF
        
        self.sram_start = 0xA000  # SRAM: 128 KB
        self.sram_end = 0xBFFF

    def load_rom(self, rom_data):
        """Carga la ROM en la memoria. La ROM ocupa las direcciones 0x0000 a 0x1FFFFF (2 MB)."""
        if len(rom_data) > 0x200000:  # Si la ROM es mayor a 2 MB (0x200000 bytes)
            raise ValueError(f"Error: La ROM no puede ser más grande que 2 MB (0x200000). La ROM tiene {len(rom_data)} bytes.")
        
        # Cargar la ROM en la memoria (desde la dirección 0x0000 hasta el final de la ROM)
        self.memory[self.rom_start:self.rom_start + len(rom_data)] = rom_data
        print(f"ROM cargada en memoria: {len(rom_data)} bytes")  # Mostrar el tamaño real cargado

    def read_byte(self, address):
        """Lee un byte desde una dirección específica de la memoria."""
        if 0 <= address < 0x200000:
            return self.memory[address]
        else:
            raise ValueError(f"Dirección de memoria fuera de rango: {address:#04x}")

    def write_byte(self, address, value):
        """Escribe un byte en una dirección específica de la memoria."""
        # Dirección para VRAM (0x8000 - 0x9FFF)
        if self.vram_start <= address <= self.vram_end:
            print(f"Escribiendo en VRAM (dirección {address:#04x})")
        
        # Dirección para WRAM (0xC000 - 0xDFFF)
        elif self.wram_start <= address <= self.wram_end:
            print(f"Escribiendo en WRAM (dirección {address:#04x})")
        
        # Dirección para SRAM (0xA000 - 0xBFFF)
        elif self.sram_start <= address <= self.sram_end:
            print(f"Escribiendo en SRAM (dirección {address:#04x})")
        
        # Intento de escribir en la ROM (0x0000 - 0x1FFFFF) no permitido
        elif self.rom_start <= address <= self.rom_end:
            raise ValueError(f"Intento de escritura en la ROM (dirección {address:#04x}), operación no permitida.")
        
        # Dirección válida para RAM (0x0000 a 0x7FFF, aparte de la ROM)
        self.memory[address] = value

    def __repr__(self):
        """Representación de la memoria para facilitar el diagnóstico."""
        return (
            f"<Memory: {len(self.memory)} bytes, "
            f"ROM: {self.rom_start:#04x}-{self.rom_end:#04x} (2 MB), "
            f"VRAM: {self.vram_start:#04x}-{self.vram_end:#04x} (8 KB), "
            f"WRAM: {self.wram_start:#04x}-{self.wram_end:#04x} (32 KB), "
            f"SRAM: {self.sram_start:#04x}-{self.sram_end:#04x} (128 KB), "
            f"ROM cargada: {any(self.memory[self.rom_start:self.rom_end])}>"
        )