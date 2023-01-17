import wave
from os import PathLike
from pathlib import Path

from foundation import BinaryReader


def convert_voice(reader: BinaryReader, out_file_name: str | PathLike[str] | Path):
    # http://wiki.multimedia.cx/index.php?title=Creative_Voice
    try:
        magic_a = reader.read_bytes(19).decode('utf-8')
    except Exception:
        # turns out that _most_ of the VOC files are actually just raw PCM data...
        # print("Invalid VOC file (bad/no signature)({}).".format(filename), file=sys.stderr)
        # RAW PCM data at 22050 Hz, 8 bits, Mono
        reader.seek(0)
        dump_wave(out_file_name, 22050, 1, reader.read_all())
        return

    magic_b = reader.read_uint8()
    if (magic_a != "Creative Voice File") or (magic_b != 0x1A):
        # print("Invalid VOC file (bad signature)({}).".format(filename), file=sys.stderr)
        # RAW PCM data
        reader.seek(0)
        dump_wave(out_file_name, 22050, 1, reader.read_all())
        return

    reader.read_uint16()
    maj_min = reader.read_uint16()
    ver_chk = reader.read_uint16()
    if ver_chk != 0x1234 + ~maj_min:
        print("Invalid VOC File (bad version check)({}).".format(out_file_name))
        return

    while 1:
        block_type = reader.read_uint8()
        if block_type == 0 or block_type is None:
            break

        # check for our small implementation set (all valid Ascendancy VOCs use this configuration):
        # 8 bit unsigned, 22050 Hz, mono, Uncompressed -- OR
        # 8 bit unsigned, 11025 Hz, stereo, Uncompressed
        if block_type == 9:
            reader.seek(reader.position-1)
            size = reader.read_uint32() >> 8
            sample_rate = reader.read_uint32()
            sample_bits = reader.read_uint8()
            channel_count = reader.read_uint8()
            codec_id = reader.read_uint16()
            reader.read_uint32()
            if sample_bits != 8:
                raise Exception("Non-standard sample bits ({}).".format(sample_bits))
            if codec_id != 0:
                raise Exception("Non-standard codec id ({}).".format(codec_id))
            dump_wave(out_file_name, sample_rate, channel_count, reader.read_bytes(size))
        else:
            raise Exception("Unimplemented block type {:02X}".format(block_type))


def dump_wave(file_name: str | PathLike[str] or Path, rate: int, channels: int, data: any):
    with wave.open(file_name, 'wb') as wav:
        wav.setsampwidth(1)
        wav.setnchannels(channels)
        wav.setframerate(rate)
        wav.writeframes(data)
