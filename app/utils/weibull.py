import numpy as np
from scipy import stats

def generate_weibull_data(beta, eta, num_points=1000, max_time_multiplier=3.0):
    """
    Generate Weibull distribution data for plotting.
    
    Args:
        beta (float): Shape parameter (Weibull beta)
        eta (float): Scale parameter (Weibull eta)
        num_points (int): Number of data points to generate
        max_time_multiplier (float): Multiplier for maximum time value
    
    Returns:
        dict: Dictionary containing time points and corresponding 
              failure probability and reliability values
    """
    # Create time points (more points at the beginning for better resolution)
    max_time = eta * max_time_multiplier
    time_points = np.geomspace(1, max_time, num_points)
    
    # Calculate Weibull CDF (failure probability)
    weibull_dist = stats.weibull_min(beta, scale=eta)
    failure_probability = weibull_dist.cdf(time_points)
    
    # Calculate reliability (survival function)
    reliability = 1 - failure_probability
    
    # Calculate failure rate (hazard function)
    failure_rate = weibull_dist.pdf(time_points) / reliability
    
    # Calculate additional metrics
    mttf = eta * np.exp(np.log(np.e) / beta)  # Mean Time To Failure
    
    return {
        "time": time_points.tolist(),
        "failure_probability": failure_probability.tolist(),
        "reliability": reliability.tolist(),
        "failure_rate": failure_rate.tolist(),
        "mttf": mttf
    }

def calculate_system_reliability(component_reliabilities, system_type="series"):
    """
    Calculate system reliability based on component reliabilities.
    
    Args:
        component_reliabilities (list): List of component reliability values
        system_type (str): 'series' or 'parallel'
    
    Returns:
        float: System reliability
    """
    if system_type == "series":
        # In a series system, all components must work for the system to work
        system_reliability = np.prod(component_reliabilities)
    elif system_type == "parallel":
        # In a parallel system, at least one component must work
        system_reliability = 1 - np.prod([1 - r for r in component_reliabilities])
    else:
        raise ValueError("System type must be 'series' or 'parallel'")
    
    return system_reliability

def b_life(beta, eta, percent):
    """
    Calculate B-life, which is the time by which a given percentage of units will fail.
    
    Args:
        beta (float): Shape parameter
        eta (float): Scale parameter
        percent (float): Percentage of failures (0-100)
    
    Returns:
        float: Time at which the given percentage of units will fail
    """
    # Convert percentage to probability (0-1)
    p = percent / 100.0
    
    # B-life formula
    return eta * (-np.log(1 - p)) ** (1 / beta)
