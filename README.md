# Talent-Scout-Assistant

TalentScout — Hiring Assistant 🤖

TalentScout is an AI-powered hiring assistant built with Streamlit.
It helps recruiters by:

Collecting candidate details

Generating 3–5 tailored technical interview questions for each declared technology

Allowing candidates to answer questions interactively

Saving candidate data, questions, and answers for review

 Features

 Candidate information form (name, email, phone, experience, etc.)

 AI-powered mode (LLaMA local model) for generating diverse interview questions

 Fast fallback mode (template-based questions) when LLaMA is unavailable

 Modern, styled Streamlit UI with sidebar form and question cards

 Save candidate responses to JSON for recruiter review

 Debug expander to view session state

📂 Project Structure
├── app.py                 # Main Streamlit app
├── candidate_data.json    # Saved candidate data (auto-generated)
└── README.md              # Documentation

🔧 Requirements

Python 3.9+

Install dependencies:

pip install streamlit llama-cpp-python

▶ Usage

Clone the repo or copy app.py

Run the Streamlit app:

streamlit run app.py


Open the app in your browser (default: http://localhost:8501)

⚙ Configuration

LLM model: Update MODEL_PATH in app.py with your local .gguf file:

MODEL_PATH = r"C:\path\to\your\llama_model.gguf"


Toggle AI mode in the sidebar to use LLaMA (if installed).

 Example Flow

Enter candidate details and tech stack in the sidebar.

Click Generate Questions.

In fallback mode → 3 simple template questions per tech

In AI mode (LLaMA) → diverse, challenging 3–5 questions per tech

Candidate writes answers directly in the app.

Click Submit Answers → data is saved to candidate_data.json.

 UI Highlights

Sidebar for candidate info

Tabs for Form and Interview Questions

Modern card-style design for questions

Blue accent theme with hover effects
