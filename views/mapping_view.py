import streamlit as st

from services.matching_service import (
    prepare_fisik_normal,
    prepare_wms_data
)


def show_mapping_section(
    fisik_data,
    wms_data
):

    st.header(
        "🔧 2. Mapping Data"
    )

    # =====================================================
    # CEK DATA
    # =====================================================

    if fisik_data is None:

        st.warning(
            "Data Fisik belum tersedia."
        )

        return None, None

    if wms_data is None:

        st.warning(
            "Data WMS belum tersedia."
        )

        return None, None

    # =====================================================
    # DATA FISIK
    # =====================================================

    st.subheader(
        "📦 Mapping Data Fisik"
    )

    st.info(
        "Data Fisik menggunakan format vertikal."
    )

    col1, col2 = st.columns(2)

    with col1:

        fisik_nama = st.selectbox(

            "Kolom Nama",

            fisik_data.columns,

            key="fisik_nama"

        )

        fisik_produk = st.selectbox(

            "Kolom Produk",

            fisik_data.columns,

            key="fisik_produk"

        )

        fisik_qty = st.selectbox(

            "Kolom Qty",

            fisik_data.columns,

            key="fisik_qty"

        )

    with col2:

        fisik_movement = st.selectbox(

            "Kolom Movement Code / DN",

            fisik_data.columns,

            key="fisik_movement"

        )

        fisik_plan_type = st.selectbox(

            "Kolom Plan Type",

            fisik_data.columns,

            key="fisik_plan_type"

        )

    st.caption(
        "Movement Code / DN pada Data Fisik boleh kosong."
    )

    # =====================================================
    # DATA WMS
    # =====================================================

    st.divider()

    st.subheader(
        "🖥️ Mapping Data WMS"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        wms_nama = st.selectbox(

            "Kolom Nama",

            wms_data.columns,

            key="wms_nama"

        )

        wms_produk = st.selectbox(

            "Kolom Produk",

            wms_data.columns,

            key="wms_produk"

        )

    with col2:

        wms_qty = st.selectbox(

            "Kolom Qty",

            wms_data.columns,

            key="wms_qty"

        )

        wms_movement = st.selectbox(

            "Kolom Movement Code / DN",

            wms_data.columns,

            key="wms_movement"

        )

    with col3:

        wms_booking = st.selectbox(

            "Kolom Booking Code",

            wms_data.columns,

            key="wms_booking"

        )

        wms_plan_type = st.selectbox(

            "Kolom Plan Type",

            wms_data.columns,

            key="wms_plan_type"

        )

    # =====================================================
    # INFORMASI LOGIKA
    # =====================================================

    st.divider()

    st.subheader(
        "📌 Logika Balancing"
    )

    st.info(
        """
        **MATCH ditentukan berdasarkan:**

        Nama + Produk + Qty harus sama 100%.

        **Movement Code / DN:**
        Digunakan untuk mengidentifikasi dan tracking transaksi.
        Movement bukan syarat wajib MATCH.

        **Plan Type:**
        Tidak menentukan MATCH.
        Jika Plan Type Fisik dan WMS sama, akan ditampilkan.
        Jika berbeda, hasil Plan Type akan menjadi "-".

        **Booking Code:**
        Diambil dari WMS dan ditampilkan pada hasil
        untuk memudahkan tracking transaksi.
        """
    )

    # =====================================================
    # PROSES
    # =====================================================

    st.divider()

    proses = st.button(

        "🚀 PROSES BALANCING",

        type="primary",

        use_container_width=True

    )

    if proses:

        try:

            # =============================================
            # PREPARE FISIK
            # =============================================

            fisik_clean = prepare_fisik_normal(

                fisik_data,

                fisik_nama,

                fisik_produk,

                fisik_qty,

                fisik_movement,

                fisik_plan_type

            )

            # =============================================
            # PREPARE WMS
            # =============================================

            wms_clean = prepare_wms_data(

                wms_data,

                wms_nama,

                wms_produk,

                wms_qty,

                wms_movement,

                wms_booking,

                wms_plan_type

            )

            # =============================================
            # SIMPAN SESSION
            # =============================================

            st.session_state[
                "fisik_clean"
            ] = fisik_clean

            st.session_state[
                "wms_clean"
            ] = wms_clean

            st.success(
                "Data berhasil diproses dan siap untuk balancing."
            )

        except Exception as e:

            st.error(
                f"Gagal memproses data: {e}"
            )

            st.exception(e)

    # =====================================================
    # AMBIL SESSION STATE
    # =====================================================

    fisik_result = st.session_state.get(

        "fisik_clean",

        None

    )

    wms_result = st.session_state.get(

        "wms_clean",

        None

    )

    # =====================================================
    # PREVIEW DATA FISIK
    # =====================================================

    if fisik_result is not None:

        with st.expander(

            "👁️ Preview Data Fisik"

        ):

            st.dataframe(

                fisik_result.head(100),

                use_container_width=True

            )

    # =====================================================
    # PREVIEW DATA WMS
    # =====================================================

    if wms_result is not None:

        with st.expander(

            "👁️ Preview Data WMS"

        ):

            st.dataframe(

                wms_result.head(100),

                use_container_width=True

            )

    return (

        fisik_result,

        wms_result

    )