import requests
import math

INDIAN_EWASTE_CENTRES = [
    # Delhi NCR
    {"name": "Attero Recycling Pvt Ltd",         "city": "Noida",     "address": "A-83, Sector 83, Noida, UP",               "lat": 28.5355, "lon": 77.3910},
    {"name": "Cerebra Integrated Technologies",  "city": "Delhi",     "address": "Okhla Industrial Area Phase 2, New Delhi",  "lat": 28.5376, "lon": 77.2674},
    {"name": "E-Waste Recyclers India",          "city": "Delhi",     "address": "Mayapuri Industrial Area, New Delhi",       "lat": 28.6363, "lon": 77.1124},
    {"name": "Eco Birdd India Pvt Ltd",          "city": "Gurgaon",   "address": "Udyog Vihar Phase 4, Gurgaon, Haryana",    "lat": 28.5013, "lon": 77.0919},

    # Mumbai
    {"name": "Ash Recyclers",                    "city": "Mumbai",    "address": "Turbhe MIDC, Navi Mumbai",                 "lat": 19.0760, "lon": 73.0138},
    {"name": "Namo e-Waste Management",          "city": "Mumbai",    "address": "Andheri East, Mumbai",                    "lat": 19.1136, "lon": 72.8697},
    {"name": "Greenscape Eco Management",        "city": "Mumbai",    "address": "Bhandup West, Mumbai",                    "lat": 19.1543, "lon": 72.9247},

    # Bangalore
    {"name": "Sims Recycling Solutions",         "city": "Bangalore", "address": "Bommasandra Industrial Area, Bangalore",   "lat": 12.7940, "lon": 77.6878},
    {"name": "TES AMM India Pvt Ltd",            "city": "Bangalore", "address": "Whitefield, Bangalore",                   "lat": 12.9698, "lon": 77.7500},
    {"name": "Hulladek Recycling Pvt Ltd",       "city": "Bangalore", "address": "Peenya Industrial Area, Bangalore",       "lat": 13.0280, "lon": 77.5200},

    # Chennai
    {"name": "E-Parisaraa Pvt Ltd",             "city": "Chennai",   "address": "Ambattur Industrial Estate, Chennai",      "lat": 13.1143, "lon": 80.1548},
    {"name": "Grow e-Waste",                     "city": "Chennai",   "address": "Guindy Industrial Estate, Chennai",       "lat": 13.0067, "lon": 80.2206},

    # Hyderabad
    {"name": "Ramky e-Waste Recycling",          "city": "Hyderabad", "address": "IDA Bollaram, Hyderabad",                 "lat": 17.5500, "lon": 78.3200},
    {"name": "E-Waste Recycling India",          "city": "Hyderabad", "address": "Patancheru, Hyderabad",                   "lat": 17.5330, "lon": 78.2640},

    # Pune
    {"name": "Antec Technologies",               "city": "Pune",      "address": "Bhosari MIDC, Pune",                      "lat": 18.6298, "lon": 73.8553},
    {"name": "Greenscape Eco Management Pune",   "city": "Pune",      "address": "Hadapsar Industrial Estate, Pune",        "lat": 18.5018, "lon": 73.9252},

    # Kolkata
    {"name": "Rudra Environmental Solutions",    "city": "Kolkata",   "address": "Salt Lake Sector V, Kolkata",             "lat": 22.5726, "lon": 88.4319},
    {"name": "E-Waste Recyclers Kolkata",        "city": "Kolkata",   "address": "Taratala Road, Kolkata",                  "lat": 22.5100, "lon": 88.3200},

    # Ahmedabad
    {"name": "Eco Recycling Ltd (Ecoreco)",      "city": "Ahmedabad", "address": "Naroda GIDC, Ahmedabad",                  "lat": 23.0505, "lon": 72.6370},

    # Jaipur
    {"name": "E-waste Recycling Centre Jaipur",  "city": "Jaipur",    "address": "Sitapura Industrial Area, Jaipur",        "lat": 26.7606, "lon": 75.8652},
]


def calculate_distance(lat1 , lon1 , lat2 , lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a    = (math.sin(dlat/2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon/2) ** 2)
    c    = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

nearest = None
min_dist = float('inf')
def find_nearest_e_waste_centre(lat , lon):
    nearest = None
    min_dist = float('inf')
    for centre in INDIAN_EWASTE_CENTRES:
        dist = calculate_distance(lat , lon , centre["lat"] , centre["lon"])
        if dist < min_dist:
            min_dist = dist
            nearest = centre


    if nearest:
        return {
            "found" : True,
            "source" : "MoFCC Authorised list",
            "name" : nearest["name"],
            "city" : nearest["city"],
            "address" : nearest["address"],
            "distance" : f"{min_dist:.1f} km away",
            "maps_link" : f"https://www.google.com/maps?q={nearest['lat'],nearest['lon']}"
        }

    return {
        "found" : False,
        "message" : "No E_waste disposal centre found, Please vist any MCP Office near you: "
    }


result = find_nearest_e_waste_centre(28.6139, 77.2090)
print(result)