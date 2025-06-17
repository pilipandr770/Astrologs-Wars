"""
Скрипт для проверки и верификации выравнивания кнопок
в блогах на главной странице и на странице блога
"""
import os
import sys

def verify_button_alignment():
    """Проверяет наличие файлов и стилей для выравнивания кнопок"""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Проверяем наличие CSS файла для выравнивания кнопок
    button_css_path = os.path.join(root_dir, 'app', 'static', 'css', 'button_alignment.css')
    if os.path.exists(button_css_path):
        print(f"✅ CSS файл для выравнивания кнопок найден: {button_css_path}")
        
        # Проверяем содержимое CSS файла
        with open(button_css_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '-webkit-line-clamp' in content and 'line-clamp' in content:
                print("✅ CSS содержит корректные свойства для обрезки текста")
            else:
                print("❌ Возможно, CSS не содержит всех необходимых свойств для обрезки текста")
                
            if 'margin-top: auto' in content:
                print("✅ CSS содержит свойство margin-top: auto для выравнивания кнопок")
            else:
                print("❌ CSS может не содержать необходимых свойств для выравнивания кнопок")
    else:
        print(f"❌ CSS файл для выравнивания кнопок не найден: {button_css_path}")
        
    # Проверяем подключение CSS в base.html
    base_html_path = os.path.join(root_dir, 'app', 'templates', 'base.html')
    if os.path.exists(base_html_path):
        with open(base_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'button_alignment.css' in content:
                print("✅ CSS файл для выравнивания кнопок подключен в base.html")
            else:
                print("❌ CSS файл для выравнивания кнопок не подключен в base.html")
    else:
        print(f"❌ Файл base.html не найден: {base_html_path}")
    
    # Проверяем структуру на главной странице
    index_html_path = os.path.join(root_dir, 'app', 'templates', 'index.html')
    if os.path.exists(index_html_path):
        with open(index_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'post-info' in content and 'post-summary' in content:
                print("✅ HTML-структура для блоков блога на главной странице найдена")
                if 'mt-auto' in content:
                    print("✅ Использовано свойство mt-auto для выравнивания кнопок на главной")
                else:
                    print("❌ Возможно, отсутствует класс mt-auto для выравнивания кнопок на главной")
            else:
                print("❌ HTML-структура для блоков блога на главной странице не найдена")
                
    # Проверяем структуру на странице блога
    blog_index_html_path = os.path.join(root_dir, 'app', 'templates', 'blog', 'index.html')
    if os.path.exists(blog_index_html_path):
        with open(blog_index_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'flex-column' in content:
                print("✅ HTML-структура для блоков на странице блога содержит flex-column")
            else:
                print("❌ HTML-структура для блоков на странице блога может не содержать flex-column")
                
            if 'card-footer' in content and 'mt-auto' in content:
                print("✅ Для футера карточек блога используется mt-auto для выравнивания")
            else:
                print("❌ Возможно, не используется mt-auto для футера карточек блога")
    else:
        print(f"❌ Файл блога index.html не найден: {blog_index_html_path}")
    
    print("\nПроверка завершена. Для просмотра результатов перезапустите сервер и проверьте выравнивание кнопок в браузере.")

if __name__ == "__main__":
    verify_button_alignment()
