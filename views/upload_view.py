import streamlit as st

from services.excel_service import (
    get_sheet_names,
    load_selected_sheets
)


def show_upload_section():

    st.header(
        "📁 1. Upload Data"
    )

    col1, col2 = st.columns(2)

    # =========================================
    # INISIALISASI DATA
    # =========================================

    fisik_data = None
    wms_data = None

    # Default format
    fisik_format = "Format Normal"

    # =========================================
    # DATA FISIK
    # =========================================

    with col1:

        st.subheader(
            "📦 Data Fisik"
        )

        # -----------------------------------------
        # PILIH FORMAT DATA FISIK
        # -----------------------------------------

        fisik_format = st.radio(
            "Pilih format Data Fisik",
            [
                "Format Normal",
                "Format Matriks"
            ],
            horizontal=True,
            key="fisik_format"
        )

        # -----------------------------------------
        # UPLOAD FILE FISIK
        # -----------------------------------------

        fisik_file = st.file_uploader(

            "Upload Excel Data Fisik",

            type=[
                "xlsx",
                "xls",
                "xlsb"
            ],

            key="fisik_file"

        )

        # -----------------------------------------
        # PROSES FILE FISIK
        # -----------------------------------------

        if fisik_file:

            try:

                fisik_sheets = (
                    get_sheet_names(
                        fisik_file
                    )
                )

                selected_fisik_sheets = (
                    st.multiselect(

                        "Pilih 1 atau maksimal 2 sheet",

                        fisik_sheets,

                        max_selections=2,

                        default=fisik_sheets[:1],

                        key="selected_fisik_sheets"

                    )
                )

                if selected_fisik_sheets:

                    fisik_data = (
                        load_selected_sheets(

                            fisik_file,

                            selected_fisik_sheets

                        )
                    )

                    st.success(

                        f"Data Fisik: "
                        f"{len(fisik_data):,} baris"

                    )

                    with st.expander(

                        "👁️ Preview Data Fisik"

                    ):

                        st.dataframe(

                            fisik_data.head(10),

                            use_container_width=True

                        )

            except Exception as e:

                st.error(

                    f"Gagal membaca Data Fisik: {e}"

                )

    # =========================================
    # DATA WMS
    # =========================================

    with col2:

        st.subheader(
            "🖥️ Data WMS"
        )

        # -----------------------------------------
        # UPLOAD FILE WMS
        # -----------------------------------------

        wms_file = st.file_uploader(

            "Upload Excel Data WMS",

            type=[
                "xlsx",
                "xls",
                "xlsb"
            ],

            key="wms_file"

        )

        # -----------------------------------------
        # PROSES FILE WMS
        # -----------------------------------------

        if wms_file:

            try:

                wms_sheets = (
                    get_sheet_names(
                        wms_file
                    )
                )

                selected_wms_sheets = (
                    st.multiselect(

                        "Pilih Sheet WMS",

                        wms_sheets,

                        default=wms_sheets[:1],

                        key="selected_wms_sheets"

                    )
                )

                if selected_wms_sheets:

                    wms_data = (
                        load_selected_sheets(

                            wms_file,

                            selected_wms_sheets

                        )
                    )

                    st.success(

                        f"Data WMS: "
                        f"{len(wms_data):,} baris"

                    )

                    with st.expander(

                        "👁️ Preview Data WMS"

                    ):

                        st.dataframe(

                            wms_data.head(10),

                            use_container_width=True

                        )

            except Exception as e:

                st.error(

                    f"Gagal membaca Data WMS: {e}"

                )

    # =========================================
    # KEMBALIKAN DATA
    # =========================================

    return (
        fisik_data,
        wms_data,
        fisik_format
    )