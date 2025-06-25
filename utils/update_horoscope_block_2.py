"""
Script to update the outdated horoscope block (system #2)
"""
from app import create_app, db
from app.models import BlogBlock
from datetime import datetime
import os
import sys

def update_outdated_horoscope():
    """Update the content for the outdated horoscope block (system #2)"""
    app = create_app()
    
    with app.app_context():
        # Get the outdated block (system #2)
        block = BlogBlock.query.filter_by(position=2).first()
        
        if not block:
            print("Error: Block #2 not found in the database")
            return
        
        print(f"Updating block: {block.title}")
        print(f"Last updated: {block.updated_at}")
        
        # Update the block with new content
        block.title = "Ведичний гороскоп"
        block.content = f"""
<h2>Ведичний гороскоп на {datetime.now().strftime('%d.%m.%Y')}</h2>

<p>Сьогодні Місяць знаходиться у сприятливому становищі, що приносить позитивну енергію та відкриває можливості для духовного росту. Це відмінний час для медитації та внутрішньої роботи.</p>

<h3>Рекомендації на сьогодні</h3>

<p>Зірки радять приділити увагу своєму здоров'ю та балансу між фізичним і духовним. Хороший час для початку нових справ, особливо тих, що пов'язані з творчістю та навчанням.</p>

<h3>Енергетичний баланс</h3>

<ul>
    <li>Позитивні аспекти: Юпітер у сприятливому положенні сприяє особистісному росту і розширенню свідомості.</li>
    <li>Виклики: Слід уникати поспішних рішень і пам'ятати про важливість терпіння.</li>
</ul>

<p>Цей день принесе гармонію тим, хто буде уважний до знаків Всесвіту і дослухатиметься до внутрішньої мудрості. Практика усвідомленості та вдячності особливо корисна сьогодні.</p>
"""
        block.summary = f"Ведичний гороскоп на {datetime.now().strftime('%d.%m.%Y')} - день для медитації, духовного росту та уважності до знаків Всесвіту."
        block.updated_at = datetime.utcnow()
        
        # Update Ukrainian version
        block.title_ua = block.title
        block.content_ua = block.content
        block.summary_ua = block.summary
        
        # English version
        block.title_en = "Vedic Horoscope"
        block.content_en = f"""
<h2>Vedic Horoscope for {datetime.now().strftime('%B %d, %Y')}</h2>

<p>Today, the Moon is in a favorable position, bringing positive energy and opening opportunities for spiritual growth. This is an excellent time for meditation and inner work.</p>

<h3>Recommendations for Today</h3>

<p>The stars advise paying attention to your health and the balance between physical and spiritual. It's a good time to start new endeavors, especially those related to creativity and learning.</p>

<h3>Energy Balance</h3>

<ul>
    <li>Positive aspects: Jupiter in a favorable position promotes personal growth and expansion of consciousness.</li>
    <li>Challenges: Avoid hasty decisions and remember the importance of patience.</li>
</ul>

<p>This day will bring harmony to those who are attentive to the signs of the Universe and listen to their inner wisdom. The practice of mindfulness and gratitude is especially beneficial today.</p>
"""
        block.summary_en = f"Vedic Horoscope for {datetime.now().strftime('%B %d, %Y')} - a day for meditation, spiritual growth, and attentiveness to the signs of the Universe."
        
        # Update the image filename
        today = datetime.now().strftime("%Y%m%d")
        image_filename = f"astro_2_{today}.png"
        
        # Check if image needs to be updated
        if block.featured_image != image_filename:
            # If the image doesn't exist, we need to generate it
            blog_upload_dir = os.path.join(app.root_path, 'static', 'uploads', 'blog')
            image_path = os.path.join(blog_upload_dir, image_filename)
            
            if not os.path.exists(image_path):
                print(f"Image {image_filename} does not exist. Please run generate_horoscope_images.py first.")
                # Fallback to using the existing image
                print(f"Using existing image: {block.featured_image}")
            else:
                block.featured_image = image_filename
                print(f"Updated image to: {image_filename}")
        
        # Save changes to database
        db.session.commit()
        print("Horoscope block #2 updated successfully!")

if __name__ == "__main__":
    update_outdated_horoscope()
