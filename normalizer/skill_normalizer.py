class SkillNormalizer:

    CANONICAL = {

        "python3": "Python",
        "python": "Python",

        "js": "JavaScript",
        "javascript": "JavaScript",

        "mysql": "MySQL",

        "html5": "HTML",
        "html": "HTML",

        "css3": "CSS",
        "css": "CSS",

        "vue.js": "Vue",
        "vue": "Vue",

        "c++": "C++",
        "c": "C"
    }

    @classmethod
    def normalize(cls, skills):

        if not skills:
            return []

        normalized = []

        for skill in skills:
            if not isinstance(skill, str):
                continue

            key = skill.strip().lower()

            normalized.append(
                cls.CANONICAL.get(key, skill.title())
            )

        return sorted(set(normalized))
