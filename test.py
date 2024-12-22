import streamlit as st
import random
import json
from datetime import datetime
import math

# Set page configuration
st.set_page_config(
    page_title="Math Practice Pro",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# [Previous CSS styles remain the same]

# Add operation button styles
st.markdown("""
    <style>
    /* Previous styles remain... */
    
    .operation-button {
        background-color: white;
        border: 1px solid #0176d3;
        color: #0176d3;
        padding: 0.5rem 1rem;
        margin: 0.5rem;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-weight: 500;
    }
    .operation-button:hover {
        background-color: #0176d3;
        color: white;
    }
    .operation-button.active {
        background-color: #0176d3;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_operation' not in st.session_state:
    st.session_state.current_operation = "addition"
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'show_answers' not in st.session_state:
    st.session_state.show_answers = {}
if 'answer_count' not in st.session_state:
    st.session_state.answer_count = 0
if 'questions' not in st.session_state:
    st.session_state.questions = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()
if 'attempts' not in st.session_state:
    st.session_state.attempts = {}
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'category_stats' not in st.session_state:
    st.session_state.category_stats = {
        "addition": {"attempted": 0, "correct": 0},
        "subtraction": {"attempted": 0, "correct": 0},
        "multiplication": {"attempted": 0, "correct": 0},
        "division": {"attempted": 0, "correct": 0}
    }

def generate_questions(num_questions):
    """Generate questions with improved number ranges."""
    questions = {
        "addition": [],
        "subtraction": [],
        "multiplication": [],
        "division": []
    }
    
    for i in range(num_questions):
        # Addition (larger numbers)
        num1 = random.randint(10, 1000)
        num2 = random.randint(10, 1000)
        questions["addition"].append({
            "question": f"{num1:,} + {num2:,} = ?",
            "answer": num1 + num2,
            "id": f"add_{i}",
            "num1": num1,
            "num2": num2,
            "number": i + 1
        })

        # Subtraction (ensuring positive results)
        num1 = random.randint(100, 1000)
        num2 = random.randint(1, num1)
        questions["subtraction"].append({
            "question": f"{num1:,} - {num2:,} = ?",
            "answer": num1 - num2,
            "id": f"sub_{i}",
            "num1": num1,
            "num2": num2,
            "number": i + 1
        })

        # Multiplication (reasonable numbers)
        num1 = random.randint(2, 50)
        num2 = random.randint(2, 30)
        questions["multiplication"].append({
            "question": f"{num1:,} × {num2:,} = ?",
            "answer": num1 * num2,
            "id": f"mul_{i}",
            "num1": num1,
            "num2": num2,
            "number": i + 1
        })

        # Division (clean divisions)
        num2 = random.randint(2, 12)
        num1 = num2 * random.randint(1, 20)
        questions["division"].append({
            "question": f"{num1:,} ÷ {num2:,} = ?",
            "answer": num1 / num2,
            "id": f"div_{i}",
            "num1": num1,
            "num2": num2,
            "number": i + 1
        })

    return questions

def update_stats(category, is_correct, question_id):
    """Update statistics accurately."""
    if question_id not in st.session_state.attempts:
        st.session_state.category_stats[category]["attempted"] += 1
        if is_correct:
            st.session_state.category_stats[category]["correct"] += 1
            st.session_state.correct_answers += 1

def render_operation_buttons():
    """Render operation selection buttons."""
    operations = {
        "addition": "Addition",
        "subtraction": "Subtraction",
        "multiplication": "Multiplication",
        "division": "Division"
    }
    
    st.markdown('<div style="display: flex; justify-content: center; gap: 1rem;">', unsafe_allow_html=True)
    
    cols = st.columns(4)
    for idx, (op_key, op_name) in enumerate(operations.items()):
        with cols[idx]:
            if st.button(
                op_name,
                key=f"op_{op_key}",
                help=f"Switch to {op_name} questions",
                use_container_width=True
            ):
                st.session_state.current_operation = op_key
                st.session_state.current_page = 1

def calculate_stats():
    """Calculate current statistics."""
    stats = {
        'total_questions': len(st.session_state.questions[st.session_state.current_operation]),
        'attempted': st.session_state.category_stats[st.session_state.current_operation]["attempted"],
        'correct': st.session_state.category_stats[st.session_state.current_operation]["correct"]
    }
    stats['accuracy'] = (stats['correct'] / stats['attempted'] * 100) if stats['attempted'] > 0 else 0
    return stats

# Main content
st.markdown('<h1 class="main-title">Math Practice Pro</h1>', unsafe_allow_html=True)

# Control Panel
with st.container():
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        num_questions = st.number_input(
            "Number of questions per category:",
            min_value=1,
            max_value=500,
            value=10,
            step=1
        )

    with col2:
        if st.button("Generate New Questions", key="generate"):
            st.session_state.questions = generate_questions(num_questions)
            st.session_state.show_answers = {}
            st.session_state.answer_count = 0
            st.session_state.current_page = 1
            st.session_state.start_time = datetime.now()
            st.session_state.attempts = {}
            st.session_state.correct_answers = 0
            st.session_state.category_stats = {
                category: {"attempted": 0, "correct": 0}
                for category in ["addition", "subtraction", "multiplication", "division"]
            }
    st.markdown('</div>', unsafe_allow_html=True)

# Operation buttons
render_operation_buttons()

# Display questions
if st.session_state.questions:
    # Get questions for current operation
    current_questions = st.session_state.questions[st.session_state.current_operation]
    items_per_page = 10
    total_pages = math.ceil(len(current_questions) / items_per_page)
    
    # Calculate page range
    start_idx = (st.session_state.current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(current_questions))
    
    # Navigation buttons
    cols = st.columns([1, 2, 1])
    with cols[0]:
        if st.button("← Previous") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            
    with cols[2]:
        if st.button("Next →") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            
    with cols[1]:
        st.markdown(f"<div style='text-align: center'>Page {st.session_state.current_page} of {total_pages}</div>", 
                   unsafe_allow_html=True)

    # Display current page questions
    for item in current_questions[start_idx:end_idx]:
        with st.container():
            st.markdown(f"""
                <div class="question-card">
                    <div class="question-number">Question {item['number']}</div>
                    <p style="font-size: 1.4rem; color: #032d60; margin: 1rem 0; font-weight: 500;">
                        {item['question']}
                    </p>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])
            with col1:
                user_answer = st.text_input(
                    "Your answer",
                    key=f"input_{item['id']}",
                    placeholder="Enter your answer"
                )
            
            with col2:
                check_button = st.button("Check", key=f"check_{item['id']}")
                show_answer = st.button(
                    "Show Answer" if item['id'] not in st.session_state.show_answers else "Hide Answer",
                    key=f"show_{item['id']}"
                )

            # Handle answer checking
            if check_button and user_answer:
                try:
                    user_float = float(user_answer.replace(',', ''))
                    is_correct = abs(user_float - item['answer']) < 0.01
                    update_stats(st.session_state.current_operation, is_correct, item['id'])
                    st.session_state.attempts[item['id']] = is_correct
                    
                    if is_correct:
                        st.markdown(
                            '<div class="success-message">✨ Correct! Well done!</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            '<div class="error-message">Not quite right. Try again!</div>',
                            unsafe_allow_html=True
                        )
                except ValueError:
                    st.markdown(
                        '<div class="error-message">Please enter a valid number</div>',
                        unsafe_allow_html=True
                    )

            # Handle show/hide answer
            if show_answer:
                if item['id'] not in st.session_state.show_answers:
                    st.session_state.show_answers[item['id']] = True
                else:
                    del st.session_state.show_answers[item['id']]

            # Display answer if shown
            if item['id'] in st.session_state.show_answers:
                st.markdown(f"""
                    <div class="answer-box">
                        <p style="color: #0176d3; font-weight: 500; margin: 0; font-size: 1.2rem;">
                            Answer: {item['answer']:,}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

# Sidebar with statistics
with st.sidebar:
    if st.session_state.questions:
        elapsed_time = datetime.now() - st.session_state.start_time
        minutes = int(elapsed_time.total_seconds() // 60)
        seconds = int(elapsed_time.total_seconds() % 60)
        
        stats = calculate_stats()
        
        st.markdown(f"""
            <div class="stats-container">
                <h3 style="color: #032d60; margin-bottom: 1rem;">
                    {st.session_state.current_operation.capitalize()} Statistics
                </h3>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-number">{stats['attempted']}/{stats['total_questions']}</div>
                        <div class="stat-label">Questions Attempted</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{stats['correct']}</div>
                        <div class="stat-label">Correct Answers</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{stats['accuracy']:.1f}%</div>
                        <div class="stat-label">Accuracy</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{minutes:02d}:{seconds:02d}</div>
                        <div class="stat-label">Time Elapsed</div>
                    </div>
                </div>
            </div>
            
            <div class="stats-container">
                <h3 style="color: #032d60; margin-bottom: 1rem;">Category Overview</h3>
        """, unsafe_allow_html=True)
        
        for category in ["addition", "subtraction", "multiplication", "division"]:
            attempted = st.session_state.category_stats[category]["attempted"]
            correct = st.session_state.category_stats[category]["correct"]
            accuracy = (correct / attempted * 100) if attempted > 0 else 0
            
            st.markdown(f"""
                <div style="margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 500;">{category.capitalize()}</span>
                        <span>{accuracy:.1f}%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {accuracy}%;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #666;">
                        <span>Attempted: {attempted}</span>
                        <span>Correct: {correct}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)