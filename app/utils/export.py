import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO
from utils.weibull_functions import generate_weibull_curve

def export_curve_data(shape, scale, curve_type='both', num_points=1000):
    """Generate and export curve data points."""
    # Use the same function that generates plot points to ensure consistency
    if curve_type == 'pdf':
        x, pdf = generate_weibull_curve(shape, scale, num_points=num_points, curve_type='pdf')
        df = pd.DataFrame({
            'Time': x,
            'Probability_Density': pdf
        })
    elif curve_type == 'cdf':
        x, cdf = generate_weibull_curve(shape, scale, num_points=num_points, curve_type='cdf')
        df = pd.DataFrame({
            'Time': x,
            'Cumulative_Probability': cdf
        })
    elif curve_type == 'hazard':
        x, hazard = generate_weibull_curve(shape, scale, num_points=num_points, curve_type='hazard')
        df = pd.DataFrame({
            'Time': x,
            'Hazard_Rate': hazard
        })
    elif curve_type == 'all':
        x, pdf = generate_weibull_curve(shape, scale, num_points=num_points, curve_type='pdf')
        _, cdf = generate_weibull_curve(shape, scale, num_points=num_points, curve_type='cdf')
        _, hazard = generate_weibull_curve(shape, scale, num_points=num_points, curve_type='hazard')
        df = pd.DataFrame({
            'Time': x,
            'Probability_Density': pdf,
            'Cumulative_Probability': cdf,
            'Hazard_Rate': hazard
        })
    else:  # both pdf and cdf
        x, pdf = generate_weibull_curve(shape, scale, num_points=num_points, curve_type='pdf')
        _, cdf = generate_weibull_curve(shape, scale, num_points=num_points, curve_type='cdf')
        df = pd.DataFrame({
            'Time': x,
            'Probability_Density': pdf,
            'Cumulative_Probability': cdf
        })

    # Add parameters as metadata
    df.attrs['shape_parameter'] = shape
    df.attrs['scale_parameter'] = scale

    return df

def get_csv_download(df, filename_prefix):
    """Convert DataFrame to CSV bytes for download."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"
    return df.to_csv(index=False).encode('utf-8'), filename

def get_excel_download(df, filename_prefix):
    """Convert DataFrame to Excel bytes for download."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.xlsx"
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        # Add a parameters sheet to the Excel file
        params_df = pd.DataFrame({
            'Parameter': ['Shape (k)', 'Scale (λ)'],
            'Value': [df.attrs.get('shape_parameter', 'N/A'), df.attrs.get('scale_parameter', 'N/A')]
        })
        params_df.to_excel(writer, sheet_name='Parameters', index=False)
    return output.getvalue(), filename