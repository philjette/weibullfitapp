import streamlit as st
from utils.curve_storage import get_saved_curves, delete_curve
from utils.weibull_functions import generate_weibull_curve
from utils.export import export_curve_data, get_csv_download, get_excel_download
import plotly.graph_objects as go
import os

# Hide page from navigation if not logged in
if not st.session_state.get("user_id"):
    # Create empty file to indicate this page should be hidden
    os.environ["HIDE_PAGES"] = "true"
    st.stop()

st.set_page_config(
    page_title="Saved Curves | WeibullFitPro",
    page_icon="💾",
    layout="wide"
)

st.title("Your Saved Curves")
st.write("View, analyze, and export all your saved Weibull curves.")

# Get saved curves for this user
curves = get_saved_curves(st.session_state.user_id)

if not curves:
    st.write("No curves saved yet. Create a curve from any of the fitting methods to save it here.")
else:
    for curve in curves:
        with st.expander(f"{curve['name']} ({curve['timestamp']})"):
            st.write(f"Description: {curve['description']}")
            st.write(f"Method: {curve['method']}")
            st.write(f"Shape (k): {curve['shape']:.3f}")
            st.write(f"Scale (λ): {curve['scale']:.3f}")

            # Update the saved curves plotting section to include hazard function
            curve_type = st.radio(
                "View Distribution Type:", 
                [
                    "CDF (Cumulative Distribution Function)", 
                    "PDF (Probability Density Function)",
                    "Hazard Function (Failure Rate)"
                ],
                key=f"dist_type_{curve['name']}"
            )
            curve_type = "cdf" if "CDF" in curve_type else "pdf" if "PDF" in curve_type else "hazard"

            # Generate and show curve
            x_curve, y_curve = generate_weibull_curve(
                curve['shape'], 
                curve['scale'], 
                curve_type=curve_type
            )
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_curve, y=y_curve))

            y_axis_title = {
                'cdf': "Cumulative Probability",
                'pdf': "Probability Density",
                'hazard': "Hazard Rate (Failures per Unit Time)"
            }[curve_type]

            fig.update_layout(
                title=f"Saved Weibull {curve_type.upper()} Distribution",
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

            # Export options
            col1, col2, col3 = st.columns(3)

            # Generate data for export
            export_type = st.radio(
                "Export curve type:", 
                ["CDF only", "Both PDF and CDF"],
                key=f"export_type_{curve['name']}"
            )

            df = export_curve_data(
                curve['shape'], 
                curve['scale'], 
                curve_type='both' if export_type == "Both PDF and CDF" else 'cdf'
            )

            with col1:
                csv_data, csv_filename = get_csv_download(df, f"weibull_curve_{curve['name']}")
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=csv_filename,
                    mime="text/csv",
                    key=f"csv_{curve['name']}"
                )

            with col2:
                excel_data, excel_filename = get_excel_download(df, f"weibull_curve_{curve['name']}")
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name=excel_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"excel_{curve['name']}"
                )

            with col3:
                # Add delete button
                if st.button("Delete Curve", key=f"delete_{curve['name']}", type="secondary"):
                    success, message = delete_curve(curve['name'], st.session_state.user_id)
                    if success:
                        st.success(message)
                        st.rerun()  # Refresh the page to update the curve list
                    else:
                        st.error(message)

# Add footer
st.markdown("""
<div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; font-size: 0.8em;'>
    Created by <a href='https://www.linkedin.com/in/philjette/' target='_blank'>Philippe Jette</a>
</div>
""", unsafe_allow_html=True)