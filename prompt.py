def generate_questions(tech_stack: str):
    tech_stack = tech_stack.lower()
    q = []

    if "python" in tech_stack:
        q += [
            "What are Python decorators and when would you use them?",
            "Explain difference between list, tuple, and set in Python."
        ]

    if "django" in tech_stack:
        q += [
            "How does Django ORM work?",
            "Explain Django middleware with an example."
        ]

    if "java" in tech_stack:
        q += [
            "What is the difference between abstract class and interface in Java?",
            "Explain JVM, JRE, and JDK."
        ]

    if "mysql" in tech_stack or "database" in tech_stack:
        q += [
            "What is normalization in databases?",
            "Explain difference between INNER JOIN and LEFT JOIN."
        ]

    if not q:
        q = ["Tell us about a project where you applied your main tech stack."]

    return q
