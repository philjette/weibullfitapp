import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO
import plotly.graph_objects as go
from scipy.optimize import minimize
from scipy.special import gamma
from utils.weibull_functions import generate_weibull_curve
from utils.export import export_curve_data, get_csv_download, get_excel_download

def calculate_lifetimes(df):
    """Calculate lifetime for each asset."""
    df['in_service_date'] = pd.to_datetime(df['in_service_date'])
    df['retirement_date'] = pd.to_datetime(df['retirement_date'])
    df['lifetime'] = (df['retirement_date'] - df['in_service_date']).dt.total_seconds() / (365.25 * 24 * 60 * 60)  # Convert to years
    return df[df['lifetime'] > 0]  # Filter out negative or zero lifetimes

def weibull_loglik(params, lifetimes):
    """Calculate negative log-likelihood for Weibull distribution."""
    shape, scale = params
    if shape <= 0 or scale <= 0:
        return float('inf')

    try:
        # Add small constant to prevent log(0)
        eps = 1e-10
        lifetimes_safe = np.maximum(lifetimes, eps)

        n = len(lifetimes)
        log_likelihood = (n * np.log(shape) - 
                         n * shape * np.log(scale) + 
                         (shape - 1) * np.sum(np.log(lifetimes_safe)) - 
                         np.sum((lifetimes_safe / scale) ** shape))

        if not np.isfinite(log_likelihood):
            return float('inf')

        return -log_likelihood  # Return negative since we're minimizing
    except:
        return float('inf')

def fit_weibull_mle(lifetimes):
    """Fit Weibull parameters using Maximum Likelihood Estimation."""
    if len(lifetimes) < 2:
        raise ValueError("Need at least 2 data points for fitting")

    if np.any(lifetimes <= 0):
        raise ValueError("All lifetimes must be positive")

    # Better initial guess using percentiles
    p25, p50, p75 = np.percentile(lifetimes, [25, 50, 75])

    # Estimate initial shape parameter using IQR method
    shape_guess = np.log(np.log(4)) / np.log(p75/p25)
    shape_guess = max(0.5, min(5.0, shape_guess))  # Bound initial shape

    # Estimate scale parameter using median
    scale_guess = p50 / (np.log(2) ** (1/shape_guess))

    try:
        result = minimize(
            weibull_loglik,
            x0=[shape_guess, scale_guess],
            args=(lifetimes,),
            bounds=[(0.1, 50), (0.1, np.max(lifetimes) * 2)],
            method='Nelder-Mead',
            options={'maxiter': 1000}
        )

        if not result.success:
            raise ValueError(f"Optimization failed: {result.message}")

        shape, scale = result.x
        if not (np.isfinite(shape) and np.isfinite(scale)):
            raise ValueError("Optimization resulted in invalid parameters")

        return shape, scale

    except Exception as e:
        raise ValueError(f"Fitting error: {str(e)}")

