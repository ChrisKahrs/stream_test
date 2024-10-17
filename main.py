import streamlit as st
import json
import copy
import time
import datetime
import requests

# Fetch menu data from the server
if "initial_menu_data" not in st.session_state:
    response = requests.post("https://ckfastapi.azurewebsites.net/menu")
    st.session_state.initial_menu_data = response.json()

if "finish_time" not in st.session_state:
    st.session_state.finish_time = datetime.datetime.now() + datetime.timedelta(seconds=st.session_state.initial_menu_data.get("time_limit", 30))

# Create a deep copy of the original data to track changes
menu_data = copy.deepcopy(st.session_state.initial_menu_data)
changed_items = {}

def str2bool(v):
    if v.lower() == "true":
        return True
    return False

# Streamlit app
def main():
    global menu_data, changed_items
    st.title("Interactive Menu Editor")

    # URL suffix input
    url_suffix = st.text_input("Enter URL Suffix", key="url_suffix")

    # Show instructions
    st.write("Click on a menu item to edit the value.")

    # Track changes
    updated_menu_data = copy.deepcopy(menu_data)

    # Timer and progress bar settings at the top
    if "finish_time" not in st.session_state:
        st.session_state.finish_time = datetime.datetime.now() + datetime.timedelta(seconds=30)

    progress_bar_top = st.progress(0)
    timer_placeholder_top = st.empty()

    submit_button_pressed = st.button("Submit Data to Server")

    # Create an expandable frame for each top-level item in the JSON
    for category, items in menu_data.items():
        with st.expander(f"{category}"):
            for item, attributes in items.items():
                value = attributes.get("value")
                value_type = attributes.get("type")

                # Determine the type of value and create the appropriate widget
                if value_type == "int":
                    new_value = st.number_input(f"{item}", value=int(value), min_value=0, key=f"{category}_{item}")
                elif value_type == "float":
                    new_value = st.number_input(f"{item}", value=float(value), min_value=0.0, key=f"{category}_{item}")
                elif value_type == "str":
                    new_value = st.text_input(f"{item}", value=str(value), key=f"{category}_{item}")
                elif value_type == "bool":
                    new_value = st.checkbox(f"{item}", value=str2bool(value), key=f"{category}_{item}")
                elif value_type == "single_select_list":
                    options = attributes.get("options", [])
                    new_value = st.selectbox(f"{item}", options=options, index=options.index(value) if value in options else 0, key=f"{category}_{item}")
                else:
                    new_value = value  # Leave unchanged if type is not recognized

                # Update the JSON data with the new value
                updated_menu_data[category][item]["value"] = new_value

    # Add an open text input for other ideas
    other_ideas = st.text_input("Other Ideas", key="Other_Ideas")
    if other_ideas:
        updated_menu_data["Other_Ideas"] = {"value": other_ideas, "type": "str"}

    progress_bar_bottom = st.progress(0)
    timer_placeholder_bottom = st.empty()

    # Function to simulate data submission
    def submit_data():
        global changed_items

        # Simulating sending data to server
        if changed_items:
            post_url = f"https://ckfastapi.azurewebsites.net/menu2/{url_suffix}" if url_suffix else "https://ckfastapi.azurewebsites.net/menu2"
            response = requests.post(post_url, json=changed_items)
            if response.status_code == 200:
                st.success("Data submitted to the server!")
            else:
                st.error("Failed to submit data to the server.")
        else:
            st.warning("No changes to submit.")

        # Reset the timer after submission
        st.session_state.finish_time = datetime.datetime.now() + datetime.timedelta(seconds=30)

    # Display changed items ready for submission at the bottom
    changed_items = {}
    for category, items in updated_menu_data.items():
        for item, attributes in items.items():
            new_value = attributes.get("value")
            old_value = st.session_state.initial_menu_data.get(category, {}).get(item, {}).get("value")
            if new_value != old_value:
                if type(new_value) == bool and (str2bool(old_value) == new_value):
                        continue
                else:
                    if category not in changed_items:
                        changed_items[category] = {}
                    changed_items[category][item] = new_value

    if changed_items:
        st.subheader("Changed Items Ready to Submit:")
        st.json(changed_items)

    # Start the countdown timer
    while True:
        current_time = datetime.datetime.now()
        time_left = (st.session_state.finish_time - current_time).total_seconds()
        time_limit = st.session_state.initial_menu_data.get("time_limit", 30)

        if time_left <= 0:
            st.warning("Time's up! Automatically submitting data to the server...")
            submit_data()
            break
        elif submit_button_pressed:
            submit_data()
            break
        else:
            progress_bar_top.progress((time_limit - time_left) / time_limit)
            timer_placeholder_top.text(f"Time left: {int(time_left)} seconds")
            progress_bar_bottom.progress((time_limit - time_left) / time_limit)
            timer_placeholder_bottom.text(f"Time left: {int(time_left)} seconds")

        # Wait for one second between updates
        time.sleep(1)

if __name__ == "__main__":
    main()