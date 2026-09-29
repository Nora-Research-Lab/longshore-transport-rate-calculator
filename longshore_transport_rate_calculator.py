import math

# Constants
GAMMA = 0.78        # breaker index
G = 9.81            # gravity (m/s²)
RHO_W = 1025        # seawater density (kg/m³)
S = 2.65            # sediment density ratio (quartz)
P = 0.4             # porosity
SECONDS_PER_YEAR = 31_536_000

# Default K coefficients from CERC
SEDIMENT_K_MAP = {
    "Fine Sand": 0.77,
    "Medium Sand": 0.92,
    "Coarse Sand": 1.1,
    "Gravel": 1.3
}

def classify_transport(Q_m3_per_year: float) -> str:
    """Classify transport rate into qualitative categories."""
    if Q_m3_per_year < 1000:
        return "Very Low"
    elif 1000 <= Q_m3_per_year < 10000:
        return "Low"
    elif 10000 <= Q_m3_per_year < 50000:
        return "Moderate"
    elif 50000 <= Q_m3_per_year < 200000:
        return "High"
    else:
        return "Very High"

def compute_transport_rate(H_b: float, alpha_b: float, T_p: float,
                           sediment_type: str = "Medium Sand",
                           K_override: float = None):
    """
    Compute longshore sediment transport rate using CERC formula.

    Parameters
    ----------
    H_b : float
        Significant wave height at breaking (m).
    alpha_b : float
        Wave angle relative to shoreline at breaking (degrees).
    T_p : float
        Peak wave period (s).
    sediment_type : str, optional
        One of the keys in SEDIMENT_K_MAP (case‑sensitive).
    K_override : float, optional
        Custom dimensionless coefficient. If given, overrides sediment type.

    Returns
    -------
    tuple (Q_m3_per_year, classification)
    """
    # Determine K coefficient
    if K_override is not None:
        K = K_override
    else:
        K = SEDIMENT_K_MAP.get(sediment_type, 0.92)  # default Medium Sand

    # Step 1: Breaker depth
    h_b = H_b / GAMMA

    # Step 2: Group velocity at breaking (shallow water approximation)
    C_g = math.sqrt(G * h_b)

    # Step 3: Wave energy flux longshore component
    alpha_rad = math.radians(alpha_b)
    P_l = (RHO_W * G * H_b**2 * C_g * math.sin(2 * alpha_rad)) / 16.0

    # Step 4: Volumetric transport rate (m³/s)
    Q_volume_per_sec = K * P_l / (RHO_W * G * (S - 1) * (1 - P))

    # Step 5: Convert to m³/year
    Q_m3_per_year = Q_volume_per_sec * SECONDS_PER_YEAR

    # Step 6: Classify
    classification = classify_transport(Q_m3_per_year)

    return Q_m3_per_year, classification
