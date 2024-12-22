import streamlit as st
import random
import json
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Math Practice Pro",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Salesforce-inspired UI
st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #f3f3f3;
    }
    
    /* Button Styles */
    .stButton > button {
        background-color: #0176d3;
        color: white;
        border-radius: 4px;
        padding: 0.7rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
        border: none;
        box-shadow: 0 2px 4px rgba(1, 118, 211, 0.1);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stButton > button:hover {
        background-color: #014486;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(1, 118, 211, 0.2);
    }
    
    /* Card Styles */
    .question-card {
        background-color: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin: 1rem 0;
        border: 1px solid #e5e5e5;
        transition: all 0.2s ease;
    }
    .question-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Header Styles */
    .main-title {
        color: #032d60;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: left;
        margin: 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e5e5e5;
    }
    
    /* Stats Card Styles */
    .stats-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e5e5e5;
        margin-bottom: 1.5rem;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .stat-item {
        padding: 1rem;
        background-color: #f8f9fd;
        border-radius: 6px;
        border: 1px solid #e5e5e5;
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0176d3;
        margin-bottom: 0.3rem;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #444;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Progress Bar */
    .progress-container {
        margin-top: 1rem;
        padding: 1rem;
        background-color: #f8f9fd;
        border-radius: 6px;
        border: 1px solid #e5e5e5;
    }
    .progress-bar {
        height: 6px;
        background-color: #e5e5e5;
        border-radius: 3px;
        margin: 0.5rem 0;
    }
    .progress-fill {
        height: 100%;
        background-color: #0176d3;
        border-radius: 3px;
        transition: width 0.3s ease;
    }
    
    /* Category Badge */
    .category-badge {
        display: inline-block;
        background-color: #f0f7ff;
        color: #0176d3;
        padding: 0.4rem 0.8rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }
    
    /* Answer Box */
    .answer-box {
        background-color: #f8f9fd;
        padding: 1.2rem;
        border-radius: 6px;
        margin-top: 1rem;
        border: 1px solid #e5e5e5;
    }
    
    /* Input Controls */
    .control-panel {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border: 1px solid #e5e5e5;
    }
    
    /* Pagination */
    .pagination-container {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        border: 1px solid #e5e5e5;
        text-align: center;
    }
    
    /* Performance Indicators */
    .performance-indicator {
        display: inline-block;
        padding: 0.3rem 0.6rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-left: 1rem;
    }
    .performance-good {
        background-color: #ecfbf3;
        color: #1a804c;
    }
    .performance-average {
        background-color: #fff4ec;
        color: #b95000;
    }
    .performance-needs-practice {
        background-color: #fef1f1;
        color: #ba0517;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
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
        questions["addition"].append({
            "question": question,
            "answer": answer,
            "id": f"add_{_}",
            "difficulty": "Easy" if max(num1, num2) < 100 else "Medium" if max(num1, num2) < 1000 else "Hard"
        })

        # Similar pattern for other operations...
        # [Previous code for subtraction, multiplication, and division]
        # Add difficulty ratings based on number sizes

    return questions

# Sidebar with analytics dashboard
with st.sidebar:
    st.markdown("### Analytics Dashboard")
    
    if st.session_state.questions:
        total_questions = len(st.session_state.questions["addition"]) * 4
        attempted = len(st.session_state.attempts)
        progress = (st.session_state.answer_count / total_questions) * 100
        
        # Time tracking
        elapsed_time = datetime.now() - st.session_state.start_time
        minutes = int(elapsed_time.total_seconds() // 60)
        seconds = int(elapsed_time.total_seconds() % 60)
        
        st.markdown("""
            <div class="stats-container">
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-number">{}</div>
                        <div class="stat-label">Total Questions</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{}</div>
                        <div class="stat-label">Questions Attempted</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{}</div>
                        <div class="stat-label">Correct Answers</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{:02d}:{:02d}</div>
                        <div class="stat-label">Time Elapsed</div>
                    </div>
                </div>
                
                <div class="progress-container">
                    <div class="stat-label">Overall Progress</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {}%;"></div>
                    </div>
                    <div style="text-align: right; font-size: 0.9rem; color: #666;">
                        {:.1f}%
                    </div>
                </div>
            </div>
        """.format(
            total_questions,
            attempted,
            st.session_state.correct_answers,
            minutes,
            seconds,
            progress,
            progress
        ), unsafe_allow_html=True)

        # Performance Analysis
        if attempted > 0:
            accuracy = (st.session_state.correct_answers / attempted) * 100
            performance_class = "performance-good" if accuracy >= 80 else "performance-average" if accuracy >= 60 else "performance-needs-practice"
            
            st.markdown(f"""
                <div class="stats-container">
                    <h4>Performance Analysis</h4>
                    <div class="stat-item">
                        <div class="stat-number">{accuracy:.1f}%</div>
                        <div class="stat-label">Accuracy Rate</div>
                        <span class="performance-indicator {performance_class}">
                            {("Excellent" if accuracy >= 80 else "Good" if accuracy >= 60 else "Needs Practice")}
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Main content
st.markdown('<h1 class="main-title">Math Practice Pro</h1>', unsafe_allow_html=True)

# Control Panel
st.markdown('<div class="control-panel">', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    num_questions = st.number_input(
        "Questions per category:",
        min_value=1,
        max_value=100,
        value=10,
        step=1
    )

with col2:
    if st.button("Generate New Set", key="generate"):
        st.session_state.questions = generate_questions(num_questions)
        st.session_state.show_answers = {}
        st.session_state.answer_count = 0
        st.session_state.current_page = 1
        st.session_state.start_time = datetime.now()
        st.session_state.attempts = {}
        st.session_state.correct_answers = 0

st.markdown('</div>', unsafe_allow_html=True)

# Display questions
if st.session_state.questions:
    items_per_page = 10
    total_items = num_questions * 4
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    # Pagination controls
    st.markdown('<div class="pagination-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        page_nums = st.select_slider(
            "Navigate Pages",
            options=list(range(1, total_pages + 1)),
            value=st.session_state.current_page
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.session_state.current_page = page_nums

    # Question display
    start_idx = (st.session_state.current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)

    current_items = []
    for category in ["addition", "subtraction", "multiplication", "division"]:
        for q in st.session_state.questions[category]:
            current_items.append((category, q))

    for idx, (category, item) in enumerate(current_items[start_idx:end_idx]):
        with st.container():
            st.markdown(
                f"""
                <div class="question-card">
                    <span class="category-badge">{category.capitalize()}</span>
                    <p style="font-size: 1.4rem; color: #032d60; margin: 1rem 0; font-weight: 500;">
                        {item['question']}
                    </p>
                """,
                unsafe_allow_html=True
            )
            
            # Answer input and validation
            user_answer = st.text_input(
                "Your answer",
                key=f"input_{item['id']}",
                placeholder="Enter your answer here"
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Check Answer", key=f"check_{item['id']}"):
                    try:
                        user_answer_float = float(user_answer)
                        is_correct = abs(user_answer_float - item['answer']) < 0.01  # Allow small floating point differences
                        st.session_state.attempts[item['id']] = is_correct
                        if is_correct and item['id'] not in st.session_state.show_answers:
                            st.session_state.correct_answers += 1
                    except ValueError:
                        st.error("Please enter a valid number")

            with col2:
                if item['id'] in st.session_state.attempts:
                    if st.session_state.attempts[item['id']]:
                        st.success("Correct! Well done!")
                    else:
                        st.error("Not quite right. Try again or view the answer for help.")
            
            # Show/Hide answer button
            if st.button(
                "Show Answer" if item['id'] not in st.session_state.show_answers else "Hide Answer",
                key=f"btn_{item['id']}"
            ):
                if item['id'] not in st.session_state.show_answers:
                    st.session_state.show_answers[item['id']] = True
                    st.session_state.answer_count += 1
                else:
                    del st.session_state.show_answers[item['id']]
                    st.session_state.answer_count -= 1
            
            # Display answer if show_answer is True
            if item['id'] in st.session_state.show_answers:
                st.markdown(
                    f"""
                    <div class="answer-box">
                        <p style="color: #0176d3; font-weight: 500; margin: 0; font-size: 1.2rem;">
                            Correct Answer: {item['answer']}
                        </p>
                        <p style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">
                            {get_explanation(category, item)}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            st.markdown("</div>", unsafe_allow_html=True)

    # Export functionality
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Export Session", key="export"):
            export_data = {
                "session_info": {
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "total_questions": num_questions * 4,
                    "questions_attempted": len(st.session_state.attempts),
                    "correct_answers": st.session_state.correct_answers,
                    "accuracy_rate": (st.session_state.correct_answers / len(st.session_state.attempts) * 100) if st.session_state.attempts else 0,
                    "completion_rate": (st.session_state.answer_count / (num_questions * 4)) * 100
                },
                "questions": st.session_state.questions,
                "performance": {
                    "attempts": st.session_state.attempts,
                    "viewed_answers": list(st.session_state.show_answers.keys())
                }
            }
            
            st.download_button(
                label="Download Report",
                data=json.dumps(export_data, indent=2),
                file_name=f"math_practice_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def get_explanation(category, item):
    """Generate explanations for different types of math problems."""
    if category == "addition":
        return "Add the numbers together. Break them into smaller parts if needed."
    elif category == "subtraction":
        return "Subtract the second number from the first. Consider borrowing if necessary."
    elif category == "multiplication":
        return "Multiply the numbers. Consider breaking them down if they're large."
    else:  # division
        return "Divide the first number by the second. Round to 2 decimal places if needed."