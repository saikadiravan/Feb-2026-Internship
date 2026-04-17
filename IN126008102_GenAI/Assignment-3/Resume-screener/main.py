import os
import json
from dotenv import load_dotenv

from chains.extraction_chain import extraction_chain
from chains.matching_chain import matching_chain
from chains.scoring_chain import scoring_chain
from chains.explanation_chain import explanation_chain

load_dotenv()


# Read file utility
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# Save JSON output
def save_json(results, filename="outputs/results.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)


# Save .txt output
def save_txt(results, filename="outputs/results.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for candidate, data in results.items():
            f.write(f"\n================ {candidate} Candidate ================\n")
            f.write(f"Score:\n{data['score']}\n\n")
            f.write(f"Explanation:\n{data['explanation']}\n")
            f.write("\n" + "-"*60 + "\n")

# Pipeline function
def run_pipeline(resume, jd):

    print("\n--- STEP 1: EXTRACTION ---")
    extracted = extraction_chain.invoke({"resume": resume}).content
    print(extracted)

    print("\n--- STEP 2: MATCHING ---")
    matched = matching_chain.invoke({
        "jd": jd,
        "resume_data": extracted
    }).content
    print(matched)

    print("\n--- STEP 3: SCORING ---")
    score = scoring_chain.invoke({
        "match_data": matched
    }).content
    print(score)

    print("\n--- STEP 4: EXPLANATION ---")
    explanation = explanation_chain.invoke({
        "all_data": f"{extracted}\n{matched}\n{score}"
    }).content
    print(explanation)

    return {
        "score": score,
        "explanation": explanation
    }

# Main execution of resume screener
if __name__ == "__main__":

    jd = read_file("data/job_description.txt")

    resumes = [
        ("Strong", "data/strong_resume.txt"),
        ("Average", "data/average_resume.txt"),
        ("Weak", "data/weak_resume.txt"),
    ]

    all_results = {}

    for label, path in resumes:
        print(f"\n================ {label} Candidate ================")
        resume = read_file(path)
        result = run_pipeline(resume, jd)

        all_results[label] = result

# Save outputs in both json and .txt forms
    save_json(all_results)
    save_txt(all_results)

    print("\n✅ Results saved in 'outputs/' folder")