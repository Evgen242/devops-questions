#!/usr/bin/env python3
import json
import glob
import re

def generate_app():
    all_questions = []
    
    for json_file in sorted(glob.glob("topics/*.json")):
        with open(json_file, 'r') as f:
            data = json.load(f)
            topic = data['topic']
            for q in data['questions']:
                q['topic'] = topic
                all_questions.append(q)
    
    # Генерируем список вопросов с порядковыми номерами
    questions_list = []
    for idx, q in enumerate(all_questions, start=1):
        question = q["question"].replace('"', '\\"')
        correct = q["correct"].replace('"', '\\"')
        options = q["options"]
        questions_list.append(f'    {{"id": {idx}, "topic": "{q["topic"]}", "question": "{question}", "options": {options}, "correct": "{correct}"}}')
    
    questions_str = "questions = [\n" + ",\n".join(questions_list) + "\n]\n"
    
    with open('app_template.py', 'r') as f:
        app_content = f.read()
    
    pattern = r'questions = \[.*?\]'
    new_content = re.sub(pattern, questions_str, app_content, flags=re.DOTALL)
    
    with open('app.py', 'w') as f:
        f.write(new_content)
    
    print(f"✅ Generated app.py with {len(all_questions)} questions")

if __name__ == '__main__':
    generate_app()
