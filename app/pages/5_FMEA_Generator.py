import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import json
import io
from datetime import datetime

from utils.openai_service import generate_fmea_with_gpt
from utils.weibull import generate_weibull_data
from utils.asset_data import (
    get_asset_types,
    get_operating_characteristics,
    get_default_failure_modes,
)

# Page configuration
st.set_page_config(
    page_title="FMEA Generator",
    page_icon="⚡",
    layout="wide",
)

# Title and description
st.title("FMEA Generator for Electrical T&D Assets")
st.markdown(
    """
    This tool helps generate Failure Mode and Effects Analysis (FMEA) for electrical 
    transmission and distribution assets. Specify your asset characteristics below
    and the system will generate an FMEA along with corresponding Weibull failure curves.
    """
)

# Initialize session state variables if they don't exist
if "fmea_results" not in st.session_state:
    st.session_state.fmea_results = None
if "weibull_data" not in st.session_state:
    st.session_state.weibull_data = None
if "raw_llm_response" not in st.session_state:
    st.session_state.raw_llm_response = None

# Main configuration area on the main page
if st.session_state.fmea_results is None:
    # Show the configuration form when no results exist
    st.header("Asset Configuration")
    
    # Use columns for better layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Asset type selection
        asset_types = get_asset_types()
        asset_type = st.selectbox(
            "Select Asset Type",
            options=asset_types,
            index=0,
        )
    
    # Get relevant operating characteristics based on asset type
    characteristics = get_operating_characteristics(asset_type)
    
    # Create two columns for characteristics
    col1, col2 = st.columns(2)
    
    st.subheader("Operating Characteristics")
    
    # Process characteristics and display in columns
    selected_characteristics = {}
    char_items = list(characteristics.items())
    half = len(char_items) // 2 + len(char_items) % 2  # Ceiling division for odd numbers
    
    # First half in left column
    with col1:
        for char_name, char_options in char_items[:half]:
            if isinstance(char_options, list):
                # Handle options list
                selected_characteristics[char_name] = st.selectbox(
                    f"{char_name}",
                    options=char_options,
                    key=f"char_{char_name}"
                )
            elif isinstance(char_options, tuple) and len(char_options) == 3:
                # Handle numeric ranges with (min, max, default)
                min_val, max_val, default = char_options
                selected_characteristics[char_name] = st.slider(
                    f"{char_name}",
                    min_value=min_val,
                    max_value=max_val,
                    value=default,
                    key=f"char_{char_name}"
                )
            elif isinstance(char_options, dict) and char_options.get("type") == "range":
                # Handle range with step size
                range_options = char_options
                selected_characteristics[char_name] = st.slider(
                    f"{char_name}",
                    min_value=range_options.get("min", 0),
                    max_value=range_options.get("max", 100),
                    value=range_options.get("default", range_options.get("min", 0)),
                    step=range_options.get("step", 1),
                    key=f"char_{char_name}"
                )
            elif isinstance(char_options, bool):
                # Handle boolean options
                selected_characteristics[char_name] = st.checkbox(
                    f"{char_name}",
                    value=char_options,
                    key=f"char_{char_name}"
                )
    
    # Second half in right column
    with col2:
        for char_name, char_options in char_items[half:]:
            if isinstance(char_options, list):
                # Handle options list
                selected_characteristics[char_name] = st.selectbox(
                    f"{char_name}",
                    options=char_options,
                    key=f"char_{char_name}"
                )
            elif isinstance(char_options, tuple) and len(char_options) == 3:
                # Handle numeric ranges with (min, max, default)
                min_val, max_val, default = char_options
                selected_characteristics[char_name] = st.slider(
                    f"{char_name}",
                    min_value=min_val,
                    max_value=max_val,
                    value=default,
                    key=f"char_{char_name}"
                )
            elif isinstance(char_options, dict) and char_options.get("type") == "range":
                # Handle range with step size
                range_options = char_options
                selected_characteristics[char_name] = st.slider(
                    f"{char_name}",
                    min_value=range_options.get("min", 0),
                    max_value=range_options.get("max", 100),
                    value=range_options.get("default", range_options.get("min", 0)),
                    step=range_options.get("step", 1),
                    key=f"char_{char_name}"
                )
            elif isinstance(char_options, bool):
                # Handle boolean options
                selected_characteristics[char_name] = st.checkbox(
                    f"{char_name}",
                    value=char_options,
                    key=f"char_{char_name}"
                )
    
    # Advanced options in expandable section
    with st.expander("Advanced Options"):
        adv_col1, adv_col2, adv_col3 = st.columns(3)
        
        with adv_col1:
            temperature_profile = st.selectbox(
                "Temperature Profile",
                options=["Normal", "Extreme Hot", "Extreme Cold", "Highly Variable"],
                index=0
            )
        
        with adv_col2:
            maintenance_regime = st.selectbox(
                "Maintenance Regime",
                options=["Minimal", "Standard", "Enhanced", "Predictive"],
                index=1
            )
        
        with adv_col3:
            environment = st.selectbox(
                "Environmental Conditions",
                options=["Urban", "Rural", "Coastal", "Industrial", "Desert"],
                index=0
            )
    
    # Generate button - centered
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Generate FMEA", type="primary", use_container_width=True):
            with st.spinner("Generating FMEA and Weibull curves..."):
                # Combine all characteristics for the prompt
                all_characteristics = {
                    **selected_characteristics,
                    "Temperature Profile": temperature_profile,
                    "Maintenance Regime": maintenance_regime,
                    "Environmental Conditions": environment
                }
                
                # Get response from OpenAI
                try:
                    fmea_data = generate_fmea_with_gpt(asset_type, all_characteristics)
                    st.session_state.raw_llm_response = fmea_data
                    
                    # Extract FMEA data
                    failure_modes = fmea_data.get("failure_modes", [])
                    
                    # If no failure modes returned, use defaults and show warning
                    if not failure_modes:
                        st.warning("No failure modes returned from LLM. Using default failure modes for this asset type.")
                        failure_modes = get_default_failure_modes(asset_type)
                    
                    # Generate Weibull data for each failure mode
                    weibull_data = {}
                    for mode in failure_modes:
                        mode_name = mode["failure_mode"]
                        beta = mode.get("weibull_beta", 1.5)  # Shape parameter
                        eta = mode.get("weibull_eta", 10000)  # Scale parameter (hours)
                        weibull_data[mode_name] = generate_weibull_data(beta, eta)
                    
                    # Store data in session state
                    st.session_state.fmea_results = failure_modes
                    st.session_state.weibull_data = weibull_data
                    
                    # Store input parameters for later use in export
                    st.session_state.asset_type = asset_type
                    st.session_state.selected_characteristics = selected_characteristics
                    st.session_state.temperature_profile = temperature_profile
                    st.session_state.maintenance_regime = maintenance_regime
                    st.session_state.environment = environment
                    
                    # Success message
                    st.success("FMEA generated successfully!")
                except Exception as e:
                    st.error(f"Error generating FMEA: {str(e)}")

