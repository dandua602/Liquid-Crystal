/* Optional mGBA 0.10.5 headless research frontend. MPL-2.0 API dependency.
 * Use disposable ROM/save copies. RAM writes are explicitly limited to EWRAM
 * and IWRAM; the cartridge adapter changes only its private embedded-save window and
 * disposable save file. Game saving is driven by emulated buttons.
 * Commands: f frames decimal_keys; r hex_address decimal_length;
 * w hex_address hex_bytes; p ppm_path; s state_path; l state_path; q.
 */
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <mgba/internal/arm/arm.h>
#include <mgba/internal/gba/gba.h>
#include <fcntl.h>

/* This exact uploaded image contains a banked-SRAM conversion, despite its
 * retained FLASH1M signature. Model the external cartridge, not a ROM patch.
 * Persistence uses the private NOR save window 0x08C80000..0x08CA0000.
 * Bank port provenance: 0x1DE834 -> 0x08C72101, copied handler -> 0x09000000.
 * CPU byte accesses use two 64 KiB banks. The original 128 KiB file is loaded
 * into the adapter; only caller-supplied disposable save copies are written.
 */
static bool banked, dirty;
static unsigned bank, bank_writes, sram_writes, nor_programs, nor_erases;
static bool program_armed, erase_armed;
static struct mCore *mapper_core;
#define SAVE_ROM_ADDRESS 0x08C80000U
#define SAVE_ROM_SIZE 0x20000U
static uint8_t sram[0x20000];
static FILE *sram_file;
static struct ARMMemory original_memory;

static bool is_sram(uint32_t address) { return address >= 0x0E000000 && address < 0x10000000; }
static uint32_t read8(struct ARMCore *cpu, uint32_t address, int *cycles) {
    uint32_t value = original_memory.load8(cpu, address, cycles);
    return is_sram(address) ? sram[bank*0x10000+(address & 0xFFFF)] : value;
}
static uint32_t read16(struct ARMCore *cpu, uint32_t address, int *cycles) {
    uint32_t value = original_memory.load16(cpu, address, cycles);
    return is_sram(address) ? sram[bank*0x10000+(address & 0xFFFF)] * 0x0101U : value;
}
static uint32_t read32(struct ARMCore *cpu, uint32_t address, int *cycles) {
    uint32_t value = original_memory.load32(cpu, address, cycles);
    return is_sram(address) ? sram[bank*0x10000+(address & 0xFFFF)] * 0x01010101U : value;
}
static bool mapped_write(struct ARMCore *cpu, uint32_t address, uint8_t value, int *cycles) {
    if (address == 0x09000000) { bank = value & 1; ++bank_writes; return true; }
    if (!is_sram(address)) return false;
    sram[bank*0x10000+(address & 0xFFFF)] = value;
    ++sram_writes;
    if (cycles) *cycles += 1 + ((struct GBA*)cpu->master)->memory.waitstatesNonseq16[0xE];
    return true;
}
static void write8(struct ARMCore *cpu, uint32_t address, int8_t value, int *cycles) {
    if (!mapped_write(cpu,address,(uint8_t)value,cycles)) original_memory.store8(cpu,address,value,cycles);
}
/* Functional NOR protocol for the observed D0/D1-swapped AMD fallback.
 * The ROM boot copies this embedded 128 KiB save into banked SRAM; saving
 * programs it back. Only this cartridge save window is mutable in memory.
 * No cartridge ROM file is written. Timing/chip-ID emulation is not claimed.
 */
