from typing import Optional

# シグネチャ（形式を示すバイト列）から形式を導く規則のリスト
# https://en.wikipedia.org/wiki/List_of_file_signatures
RULES = [
    ([0x38, 0x42, 0x50, 0x53], 'psd'),
    ([0xFF, 0xD8], 'jpeg'),
    ([0x89, 0x50, 0x4E, 0x47], 'png'),
    ([0x47, 0x49, 0x46, 0x38], 'gif'),
    ([0x25, 0x50, 0x44, 0x46], 'pdf'),
]

def test_image(byteIo: ByteIO) -> bool:
    # TODO: test_image
    return infer_image_format_from_bytes(byteIo) is not None

# ファイルのシグネチャから、画像として形式を推測します。
def infer_image_format_from_signature(byteIo: ByteIO) -> Optional[str]:
    # TODO: infer_image_format_from_bytes
    None
