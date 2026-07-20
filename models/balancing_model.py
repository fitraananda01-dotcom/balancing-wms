from dataclasses import dataclass
from typing import Optional


@dataclass
class BalancingResult:

    nama: str

    produk: str

    qty_fisik: float

    qty_wms: float

    selisih: float

    kode_movement: str

    tipe_transaksi: str

    booking_kode: str = "-"

    status: str = ""

    sheet_fisik: str = "-"

    sheet_wms: str = "-"


@dataclass
class UploadData:

    file_name: str

    selected_sheets: list

    data_format: Optional[str] = None