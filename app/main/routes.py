# app/main/routes.py

from flask import Blueprint, render_template, redirect, url_for, abort, g, session, current_app
from app.models import Block, PaymentMethod, Settings, Category, Product
from app import db

main = Blueprint('main', __name__)

# Вспомогательные функции для получения локализованного контента
def get_block_title(block):
    """Получает заголовок блока в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return block.title_ua or block.title
    elif lang == 'en':
        return block.title_en or block.title
    elif lang == 'de':
        return block.title_de or block.title
    elif lang == 'ru':
        return block.title_ru or block.title
    return block.title

def get_block_content(block):
    """Получает содержимое блока в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return block.content_ua or block.content
    elif lang == 'en':
        return block.content_en or block.content
    elif lang == 'de':
        return block.content_de or block.content
    elif lang == 'ru':
        return block.content_ru or block.content
    return block.content

# Новые вспомогательные функции для многоязычного контента
def get_category_name(category):
    """Получает имя категории в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return category.name_ua or category.name
    elif lang == 'en':
        return category.name_en or category.name
    elif lang == 'de':
        return category.name_de or category.name
    elif lang == 'ru':
        return category.name_ru or category.name
    return category.name

def get_product_name(product):
    """Получает имя продукта в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return product.name_ua or product.name
    elif lang == 'en':
        return product.name_en or product.name
    elif lang == 'de':
        return product.name_de or product.name
    elif lang == 'ru':
        return product.name_ru or product.name
    return product.name

def get_product_description(product):
    """Получает описание продукта в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return product.description_ua or product.description
    elif lang == 'en':
        return product.description_en or product.description
    elif lang == 'de':
        return product.description_de or product.description
    elif lang == 'ru':
        return product.description_ru or product.description
    return product.description

# Эти функции больше не используются напрямую, так как они импортируются из app.blog.routes.
# Их определения были перемещены туда и переименованы в get_blog_block_*
# Эти определения оставлены для обратной совместимости.
def get_blog_block_title(block):
    """Получает заголовок блока блога в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return block.title  # Основной язык
    elif lang == 'en':
        return block.title_en or block.title
    elif lang == 'de':
        return block.title_de or block.title
    elif lang == 'ru':
        return block.title_ru or block.title
    return block.title

def get_blog_block_content(block):
    """Получает содержимое блока блога в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return block.content  # Основной язык
    elif lang == 'en':
        return block.content_en or block.content
    elif lang == 'de':
        return block.content_de or block.content
    elif lang == 'ru':
        return block.content_ru or block.content
    return block.content

def get_blog_block_summary(block):
    """Получает краткое содержание блока блога в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return block.summary  # Основной язык
    elif lang == 'en':
        return post.summary_en or post.summary
    elif lang == 'de':
        return post.summary_de or post.summary
    elif lang == 'ru':
        return post.summary_ru or post.summary
    return post.summary

@main.route('/')
def index():
    """Головна сторінка з блоками різних астрологічних систем"""
    blocks = Block.query.filter_by(is_active=True).order_by(Block.order).all()
    settings = Settings.query.first()
    
    # Импортируем функцию для очистки HTML
    from app.utils.text_utils import strip_html_tags
    
    # Получаем активные блоки блога
    from app.models import BlogBlock
    from app.blog.routes import get_blog_block_title, get_blog_block_content
    # Используем локальную версию get_blog_block_summary с очисткой HTML
    def get_blog_block_summary(block):
        lang = g.get('lang', session.get('lang', 'uk'))
        if lang == 'uk':
            summary = block.summary_ua if block.summary_ua else block.summary
        elif lang == 'en' and block.summary_en:
            summary = block.summary_en
        elif lang == 'de' and block.summary_de:
            summary = block.summary_de
        elif lang == 'ru' and block.summary_ru:
            summary = block.summary_ru
        else:
            summary = block.summary
        return strip_html_tags(summary)
    
    # Получаем 7 блоков блога для разных астрологических систем
    recent_blog_blocks = BlogBlock.query.filter_by(is_active=True).order_by(BlogBlock.position).limit(7).all()
    
    # Получаем последние активные продукты для блока магазина
    featured_products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(3).all()
    
    # Обязательно передаем все вспомогательные функции для локализации
    return render_template('index.html', blocks=blocks, settings=settings, 
                           recent_blog_blocks=recent_blog_blocks,
                           featured_products=featured_products,
                           get_block_title=get_block_title,
                           get_block_content=get_block_content,
                           get_blog_block_title=get_blog_block_title,
                           get_blog_block_content=get_blog_block_content,
                           get_blog_block_summary=get_blog_block_summary)

@main.route('/block/<slug>')
def block_detail(slug):
    """Детальна сторінка блоку"""
    block = Block.query.filter_by(slug=slug, is_active=True).first_or_404()
    return render_template('block_detail.html', block=block)

@main.route('/payment')
def payment():
    """Сторінка з усіма методами оплати"""
    methods = PaymentMethod.query.filter_by(is_active=True).order_by(PaymentMethod.order).all()
    return render_template('payment.html', methods=methods)

@main.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main.route('/impressum')
def impressum():
    return render_template('impressum.html')

@main.route('/contacts')
def contacts():
    return render_template('contacts.html')
