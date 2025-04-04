import os
import json
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL_NAME = "gpt-4o"

def get_openai_client():
    """Initialize and return the OpenAI client."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    return OpenAI(api_key=api_key)

def generate_fmea_with_gpt(asset_type, characteristics):
    """
    Generate FMEA data using GPT for a given asset type and its characteristics.
    
    Args:
        asset_type (str): The type of electrical T&D asset
        characteristics (dict): Operating characteristics of the asset
    
    Returns:
        dict: Structured FMEA data with failure modes and Weibull parameters
    """
    client = get_openai_client()
    
    # Format characteristics for prompt
    characteristics_str = "\n".join([f"- {key}: {value}" for key, value in characteristics.items()])
    
    # Create system prompt with expert context and detailed instructions
    system_prompt = """
    You are an expert electrical engineer specializing in reliability engineering for transmission and distribution assets.
    Your task is to generate a comprehensive Failure Mode and Effects Analysis (FMEA) for the specified electrical asset type,
    considering its operating characteristics.
    
    For each failure mode:
    1. Identify the potential causes
    2. Describe the effects
    3. Assess severity (1-10), occurrence (1-10), and detection (1-10) ratings
    4. Calculate the RPN (Risk Priority Number = Severity × Occurrence × Detection)
    5. Provide realistic Weibull distribution parameters (beta and eta) for each failure mode
    6. Include Mean Time To Failure (MTTF) estimates
    
    The Weibull beta parameter should reflect the failure pattern:
    - β < 1 for early failures/infant mortality
    - β = 1 for random failures
    - β > 1 for wear-out failures
    
    The Weibull eta parameter should be the characteristic life in hours.
    
    You must respond with valid JSON only, using the following structure:
    {
        "failure_modes": [
            {
                "failure_mode": "string",
                "cause": "string",
                "effect": "string",
                "severity": number(1-10),
                "occurrence": number(1-10),
                "detection": number(1-10),
                "rpn": number,
                "weibull_beta": number,
                "weibull_eta": number,
                "mttf": number,
                "recommendations": "string"
            },
            ...
        ]
    }
    """
    
    # Create user prompt with asset details
    user_prompt = f"""
    Generate an FMEA for a {asset_type} with the following operating characteristics:
    
    {characteristics_str}
    
    Please provide realistic failure modes specific to this asset type and operating environment,
    with appropriate severity, occurrence, detection ratings, and Weibull parameters.
    """
    
    try:
        # Make API call to OpenAI
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.5,  # Lower temperature for more consistent results
            max_tokens=4000  # Ensure we get complete responses
        )
        
        # Parse and return the response
        content = response.choices[0].message.content
        fmea_data = json.loads(content)
        
        # Validate the structure of the returned data
        if "failure_modes" not in fmea_data:
            raise ValueError("OpenAI response missing 'failure_modes' field")
        
        # Ensure all failure modes have the required fields
        for mode in fmea_data["failure_modes"]:
            # Calculate RPN if not already calculated
            if "rpn" not in mode and all(k in mode for k in ["severity", "occurrence", "detection"]):
                mode["rpn"] = mode["severity"] * mode["occurrence"] * mode["detection"]
        
        return fmea_data
    
    except Exception as e:
        raise Exception(f"Error in OpenAI FMEA generation: {str(e)}")
