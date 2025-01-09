import gradio as gr

# Function to generate a greeting based on the slider value
def generate_greeting(intensity):
    # TODO: make these more interesting and dynamic, from bored student to excited puppy
    greetings = [
        "hi..",
        "hi...",
        "hihi...",
        "hihi..",
        "hihihi...",
        "hihihi..",
        "hihihihi...",
        "hihihihi..",
        "wow, hihihihi!!!"
    ]
    return greetings[intensity]

# Gradio interface with a slider and a button
with gr.Blocks() as demo:
    slider = gr.Slider(0, 9, label="Greeting Intensity")
    button = gr.Button("Hello")
    output = gr.Textbox()

    button.click(fn=generate_greeting, inputs=slider, outputs=output)

demo.launch()
