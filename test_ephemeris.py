"""
Test script for ephemeris calculations
Used to verify ephemeris data generation
"""
import sys
import os
from datetime import datetime

# Add parent directory to path to import ephemeris module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ephemeris import calculate_planet_positions, get_ephemeris_report

def test_ephemeris_calculation():
    """Test basic ephemeris calculations"""
    # Get current date ephemeris
    now = datetime.utcnow()
    print(f"Testing ephemeris calculations for: {now}")
    
    # Get position data
    positions = calculate_planet_positions(now)
    
    # Check if we have all expected planets
    expected_planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 
                        'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
    
    for planet in expected_planets:
        if planet in positions['positions']:
            print(f"✓ {planet} position calculated")
        else:
            print(f"✗ Failed to calculate {planet} position")
    
    # Check aspects
    if positions['aspects']:
        print(f"✓ Found {len(positions['aspects'])} planetary aspects")
    else:
        print("✗ No planetary aspects found")
        
    # Check moon phase
    if positions['moon_phase'] and 'phase_name' in positions['moon_phase']:
        print(f"✓ Moon phase: {positions['moon_phase']['phase_name']}")
    else:
        print("✗ Failed to calculate moon phase")
    
    return positions

def test_ephemeris_report():
    """Test ephemeris report generation"""
    print("\nTesting ephemeris report generation:")
    
    # Text format
    text_report = get_ephemeris_report(format='text')
    print("\nTEXT REPORT PREVIEW:")
    print("-" * 40)
    print("\n".join(text_report.split('\n')[:10]) + "\n... (truncated)")
    
    # HTML format
    html_report = get_ephemeris_report(format='html')
    print("\nHTML REPORT PREVIEW:")
    print("-" * 40)
    print("\n".join(html_report.split('\n')[:5]) + "\n... (truncated)")
    
    return {
        'text': text_report,
        'html': html_report
    }

if __name__ == "__main__":
    # Run the tests
    print("=" * 60)
    print("EPHEMERIS MODULE TESTING")
    print("=" * 60)
    
    # Test basic calculations
    positions = test_ephemeris_calculation()
    
    # Test report generation
    reports = test_ephemeris_report()
    
    print("\nAll tests completed.")
