import streamlit as st
import plotly.graph_objects as go
from utils.weibull_functions import generate_weibull_curve, validate_parameters
from utils.export import export_curve_data, get_csv_download, get_excel_download

def direct_params_interface():
    """Interface for direct parameter input."""
    st.subheader("Direct Parameter Input")
    st.write("Enter Weibull parameters directly to generate the curve.")

    col1, col2 = st.columns(2)

    with col1:
        shape = st.number_input(
            "Shape Parameter (k)",
            min_value=0.1,
            value=2.0,
            help="Controls the shape of the distribution. Higher values lead to narrower peaks."
        )

        scale = st.number_input(
            "Scale Parameter (λ)",
            min_value=0.1,
            value=1.0,
            help="Controls the scale of the distribution. Higher values stretch the distribution."
        )

    # Distribution type selector
    curve_type = st.radio(
        "Distribution Type",
        [
            "CDF (Cumulative Distribution Function)", 
            "PDF (Probability Density Function)",
            "Hazard Function (Failure Rate)"
        ],
        index=0,  # Default to CDF
        key="direct_params_dist_type"
    )
    curve_type = "cdf" if "CDF" in curve_type else "pdf" if "PDF" in curve_type else "hazard"

    valid, message = validate_parameters(shape, scale)

    if valid:
        x_curve, y_curve = generate_weibull_curve(shape, scale, curve_type=curve_type)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_curve, y=y_curve))

        y_axis_title = {
            'cdf': "Cumulative Probability",
            'pdf': "Probability Density",
            'hazard': "Hazard Rate (Failures per Unit Time)"
        }[curve_type]

        fig.update_layout(
            title=f"Weibull {curve_type.upper()} Distribution",
            xaxis_title="Time",
            yaxis_title=y_axis_title,
            showlegend=False,
            width=800,
            font=dict(
                size=14,
                family="Arial, sans-serif",
                color="black"
            ),
            xaxis=dict(
                title_font=dict(size=16, family="Arial, sans-serif"),
                tickfont=dict(size=14)
            ),
            yaxis=dict(
                title_font=dict(size=16, family="Arial, sans-serif"),
                tickfont=dict(size=14)
            )
        )

        st.plotly_chart(fig)

        # Export data section
        st.subheader("Export Curve Data")
        
        export_type = st.radio(
            "Export Data Type",
            ["PDF Only", "CDF Only", "Hazard Function Only", "PDF and CDF", "All Functions"],
            index=3,
            key="direct_params_export_type"
        )
        
        export_curve_type = {
            "PDF Only": "pdf",
            "CDF Only": "cdf",
            "Hazard Function Only": "hazard",
            "PDF and CDF": "both",
            "All Functions": "all"
        }[export_type]
        
        # Generate export data
        export_df = export_curve_data(shape, scale, curve_type=export_curve_type)
        
        col1, col2 = st.columns(2)
        with col1:
            # CSV download
            csv_data, csv_filename = get_csv_download(export_df, f"weibull_curve_shape{shape}_scale{scale}")
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=csv_filename,
                mime="text/csv"
            )
        
        with col2:
            # Excel download
            excel_data, excel_filename = get_excel_download(export_df, f"weibull_curve_shape{shape}_scale{scale}")
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name=excel_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.error(message)