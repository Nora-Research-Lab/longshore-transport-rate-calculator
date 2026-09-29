![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Longshore Transport Rate Calculator
 
*For coastal engineers and geoscientists: enter wave height, angle, and sediment characteristics to instantly compute annual longshore sediment transport using the CERC formula.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Coastal & Sedimentary Studies
 
The Longshore Transport Rate Calculator implements the Coastal Engineering Research Center (CERC) formula for longshore sediment transport. The user provides three wave parameters at breaking: significant wave height H_b (in meters, range 0.1–10 m), wave angle relative to the shoreline α_b (in degrees, range 0–90°), and wave peak period T_p (in seconds, range 2–20 s). Additional inputs: sediment type selection from dropdown (fine sand, medium sand, coarse sand, gravel) which sets a default dimensionless K coefficient (0.77, 0.92, 1.1, 1.3 respectively) based on published values; the user may override K with a custom value (0.2–2.0). The calculation steps: 1) Breaker index γ = 0.78; breaker depth h_b = H_b / γ. 2) Group velocity at breaking C_g = sqrt(g * h_b) with g = 9.81 m/s². 3) Wave energy flux longshore component P_l = (ρ_w * g * H_b² * C_g * sin(2α_b)) / 16, where ρ_w = 1025 kg/m³. 4) Longshore sediment transport rate Q = K * P_l / (ρ_w * g * (s-1)*(1-p)), with s = 2.65 (quartz density ratio) and p = 0.4 (sediment porosity). 5) Convert Q from m³/s to m³/year (multiply by 31,536,000). 6) Classify: very low (<1,000), low (1,000–10,000), moderate (10,000–50,000), high (50,000–200,000), very high (>200,000) m³/yr. Gradio UI: row of inputs (H_b number, α_b slider 0–90°, T_p number, sediment type dropdown, K override number box); a compute button; outputs: numeric Q (m³/yr) with classification text, and a horizontal bar chart showing Q relative to class thresholds. No AI/ML component; purely deterministic engineering calculation.
 
## Run it
 
```bash
docker build -t longshore-transport-rate-calculator .
docker run -p 7860:7860 longshore-transport-rate-calculator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-29.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
