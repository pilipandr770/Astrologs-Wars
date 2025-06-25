"""
Ephemeris module for calculating planetary positions
Used for enhancing horoscope generation with accurate astronomical data
"""
import ephem
import pytz
from datetime import datetime, timedelta

def calculate_planet_positions(date=None, location=None):
    """
    Calculate positions of planets for a given date and location
    
    Args:
        date (datetime, optional): Date for calculations, defaults to current UTC date
        location (tuple, optional): (latitude, longitude) tuple, defaults to Kyiv location
        
    Returns:
        dict: Dictionary with planetary positions and aspects
    """
    # Default to current date if none provided
    if date is None:
        date = datetime.utcnow()
        
    # Default location is Kyiv, Ukraine
    if location is None:
        location = (50.4501, 30.5234)  # Kyiv latitude, longitude
        
    # Format date for ephem
    date_str = date.strftime('%Y/%m/%d %H:%M:%S')
    
    # Initialize an observer (location on Earth)
    observer = ephem.Observer()
    observer.lat = str(location[0])
    observer.lon = str(location[1])
    observer.date = date_str
    
    # List of planets and celestial bodies to calculate
    bodies = {
        'Sun': ephem.Sun(),
        'Moon': ephem.Moon(),
        'Mercury': ephem.Mercury(),
        'Venus': ephem.Venus(),
        'Mars': ephem.Mars(),
        'Jupiter': ephem.Jupiter(),
        'Saturn': ephem.Saturn(),
        'Uranus': ephem.Uranus(),
        'Neptune': ephem.Neptune(),
        'Pluto': ephem.Pluto()
    }
    
    # Calculate positions
    positions = {}
    for name, body in bodies.items():
        body.compute(observer)
        
        # Convert position to zodiac sign and degrees
        lon_degrees = body.hlon * 180 / ephem.pi
        zodiac_sign, position_in_sign = get_zodiac_position(lon_degrees)
        
        positions[name] = {
            'zodiac_sign': zodiac_sign,
            'position_degrees': position_in_sign,
            'right_ascension': str(body.ra),
            'declination': str(body.dec),
            'phase': getattr(body, 'phase', None),
            'magnitude': getattr(body, 'mag', None)
        }
    
    # Calculate moon phase
    moon_phase = calculate_moon_phase(observer.date)
    
    # Calculate aspects between planets
    aspects = calculate_aspects(bodies)
    
    return {
        'date': date.strftime('%Y-%m-%d'),
        'time': date.strftime('%H:%M:%S'),
        'location': {
            'latitude': location[0],
            'longitude': location[1]
        },
        'positions': positions,
        'moon_phase': moon_phase,
        'aspects': aspects
    }

def get_zodiac_position(longitude):
    """
    Convert longitude to zodiac sign and position in sign
    
    Args:
        longitude (float): Celestial longitude in degrees
        
    Returns:
        tuple: (zodiac_sign, position_in_sign)
    """
    # Normalize longitude to 0-360 range
    longitude = longitude % 360
    
    # Define zodiac signs
    signs = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 
        'Leo', 'Virgo', 'Libra', 'Scorpio', 
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    # Calculate sign index (each sign is 30 degrees)
    sign_index = int(longitude / 30)
    
    # Calculate position within the sign
    position_in_sign = longitude % 30
    
    return signs[sign_index], position_in_sign

def calculate_moon_phase(date):
    """
    Calculate the phase of the moon
    
    Args:
        date (str): Date string in ephem format
        
    Returns:
        dict: Moon phase information
    """
    moon = ephem.Moon()
    moon.compute(date)
    
    # Moon phase is a number between 0 and 1
    phase = moon.phase / 100.0
    
    # Determine the phase name
    if phase < 0.01:
        phase_name = "New Moon"
    elif phase < 0.25:
        phase_name = "Waxing Crescent"
    elif phase < 0.26:
        phase_name = "First Quarter"
    elif phase < 0.49:
        phase_name = "Waxing Gibbous"
    elif phase < 0.51:
        phase_name = "Full Moon"
    elif phase < 0.75:
        phase_name = "Waning Gibbous"
    elif phase < 0.76:
        phase_name = "Last Quarter"
    else:
        phase_name = "Waning Crescent"
    
    return {
        'phase_fraction': moon.phase / 100.0,
        'phase_name': phase_name,
        'illuminated': moon.phase
    }

