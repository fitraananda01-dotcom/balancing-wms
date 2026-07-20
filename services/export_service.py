from io import BytesIO
import pandas as pd


def export_to_excel(

    hasil,

    produk_berbeda=None

):

    output = BytesIO()

    with pd.ExcelWriter(

        output,

        engine="openpyxl"

    ) as writer:

        hasil.to_excel(

            writer,

            index=False,

            sheet_name="Hasil Balancing"

        )

        summary = (

            hasil["Status"]

            .value_counts()

            .reset_index()

        )

        summary.columns = [

            "Status",

            "Jumlah"

        ]

        summary.to_excel(

            writer,

            index=False,

            sheet_name="Summary"

        )

        if produk_berbeda is not None:

            produk_berbeda.to_excel(

                writer,

                index=False,

                sheet_name="Produk Berbeda"

            )

    return output.getvalue()