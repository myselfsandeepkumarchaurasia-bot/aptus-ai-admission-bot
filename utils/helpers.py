import json


def load_courses():

    with open(
        "data/courses.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def load_faq():

    with open(
        "data/faq.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def build_context():

    courses = load_courses()
    faq = load_faq()

    context = "COURSES:\n"

    for course in courses:

        context += f"""
Course: {course['name']}
Duration: {course['duration']}
Mode: {course['mode']}
Price: {course['price']}
Tools: {', '.join(course['tools'])}
Career: {', '.join(course['career'])}
"""

    context += "\nFAQ:\n"

    for item in faq:

        context += f"""
Question: {item['question']}
Answer: {item['answer']}
"""

    return context