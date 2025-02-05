# tasks.py
def create_problem_prompt(difficulty, topic):
    return f"""Create a {difficulty.lower()} level coding problem about {topic} following this structured format:

Problem Title
Create an engaging, descriptive title for the problem.

Problem Statement
1. Start with a real-world scenario or practical application when possible
2. Clearly state the task requirements
3. Define all terms and concepts that might be ambiguous
4. Specify any constraints on input values
5. State the expected format of input and output

Input Format
- Describe exactly how input will be provided
- Specify data types and ranges for all inputs
- Include any formatting requirements

Output Format
- Describe exactly what should be returned/printed
- Specify data types and formatting requirements
- Clarify handling of special cases (empty input, error conditions)

Constraints
- Time Complexity: Required Big O notation
- Space Complexity: Required Big O notation
- Input size limits
- Value ranges for all variables
- Any other technical constraints

Example 1
Input: (simple example showing basic case)
Output: (corresponding output)
Explanation: Step-by-step breakdown of how to get from input to output

Example 2
Input: (example showing important edge case)
Output: (corresponding output)
Explanation: Step-by-step breakdown of how to get from input to output

Notes
- Any helpful hints or common pitfalls to watch out for
- Relevant algorithmic concepts or data structures to consider
- Follow-up questions for additional challenge

Requirements:
1. Should test both theoretical understanding and practical coding skills
2. Must have clear edge cases and corner cases
3. Must be unambiguous and well-specified
4. Should match the requested difficulty level: {difficulty}
5. Should focus on the requested topic: {topic}"""

def create_evaluation_prompt(problem, code):
    return f"""Evaluate the following code submission comprehensively:

[Problem]
{problem}

[Submitted Code]
{code}

Provide a detailed evaluation following this structure:

Correctness Analysis
1. Does the solution solve the core problem? (Yes/No)
2. Does it handle all edge cases? (List any missing)
3. Does it meet all stated requirements? (List any violations)
4. Are there any logical errors or bugs? (Provide specific examples)

Technical Implementation
1. Time Complexity: 
   - Analyze the actual Big O complexity
   - Compare against requirements
   - Identify any performance bottlenecks

2. Space Complexity:
   - Analyze the actual space usage
   - Compare against requirements
   - Identify any memory optimization opportunities

3. Code Quality:
   - Variable/function naming
   - Code organization and structure
   - Comments and documentation
   - Adherence to language conventions
   - Error handling
   - Input validation

Scoring
Provide scores out of 10 for each category:
- Correctness: /10
- Efficiency: /10
- Code Quality: /10
- Overall Score: /10

Detailed Feedback
1. Strengths:
   - List specific things done well
   - Highlight clever optimizations or elegant solutions

2. Areas for Improvement:
   - Specific suggestions for better approaches
   - Code snippets demonstrating improvements
   - Explanations of why changes would help

3. Security & Edge Cases:
   - Identify any security vulnerabilities
   - List untested edge cases
   - Suggest additional test cases

Keep feedback constructive and actionable, with specific examples and explanations."""
    
def create_explanation_prompt(evaluation_result):
    return f"""Based on the code evaluation:
{evaluation_result}

Provide a comprehensive solution analysis report retrieved from Principal Software Engineer & Technical Lead Agent following the format defined in create_evaluation_prompt.
Provide a comprehensive educational explanation following this structure:

Solution Approaches
Compare the provided solution to the optimal approach and guide user how the code can be optimized for better performance.
1. Optimal Approach
   - End to end code Implementation
   - Time/Space complexity
   - Key optimizations
   

2. Alternative Approaches
   - Other valid solutions
   - Trade-offs between approaches
   - When each approach might be preferred

Common Mistakes
1. Typical errors to avoid
2. Performance pitfalls
3. Edge cases often missed

Best Practices
1. Code organization tips
2. Naming conventions
3. Error handling patterns
4. Documentation guidelines


Make explanations clear and accessible while maintaining technical depth.
Use analogies and visualizations where helpful.
Include code examples for key concepts."""


def create_feedback_report_prompt(evaluation_result, explanation_result):
    return f"""Based on the code evaluation and optimization explanation:

Evaluation Results:
{evaluation_result}

Optimization Explanation:
{explanation_result}

Create comprehensive feedback report following this structure:

1. **Solution Evaluation**
   - **Correctness:** Evaluate if the solution meets the problem requirements. Deduct points for any inaccuracies.
   - **Efficiency:** Assess time and space complexity. Deduct points if performance can be improved.
   - **Test Cases:** Report on the status of test cases and deduct points for any failures.
   - **Code Quality:** Evaluate code readability, structure, and adherence to best practices.
   - **Overall Score:** Provide an overall score out of 10.
     - **If the overall score is 7/10 or higher:** Generate a fun and engaging congratulatory message that encourages the user, using playful language, emojis, and light-hearted jokes.
     - **If the overall score is below 7/10:** Generate a playful insult that is light-hearted and humorous (e.g., "Looks like your code took a nap on the job—time to wake it up!") while still offering encouragement to improve.

2. Key Strengths:
   - List main positive aspects identified in the evaluation of the code.


3. Areas for Improvement:
   - List critical issues found in the code evaluation and mention areas for improvement.

Performance Analysis
1. Time Complexity: Current vs Expected
2. Space Complexity: Current vs Expected
3. Key Performance Bottlenecks

Optimization Recommendations
1. High-Priority Improvements
   - List immediate optimization opportunities.
   - Include relevant code examples.
2. Advanced Optimization Techniques
   - Suggested algorithmic improvements
   - Data structure optimizations

Learning Resources
1. Recommended practice problems
2. Relevant concepts to review
3. Helpful documentation links

Keep the report focused and actionable, highlighting the most important feedback points."""
