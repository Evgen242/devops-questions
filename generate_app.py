#!/usr/bin/env python3
# Просто копируем рабочий шаблон
with open('app_template.py', 'r') as src:
    with open('app.py', 'w') as dst:
        dst.write(src.read())
print("✅ Copied app_template.py to app.py")
