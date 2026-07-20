import pandas as pd


# =========================================================
# NORMALISASI TEKS
# =========================================================

def normalize_text(series):
    """
    Membersihkan teks agar lebih mudah dicocokkan.
    """

    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
    )


# =========================================================
# NORMALISASI QTY
# =========================================================

def normalize_qty(series):
    """
    Mengubah Qty menjadi angka.
    Nilai yang tidak valid dianggap 0.
    """

    return pd.to_numeric(
        series,
        errors="coerce"
    ).fillna(0)


# =========================================================
# PREPARE FISIK NORMAL
# =========================================================

def prepare_fisik_normal(
    df,
    nama_col,
    produk_col,
    qty_col,
    movement_col,
    type_col
):
    """
    Format Normal:

    Nama
    Produk
    Qty
    Movement
    Tipe Transaksi
    """

    result = pd.DataFrame()

    result["Nama"] = normalize_text(
        df[nama_col]
    )

    result["Produk"] = normalize_text(
        df[produk_col]
    )

    result["Qty"] = normalize_qty(
        df[qty_col]
    )

    result["Kode Movement"] = normalize_text(
        df[movement_col]
    )

    result["Tipe Transaksi"] = normalize_text(
        df[type_col]
    )

    if "Source Sheet" in df.columns:

        result["Source Sheet"] = (
            df["Source Sheet"]
            .fillna("-")
            .astype(str)
        )

    else:

        result["Source Sheet"] = "-"

    return result


# =========================================================
# PREPARE FISIK MATRIKS
# =========================================================

def prepare_fisik_matrix(
    df,
    nama_col,
    movement_col,
    type_value="OUTBOUND",
    remove_zero=True
):
    """
    Mengubah format matriks menjadi format transaksi.

    Contoh:

    Nama       DN       Produk A    Produk B    Produk C
    Budi       DN001    10          20          0

    Menjadi:

    Nama       Produk     Qty
    Budi       Produk A   10
    Budi       Produk B   20

    Movement dari kolom DN.
    """

    result_rows = []

    # Kolom yang bukan metadata dianggap sebagai produk
    excluded_columns = {
        nama_col,
        movement_col,
        "Source Sheet"
    }

    product_columns = [
        col
        for col in df.columns
        if col not in excluded_columns
    ]

    for _, row in df.iterrows():

        nama = str(
            row.get(nama_col, "")
        ).strip()

        movement = str(
            row.get(movement_col, "")
        ).strip()

        source_sheet = str(
            row.get("Source Sheet", "-")
        )

        for product_col in product_columns:

            qty = pd.to_numeric(
                row.get(product_col, 0),
                errors="coerce"
            )

            if pd.isna(qty):
                qty = 0

            if remove_zero and qty == 0:
                continue

            result_rows.append(
                {
                    "Nama": nama.upper(),
                    "Produk": str(
                        product_col
                    ).strip().upper(),
                    "Qty": qty,
                    "Kode Movement": movement.upper(),
                    "Tipe Transaksi": str(
                        type_value
                    ).strip().upper(),
                    "Source Sheet": source_sheet
                }
            )

    if not result_rows:

        return pd.DataFrame(
            columns=[
                "Nama",
                "Produk",
                "Qty",
                "Kode Movement",
                "Tipe Transaksi",
                "Source Sheet"
            ]
        )

    return pd.DataFrame(
        result_rows
    )


# =========================================================
# PREPARE DATA WMS
# =========================================================

def prepare_wms_data(
    df,
    nama_col,
    produk_col,
    qty_col,
    movement_col,
    type_col,
    booking_col
):
    """
    Menyiapkan data WMS.

    Booking Kode hanya ada di WMS.
    """

    result = pd.DataFrame()

    result["Nama"] = normalize_text(
        df[nama_col]
    )

    result["Produk"] = normalize_text(
        df[produk_col]
    )

    result["Qty"] = normalize_qty(
        df[qty_col]
    )

    result["Kode Movement"] = normalize_text(
        df[movement_col]
    )

    result["Tipe Transaksi"] = normalize_text(
        df[type_col]
    )

    result["Booking Kode"] = normalize_text(
        df[booking_col]
    )

    if "Source Sheet" in df.columns:

        result["Source Sheet"] = (
            df["Source Sheet"]
            .fillna("-")
            .astype(str)
        )

    else:

        result["Source Sheet"] = "-"

    return result


