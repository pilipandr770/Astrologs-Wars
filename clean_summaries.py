#!/usr/bin/env python3
"""
Скрипт для очистки summary в базе:
- Удаляет markdown-блоки (```...```) и html-теги из всех summary/summary_ua/summary_en/summary_de/summary_ru
- Можно запускать однократно для исправления старых данных
"""
import re
from app import db
from app.models import BlogBlock
from app.utils.text_utils import strip_html_tags

def clean_all_summaries():
    blocks = BlogBlock.query.all()
    for block in blocks:
        for field in ['summary', 'summary_ua', 'summary_en', 'summary_de', 'summary_ru']:
            if hasattr(block, field):
                val = getattr(block, field)
                if val:
                    val = re.sub(r'```.*?```', '', val, flags=re.DOTALL)
                    val = strip_html_tags(val)
                    setattr(block, field, val[:200] + '...' if len(val) > 200 else val)
    db.session.commit()
    print('Все summary очищены!')

if __name__ == "__main__":
    clean_all_summaries()
