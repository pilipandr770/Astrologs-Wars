#!/usr/bin/env python3
"""
Script to update homepage to show horoscope blocks (local version).
- Removes recent blog posts section
- Adds astrology blocks with links to detail pages
"""
import os
import shutil

def update_files():
    """Update necessary files to modify homepage"""
    # Get the base path for the project
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Create directory for CSS file if it doesn't exist
    css_path = os.path.join(base_path, 'app', 'static', 'css')
    os.makedirs(css_path, exist_ok=True)
    
    # Create horoscope-blocks.css file
    css_content = """/* Стили для блоков гороскопов на главной странице */
.horoscope-block {
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 15px;
  height: 100%;
  cursor: pointer;
  background-color: #fff;
}

.horoscope-block:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.horoscope-block h3 {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #333;
}

.horoscope-block p {
  font-size: 0.9rem;
  color: #666;
  flex-grow: 1;
  margin-bottom: 15px;
}

.horoscope-block img {
  border-radius: 8px;
  margin-bottom: 12px;
  height: 150px;
  object-fit: cover;
  width: 100%;
}

.horoscope-block .btn {
  align-self: center;
}"""
    
    css_file_path = os.path.join(css_path, 'horoscope-blocks.css')
    with open(css_file_path, 'w') as f:
        f.write(css_content)
    
    print(f"✅ Created horoscope-blocks.css file at {css_file_path}")
    
    # Update the main/routes.py file
    routes_file = os.path.join(base_path, 'app', 'main', 'routes.py')
    if not os.path.exists(routes_file):
        print(f"❌ Error: Routes file not found at {routes_file}")
        return
    
    with open(routes_file, 'r', encoding='utf-8') as f:
        content = f.read()
      # Replace the index route
    old_index_route = '''@main.route('/')
def index():
    """Головна сторінка з блоками різних астрологічних систем"""'''
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
                           get_blog_block_summary=get_blog_block_summary)"""
      new_index_route = '''@main.route('/')
def index():
    """Головна сторінка з блоками різних астрологічних систем"""'''
    # Получаем только главный блок (is_top=True)
    top_block = Block.query.filter_by(is_active=True, is_top=True).first()
    settings = Settings.query.first()
    
    # Импортируем функцию для очистки HTML
    from app.utils.text_utils import strip_html_tags
    
    # Получаем активные блоки блога для гороскопов
    from app.models import BlogBlock
    from app.blog.routes import get_blog_block_title, get_blog_block_content
    
    # Функция для получения краткого содержания блога с очисткой HTML
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
    
    # Получаем 8 гороскопных блоков (позиции 1-8)
    astrology_blocks = BlogBlock.query.filter_by(is_active=True).filter(BlogBlock.position <= 8).order_by(BlogBlock.position).all()
    
    # Получаем последние активные продукты для блока магазина
    featured_products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(3).all()
    
    # Если есть главный блок, создаем массив блоков для совместимости с шаблоном
    blocks = [top_block] if top_block else []
    
    # Обязательно передаем все вспомогательные функции для локализации
    return render_template('index.html', blocks=blocks, settings=settings, 
                           astrology_blocks=astrology_blocks, # новая переменная для гороскопов
                           featured_products=featured_products,
                           get_block_title=get_block_title,
                           get_block_content=get_block_content,
                           get_blog_block_title=get_blog_block_title,
                           get_blog_block_content=get_blog_block_content,
                           get_blog_block_summary=get_blog_block_summary)"""
    
    if old_index_route in content:
        content = content.replace(old_index_route, new_index_route)
        
        with open(routes_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {routes_file}")
    else:
        print("⚠️ Could not find the index route to update. The file may have been modified.")
        print("Please check and update the route manually if needed.")
    
    # Update the index.html template
    template_file = os.path.join(base_path, 'app', 'templates', 'index.html')
    if not os.path.exists(template_file):
        print(f"❌ Error: Template file not found at {template_file}")
        return
    
    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Replace recent blog blocks section with astrology blocks
    old_section = """  {% endif %}
  
  {# --- Блок з останніми блоками блогу --- #}
  {% if recent_blog_blocks %}
  <div class="block-card blog-block">
    <h3>
      {% if g.get('lang') == 'en' %}
        {{ _('Latest Blog Articles') }}
      {% elif g.get('lang') == 'de' %}
        {{ _('Neueste Blogartikel') }}
      {% elif g.get('lang') == 'ru' %}
        {{ _('Последние статьи блога') }}
      {% else %}
        {{ _('Останні статті з блогу') }}
      {% endif %}
    </h3>
    <div class="recent-blog-posts">
      {% for block in recent_blog_blocks %}      <div class="recent-post">
        {% if block.featured_image %}
        <div class="post-image">
          <img src="{{ url_for('static', filename='uploads/blog/' + block.featured_image) }}" 
               alt="{{ block.title }}" class="img-fluid rounded"
               onerror="this.src='{{ url_for('static', filename='uploads/' + block.featured_image) }}'">
        </div>
        {% endif %}
        <div class="post-info">
          <h4>{{ get_blog_block_title(block) }}</h4>
          <p class="post-summary">{{ get_blog_block_summary(block) }}</p>
          <div class="mt-auto">
            <a href="{{ url_for('blog.block_detail', position=block.position) }}" class="btn btn-outline-primary btn-sm">
              {% if g.get('lang') == 'en' %}
                {{ _('Read more') }}
              {% elif g.get('lang') == 'de' %}
                {{ _('Mehr lesen') }}
              {% elif g.get('lang') == 'ru' %}
                {{ _('Читать далее') }}
              {% else %}
                {{ _('Читати далі') }}
              {% endif %}
            </a>
          </div>
        </div>
      </div>
      {% if not loop.last %}<hr>{% endif %}
      {% endfor %}
    </div>
    <div class="text-center mt-3">
      <a href="{{ url_for('blog.index') }}" class="btn btn-primary">
        {% if g.get('lang') == 'en' %}
          {{ _('Go to Blog') }}
        {% elif g.get('lang') == 'de' %}
          {{ _('Zum Blog') }}
        {% elif g.get('lang') == 'ru' %}
          {{ _('Перейти в блог') }}
        {% else %}
          {{ _('Перейти до блогу') }}
        {% endif %}
      </a>
    </div>
  </div>
  {% endif %}"""
    
    new_section = """  {% endif %}
  
  {# --- БЛОКИ ГОРОСКОПОВ --- #}
  {% if astrology_blocks %}
  <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-4 mb-4">
    {% for block in astrology_blocks %}
    <div class="col">
      <div class="block-card horoscope-block h-100" onclick="window.location='{{ url_for('blog.block_detail', position=block.position) }}'">
        {% if block.featured_image %}
        <img src="{{ url_for('static', filename='uploads/blog/' + block.featured_image) }}" 
             alt="{{ get_blog_block_title(block) }}" class="card-img-top"
             onerror="this.src='{{ url_for('static', filename='uploads/' + block.featured_image) }}'">
        {% endif %}
        <h3>{{ get_blog_block_title(block) }}</h3>
        <p>{{ get_blog_block_summary(block)|safe }}</p>
        <div class="text-center mt-auto">
          <a href="{{ url_for('blog.block_detail', position=block.position) }}" class="btn btn-outline-primary">
            {% if g.get('lang') == 'en' %}
              {{ _('Read more') }}
            {% elif g.get('lang') == 'de' %}
              {{ _('Mehr lesen') }}
            {% elif g.get('lang') == 'ru' %}
              {{ _('Читать далее') }}
            {% else %}
              {{ _('Читати далі') }}
            {% endif %}
          </a>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
  {% endif %}"""
    
    if old_section in template_content:
        template_content = template_content.replace(old_section, new_section)
        
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"✅ Updated {template_file}")
    else:
        print("⚠️ Could not find the blog section to replace in the template. The file may have been modified.")
        print("Please check and update the template manually if needed.")
    
    # Update base.html to include horoscope-blocks.css
    base_file = os.path.join(base_path, 'app', 'templates', 'base.html')
    if not os.path.exists(base_file):
        print(f"❌ Error: Base template file not found at {base_file}")
        return
        
    with open(base_file, 'r', encoding='utf-8') as f:
        base_content = f.read()
    
    if "horoscope-blocks.css" not in base_content:
        css_link_section = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/button_alignment.css\') }}">'
        new_css_link = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/button_alignment.css\') }}">\n    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/horoscope-blocks.css\') }}">'
        
        if css_link_section in base_content:
            base_content = base_content.replace(css_link_section, new_css_link)
            
            with open(base_file, 'w', encoding='utf-8') as f:
                f.write(base_content)
            
            print(f"✅ Updated {base_file}")
        else:
            print("⚠️ Could not find the CSS link section in base.html. The file may have been modified.")
            print("Please add the CSS link manually: <link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/horoscope-blocks.css') }}\">")
    else:
        print("ℹ️ horoscope-blocks.css already included in base.html")
    
    print("\n🎉 All updates completed successfully!")
    print("Restart your Flask server to see the changes!")

if __name__ == "__main__":
    update_files()
