# app.py
import streamlit as st
import json
import time

# Try to import llama; if not installed, we'll use fallback questions
try:
    from llama_cpp import Llama
    HAVE_LLAMA = True
except Exception:
    HAVE_LLAMA = False

# === CONFIG ===
MODEL_PATH = r"C:\Users\HONER\Downloads\dolphin3.0-llama3.2-3b-q4_k_m.gguf"  # update if needed
LLM_CTX = 1024
LLM_THREADS = 4

# Lazily load model
_llm = None
def load_llm():
    global _llm
    if not HAVE_LLAMA:
        return None
    if _llm is None:
        with st.spinner("Loading local LLaMA model (this may take 5–30s)..."):
            _llm = Llama(
                model_path=MODEL_PATH,
                n_ctx=LLM_CTX,
                n_threads=LLM_THREADS,
                verbose=False
            )
    return _llm

# === QUESTION GENERATORS ===
def generate_questions_fallback(tech_list):
    """Deterministic fast fallback: 3 template Qs per tech"""
    questions = {}
    for tech in tech_list:
        base = tech.strip().split()[0].capitalize()
        questions[tech] = [
            f"Explain a core concept of {base}.",
            f"Describe a real-world use case of {base}.",
            f"Give a short code example using {base}."
        ]
    if not questions:
        questions["General"] = [
            "Tell us about a project where you applied your main tech stack."
        ]
    return questions

def generate_questions_with_llm(tech_list, max_tokens=300):
    """Use LLaMA to generate 3–5 diverse questions per tech"""
    llm = load_llm()
    if llm is None:
        return generate_questions_fallback(tech_list)

    techs_str = ", ".join(tech_list)
    prompt = (
        f"You are an interviewer. For each of these technologies: {techs_str}, "
        f"generate 3 to 5 diverse, practical technical interview questions. "
        "Keep them short, clear, and challenging.\n\n"
        "Format:\n"
        "Technology: <name>\n"
        "- Question 1\n"
        "- Question 2\n"
        "...\n\n"
    )

    try:
        resp = llm(prompt, max_tokens=max_tokens, temperature=0.7)
        text = resp["choices"][0]["text"].strip()
    except Exception as e:
        st.warning(f"LLM call failed: {e}")
        return generate_questions_fallback(tech_list)

    # Parse text into dict
    parsed = {}
    current_tech = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith("technology:"):
            current_tech = line.split(":", 1)[1].strip()
            parsed[current_tech] = []
        elif line.startswith("-") and current_tech:
            parsed[current_tech].append(line.lstrip("- ").strip())

    if not parsed:
        return generate_questions_fallback(tech_list)
    return parsed

# === SAVE UTILITY ===
def save_candidate(candidate_info, questions, answers, filename="candidate_data.json"):
    obj = {
        "candidate_info": candidate_info,
        "questions": questions,
        "answers": answers,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    return filename

# === STREAMLIT UI CONFIG ===
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #f8f9fb;
    }
    .main {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    .stTextInput, .stTextArea {
        border-radius: 10px !important;
        border: 1px solid #ddd !important;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 12px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #357ab7;
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header / Branding ---
st.markdown("<h1 style='text-align: center;'>🤖 TalentScout — Hiring Assistant</h1>", unsafe_allow_html=True)
st.write("")

# === Session state ===
if "candidate" not in st.session_state:
    st.session_state.candidate = None
if "questions" not in st.session_state:
    st.session_state.questions = {}
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "generated" not in st.session_state:
    st.session_state.generated = False

# === Sidebar: Candidate Info ===
with st.sidebar:
    st.header("📋 Candidate Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    years = st.text_input("Years of Experience")
    position = st.text_input("Desired Position(s)")
    location = st.text_input("Current Location")
    tech_stack_raw = st.text_input("Tech Stack (comma-separated, e.g., Python, SQL, Django)")
    use_llm = st.toggle("⚡ Use AI Mode (LLaMA)", value=HAVE_LLAMA)

# === Main Tabs ===
tab1, tab2 = st.tabs(["📝 Candidate Form", "❓ Interview Questions"])

with tab1:
    if st.button("Generate Questions"):
        tech_stack_raw = tech_stack_raw or ""
        tech_list = [t.strip() for t in tech_stack_raw.split(",") if t.strip()]

        if not tech_list:
            st.error("Please enter your tech stack (comma-separated). Example: `Python, SQL, Django`")
        else:
            st.session_state.candidate = {
                "full_name": name,
                "email": email,
                "phone": phone,
                "years_experience": years,
                "desired_positions": position,
                "location": location,
                "tech_stack_list": tech_list
            }

            with st.spinner("Generating questions..."):
                if use_llm and HAVE_LLAMA:
                    load_llm()
                    questions = generate_questions_with_llm(tech_list)
                else:
                    questions = generate_questions_fallback(tech_list)

                # Ensure each tech has at least 3 questions
                for t in tech_list:
                    if not questions.get(t):
                        questions[t] = generate_questions_fallback([t])[t]

                st.session_state.questions = questions
                st.session_state.answers = {t: [""] * len(questions[t]) for t in questions}
                st.session_state.generated = True
                st.success("Questions generated — check the 'Interview Questions' tab.")

with tab2:
    if st.session_state.generated and st.session_state.questions:
        st.markdown("## Generated Questions")
        for tech, q_list in st.session_state.questions.items():
            st.markdown(f"### {tech}")
            for i, q in enumerate(q_list, start=1):
                st.markdown(f"""
                    <div style="
                        background:#ffffff;
                        padding:1rem;
                        border-radius:12px;
                        margin-bottom:1rem;
                        border-left: 6px solid #4a90e2;
                        box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
                    ">
                        <p style="color:#2c3e50; font-size:16px; font-weight:500; margin:0;">
                            <b>Q{i}:</b> {q}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                key = f"{tech}__q{i}"
                st.session_state.answers[tech][i-1] = st.text_area(
                    "Your Answer",
                    value=st.session_state.answers[tech][i-1],
                    key=key
                )

        if st.button("Submit Answers"):
            if not st.session_state.candidate:
                st.error("Candidate details missing — please fill the form again and generate questions.")
            else:
                fname = save_candidate(
                    st.session_state.candidate,
                    st.session_state.questions,
                    st.session_state.answers
                )
                st.success(f"✅ Saved to {fname}")
                st.balloons()

# Debug helper
with st.expander("🔧 Debug Info"):
    st.write("HAVE_LLAMA:", HAVE_LLAMA)
    st.write("Candidate:", st.session_state.candidate)
    st.write("Questions:", st.session_state.questions)
    st.write("Answers (current):", st.session_state.answers)
