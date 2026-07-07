import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="Crew Text Gen", page_icon="🚀", layout="centered")
st.title("🚀 The Crew's Chat & Email Generator")
st.write("Turn your messy thoughts into clean, ready-to-send messages.")

# 2. Sidebar Settings (Customizations)
st.sidebar.header("⚙️ Generation Settings")
msg_type = st.sidebar.selectbox("Message Type", ["Email", "WhatsApp/Chat", "Formal Letter"])
tone = st.sidebar.selectbox("Vibe/Tone", ["Professional", "Casual & Warm", "Direct & Short", "Saudi Slang (العامية)"])

# 3. Secure API Key Input (You can hardcode this or use Streamlit Secrets later)
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# 4. Main User Input
context = st.text_area("What do you want to say? (Just write bullet points or raw thoughts)", 
                       placeholder="e.g., Tell my boss I'm sick today but will check urgent emails.")

# 5. The Magic Button
if st.button("✨ Generate Text"):
    if not api_key:
        st.error("Please enter your OpenAI API Key in the sidebar first!")
    elif not context:
        st.warning("Write something in the text area first!")
    else:
        with st.spinner("Writing your message..."):
            try:
                # Initialize OpenAI client
                client = OpenAI(api_key=api_key)
                
                # Crafting the system prompt based on selections
                system_prompt = f"You are an expert copywriter. Write a {msg_type} based on the user's notes. The tone must be strictly {tone}."
                
                # API Call
                response = client.chat.completions.create(
                    model="gpt-4o-mini", # Fast and cheap model
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": context}
                    ]
                )
                
                # Display Result
                generated_text = response.choices[0].message.content
                st.success("🎉 Done! Copy the text below:")
                st.text_area("Result", value=generated_text, height=250)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
