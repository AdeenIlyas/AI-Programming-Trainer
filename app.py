import streamlit as st
from crewai import Task, Crew
from agents import get_problem_generator, get_code_evaluator, get_solution_explainer, get_feedback_reporter
from tasks import create_problem_prompt, create_evaluation_prompt, create_explanation_prompt, create_feedback_report_prompt
from history import init_history, add_history_item, get_history
from code_runner import check_code_syntax, execute_code

def clear_execution_state():
    """Clear execution-related session state variables"""
    if 'executing' in st.session_state:
        del st.session_state.executing
    if 'execution_result' in st.session_state:
        del st.session_state.execution_result

def main():
    st.title("AI Coding Interviewer ֎")
    st.markdown("Practice coding interviews with AI-powered feedback!")

    # Apply CSS to ensure button text stays in a single line
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] button {
            white-space: nowrap !important;
            width: auto !important;
            padding: 6px 15px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize chat history
    init_history()

    # Sidebar for settings and chat history review
    with st.sidebar:
        st.header("Settings")
        difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"], index=1)
        topic = st.selectbox("Select Topic", ["Arrays", "Graphs", "Dynamic Programming", "Sorting", "Strings", "Data Structures and Algorithms"], index=0)

        st.header("Chat History")
        history = get_history()
        if history:
            for idx, item in enumerate(history):
                if st.button(f"View {idx+1}: {item['title']}", key=f"history_{idx}"):
                    st.session_state['selected_history'] = item['content']
        else:
            st.write("No history yet.")

    # Display selected chat history if available
    if 'selected_history' in st.session_state:
        st.subheader("Selected Chat History")
        st.markdown(st.session_state['selected_history'])

    # Layout: Three columns for generating problem, code editor, and output
    col1, col2, col3 = st.columns([1, 1, 1])

    # Column 1: Problem Generation
    with col1:
        if st.button("Generate New Problem"):
            with st.spinner("Creating challenge..."):
                problem_generator = get_problem_generator()
                problem_prompt = create_problem_prompt(difficulty, topic)
                problem_task = Task(
                    description=problem_prompt,
                    expected_output="A comprehensive, well-structured coding problem following the specified format",
                    agent=problem_generator
                )
                crew = Crew(
                    agents=[problem_generator],
                    tasks=[problem_task],
                    verbose=True
                )
                generated_problem = crew.kickoff()
                st.session_state.generated_problem = generated_problem
                st.session_state.user_code = ""
                add_history_item("Generated Problem", generated_problem)

        if 'generated_problem' in st.session_state and st.session_state.generated_problem:
            st.subheader("Coding Challenge")
            st.markdown(st.session_state.generated_problem)

    # Column 2: Code Submission & Language Selection
    with col2:
        if 'generated_problem' in st.session_state and st.session_state.generated_problem:
            st.subheader("Write Your Solution")

            # Language selection
            language = st.selectbox(
                "Select Programming Language",
                ["Python", "C++", "Java"],
                key="language_selector"
            )

            # Initialize code editor with placeholder text if no code is entered yet
            if 'user_code' not in st.session_state:
                st.session_state.user_code = ""

            placeholder_text = {
                "Python": "def solution():\n    # Write your code here\n    pass",
                "C++": "#include <iostream>\nusing namespace std;\n\nint main() {\n    // Write your code here\n    return 0;\n}",
                "Java": "public class Solution {\n    public static void main(String[] args) {\n        // Write your code here\n    }\n}"
            }

            st.session_state.user_code = st.text_area(
                "Code Editor",
                value=st.session_state.user_code if st.session_state.user_code else placeholder_text[language],
                height=400,
                key="code_editor"
            )

            # Buttons for syntax checking and submission
            col2_buttons = st.columns([1, 1])
            with col2_buttons[0]:
                if st.button("Check Syntax"):
                    with st.spinner("Checking syntax..."):
                        syntax_result = check_code_syntax(
                            st.session_state.user_code,
                            language.lower()
                        )
                        if syntax_result['success']:
                            st.success(syntax_result.get('message', "Syntax check passed!"))
                        else:
                            st.error(syntax_result['error'])

            with col2_buttons[1]:
                if st.button("Submit Solution"):
                    st.session_state.analyzing = True

    # Column 3: Code Execution Output
    with col3:
        st.subheader("Code Output")

        # Buttons to run code and clear output
        button_container = st.container()
        with button_container:
            left_col, right_col = st.columns(2)
            with left_col:
                run_clicked = st.button("Run Code", key="run_code", use_container_width=True)
            with right_col:
                clear_clicked = st.button("Clear Output", key="clear_output", use_container_width=True)

        st.write("")

        if run_clicked:
            st.session_state.executing = True
            # Execute only the code provided by the user in the text area
            st.session_state.execution_result = execute_code(
                st.session_state.user_code,
                language.lower()
            )

        if clear_clicked:
            clear_execution_state()

        if 'execution_result' in st.session_state:
            if st.session_state.execution_result['success']:
                st.code(
                    st.session_state.execution_result['output'],
                    language=language.lower()
                )
            else:
                st.error(st.session_state.execution_result['error'])

        if 'executing' in st.session_state:
            del st.session_state.executing

    # Feedback Report Section (spanning columns 2 and 3)
    if 'analyzing' in st.session_state and st.session_state.analyzing:
        feedback_container = st.container()
        with feedback_container:
            cols = st.columns([1, 2])
            with cols[1]:
                with st.spinner("Analyzing your code..."):
                    evaluator = get_code_evaluator()
                    explainer = get_solution_explainer()

                    evaluation_task = Task(
                        description=create_evaluation_prompt(
                            st.session_state.generated_problem,
                            st.session_state.user_code
                        ),
                        expected_output="Detailed code evaluation report following the specified format including submitted code score /10 and feedback",
                        agent=evaluator,
                        allow_delegation=True
                    )

                    explanation_task = Task(
                        description=create_explanation_prompt("[evaluation_result]"),
                        expected_output="Comprehensive educational explanation following the specified format",
                        agent=explainer,
                        dependencies=[evaluation_task]
                    )

                    reporter = get_feedback_reporter()
                    feedback_task = Task(
                        description=create_feedback_report_prompt(
                            "[evaluation_result]",
                            "[explanation_result]"
                        ),
                        expected_output="Concise feedback report combining evaluation and optimization insights",
                        agent=reporter,
                        dependencies=[evaluation_task, explanation_task]
                    )
                    crew = Crew(
                        agents=[evaluator, explainer, reporter],
                        tasks=[evaluation_task, explanation_task, feedback_task],
                        verbose=True
                    )

                    results = crew.kickoff()
                    st.markdown(results)
                    st.session_state.analyzing = False

if __name__ == "__main__":
    main()
