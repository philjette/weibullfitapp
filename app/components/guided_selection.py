import streamlit as st
import plotly.graph_objects as go
from utils.weibull_functions import generate_weibull_curve
from utils.export import export_curve_data, get_csv_download, get_excel_download

def guided_selection_interface():
    """Interface for guided parameter selection."""
    st.subheader("Guided Parameter Selection")
    st.write("Answer these questions to determine appropriate Weibull parameters.")

    # Initialize shape parameter based on selection
    failure_pattern = st.radio(
        "What's the primary failure pattern?",
        [
            "Aging and wear-out dominant",
            "Early-life or random failure dominant",
            "Neither of the above"
        ],
        help="Select the pattern that best describes the failure behavior"
    )

    if failure_pattern == "Aging and wear-out dominant":
        predictable = st.radio(
            "Do failures occur predictably near end of life?",
            ["Yes", "No"]
        )
        initial_shape = 4.0 if predictable == "Yes" else 2.5

    elif failure_pattern == "Early-life or random failure dominant":
        defects = st.radio(
            "Are failures mostly due to manufacturing defects or bugs?",
            ["Yes", "No"]
        )
        initial_shape = 0.5 if defects == "Yes" else 1.0

    else:  # Neither of the above
        late_life = st.radio(
            "Does failure probability remain low until late life?",
            ["Yes", "No"]
        )
        initial_shape = 6.0 if late_life == "Yes" else 1.5

    # Average life input for initial scale parameter
    st.write("### Asset Life Expectancy")
    initial_scale = st.number_input(
        "What's the average expected life of this type of asset?",
        min_value=0.1,
        value=1.0,
        help="Enter the typical lifetime of the asset"
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
        key="guided_dist_type"
    )
    curve_type = "cdf" if "CDF" in curve_type else "pdf" if "PDF" in curve_type else "hazard"

    # Plot container
    plot_container = st.container()

    # Generate and plot curve with current parameters
    with plot_container:
        x_curve, y_curve = generate_weibull_curve(initial_shape, initial_scale, curve_type=curve_type)
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
        st.plotly_chart(fig, key="guided_selection_plot", use_container_width=False)

    # Fine-tuning sliders after the plot
    st.subheader("Fine-tune Parameters")

    shape = st.slider(
        "Adjust Shape Parameter (k)",
        min_value=0.1,
        max_value=10.0,
        value=float(initial_shape),
        help="Fine-tune the shape parameter"
    )

    scale = st.slider(
        "Adjust Scale Parameter (λ)",
        min_value=0.1,
        max_value=initial_scale * 2,
        value=float(initial_scale),
        help="Fine-tune the scale parameter"
    )

    # Display current parameters
    st.write(f"Current Parameters:")
    st.write(f"Shape (k): {shape:.3f}")
    st.write(f"Scale (λ): {scale:.3f}")

    # Export data section
    st.subheader("Export Curve Data")
    
    export_type = st.radio(
        "Export Data Type",
        ["PDF Only", "CDF Only", "Hazard Function Only", "PDF and CDF", "All Functions"],
        index=3,
        key="guided_export_type"
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
        csv_data, csv_filename = get_csv_download(export_df, f"weibull_curve_shape{shape:.2f}_scale{scale:.2f}")
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=csv_filename,
            mime="text/csv"
        )
    
    with col2:
        # Excel download
        excel_data, excel_filename = get_excel_download(export_df, f"weibull_curve_shape{shape:.2f}_scale{scale:.2f}")
        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name=excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )