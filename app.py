import streamlit as st
import openai
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# ----------------------------
# RESEARCHER NODE
# ----------------------------
def researcher_node(destination: str) -> str:
    prompt = f"""
    Generate 10 questions based on the {destination}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Researcher node failed: {e}"

# ----------------------------
# PLANNER NODE
# ----------------------------
def planner_node(destination: str, days: int, research_notes: str) -> str:
    prompt = f"""
    Generate a quiz based on the difficulty {days}:
    {research_notes}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Planner node failed: {e}"

# ----------------------------
# STREAMLIT UI
# ----------------------------
def main():
    st.set_page_config(page_title="AI Travel Agent", page_icon="🌎", layout="centered")
    st.title("🌎 Generate Quiz")
    st.write("This generates a quiz based on your preferences")

    # Inputs
    destination = st.text_input("Select Topic", placeholder="e.g., Paris")
    days = st.number_input("Level of Difficulty from 1 to 10", min_value=1, max_value=30, value=3)

    if st.button("Generate Quiz"):
        if not destination.strip():
            st.error("Please enter a valid Topic.")
        else:
            with st.spinner("Researching your destination..."):
                research_notes = researcher_node(destination)

            st.subheader("Research Notes")
            st.write(research_notes)

            with st.spinner("Building your itinerary..."):
                itinerary = planner_node(destination, days, research_notes)

            st.subheader("Final Itinerary")
            st.write(itinerary)

if __name__ == "__main__":
    main()
