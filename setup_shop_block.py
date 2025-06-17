"""
Script to set up the shop block (position 12) for the blog page
"""
from app import create_app, db
from app.models import BlogBlock

def setup_shop_block():
    """Create or update the shop block (position 12)"""
    app = create_app()
    
    with app.app_context():
        # Check if shop block exists
        shop_block = BlogBlock.query.filter_by(order=12).first()
        
        if not shop_block:
            print("Creating new shop block...")
            shop_block = BlogBlock(
                title="Магазин",
                title_ua="Магазин",
                title_en="Shop",
                title_de="Shop",
                title_ru="Магазин",
                content="""<h2>Посетите наш магазин</h2>
                <p>Здесь вы найдете полезные товары для вашей духовной практики.</p>
                <p><a href="/store" class="btn btn-primary">Перейти в магазин</a></p>""",
                content_ua="""<h2>Відвідайте наш магазин</h2>
                <p>Тут ви знайдете корисні товари для вашої духовної практики.</p>
                <p><a href="/store" class="btn btn-primary">Перейти до магазину</a></p>""",
                content_en="""<h2>Visit our shop</h2>
                <p>Here you'll find useful products for your spiritual practice.</p>
                <p><a href="/store" class="btn btn-primary">Go to shop</a></p>""",
                content_de="""<h2>Besuchen Sie unseren Shop</h2>
                <p>Hier finden Sie nützliche Produkte für Ihre spirituelle Praxis.</p>
                <p><a href="/store" class="btn btn-primary">Zum Shop</a></p>""",
                content_ru="""<h2>Посетите наш магазин</h2>
                <p>Здесь вы найдете полезные товары для вашей духовной практики.</p>
                <p><a href="/store" class="btn btn-primary">Перейти в магазин</a></p>""",
                summary="Посетите наш магазин для духовной практики",
                summary_ua="Відвідайте наш магазин для духовної практики",
                summary_en="Visit our shop for spiritual practice",
                summary_de="Besuchen Sie unseren Shop für spirituelle Praxis",
                summary_ru="Посетите наш магазин для духовной практики",
                position=12,
                is_active=True,
            )
            db.session.add(shop_block)
            db.session.commit()
            print("Shop block created successfully")
        else:
            print("Shop block already exists, updating...")
            shop_block.title = "Магазин"
            shop_block.title_ua = "Магазин"
            shop_block.title_en = "Shop"
            shop_block.title_de = "Shop"
            shop_block.title_ru = "Магазин"
            shop_block.is_active = True
            db.session.commit()
            print("Shop block updated successfully")

if __name__ == "__main__":
    setup_shop_block()
