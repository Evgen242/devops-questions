#!/usr/bin/env python3
import re
import json
import os
from collections import defaultdict

def extract_questions(text):
    """Извлекает все вопросы из Python кода"""
    pattern = r'\{\s*"id":\s*\d+,\s*"topic":\s*"([^"]+)",\s*"question":\s*"([^"]+)",\s*"options":\s*(\[[^\]]+\]),\s*"correct":\s*"([^"]+)"\s*\}'
    matches = re.findall(pattern, text, re.DOTALL)
    
    questions = []
    for match in matches:
        topic = match[0]
        question = match[1]
        options_str = match[2]
        correct = match[3]
        
        # Преобразуем строку options в список
        options = eval(options_str)
        
        questions.append({
            'topic': topic,
            'question': question,
            'options': options,
            'correct': correct
        })
    return questions

# Читаем app.py
with open('../devops-test-app/app.py', 'r') as f:
    content = f.read()

# Извлекаем вопросы
questions = extract_questions(content)

if not questions:
    print("❌ Не удалось найти вопросы в app.py")
    exit()

print(f"🔍 Найдено {len(questions)} вопросов")

# Группируем по темам
topics = defaultdict(list)
for q in questions:
    topics[q['topic']].append(q)

# Сохраняем в JSON
os.makedirs('topics', exist_ok=True)
for topic, qs in topics.items():
    filename = topic.lower().replace(' ', '_').replace('/', '_') + '.json'
    with open(f'topics/{filename}', 'w') as f:
        json.dump({
            'topic': topic,
            'questions': qs
        }, f, indent=2, ensure_ascii=False)
    print(f"✅ Создан topics/{filename} ({len(qs)} вопросов)")

print(f"✅ Всего вопросов: {len(questions)}")
