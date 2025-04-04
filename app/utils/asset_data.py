def get_asset_types():
    """
    Returns a list of supported electrical transmission and distribution asset types.
    """
    return [
        "Power Transformer",
        "Circuit Breaker",
        "Disconnect Switch",
        "Surge Arrester",
        "Recloser",
        "Capacitor Bank",
        "Current Transformer",
        "Voltage Transformer",
        "Transmission Line",
        "Distribution Line",
        "Busbar",
        "Underground Cable",
        "Insulator",
        "Lightning Arrester",
        "Load Tap Changer"
    ]

def get_operating_characteristics(asset_type):
    """
    Returns relevant operating characteristics based on the asset type.
    
    Args:
        asset_type (str): The type of electrical asset
    
    Returns:
        dict: Dictionary of characteristic names and their possible values
    """
    # Define common characteristics for all assets
    common_characteristics = {
        "Installation Type": ["Indoor", "Outdoor", "Underground", "Substation", "Pole-mounted"],
        "Age (years)": (0, 50, 10),  # min, max, default
        "Duty Cycle": ["Continuous", "Intermittent", "Standby", "Peak load only"],
        "Humidity Level": ["Low", "Medium", "High", "Variable"],
    }
    
    # Specific characteristics by asset type
    asset_specific = {
        "Power Transformer": {
            "Cooling Type": ["ONAN", "ONAF", "OFAF", "ODAF"],
            "Rating (MVA)": {"type": "range", "min": 1, "max": 1000, "default": 100, "step": 1},
            "Oil Type": ["Mineral Oil", "Synthetic Ester", "Natural Ester", "Silicone"],
            "Tap Changer Type": ["On-load", "Off-load", "None"],
            "Winding Configuration": ["Delta-Wye", "Wye-Wye", "Delta-Delta"],
            "Overload Frequency": ["Rare", "Occasional", "Frequent"]
        },
        "Circuit Breaker": {
            "Type": ["Air", "Oil", "SF6", "Vacuum"],
            "Voltage Rating (kV)": {"type": "range", "min": 1, "max": 800, "default": 138, "step": 1},
            "Current Rating (A)": {"type": "range", "min": 100, "max": 5000, "default": 1200, "step": 100},
            "Interrupting Capacity (kA)": {"type": "range", "min": 10, "max": 100, "default": 40, "step": 5},
            "Operating Mechanism": ["Spring", "Hydraulic", "Pneumatic", "Magnetic"]
        },
        "Disconnect Switch": {
            "Type": ["Vertical Break", "Center Break", "Double Break", "Pantograph"],
            "Voltage Rating (kV)": {"type": "range", "min": 1, "max": 800, "default": 138, "step": 1},
            "Current Rating (A)": {"type": "range", "min": 100, "max": 4000, "default": 1200, "step": 100},
            "Operating Mechanism": ["Manual", "Motor Operated"]
        },
        "Surge Arrester": {
            "Type": ["Metal Oxide", "Gapped Silicon Carbide", "Polymeric", "Porcelain"],
            "Voltage Rating (kV)": {"type": "range", "min": 1, "max": 800, "default": 138, "step": 1},
            "Energy Capability (kJ/kV)": {"type": "range", "min": 1.0, "max": 20.0, "default": 5.0, "step": 0.5}
        },
        "Recloser": {
            "Type": ["Oil", "Vacuum", "SF6"],
            "Voltage Rating (kV)": {"type": "range", "min": 1, "max": 40, "default": 15, "step": 1},
            "Control Type": ["Electromechanical", "Electronic", "Microprocessor"],
            "Operating Cycles": {"type": "range", "min": 1, "max": 5, "default": 3, "step": 1}
        },
        "Capacitor Bank": {
            "Connection Type": ["Wye", "Delta"],
            "Switching Type": ["Fixed", "Switched"],
            "Voltage Rating (kV)": {"type": "range", "min": 1, "max": 40, "default": 15, "step": 1},
            "kVAR Rating": {"type": "range", "min": 100, "max": 10000, "default": 1200, "step": 100}
        },
        "Current Transformer": {
            "Type": ["Wound", "Bar", "Bushing", "Toroidal"],
            "Ratio": ["100:5", "200:5", "300:5", "400:5", "500:5", "600:5", "800:5", "1000:5", "1200:5", "2000:5"],
            "Accuracy Class": ["0.1", "0.2", "0.5", "1.0", "3.0", "5.0"],
            "Burden (VA)": {"type": "range", "min": 5, "max": 100, "default": 15, "step": 5}
        },
        "Voltage Transformer": {
            "Type": ["Magnetic", "Capacitive"],
            "Ratio": ["66000:110", "110000:110", "132000:110", "220000:110", "400000:110", "765000:110"],
            "Accuracy Class": ["0.1", "0.2", "0.5", "1.0", "3.0"],
            "Burden (VA)": {"type": "range", "min": 10, "max": 200, "default": 50, "step": 10}
        },
        "Transmission Line": {
            "Conductor Type": ["ACSR", "AAAC", "ACAR", "ACCC", "OPGW"],
            "Voltage Rating (kV)": {"type": "range", "min": 69, "max": 765, "default": 138, "step": 1},
            "Structure Type": ["Lattice Tower", "Monopole", "H-Frame", "Guyed-V"],
            "Span Length (m)": {"type": "range", "min": 100, "max": 1000, "default": 300, "step": 50},
            "Wind Exposure": ["Low", "Medium", "High", "Extreme"]
        },
        "Distribution Line": {
            "Conductor Type": ["Bare", "Covered", "Insulated"],
            "Voltage Rating (kV)": {"type": "range", "min": 4, "max": 35, "default": 12, "step": 1},
            "Structure Type": ["Wood Pole", "Concrete Pole", "Steel Pole", "Underground"],
            "Span Length (m)": {"type": "range", "min": 30, "max": 300, "default": 100, "step": 10}
        },
        "Busbar": {
            "Material": ["Aluminum", "Copper", "Silver-plated"],
            "Configuration": ["Single", "Double", "Ring", "Breaker-and-a-Half"],
            "Voltage Rating (kV)": {"type": "range", "min": 1, "max": 800, "default": 138, "step": 1},
            "Current Rating (A)": {"type": "range", "min": 1000, "max": 10000, "default": 3000, "step": 500}
        },
        "Underground Cable": {
            "Insulation Type": ["XLPE", "EPR", "PILC", "HMWPE"],
            "Voltage Rating (kV)": {"type": "range", "min": 1, "max": 500, "default": 35, "step": 1},
            "Installation Method": ["Direct Buried", "Duct Bank", "Tunnel", "Submarine"],
            "Shielding": ["Tape Shield", "Wire Shield", "Lead Sheath", "None"]
        },
        "Insulator": {
            "Type": ["Porcelain", "Glass", "Polymer/Composite", "Hybrid"],
            "Configuration": ["Suspension", "Post", "Pin", "Line Post"],
            "Voltage Rating (kV)": {"type": "range", "min": 10, "max": 800, "default": 138, "step": 1},
            "Pollution Level": ["Light", "Medium", "Heavy", "Very Heavy"]
        },
        "Lightning Arrester": {
            "Type": ["Metal Oxide", "Silicon Carbide", "Expulsion"],
            "Voltage Rating (kV)": {"type": "range", "min": 1, "max": 800, "default": 138, "step": 1},
            "Discharge Current (kA)": {"type": "range", "min": 5, "max": 100, "default": 10, "step": 5},
            "Housing Material": ["Porcelain", "Polymer"]
        },
        "Load Tap Changer": {
            "Type": ["Resistive", "Reactive", "Vacuum", "Off-circuit"],
            "Control Type": ["Manual", "Automatic", "Remote"],
            "Number of Taps": {"type": "range", "min": 3, "max": 33, "default": 17, "step": 2},
            "Voltage Range (%)": {"type": "range", "min": 5, "max": 20, "default": 10, "step": 1},
            "Switching Frequency": ["Low", "Medium", "High"]
        }
    }
    
    # Merge common characteristics with asset-specific ones
    if asset_type in asset_specific:
        return {**common_characteristics, **asset_specific[asset_type]}
    else:
        return common_characteristics

