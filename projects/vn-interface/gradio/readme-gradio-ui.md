# gradio ui test

we should use a simple gradio ui for testing...

TODO: look at what the react demo did, and maybe do something similar (not using react, but gradio)

# Gradio UI Project

This project contains a sample Gradio app that allows you to adjust a slider from zero ('hi..') to nine ('wow, hihihihi!!!') and get a greeting of variable intensity from the app when you push "Hello".

## Getting Started

To set up and run the Gradio app, follow these steps:

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/norrisaftcc/the_intern.git
   cd the_intern/projects/gradio-ui
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

1. **Run the Gradio app**:
   ```bash
   python app.py
   ```

2. **Access the app**:
   - Open your web browser and go to `http://127.0.0.1:7860` to access the Gradio interface.

### Example Output

When you run the app and adjust the slider, you will see greetings of variable intensity based on the slider value. For example:
- Slider at 0: "hi.."
- Slider at 9: "wow, hihihihi!!!"

Enjoy experimenting with the greeting intensities!

### Note

The Gradio app now generates dynamic greetings based on the slider value, ranging from "hi.." to "wow, hihihihi!!!". The greetings are more interesting and dynamic, making the app more engaging.
