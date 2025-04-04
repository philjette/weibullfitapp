import streamlit as st
from utils.curve_storage import get_saved_curves
import plotly.graph_objects as go
from utils.weibull_functions import generate_weibull_curve
import os

# Hide page from navigation if not logged in
if not st.session_state.get("user_id"):
    # Create empty file to indicate this page should be hidden
    os.environ["HIDE_PAGES"] = "true"
    st.stop()

st.set_page_config(
    page_title="Compare Curves | WeibullFitPro",
    page_icon="📈",
    layout="wide"
)

def display_curve_comparison():
    """Display comparison of selected curves."""
    st.title("Compare Curves")
    st.write("Select multiple curves to compare their distributions.")

    # Get saved curves for this user
    curves = get_saved_curves(st.session_state.user_id)
    
    if not curves:
        st.write("No curves available for comparison. Create some curves first!")
        return

    # Create multiselect for curve selection
    curve_names = [curve['name'] for curve in curves]
    selected_curves = st.multiselect(
        "Select curves to compare",
        options=curve_names,
        default=curve_names[0] if curve_names else None
    )

    if not selected_curves:
        st.write("Please select at least one curve to display.")
        return

    # Distribution type selector
    curve_type = st.radio(
        "Distribution Type",
        [
            "CDF (Cumulative Distribution Function)", 
            "PDF (Probability Density Function)",
            "Hazard Function (Failure Rate)"
        ],
        index=0,  # Default to CDF
        key="comparison_dist_type"
    )
    curve_type = "cdf" if "CDF" in curve_type else "pdf" if "PDF" in curve_type else "hazard"

    # Create comparison plot
    fig = go.Figure()

    # Plot selected curves
    for curve_name in selected_curves:
        curve_data = next(curve for curve in curves if curve['name'] == curve_name)
        x_curve, y_curve = generate_weibull_curve(
            curve_data['shape'],
            curve_data['scale'],
            curve_type=curve_type
        )
        fig.add_trace(go.Scatter(
            x=x_curve,
            y=y_curve,
            name=f"{curve_name} (k={curve_data['shape']:.2f}, λ={curve_data['scale']:.2f})",
            line=dict(width=2)
        ))

    y_axis_title = {
        'cdf': "Cumulative Probability",
        'pdf': "Probability Density",
        'hazard': "Hazard Rate (Failures per Unit Time)"
    }[curve_type]

    fig.update_layout(
        title=f"Weibull {curve_type.upper()} Distribution Comparison",
        xaxis_title="Time",
        yaxis_title=y_axis_title,
        showlegend=True,
        width=800,
        height=500,
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
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        )
    )

    st.plotly_chart(fig)

# Display the comparison interface
display_curve_comparison()

# Add footer
st.markdown("""
<div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; font-size: 0.8em;'>
    Created by <a href='https://www.linkedin.com/in/philjette/' target='_blank'>Philippe Jette</a>
</div>
""", unsafe_allow_html=True)