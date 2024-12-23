import streamlit as st
import random
import json
import base64
import pandas as pd
from datetime import datetime

def generate_numbers(digits=2):
    """Generate random numbers with specified number of digits"""
    min_num = 10 ** (digits - 1)
    max_num = (10 ** digits) - 1
    return random.randint(min_num, max_num)

def generate_question(operation):
    """Generate a math question based on the operation"""
    num1 = generate_numbers()
    num2 = generate_numbers()
    
    if operation == 'multiplication':
        answer = num1 * num2
        symbol = '×'
    elif operation == 'addition':
        answer = num1 + num2
        symbol = '+'
    elif operation == 'subtraction':
        # Make sure the result is positive
        num1, num2 = max(num1, num2), min(num1, num2)
        answer = num1 - num2
        symbol = '-'
    else:  # division
        # Make sure division results in a whole number
        answer = random.randint(1, 99)
        num2 = random.randint(1, 99)
        num1 = answer * num2
        symbol = '÷'
    
    question = f"{num1} {symbol} {num2}"
    return {
        'question': question,
        'num1': num1,
        'num2': num2,
        'operation': operation,
        'answer': answer
    }

def generate_bulk_questions(operation, count=500):
    """Generate multiple questions"""
    return [generate_question(operation) for _ in range(count)]

def get_download_link(data, filename, text):
    """Generate a download link for the data"""
    json_str = json.dumps(data, indent=2)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="{filename}">{text}</a>'
    return href

def main():
    st.title("Math Practice Generator")
    
    # Add CSS to center align text and make it bigger
    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Operation selection
    operation = st.selectbox(
        "Choose operation",
        ['multiplication', 'addition', 'subtraction', 'division']
    )
    
    # Two modes: Single question practice and Bulk generation
    mode = st.radio("Select mode", ["Practice Mode", "Bulk Generation"])
    
    if mode == "Practice Mode":
        # Session state initialization
        if 'question' not in st.session_state:
            st.session_state.question = ''
            st.session_state.answer = 0
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.questions_attempted = []  # Track all attempted questions
        
        # Display progress metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Questions Completed", len(st.session_state.questions_attempted))
        with col2:
            st.metric("Correct Answers", st.session_state.score)
        with col3:
            accuracy = (st.session_state.score / max(len(st.session_state.questions_attempted), 1)) * 100
            st.metric("Accuracy", f"{accuracy:.1f}%")
        
        # Generate new question button
        if st.button("Generate New Question"):
            question_data = generate_question(operation)
            st.session_state.question = question_data['question']
            st.session_state.answer = question_data['answer']
            st.session_state.user_answer = ''
        
        # Display question
        if st.session_state.question:
            st.markdown(f'<p class="big-font">{st.session_state.question} = ?</p>', unsafe_allow_html=True)
            
            # Get user answer
            user_answer = st.text_input("Your answer:", key='user_answer')
            
            # Check answer button
            if st.button("Check Answer"):
                try:
                    user_answer = int(user_answer)
                    # Track the question and response
                    question_data = {
                        'question': st.session_state.question,
                        'user_answer': user_answer,
                        'correct_answer': st.session_state.answer,
                        'is_correct': user_answer == st.session_state.answer
                    }
                    st.session_state.questions_attempted.append(question_data)
                    
                    if user_answer == st.session_state.answer:
                        st.success("Correct! 🎉")
                        st.session_state.score += 1
                    else:
                        st.error(f"Wrong! The correct answer is {st.session_state.answer}")
                    
                    # Show recent questions
                    if len(st.session_state.questions_attempted) > 0:
                        st.subheader("Recent Questions")
                        recent_df = pd.DataFrame(st.session_state.questions_attempted[-5:])  # Show last 5 questions
                        st.dataframe(recent_df.assign(
                            Result=recent_df.is_correct.map({True: '✅', False: '❌'})
                        )[['question', 'user_answer', 'correct_answer', 'Result']])
                    
                except ValueError:
                    st.error("Please enter a valid number")
    
    else:  # Bulk Generation mode
        st.header("Bulk Question Generator")
        
        # Number of questions selector
        num_questions = st.slider("Number of questions to generate", 10, 500, 500)
        
        if st.button("Generate Questions"):
            # Generate questions
            questions = generate_bulk_questions(operation, num_questions)
            
            # Create download links
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"math_questions_{operation}_{timestamp}.json"
            
            # Display download link
            st.markdown(
                get_download_link(questions, filename, "📥 Download Questions (JSON)"),
                unsafe_allow_html=True
            )
            
            # Display preview
            st.subheader("Preview of Generated Questions")
            preview_df = pd.DataFrame(questions[:5])  # Show first 5 questions
            st.dataframe(preview_df)
            
            # Display statistics
            st.subheader("Question Statistics")
            st.write(f"Total questions generated: {len(questions)}")
            if operation == 'multiplication':
                avg_answer = sum(q['answer'] for q in questions) / len(questions)
                st.write(f"Average answer: {avg_answer:.2f}")
    
 

if __name__ == "__main__":
    main()