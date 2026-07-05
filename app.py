import streamlit as str
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
# It automatically picks up the OPENAI_API_KEY environment variable
client = OpenAI()

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Application Header
st.title("🌍 AI Travel Planner")
st.markdown("Plan your next adventure with personalized, AI-generated itineraries.")

# Sidebar Configuration
st.sidebar.header("✈️ Trip Customization")

destination = st.sidebar.text_input("Where are you going?", placeholder="e.g., Paris, Tokyo, New York")
duration = st.sidebar.slider("Number of Days", min_value=1, max_value=14, value=3)
travel_style = st.sidebar.selectbox(
    "Travel Style",
    ["Balanced", "Adventure & Active", "Relaxed & Leisure", "Cultural & Historical", "Family-Friendly"]
)
budget = st.sidebar.selectbox(
    "Budget Level",
    ["Economy", "Moderate", "Luxury"]
)

submit_button = st.sidebar.button("Generate Itinerary ✨")

# Main Content Logic
if submit_button:
    if not destination.strip():
        st.error("Please enter a destination to start planning!")
    else:
        with st.spinner(f"Crafting your perfect {duration}-day itinerary for {destination}..."):
            try:
                # Construct the prompt
                prompt = f"""
                Create a detailed, professional travel itinerary for a {duration}-day trip to {destination}.
                
                Trip Details:
                - Destination: {destination}
                - Duration: {duration} days
                - Travel Style: {travel_style}
                - Budget Level: {budget}
                
                Please structure the response beautifully with the following Markdown format:
                
                ## 🗓️ Trip Overview
                [Provide a quick summary of what makes this trip special based on the travel style and budget]
                
                ## 🗺️ Day-by-Day Itinerary
                ### Day 1: [Catchy Title]
                - **Morning:** [Activity detail]
                - **Afternoon:** [Activity detail]
                - **Evening:** [Activity detail]
                
                [Repeat for all {duration} days]
                
                ## 🍽️ Recommended Dining & Local Eats
                - **Breakfast/Cafes:** [Options]
                - **Lunch/Dinner:** [Options matching the {budget} budget]
                
                ## 💰 Practical Tips & Budget Estimates
                - **Estimated Daily Budget:** [Provide realistic estimate based on {budget} level]
                - **Local Transport Tip:** [Best way to get around]
                - **Packing Essential:** [One must-have item for this specific destination]
                """

                # Call the OpenAI API
                response = client.chat.completions.create(
                    model="gpt-4o",  # Using a reliable, fast model
                    messages=[
                        {"role": "system", "content": "You are an expert travel guide and itinerary planner."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                
                # Extract and display the result
                itinerary_text = response.choices[0].message.content
                
                st.success("🎉 Your personalized itinerary is ready!")
                st.markdown("---")
                st.markdown(itinerary_text)
                st.markdown("---")
                
                # Add a feature to download the text directly
                st.download_button(
                    label="📥 Download Itinerary as Text",
                    data=itinerary_text,
                    file_name=f"{destination.lower().replace(' ', '_')}_itinerary.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error("An error occurred while generating the itinerary.")
                st.exception(e)
else:
    # Default landing screen message
    st.info("👈 Use the sidebar to set up your destination, duration, and travel preferences, then click 'Generate Itinerary'!")
