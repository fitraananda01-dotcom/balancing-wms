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

    page_title="Balancing FISIK VS FLUX WMS",

    page_icon="",

    layout="wide"

)


# =========================================================
# JUDUL
# =========================================================

st.title(

    "Balancing FISIK VS FLUX WMS"

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
        System ini di bangun oleh Fitra Ananda

        Kunci pencocokan utama:

        • Nama
        • Produk
        • Qty

        Movement Code / DN digunakan
        untuk identifikasi dan tracking transaksi.

        Plan Type tidak digunakan
        sebagai penentu balancing.

        Booking Code diambil dari WMS
        untuk kebutuhan tracking.

        Semoga membantu
        """

    )


# =========================================================
# STEP 1
# UPLOAD DATA
# =========================================================

fisik_data, wms_data, fisik_format = (

    show_upload_section()

)


# =========================================================
# STEP 2
# MAPPING DATA
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

            wms_data

        )

    )


# =========================================================
# STEP 3
# HASIL BALANCING
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