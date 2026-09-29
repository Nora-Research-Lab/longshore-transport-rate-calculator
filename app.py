import gradio as gr
import plotly.graph_objects as go
from longshore_transport_rate_calculator import compute_transport_rate, SEDIMENT_K_MAP, classify_transport

def compute_and_plot(H_b, alpha_b, T_p, sediment_type, K_custom):
    if H_b is None or T_p is None:
        return "Please provide values for wave height and period.", None
    try:
        H_b = float(H_b)
        alpha_b = float(alpha_b)
        T_p = float(T_p)
    except (ValueError, TypeError):
        return "Invalid numeric input.", None
    if H_b <= 0 or H_b > 10:
        return "Wave height must be between 0.1 and 10 m.", None
    if alpha_b < 0 or alpha_b > 90:
        return "Wave angle must be between 0 and 90 degrees.", None
    if T_p < 2 or T_p > 20:
        return "Wave period must be between 2 and 20 s.", None

    K_override = None
    if K_custom is not None and K_custom != "":
        try:
            K_override = float(K_custom)
            if K_override < 0.2 or K_override > 2.0:
                return "Custom K must be between 0.2 and 2.0.", None
        except (ValueError, TypeError):
            return "Invalid custom K value.", None

    try:
        Q, classification = compute_transport_rate(H_b, alpha_b, T_p, sediment_type, K_override)
    except Exception as e:
        return f"Calculation error: {str(e)}", None

    thresholds = [1000, 10000, 50000, 200000]
    colors = [(0, 'green'), (1000, 'yellow'), (10000, 'orange'), (50000, 'red'), (200000, 'darkred')]
    bar_color = 'steelblue'
    for thresh, col in reversed(colors):
        if Q >= thresh:
            bar_color = col
            break

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[Q],
        y=['Longshore transport rate'],
        orientation='h',
        marker_color=bar_color,
        text=[f"{Q:,.0f} m³/yr"],
        textposition='outside',
        showlegend=False,
        width=0.4
    ))
    for thresh in thresholds:
        fig.add_vline(x=thresh, line_dash="dash", line_color="grey", annotation_text=f"{thresh:,}", 
                      annotation_position="top", annotation_font_size=10)
    max_x = max(Q * 1.1, 250000)
    fig.update_xaxes(range=[0, max_x])
    fig.update_layout(
        title=f"Transport Rate: {Q:,.0f} m³/yr – {classification}",
        xaxis_title="Rate (m³/yr)",
        yaxis=dict(showticklabels=False),
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    text_out = f"**Longshore Sediment Transport Rate:** {Q:,.0f} m³/yr\n**Classification:** {classification}"
    return text_out, fig

with gr.Blocks(title="Longshore Transport Rate Calculator") as demo:
    gr.Markdown("# Longshore Transport Rate Calculator (CERC Formula)")
    with gr.Row():
        H_b = gr.Number(label="Wave Height at Breaking H_b (m)", value=1.0, minimum=0.1, maximum=10.0, step=0.1)
        alpha_b = gr.Slider(label="Wave Angle α_b (degrees)", minimum=0, maximum=90, value=10, step=1)
        T_p = gr.Number(label="Wave Peak Period T_p (s)", value=8.0, minimum=2.0, maximum=20.0, step=0.5)
    with gr.Row():
        sediment_type = gr.Dropdown(
            choices=list(SEDIMENT_K_MAP.keys()),
            label="Sediment Type",
            value="Medium Sand"
        )
        K_custom = gr.Number(label="Custom K (optional, 0.2–2.0)", value=None, minimum=0.2, maximum=2.0, step=0.01)
    compute_btn = gr.Button("Compute Transport Rate", variant="primary")
    with gr.Row():
        output_text = gr.Markdown()
    output_plot = gr.Plot()

    compute_btn.click(
        fn=compute_and_plot,
        inputs=[H_b, alpha_b, T_p, sediment_type, K_custom],
        outputs=[output_text, output_plot]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
