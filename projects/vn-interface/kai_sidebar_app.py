import gradio as gr

# Sidebar avatar component
def kai_sidebar(lesson_step):
    # Define states for different parts of the tutorial
    avatar_emotes = {
        "default": ("#00BFFF", "[*Kai in investigative mode*] Let’s follow the data trail..."),
        "step1": ("#1E90FF", "[*Tips fedora*] We’re getting started with account creation!"),
        "step2": ("#4682B4", "[*Pushes up glasses*] Time to set your username and password!"),
        "step3": ("#5F9EA0", "[*Adjusts hoodie*] Let’s tackle the verification steps!"),
        "final": ("#87CEEB", "[*Victory pose*] You’re all set and logged in. Well done!"),
    }

    color, emote = avatar_emotes.get(lesson_step, avatar_emotes["default"])
    html_content = f"""
    <div style="background-color: {color}; padding: 20px; border-radius: 10px; text-align: center;">
        <h3 style="color: white;">{emote}</h3>
        <p>Current Lesson Step: {lesson_step}</p>
    </div>
    """
    return html_content

# Define Gradio interface
lesson_steps = ["default", "step1", "step2", "step3", "final"]
demo = gr.Interface(
    fn=kai_sidebar,
    inputs=gr.Dropdown(choices=lesson_steps, label="Select Lesson Step"),
    outputs="html",
    title="Kai's GitHub Onboarding Walkthrough",
    description="Choose a lesson step to see Kai's avatar and emote change as you progress through the GitHub onboarding tutorial."
)

# Launch the Gradio app
demo.launch()