static bool nor_write(uint32_t address, uint16_t value) {
    if (address < 0x08000000 || address >= 0x0E000000) return false;
    uint32_t normalized=0x08000000 | (address & 0x01FFFFFF);
    bool target=normalized>=SAVE_ROM_ADDRESS && normalized<SAVE_ROM_ADDRESS+SAVE_ROM_SIZE;
    if (program_armed && target) {
        uint16_t old=mapper_core->busRead16(mapper_core,normalized);
        mapper_core->rawWrite16(mapper_core,normalized,-1,old & value);
        program_armed=false; dirty=true; ++nor_programs; return true;
    }
    if (erase_armed && target && value==0x30) {
        uint32_t base=normalized & ~0xFFFFU;
        for (unsigned n=0;n<0x10000;n+=2) mapper_core->rawWrite16(mapper_core,base+n,-1,0xFFFF);
        erase_armed=false; dirty=true; ++nor_erases; return true;
    }
    if (value==0xA0 && (normalized==0x08000AAA || normalized==0x08000555)) program_armed=true;
    else if (value==0x80 && (normalized==0x08000AAA || normalized==0x08000555)) erase_armed=true;
    else if (value==0xF0 || value==0xFF) { program_armed=false; erase_armed=false; }
    return true;
}
static void write16(struct ARMCore *cpu, uint32_t address, int16_t value, int *cycles) {
    if (nor_write(address,(uint16_t)value)) return;
    if (!mapped_write(cpu,address,(uint16_t)value >> (8*(address&1)),cycles)) original_memory.store16(cpu,address,value,cycles);
}
static void write32(struct ARMCore *cpu, uint32_t address, int32_t value, int *cycles) {
    if (!mapped_write(cpu,address,(uint32_t)value >> (8*(address&3)),cycles)) original_memory.store32(cpu,address,value,cycles);
}
static void install_mapper(struct mCore *core) {
    struct ARMCore *cpu = core->cpu;
    cpu->memory.load8=read8; cpu->memory.load16=read16; cpu->memory.load32=read32;
    cpu->memory.store8=write8; cpu->memory.store16=write16; cpu->memory.store32=write32;
}
static bool flush_cartridge_save(void) {
    if (!dirty) return true;
    if (fseek(sram_file,0,SEEK_SET) || fwrite((uint8_t*)((struct GBA*)mapper_core->board)->memory.rom+0xC80000,1,sizeof(sram),sram_file)!=sizeof(sram) || fflush(sram_file)) return false;
    dirty=false; return true;
}

static void quiet(struct mLogger *logger, int category, enum mLogLevel level,
                  const char *format, va_list args) {
    (void)logger; (void)category; (void)level; (void)format; (void)args;
}

