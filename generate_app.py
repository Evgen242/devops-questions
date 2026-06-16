#!/usr/bin/env python3
import json
import glob
import re

def generate_app():
    all_questions = []
    topic_names = []

    # Читаем все JSON файлы
    for json_file in sorted(glob.glob("topics/*.json")):
        with open(json_file, 'r') as f:
            data = json.load(f)
            topic = data['topic']
            topic_names.append(topic)
            for q in data['questions']:
                q['topic'] = topic
                all_questions.append(q)

    # Генерируем список вопросов
    questions_str = "questions = [\n"
    for i, q in enumerate(all_questions):
        question = q["question"].replace('"', '\\"')
        correct = q["correct"].replace('"', '\\"')
        options = q["options"]
        questions_str += f'    {{"id": {i+1}, "topic": "{q["topic"]}", "question": "{question}", "options": {options}, "correct": "{correct}"}}'
        if i < len(all_questions) - 1:
            questions_str += ",\n"
        else:
            questions_str += "\n"
    questions_str += "]\n"

    # Читаем шаблон
    with open('app_template.py', 'r') as f:
        app_content = f.read()

    # 1. Заменяем вопросы
    pattern = r'questions = \[.*?\]'
    new_content = re.sub(pattern, questions_str, app_content, flags=re.DOTALL)

    # 2. Обновляем список topics в home()
    topics_str = "topics = [\n"
    for topic in topic_names:
        topics_str += f'    ("{topic}", "{topic}"),\n'
    topics_str += "]"
    # Находим старый список topics
    pattern_topics = r'topics = \[.*?\]'
    new_content = re.sub(pattern_topics, topics_str, new_content, flags=re.DOTALL)

    # 3. Обновляем name_map в start()
    name_map_str = "name_map = {\n"
    for topic in topic_names:
        name_map_str += f'    "{topic}": "{topic}",\n'
    name_map_str += "}"
    # Находим старый name_map
    pattern_name_map = r'name_map = \{.*?\}'
    new_content = re.sub(pattern_name_map, name_map_str, new_content, flags=re.DOTALL)

    with open('app.py', 'w') as f:
        f.write(new_content)

    print(f"✅ Generated app.py with {len(all_questions)} questions")
    print(f"📊 Topics: {topic_names}")

if __name__ == '__main__':
    generate_app()
