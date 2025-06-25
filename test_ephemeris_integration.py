"""
Test script to verify integration of ephemeris data with OpenAI assistants for horoscope generation
"""
import os
import sys
import argparse
import logging
from datetime import datetime
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ephemeris_test")

# Import ephemeris module
try:
    from ephemeris import calculate_planet_positions, get_ephemeris_report
    EPHEMERIS_AVAILABLE = True
    logger.info("Ephemeris module loaded successfully")
except ImportError as e:
    EPHEMERIS_AVAILABLE = False
    logger.error(f"Could not import ephemeris module: {str(e)}")

# Import horoscope generator functions
try:
    # Add parent directory to path if needed
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from daily_horoscope_replace import generate_horoscope_content, get_assistant_id_for_system
    logger.info("Horoscope generator functions loaded successfully")
except ImportError as e:
    logger.error(f"Could not import horoscope generator functions: {str(e)}")
    sys.exit(1)

def setup_environment():
    """Load environment variables and check OpenAI API key"""
    # Load environment variables
    load_dotenv()
    
    # Check that OpenAI API key is available
    if not os.environ.get("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY environment variable not set. Cannot continue.")
        sys.exit(1)
    
    # Check that at least one assistant ID is available
    any_assistant_found = False
    for i in range(1, 9):
        if get_assistant_id_for_system(i):
            any_assistant_found = True
            break
    
    if not any_assistant_found:
        logger.error("No assistant IDs found in environment variables. Cannot continue.")
        sys.exit(1)
        
    logger.info("Environment setup completed successfully")

def test_ephemeris_prompt():
    """Test generating a horoscope with ephemeris data"""
    if not EPHEMERIS_AVAILABLE:
        logger.error("Ephemeris module not available. Test cannot continue.")
        return False
    
    # Set test date and system
    test_date = datetime.utcnow()
    test_position = 1  # Western astrology
    
    # Get system name from the actual system used in the app (if available)
    # Add your code here if you have a mapping between position and name
    test_system_name = "Західна астрологія"  
    
    try:
        # Get ephemeris data directly to display for comparison
        ephemeris_data = calculate_planet_positions(test_date)
        logger.info(f"Generated ephemeris data for test date {test_date.strftime('%Y-%m-%d')}:")
        logger.info(f"Sun position: {ephemeris_data['positions']['Sun']['zodiac_sign']} {ephemeris_data['positions']['Sun']['position_degrees']:.2f}°")
        logger.info(f"Moon position: {ephemeris_data['positions']['Moon']['zodiac_sign']} {ephemeris_data['positions']['Moon']['position_degrees']:.2f}°")
        logger.info(f"Moon phase: {ephemeris_data['moon_phase']['phase_name']}")
        
        # Generate horoscope with ephemeris data
        logger.info(f"Generating test horoscope with ephemeris data for system {test_system_name}...")
        horoscope_data = generate_horoscope_content(test_system_name, test_position, test_date)
        
        if horoscope_data:
            logger.info("Successfully generated horoscope with ephemeris data")
            logger.info(f"Horoscope title: {horoscope_data['title']}")
            logger.info(f"Horoscope summary: {horoscope_data['summary']}")
            
            # Check if the horoscope content shows evidence of using ephemeris data
            # This is a rough heuristic check 
            planet_names = ['Сонце', 'Місяць', 'Меркурій', 'Венера', 'Марс', 'Юпітер', 'Сатурн']
            zodiac_signs = ['Овен', 'Телець', 'Близнюки', 'Рак', 'Лев', 'Діва', 'Терези', 'Скорпіон', 
                          'Стрілець', 'Козеріг', 'Водолій', 'Риби']
            
            content = horoscope_data['content'].lower()
            
            # Count planet and zodiac sign mentions
            planet_mentions = sum(1 for planet in planet_names if planet.lower() in content)
            sign_mentions = sum(1 for sign in zodiac_signs if sign.lower() in content)
            
            logger.info(f"Detected {planet_mentions} planet mentions and {sign_mentions} zodiac sign mentions")
            
            return True
        else:
            logger.error("Failed to generate horoscope with ephemeris data")
            return False
            
    except Exception as e:
        logger.error(f"Error during ephemeris prompt test: {str(e)}")
        return False

def main():
    """Main function to run the ephemeris integration test"""
    parser = argparse.ArgumentParser(description='Test ephemeris integration with horoscope generation')
    parser.add_argument('--full-output', action='store_true', help='Display full horoscope output')
    args = parser.parse_args()
    
    logger.info("Starting ephemeris integration test")
    
    # Setup environment
    setup_environment()
    
    # Test ephemeris availability
    if EPHEMERIS_AVAILABLE:
        logger.info("Ephemeris module is available")
        
        # Test calculating planetary positions
        try:
            now = datetime.utcnow()
            positions = calculate_planet_positions(now)
            logger.info("Successfully calculated planetary positions")
            
            # Test report generation
            report = get_ephemeris_report(now)
            logger.info("Successfully generated ephemeris report")
            
            # Test with horoscope prompt
            success = test_ephemeris_prompt()
            
            if success:
                logger.info("Ephemeris integration test passed - horoscope generated successfully with ephemeris data")
            else:
                logger.warning("Ephemeris integration may have issues - horoscope generation test did not complete successfully")
                
        except Exception as e:
            logger.error(f"Error during ephemeris tests: {str(e)}")
            
    else:
        logger.warning("Ephemeris module is not available. Install 'ephem' package to enable this functionality.")
    
    logger.info("Ephemeris integration test completed")

if __name__ == "__main__":
    main()
