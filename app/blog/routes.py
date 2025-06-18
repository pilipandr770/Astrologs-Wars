from flask import Blueprint, render_template, redirect, url_for, flash, request, g, session
from flask_login import current_user
from app.models import db, BlogBlock
from app.forms import BlogBlockForm
from app.utils.file_utils import save_uploaded_file
from app.admin.routes import admin_required
import os
from datetime import datetime

from app.blog import blog_bp

# Вспомогательные функции для получения локализованного контента блога
def get_blog_block_title(block):
    """Получает заголовок блока блога в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return block.title_ua if block.title_ua else block.title
    elif lang == 'en' and block.title_en:
        return block.title_en
    elif lang == 'de' and block.title_de:
        return block.title_de
    elif lang == 'ru' and block.title_ru:
        return block.title_ru
    return block.title

def get_blog_block_content(block):
    """Получает содержимое блока блога в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return block.content_ua if block.content_ua else block.content
    elif lang == 'en' and block.content_en:
        return block.content_en
    elif lang == 'de' and block.content_de:
        return block.content_de
    elif lang == 'ru' and block.content_ru:
        return block.content_ru
    return block.content

def get_blog_block_summary(block):
    """Получает краткое описание блока блога в текущем языке"""
    import re
    from app.utils.text_utils import strip_html_tags

    lang = g.get('lang', session.get('lang', 'uk'))
    summary = ''
    if lang == 'uk':
        summary = block.summary_ua or block.summary or ''
    elif lang == 'en' and getattr(block, 'summary_en', None):
        summary = block.summary_en
    elif lang == 'de' and getattr(block, 'summary_de', None):
        summary = block.summary_de
    elif lang == 'ru' and getattr(block, 'summary_ru', None):
        summary = block.summary_ru
    elif hasattr(block, 'summary'):
        summary = block.summary or ''
    # Удаляем markdown-блоки кода ```...```
    summary_no_code = re.sub(r'```.*?```', '', summary or '', flags=re.DOTALL)
    # Удаляем HTML теги
    clean_summary = strip_html_tags(summary_no_code)
    return clean_summary[:200] + '...' if len(clean_summary) > 200 else clean_summary

@blog_bp.route('/')
def index():
    """Main blog index page with all active blocks"""
    blocks = BlogBlock.query.filter_by(is_active=True).filter(BlogBlock.position <= 8).order_by(BlogBlock.position).all()
    return render_template('blog/index.html', 
                           blocks=blocks,
                           get_blog_block_title=get_blog_block_title,
                           get_blog_block_summary=get_blog_block_summary,
                           get_blog_block_content=get_blog_block_content)

@blog_bp.route('/<int:position>')
def block_detail(position):
    """Detail page for a specific block"""
    block = BlogBlock.query.filter_by(position=position, is_active=True).first_or_404()
    return render_template('blog/block_detail.html', 
                           block=block,
                           get_blog_block_title=get_blog_block_title,
                           get_blog_block_summary=get_blog_block_summary,
                           get_blog_block_content=get_blog_block_content)

# Admin routes for blog management
@blog_bp.route('/admin', strict_slashes=False)
@admin_required
def admin_dashboard():
    """Admin dashboard for the blog blocks"""
    blocks = []
    for position in range(1, 13):
        block = BlogBlock.query.filter_by(position=position).first()
        if not block:
            block = BlogBlock(
                title=f"Блок #{position}",
                content=f"Содержимое блока #{position}",
                summary=f"Краткое описание блока #{position}",
                position=position
            )
            db.session.add(block)
            db.session.commit()
        blocks.append(block)
    
    return render_template('blog/admin/dashboard.html', blocks=blocks)

@blog_bp.route('/admin/blocks/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_block(id):
    """Admin view for editing a blog block"""
    block = BlogBlock.query.get_or_404(id)
    form = BlogBlockForm(obj=block)

    if form.validate_on_submit():
        block.title = form.title.data
        block.title_en = form.title_en.data
        block.title_de = form.title_de.data
        block.title_ru = form.title_ru.data
        block.content = form.content.data
        block.content_en = form.content_en.data
        block.content_de = form.content_de.data
        block.content_ru = form.content_ru.data
        block.summary = form.summary.data
        block.summary_en = form.summary_en.data
        block.summary_de = form.summary_de.data
        block.summary_ru = form.summary_ru.data
        block.is_active = form.is_active.data

        # Handle featured image
        if form.featured_image.data:
            filename = save_uploaded_file(form.featured_image.data, 'uploads/blog')
            if '/' in filename:
                block.featured_image = filename.split('/')[-1]
            else:
                block.featured_image = filename

        db.session.commit()
        flash('Блок успешно обновлён!', 'success')
        return redirect(url_for('blog.admin_dashboard'))

    return render_template('blog/admin/edit_block.html', form=form, block=block)
