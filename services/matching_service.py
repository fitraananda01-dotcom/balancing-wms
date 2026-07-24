import pandas as pd


# =========================================================
# HELPER
# =========================================================

def clean_text(value):
    if pd.isna(value):
        return ""

    return str(value).strip()


def clean_qty(value):
    if pd.isna(value) or value == "":
        return 0.0

    try:
        return float(value)
    except:
        try:
            return float(
                str(value)
                .replace(",", "")
                .strip()
            )
        except:
            return 0.0


# =========================================================
# PREPARE DATA FISIK
# =========================================================

def prepare_fisik_normal(
    df,
    nama_col,
    produk_col,
    qty_col,
    movement_col,
    plan_type_col
):

    result = pd.DataFrame()

    result["Nama"] = (
        df[nama_col]
        .apply(clean_text)
    )

    result["Produk"] = (
        df[produk_col]
        .apply(clean_text)
    )

    result["Qty"] = (
        df[qty_col]
        .apply(clean_qty)
    )

    result["Movement"] = (
        df[movement_col]
        .apply(clean_text)
    )

    result["Plan Type"] = (
        df[plan_type_col]
        .apply(clean_text)
    )

    result = result[
        ~(
            (result["Nama"] == "")
            &
            (result["Produk"] == "")
            &
            (result["Qty"] == 0)
        )
    ].copy()

    result.reset_index(
        drop=True,
        inplace=True
    )

    return result


# =========================================================
# PREPARE DATA WMS
# =========================================================

def prepare_wms_data(
    df,
    nama_col,
    produk_col,
    qty_col,
    movement_col,
    booking_col,
    plan_type_col
):

    result = pd.DataFrame()

    result["Nama"] = (
        df[nama_col]
        .apply(clean_text)
    )

    result["Produk"] = (
        df[produk_col]
        .apply(clean_text)
    )

    result["Qty"] = (
        df[qty_col]
        .apply(clean_qty)
    )

    result["Movement"] = (
        df[movement_col]
        .apply(clean_text)
    )

    result["Booking Code"] = (
        df[booking_col]
        .apply(clean_text)
    )

    result["Plan Type"] = (
        df[plan_type_col]
        .apply(clean_text)
    )

    result = result[
        ~(
            (result["Nama"] == "")
            &
            (result["Produk"] == "")
            &
            (result["Qty"] == 0)
        )
    ].copy()

    result.reset_index(
        drop=True,
        inplace=True
    )

    return result


# =========================================================
# HASIL PLAN TYPE
# =========================================================

def get_plan_type_result(
    plan_fisik,
    plan_wms
):

    plan_fisik = clean_text(
        plan_fisik
    )

    plan_wms = clean_text(
        plan_wms
    )

    if (
        plan_fisik != ""
        and
        plan_wms != ""
        and
        plan_fisik == plan_wms
    ):
        return plan_fisik

    return "-"


# =========================================================
# BALANCING
# =========================================================

