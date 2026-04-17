🧠 AI Resume Screening System with Tracing

An AI-powered Resume Screening System that evaluates candidates based on a given job description using LLM pipelines. Built using LangChain and traced with LangSmith for transparency and debugging.

🚀 Objective
Build an AI system to evaluate resumes against a job description
Implement modular LLM pipelines using LangChain
Provide scoring (0–100) and explainable outputs
Use LangSmith for tracing and debugging
⚙️ Tech Stack
Python
LangChain (LCEL)
Groq API (LLM)
LangSmith (Tracing & Debugging)
dotenv for environment management
🧩 System Architecture
Resume → Skill Extraction → Matching → Scoring → Explanation

Each stage is implemented as a modular chain using LangChain.

📂 Project Structure
resume_screening/
│
├── prompts/        # Prompt templates
├── chains/         # LangChain pipeline components
├── data/           # Resume + Job Description
├── outputs/        # Generated results (JSON + TXT)
├── utils/          # LLM setup
├── main.py         # Pipeline execution


🔄 Pipeline Flow
1. Skill Extraction
Extracts:
Skills
Tools
Experience
Uses structured JSON output
2. Matching
Compares resume with job description
Outputs:
matched_skills
missing_skills
3. Scoring
Assigns a score (0–100)
Based on:
Skill match percentage
Missing critical skills
Candidate background relevance
4. Explanation
Generates:
Strengths
Weaknesses
Final reasoning
📊 Sample Results
Candidate	Description	Score
Strong	Full skill match, 3+ years experience	High (90–100)
Average	Partial skills, internship experience	Medium (40–60)
Weak	No relevant skills, basic IT background	Low (5–20)
🧠 Debugging & Improvement

During testing, an issue was identified in the scoring logic:

Weak candidates with basic technical background (e.g., IT graduate) were assigned a score of 0, which is unrealistic.
🔍 Problem

The system treated missing skills too strictly, ignoring baseline relevance.

✅ Solution
Updated scoring logic to assign a minimum score (5–20) for candidates with relevant background
Ensured:
0 score only for completely unrelated candidates
More realistic evaluation

📈 Result
Improved scoring fairness
Better alignment with real-world recruitment practices
🔎 LangSmith Tracing

The system is fully traced using LangSmith:

Tracks each pipeline step:
Extraction
Matching
Scoring
Explanation
Enables debugging and performance analysis
📁 Output

Results are stored in:

outputs/results.json → Structured output
outputs/results.txt → Human-readable output

✅ Key Features
Modular LangChain pipeline
Structured JSON outputs
Explainable AI decisions
Real-time tracing with LangSmith
Debugging and refinement of LLM behavior
📌 Conclusion

This project demonstrates how LLMs can be used to build real-world AI evaluation systems with:

Structured reasoning
Explainability
Debugging capabilities

It highlights the importance of prompt engineering, modular pipelines, and tracing in building reliable GenAI applications.

🔗 Tags

#AI #LangChain #GenAI #MachineLearning #LLM #Projects