# Main content area - shown when results are available
if st.session_state.fmea_results:
    # Make sure these variables are available in this scope for the export functionality
    asset_type = st.session_state.get("asset_type", "Unknown Asset")
    selected_characteristics = st.session_state.get("selected_characteristics", {})
    temperature_profile = st.session_state.get("temperature_profile", "Normal")
    maintenance_regime = st.session_state.get("maintenance_regime", "Standard")
    environment = st.session_state.get("environment", "Urban")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["FMEA Results", "Weibull Analysis", "Export"])
    
    # Tab 1: FMEA Results
    with tab1:
        st.header("Failure Mode and Effects Analysis (FMEA)")
        
        # Convert FMEA results to DataFrame for display
        fmea_df = pd.DataFrame(st.session_state.fmea_results)
        
        # Allow column reordering for better display
        if not fmea_df.empty and set(['failure_mode', 'effect', 'cause', 'severity', 'occurrence', 'detection', 'rpn']).issubset(fmea_df.columns):
            fmea_df = fmea_df[['failure_mode', 'effect', 'cause', 'severity', 'occurrence', 'detection', 'rpn'] + 
                             [col for col in fmea_df.columns if col not in ['failure_mode', 'effect', 'cause', 'severity', 'occurrence', 'detection', 'rpn', 'weibull_beta', 'weibull_eta']]]
        
        # Display the DataFrame
        st.dataframe(fmea_df, use_container_width=True)
        
        # Display RPN breakdown as a horizontal bar chart
        if 'rpn' in fmea_df.columns and 'failure_mode' in fmea_df.columns:
            st.subheader("Risk Priority Number (RPN) by Failure Mode")
            fig = px.bar(
                fmea_df.sort_values(by='rpn', ascending=False),
                x='rpn',
                y='failure_mode',
                orientation='h',
                color='rpn',
                color_continuous_scale=[(0, "green"), (0.5, "yellow"), (1, "red")],
                labels={'rpn': 'Risk Priority Number', 'failure_mode': 'Failure Mode'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Weibull Analysis
    with tab2:
        st.header("Weibull Reliability Analysis")
        
        if st.session_state.weibull_data:
            # 1. Show combined Weibull curves
            st.subheader("Failure Probability over Time")
            
            fig = go.Figure()
            colors = px.colors.qualitative.Plotly  # Get a color palette
            
            for i, (mode_name, data) in enumerate(st.session_state.weibull_data.items()):
                color_idx = i % len(colors)  # Cycle through colors if more modes than colors
                fig.add_trace(go.Scatter(
                    x=data['time'],
                    y=data['failure_probability'],
                    mode='lines',
                    name=mode_name,
                    line=dict(color=colors[color_idx]),
                ))
            
            fig.update_layout(
                xaxis_title="Time (hours)",
                yaxis_title="Failure Probability",
                legend_title="Failure Modes",
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 2. Allow individual Weibull curve analysis
            st.subheader("Detailed Analysis by Failure Mode")
            selected_mode = st.selectbox(
                "Select Failure Mode",
                options=list(st.session_state.weibull_data.keys())
            )
            
            if selected_mode:
                # Get failure mode details from FMEA results
                mode_details = next((mode for mode in st.session_state.fmea_results 
                                     if mode["failure_mode"] == selected_mode), {})
                
                # Display mode details
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Severity", mode_details.get("severity", "N/A"))
                with col2:
                    st.metric("Occurrence", mode_details.get("occurrence", "N/A"))
                with col3:
                    st.metric("Detection", mode_details.get("detection", "N/A"))
                
                # Display Weibull parameters
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Weibull Shape (β)", f"{mode_details.get('weibull_beta', 'N/A')}")
                with col2:
                    st.metric("Weibull Scale (η)", f"{mode_details.get('weibull_eta', 'N/A')} hours")
                
                # Show individual Weibull curve
                data = st.session_state.weibull_data[selected_mode]
                
                # Create figure with 2 y-axes
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=data['time'],
                    y=data['failure_probability'],
                    name='Failure Probability',
                    line=dict(color='red')
                ))
                fig.add_trace(go.Scatter(
                    x=data['time'],
                    y=data['reliability'],
                    name='Reliability',
                    line=dict(color='green'),
                    yaxis="y2"
                ))
                
                fig.update_layout(
                    xaxis=dict(title="Time (hours)"),
                    yaxis=dict(
                        title=dict(
                            text="Failure Probability",
                            font=dict(color="red")
                        ),
                        tickfont=dict(color="red")
                    ),
                    yaxis2=dict(
                        title=dict(
                            text="Reliability",
                            font=dict(color="green")
                        ),
                        tickfont=dict(color="green"),
                        anchor="x",
                        overlaying="y",
                        side="right"
                    ),
                    legend=dict(x=0.01, y=0.99, bordercolor="Black", borderwidth=1),
                    hovermode="x unified"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Life characteristics
                st.subheader("Life Characteristics")
                mttf = mode_details.get('mttf', data['time'][-1] * 0.5)  # Default to a sensible value if not provided
                
                life_data = [
                    {"metric": "Mean Time To Failure (MTTF)", "value": f"{mttf:.2f} hours"},
                    {"metric": "B10 Life (10% fail)", "value": f"{data['time'][next((i for i, p in enumerate(data['failure_probability']) if p >= 0.10), 0)]:.2f} hours"},
                    {"metric": "B50 Life (50% fail)", "value": f"{data['time'][next((i for i, p in enumerate(data['failure_probability']) if p >= 0.50), 0)]:.2f} hours"},
                    {"metric": "Reliability at 10,000 hours", "value": f"{data['reliability'][next((i for i, t in enumerate(data['time']) if t >= 10000), -1)] * 100:.2f}%"},
                ]
                
                life_df = pd.DataFrame(life_data)
                st.table(life_df)
    
    # Tab 3: Export
    with tab3:
        st.header("Export Results")
        
        # Create options for export
        export_format = st.radio(
            "Select export format:",
            options=["CSV", "JSON", "Excel"],
            index=0
        )
        
        if st.button("Generate Export"):
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename_base = f"FMEA_{timestamp}"
                
                # Create FMEA DataFrame
                fmea_df = pd.DataFrame(st.session_state.fmea_results)
                
                # Create Weibull DataFrame (summarized)
                weibull_summary = []
                for mode_name, data in st.session_state.weibull_data.items():
                    # Get index of 10% failure probability
                    idx_10pct = next((i for i, p in enumerate(data['failure_probability']) if p >= 0.10), 0)
                    
                    # Get index of 50% failure probability (B50 life)
                    idx_50pct = next((i for i, p in enumerate(data['failure_probability']) if p >= 0.50), 0)
                    
                    # Find MTTF from the corresponding failure mode
                    mode_details = next((mode for mode in st.session_state.fmea_results if mode["failure_mode"] == mode_name), {})
                    mttf = mode_details.get('mttf', data['time'][-1] * 0.5)
                    
                    weibull_summary.append({
                        "failure_mode": mode_name,
                        "beta": mode_details.get('weibull_beta', 'N/A'),
                        "eta": mode_details.get('weibull_eta', 'N/A'),
                        "mttf": mttf,
                        "b10_life": data['time'][idx_10pct],
                        "b50_life": data['time'][idx_50pct],
                    })
                
                weibull_df = pd.DataFrame(weibull_summary)
                
                if export_format == "CSV":
                    # For CSV, create two separate files
                    fmea_csv = fmea_df.to_csv(index=False)
                    weibull_csv = weibull_df.to_csv(index=False)
                    
                    # Create download buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download FMEA (CSV)",
                            data=fmea_csv,
                            file_name=f"{filename_base}_FMEA.csv",
                            mime="text/csv",
                        )
                    
                    with col2:
                        st.download_button(
                            label="Download Weibull Data (CSV)",
                            data=weibull_csv,
                            file_name=f"{filename_base}_Weibull.csv",
                            mime="text/csv",
                        )
                
                elif export_format == "JSON":
                    # For JSON, combine everything into one file
                    export_data = {
                        "fmea": st.session_state.fmea_results,
                        "weibull_summary": weibull_summary,
                        "asset_type": asset_type,
                        "timestamp": timestamp
                    }
                    
                    json_data = json.dumps(export_data, indent=2)
                    
                    st.download_button(
                        label="Download JSON Report",
                        data=json_data,
                        file_name=f"{filename_base}.json",
                        mime="application/json",
                    )
                
                elif export_format == "Excel":
                    # For Excel, use pandas ExcelWriter to create a workbook with multiple sheets
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        fmea_df.to_excel(writer, sheet_name='FMEA', index=False)
                        weibull_df.to_excel(writer, sheet_name='Weibull_Summary', index=False)
                        
                        # Create a sheet for asset characteristics
                        char_df = pd.DataFrame([{
                            "Asset Type": asset_type,
                            **selected_characteristics,
                            "Temperature Profile": temperature_profile,
                            "Maintenance Regime": maintenance_regime,
                            "Environmental Conditions": environment
                        }]).T.reset_index()
                        char_df.columns = ['Characteristic', 'Value']
                        char_df.to_excel(writer, sheet_name='Asset_Characteristics', index=False)
                    
                    output.seek(0)
                    
                    st.download_button(
                        label="Download Excel Report",
                        data=output,
                        file_name=f"{filename_base}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                
                st.success("Export files generated successfully!")
            
            except Exception as e:
                st.error(f"Error generating export: {str(e)}")

else:
    # This should not be displayed since we're showing the configuration form above when no results exist
    pass
    
    # Placeholder content with explanations
    with st.expander("What is an FMEA?"):
        st.markdown("""
        **Failure Mode and Effects Analysis (FMEA)** is a systematic, proactive method for evaluating a process 
        to identify where and how it might fail, and to assess the relative impact of different failures to 
        prioritize corrective actions.
        
        FMEA typically includes:
        - **Failure Modes**: The ways in which something might fail
        - **Effects**: The consequences of those failures
        - **Causes**: Why the failures might occur
        - **Risk Assessment**: Typically using Severity, Occurrence, and Detection ratings
        - **RPN (Risk Priority Number)**: A metric to prioritize attention (Severity × Occurrence × Detection)
        """)
    
    with st.expander("What is a Weibull Analysis?"):
        st.markdown("""
        **Weibull Analysis** is a method used in reliability engineering to model and analyze failure data. 
        The Weibull distribution is flexible and can model a variety of failure behaviors.
        
        Key components:
        - **Weibull Shape Parameter (β)**: Describes the pattern of failures over time
          - β < 1: Decreasing failure rate (early failures)
          - β = 1: Constant failure rate (random failures)
          - β > 1: Increasing failure rate (wear-out failures)
        
        - **Weibull Scale Parameter (η)**: Characteristic life, the time at which 63.2% of items will fail
        
        - **Weibull Curves**: Visual representation of failure probability or reliability over time
        """)
    
    with st.expander("How to use this application"):
        st.markdown("""
        1. Select your asset type from the dropdown above
        2. Configure the operating characteristics relevant to your asset
        3. Set advanced options if needed (temperature profile, maintenance regime, etc.)
        4. Click 'Generate FMEA' to create your analysis
        5. Explore the results in the FMEA Results and Weibull Analysis tabs
        6. Export your results in your preferred format
        """)