def get_default_failure_modes(asset_type):
    """
    Provides default failure modes for an asset type if the LLM fails to generate them.
    
    Args:
        asset_type (str): The type of electrical asset
    
    Returns:
        list: List of dictionaries with default failure modes
    """
    # Define common default values
    default_rpn_values = {
        "Low": {"severity": 3, "occurrence": 2, "detection": 2, "rpn": 12},
        "Medium": {"severity": 5, "occurrence": 4, "detection": 4, "rpn": 80},
        "High": {"severity": 8, "occurrence": 6, "detection": 5, "rpn": 240}
    }
    
    # Define default Weibull parameters by asset type
    default_weibull = {
        "Early Failure": {"beta": 0.8, "eta": 15000, "mttf": 16875},
        "Random Failure": {"beta": 1.0, "eta": 50000, "mttf": 50000},
        "Wear-out Failure": {"beta": 3.5, "eta": 80000, "mttf": 71851}
    }
    
    # Default failure modes by asset type
    default_modes = {
        "Power Transformer": [
            {
                "failure_mode": "Insulation Breakdown",
                "cause": "Aging, overheating, moisture ingress, or electrical stress",
                "effect": "Dielectric failure, internal arcing, potential fire or explosion",
                **default_rpn_values["High"],
                **default_weibull["Wear-out Failure"],
                "recommendations": "Regular oil testing, dissolved gas analysis, and thermal imaging"
            },
            {
                "failure_mode": "Bushing Failure",
                "cause": "Contamination, cracking, or moisture ingress",
                "effect": "Flashover, loss of insulation, and transformer damage",
                **default_rpn_values["Medium"],
                **default_weibull["Wear-out Failure"],
                "recommendations": "Regular inspections, power factor testing, and timely replacement"
            },
            {
                "failure_mode": "Cooling System Malfunction",
                "cause": "Fan failure, pump issues, radiator blockage",
                "effect": "Overheating, accelerated aging, potential winding damage",
                **default_rpn_values["Medium"],
                **default_weibull["Random Failure"],
                "recommendations": "Regular maintenance of cooling systems, temperature monitoring"
            },
            {
                "failure_mode": "Tap Changer Issues",
                "cause": "Contact wear, mechanism failure, or control issues",
                "effect": "Improper voltage regulation, arcing, or mechanism seizure",
                **default_rpn_values["Medium"],
                **default_weibull["Wear-out Failure"],
                "recommendations": "Regular tap changer maintenance, oil filtration, and contact inspection"
            },
            {
                "failure_mode": "Core Failure",
                "cause": "Core lamination damage, grounding issues",
                "effect": "Increased losses, heating, noise, and vibration",
                **default_rpn_values["Low"],
                **default_weibull["Wear-out Failure"],
                "recommendations": "Core ground testing, vibration monitoring"
            }
        ],
        "Circuit Breaker": [
            {
                "failure_mode": "Contact Wear",
                "cause": "Repeated operations, fault interruptions, and arcing",
                "effect": "Increased contact resistance, heating, and potential for failure to interrupt",
                **default_rpn_values["Medium"],
                **default_weibull["Wear-out Failure"],
                "recommendations": "Contact resistance testing, travel timing analysis, and inspection"
            },
            {
                "failure_mode": "Operating Mechanism Failure",
                "cause": "Mechanical wear, lubrication issues, or component breakage",
                "effect": "Slow operation, failure to operate, or incomplete operation",
                **default_rpn_values["High"],
                **default_weibull["Wear-out Failure"],
                "recommendations": "Regular mechanism maintenance, lubrication, and timing tests"
            },
            {
                "failure_mode": "Insulating Medium Degradation",
                "cause": "Contamination, moisture, or aging of oil/gas/vacuum",
                "effect": "Reduced dielectric strength, internal flashover",
                **default_rpn_values["Medium"],
                **default_weibull["Wear-out Failure"],
                "recommendations": "Medium testing, monitoring, and scheduled replacement"
            },
            {
                "failure_mode": "Control Circuit Failure",
                "cause": "Faulty wiring, component failure, or relay malfunction",
                "effect": "Failure to trip/close or spurious operation",
                **default_rpn_values["High"],
                **default_weibull["Random Failure"],
                "recommendations": "Control circuit verification, component testing"
            }
        ]
    }
    
    # Return default modes for the specified asset type, or a generic list if not found
    if asset_type in default_modes:
        return default_modes[asset_type]
    else:
        # Generic failure modes for any electrical asset
        return [
            {
                "failure_mode": "Insulation Failure",
                "cause": "Aging, environmental stress, or electrical overstress",
                "effect": "Short circuit, ground fault, or equipment damage",
                **default_rpn_values["High"],
                **default_weibull["Wear-out Failure"],
                "recommendations": "Regular insulation testing and environmental protection"
            },
            {
                "failure_mode": "Mechanical Failure",
                "cause": "Wear, fatigue, or improper installation",
                "effect": "Structural damage, misalignment, or operational failure",
                **default_rpn_values["Medium"],
                **default_weibull["Wear-out Failure"],
                "recommendations": "Regular mechanical inspections and preventive maintenance"
            },
            {
                "failure_mode": "Electrical Connection Failure",
                "cause": "Loose connections, corrosion, or thermal cycling",
                "effect": "High resistance connections, heating, and potential fire",
                **default_rpn_values["Medium"],
                **default_weibull["Random Failure"],
                "recommendations": "Thermographic inspection, connection torque verification"
            },
            {
                "failure_mode": "Environmental Damage",
                "cause": "Water ingress, contamination, or extreme temperatures",
                "effect": "Corrosion, reduced lifespan, or catastrophic failure",
                **default_rpn_values["Medium"],
                **default_weibull["Random Failure"],
                "recommendations": "Improved environmental protection, regular cleaning"
            }
        ]
