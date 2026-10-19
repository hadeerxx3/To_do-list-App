import json
import os
import streamlit as st

FILENAME = "todo_list.json"

def load_data():
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return []
    return []

def save_data(tasks):
    try:
        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Page configuration
st.set_page_config(page_title="To Do List", page_icon="📝", layout="centered")

# Custom CSS for colors, buttons, and checkbox styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    
    /* Elegant blue color for the Add button inside the form */
    div[data-testid="stForm"] div.stButton > button {
        background-color: #4A90E2 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
    }
    div[data-testid="stForm"] div.stButton > button:hover {
        background-color: #357ABD !important;
    }

    /* Make checkbox accent color green when checked */
    input[type="checkbox"]:checked {
        accent-color: #28A745 !important;
    }

    /* Style for completed task text (black text, with line-through) */
    .completed-task {
        color: #000000;
        text-decoration: line-through;
    }

    /* Clean transparent delete button (trash icon without border/background) */
    div[data-testid="stHorizontalBlock"] div.stButton > button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
        font-size: 18px !important;
    }

    /* Elegant red style for Clear All Tasks button */
    .clear-btn > button {
        background-color: #E74C3C !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
    }
    .clear-btn > button:hover {
        background-color: #C0392B !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📝 To Do List")
st.caption("Organize your day efficiently!")

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = load_data()

# Add Task Section using st.form to safely auto-clear the input
with st.form(key="task_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        new_task_input = st.text_input("New Task", placeholder="Type a task and press Add...", label_visibility="collapsed", key="task_text_box")
    with col2:
        submit_button = st.form_submit_button("➕ Add", use_container_width=True)

if submit_button:
    task_value = st.session_state.task_text_box.strip()
    if task_value:
        st.session_state.tasks.append({"title": task_value, "completed": False})
        save_data(st.session_state.tasks)
        st.rerun()

st.divider()
st.subheader("📋 My Tasks List")

# Tasks Display List
if not st.session_state.tasks:
    st.info("No tasks added yet!")
else:
    for index, task in enumerate(st.session_state.tasks):
        col_check, col_text, col_delete = st.columns([0.1, 0.8, 0.1])
        
        with col_check:
            is_done = st.checkbox("", value=task["completed"], key=f"check_{index}", label_visibility="collapsed")
            if is_done != task["completed"]:
                st.session_state.tasks[index]["completed"] = is_done
                save_data(st.session_state.tasks)
                st.rerun()

        with col_text:
            if task["completed"]:
                st.markdown(f'<span class="completed-task"><b>{task["title"]}</b></span>', unsafe_allow_html=True)
            else:
                st.markdown(f"**{task['title']}**")

        with col_delete:
            if st.button("🗑️", key=f"del_{index}"):
                st.session_state.tasks.pop(index)
                save_data(st.session_state.tasks)
                st.rerun()

st.divider()

# Clear all button inside a container with a custom red style
st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
if st.button("⚠️ Clear All Tasks", use_container_width=True):
    st.session_state.tasks = []
    save_data([])
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)