"""
Скрипт для организации файловой структуры проекта
Перемещает устаревшие файлы в соответствующие архивные директории
"""

import os
import shutil
import logging
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ProjectOrganizer")

# Базовый путь проекта
base_path = Path(__file__).resolve().parent

# Пути к архивным директориям
archive_horoscope = base_path / "archive" / "horoscope_generators"
archive_fixes = base_path / "archive" / "fixes"
archive_docs = base_path / "archive" / "docs"
utils_dir = base_path / "utils"
docs_dir = base_path / "docs"

# Создаем директории, если они не существуют
for directory in [archive_horoscope, archive_fixes, archive_docs, utils_dir, docs_dir]:
    os.makedirs(directory, exist_ok=True)
    logger.info(f"Обеспечено существование директории: {directory}")

# Файлы для перемещения в архив генераторов гороскопов
horoscope_archive_files = [
    "daily_horoscope_generator_old.py", 
    "daily_horoscope_generator_new.py",
    "daily_horoscope_generator_fixed.py",
    "daily_horoscope_generator_fix.py", 
    "daily_horoscope_generator_final.py",
    "daily_horoscope_generator_field_fix.py",
    "daily_horoscope_generator_compatible.py",
    "daily_horoscope_generator_backup.py",
    "daily_horoscope_generator.py",
    "daily_horoscope_generator.py.bak",
    "daily_horoscope_generator.py.new",
    "daily_horoscope_model_fix.py",
    "daily_horoscope_sql_fix.py",
    "test_horoscope_astro.py",
    "test_horoscope_generator.py",
    "generate_horoscope_images.py"
]

# Активные скрипты для гороскопов - оставляем в корне
active_horoscope_files = [
    "daily_horoscope_replace.py",
    "daily_horoscope_with_images.py",
    "daily_horoscope_sql_fix.py",
    "force_cleanup_horoscope_images.py",
    "check_horoscope_images.py"
]

# Скрипты исправлений для перемещения в архив исправлений
fix_archive_files = [
    "fix_template_syntax.py",
    "fix_syntax_errors.py",
    "fix_remaining_css.py",
    "fix_layout_issues.py",
    "fix_indentation_errors.py",
    "fix_horoscope_blocks.py",
    "fix_footer.py",
    "fix_duplicated_blocks_render.py",
    "fix_duplicated_blocks.py",
    "fix_chat_widget.py",
    "fix_blog_display.py",
    "fix_all_images.py",
    "fix_admin_user.py"
]

# Утилиты для перемещения в директорию utils
utils_files = [
    "check_ukrainian_integration.py",
    "check_scheduler.py",
    "check_model_fields.py",
    "check_horoscope_updates.py",
    "check_horoscope_blocks.py",
    "check_db_models.py",
    "check_blog_render.py",
    "check_blog_images.py",
    "check_blog_content.py",
    "check_blog_blocks.py",
    "check_blogs.py",
    "check_assistants.py",
    "check_all_blocks.py",
    "check_active_blogs.py",
    "update_scheduler_to_replacement.py",
    "create_placeholder_images.py",
    "create_horoscope_blog_blocks.py",
    "create_blog_automation_tables.py",
    "create_astro_products.py",
    "create_astro_images.py",
    "add_ukrainian_language.py",
    "clean_environment_file.py",
    "clean_html_blocks.py",
    "clean_summaries.py",
    "debug_blog_html.py",
    "debug_database_connection.py",
    "debug_database_url.py",
    "debug_payment_form.py",
    "enhance_blog_automation.py",
    "ensure_fixed_header_footer.py", 
    "finalize_layout.py",
    "final_cleanup.py",
    "initialize_render_db.py",
    "init_db.py",
    "manage_images.py",
    "migrate_blog_blocks.py",
    "recreate_admin.py",
    "remove_token_functionality.py",
    "restore_fixed_layout.py",
    "run_simplify_homepage.py",
    "setup_astro_assistants.py",
    "setup_astro_blogs.py",
    "setup_shop_block.py",
    "simplify_homepage.py",
    "update_autoposting_schedule.py",
    "update_db_models.py",
    "update_homepage_local.py",
    "update_homepage_render.py",
    "update_homepage_simple.py",
    "update_homepage_to_simple.py",
    "update_horoscope_blocks_visual.py",
    "update_horoscope_block_2.py",
    "update_horoscope_scheduler.py",
    "update_navigation_labels.py",
    "update_product_images.py",
]

# Документация для перемещения в директорию docs (оставляем только самые актуальные в корне)
docs_files = [
    "button_alignment_summary.md",
    "BLOG_TRANSFORMATION_README.md",
    "blog_layout_update.md",
    "blog_fixes_summary.md",
    "BLOG_AUTOMATION_README.md",
    "ASTROLOGY_BLOG_README.md",
    "render_deployment_instructions.md",
    "RENDER_DATABASE_MIGRATION.md",
    "PRODUCTION_RECOMMENDATIONS.md",
    "PAYMENT_FUNCTIONALITY_REPORT.md",
    "SYNTAX_FIX_DOCUMENTATION.md",
    "SIMPLIFIED_HOMEPAGE_README.md",
    "SIMPLIFIED_FIX.md",
    "NAVIGATION_UPDATE.md",
    "MODEL_COMPATIBILITY_FIX.md",
    "layout_fixes_summary.md",
    "layout_fixes_final_summary.md",
    "IMAGE_FIX_DOCUMENTATION.md",
    "IMAGES_FIX_REPORT.md",
    "IMAGES_ISSUE_SOLUTION.md",
    "fix_blog_html_display.md",
    "fixed_layout_summary.txt",
    "home_page_shop_block_update.md"
]