def calculate_aspects(bodies):
    """
    Calculate aspects between planets
    
    Args:
        bodies (dict): Dictionary of ephem body objects
        
    Returns:
        list: List of aspects between planets
    """
    aspects = []
    
    # Define aspect types and their orbs (tolerance in degrees)
    aspect_types = {
        'Conjunction': (0, 8),
        'Sextile': (60, 4),
        'Square': (90, 8),
        'Trine': (120, 8),
        'Opposition': (180, 8)
    }
    
    # Compare each pair of planets
    planet_list = list(bodies.keys())
    for i, p1_name in enumerate(planet_list):
        for p2_name in planet_list[i+1:]:
            p1 = bodies[p1_name]
            p2 = bodies[p2_name]
            
            # Calculate the angle between the planets
            angle = abs((p1.hlon - p2.hlon) * 180 / ephem.pi) % 360
            if angle > 180:
                angle = 360 - angle
                
            # Check if this angle corresponds to an aspect
            for aspect_name, (aspect_angle, orb) in aspect_types.items():
                if abs(angle - aspect_angle) <= orb:
                    aspects.append({
                        'aspect': aspect_name,
                        'body1': p1_name,
                        'body2': p2_name,
                        'angle': angle,
                        'orb': abs(angle - aspect_angle)
                    })
    
    return aspects

def get_ephemeris_report(date=None, format='text'):
    """
    Generate a readable ephemeris report for use in horoscope generation
    
    Args:
        date (datetime, optional): Date for report, defaults to current date
        format (str): Output format - 'text' or 'html'
        
    Returns:
        str: Formatted report of planetary positions and aspects
    """
    # Get raw data
    data = calculate_planet_positions(date)
    
    if format == 'html':
        # HTML formatted report
        report = f"""<div class="ephemeris-report">
    <h3>Planetary Positions for {data['date']}</h3>
    <ul>"""
        
        # Add planet positions
        for planet, info in data['positions'].items():
            report += f"\n        <li><strong>{planet}:</strong> {info['zodiac_sign']} {info['position_degrees']:.2f}°"
            if info['magnitude'] is not None:
                report += f" (Magnitude: {info['magnitude']:.2f})"
            report += "</li>"
        
        report += f"""
    </ul>
    
    <h4>Moon Phase: {data['moon_phase']['phase_name']} ({data['moon_phase']['illuminated']:.1f}%)</h4>
    
    <h4>Significant Aspects:</h4>
    <ul>"""
        
        # Add aspects
        for aspect in data['aspects']:
            report += f"\n        <li>{aspect['body1']} {aspect['aspect']} {aspect['body2']} (orb: {aspect['orb']:.2f}°)</li>"
        
        report += """
    </ul>
</div>"""
        
    else:
        # Plain text report
        report = f"Planetary Positions for {data['date']}\n"
        report += "="*40 + "\n"
        
        # Add planet positions
        for planet, info in data['positions'].items():
            report += f"{planet}: {info['zodiac_sign']} {info['position_degrees']:.2f}°"
            if info['magnitude'] is not None:
                report += f" (Magnitude: {info['magnitude']:.2f})"
            report += "\n"
        
        report += f"\nMoon Phase: {data['moon_phase']['phase_name']} ({data['moon_phase']['illuminated']:.1f}%)\n"
        
        report += "\nSignificant Aspects:\n"
        report += "-"*40 + "\n"
        
        # Add aspects
        for aspect in data['aspects']:
            report += f"{aspect['body1']} {aspect['aspect']} {aspect['body2']} (orb: {aspect['orb']:.2f}°)\n"
    
    return report

if __name__ == "__main__":
    # Example usage - print today's ephemeris report
    print(get_ephemeris_report())
    
    # Example HTML output
    # print(get_ephemeris_report(format='html'))