def balance_data(
    fisik,
    wms
):

    fisik = fisik.copy()

    wms = wms.copy()

    fisik.reset_index(
        drop=True,
        inplace=True
    )

    wms.reset_index(
        drop=True,
        inplace=True
    )

    fisik["_used"] = False

    wms["_used"] = False

    hasil = []


    # =====================================================
    # BUAT HASIL
    # =====================================================

    def add_result(
        nama,
        produk_fisik,
        qty_fisik,
        movement_fisik,
        plan_fisik,
        produk_wms,
        qty_wms,
        movement_wms,
        booking_code,
        plan_wms,
        status,
        jenis_masalah,
        catatan
    ):

        hasil.append({

            "Nama":
                nama,

            "Produk":
                produk_fisik,

            "Qty Fisik":
                qty_fisik,

            "Qty WMS":
                qty_wms,

            "Selisih Qty":
                qty_fisik - qty_wms,

            "Movement Fisik":
                movement_fisik,

            "Movement WMS":
                movement_wms,

            "Booking Code":
                booking_code,

            "Plan Type Fisik":
                plan_fisik,

            "Plan Type WMS":
                plan_wms,

            "Plan Type Hasil":
                get_plan_type_result(
                    plan_fisik,
                    plan_wms
                ),

            "Status":
                status,

            "Jenis Masalah":
                jenis_masalah,

            "Catatan":
                catatan
        })


    # =====================================================
    # 1. CARI MATCH EXACT
    #
    # NAMA + PRODUK + QTY
    #
    # Movement hanya prioritas
    # =====================================================

    for f_idx, f in fisik.iterrows():

        kandidat = wms[

            (wms["_used"] == False)

            &

            (wms["Nama"] == f["Nama"])

            &

            (wms["Produk"] == f["Produk"])

            &

            (wms["Qty"] == f["Qty"])

        ]


        if kandidat.empty:

            continue


        # =================================================
        # PRIORITAS 1
        # MOVEMENT SAMA
        # =================================================

        if f["Movement"] != "":

            kandidat_sama = kandidat[

                kandidat["Movement"]

                ==

                f["Movement"]

            ]

            if not kandidat_sama.empty:

                w_idx = kandidat_sama.index[0]

            else:

                w_idx = kandidat.index[0]

        else:

            # =================================================
            # MOVEMENT FISIK KOSONG
            # CARI BERDASARKAN NAMA + PRODUK + QTY
            # =================================================

            w_idx = kandidat.index[0]


        w = wms.loc[w_idx]


        # Tandai sudah digunakan

        fisik.at[
            f_idx,
            "_used"
        ] = True

        wms.at[
            w_idx,
            "_used"
        ] = True


        movement_fisik = f["Movement"]

        movement_wms = w["Movement"]


        # =================================================
        # TENTUKAN MOVEMENT
        # =================================================

        if (

            movement_fisik != ""

            and

            movement_wms != ""

            and

            movement_fisik
            !=
            movement_wms

        ):

            jenis_masalah = (
                "MOVEMENT BERBEDA"
            )

            catatan = (
                "Nama + Produk + Qty "
                "cocok 100%, tetapi "
                "Movement berbeda."
            )

        else:

            jenis_masalah = (
                "TIDAK ADA MASALAH"
            )

            catatan = (
                "Nama + Produk + Qty "
                "cocok 100%."
            )


        add_result(

            f["Nama"],

            f["Produk"],

            f["Qty"],

            movement_fisik,

            f["Plan Type"],

            w["Produk"],

            w["Qty"],

            movement_wms,

            w["Booking Code"],

            w["Plan Type"],

            "MATCH",

            jenis_masalah,

            catatan

        )


    # =====================================================
    # 2. DATA FISIK YANG BELUM MATCH
    # =====================================================

    fisik_sisa = fisik[

        fisik["_used"] == False

    ]


    for f_idx, f in fisik_sisa.iterrows():


        # =================================================
        # CARI NAMA + PRODUK
        # QTY BOLEH BERBEDA
        # =================================================

        kandidat_qty = wms[

            (wms["_used"] == False)

            &

            (wms["Nama"] == f["Nama"])

            &

            (wms["Produk"] == f["Produk"])

        ]


        if not kandidat_qty.empty:


            # Prioritas Movement sama

            if f["Movement"] != "":

                kandidat_movement = kandidat_qty[

                    kandidat_qty["Movement"]

                    ==

                    f["Movement"]

                ]

                if not kandidat_movement.empty:

                    w_idx = kandidat_movement.index[0]

                else:

                    w_idx = kandidat_qty.index[0]

            else:

                w_idx = kandidat_qty.index[0]


            w = wms.loc[w_idx]


            wms.at[

                w_idx,

                "_used"

            ] = True


            add_result(

                f["Nama"],

                f["Produk"],

                f["Qty"],

                f["Movement"],

                f["Plan Type"],

                w["Produk"],

                w["Qty"],

                w["Movement"],

                w["Booking Code"],

                w["Plan Type"],

                "SELISIH QTY",

                "SELISIH QTY",

                (
                    "Nama + Produk sama, "
                    "tetapi Qty berbeda."
                )

            )

            continue


        # =================================================
        # CARI NAMA SAMA
        # PRODUK BERBEDA
        # =================================================

        kandidat_produk = wms[

            (wms["_used"] == False)

            &

            (wms["Nama"] == f["Nama"])

        ]


        if not kandidat_produk.empty:


            if f["Movement"] != "":

                kandidat_movement = kandidat_produk[

                    kandidat_produk["Movement"]

                    ==

                    f["Movement"]

                ]

                if not kandidat_movement.empty:

                    w_idx = kandidat_movement.index[0]

                else:

                    w_idx = kandidat_produk.index[0]

            else:

                w_idx = kandidat_produk.index[0]


            w = wms.loc[w_idx]


            wms.at[

                w_idx,

                "_used"

            ] = True


            add_result(

                f["Nama"],

                f["Produk"],

                f["Qty"],

                f["Movement"],

                f["Plan Type"],

                w["Produk"],

                w["Qty"],

                w["Movement"],

                w["Booking Code"],

                w["Plan Type"],

                "SELISIH PRODUK",

                "SELISIH PRODUK",

                (
                    "Nama sama, tetapi "
                    "Produk berbeda."
                )

            )

            continue


        # =================================================
        # HANYA FISIK
        # =================================================

        add_result(

            f["Nama"],

            f["Produk"],

            f["Qty"],

            f["Movement"],

            f["Plan Type"],

            "-",

            0,

            "-",

            "-",

            "-",

            "HANYA FISIK",

            "BELUM NAIK WMS",

            (
                "Transaksi ada di Fisik "
                "tetapi tidak ditemukan "
                "di WMS."
            )

        )


    # =====================================================
    # 3. DATA WMS YANG BELUM MATCH
    # =====================================================

    wms_sisa = wms[

        wms["_used"] == False

    ]


    for _, w in wms_sisa.iterrows():

        add_result(

            w["Nama"],

            "-",

            0,

            "-",

            "-",

            w["Produk"],

            w["Qty"],

            w["Movement"],

            w["Booking Code"],

            w["Plan Type"],

            "HANYA WMS",

            "BELUM INPUT FISIK",

            (
                "Transaksi ada di WMS "
                "tetapi tidak ditemukan "
                "di Fisik."
            )

        )


    # =====================================================
    # DATAFRAME
    # =====================================================

    result = pd.DataFrame(
        hasil
    )


    result.insert(

        0,

        "No",

        range(

            1,

            len(result) + 1

        )

    )


    return result