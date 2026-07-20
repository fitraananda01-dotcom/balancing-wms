import streamlit as st

from services.matching_service import (
    balancing_data,
    find_product_difference
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

        hasil = balancing_data(

            fisik_clean,

            wms_clean

        )

        produk_berbeda = (

            find_product_difference(

                fisik_clean,

                wms_clean

            )

        )

    except Exception as e:

        st.error(

            f"Gagal melakukan balancing: {e}"

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

    selisih = len(

        hasil[
            hasil["Status"] == "SELISIH QTY"
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

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Total",
        f"{total:,}"
    )

    c2.metric(
        "✅ Match",
        f"{match:,}"
    )

    c3.metric(
        "🔴 Selisih",
        f"{selisih:,}"
    )

    c4.metric(
        "🟡 Hanya Fisik",
        f"{hanya_fisik:,}"
    )

    c5.metric(
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

    status_filter = st.multiselect(

        "Status",

        sorted(

            hasil["Status"]

            .unique()

            .tolist()

        ),

        default=sorted(

            hasil["Status"]

            .unique()

            .tolist()

        )

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

            .str.contains(

                search_nama,

                case=False,

                na=False

            )

        ]

    # =====================================================
    # SEARCH BOOKING
    # =====================================================

    search_booking = st.text_input(

        "🔍 Cari Booking Kode",

        placeholder="Masukkan Booking Kode..."

    )

    if search_booking:

        hasil_filter = hasil_filter[

            hasil_filter["Booking Kode"]

            .str.contains(

                search_booking,

                case=False,

                na=False

            )

        ]

    st.write(

        f"Menampilkan **{len(hasil_filter):,}** data."

    )

    st.dataframe(

        hasil_filter,

        use_container_width=True,

        height=600

    )

    # =====================================================
    # PRODUK BERBEDA
    # =====================================================

    st.divider()

    st.subheader(

        "⚠️ Tracking Produk Berbeda"

    )

    if produk_berbeda.empty:

        st.success(

            "Tidak ditemukan kemungkinan produk berbeda."

        )

    else:

        st.warning(

            f"Ditemukan "
            f"{len(produk_berbeda):,} "
            f"kemungkinan produk berbeda."

        )

        st.dataframe(

            produk_berbeda,

            use_container_width=True,

            height=400

        )

    # =====================================================
    # EXPORT
    # =====================================================

    st.divider()

    excel_output = export_to_excel(

        hasil,

        produk_berbeda

    )

    st.download_button(

        "⬇️ Download Hasil Balancing Excel",

        data=excel_output,

        file_name="hasil_balancing_wms.xlsx",

        mime=(

            "application/vnd.openxmlformats-officedocument"

            ".spreadsheetml.sheet"

        ),

        use_container_width=True

    )