# =========================================================
# BALANCING UTAMA
# =========================================================

def balancing_data(
    fisik,
    wms
):
    """
    Logika utama balancing.

    ATURAN:

    1. Nama + Produk + Qty sama
       -> MATCH

    2. Movement fisik kosong
       tidak membuat transaksi gagal MATCH.

    3. Jika data WMS ditemukan
       dan movement WMS ada,
       Booking Kode ditampilkan.

    4. Produk sama tetapi Qty berbeda
       -> SELISIH QTY

    5. Nama sama tetapi Produk berbeda
       -> SELISIH PRODUK

    6. Hanya ada di Fisik
       -> HANYA FISIK
       -> BELUM NAIK WMS

    7. Hanya ada di WMS
       -> HANYA WMS
       -> BELUM INPUT FISIK
    """

    if fisik is None:
        fisik = pd.DataFrame()

    if wms is None:
        wms = pd.DataFrame()

    # =====================================================
    # AGREGASI DATA
    # =====================================================

    fisik_grouped = (
        fisik
        .groupby(
            [
                "Nama",
                "Produk"
            ],
            as_index=False
        )
        .agg(
            Qty_Fisik=(
                "Qty",
                "sum"
            ),
            Movement_Fisik=(
                "Kode Movement",
                lambda x: ", ".join(
                    sorted(
                        set(
                            str(v)
                            for v in x
                            if str(v).strip()
                        )
                    )
                )
            ),
            Sheet_Fisik=(
                "Source Sheet",
                lambda x: ", ".join(
                    sorted(
                        set(
                            str(v)
                            for v in x
                        )
                    )
                )
            )
        )
    )

    wms_grouped = (
        wms
        .groupby(
            [
                "Nama",
                "Produk"
            ],
            as_index=False
        )
        .agg(
            Qty_WMS=(
                "Qty",
                "sum"
            ),
            Movement_WMS=(
                "Kode Movement",
                lambda x: ", ".join(
                    sorted(
                        set(
                            str(v)
                            for v in x
                            if str(v).strip()
                        )
                    )
                )
            ),
            Booking_Kode=(
                "Booking Kode",
                lambda x: ", ".join(
                    sorted(
                        set(
                            str(v)
                            for v in x
                            if str(v).strip()
                        )
                    )
                )
            ),
            Sheet_WMS=(
                "Source Sheet",
                lambda x: ", ".join(
                    sorted(
                        set(
                            str(v)
                            for v in x
                        )
                    )
                )
            )
        )
    )

    # =====================================================
    # MERGE BERDASARKAN NAMA + PRODUK
    # =====================================================

    result = pd.merge(

        fisik_grouped,

        wms_grouped,

        on=[
            "Nama",
            "Produk"
        ],

        how="outer"

    )

    # =====================================================
    # ISI NILAI KOSONG
    # =====================================================

    result["Qty_Fisik"] = (
        result["Qty_Fisik"]
        .fillna(0)
    )

    result["Qty_WMS"] = (
        result["Qty_WMS"]
        .fillna(0)
    )

    for col in [
        "Movement_Fisik",
        "Movement_WMS",
        "Booking_Kode",
        "Sheet_Fisik",
        "Sheet_WMS"
    ]:

        result[col] = (
            result[col]
            .fillna("")
            .astype(str)
        )

    # =====================================================
    # SELISIH QTY
    # =====================================================

    result["Selisih_Qty"] = (
        result["Qty_Fisik"]
        -
        result["Qty_WMS"]
    )

    # =====================================================
    # STATUS DAN JENIS MASALAH
    # =====================================================

    statuses = []
    problems = []

    for _, row in result.iterrows():

        qty_fisik = row["Qty_Fisik"]

        qty_wms = row["Qty_WMS"]

        movement_wms = (
            row["Movement_WMS"]
            .strip()
        )

        # -----------------------------------------------
        # 1. FISIK ADA + WMS ADA
        # -----------------------------------------------

        if (
            qty_fisik != 0
            and
            qty_wms != 0
        ):

            if qty_fisik == qty_wms:

                status = "MATCH"

                # Movement fisik boleh kosong.
                # Jika WMS punya movement,
                # transaksi dianggap sudah naik WMS.

                if movement_wms:

                    problem = (
                        "TIDAK ADA MASALAH"
                    )

                else:

                    problem = (
                        "BELUM NAIK WMS"
                    )

            else:

                status = "SELISIH QTY"

                problem = (
                    "SELISIH QTY"
                )

        # -----------------------------------------------
        # 2. HANYA FISIK
        # -----------------------------------------------

        elif (
            qty_fisik != 0
            and
            qty_wms == 0
        ):

            status = "HANYA FISIK"

            problem = (
                "BELUM NAIK WMS"
            )

        # -----------------------------------------------
        # 3. HANYA WMS
        # -----------------------------------------------

        elif (
            qty_fisik == 0
            and
            qty_wms != 0
        ):

            status = "HANYA WMS"

            problem = (
                "BELUM INPUT FISIK"
            )

        else:

            status = "TIDAK DIKETAHUI"

            problem = "-"

        statuses.append(
            status
        )

        problems.append(
            problem
        )

    result["Status"] = statuses

    result["Jenis Masalah"] = problems

    # =====================================================
    # DETEKSI SELISIH PRODUK
    # =====================================================

    # Cari nama yang ada di Fisik dan WMS,
    # tetapi produknya berbeda.

    fisik_names = set(
        fisik["Nama"]
        .unique()
    )

    wms_names = set(
        wms["Nama"]
        .unique()
    )

    common_names = (
        fisik_names
        &
        wms_names
    )

    for idx, row in result.iterrows():

        nama = row["Nama"]

        status = row["Status"]

        if nama not in common_names:
            continue

        if status not in [
            "HANYA FISIK",
            "HANYA WMS"
        ]:
            continue

        fisik_products = set(
            fisik[
                fisik["Nama"]
                == nama
            ]["Produk"]
        )

        wms_products = set(
            wms[
                wms["Nama"]
                == nama
            ]["Produk"]
        )

        current_product = row[
            "Produk"
        ]

        # Produk fisik tidak ada di WMS
        if (
            status == "HANYA FISIK"
            and
            current_product
            not in wms_products
        ):

            result.at[
                idx,
                "Jenis Masalah"
            ] = "SELISIH PRODUK"

        # Produk WMS tidak ada di fisik
        elif (
            status == "HANYA WMS"
            and
            current_product
            not in fisik_products
        ):

            result.at[
                idx,
                "Jenis Masalah"
            ] = "SELISIH PRODUK"

    # =====================================================
    # URUTKAN KOLOM
    # =====================================================

    result = result[
        [
            "Nama",
            "Produk",
            "Qty_Fisik",
            "Qty_WMS",
            "Selisih_Qty",
            "Movement_Fisik",
            "Movement_WMS",
            "Booking_Kode",
            "Sheet_Fisik",
            "Sheet_WMS",
            "Status",
            "Jenis Masalah"
        ]
    ]

    # Rename supaya tampilan lebih rapi

    result = result.rename(
        columns={
            "Qty_Fisik":
                "Qty Fisik",

            "Qty_WMS":
                "Qty WMS",

            "Selisih_Qty":
                "Selisih",

            "Movement_Fisik":
                "Movement Fisik",

            "Movement_WMS":
                "Movement WMS",

            "Booking_Kode":
                "Booking Kode",

            "Sheet_Fisik":
                "Sheet Fisik",

            "Sheet_WMS":
                "Sheet WMS"
        }
    )

    return result


# =========================================================
# FUNGSI TAMBAHAN
# =========================================================

def find_product_difference(
    fisik,
    wms
):
    """
    Kompatibilitas dengan kode lama.
    """

    return balancing_data(
        fisik,
        wms
    )