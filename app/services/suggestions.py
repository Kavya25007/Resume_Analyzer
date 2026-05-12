class SuggestionEngine:
    def __init__(self):
        self.messages = {
            "skills": "Add technical skills like Python, SQL, Flask, React, or Excel.",
            "education": "Include your degree, college name, and graduation details.",
            "experience": "Add internship or work experience with action verbs and impact.",
            "projects": "Add strong projects with outcomes, tools, and GitHub links.",
            "certifications": "Mention certifications such as AWS, Azure, or Coursera.",
            "linkedin": "Add a LinkedIn profile link.",
            "github": "Add a GitHub profile link.",
            "formatting": "Improve formatting with clear headings, spacing, and bullet points."
        }

    def build(self, analysis_df, ats):
        section_map = dict(zip(analysis_df["section"], analysis_df["matched_count"]))
        suggestions = []

        if section_map.get("skills", 0) < 3:
            suggestions.append(self.messages["skills"])
        if section_map.get("education", 0) < 2:
            suggestions.append(self.messages["education"])
        if section_map.get("experience", 0) < 2:
            suggestions.append(self.messages["experience"])
        if section_map.get("projects", 0) < 2:
            suggestions.append(self.messages["projects"])
        if section_map.get("certifications", 0) < 1:
            suggestions.append(self.messages["certifications"])

        if not ats.get("linkedin_found"):
            suggestions.append(self.messages["linkedin"])
        if not ats.get("github_found"):
            suggestions.append(self.messages["github"])
        if not ats.get("email_found") or not ats.get("phone_found"):
            suggestions.append(self.messages["formatting"])

        if not suggestions:
            suggestions.append("Your resume looks balanced. Tailor it to the target job role for better results.")

        return suggestions