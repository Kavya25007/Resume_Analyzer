import numpy as np

class ResumeScorer:
    def __init__(self):
        self.weights = {
            "skills": 30,
            "education": 15,
            "experience": 25,
            "projects": 20,
            "certifications": 10
        }

    def score(self, analysis_df):
        lookup = dict(zip(analysis_df["section"], analysis_df["matched_count"]))
        parts = []
        for section, weight in self.weights.items():
            count = min(lookup.get(section, 0), 5)
            parts.append((count / 5.0) * weight)
        return float(np.clip(np.sum(np.array(parts)), 0, 100))

    def breakdown(self, analysis_df):
        lookup = dict(zip(analysis_df["section"], analysis_df["matched_count"]))
        out = {}
        for section, weight in self.weights.items():
            count = min(lookup.get(section, 0), 5)
            out[section] = round((count / 5.0) * weight, 2)
        return out