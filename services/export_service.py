from io import BytesIO
import pandas as pd


def export_to_excel(
    hasil
):

    output = BytesIO()

    # =====================================================
    # URUTAN KOLOM HASIL
    # =====================================================

    kolom_hasil = [

        "No",

        "Nama",

        "Produk",

        "Qty Fisik",

        "Qty WMS",

        "Selisih Qty",

        "Movement Fisik",

        "Movement WMS",

        "Booking Code",

        "Plan Type Fisik",

        "Plan Type WMS",

        "Plan Type Hasil",

        "Status",

        "Jenis Masalah",

        "Catatan"

    ]

    # =====================================================
    # CEK KOLOM
    # =====================================================

    kolom_tersedia = [

        kolom

        for kolom in kolom_hasil

        if kolom in hasil.columns

    ]

    hasil_export = hasil[

        kolom_tersedia

    ].copy()

    # =====================================================
    # EXPORT EXCEL
    # =====================================================

    with pd.ExcelWriter(

        output,

        engine="openpyxl"

    ) as writer:

        # =================================================
        # SHEET 1
        # HASIL BALANCING
        # =================================================

        hasil_export.to_excel(

            writer,

            index=False,

            sheet_name="Hasil Balancing"

        )

        # =================================================
        # SHEET 2
        # SUMMARY STATUS
        # =================================================

        summary_status = (

            hasil_export[

                "Status"

            ]

            .value_counts()

            .reset_index()

        )

        summary_status.columns = [

            "Status",

            "Jumlah"

        ]

        summary_status.to_excel(

            writer,

            index=False,

            sheet_name="Summary"

        )

        # =================================================
        # SHEET 3
        # SUMMARY JENIS MASALAH
        # =================================================

        if "Jenis Masalah" in hasil_export.columns:

            summary_masalah = (

                hasil_export[

                    "Jenis Masalah"

                ]

                .value_counts()

                .reset_index()

            )

            summary_masalah.columns = [

                "Jenis Masalah",

                "Jumlah"

            ]

            summary_masalah.to_excel(

                writer,

                index=False,

                sheet_name="Jenis Masalah"

            )

        # =================================================
        # SHEET 4
        # DATA SELISIH QTY
        # =================================================

        if "Status" in hasil_export.columns:

            selisih_qty = hasil_export[

                hasil_export["Status"]

                == "SELISIH QTY"

            ]

            selisih_qty.to_excel(

                writer,

                index=False,

                sheet_name="Selisih Qty"

            )

        # =================================================
        # SHEET 5
        # DATA SELISIH PRODUK
        # =================================================

        if "Status" in hasil_export.columns:

            selisih_produk = hasil_export[

                hasil_export["Status"]

                == "SELISIH PRODUK"

            ]

            selisih_produk.to_excel(

                writer,

                index=False,

                sheet_name="Selisih Produk"

            )

        # =================================================
        # SHEET 6
        # HANYA FISIK
        # =================================================

        if "Status" in hasil_export.columns:

            hanya_fisik = hasil_export[

                hasil_export["Status"]

                == "HANYA FISIK"

            ]

            hanya_fisik.to_excel(

                writer,

                index=False,

                sheet_name="Hanya Fisik"

            )

        # =================================================
        # SHEET 7
        # HANYA WMS
        # =================================================

        if "Status" in hasil_export.columns:

            hanya_wms = hasil_export[

                hasil_export["Status"]

                == "HANYA WMS"

            ]

            hanya_wms.to_excel(

                writer,

                index=False,

                sheet_name="Hanya WMS"

            )

    # =====================================================
    # KEMBALIKAN FILE
    # =====================================================

    return output.getvalue()