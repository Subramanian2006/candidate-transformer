import re

class ResumeParser:
    """
    Parses extracted resume text into a structured candidate dictionary.
    """

    KNOWN_SKILLS_TAXONOMY = [
        "Python", "C", "C++", "Java", "JavaScript", "TypeScript", 
        "HTML", "CSS", "MySQL", "PostgreSQL", "MongoDB",
        "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly", 
        "Flask", "Django", "FastAPI", "SQLite", "Redis", "Celery", 
        "Vue", "React", "Angular", "Bootstrap", "AWS", "Docker",
        "Git", "Linux", "Machine Learning", "Deep Learning"
    ]

    def __init__(self, text):
        self.text = text

    def extract_email(self):
        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            self.text,
        )
        return match.group(0) if match else None

    def extract_phone(self):
        match = re.search(
            r"(\+?\d[\d\s-]{8,}\d)",
            self.text,
        )
        return match.group(0).strip() if match else None

    def extract_name(self):
        lines = self.text.splitlines()
        for line in lines:
            line = line.strip()
            if len(line) > 3:
                return line
        return None

    def extract_skills(self):
        found = []
        
        for skill in self.KNOWN_SKILLS_TAXONOMY:
            
            pattern = rf"\b{re.escape(skill)}\b"
            
            if re.search(pattern, self.text, re.IGNORECASE):
                found.append(skill)

        return sorted(set(found))

    def parse(self):
        return {
            "full_name": self.extract_name(),
            "email": self.extract_email(),
            "phone": self.extract_phone(),
            "skills": self.extract_skills(),
        }