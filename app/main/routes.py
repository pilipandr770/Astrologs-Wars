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
    """Головна сторінка з інформацією про проект"""
    # Получаем только главный блок (is_top=True) - информационный блок о проекте
    top_block = Block.query.filter_by(is_active=True, is_top=True).first()
    
    # Получаем избранные товары для секции магазина (максимум 3)
    featured_products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(3).all()
    
    # Получаем настройки сайта
    settings = Settings.query.first()
    
    # Обязательно передаем вспомогательные функции для локализации
    return render_template('index.html', 
                           top_block=top_block,
                           featured_products=featured_products,
                           settings=settings,
                           get_block_title=get_block_title,
                           get_block_content=get_block_content,
                           get_product_name=get_product_name,
                           get_product_description=get_product_description)

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
