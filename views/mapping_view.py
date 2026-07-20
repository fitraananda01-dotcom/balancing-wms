import streamlit as st

from services.matching_service import (
    prepare_fisik_normal,
    prepare_fisik_matrix,
    prepare_wms_data
)


def show_mapping_section(
    fisik_data,
    wms_data,
    fisik_format
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
        f"Format yang dipilih: **{fisik_format}**"
    )

    # =====================================================
    # FORMAT NORMAL
    # =====================================================

    if fisik_format == "Format Normal":

        col1, col2 = st.columns(2)

        with col1:

            fisik_nama = st.selectbox(
                "Kolom Nama",
                fisik_data.columns,
                key="normal_nama"
            )

            fisik_produk = st.selectbox(
                "Kolom Produk",
                fisik_data.columns,
                key="normal_produk"
            )

            fisik_qty = st.selectbox(
                "Kolom Qty",
                fisik_data.columns,
                key="normal_qty"
            )

        with col2:

            fisik_movement = st.selectbox(
                "Kolom Kode Movement",
                fisik_data.columns,
                key="normal_movement"
            )

            fisik_type = st.selectbox(
                "Kolom Tipe Transaksi",
                fisik_data.columns,
                key="normal_type"
            )

    # =====================================================
    # FORMAT MATRIKS
    # =====================================================

    else:

        st.info(
            """
            Format Matriks digunakan jika:

            • Nama orang berada ke bawah
            • Nama produk berada ke samping
            • DN / Movement Code berada di kolom
            • Qty berada di dalam tabel
            """
        )

        col1, col2 = st.columns(2)

        with col1:

            fisik_nama = st.selectbox(
                "Kolom Nama",
                fisik_data.columns,
                key="matrix_nama"
            )

        with col2:

            fisik_movement = st.selectbox(
                "Kolom Kode Movement / DN",
                fisik_data.columns,
                key="matrix_movement"
            )

        fisik_type = st.text_input(
            "Tipe Transaksi",
            value="OUTBOUND",
            key="matrix_type"
        )

        remove_zero = st.checkbox(
            "Abaikan Qty = 0",
            value=True,
            key="matrix_remove_zero"
        )

        st.caption(
            """
            Semua kolom selain:
            Nama,
            Movement / DN,
            dan Source Sheet

            akan dianggap sebagai Produk.
            """
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
            "Kolom Kode Movement",
            wms_data.columns,
            key="wms_movement"
        )

    with col3:

        wms_type = st.selectbox(
            "Kolom Tipe Transaksi",
            wms_data.columns,
            key="wms_type"
        )

        wms_booking = st.selectbox(
            "Kolom Booking Kode",
            wms_data.columns,
            key="wms_booking"
        )

    # =====================================================
    # PROSES
    # =====================================================

    st.divider()

    if st.button(
        "🚀 PROSES DATA",
        type="primary",
        use_container_width=True
    ):

        try:

            # =============================================
            # FISIK NORMAL
            # =============================================

            if fisik_format == "Format Normal":

                fisik_clean = (
                    prepare_fisik_normal(
                        fisik_data,
                        fisik_nama,
                        fisik_produk,
                        fisik_qty,
                        fisik_movement,
                        fisik_type
                    )
                )

            # =============================================
            # FISIK MATRIKS
            # =============================================

            else:

                fisik_clean = (
                    prepare_fisik_matrix(
                        fisik_data,
                        fisik_nama,
                        fisik_movement,
                        fisik_type,
                        remove_zero
                    )
                )

            # =============================================
            # WMS
            # =============================================

            wms_clean = (
                prepare_wms_data(
                    wms_data,
                    wms_nama,
                    wms_produk,
                    wms_qty,
                    wms_movement,
                    wms_type,
                    wms_booking
                )
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
                "✅ Data Fisik dan WMS berhasil diproses."
            )

        except Exception as e:

            st.error(
                f"❌ Gagal memproses data: {e}"
            )

    # =====================================================
    # AMBIL SESSION
    # =====================================================

    fisik_result = (
        st.session_state.get(
            "fisik_clean",
            None
        )
    )

    wms_result = (
        st.session_state.get(
            "wms_clean",
            None
        )
    )

    # =====================================================
    # PREVIEW FISIK
    # =====================================================

    if fisik_result is not None:

        with st.expander(
            "👁️ Preview Data Fisik Setelah Konversi"
        ):

            st.dataframe(
                fisik_result.head(100),
                use_container_width=True
            )

    # =====================================================
    # PREVIEW WMS
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