int main(int argc, char **argv) {
    if (argc != 3) return 2;
    struct mLogger logger = {.log = quiet};
    mLogSetDefaultLogger(&logger);
    struct mCore *core = mCoreFind(argv[1]);
    if (!core || !core->init(core)) return 3;
    mCoreInitConfig(core, NULL);
    mCoreConfigSetDefaultValue(&core->config, "idleOptimization", "remove");
    mCoreLoadConfig(core);
    color_t *pixels = calloc(240 * 160, sizeof(color_t));
    core->setVideoBuffer(core, pixels, 240);
    struct VFile *rom = VFileOpen(argv[1], O_RDONLY);
    struct VFile *save = VFileOpen(argv[2], O_RDWR);
    if (!rom || !save || !core->loadROM(core, rom) || !core->loadSave(core, save)) return 4;
    core->reset(core);
    banked = !getenv("LC_PROBE_LEGACY_FLASH") &&
             core->busRead16(core,0x081DE828)==0x46C0 &&
             core->busRead32(core,0x081DE840)==0x08C72101 &&
             core->busRead32(core,0x08C7213C)==0x09000000;
    if (banked) {
        sram_file=fopen(argv[2],"r+b");
        if (!sram_file || fread(sram,1,sizeof(sram),sram_file)!=sizeof(sram)) return 9;
        mapper_core=core;
        if (getenv("LC_PROBE_ROM_SAVE_BOOT")) {
            /* Hardware-package check: blank SRAM, retain the actual ROM's NOR
             * bytes. Boot must recover the save through its own driver. */
            memset(sram, 0xFF, sizeof(sram));
        } else {
            /* rawWrite uses mGBA's private copy-on-write ROM, never the input file. */
            for (unsigned n=0;n<sizeof(sram);n+=2)
                core->rawWrite16(core,SAVE_ROM_ADDRESS+n,-1,sram[n] | (sram[n+1]<<8));
        }
        original_memory=((struct ARMCore*)core->cpu)->memory;
        install_mapper(core);
    }
    puts("{\"ready\":true}"); fflush(stdout);
    char line[16384], path[4096], bytes[8192];
    while (fgets(line, sizeof(line), stdin)) {
        unsigned frames, keys, address, length;
        if (sscanf(line, "f %u %u", &frames, &keys) == 2 && frames <= 36000) {
            core->setKeys(core, keys);
            for (unsigned n = 0; n < frames; ++n) core->runFrame(core);
            if (banked && !flush_cartridge_save()) return 10;
            printf("{\"frame\":%u}\n", core->frameCounter(core));
        } else if (sscanf(line, "r %x %u", &address, &length) == 2 && length <= 4096) {
            printf("{\"address\":%u,\"hex\":\"", address);
            for (unsigned n = 0; n < length; ++n) printf("%02x", banked && is_sram(address+n) ? sram[bank*0x10000+((address+n)&0xFFFF)] : core->busRead8(core, address + n));
            puts("\"}");
        } else if (sscanf(line, "w %x %8191s", &address, bytes) == 2) {
            length = strlen(bytes) / 2;
            bool ram = (address >= 0x02000000 && address + length <= 0x02040000) ||
                       (address >= 0x03000000 && address + length <= 0x03008000);
            if (!ram || strlen(bytes) % 2) return 5;
            for (unsigned n = 0; n < length; ++n) {
                unsigned byte;
                if (sscanf(bytes + 2*n, "%2x", &byte) != 1) return 5;
                core->busWrite8(core, address + n, byte);
            }
            puts("{\"ram_write\":true}");
        } else if (sscanf(line, "p %4095s", path) == 1) {
            FILE *file = fopen(path, "wb");
            if (!file) return 6;
            fprintf(file, "P6\n240 160\n255\n");
            for (unsigned n = 0; n < 240*160; ++n) {
                fputc(pixels[n] & 255, file);
                fputc((pixels[n] >> 8) & 255, file);
                fputc((pixels[n] >> 16) & 255, file);
            }
            fclose(file); puts("{\"screenshot\":true}");
        } else if ((line[0] == 's' || line[0] == 'l') && sscanf(line+1, "%4095s", path) == 1) {
            size_t size = core->stateSize(core);
            void *state = malloc(size);
            FILE *file = fopen(path, line[0] == 's' ? "wb" : "rb");
            bool ok = file != NULL;
            if (ok && line[0] == 's') ok = core->saveState(core, state) && fwrite(state, 1, size, file) == size;
            if (ok && line[0] == 'l') ok = fread(state, 1, size, file) == size && core->loadState(core, state);
            if (ok && banked && line[0] == 's') {
                uint8_t flags[3]={bank,program_armed,erase_armed};
                ok=fwrite(flags,1,3,file)==3 && fwrite(sram,1,sizeof(sram),file)==sizeof(sram)
                   && fwrite((uint8_t*)((struct GBA*)core->board)->memory.rom+0xC80000,1,sizeof(sram),file)==sizeof(sram);
            }
            if (ok && banked && line[0] == 'l') {
                uint8_t flags[3];
                ok=fread(flags,1,3,file)==3 && fread(sram,1,sizeof(sram),file)==sizeof(sram)
                   && fread((uint8_t*)((struct GBA*)core->board)->memory.rom+0xC80000,1,sizeof(sram),file)==sizeof(sram);
                if(ok) { bank=flags[0]&1; program_armed=flags[1]; erase_armed=flags[2]; dirty=true; install_mapper(core); }
            }
            if (file) fclose(file);
            free(state);
            if (!ok) return 7;
            puts("{\"state\":true}");
        } else if (line[0] == 'm') {
            printf("{\"banked_sram\":%s,\"embedded_nor_save\":%s,\"bank\":%u,\"bank_selects\":%u,\"sram_writes\":%u,\"nor_programs\":%u,\"nor_erases\":%u}\n",banked ? "true" : "false",banked ? "true" : "false",bank,bank_writes,sram_writes,nor_programs,nor_erases);
        } else if (line[0] == 'q') break;
        else return 8;
        fflush(stdout);
    }
    if (banked) { flush_cartridge_save(); fclose(sram_file); }
    core->deinit(core); free(pixels);
    return 0;
}
