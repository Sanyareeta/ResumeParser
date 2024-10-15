import streamlit as st
from pyresparser import ResumeParser
import os
import io

# Define the scoring logic
def calculate_resume_score(parsed_data):
    score = 0
    max_score = 100

    # Check for skills
    essential_skills = ['Python', 'Java', 'SQL', 'Machine Learning', 'Communication', 'Leadership']
    skills = parsed_data.get('skills', [])
    skills_match = len(set(essential_skills) & set(skills))

    # Scoring based on skills match
    if skills_match >= 5:
        score += 50  # Skills are highly matched
    elif skills_match >= 3:
        score += 30  # Moderate skill match
    else:
        score += 10  # Poor skill match

    # Check for work experience
    experience = parsed_data.get('total_experience', 0)
    if experience >= 5:
        score += 30  # More than 5 years of experience
    elif experience >= 2:
        score += 20  # Moderate experience
    else:
        score += 10  # Less experience

    # Education check
    education = parsed_data.get('degree', [])
    if education:
        score += 10  # Presence of education is important
    else:
        score += 5   # Education is missing or incomplete

    return score, max_score

# Function to suggest improvements
def suggest_improvements(parsed_data):
    suggestions = []
    
    # Check skills suggestions
    essential_skills = ['Python', 'Java', 'SQL', 'Machine Learning', 'Communication', 'Leadership']
    skills = parsed_data.get('skills', [])
    missing_skills = set(essential_skills) - set(skills)

    if missing_skills:
        suggestions.append(f"Consider learning these skills: {', '.join(missing_skills)}")

    # Work experience suggestion
    experience = parsed_data.get('total_experience', 0)
    if experience < 2:
        suggestions.append("Gain more work experience to improve your resume.")

    # Education suggestion
    education = parsed_data.get('degree', [])
    if not education:
        suggestions.append("Include details about your educational background.")
    
    return suggestions

# Main app
def main():
    st.title("Resume Parser and Enhancer")

    # Upload resume
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    
    if uploaded_file:
        with st.spinner('Parsing your resume...'):
            # Save the uploaded file
            temp_file_path = os.path.join('temp', uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Parse the resume
            parsed_data = ResumeParser(temp_file_path).get_extracted_data()
            
            if parsed_data:
                # Display parsed resume data
                st.subheader("Parsed Resume Data:")
                st.json(parsed_data)
                
                # Calculate the resume score
                score, max_score = calculate_resume_score(parsed_data)
                st.subheader(f"Your Resume Score: {score}/{max_score}")

                # Suggest improvements
                suggestions = suggest_improvements(parsed_data)
                st.subheader("Suggestions to Improve Your Resume:")
                for suggestion in suggestions:
                    st.write(f"- {suggestion}")

            else:
                st.error("Could not parse the resume. Please try again.")

# Run the app
if __name__ == '__main__':
    main()
