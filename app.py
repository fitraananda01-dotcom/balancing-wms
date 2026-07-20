import streamlit as st

from views.upload_view import (
    show_upload_section
)

from views.mapping_view import (
    show_mapping_section
)

from views.result_view import (
    show_result_section
)


# =========================================================
# KONFIGURASI
# =========================================================

st.set_page_config(

    page_title="Balancing Fisik vs WMS",

    page_icon="📦",

    layout="wide"

)


# =========================================================
# JUDUL
# =========================================================

st.title(

    "📦 Balancing Data Fisik vs WMS"

)

st.caption(

    "Sistem pencocokan transaksi Fisik dan WMS"

)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header(
        "⚙️ Balancing WMS"
    )

    st.info(

        """
        Kunci pencocokan:

        • Nama
        • Produk
        • Kode Movement
        • Tipe Transaksi

        Qty digunakan untuk
        menghitung selisih.

        Booking Kode diambil
        dari data WMS untuk
        kebutuhan tracking.
        """

    )


# =========================================================
# STEP 1
# =========================================================

fisik_data, wms_data, fisik_format = (

    show_upload_section()

)


# =========================================================
# STEP 2
# =========================================================

fisik_clean = st.session_state.get(

    "fisik_clean",

    None

)

wms_clean = st.session_state.get(

    "wms_clean",

    None

)


if (

    fisik_data is not None

    and

    wms_data is not None

):

    fisik_clean, wms_clean = (

        show_mapping_section(

            fisik_data,

            wms_data,

            fisik_format

        )

    )


# =========================================================
# STEP 3
# =========================================================

if (

    fisik_clean is not None

    and

    wms_clean is not None

):

    show_result_section(

        fisik_clean,

        wms_clean

    )