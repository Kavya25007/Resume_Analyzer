import re
import pandas as pd
import PyPDF2

class ResumeAnalyzer:
    def __init__(self):
        self.keyword_map = {
            "skills": ["python", "sql", "flask", "django", "react", "javascript", "numpy", "pandas", "excel", "communication"],
            "education": ["b.tech", "btech", "bachelor", "master", "degree", "university", "college", "cgpa", "gpa"],
            "experience": ["internship", "experience", "developer", "engineer", "worked", "built", "implemented", "managed"],
            "projects": ["project", "github", "api", "dashboard", "automation", "app", "website", "deployment"],
            "certifications": ["certification", "aws", "azure", "google", "coursera", "udemy", "nptel", "oracle"]
        }

    def extract_pdf_text(self, pdf_path):
        collected = []
        with open(pdf_path, "rb") as fh:
            reader = PyPDF2.PdfReader(fh)
            for page in reader.pages:
                collected.append(page.extract_text() or "")
        return "\n".join(collected).strip()

    def normalize(self, text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9+\-\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def analyze_keywords(self, text):
        clean = self.normalize(text)
        rows = []
        for section, terms in self.keyword_map.items():
            matched = [t for t in terms if t in clean]
            rows.append({
                "section": section,
                "matched_count": len(matched),
                "matched_terms": ", ".join(matched) if matched else "None"
            })
        return pd.DataFrame(rows)

    def ats_check(self, text):
        clean = self.normalize(text)
        return {
            "email_found": bool(re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)),
            "phone_found": bool(re.search(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\d{10}|\d{3}[-.\s]\d{3}[-.\s]\d{4})\b", text)),
            "linkedin_found": "linkedin" in clean,
            "github_found": "github" in clean,
        }