# Активные документы, которые оставляем в корне
active_docs = [
    "PROJECT_STRUCTURE.md",
    "README.md",
    "HOROSCOPE_REPLACEMENT_MODE.md",
    "HOROSCOPE_QUICK_REFERENCE.md", 
    "RENDER_DEPLOYMENT_UPDATE.md",
    "OPENAI_API_MIGRATION_GUIDE.md",
    "HOROSCOPE_IMAGE_FIX_FINAL_REPORT.md",
    "HOROSCOPE_IMAGES_INTEGRATION_GUIDE.md",
    "FINAL_SUCCESS_REPORT.md",
    "HOROSCOPE_REPLACEMENT_REPORT.md"
]

# Остальные MD и документационные файлы для перемещения в docs
additional_docs = [
    "FINAL_DATABASE_FIX.md",
    "FINAL_SOLUTION_SUMMARY.md",
    "FINAL_SYNTAX_FIX.md",
    "FIX_DUPLICATED_BLOCKS_INSTRUCTIONS.md",
    "HOROSCOPE_BLOCKS_FIX.md",
    "HOROSCOPE_BLOCKS_STYLING_GUIDE.md",
    "HOROSCOPE_GENERATOR_FIX.md",
    "HOROSCOPE_GENERATOR_GUIDE.md",
    "HOROSCOPE_IMAGE_FIX_REPORT.md",
    "IMMEDIATE_FIX.md",
    "INDENTATION_FIX_DOCUMENTATION.md",
    "DATABASE_SETUP.md",
    "DATABASE_SETUP_RENDER.md",
    "template_fix_verified.txt",
    "TEMPLATE_FIX_DOCUMENTATION.md",
    "UPDATE_HOMEPAGE_INSTRUCTIONS.md",
    "UPDATE_HOMEPAGE_INSTRUCTIONS_V2.md",
    "database_fix_report.md",
    "RENDER_BLOGBLOCK_FIX_COMMANDS.txt",
    "RENDER_MANUAL_COMMANDS.txt"
]

def move_files(file_list, destination_dir, description):
    """Перемещает файлы из списка в указанную директорию"""
    for filename in file_list:
        source_path = base_path / filename
        dest_path = destination_dir / filename
        
        if source_path.exists():
            try:
                shutil.move(str(source_path), str(dest_path))
                logger.info(f"Перемещен {description}: {filename}")
            except Exception as e:
                logger.error(f"Ошибка при перемещении {filename}: {e}")
        else:
            logger.warning(f"Файл не найден: {filename}")

# Выполняем перемещение файлов
logger.info("Начинаем организацию файлов проекта...")

# Перемещаем устаревшие файлы гороскопов в архив
move_files(horoscope_archive_files, archive_horoscope, "устаревший генератор гороскопов")

# Перемещаем файлы исправлений в архив
move_files(fix_archive_files, archive_fixes, "скрипт исправления")

# Перемещаем утилиты в директорию utils
move_files(utils_files, utils_dir, "утилита")

# Тесты для перемещения в архив/tests
test_files = [
    "test_astro.py",
    "test_astro_standalone.py",
    "test_blog_blocks.py",
    "test_corrected_connection.py",
    "test_db_connection.py",
    "test_ephem.py",
    "test_flatlib.py",
    "verify_blocks_fix.py",
    "verify_blog_display.py",
    "verify_blog_fixes.py",
    "verify_blog_layout.py",
    "verify_button_alignment.py",
    "verify_chat_widget.py",
    "verify_fixed_layout.py",
    "verify_fixed_positioning.py",
    "verify_footer_fix.py",
    "verify_layout_fixes.py",
    "verify_shop_block.py",
    "verify_template_fix.py",
]

# Создаем директорию для тестов
test_dir = base_path / "archive" / "tests"
os.makedirs(test_dir, exist_ok=True)
logger.info(f"Обеспечено существование директории: {test_dir}")

# Создаем директорию для скриптов БД
db_dir = base_path / "utils" / "database"
os.makedirs(db_dir, exist_ok=True)
logger.info(f"Обеспечено существование директории: {db_dir}")

# Скрипты базы данных для перемещения в utils/database
db_files = [
    "add_missing_columns.py",
    "create_and_setup_db.sh",
    "create_database.sql",
    "create_database_if_missing.py",
    "database_init_wrapper.py",
    "quick_fix_db.ps1",
    "quick_fix_db.sh",
    "quick_fix_db_clean.ps1",
    "render-db-init.ps1",
    "render-db-init.sh",
    "render_initialize_db.py",
    "render_manual_db_init.py",
    "render_setup_db.py",
    "setup_astro_blog_db.sh"
]

# Перемещаем документацию в директорию docs
move_files(docs_files, docs_dir, "документация")

# Перемещаем дополнительную документацию в директорию docs
move_files(additional_docs, docs_dir, "дополнительная документация")

# Перемещаем тесты в директорию для тестов
move_files(test_files, test_dir, "тестовый скрипт")

# Перемещаем скрипты БД в директорию для БД
move_files(db_files, db_dir, "скрипт базы данных")

logger.info("Организация файлов проекта завершена")
print("\nФайловая структура проекта успешно организована!")
print("Подробности смотрите в PROJECT_STRUCTURE.md")
