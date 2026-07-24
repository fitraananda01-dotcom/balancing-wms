import streamlit as st

from services.matching_service import (
    balance_data
)

from services.export_service import (
    export_to_excel
)


def show_result_section(

    fisik_clean,

    wms_clean

):

    st.header(
        "📊 3. Hasil Balancing"
    )

    # =====================================================
    # CEK DATA
    # =====================================================

    if fisik_clean is None or wms_clean is None:

        return

    if fisik_clean.empty:

        st.warning(
            "Data Fisik kosong."
        )

        return

    if wms_clean.empty:

        st.warning(
            "Data WMS kosong."
        )

        return

    # =====================================================
    # BALANCING
    # =====================================================

    try:

        hasil = balance_data(

            fisik_clean,

            wms_clean

        )

    except Exception as e:

        st.error(

            f"Gagal melakukan balancing: {e}"

        )

        st.exception(e)

        return

    # =====================================================
    # CEK HASIL
    # =====================================================

    if hasil is None or hasil.empty:

        st.warning(

            "Tidak ada hasil balancing."

        )

        return

    # =====================================================
    # KPI
    # =====================================================

    total = len(hasil)

    match = len(

        hasil[
            hasil["Status"] == "MATCH"
        ]

    )

    selisih_qty = len(

        hasil[
            hasil["Status"] == "SELISIH QTY"
        ]

    )

    selisih_produk = len(

        hasil[
            hasil["Status"] == "SELISIH PRODUK"
        ]

    )

    hanya_fisik = len(

        hasil[
            hasil["Status"] == "HANYA FISIK"
        ]

    )

    hanya_wms = len(

        hasil[
            hasil["Status"] == "HANYA WMS"
        ]

    )

    # =====================================================
    # KPI BARIS 1
    # =====================================================

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(

        "📊 Total",

        f"{total:,}"

    )

    c2.metric(

        "✅ Match",

        f"{match:,}"

    )

    c3.metric(

        "🔴 Selisih Qty",

        f"{selisih_qty:,}"

    )

    c4.metric(

        "🟣 Selisih Produk",

        f"{selisih_produk:,}"

    )

    c5.metric(

        "🟡 Hanya Fisik",

        f"{hanya_fisik:,}"

    )

    # =====================================================
    # KPI BARIS 2
    # =====================================================

    st.metric(

        "🟠 Hanya WMS",

        f"{hanya_wms:,}"

    )

    # =====================================================
    # FILTER
    # =====================================================

    st.divider()

    st.subheader(

        "🔎 Filter Hasil"

    )

    status_options = sorted(

        hasil["Status"]

        .dropna()

        .unique()

        .tolist()

    )

    status_filter = st.multiselect(

        "Status",

        status_options,

        default=status_options

    )

    hasil_filter = hasil[

        hasil["Status"].isin(

            status_filter

        )

    ]

    # =====================================================
    # SEARCH NAMA
    # =====================================================

    search_nama = st.text_input(

        "🔍 Cari Nama",

        placeholder="Masukkan nama..."

    )

    if search_nama:

        hasil_filter = hasil_filter[

            hasil_filter["Nama"]

            .astype(str)

            .str.contains(

                search_nama,

                case=False,

                na=False

            )

        ]

    # =====================================================
    # SEARCH PRODUK
    # =====================================================

    search_produk = st.text_input(

        "🔍 Cari Produk",

        placeholder="Masukkan nama produk..."

    )

    if search_produk:

        hasil_filter = hasil_filter[

            hasil_filter["Produk"]

            .astype(str)

            .str.contains(

                search_produk,

                case=False,

                na=False

            )

        ]

    # =====================================================
    # SEARCH MOVEMENT
    # =====================================================

    search_movement = st.text_input(

        "🔍 Cari Movement Code / DN",

        placeholder="Masukkan Movement Code / DN..."

    )

    if search_movement:

        hasil_filter = hasil_filter[

            (

                hasil_filter["Movement Fisik"]

                .astype(str)

                .str.contains(

                    search_movement,

                    case=False,

                    na=False

                )

            )

            |

            (

                hasil_filter["Movement WMS"]

                .astype(str)

                .str.contains(

                    search_movement,

                    case=False,

                    na=False

                )

            )

        ]

    # =====================================================
    # SEARCH BOOKING CODE
    # =====================================================

    search_booking = st.text_input(

        "🔍 Cari Booking Code",

        placeholder="Masukkan Booking Code..."

    )

    if search_booking:

        hasil_filter = hasil_filter[

            hasil_filter["Booking Code"]

            .astype(str)

            .str.contains(

                search_booking,

                case=False,

                na=False

            )

        ]

    # =====================================================
    # SEARCH PLAN TYPE
    # =====================================================

    search_plan = st.text_input(

        "🔍 Cari Plan Type",

        placeholder="Masukkan Plan Type..."

    )

    if search_plan:

        hasil_filter = hasil_filter[

            (

                hasil_filter["Plan Type Fisik"]

                .astype(str)

                .str.contains(

                    search_plan,

                    case=False,

                    na=False

                )

            )

            |

            (

                hasil_filter["Plan Type WMS"]

                .astype(str)

                .str.contains(

                    search_plan,

                    case=False,

                    na=False

                )

            )

        ]

    # =====================================================
    # JUMLAH HASIL
    # =====================================================

    st.write(

        f"Menampilkan **{len(hasil_filter):,}** data."

    )

    # =====================================================
    # TABEL HASIL
    # =====================================================

    st.dataframe(

        hasil_filter,

        use_container_width=True,

        height=600

    )

    # =====================================================
    # RINGKASAN JENIS MASALAH
    # =====================================================

    st.divider()

    st.subheader(

        "📋 Ringkasan Jenis Masalah"

    )

    if "Jenis Masalah" in hasil.columns:

        ringkasan = (

            hasil[

                "Jenis Masalah"

            ]

            .value_counts()

            .reset_index()

        )

        ringkasan.columns = [

            "Jenis Masalah",

            "Jumlah"

        ]

        st.dataframe(

            ringkasan,

            use_container_width=True,

            hide_index=True

        )

    # =====================================================
    # EXPORT EXCEL
    # =====================================================

    st.divider()

    st.subheader(

        "📥 Export Hasil"

    )

    try:

        # Tidak lagi menggunakan
        # find_product_difference
        #
        # Karena hasil balance_data()
        # sudah menangani:
        #
        # MATCH
        # SELISIH QTY
        # SELISIH PRODUK
        # HANYA FISIK
        # HANYA WMS

        excel_output = export_to_excel(

            hasil

        )

        st.download_button(

            "⬇️ Download Hasil Balancing Excel",

            data=excel_output,

            file_name=(

                "hasil_balancing_wms.xlsx"

            ),

            mime=(

                "application/vnd.openxmlformats-officedocument"

                ".spreadsheetml.sheet"

            ),

            use_container_width=True

        )

    except Exception as e:

        st.error(

            f"Gagal membuat file Excel: {e}"

        )

        st.exception(e)