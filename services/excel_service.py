import pandas as pd


# =========================================================
# MEMBACA DAFTAR SHEET EXCEL
# =========================================================

def get_sheet_names(uploaded_file):

    if uploaded_file is None:
        return []

    try:

        # Pastikan posisi file kembali ke awal
        uploaded_file.seek(0)

        excel_file = pd.ExcelFile(
            uploaded_file
        )

        return excel_file.sheet_names

    except Exception as e:

        raise Exception(
            f"Gagal membaca daftar sheet: {e}"
        )


# =========================================================
# MEMBACA SHEET YANG DIPILIH
# =========================================================

def load_selected_sheets(
    uploaded_file,
    selected_sheets
):

    if uploaded_file is None:
        return pd.DataFrame()

    if not selected_sheets:
        return pd.DataFrame()

    dataframes = []

    try:

        for sheet in selected_sheets:

            uploaded_file.seek(0)

            df = pd.read_excel(
                uploaded_file,
                sheet_name=sheet
            )

            # Tambahkan informasi sheet
            df["Source Sheet"] = sheet

            dataframes.append(
                df
            )

        if not dataframes:
            return pd.DataFrame()

        return pd.concat(
            dataframes,
            ignore_index=True
        )

    except Exception as e:

        raise Exception(
            f"Gagal membaca sheet: {e}"
        )


# =========================================================
# MENGUBAH DATA MATRIKS MENJADI FORMAT NORMAL
# =========================================================

def convert_matrix_to_normal(
    df,
    nama_col,
    movement_col,
    remove_zero=True
):

    if df is None or df.empty:

        return pd.DataFrame()

    # -----------------------------------------
    # Validasi kolom
    # -----------------------------------------

    if nama_col not in df.columns:

        raise ValueError(
            f"Kolom Nama '{nama_col}' tidak ditemukan."
        )

    if movement_col not in df.columns:

        raise ValueError(
            f"Kolom Movement '{movement_col}' tidak ditemukan."
        )

    # -----------------------------------------
    # Cari kolom produk
    # -----------------------------------------

    excluded_columns = [
        nama_col,
        movement_col,
        "Source Sheet"
    ]

    product_columns = [
        col
        for col in df.columns
        if col not in excluded_columns
    ]

    if not product_columns:

        raise ValueError(
            "Tidak ditemukan kolom produk."
        )

    # -----------------------------------------
    # Ubah matriks menjadi normal
    # -----------------------------------------

    result = df.melt(

        id_vars=[
            nama_col,
            movement_col
        ],

        value_vars=product_columns,

        var_name="Produk",

        value_name="Qty"

    )

    # -----------------------------------------
    # Rename kolom
    # -----------------------------------------

    result = result.rename(

        columns={

            nama_col:
                "Nama",

            movement_col:
                "Kode Movement"

        }

    )

    # -----------------------------------------
    # Konversi Qty
    # -----------------------------------------

    result["Qty"] = pd.to_numeric(

        result["Qty"],

        errors="coerce"

    ).fillna(0)

    # -----------------------------------------
    # Bersihkan Nama
    # -----------------------------------------

    result["Nama"] = (

        result["Nama"]

        .astype(str)

        .str.strip()

    )

    # -----------------------------------------
    # Bersihkan Produk
    # -----------------------------------------

    result["Produk"] = (

        result["Produk"]

        .astype(str)

        .str.strip()

    )

    # -----------------------------------------
    # Bersihkan Movement
    # -----------------------------------------

    result["Kode Movement"] = (

        result["Kode Movement"]

        .astype(str)

        .str.strip()

    )

    # -----------------------------------------
    # Tambahkan Tipe Transaksi
    # -----------------------------------------

    result[
        "Tipe Transaksi"
    ] = "-"

    # -----------------------------------------
    # Hapus Qty 0
    # -----------------------------------------

    if remove_zero:

        result = result[
            result["Qty"] != 0
        ]

    # -----------------------------------------
    # Reset index
    # -----------------------------------------

    result = result.reset_index(
        drop=True
    )

    return result[
        [
            "Nama",
            "Produk",
            "Qty",
            "Kode Movement",
            "Tipe Transaksi"
        ]
    ]


# =========================================================
# NORMALISASI DATA NORMAL
# =========================================================

def normalize_normal_data(

    df,

    nama_col,

    produk_col,

    qty_col,

    movement_col,

    type_col

):

    if df is None or df.empty:

        return pd.DataFrame()

    result = pd.DataFrame()

    result["Nama"] = (

        df[nama_col]

        .astype(str)

        .str.strip()

    )

    result["Produk"] = (

        df[produk_col]

        .astype(str)

        .str.strip()

    )

    result["Qty"] = pd.to_numeric(

        df[qty_col],

        errors="coerce"

    ).fillna(0)

    result["Kode Movement"] = (

        df[movement_col]

        .astype(str)

        .str.strip()

    )

    result["Tipe Transaksi"] = (

        df[type_col]

        .astype(str)

        .str.strip()

    )

    return result


# =========================================================
# DETEKSI FORMAT DATA FISIK
# =========================================================

def prepare_fisik_data(

    df,

    fisik_format,

    nama_col=None,

    movement_col=None,

    produk_col=None,

    qty_col=None,

    type_col=None,

    remove_zero=True

):

    # -----------------------------------------
    # FORMAT NORMAL
    # -----------------------------------------

    if fisik_format == "Format Normal":

        if not all([

            nama_col,

            produk_col,

            qty_col,

            movement_col,

            type_col

        ]):

            raise ValueError(

                "Mapping kolom Format Normal "
                "belum lengkap."

            )

        return normalize_normal_data(

            df,

            nama_col,

            produk_col,

            qty_col,

            movement_col,

            type_col

        )

    # -----------------------------------------
    # FORMAT MATRIKS
    # -----------------------------------------

    elif fisik_format == "Format Matriks":

        if not nama_col:

            raise ValueError(

                "Kolom Nama belum dipilih."

            )

        if not movement_col:

            raise ValueError(

                "Kolom Kode Movement belum dipilih."

            )

        return convert_matrix_to_normal(

            df,

            nama_col,

            movement_col,

            remove_zero

        )

    else:

        raise ValueError(

            f"Format tidak dikenali: "
            f"{fisik_format}"

        )