def mle_fitting_interface():
    """Interface for MLE-based Weibull fitting from CSV data."""
    st.subheader("Maximum Likelihood Estimation from Asset Records")
    st.write("""
    Upload a CSV file containing asset lifetime data.

    Required columns:
    - asset_identifier: Unique identifier for each asset
    - in_service_date: Date when the asset was put into service (YYYY-MM-DD)
    - retirement_date: Date when the asset was retired (YYYY-MM-DD). If the asset is still in service, this field should be left blank.
    """)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            # Read and validate the CSV
            df = pd.read_csv(uploaded_file)
            required_columns = ['asset_identifier', 'in_service_date', 'retirement_date']

            if not all(col in df.columns for col in required_columns):
                st.error("CSV must contain columns: asset_identifier, in_service_date, and retirement_date")
                return

            # Calculate lifetimes
            df = calculate_lifetimes(df)

            if len(df) == 0:
                st.error("No valid lifetime data found after processing")
                return

            # Display data summary
            st.write("### Data Summary")
            st.write(f"Number of assets: {len(df)}")
            st.write(f"Average lifetime: {df['lifetime'].mean():.2f} years")
            st.write(f"Lifetime range: {df['lifetime'].min():.2f} to {df['lifetime'].max():.2f} years")

            # Fit Weibull distribution
            try:
                shape, scale = fit_weibull_mle(df['lifetime'].values)

                # Display parameters
                st.write("### Fitted Parameters")
                st.write(f"Shape (k): {shape:.3f}")
                st.write(f"Scale (λ): {scale:.3f}")

                # Plot
                fig = go.Figure()

                # Add histogram of actual data
                fig.add_trace(go.Histogram(
                    x=df['lifetime'],
                    name='Actual Data',
                    histnorm='probability density',
                    opacity=0.5,
                    nbinsx=30  # Adjust number of bins
                ))

                # Generate fitted curve
                x_curve, y_curve = generate_weibull_curve(shape, scale, curve_type='pdf')
                fig.add_trace(go.Scatter(
                    x=x_curve,
                    y=y_curve,
                    name='Fitted Weibull',
                    line=dict(color='red', width=2)
                ))

                fig.update_layout(
                    title="Fitted Weibull Distribution vs. Actual Data",
                    xaxis_title="Lifetime (years)",
                    yaxis_title="Probability Density",
                    width=800,
                    showlegend=True,
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
                
                # View different distribution types
                dist_type = st.radio(
                    "View Distribution Type",
                    ["PDF", "CDF", "Hazard Function"],
                    index=0,
                    key="mle_dist_view"
                )
                
                view_curve_type = dist_type.lower().replace(" function", "")
                
                # Show the selected curve type
                x_view, y_view = generate_weibull_curve(shape, scale, curve_type=view_curve_type)
                
                view_fig = go.Figure()
                view_fig.add_trace(go.Scatter(
                    x=x_view,
                    y=y_view,
                    name=f'Fitted {dist_type}'
                ))
                
                y_axis_title = {
                    'pdf': "Probability Density",
                    'cdf': "Cumulative Probability",
                    'hazard': "Hazard Rate (Failures per Unit Time)"
                }[view_curve_type]
                
                view_fig.update_layout(
                    title=f"Fitted Weibull {dist_type}",
                    xaxis_title="Lifetime (years)",
                    yaxis_title=y_axis_title,
                    width=800
                )
                
                st.plotly_chart(view_fig)
                
                # Export options
                export_type = st.radio(
                    "Export Data Type",
                    ["PDF Only", "CDF Only", "Hazard Function Only", "PDF and CDF", "All Functions"],
                    index=3,
                    key="mle_export_type"
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
                
                # Also export the raw data used for fitting
                if st.checkbox("Include raw data in export"):
                    original_data_df = pd.DataFrame({
                        'asset_identifier': df['asset_identifier'],
                        'in_service_date': df['in_service_date'],
                        'retirement_date': df['retirement_date'],
                        'lifetime_years': df['lifetime']
                    })
                    
                    # Create a dictionary for Excel writer to handle multiple sheets
                    excel_dfs = {
                        'Fitted_Curve': export_df,
                        'Raw_Data': original_data_df
                    }
                    
                    # Custom Excel export for multiple sheets
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    excel_filename = f"weibull_mle_fit_{timestamp}.xlsx"
                    
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        for sheet_name, sheet_df in excel_dfs.items():
                            sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
                        
                        # Add parameters sheet
                        params_df = pd.DataFrame({
                            'Parameter': ['Shape (k)', 'Scale (λ)'],
                            'Value': [shape, scale]
                        })
                        params_df.to_excel(writer, sheet_name='Parameters', index=False)
                    
                    excel_data = output.getvalue()
                    
                    # Single CSV with just the curve data
                    csv_data, csv_filename = get_csv_download(export_df, f"weibull_mle_fit")
                else:
                    # Standard export
                    csv_data, csv_filename = get_csv_download(export_df, f"weibull_curve_shape{shape:.2f}_scale{scale:.2f}")
                    excel_data, excel_filename = get_excel_download(export_df, f"weibull_curve_shape{shape:.2f}_scale{scale:.2f}")
                
                # Download buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=csv_filename,
                        mime="text/csv"
                    )
                
                with col2:
                    st.download_button(
                        label="Download Excel",
                        data=excel_data,
                        file_name=excel_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

            except ValueError as ve:
                st.error(f"Error fitting Weibull distribution: {str(ve)}")

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")