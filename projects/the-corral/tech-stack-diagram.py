tech-stack-diagram.py

# Replacing FancyArrowPatch with Arrow for compatibility
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Function to add boxes
def add_box(x, y, width, height, label, color='lightblue'):
    rect = patches.Rectangle((x, y), width, height, edgecolor='black', facecolor=color, lw=1.5)
    ax.add_patch(rect)
    ax.text(x + width / 2, y + height / 2, label, ha='center', va='center', fontsize=10, fontweight='bold')

# Function to add arrows
def add_arrow(x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor='black', arrowstyle='->'))

# Add components
add_box(1, 8, 2, 1, 'Frontend (React UI)')
add_box(4, 8, 2, 1, 'API (FastAPI/Node.js)')
add_box(7, 8, 2, 1, 'WebSocket Service')
add_box(4, 6, 2, 1, 'LangChain (Agent Manager)', color='lightgreen')
add_box(1, 4, 2, 1, 'Authentication (Auth0)')
add_box(4, 4, 2, 1, 'Memory Store (Redis)', color='khaki')
add_box(7, 4, 2, 1, 'LLM API (GPT/Codex)', color='lightcoral')
add_box(4, 2, 2, 1, 'Task Queue (Celery/NATS)', color='lightpink')
add_box(1, 2, 2, 1, 'Database (PostgreSQL)')

# Add arrows
add_arrow(2, 8, 4, 8.5)  # Frontend to API
add_arrow(6, 8.5, 7, 8.5)  # API to WebSocket
add_arrow(5, 8, 5, 6.9)  # API to LangChain
add_arrow(5, 6, 5, 4.9)  # LangChain to Memory Store
add_arrow(6, 6.5, 7, 5)  # LangChain to LLM API
add_arrow(4, 6.5, 1, 5)  # LangChain to Auth
add_arrow(5, 4, 5, 2.9)  # Memory Store to Task Queue
add_arrow(2, 4, 2, 2.9)  # Auth to Database
add_arrow(5, 2, 7, 2.5)  # Task Queue to LLM API

# Add legend explanation
plt.text(1, 9.5, "Tech Stack Overview for Multi-Agent Collaboration Site", fontsize=14, fontweight='bold', ha='left')
plt.show()
