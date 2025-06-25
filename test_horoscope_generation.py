"""
Test script for horoscope content generation using OpenAI assistants.

This script tests the horoscope generation functionality from daily_horoscope_replace.py
without making any changes to the database or generating images.
"""
import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("horoscope_generation_test.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("HoroscopeGenerationTest")

# Load environment variables
load_dotenv()

# Import only the necessary function from the horoscope generator
try:
    from daily_horoscope_replace import generate_horoscope_content
    logger.info("Successfully imported horoscope generation function")
except ImportError as e:
    logger.error(f"Failed to import from daily_horoscope_replace.py: {e}")
    sys.exit(1)
    
def test_horoscope_generation():
    """Test horoscope generation for each system"""
    current_date = datetime.utcnow()
    date_str = current_date.strftime("%Y-%m-%d")
    logger.info(f"Testing horoscope content generation for date: {date_str}")
    
    # Define the systems to test
    systems = [
        {"name": "Західна астрологія", "position": 1},
        {"name": "Китайська астрологія", "position": 2},
        {"name": "Ведична астрологія", "position": 3},
        {"name": "Нумерологія", "position": 4},
        {"name": "Таро", "position": 5},
        {"name": "Кармічна астрологія", "position": 6},
        {"name": "Езотерична астрологія", "position": 7},
        {"name": "Світла прогностика", "position": 8}
    ]
    
    results = []
    
    # Test content generation for each system
    for system in systems:
        position = system['position']
        system_name = system['name']
        
        logger.info(f"Testing horoscope generation for system {position}: {system_name}")
        
        try:
            # Generate horoscope content
            horoscope_data = generate_horoscope_content(system_name, position, current_date)
            
            # Check if we got valid data
            if horoscope_data and "content" in horoscope_data:
                content_length = len(horoscope_data["content"])
                
                # Check if content is not just the fallback
                is_fallback = "День сприятливий для початку нових проектів" in horoscope_data["content"]
                
                results.append({
                    "system": system_name,
                    "position": position,
                    "success": True,
                    "fallback_used": is_fallback,
                    "content_length": content_length
                })
                
                logger.info(f"Generated content for {system_name} ({content_length} chars, fallback: {is_fallback})")
                
                # Log a sample of content
                content_sample = horoscope_data["content"][:200] + "..." if len(horoscope_data["content"]) > 200 else horoscope_data["content"]
                logger.info(f"Content sample: {content_sample}")
                
            else:
                results.append({
                    "system": system_name,
                    "position": position,
                    "success": False,
                    "fallback_used": True,
                    "content_length": 0
                })
                logger.error(f"Generated empty content for {system_name}")
                
        except Exception as e:
            results.append({
                "system": system_name,
                "position": position,
                "success": False,
                "error": str(e)
            })
            logger.error(f"Error generating content for {system_name}: {str(e)}")
    
    # Print summary results
    logger.info("--- Test Results Summary ---")
    successful_generations = sum(1 for r in results if r.get("success", False) and not r.get("fallback_used", True))
    logger.info(f"Successfully generated {successful_generations}/{len(systems)} horoscopes with OpenAI assistants")
    
    fallback_count = sum(1 for r in results if r.get("fallback_used", False))
    logger.info(f"Used fallback content for {fallback_count}/{len(systems)} horoscopes")
    
    error_count = sum(1 for r in results if not r.get("success", False))
    logger.info(f"Errors encountered: {error_count}/{len(systems)}")
    
    # Print system-specific results
    logger.info("--- System-specific Results ---")
    for result in results:
        status = "SUCCESS" if result.get("success", False) and not result.get("fallback_used", True) else "FALLBACK" if result.get("fallback_used", True) else "ERROR"
        logger.info(f"System {result['position']}: {result['system']} - {status}")
    
    return successful_generations > 0

if __name__ == "__main__":
    success = test_horoscope_generation()
    sys.exit(0 if success else 1)
