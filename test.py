import streamlit as st
import random
import json

# Function to generate random questions
def generate_questions(num_questions):
    questions = {
        "addition": [],
        "subtraction": [],
        "multiplication": [],
        "division": []
    }

    for _ in range(num_questions):
        # Addition
        num1 = random.randint(1, 10**random.randint(1, 4))
        num2 = random.randint(1, 10**random.randint(1, 4))
        question = f"{num1} + {num2} = ?"
        answer = num1 + num2
        questions["addition"].append({"question": question, "answer": answer})

        # Subtraction
        num1 = random.randint(1, 10**random.randint(1, 4))
        num2 = random.randint(1, num1)
        question = f"{num1} - {num2} = ?"
        answer = num1 - num2
        questions["subtraction"].append({"question": question, "answer": answer})

        # Multiplication
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        question = f"{num1} × {num2} = ?"
        answer = num1 * num2
        questions["multiplication"].append({"question": question, "answer": answer})

        # Division
        num1 = random.randint(1, 10000)
        num2 = random.randint(1, 100)
        while num2 == 0:
            num2 = random.randint(1, 100)
        question = f"{num1} ÷ {num2} = ?"
        answer = round(num1 / num2, 2)
        questions["division"].append({"question": question, "answer": answer})

    return questions

# Streamlit UI
st.title("Math Question Generator")
st.markdown("Generate random math questions for addition, subtraction, multiplication, and division.")

# Input for the number of questions
num_questions = st.number_input(
    "Number of questions to generate:",
    min_value=1,
    max_value=10000,
    value=10,
    step=1
)

# Generate button
if st.button("Generate Questions"):
    st.write("Generating questions...")
    questions = generate_questions(num_questions)

    # Display questions in UI
    st.subheader("Generated Questions (Preview)")
    st.write("Here are the first few questions from each category:")
    
    for category, q_list in questions.items():
        st.markdown(f"**{category.capitalize()}**")
        for item in q_list[:5]:  # Show only the first 5 questions per category
            st.write(f"- {item['question']}")

    # Save to JSON for download
    filename = "math_questions.json"
    json_data = json.dumps(questions, indent=4)
    
    # Download button
    st.download_button(
        label="Download All Questions as JSON",
        data=json_data,
        file_name=filename,
        mime="application/json"
    )
