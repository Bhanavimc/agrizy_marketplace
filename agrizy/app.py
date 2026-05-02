# -*- coding: utf-8 -*-
from flask import Flask, render_template,request, redirect, url_for, flash, session, jsonify
import mysql.connector
import os
from werkzeug.utils import secure_filename
import requests
#from bs4 import BeautifulSoup
app = Flask(__name__)
app.secret_key = "secret123"
app.config['JSON_AS_ASCII'] = False

# Force UTF-8 on all HTML responses
@app.after_request
def set_utf8(response):
    if response.content_type and response.content_type.startswith('text/html'):
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="agrizy",
    charset="utf8"
)
cursor = conn.cursor()

UPLOAD_FOLDER = "static/qrcodes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# create folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ========== PRODUCT CATEGORIES ==========
PRODUCT_CATEGORIES = [
    "Fruits",
    "Vegetables",
    "Grains & Cereals",
    "Pulses & Lentils",
    "Spices",
    "Oilseeds",
    "Flowers",
    "Dairy & Poultry",
    "Other"
]

# ========== LOCALIZATION (English + Kannada) ==========
TRANSLATIONS = {
    "en": {
        "app_name": "Agrizy",
        "home": "Home",
        "about": "About",
        "contact": "Contact",
        "login": "Login",
        "logout": "Logout",
        "register": "Register",
        "dashboard": "Dashboard",
        "add_product": "Add Product",
        "community": "Community",
        "my_products": "My Products",
        "sold_products": "Sold Products",
        "profile": "Profile",
        "shop": "Shop",
        "orders": "Orders",
        "cart": "Cart",
        "welcome_farmer": "Welcome, Farmer",
        "live_crop_prices": "Live Crop Prices",
        "search_products": "Search products...",
        "category": "Category",
        "all_categories": "All Categories",
        "state": "State",
        "pincode": "Pincode",
        "apply_filter": "Apply Filter",
        "price_per_kg": "Price/kg",
        "available": "Available",
        "add_to_cart": "Add to Cart",
        "already_in_cart": "Already in Cart",
        "qty_kg": "Qty (kg)",
        "product_name": "Product Name",
        "weight_kg": "Total Weight in KG",
        "price_per_kg_label": "Price per KG (₹)",
        "description": "Description",
        "upload_image": "Upload Product Image",
        "select_category": "Select Category",
        "add_product_btn": "Add Product",
        "login_to": "Login to Agrizy",
        "select_role": "Select Role",
        "farmer": "Farmer",
        "consumer": "Consumer",
        "retailer": "Retailer",
        "admin": "Admin",
        "email": "Email",
        "password": "Password",
        "new_farmer": "New Farmer?",
        "connecting_farmers": "Connecting Farmers Directly to Buyers",
        "no_middlemen": "No middlemen. Better prices. Fresh products.",
        "im_farmer": "I'm a Farmer",
        "im_consumer": "I'm a Consumer",
        "im_retailer": "I'm a Retailer",
        "why_agrizy": "Why Agrizy?",
        "better_pricing": "Better Pricing",
        "better_pricing_desc": "No middlemen ensures farmers earn more profit.",
        "direct_delivery": "Direct Delivery",
        "direct_delivery_desc": "Consumers get fresh farm products directly.",
        "smart_dashboard": "Smart Dashboard",
        "smart_dashboard_desc": "Farmers manage crops, sales, and payments easily.",
        "join_today": "Join Agrizy Today",
        "empowering": "Empowering Farmers. Connecting Communities.",
        "get_started": "Get Started",
        "footer": "© 2026 Agrizy | Built for Farmers",
        "language": "Language",
        "filter_by_state": "Filter by State",
        "filter_by_market": "Filter by Market",
        "all_states": "All States",
        "all_markets": "All Markets",
        "no_crops_found": "No crop prices found. Try changing filters.",
        "add_new_product": "Add New Product",
        "fruits": "Fruits",
        "vegetables": "Vegetables",
        "grains_cereals": "Grains & Cereals",
        "pulses_lentils": "Pulses & Lentils",
        "spices": "Spices",
        "oilseeds": "Oilseeds",
        "flowers": "Flowers",
        "dairy_poultry": "Dairy & Poultry",
        "other": "Other",
        "search_crops": "Search crops...",
        "weather_forecast": "Weather Forecast",
        "soil_analysis": "Soil Analysis & Crop Recommendations",
        "govt_schemes": "Government Schemes for Farmers",
        "organic_farming": "Organic Farming",
        "enter_location": "Enter your city/district",
        "get_weather": "Get Weather",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "wind_speed": "Wind Speed",
        "condition": "Condition",
        "soil_type": "Soil Type",
        "select_soil": "Select your soil type",
        "recommended_crops": "Recommended Crops",
        "soil_tips": "Soil Tips",
        "view_details": "View Details",
        "scheme_name": "Scheme Name",
        "benefit": "Benefit",
        "eligibility": "Eligibility",
        "how_to_apply": "How to Apply",
        "organic_tips": "Organic Farming Tips",
        "composting_guide": "Composting Guide",
        "natural_pest_control": "Natural Pest Control",
        "organic_fertilizers": "Organic Fertilizers",
        "crop_rotation": "Crop Rotation",
        "benefits_of_organic": "Benefits of Organic Farming",
        "certification": "Organic Certification",
        "language": "Language",
        "weather_advisory": "Weather Advisory",
        "feels_like": "Feels Like",
        "forecast_5day": "5-Day Forecast",
    },
    "kn": {
        "app_name": "ಅಗ್ರಿಜಿ",
        "home": "ಮುಖಪುಟ",
        "about": "ನಮ್ಮ ಬಗ್ಗೆ",
        "contact": "ಸಂಪರ್ಕ",
        "login": "ಲಾಗಿನ್",
        "logout": "ಲಾಗ್ ಔಟ್",
        "register": "ನೋಂದಣಿ",
        "dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "add_product": "ಉತ್ಪನ್ನ ಸೇರಿಸಿ",
        "my_products": "ನನ್ನ ಉತ್ಪನ್ನಗಳು",
        "community": "ಸಮುದಾಯ",
        "sold_products": "ಮಾರಾಟವಾದ ಉತ್ಪನ್ನಗಳು",
        "profile": "ಪ್ರೊಫೈಲ್",
        "shop": "ಅಂಗಡಿ",
        "orders": "ಆರ್ಡರ್‌ಗಳು",
        "cart": "ಕಾರ್ಟ್",
        "welcome_farmer": "ಸ್ವಾಗತ, ರೈತ",
        "live_crop_prices": "ಲೈವ್ ಬೆಳೆ ಬೆಲೆಗಳು",
        "search_products": "ಉತ್ಪನ್ನಗಳನ್ನು ಹುಡುಕಿ...",
        "category": "ವರ್ಗ",
        "all_categories": "ಎಲ್ಲಾ ವರ್ಗಗಳು",
        "state": "ರಾಜ್ಯ",
        "pincode": "ಪಿನ್‌ಕೋಡ್",
        "apply_filter": "ಫಿಲ್ಟರ್ ಅನ್ವಯಿಸಿ",
        "price_per_kg": "ಬೆಲೆ/ಕೆಜಿ",
        "available": "ಲಭ್ಯವಿದೆ",
        "add_to_cart": "ಕಾರ್ಟ್‌ಗೆ ಸೇರಿಸಿ",
        "already_in_cart": "ಈಗಾಗಲೇ ಕಾರ್ಟ್‌ನಲ್ಲಿದೆ",
        "qty_kg": "ಪ್ರಮಾಣ (ಕೆಜಿ)",
        "product_name": "ಉತ್ಪನ್ನದ ಹೆಸರು",
        "weight_kg": "ಒಟ್ಟು ತೂಕ (ಕೆಜಿ)",
        "price_per_kg_label": "ಪ್ರತಿ ಕೆಜಿ ಬೆಲೆ (₹)",
        "description": "ವಿವರಣೆ",
        "upload_image": "ಉತ್ಪನ್ನ ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "select_category": "ವರ್ಗ ಆಯ್ಕೆಮಾಡಿ",
        "add_product_btn": "ಉತ್ಪನ್ನ ಸೇರಿಸಿ",
        "login_to": "ಅಗ್ರಿಜಿಗೆ ಲಾಗಿನ್ ಮಾಡಿ",
        "select_role": "ಪಾತ್ರ ಆಯ್ಕೆಮಾಡಿ",
        "farmer": "ರೈತ",
        "consumer": "ಗ್ರಾಹಕ",
        "retailer": "ಚಿಲ್ಲರೆ ವ್ಯಾಪಾರಿ",
        "admin": "ನಿರ್ವಾಹಕ",
        "email": "ಇಮೇಲ್",
        "password": "ಪಾಸ್‌ವರ್ಡ್",
        "new_farmer": "ಹೊಸ ರೈತರೇ?",
        "connecting_farmers": "ರೈತರನ್ನು ನೇರವಾಗಿ ಖರೀದಿದಾರರಿಗೆ ಸಂಪರ್ಕಿಸುವುದು",
        "no_middlemen": "ಮಧ್ಯವರ್ತಿಗಳಿಲ್ಲ. ಉತ್ತಮ ಬೆಲೆ. ತಾಜಾ ಉತ್ಪನ್ನಗಳು.",
        "im_farmer": "ನಾನು ರೈತ",
        "im_consumer": "ನಾನು ಗ್ರಾಹಕ",
        "im_retailer": "ನಾನು ಚಿಲ್ಲರೆ ವ್ಯಾಪಾರಿ",
        "why_agrizy": "ಅಗ್ರಿಜಿ ಏಕೆ?",
        "better_pricing": "ಉತ್ತಮ ಬೆಲೆ",
        "better_pricing_desc": "ಮಧ್ಯವರ್ತಿಗಳಿಲ್ಲದೆ ರೈತರು ಹೆಚ್ಚು ಲಾಭ ಗಳಿಸುತ್ತಾರೆ.",
        "direct_delivery": "ನೇರ ವಿತರಣೆ",
        "direct_delivery_desc": "ಗ್ರಾಹಕರಿಗೆ ತಾಜಾ ಕೃಷಿ ಉತ್ಪನ್ನಗಳು ನೇರವಾಗಿ ಸಿಗುತ್ತವೆ.",
        "smart_dashboard": "ಸ್ಮಾರ್ಟ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "smart_dashboard_desc": "ರೈತರು ಬೆಳೆ, ಮಾರಾಟ ಮತ್ತು ಪಾವತಿಗಳನ್ನು ಸುಲಭವಾಗಿ ನಿರ್ವಹಿಸುತ್ತಾರೆ.",
        "join_today": "ಇಂದೇ ಅಗ್ರಿಜಿಗೆ ಸೇರಿ",
        "empowering": "ರೈತರನ್ನು ಸಶಕ್ತಗೊಳಿಸುವುದು. ಸಮುದಾಯಗಳನ್ನು ಸಂಪರ್ಕಿಸುವುದು.",
        "get_started": "ಪ್ರಾರಂಭಿಸಿ",
        "footer": "© 2026 ಅಗ್ರಿಜಿ | ರೈತರಿಗಾಗಿ ನಿರ್ಮಿಸಲಾಗಿದೆ",
        "language": "ಭಾಷೆ",
        "filter_by_state": "ರಾಜ್ಯದ ಮೂಲಕ ಫಿಲ್ಟರ್",
        "filter_by_market": "ಮಾರುಕಟ್ಟೆ ಮೂಲಕ ಫಿಲ್ಟರ್",
        "all_states": "ಎಲ್ಲಾ ರಾಜ್ಯಗಳು",
        "all_markets": "ಎಲ್ಲಾ ಮಾರುಕಟ್ಟೆಗಳು",
        "no_crops_found": "ಬೆಳೆ ಬೆಲೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ಫಿಲ್ಟರ್‌ಗಳನ್ನು ಬದಲಾಯಿಸಿ ನೋಡಿ.",
        "add_new_product": "ಹೊಸ ಉತ್ಪನ್ನ ಸೇರಿಸಿ",
        "fruits": "ಹಣ್ಣುಗಳು",
        "vegetables": "ತರಕಾರಿಗಳು",
        "grains_cereals": "ಧಾನ್ಯಗಳು ಮತ್ತು ಸಿರಿಧಾನ್ಯಗಳು",
        "pulses_lentils": "ಬೇಳೆಕಾಳುಗಳು",
        "spices": "ಮಸಾಲೆಗಳು",
        "oilseeds": "ಎಣ್ಣೆ ಬೀಜಗಳು",
        "flowers": "ಹೂವುಗಳು",
        "dairy_poultry": "ಹೈನು ಮತ್ತು ಕೋಳಿ ಸಾಕಾಣಿಕೆ",
        "other": "ಇತರೆ",
        "search_crops": "ಬೆಳೆಗಳನ್ನು ಹುಡುಕಿ...",
        "weather_forecast": "ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ",
        "soil_analysis": "ಮಣ್ಣಿನ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಬೆಳೆ ಶಿಫಾರಸುಗಳು",
        "govt_schemes": "ರೈತರಿಗಾಗಿ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
        "organic_farming": "ಸಾವಯವ ಕೃಷಿ",
        "enter_location": "ನಿಮ್ಮ ನಗರ/ಜಿಲ್ಲೆ ನಮೂದಿಸಿ",
        "get_weather": "ಹವಾಮಾನ ಪಡೆಯಿರಿ",
        "temperature": "ತಾಪಮಾನ",
        "humidity": "ಆರ್ದ್ರತೆ",
        "wind_speed": "ಗಾಳಿ ವೇಗ",
        "condition": "ಸ್ಥಿತಿ",
        "soil_type": "ಮಣ್ಣಿನ ಪ್ರಕಾರ",
        "select_soil": "ನಿಮ್ಮ ಮಣ್ಣಿನ ಪ್ರಕಾರವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "recommended_crops": "ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆಗಳು",
        "soil_tips": "ಮಣ್ಣಿನ ಸಲಹೆಗಳು",
        "view_details": "ವಿವರಗಳನ್ನು ನೋಡಿ",
        "scheme_name": "ಯೋಜನೆಯ ಹೆಸರು",
        "benefit": "ಪ್ರಯೋಜನ",
        "eligibility": "ಅರ್ಹತೆ",
        "how_to_apply": "ಅರ್ಜಿ ಹೇಗೆ ಸಲ್ಲಿಸುವುದು",
        "organic_tips": "ಸಾವಯವ ಕೃಷಿ ಸಲಹೆಗಳು",
        "composting_guide": "ಕಂಪೋಸ್ಟ್ ಮಾರ್ಗದರ್ಶಿ",
        "natural_pest_control": "ನೈಸರ್ಗಿಕ ಕೀಟ ನಿಯಂತ್ರಣ",
        "organic_fertilizers": "ಸಾವಯವ ಗೊಬ್ಬರಗಳು",
        "crop_rotation": "ಬೆಳೆ ಬದಲಾವಣೆ",
        "benefits_of_organic": "ಸಾವಯವ ಕೃಷಿಯ ಪ್ರಯೋಜನಗಳು",
        "certification": "ಸಾವಯವ ಪ್ರಮಾಣೀಕರಣ",
        "language": "ಭಾಷೆ",
        "weather_advisory": "ಹವಾಮಾನ ಸಲಹೆ",
        "feels_like": "ಅನುಭವಿಸುವಂತೆ",
        "forecast_5day": "5-ದಿನ ಮುನ್ಸೂಚನೆ",
    },
    "hi": {
        "app_name": "एग्रिजी",
        "community": "समुदाय",
        "home": "होम",
        "about": "हमारे बारे में",
        "contact": "संपर्क",
        "login": "लॉगिन",
        "logout": "लॉग आउट",
        "register": "पंजीकरण",
        "dashboard": "डैशबोर्ड",
        "add_product": "उत्पाद जोड़ें",
        "my_products": "मेरे उत्पाद",
        "sold_products": "बेचे गए उत्पाद",
        "profile": "प्रोफ़ाइल",
        "shop": "दुकान",
        "orders": "ऑर्डर",
        "cart": "कार्ट",
        "welcome_farmer": "स्वागत है, किसान",
        "live_crop_prices": "लाइव फसल भाव",
        "search_products": "उत्पाद खोजें...",
        "category": "श्रेणी",
        "all_categories": "सभी श्रेणियाँ",
        "state": "राज्य",
        "pincode": "पिनकोड",
        "apply_filter": "फ़िल्टर लागू करें",
        "price_per_kg": "मूल्य/किलो",
        "available": "उपलब्ध",
        "add_to_cart": "कार्ट में जोड़ें",
        "already_in_cart": "पहले से कार्ट में है",
        "qty_kg": "मात्रा (किलो)",
        "product_name": "उत्पाद का नाम",
        "weight_kg": "कुल वजन (किलो)",
        "price_per_kg_label": "प्रति किलो मूल्य (₹)",
        "description": "विवरण",
        "upload_image": "उत्पाद छवि अपलोड करें",
        "select_category": "श्रेणी चुनें",
        "add_product_btn": "उत्पाद जोड़ें",
        "login_to": "एग्रिजी में लॉगिन करें",
        "select_role": "भूमिका चुनें",
        "farmer": "किसान",
        "consumer": "उपभोक्ता",
        "retailer": "खुदरा विक्रेता",
        "admin": "व्यवस्थापक",
        "email": "ईमेल",
        "password": "पासवर्ड",
        "new_farmer": "नए किसान?",
        "connecting_farmers": "किसानों को सीधे खरीदारों से जोड़ना",
        "no_middlemen": "कोई बिचौलिया नहीं। बेहतर कीमत। ताजा उत्पाद।",
        "im_farmer": "मैं किसान हूँ",
        "im_consumer": "मैं उपभोक्ता हूँ",
        "im_retailer": "मैं खुदरा विक्रेता हूँ",
        "why_agrizy": "एग्रिजी क्यों?",
        "better_pricing": "बेहतर मूल्य",
        "better_pricing_desc": "बिचौलियों के बिना किसान अधिक लाभ कमाते हैं।",
        "direct_delivery": "सीधी डिलीवरी",
        "direct_delivery_desc": "उपभोक्ताओं को ताजा कृषि उत्पाद सीधे मिलते हैं।",
        "smart_dashboard": "स्मार्ट डैशबोर्ड",
        "smart_dashboard_desc": "किसान फसल, बिक्री और भुगतान आसानी से प्रबंधित करते हैं।",
        "join_today": "आज ही एग्रिजी से जुड़ें",
        "empowering": "किसानों को सशक्त बनाना। समुदायों को जोड़ना।",
        "get_started": "शुरू करें",
        "footer": "© 2026 एग्रिजी | किसानों के लिए बनाया गया",
        "language": "भाषा",
        "filter_by_state": "राज्य के अनुसार फ़िल्टर",
        "filter_by_market": "बाज़ार के अनुसार फ़िल्टर",
        "all_states": "सभी राज्य",
        "all_markets": "सभी बाज़ार",
        "no_crops_found": "कोई फसल भाव नहीं मिला। फ़िल्टर बदलकर देखें।",
        "add_new_product": "नया उत्पाद जोड़ें",
        "fruits": "फल",
        "vegetables": "सब्जियाँ",
        "grains_cereals": "अनाज और दलहन",
        "pulses_lentils": "दालें",
        "spices": "मसाले",
        "oilseeds": "तिलहन",
        "flowers": "फूल",
        "dairy_poultry": "डेयरी और मुर्गीपालन",
        "other": "अन्य",
        "search_crops": "फसल खोजें...",
        "weather_forecast": "मौसम का पूर्वानुमान",
        "soil_analysis": "मिट्टी विश्लेषण और फसल सिफारिशें",
        "govt_schemes": "किसानों के लिए सरकारी योजनाएं",
        "organic_farming": "जैविक खेती",
        "enter_location": "अपना शहर/जिला दर्ज करें",
        "get_weather": "मौसम देखें",
        "temperature": "तापमान",
        "humidity": "नमी",
        "wind_speed": "हवा की गति",
        "condition": "स्थिति",
        "soil_type": "मिट्टी का प्रकार",
        "select_soil": "अपनी मिट्टी का प्रकार चुनें",
        "recommended_crops": "सुझाई गई फसलें",
        "soil_tips": "मिट्टी के सुझाव",
        "view_details": "विवरण देखें",
        "scheme_name": "योजना का नाम",
        "benefit": "लाभ",
        "eligibility": "पात्रता",
        "how_to_apply": "आवेदन कैसे करें",
        "organic_tips": "जैविक खेती के सुझाव",
        "composting_guide": "कंपोस्ट गाइड",
        "natural_pest_control": "प्राकृतिक कीट नियंत्रण",
        "organic_fertilizers": "जैविक उर्वरक",
        "crop_rotation": "फसल चक्र",
        "benefits_of_organic": "जैविक खेती के लाभ",
        "certification": "जैविक प्रमाणीकरण",
        "weather_advisory": "मौसम सलाह",
        "feels_like": "अनुभव होता है",
        "forecast_5day": "5 दिन का पूर्वानुमान",
    }
}

def get_lang():
    """Get current language from session, default English."""
    return session.get("lang", "en")

def t():
    """Get translation dict for current language."""
    return TRANSLATIONS.get(get_lang(), TRANSLATIONS["en"])

@app.context_processor
def inject_translations():
    """Make translations available in all templates."""
    lang = get_lang()
    return {
        "t": TRANSLATIONS.get(lang, TRANSLATIONS["en"]),
        "current_lang": lang,
        "categories": PRODUCT_CATEGORIES,
    }

@app.route("/set_language/<lang>")
def set_language(lang):
    if lang in TRANSLATIONS:
        session["lang"] = lang
    return redirect(request.referrer or "/")
    

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register_farmer")
def register_farmer():
    return render_template("farmer_register.html")

@app.route("/save_farmer", methods=["POST"])
def save_farmer():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    aadhar = request.form["aadhar"]
    state = request.form["state"]
    city = request.form["city"]
    pincode = request.form["pincode"]
    password = request.form["password"]
    file = request.files["qr_image"]

    filename = ""
    if file and file.filename != "":
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

    try:
        query = """INSERT INTO farmers 
        (name, email, phone, aadhar, state, city, pincode, password, qr_image)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        cursor.execute(query, (name, email, phone, aadhar, state, city, pincode, password, filename))
        conn.commit()

        flash("Registration Successful!", "success")

    except Exception as e:
        print(e)
        flash("Error or Email already exists!", "danger")

    return redirect("/register_farmer")


# Consumer Register Page

@app.route("/register_consumer")
def register_consumer():
    return render_template("consumer_register.html")


@app.route("/save_consumer", methods=["POST"])
def save_consumer():
    data = (
        request.form["name"],
        request.form["email"],
        request.form["phone"],
        request.form["state"],
        request.form["city"],
        request.form["pincode"],
        request.form["password"]
    )

    try:
        cursor.execute("""
            INSERT INTO consumers 
            (name,email,phone,state,city,pincode,password)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, data)
        conn.commit()
        flash("Consumer Registered Successfully!", "success")
    except:
        flash("Email already exists!", "danger")

    return redirect("/register_consumer")



# Retailer Register Page

@app.route("/register_retailer")
def register_retailer():
    return render_template("retailer_register.html")


@app.route("/save_retailer", methods=["POST"])
def save_retailer():
    data = (
        request.form["name"],
        request.form["email"],
        request.form["phone"],
        request.form["shop_name"],
        request.form["state"],
        request.form["city"],
        request.form["pincode"],
        request.form["password"]
    )

    try:
        cursor.execute("""
            INSERT INTO retailers 
            (name,email,phone,shop_name,state,city,pincode,password)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, data)
        conn.commit()
        flash("Retailer Registered Successfully!", "success")
    except:
        flash("Email already exists!", "danger")

    return redirect("/register_retailer")
# Show login page
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

from flask import session


# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    role = request.form["role"]
    email = request.form["email"]
    password = request.form["password"]

    # ================= FARMER =================
    if role == "farmer":
        cursor.execute("SELECT * FROM farmers WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session["user_id"] = user[0]
            session["role"] = "farmer"
            flash("Farmer login successful", "success")
            return redirect("/farmer_dashboard")

    # ================= CONSUMER =================
    elif role == "consumer":
        cursor.execute("SELECT * FROM consumers WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session["user_id"] = user[0]
            session["role"] = "consumer"
            flash("Login successful 🛒", "success")
            return redirect("/consumer_dashboard")

    # ================= RETAILER =================
    elif role == "retailer":
        cursor.execute("SELECT * FROM retailers WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session["user_id"] = user[0]
            session["role"] = "retailer"
            flash("Retailer login successful", "success")
            return redirect("/retailer_dashboard")   # same UI as consumer

    # ================= ADMIN =================
    elif role == "admin":
        cursor.execute("SELECT * FROM admin WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session["role"] = "admin"
            flash("Admin login successful", "success")
            return redirect("/admin_dashboard")

    # ================= INVALID =================
    flash("Invalid credentials ❌", "danger")
    return redirect("/login")

@app.route("/farmer_dashboard")
def farmer_dashboard():
    if "user_id" in session and session["role"] == "farmer":
        farmer_id = session["user_id"]
        cursor.execute("SELECT state, city FROM farmers WHERE id=%s", (farmer_id,))
        farmer_info = cursor.fetchone()
        farmer_state = farmer_info[0] if farmer_info else ""
        farmer_city = farmer_info[1] if farmer_info else ""
        return render_template("farmer_dashboard.html", farmer_state=farmer_state, farmer_city=farmer_city)
    else:
        return redirect("/login")
    
@app.route("/add_product")
def add_product():
    if "user_id" in session and session["role"] == "farmer":
        return render_template("add_product.html")
    else:
        return redirect("/login")
    
@app.route("/save_product", methods=["POST"])
def save_product():
    if "user_id" not in session:
        return redirect("/login")

    farmer_id = session["user_id"]

    name = request.form["name"]
    weight = request.form["weight"]
    price = request.form["price"]
    description = request.form["description"]
    category = request.form.get("category", "Other")

    file = request.files["image"]

    filename = ""
    if file and file.filename != "":
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    query = """INSERT INTO products 
    (farmer_id, name, weight, price, description, image, category)
    VALUES (%s,%s,%s,%s,%s,%s,%s)"""

    cursor.execute(query, (farmer_id, name, weight, price, description, filename, category))
    conn.commit()

    flash("Product added successfully! Waiting for admin approval.", "success")
    return redirect("/add_product")

@app.route("/view_products")
def view_products():
    if "user_id" not in session:
        return redirect("/login")

    farmer_id = session["user_id"]

    cursor.execute("SELECT * FROM products WHERE farmer_id=%s and availability=%s ORDER BY id DESC", (farmer_id,'available'))
    products = cursor.fetchall()

    return render_template("view_products.html", products=products)

@app.route("/delete_product/<int:id>")
def delete_product(id):
    cursor.execute("DELETE FROM products WHERE id=%s", (id,))
    conn.commit()
    flash("Product deleted successfully!", "success")
    return redirect("/view_products")


@app.route("/admin_dashboard")
def admin_dashboard():
    if "role" not in session or session["role"] != "admin":
        return redirect("/login")

    cursor.execute("""
        SELECT products.*, farmers.name 
        FROM products 
        JOIN farmers ON products.farmer_id = farmers.id
        ORDER BY products.id DESC
    """)
    
    products = cursor.fetchall()

    return render_template("admin_dashboard.html", products=products)

@app.route("/approve_product/<int:id>")
def approve_product(id):
    cursor.execute("UPDATE products SET status='approved' WHERE id=%s", (id,))
    conn.commit()
    flash("Product Approved ✅", "success")
    return redirect("/admin_dashboard")

@app.route("/reject_product/<int:id>")
def reject_product(id):
    cursor.execute("UPDATE products SET status='rejected' WHERE id=%s", (id,))
    conn.commit()
    flash("Product Rejected ❌", "danger")
    return redirect("/admin_dashboard")


@app.route("/consumer_dashboard")
def consumer_dashboard():

    # 🔐 Auth check
    if "user_id" not in session or session["role"] not in ["consumer", "retailer"]:
        return redirect("/login")

    user_id = session["user_id"]

    # 🔍 Get filters
    search = request.args.get("search")
    state = request.args.get("state")
    pincode = request.args.get("pincode")
    category = request.args.get("category")

    # 🧠 Base query (IMPORTANT FIX)
    query = """
        SELECT products.*, farmers.state, farmers.pincode
        FROM products
        JOIN farmers ON products.farmer_id = farmers.id
        WHERE products.status='approved'
        AND products.availability='available'
    """

    filters = []
    values = []

    # 🔍 Apply filters
    if search:
        filters.append("products.name LIKE %s")
        values.append(f"%{search}%")

    if state:
        filters.append("farmers.state = %s")
        values.append(state)

    if pincode:
        filters.append("farmers.pincode = %s")
        values.append(pincode)

    if category:
        filters.append("products.category = %s")
        values.append(category)

    # ➕ Add filters to query
    if filters:
        query += " AND " + " AND ".join(filters)

    # 🛒 Cart count
    cursor.execute("SELECT COUNT(*) FROM cart WHERE user_id=%s", (user_id,))
    cart_count = cursor.fetchone()[0]

    # 🛒 Cart product IDs (for UI)
    cursor.execute("SELECT product_id FROM cart WHERE user_id=%s", (user_id,))
    cart_items = cursor.fetchall()
    cart_product_ids = [i[0] for i in cart_items]

    # 📦 Fetch products
    cursor.execute(query, tuple(values))
    products = cursor.fetchall()

    return render_template(
        "consumer_dashboard.html",
        products=products,
        cart_count=cart_count,
        cart_product_ids=cart_product_ids
    )

@app.route("/retailer_dashboard")
def retailer_dashboard():

    if "user_id" not in session or session["role"] not in ["retailer"]:
        return redirect("/login")

    user_id = session["user_id"]

    # 🔍 Get filters
    search = request.args.get("search")
    state = request.args.get("state")
    pincode = request.args.get("pincode")
    category = request.args.get("category")

    # 🧠 Base query (IMPORTANT FIX)
    query = """
        SELECT products.*, farmers.state, farmers.pincode
        FROM products
        JOIN farmers ON products.farmer_id = farmers.id
        WHERE products.status='approved'
        AND products.availability='available'
    """

    filters = []
    values = []

    # 🔍 Apply filters
    if search:
        filters.append("products.name LIKE %s")
        values.append(f"%{search}%")

    if state:
        filters.append("farmers.state = %s")
        values.append(state)

    if pincode:
        filters.append("farmers.pincode = %s")
        values.append(pincode)

    if category:
        filters.append("products.category = %s")
        values.append(category)

    # ➕ Add filters to query
    if filters:
        query += " AND " + " AND ".join(filters)

    # 🛒 Cart count
    cursor.execute("SELECT COUNT(*) FROM recart WHERE user_id=%s", (user_id,))
    cart_count = cursor.fetchone()[0]

    # 🛒 Cart product IDs (for UI)
    cursor.execute("SELECT product_id FROM recart WHERE user_id=%s", (user_id,))
    cart_items = cursor.fetchall()
    cart_product_ids = [i[0] for i in cart_items]

    # 📦 Fetch products
    cursor.execute(query, tuple(values))
    products = cursor.fetchall()

    return render_template(
        "retailer_dashboard.html",
        products=products,
        cart_count=cart_count,
        cart_product_ids=cart_product_ids
    )
@app.route("/add_to_cart/<int:product_id>", methods=["GET", "POST"])
def add_to_cart(product_id):

    user_id = session["user_id"]
    role = session["role"]

    # Get requested quantity in kg (default 1)
    if request.method == "POST":
        qty = float(request.form.get("quantity", 1))
    else:
        qty = float(request.args.get("quantity", 1))

    if qty <= 0:
        flash("Quantity must be greater than 0 ❌", "danger")
        return redirect("/retailer_dashboard" if role == "retailer" else "/consumer_dashboard")

    # Check product availability and weight
    cursor.execute("SELECT availability, weight FROM products WHERE id=%s", (product_id,))
    product_info = cursor.fetchone()

    if not product_info or product_info[0] == "sold":
        flash("Product not available ❌", "danger")
        return redirect("/retailer_dashboard" if role == "retailer" else "/consumer_dashboard")

    available_weight = float(product_info[1])
    if qty > available_weight:
        flash(f"Only {available_weight} kg available ⚠️", "warning")
        return redirect("/retailer_dashboard" if role == "retailer" else "/consumer_dashboard")

    if role == "retailer":
        # Check if already in cart
        cursor.execute("SELECT * FROM recart WHERE user_id=%s AND product_id=%s",
                    (user_id, product_id))
        existing = cursor.fetchone()

        if existing:
            flash("Already in cart ⚠️", "warning")
            return redirect("/retailer_dashboard")

        cursor.execute("""
            INSERT INTO recart (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (user_id, product_id, qty))
        conn.commit()
        return redirect("/retailer_dashboard")
    else:
        # Check if already in cart
        cursor.execute("SELECT * FROM cart WHERE user_id=%s AND product_id=%s",
                    (user_id, product_id))
        existing = cursor.fetchone()

        if existing:
            flash("Already in cart ⚠️", "warning")
            return redirect("/consumer_dashboard")

        cursor.execute("""
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (user_id, product_id, qty))
        conn.commit()
        return redirect("/consumer_dashboard")

@app.route("/cart")
def view_cart():
    user_id = session["user_id"]
    role = session["role"]
    if role=="consumer":
        cursor.execute("""
            SELECT cart.id, products.name, products.price, products.image, cart.quantity, products.weight
            FROM cart
            JOIN products ON cart.product_id = products.id
            WHERE cart.user_id=%s
        """, (user_id,))

        items = cursor.fetchall()

        return render_template("cart.html", items=items)
    else:
        cursor.execute("""
            SELECT recart.id, products.name, products.price, products.image, recart.quantity, products.weight
            FROM recart
            JOIN products ON recart.product_id = products.id
            WHERE recart.user_id=%s
        """, (user_id,))

        items = cursor.fetchall()

        return render_template("recart.html", items=items)

@app.route("/remove_item/<int:id>")
def remove_item(id):
    role = session['role']
    if role=="consumer":
        cursor.execute("DELETE FROM cart WHERE id=%s", (id,))
        conn.commit()
        return redirect("/cart")
    else:
        cursor.execute("DELETE FROM recart WHERE id=%s", (id,))
        conn.commit()
        return redirect("/cart")

@app.route("/checkout")
def checkout():
    user_id = session["user_id"]
    role = session["role"]
    if role=="consumer":
        cursor.execute("""
            SELECT cart.product_id, cart.quantity,
                products.name, products.price,
                farmers.id, farmers.qr_image
            FROM cart
            JOIN products ON cart.product_id = products.id
            JOIN farmers ON products.farmer_id = farmers.id
            WHERE cart.user_id=%s
        """, (user_id,))

        items = cursor.fetchall()

        return render_template("checkout.html", items=items)
    else:
        cursor.execute("""
            SELECT recart.product_id, recart.quantity,
                products.name, products.price,
                farmers.id, farmers.qr_image
            FROM recart
            JOIN products ON recart.product_id = products.id
            JOIN farmers ON products.farmer_id = farmers.id
            WHERE recart.user_id=%s
        """, (user_id,))

        items = cursor.fetchall()

        return render_template("checkout.html", items=items)

@app.route("/confirm_payment", methods=["POST"])
def confirm_payment():

    user_id = session["user_id"]
    role = session["role"]

    try:
        if role == "consumer":

            cursor.execute("""
                SELECT product_id, quantity 
                FROM cart 
                WHERE user_id=%s
            """, (user_id,))
            
            cart_items = cursor.fetchall()

            for item in cart_items:
                product_id = item[0]
                qty = item[1]

                # ✅ get price + farmer_id
                cursor.execute("""
                    SELECT price, farmer_id 
                    FROM products 
                    WHERE id=%s
                """, (product_id,))
                
                product = cursor.fetchone()
                if not product:
                    continue

                price, farmer_id = product
                total_price = price * qty

                # orders
                cursor.execute("""
                    INSERT INTO orders (user_id, product_id, quantity, total_price)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, product_id, qty, total_price))

                # transactions
                cursor.execute("""
                    INSERT INTO transactions 
                    (user_id, farmer_id, product_id, quantity, total_price, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, farmer_id, product_id, qty, total_price, 'paid'))

                # update product weight
                cursor.execute("""
                    UPDATE products 
                    SET weight = weight - %s
                    WHERE id=%s
                """, (qty, product_id))

                # mark as sold if no weight left
                cursor.execute("SELECT weight FROM products WHERE id=%s", (product_id,))
                remaining = cursor.fetchone()[0]
                if remaining <= 0:
                    cursor.execute("""
                        UPDATE products 
                        SET availability='sold'
                        WHERE id=%s
                    """, (product_id,))

            # ✅ clear full cart
            cursor.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))

        else:
            cursor.execute("""
                SELECT product_id, quantity 
                FROM recart 
                WHERE user_id=%s
            """, (user_id,))
            
            cart_items = cursor.fetchall()

            for item in cart_items:
                product_id = item[0]
                qty = item[1]

                # ✅ FIX: fetch farmer_id also
                cursor.execute("""
                    SELECT price, farmer_id 
                    FROM products 
                    WHERE id=%s
                """, (product_id,))
                
                product = cursor.fetchone()
                if not product:
                    continue

                price, farmer_id = product
                total_price = price * qty

                cursor.execute("""
                    INSERT INTO reorders (user_id, product_id, quantity, total_price)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, product_id, qty, total_price))

                cursor.execute("""
                    INSERT INTO REtransactions 
                    (user_id, farmer_id, product_id, quantity, total_price, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, farmer_id, product_id, qty, total_price, 'paid'))

                # update product weight
                cursor.execute("""
                    UPDATE products 
                    SET weight = weight - %s
                    WHERE id=%s
                """, (qty, product_id))

                # mark as sold if no weight left
                cursor.execute("SELECT weight FROM products WHERE id=%s", (product_id,))
                remaining = cursor.fetchone()[0]
                if remaining <= 0:
                    cursor.execute("""
                        UPDATE products 
                        SET availability='sold'
                        WHERE id=%s
                    """, (product_id,))

            # ✅ clear full cart
            cursor.execute("DELETE FROM recart WHERE user_id=%s", (user_id,))

        conn.commit()
        return redirect("/my_orders")

    except Exception as e:
        conn.rollback()
        return str(e)
        

@app.route("/my_orders")
def my_orders():
    user_id = session["user_id"]
    role = session["role"]
    if role=="consumer":

        cursor.execute("""
            SELECT products.name, transactions.quantity, transactions.total_price, transactions.created_at
            FROM transactions
            JOIN products ON transactions.product_id = products.id
            WHERE transactions.user_id=%s
            ORDER BY transactions.id DESC
        """, (user_id,))

        orders = cursor.fetchall()

        return render_template("orders.html", orders=orders)
    else:
        cursor.execute("""
            SELECT products.name, retransactions.quantity, retransactions.total_price, retransactions.created_at
            FROM retransactions
            JOIN products ON retransactions.product_id = products.id
            WHERE retransactions.user_id=%s
            ORDER BY retransactions.id DESC
        """, (user_id,))

        orders = cursor.fetchall()

        return render_template("reorders.html", orders=orders)


@app.route("/sold_products")
def sold_products():

    if "user_id" not in session or session["role"] != "farmer":
        return redirect("/login")

    farmer_id = session["user_id"]

    # Get sold products with buyer details
    '''cursor.execute("""
        SELECT 
            products.name,
            orders.quantity,
            orders.total_price,
            orders.order_date,
            consumers.name,
            consumers.phone
        FROM orders
        JOIN products ON orders.product_id = products.id
        JOIN consumers ON orders.user_id = consumers.id
        WHERE products.farmer_id = %s
        ORDER BY orders.order_date DESC
    """, (farmer_id,))'''
    cursor.execute("""
    SELECT 
        products.name AS product_name,
        orders.quantity,
        orders.total_price,
        orders.order_date,
        consumers.name AS customer_name,
        consumers.phone,
        'Consumer' AS order_type
    FROM orders
    JOIN products ON orders.product_id = products.id
    JOIN consumers ON orders.user_id = consumers.id
    WHERE products.farmer_id = %s

    UNION ALL

    SELECT 
        products.name AS product_name,
        reorders.quantity,
        reorders.total_price,
        reorders.order_date,
        retailers.name AS customer_name,
        retailers.phone,
        'Retailer' AS order_type
    FROM reorders
    JOIN products ON reorders.product_id = products.id
    JOIN retailers ON reorders.user_id = retailers.id
    WHERE products.farmer_id = %s

    ORDER BY order_date DESC
    """, (farmer_id, farmer_id))

    sold_products = cursor.fetchall()

    return render_template("farmer_sold_products.html", sold_products=sold_products)

@app.route("/profile")
def profile():

    if "user_id" not in session or session["role"] != "farmer":
        return redirect("/login")

    farmer_id = session["user_id"]

    cursor.execute("SELECT name, email, phone, aadhar, state, city, pincode, qr_image FROM farmers WHERE id=%s", (farmer_id,))
    farmer = cursor.fetchone()

    return render_template("farmer_profile.html", farmer=farmer)

@app.route("/update_profile", methods=["POST"])
def update_profile():

    farmer_id = session["user_id"]

    phone = request.form["phone"]
    password = request.form["password"]
    qr_image = request.files["qr_image"]

    # Update basic details
    if password:
        cursor.execute("""
            UPDATE farmers SET phone=%s, password=%s WHERE id=%s
        """, (phone, password, farmer_id))
    else:
        cursor.execute("""
            UPDATE farmers SET phone=%s WHERE id=%s
        """, (phone, farmer_id))

    # Update QR if uploaded
    if qr_image and qr_image.filename != "":
        filename = secure_filename(qr_image.filename)
        path = os.path.join("static/uploads", filename)
        qr_image.save(path)

        cursor.execute("""
            UPDATE farmers SET qr_image=%s WHERE id=%s
        """, (filename, farmer_id))

    conn.commit()

    return redirect("/profile")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect("/login")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


import base64
import json

# ==================== CROP CHATBOT ====================

TOLL_FREE_HELPLINES = {
    "kisan_call_center": {"number": "1800-180-1551", "name": "Kisan Call Center", "desc": "24x7 free agricultural helpline by Govt. of India (available in Kannada, Hindi, English)"},
    "pm_kisan": {"number": "155261", "name": "PM-KISAN Helpline", "desc": "For PM-KISAN scheme queries & enrollment"},
    "crop_insurance": {"number": "1800-200-7710", "name": "Crop Insurance (PMFBY)", "desc": "Pradhan Mantri Fasal Bima Yojana helpline"},
    "soil_health": {"number": "1800-180-1551", "name": "Soil Health Card", "desc": "For soil testing & health card queries"},
    "karnataka_agri": {"number": "1800-425-1552", "name": "Karnataka Agriculture Helpline", "desc": "State agriculture department helpline"},
    "animal_husbandry": {"number": "1800-180-1551", "name": "Animal Husbandry", "desc": "For livestock & dairy related queries"},
}

GOVERNMENT_SCHEMES = {
    "pm kisan": "**PM-KISAN Samman Nidhi**: ₹6,000/year in 3 installments directly to farmer's bank account. Eligibility: All landholding farmer families. Register at: pmkisan.gov.in or call 155261",
    "pmfby": "**PM Fasal Bima Yojana (PMFBY)**: Crop insurance at just 2% premium for Kharif, 1.5% for Rabi. Covers natural calamities, pests & diseases. Register through bank or CSC. Helpline: 1800-200-7710",
    "kcc": "**Kisan Credit Card (KCC)**: Get crop loans at 4% interest (with subsidy). Covers farming expenses, storage & more. Apply at any bank with land documents.",
    "soil health card": "**Soil Health Card Scheme**: Free soil testing from government labs. Get nutrient recommendations for your farm. Contact your nearest Krishi Vigyan Kendra or call 1800-180-1551",
    "e-nam": "**e-NAM (National Agriculture Market)**: Sell your produce online at the best price. Register at enam.gov.in. No middlemen — transparent bidding.",
    "mksp": "**Mahila Kisan Sashaktikaran Pariyojana**: Empowerment scheme for women farmers. Training, seed kits & financial support. Contact local agriculture office.",
    "nfsm": "**National Food Security Mission (NFSM)**: Subsidies on seeds, bio-fertilizers, farm machinery. Covers Rice, Wheat, Pulses, Coarse Cereals. Contact district agriculture officer.",
    "rkvy": "**Rashtriya Krishi Vikas Yojana (RKVY)**: State-level scheme for agriculture development. Subsidies on farm infrastructure, equipment, organic farming."
}

MSP_PRICES = {
    "paddy": {"common": 2300, "grade_a": 2320},
    "rice": {"common": 2300, "grade_a": 2320},
    "wheat": {"common": 2275},
    "jowar": {"hybrid": 3180, "maldandi": 3225},
    "bajra": {"common": 2500},
    "maize": {"common": 2090},
    "ragi": {"common": 3846},
    "tur": {"common": 7000},
    "moong": {"common": 8558},
    "urad": {"common": 6950},
    "groundnut": {"common": 6377},
    "soybean": {"yellow": 4892},
    "sunflower": {"common": 6760},
    "sugarcane": {"common": 315, "unit": "per quintal"},
    "cotton": {"medium_staple": 6620, "long_staple": 7020},
    "sesamum": {"common": 8635},
    "mustard": {"common": 5650},
    "copra": {"milling": 11160, "ball": 12000},
}

CROP_KNOWLEDGE = {
    "rice": {
        "season": "Kharif (June-November)",
        "soil": "Clayey loam soil with good water retention",
        "water": "Requires standing water (5-10 cm) during most of the growing period",
        "fertilizer": "NPK ratio 120:60:40 kg/ha. Apply urea in 3 splits",
        "harvest": "120-150 days after sowing. Harvest when 80% grains turn golden",
        "yield": "40-60 quintals/hectare with good practices",
        "spacing": "Row to row: 20 cm, Plant to plant: 15 cm",
        "seed_rate": "20-25 kg/hectare (transplanting), 80-100 kg/hectare (broadcasting)",
        "varieties": "Karnataka: Jyothi, IR-64, KRH-4, Rasi, Thanu, Jaya",
        "diseases": {
            "blast": "Caused by Magnaporthe oryzae. Symptoms: diamond-shaped lesions on leaves. Cure: Apply Tricyclazole (0.06%) or Isoprothiolane. Prevention: Use resistant varieties, avoid excess nitrogen.",
            "brown spot": "Caused by Bipolaris oryzae. Symptoms: brown oval spots on leaves. Cure: Spray Mancozeb (0.25%). Prevention: Balanced fertilizer, seed treatment with Carbendazim.",
            "bacterial leaf blight": "Caused by Xanthomonas oryzae. Symptoms: water-soaked stripes on leaves. Cure: Spray Streptocycline (0.01%). Prevention: Use resistant varieties, avoid clipping seedlings.",
            "sheath blight": "Caused by Rhizoctonia solani. Symptoms: oval lesions on leaf sheaths near water level. Cure: Spray Hexaconazole (0.1%) or Validamycin. Prevention: Avoid dense planting, drain excess water.",
            "stem borer": "Pest: Yellow stem borer. Symptoms: dead hearts in vegetative stage, white ears at heading. Cure: Apply Cartap Hydrochloride or Chlorantraniliprole. Prevention: Clip leaf tips during transplanting, light traps."
        }
    },
    "wheat": {
        "season": "Rabi (November-April)",
        "soil": "Well-drained loamy soil with pH 6.0-7.5",
        "water": "4-6 irrigations needed. Critical stages: Crown root, tillering, flowering, grain filling",
        "fertilizer": "NPK ratio 120:60:40 kg/ha",
        "harvest": "120-150 days. Harvest when grains are hard and golden",
        "yield": "35-50 quintals/hectare",
        "spacing": "Row to row: 20-23 cm",
        "seed_rate": "100-125 kg/hectare",
        "varieties": "HD-2967, PBW-343, WH-147, DBW-17, Lok-1",
        "diseases": {
            "rust": "Caused by Puccinia species. Symptoms: orange-brown pustules on leaves/stems. Cure: Spray Propiconazole (0.1%). Prevention: Use resistant varieties, early sowing.",
            "powdery mildew": "Caused by Blumeria graminis. Symptoms: white powdery patches on leaves. Cure: Spray Karathane (0.05%). Prevention: Avoid dense sowing, use resistant varieties.",
            "loose smut": "Caused by Ustilago tritici. Symptoms: black powdery mass replacing grains. Cure: Seed treatment with Carboxin or Vitavax. Prevention: Use certified disease-free seeds.",
            "karnal bunt": "Caused by Tilletia indica. Symptoms: partial bunting of grains, fishy smell. Cure: Seed treatment with Thiram + Carboxin. Prevention: Use clean seeds, avoid late sowing.",
            "aphid": "Pest: Wheat aphid. Symptoms: yellowing, honeydew on leaves. Cure: Spray Dimethoate (0.03%) or Imidacloprid. Prevention: Early sowing, natural predators like ladybugs."
        }
    },
    "maize": {
        "season": "Kharif (June-October) and Rabi (October-February)",
        "soil": "Well-drained sandy loam to loamy soil, pH 5.5-7.5",
        "water": "Requires 500-800mm rainfall. Critical at tasseling and grain filling stages",
        "fertilizer": "NPK ratio 120:60:40 kg/ha. Apply nitrogen in 3 splits",
        "harvest": "90-120 days. Harvest when husks turn brown and kernels are hard",
        "yield": "50-80 quintals/hectare (hybrid)",
        "spacing": "Row to row: 60-75 cm, Plant to plant: 20-25 cm",
        "seed_rate": "18-20 kg/hectare",
        "varieties": "Karnataka: NAH-2049, All rounder, DHM-117, Hema, Deccan-103",
        "diseases": {
            "leaf blight": "Caused by Exserohilum turcicum. Symptoms: long cigar-shaped grey-green lesions. Cure: Spray Mancozeb (0.25%). Prevention: Crop rotation, use resistant hybrids.",
            "stalk rot": "Caused by Fusarium spp. Symptoms: wilting, stalk breakage, rotting at base. Cure: Apply Carbendazim drench. Prevention: Avoid waterlogging, balanced fertilization.",
            "downy mildew": "Caused by Peronosclerospora sorghi. Symptoms: white downy growth on leaves. Cure: Spray Metalaxyl (0.2%). Prevention: Seed treatment with Metalaxyl, use resistant varieties.",
            "fall armyworm": "Pest: Spodoptera frugiperda. Symptoms: ragged holes in leaves, frass in whorl. Cure: Spray Emamectin Benzoate or Chlorantraniliprole. Prevention: Pheromone traps, early detection, intercropping."
        }
    },
    "cotton": {
        "season": "Kharif (April-December)",
        "soil": "Black cotton soil (Vertisols) with good drainage, pH 6.0-8.0",
        "water": "Requires 700-1200mm rainfall. Drip irrigation recommended",
        "fertilizer": "NPK ratio 120:60:60 kg/ha",
        "harvest": "150-180 days. Pick when bolls open fully and cotton is fluffy",
        "yield": "15-25 quintals/hectare (lint)",
        "spacing": "Row to row: 90-120 cm, Plant to plant: 45-60 cm",
        "seed_rate": "2.5-3 kg/hectare (Bt hybrid)",
        "varieties": "Bt hybrids: Bollgard-II, RCH-2, MRC-7351, Ankur-3028",
        "diseases": {
            "bacterial blight": "Caused by Xanthomonas citri. Symptoms: angular water-soaked spots on leaves. Cure: Spray Streptocycline + Copper oxychloride. Prevention: Use resistant varieties, acid-delinted seeds.",
            "fusarium wilt": "Caused by Fusarium oxysporum. Symptoms: yellowing and wilting of leaves. Cure: Soil treatment with Trichoderma viride. Prevention: Crop rotation, use wilt-resistant varieties.",
            "bollworm": "Pest by Helicoverpa armigera. Symptoms: bore holes in bolls. Cure: Spray Emamectin Benzoate (0.2%). Prevention: Use Bt cotton, pheromone traps.",
            "pink bollworm": "Pest: Pectinophora gossypiella. Symptoms: rosette flowers, damaged bolls. Cure: Spray Profenophos + Cypermethrin. Prevention: Destroy crop residues, use pheromone traps, short duration varieties.",
            "whitefly": "Pest: Bemisia tabaci. Symptoms: yellowing, sticky leaves, sooty mold. Cure: Spray Diafenthiuron or Spiromesifen. Prevention: Avoid monoculture, neem oil sprays."
        }
    },
    "tomato": {
        "season": "Year-round in most parts of India",
        "soil": "Well-drained sandy loam, pH 6.0-7.0",
        "water": "Regular watering, avoid waterlogging. Drip irrigation is ideal",
        "fertilizer": "NPK ratio 120:60:60 kg/ha with micronutrients",
        "harvest": "60-80 days after transplanting. Pick when fruits turn red/pink",
        "yield": "250-400 quintals/hectare",
        "spacing": "Row to row: 60 cm, Plant to plant: 45 cm",
        "seed_rate": "400-500 grams/hectare (nursery)",
        "varieties": "Arka Rakshak, Arka Samrat, Pusa Ruby, NS-516, Laxmi",
        "diseases": {
            "early blight": "Caused by Alternaria solani. Symptoms: dark brown spots with concentric rings on leaves. Cure: Spray Mancozeb (0.25%) or Chlorothalonil. Prevention: Crop rotation, remove infected debris.",
            "late blight": "Caused by Phytophthora infestans. Symptoms: water-soaked lesions turning brown, white mold underneath. Cure: Spray Metalaxyl + Mancozeb. Prevention: Avoid overhead irrigation, use resistant varieties.",
            "leaf curl": "Caused by Tomato Leaf Curl Virus (whitefly-transmitted). Symptoms: upward curling, stunting. Cure: No direct cure; remove infected plants. Prevention: Control whiteflies with Imidacloprid, use resistant varieties.",
            "bacterial wilt": "Caused by Ralstonia solanacearum. Symptoms: sudden wilting without yellowing. Cure: No chemical cure. Prevention: Crop rotation, use grafted seedlings, soil solarization.",
            "fruit borer": "Pest: Helicoverpa armigera. Symptoms: bore holes in fruits. Cure: Spray Neem oil or Bt. Prevention: Pheromone traps, handpicking."
        }
    },
    "potato": {
        "season": "Rabi (October-March)",
        "soil": "Well-drained sandy loam, pH 5.0-6.5",
        "water": "Regular light irrigation. Avoid waterlogging",
        "fertilizer": "NPK ratio 150:60:100 kg/ha",
        "harvest": "90-120 days. Harvest when tops die and skin is firm",
        "yield": "200-300 quintals/hectare",
        "spacing": "Row to row: 60 cm, Tuber to tuber: 20 cm",
        "seed_rate": "20-25 quintals/hectare (seed tubers)",
        "varieties": "Kufri Jyoti, Kufri Pukhraj, Kufri Badshah, Kufri Chipsona",
        "diseases": {
            "late blight": "Caused by Phytophthora infestans. Symptoms: dark water-soaked spots on leaves, white mold. Cure: Spray Mancozeb + Metalaxyl. Prevention: Use certified seed tubers, destroy infected plants.",
            "black scurf": "Caused by Rhizoctonia solani. Symptoms: black masses on tuber surface. Cure: Seed treatment with Boric acid (3%). Prevention: Crop rotation, use disease-free seed tubers.",
            "common scab": "Caused by Streptomyces scabies. Symptoms: rough corky patches on tubers. Cure: Maintain soil pH below 5.5. Prevention: Avoid lime application before planting, keep soil moist."
        }
    },
    "sugarcane": {
        "season": "Planted in January-March, harvested after 12-18 months",
        "soil": "Deep, well-drained loamy soil, pH 6.5-7.5",
        "water": "High water requirement (1500-2500mm). Critical at tillering and elongation",
        "fertilizer": "NPK ratio 250:100:120 kg/ha",
        "harvest": "12-18 months. Harvest when Brix value reaches 18-20",
        "yield": "800-1000 quintals/hectare",
        "spacing": "Row to row: 90-120 cm",
        "seed_rate": "35,000-40,000 setts/hectare",
        "varieties": "Co-86032, CoC-671, Co-62175, Co-0238",
        "diseases": {
            "red rot": "Caused by Colletotrichum falcatum. Symptoms: red discoloration inside stalk. Cure: No chemical cure; remove infected clumps. Prevention: Use resistant varieties, hot water treatment of setts.",
            "smut": "Caused by Sporisorium scitamineum. Symptoms: black whip-like structure from growing point. Cure: Remove and burn infected plants. Prevention: Use resistant varieties, treat setts with Carbendazim.",
            "grassy shoot": "Caused by Phytoplasma. Symptoms: thin tillers with grassy appearance. Cure: No cure; destroy infected plants. Prevention: Use disease-free setts, control leafhopper vectors."
        }
    },
    "ragi": {
        "season": "Kharif (June-October)",
        "soil": "Red loamy soil, well-drained, pH 5.0-7.0",
        "water": "400-500mm rainfall. Drought tolerant but responsive to irrigation",
        "fertilizer": "NPK ratio 50:40:25 kg/ha. FYM 10 tonnes/ha",
        "harvest": "100-130 days. Harvest when earheads turn brown",
        "yield": "25-35 quintals/hectare",
        "spacing": "Row to row: 30 cm, Plant to plant: 10 cm",
        "seed_rate": "5 kg/hectare (transplanting), 10 kg/hectare (broadcasting)",
        "varieties": "GPU-28, GPU-48, GPU-67, MR-1, MR-6, Indaf-15",
        "diseases": {
            "blast": "Caused by Pyricularia grisea. Symptoms: diamond-shaped spots on leaves, neck blast. Cure: Spray Tricyclazole (0.06%) or Carbendazim. Prevention: Seed treatment, resistant varieties.",
            "smut": "Caused by Melanopsichium eleusinis. Symptoms: green ear with dark smut mass. Cure: No effective chemical cure. Prevention: Use disease-free seeds, remove infected earheads."
        }
    },
    "coconut": {
        "season": "Perennial crop, planted in June-September (monsoon)",
        "soil": "Laterite, red sandy loam, alluvial soils, pH 5.5-7.0",
        "water": "Requires 1500-2500mm rainfall. Basin irrigation or drip recommended",
        "fertilizer": "Per palm/year: 500g N, 320g P2O5, 1200g K2O. Apply organic manure 25 kg/palm",
        "harvest": "First harvest after 6-8 years. Then every 45-60 days year-round",
        "yield": "80-100 nuts/palm/year",
        "spacing": "7.5m x 7.5m (triangular) or 8m x 8m (square)",
        "seed_rate": "175 palms/hectare",
        "varieties": "West Coast Tall, Chowghat Dwarf, TxD Hybrid, Lakhadweep Ordinary",
        "diseases": {
            "bud rot": "Caused by Phytophthora palmivora. Symptoms: rotting of terminal bud, yellowing of spindle leaf. Cure: Remove infected tissue, apply Bordeaux paste. Prevention: Good drainage, avoid injury to crown.",
            "root wilt": "Caused by Phytoplasma. Symptoms: flaccidity of leaflets, yellowing. Cure: No cure. Prevention: Use disease-free seedlings, manage leaf-feeding insects.",
            "rhinoceros beetle": "Pest: Oryctes rhinoceros. Symptoms: V-shaped cuts on fronds, bore holes in crown. Cure: Hook out beetles, apply Metarhizium. Prevention: Fill breeding sites, pheromone traps."
        }
    },
    "arecanut": {
        "season": "Planted in June-July (monsoon)",
        "soil": "Red laterite, well-drained loamy soil",
        "water": "Requires 1500-2000mm rainfall. Irrigate during summer",
        "fertilizer": "Per palm/year: 100g N, 40g P2O5, 140g K2O",
        "harvest": "4-5 years after planting. Harvest when nuts turn yellow-orange",
        "yield": "1.5-2.5 kg dry nuts/palm/year",
        "spacing": "2.7m x 2.7m",
        "seed_rate": "1370 palms/hectare",
        "varieties": "Mangala, Sumangala, Sreemangala, South Kanara local",
        "diseases": {
            "koleroga": "Caused by Phytophthora arecae (fruit rot). Symptoms: rotting of developing nuts during monsoon. Cure: Spray Bordeaux mixture (1%) before monsoon. Prevention: Remove diseased bunches, improve drainage.",
            "yellow leaf disease": "Caused by Phytoplasma. Symptoms: yellowing of lower leaves. Cure: No chemical cure. Prevention: Use healthy seedlings, remove infected palms."
        }
    }
}

PLANT_DISEASE_SYMPTOMS = {
    "yellow leaves": {"diseases": ["nitrogen deficiency", "iron chlorosis", "fusarium wilt", "magnesium deficiency"], "crops": ["all"], "advice": "Check for nutrient deficiency first. Apply balanced NPK fertilizer. If yellowing starts from lower leaves, it's likely nitrogen deficiency — apply urea (46-0-0) at 50kg/ha. If veins remain green (interveinal chlorosis), it's iron chlorosis — spray ferrous sulfate (FeSO4) 0.5%. If yellowing is on older leaves between veins, it may be magnesium deficiency — apply MgSO4 (25kg/ha).\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"},
    "brown spots": {"diseases": ["fungal leaf spot", "bacterial blight", "early blight", "Cercospora leaf spot"], "crops": ["all"], "advice": "Likely a fungal infection. Spray Mancozeb (0.25%) or Copper oxychloride (0.3%). Remove and destroy severely infected leaves. Improve air circulation. If spots have concentric rings → likely Alternaria (early blight). If spots have yellow halo → likely bacterial.\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"},
    "white powder": {"diseases": ["powdery mildew"], "crops": ["all"], "advice": "Powdery mildew detected. Spray Karathane (0.05%) or sulfur-based fungicide (Sulphur 80% WP at 3g/L). Avoid overhead irrigation. Improve spacing between plants. Apply in early morning or evening.\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"},
    "wilting": {"diseases": ["fusarium wilt", "bacterial wilt", "root rot", "verticillium wilt"], "crops": ["all"], "advice": "Could be wilt disease or root rot. Quick test: cut the stem — if vascular tissue is brown, it's wilt. Check roots — if brown and mushy, it's root rot.\n\n**For wilt**: Apply Trichoderma viride (4g/kg seed or 2.5kg/ha in soil). **For root rot**: Improve drainage, apply Metalaxyl.\n\nSoil solarization during summer can prevent both.\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"},
    "holes in leaves": {"diseases": ["caterpillar damage", "beetle damage", "leaf miner"], "crops": ["all"], "advice": "Pest damage detected. **For caterpillars**: spray Neem oil (5ml/L) or Bacillus thuringiensis (Bt) at 1g/L. **For beetles**: spray Carbaryl (0.1%). **For leaf miners** (serpentine marks): spray Abamectin. Use pheromone traps for monitoring. Prefer biological control first.\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"},
    "curling leaves": {"diseases": ["viral infection", "aphid damage", "leaf curl virus", "thrips damage"], "crops": ["all"], "advice": "Likely viral infection transmitted by whiteflies/aphids/thrips. **Step 1**: Control vectors — spray Imidacloprid (0.3ml/L) or Thiamethoxam. **Step 2**: Remove and destroy infected plants. **Step 3**: Use yellow/blue sticky traps. No cure for viral infections — prevention is key!\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"},
    "black spots": {"diseases": ["anthracnose", "black spot disease", "sooty mold", "Sigatoka"], "crops": ["all"], "advice": "Likely fungal disease. Spray Carbendazim (0.1%) or Copper fungicide (Copper oxychloride 3g/L). Remove infected plant parts. Maintain field hygiene. If there's a sticky substance below → likely sooty mold (control the insects causing honeydew).\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"},
    "rotting": {"diseases": ["stem rot", "root rot", "fruit rot", "collar rot"], "crops": ["all"], "advice": "Rotting indicates excess moisture or fungal attack. **Immediate**: Remove rotting parts, improve drainage. **For root/collar rot**: Drench soil with Metalaxyl (2g/L) or Carbendazim (1g/L). **For fruit rot**: Spray Mancozeb before fruiting stage. Apply Trichoderma viride to soil as preventive.\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"},
    "stunted growth": {"diseases": ["nematode damage", "nutrient deficiency", "viral infection", "zinc deficiency"], "crops": ["all"], "advice": "Check roots for knots (nematodes) — apply Carbofuran (1kg a.i./ha) if found. Test soil for nutrient deficiency. **Zinc deficiency** (common in rice/maize): apply ZnSO4 25kg/ha. If leaves show mosaic/mottling pattern, it's viral — remove infected plants immediately.\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"},
    "mold": {"diseases": ["downy mildew", "grey mold", "white mold"], "crops": ["all"], "advice": "Fungal mold detected. **Downy mildew** (grey-purple mold on leaf underside): Spray Metalaxyl + Mancozeb. **Grey mold** (fuzzy grey growth): spray Iprodione, improve ventilation. **White mold** (cottony growth): spray Carbendazim. Reduce humidity around plants.\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"},
    "dry leaves": {"diseases": ["drought stress", "bacterial leaf scorch", "spider mite damage"], "crops": ["all"], "advice": "Could be water stress, nutrient deficiency, or spider mite damage. **Check underside of leaves** for tiny mites/webs → spray Dicofol or sulfur. **If soil is dry**: irrigate immediately, apply mulch. **If tips are burning** → possible salt/fertilizer burn, flush with water.\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"},
    "white insects": {"diseases": ["whitefly infestation", "mealybug"], "crops": ["all"], "advice": "**Whiteflies** (tiny white flying insects under leaves): Spray Imidacloprid (0.3ml/L) or Thiamethoxam. Use yellow sticky traps. **Mealybugs** (white cottony masses): Spray Neem oil (5ml/L) or Profenophos. Remove severely infested parts. Encourage natural enemies like ladybugs.\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"},
    "fruit dropping": {"diseases": ["hormonal imbalance", "nutrient deficiency", "pest damage"], "crops": ["all"], "advice": "Premature fruit drop can be caused by: **Water stress** → maintain regular irrigation. **Boron deficiency** → spray Borax (0.2%). **Pest damage** → check for fruit fly or borer. Spray NAA (Naphthalene Acetic Acid) 20ppm to reduce fruit drop.\n\n📞 Need expert help? Call Kisan Helpline: **1800-180-1551** (toll-free, 24x7)"}
}

FARMING_TIPS = {
    "intercropping": "**Intercropping Suggestions**:\n• Maize + Soybean/Groundnut\n• Sugarcane + Onion/Garlic\n• Coconut + Cocoa/Pepper/Banana\n• Arecanut + Pepper/Cocoa\n• Cotton + Black gram\n\nBenefits: Better land use, pest reduction, extra income!",
    "composting": "**How to Make Vermicompost**:\n1. Build a bed (6ft x 3ft x 2ft) in shade\n2. Layer: crop residues → cow dung → soil\n3. Add Eisenia fetida (red earthworms) — 1kg per bed\n4. Maintain moisture (40-50%), cover with jute sack\n5. Turn every 15 days\n6. Ready in 60-90 days\n\nYield: ~300-400 kg per bed per batch",
    "drip": "**Drip Irrigation Benefits**:\n• Saves 30-60% water\n• Increases yield by 20-40%\n• Subsidy: 55-90% under PMKSY (Micro Irrigation)\n• Apply through agriculture department\n• Cost: ₹40,000-1,00,000/hectare (before subsidy)\n\n📞 Contact: Karnataka Agriculture Helpline **1800-425-1552**",
    "mulching": "**Mulching Benefits**:\n• Conserves soil moisture (30-50% less irrigation)\n• Controls weeds naturally\n• Regulates soil temperature\n• Materials: Straw, dry leaves, black polyethylene\n• Apply 5-10 cm thick organic mulch after planting",
    "storage": "**Post-Harvest Storage Tips**:\n• Dry grains to 12-14% moisture before storing\n• Use airtight containers or hermetic bags\n• Add Neem leaves between grain layers\n• Store in cool, dry place on raised platform\n• Check regularly for pest infestation\n• For cold storage crops: maintain 2-4°C for potato, 10-12°C for tomato"
}

def get_chatbot_response(message):
    """Process chatbot message and return appropriate response."""
    msg = message.lower().strip()

    # Greetings
    if any(w in msg for w in ["hello", "hi", "hey", "namaste", "namaskar", "vanakkam"]):
        return ("Hello! 👨‍🌾 I'm your **Agrizy Crop Assistant**. I can help you with:\n\n"
                "🌾 **Crop info** — Ask about any crop (rice, wheat, maize, ragi, coconut, arecanut & more)\n"
                "🦠 **Disease diagnosis** — Upload a photo or describe symptoms\n"
                "💊 **Treatment & cure** — Get medicine recommendations\n"
                "💰 **MSP prices** — Current minimum support prices\n"
                "📋 **Government schemes** — PM-KISAN, PMFBY, KCC & more\n"
                "📞 **Helpline numbers** — Toll-free farmer helplines\n\n"
                "📞 **Kisan Call Center: 1800-180-1551** (Toll-Free, 24x7)\n\n"
                "Try: *'Tell me about rice'*, *'MSP of wheat'*, *'schemes'*, or *'helpline'*")

    # Help
    if any(w in msg for w in ["help", "what can you do", "options", "menu"]):
        return ("I can help with:\n\n"
                "1️⃣ **Crop Info** — 'Tell me about wheat', 'Ragi varieties'\n"
                "2️⃣ **Disease Help** — 'My leaves have brown spots', 'How to cure blast?'\n"
                "3️⃣ **Upload Photo** — Click 📷 to upload an infected plant photo\n"
                "4️⃣ **MSP Prices** — 'MSP of rice', 'What is MSP of cotton?'\n"
                "5️⃣ **Govt Schemes** — 'PM KISAN', 'crop insurance', 'KCC'\n"
                "6️⃣ **Farming Tips** — 'intercropping', 'drip irrigation', 'composting'\n"
                "7️⃣ **Helpline** — 'helpline', 'toll free number', 'call'\n\n"
                "📞 **24x7 Kisan Helpline: 1800-180-1551** (Toll-Free)")

    # Helpline / toll-free number queries
    if any(w in msg for w in ["helpline", "toll free", "tollfree", "phone", "call", "number", "contact", "dial", "emergency"]):
        response = "📞 **Farmer Toll-Free Helpline Numbers**:\n\n"
        for key, info in TOLL_FREE_HELPLINES.items():
            response += f"☎️ **{info['name']}**: **{info['number']}**\n   {info['desc']}\n\n"
        response += "💡 All numbers are **toll-free** — no charges apply!\n"
        response += "⏰ Kisan Call Center (1800-180-1551) is available **24 hours, 7 days a week** in your local language."
        return response

    # MSP queries
    if any(w in msg for w in ["msp", "minimum support price", "support price", "government price"]):
        # Check for specific crop MSP
        for crop, prices in MSP_PRICES.items():
            if crop in msg:
                response = f"💰 **MSP of {crop.title()} (2024-25)**:\n\n"
                for grade, price in prices.items():
                    if grade == "unit":
                        continue
                    unit = prices.get("unit", "per quintal")
                    response += f"• **{grade.replace('_', ' ').title()}**: ₹{price} {unit}\n"
                response += f"\n📞 For queries: **PM-KISAN Helpline: 155261**"
                return response

        # Show all MSP
        response = "💰 **Minimum Support Prices (MSP) 2024-25**:\n\n"
        for crop, prices in MSP_PRICES.items():
            main_price = list(prices.values())[0]
            if isinstance(main_price, int):
                response += f"• **{crop.title()}**: ₹{main_price}/quintal\n"
        response += f"\n📞 For queries: **PM-KISAN Helpline: 155261**"
        return response

    # Government schemes
    if any(w in msg for w in ["scheme", "government", "subsidy", "yojana", "pm kisan", "pmfby", "kcc", "credit card", "insurance", "e-nam", "enam", "nfsm", "rkvy"]):
        # Check for specific scheme
        for key, info in GOVERNMENT_SCHEMES.items():
            if key in msg or any(w in msg for w in key.split()):
                return f"📋 {info}"

        # Show all schemes
        response = "📋 **Government Schemes for Farmers**:\n\n"
        for key, info in GOVERNMENT_SCHEMES.items():
            name = info.split("**")[1] if "**" in info else key.upper()
            response += f"• **{name}** — Type '{key}' for details\n"
        response += "\n📞 **PM-KISAN Helpline: 155261** | **Crop Insurance: 1800-200-7710**"
        return response

    # Farming tips
    for tip_key, tip_info in FARMING_TIPS.items():
        if tip_key in msg or any(w in msg for w in tip_key.split()):
            return f"🌱 {tip_info}\n\n📞 **Kisan Helpline: 1800-180-1551**"

    # Check for specific crop queries
    for crop, info in CROP_KNOWLEDGE.items():
        if crop in msg:
            # Season question
            if any(w in msg for w in ["season", "when to plant", "when to sow", "when to grow", "planting time"]):
                return f"🌱 **{crop.title()} Season**: {info['season']}\n\n📞 **Kisan Helpline: 1800-180-1551**"

            # Soil question
            if any(w in msg for w in ["soil", "land", "ground"]):
                return f"🌍 **{crop.title()} Soil Requirement**: {info['soil']}\n\n📞 **Kisan Helpline: 1800-180-1551**"

            # Water question
            if any(w in msg for w in ["water", "irrigation", "rain"]):
                return f"💧 **{crop.title()} Water Needs**: {info['water']}\n\n📞 **Kisan Helpline: 1800-180-1551**"

            # Fertilizer question
            if any(w in msg for w in ["fertilizer", "manure", "nutrient", "npk", "urea"]):
                return f"🧪 **{crop.title()} Fertilizer**: {info['fertilizer']}\n\n📞 **Kisan Helpline: 1800-180-1551**"

            # Harvest question
            if any(w in msg for w in ["harvest", "pick", "collect", "ready"]):
                return f"🌾 **{crop.title()} Harvest**: {info['harvest']}\n\n📞 **Kisan Helpline: 1800-180-1551**"

            # Yield question
            if any(w in msg for w in ["yield", "production", "output", "how much"]):
                return f"📊 **{crop.title()} Expected Yield**: {info.get('yield', 'Data not available')}\n\n📞 **Kisan Helpline: 1800-180-1551**"

            # Variety question
            if any(w in msg for w in ["variety", "varieties", "type", "hybrid", "seed"]):
                return f"🌱 **{crop.title()} Recommended Varieties**: {info.get('varieties', 'Contact your local KVK for variety recommendations')}\n\n**Seed rate**: {info.get('seed_rate', 'N/A')}\n\n📞 **Kisan Helpline: 1800-180-1551**"

            # Spacing question
            if any(w in msg for w in ["spacing", "distance", "gap", "planting distance"]):
                return f"📏 **{crop.title()} Spacing**: {info.get('spacing', 'Contact your local KVK')}\n\n📞 **Kisan Helpline: 1800-180-1551**"

            # Disease questions for specific crop
            for disease, cure in info.get("diseases", {}).items():
                if disease in msg:
                    return f"🦠 **{crop.title()} — {disease.title()}**:\n\n{cure}\n\n📞 **Kisan Helpline: 1800-180-1551**"

            # General disease question about this crop
            if any(w in msg for w in ["disease", "infection", "problem", "cure", "treatment"]):
                response = f"🦠 **Common {crop.title()} Diseases & Pests**:\n\n"
                for disease, cure in info.get("diseases", {}).items():
                    response += f"**{disease.title()}**: {cure}\n\n"
                response += "📞 **Kisan Helpline: 1800-180-1551** (Toll-Free, 24x7)"
                return response

            # General info about the crop
            return (f"🌾 **{crop.title()} — Complete Guide**:\n\n"
                    f"📅 **Season**: {info['season']}\n"
                    f"🌍 **Soil**: {info['soil']}\n"
                    f"💧 **Water**: {info['water']}\n"
                    f"🧪 **Fertilizer**: {info['fertilizer']}\n"
                    f"📏 **Spacing**: {info.get('spacing', 'N/A')}\n"
                    f"🌱 **Varieties**: {info.get('varieties', 'N/A')}\n"
                    f"📊 **Yield**: {info.get('yield', 'N/A')}\n"
                    f"🌾 **Harvest**: {info['harvest']}\n\n"
                    f"Ask me about diseases, varieties, or upload a plant photo!\n\n"
                    f"📞 **Kisan Helpline: 1800-180-1551**")

    # Symptom-based diagnosis
    for symptom, data in PLANT_DISEASE_SYMPTOMS.items():
        if symptom in msg or any(w in msg for w in symptom.split()):
            possible = ", ".join(data["diseases"])
            return (f"🔍 **Symptom Detected: {symptom.title()}**\n\n"
                    f"**Possible causes**: {possible}\n\n"
                    f"**Recommended Action**: {data['advice']}\n\n"
                    f"💡 Upload a photo using 📷 for better diagnosis.")

    # General farming questions
    if any(w in msg for w in ["organic", "natural", "chemical free", "jaivik"]):
        return ("🌿 **Organic Farming Tips**:\n\n"
                "• **Pest control**: Neem oil (5ml/L), Panchagavya, Dashaparni\n"
                "• **Fertilizer**: Vermicompost, Jeevamrutha, Bio-NPK\n"
                "• **Disease prevention**: Trichoderma viride, Pseudomonas fluorescens\n"
                "• **Practice**: Crop rotation, intercropping, mulching\n"
                "• **Certification**: Apply for organic certification through APEDA/PGS\n\n"
                "📋 **PKVY (Paramparagat Krishi Vikas Yojana)**: ₹50,000/ha over 3 years for organic farming\n\n"
                "📞 **Kisan Helpline: 1800-180-1551**")

    if any(w in msg for w in ["pest", "insect", "bug", "keet"]):
        return ("🐛 **Integrated Pest Management (IPM)**:\n\n"
                "**Biological**: Neem oil (5ml/L), Bt spray, Trichogramma cards\n"
                "**Mechanical**: Yellow/Blue sticky traps, pheromone traps, light traps\n"
                "**Chemical (last resort)**:\n"
                "• Sucking pests → Imidacloprid (0.3ml/L)\n"
                "• Caterpillars → Emamectin Benzoate (0.2g/L)\n"
                "• Mites → Dicofol or Sulphur\n"
                "• Fruit fly → Methyl Eugenol traps\n\n"
                "⚠️ Always follow label recommendations. Maintain safe harvest interval.\n\n"
                "📞 **Kisan Helpline: 1800-180-1551**")

    if any(w in msg for w in ["weather", "climate", "rain", "monsoon", "forecast"]):
        return ("🌤️ **Weather & Climate Tips**:\n\n"
                "• Check daily forecasts: **mausam.imd.gov.in** or **Meghdoot app**\n"
                "• Don't spray pesticides before expected rain\n"
                "• Drain excess water during heavy monsoon\n"
                "• Protect nurseries from frost (Dec-Jan) using covers\n"
                "• Harvest & dry produce before predicted rain\n\n"
                "📱 Download **Meghdoot** or **Damini** (lightning alert) app\n\n"
                "📞 **Kisan Helpline: 1800-180-1551**")

    if any(w in msg for w in ["market", "sell", "price", "mandi", "where to sell"]):
        return ("🏪 **Market & Selling Tips**:\n\n"
                "• **e-NAM**: Register at enam.gov.in to sell online at best prices\n"
                "• **APMC Mandi**: Check rates at agmarknet.gov.in\n"
                "• **FPO**: Join Farmer Producer Organization for collective bargaining\n"
                "• **Direct sale**: Use Agrizy platform to sell directly to consumers!\n"
                "• **Cold storage**: For perishables, use local cold storage facilities\n\n"
                "📞 **Kisan Helpline: 1800-180-1551**")

    if any(w in msg for w in ["loan", "bank", "finance", "credit", "money"]):
        return ("🏦 **Agricultural Finance**:\n\n"
                "• **KCC (Kisan Credit Card)**: Crop loan at 4% interest (with subsidy). Apply at any bank.\n"
                "• **NABARD**: Refinance for agriculture & allied activities\n"
                "• **PM-KISAN**: ₹6,000/year directly to bank account\n"
                "• **Crop Insurance (PMFBY)**: Just 2% premium for Kharif, 1.5% for Rabi\n\n"
                "📞 **PM-KISAN Helpline: 155261**\n"
                "📞 **Crop Insurance: 1800-200-7710**\n"
                "📞 **Kisan Helpline: 1800-180-1551**")

    if any(w in msg for w in ["thank", "thanks", "dhanyavaad", "dhanyawad"]):
        return ("You're welcome! 🙏 Happy farming! 🌾\n\n"
                "Remember, I'm always here to help. Just ask!\n\n"
                "📞 **24x7 Kisan Helpline: 1800-180-1551** (Toll-Free)")

    if any(w in msg for w in ["bye", "goodbye", "exit", "quit"]):
        return ("Goodbye! 👋 Happy farming! 🌾\n\n"
                "Come back anytime for crop advice.\n\n"
                "📞 **24x7 Kisan Helpline: 1800-180-1551** (Toll-Free)")

    # Default response
    return ("I'm not sure about that. Try asking about:\n\n"
            "🌾 **Crops**: 'Tell me about rice', 'Ragi varieties'\n"
            "🦠 **Symptoms**: 'My leaves have brown spots'\n"
            "📷 **Photo**: Upload an image using the 📷 button\n"
            "💰 **MSP**: 'MSP of wheat', 'minimum support price'\n"
            "📋 **Schemes**: 'PM KISAN', 'crop insurance'\n"
            "🌱 **Tips**: 'intercropping', 'drip irrigation'\n"
            "📞 **Helpline**: 'toll free number'\n\n"
            "**Available crops**: Rice, Wheat, Maize, Cotton, Tomato, Potato, Sugarcane, Ragi, Coconut, Arecanut\n\n"
            "📞 **Kisan Helpline: 1800-180-1551** (Toll-Free, 24x7)")


def analyze_plant_image(description):
    """Analyze plant image based on user description and return diagnosis."""
    desc = description.lower() if description else ""

    # Try to match symptoms from description
    for symptom, data in PLANT_DISEASE_SYMPTOMS.items():
        if symptom in desc or any(w in desc for w in symptom.split()):
            possible = ", ".join(data["diseases"])
            return (f"📸 **Image Analysis Result**:\n\n"
                    f"🔍 **Detected Symptom**: {symptom.title()}\n"
                    f"🦠 **Possible Diseases**: {possible}\n\n"
                    f"💊 **Treatment**: {data['advice']}\n\n"
                    f"⚠️ For accurate diagnosis, consult your nearest **Krishi Vigyan Kendra (KVK)**.\n\n"
                    f"📞 **Kisan Helpline: 1800-180-1551** (Toll-Free, 24x7)")

    return ("📸 **Image Received!**\n\n"
            "I can see your plant photo. Please also describe the symptoms:\n\n"
            "• What color are the spots? (yellow, brown, black, white)\n"
            "• Which part is affected? (leaves, stem, fruit, roots)\n"
            "• Any wilting, curling, holes, or mold?\n"
            "• Is there any sticky substance or insects visible?\n\n"
            "This will help me give a better diagnosis.\n\n"
            "📞 **Kisan Helpline: 1800-180-1551** (Toll-Free, 24x7)")


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    message = data.get('message', '')
    image_data = data.get('image', None)
    image_description = data.get('description', '')

    if image_data:
        response = analyze_plant_image(image_description)
    else:
        response = get_chatbot_response(message)

    return jsonify({"response": response})


CROP_IMAGES = {
    "Rice": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop",
    "Wheat": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=300&fit=crop",
    "Maize": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400&h=300&fit=crop",
    "Cotton": "https://images.unsplash.com/photo-1616431101997-8aa4de292054?w=400&h=300&fit=crop",
    "Jowar(Sorghum)": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=400&h=300&fit=crop",
    # "Ragi": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=400&h=300&fit=crop",
    # "Tomato": "https://images.unsplash.com/photo-1546470427-0d4db154ceb8?w=400&h=300&fit=crop",
    # "Onion": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=400&h=300&fit=crop",
    # "Potato": "https://images.unsplash.com/photo-1518977676601-b53f82ber8a3?w=400&h=300&fit=crop",
    # "Green Chilli": "https://images.unsplash.com/photo-1588252303782-cb80119abd6d?w=400&h=300&fit=crop",
    # "Chilli Red": "https://images.unsplash.com/photo-1583119022894-919a68a3d0e3?w=400&h=300&fit=crop",
    # "Brinjal": "https://images.unsplash.com/photo-1615484477778-ca3b77940c25?w=400&h=300&fit=crop",
    # "Banana": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&h=300&fit=crop",
    # "Coconut": "https://images.unsplash.com/photo-1580984969071-a8da5656c2fb?w=400&h=300&fit=crop",
    # "Groundnut": "https://images.unsplash.com/photo-1567892737950-30c4db37cd89?w=400&h=300&fit=crop",
    # "Sunflower": "https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=400&h=300&fit=crop",
    # "Sugarcane": "https://images.unsplash.com/photo-1562593028-bdd7bb01a683?w=400&h=300&fit=crop",
    # "Turmeric": "https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=400&h=300&fit=crop",
    # "Ginger": "https://images.unsplash.com/photo-1615485291926-e3b368888dfd?w=400&h=300&fit=crop",
    # "Garlic": "https://images.unsplash.com/photo-1540148426945-6cf22a6b2f85?w=400&h=300&fit=crop",
     "Coriander(Leaves)": "https://images.unsplash.com/photo-1592928302636-c83cf1e1c817?w=400&h=300&fit=crop",
    # "Capsicum": "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=400&h=300&fit=crop",
    # "Cabbage": "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=400&h=300&fit=crop",
    # "Cauliflower": "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400&h=300&fit=crop",
    # "Carrot": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400&h=300&fit=crop",
    # "Beans": "https://images.unsplash.com/photo-1567375698348-5d9d5ae10c3a?w=400&h=300&fit=crop",
    # "Bitter gourd": "https://images.unsplash.com/photo-1604145559206-e3b5f3adbe65?w=400&h=300&fit=crop",
    # "Bottle gourd": "https://images.unsplash.com/photo-1622943590528-430ba21ca833?w=400&h=300&fit=crop",
    # "Cucumber": "https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=400&h=300&fit=crop",
    # "Drumstick": "https://images.unsplash.com/photo-1622943590528-430ba21ca833?w=400&h=300&fit=crop",
    # "Ladies Finger": "https://images.unsplash.com/photo-1425543103986-22abb7d7e8d2?w=400&h=300&fit=crop",
    # "Mango": "https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=300&fit=crop",
    # "Papaya": "https://images.unsplash.com/photo-1517282009859-f000ec3b26fe?w=400&h=300&fit=crop",
    # "Grapes": "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=400&h=300&fit=crop",
    # "Pomegranate": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400&h=300&fit=crop",
    # "Lemon": "https://images.unsplash.com/photo-1590502593747-42a996133562?w=400&h=300&fit=crop",
    # "Orange": "https://images.unsplash.com/photo-1547514701-42782101795e?w=400&h=300&fit=crop",
    # "Arecanut(Betelnut/Supari)": "https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?w=400&h=300&fit=crop",
    # "Black pepper": "https://images.unsplash.com/photo-1599909533002-c81e40f0853e?w=400&h=300&fit=crop",
    # "Cardamom": "https://images.unsplash.com/photo-1596547609652-9cf5d8c10616?w=400&h=300&fit=crop",
    # "Coffee": "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400&h=300&fit=crop",
    # "Cashewnuts": "https://images.unsplash.com/photo-1563292769-4e05b684851a?w=400&h=300&fit=crop",
    # "Peas": "https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=400&h=300&fit=crop",
    # "Soyabean": "https://images.unsplash.com/photo-1599058917212-d750089bc07e?w=400&h=300&fit=crop",
    # "Bengal Gram(Gram)(Whole)": "https://images.unsplash.com/photo-1612257416648-ee7a6c5b4060?w=400&h=300&fit=crop",
    # "Tur/Arhar Dal": "https://images.unsplash.com/photo-1612257416648-ee7a6c5b4060?w=400&h=300&fit=crop",
    # "Green Gram (Moong)(Whole)": "https://images.unsplash.com/photo-1612257416648-ee7a6c5b4060?w=400&h=300&fit=crop",
    # "Bajra(Pearl Millet/Cumbu)": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=400&h=300&fit=crop",
    # "Paddy(Dhan)(Common)": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop",
    # "Copra": "https://images.unsplash.com/photo-1580984969071-a8da5656c2fb?w=400&h=300&fit=crop",
    "Dry Chillies": "https://images.unsplash.com/photo-1583119022894-919a68a3d0e3?w=400&h=300&fit=crop",
    # "Tamarind Fruit": "https://images.unsplash.com/photo-1590301157890-4810ed352733?w=400&h=300&fit=crop",
    # "Jackfruit": "https://images.unsplash.com/photo-1528825871115-3581a5387919?w=400&h=300&fit=crop",
    # "Watermelon": "https://images.unsplash.com/photo-1563114773-84221bd62daa?w=400&h=300&fit=crop",
    # "Pumpkin": "https://images.unsplash.com/photo-1570586437263-ab629fccc818?w=400&h=300&fit=crop",
    # "Sweet Potato": "https://images.unsplash.com/photo-1596097635121-14b63a7fe734?w=400&h=300&fit=crop",
    # "Beetroot": "https://images.unsplash.com/photo-1593105544559-ecb03bf76f82?w=400&h=300&fit=crop",
    # "Radish": "https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=400&h=300&fit=crop",
    # "Spinach": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400&h=300&fit=crop",
    # "Methi(Fenugreek Leaves)": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400&h=300&fit=crop",
    "Guava": "https://images.unsplash.com/photo-1536511132770-e5058c7e8c46?w=400&h=300&fit=crop",
    # "Sapota": "https://images.unsplash.com/photo-1536511132770-e5058c7e8c46?w=400&h=300&fit=crop",
    # "Sesamum(Sesame,Gingelly,Til)": "https://images.unsplash.com/photo-1599058917212-d750089bc07e?w=400&h=300&fit=crop",
    # "Castor Seed": "https://images.unsplash.com/photo-1599058917212-d750089bc07e?w=400&h=300&fit=crop",
    # "Linseed": "https://images.unsplash.com/photo-1599058917212-d750089bc07e?w=400&h=300&fit=crop",
    # "Mustard": "https://images.unsplash.com/photo-1599058917212-d750089bc07e?w=400&h=300&fit=crop",
"Arhar Dal(Tur Dal)":  "https://sumangrocery.in/public/uploads/media/Ohoa7vxjTF2Cd42llbMZsGJCoeeBSSc3D7ecwpAi.jpg",
"Garlic": "https://i.guim.co.uk/img/media/43442656c722147e053264b6b914b3258642db2e/0_37_3812_2290/master/3812.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=24943c703401dec3d0e8e0da56fec7aa",
"Ginger(Green)": "https://img1.exportersindia.com/product_images/bc-full/2025/4/13646452/fresh-green-ginger-1744628096-7998609.jpeg",
"Bitter gourd": "https://orgfarm.store/cdn/shop/files/Bitter-Gourds.png?v=1721729267&width=1214",
"Apple": "https://freshindiaorganics.com/cdn/shop/products/Apples.jpg?v=1686739530",
"Chikoos(Sapota)": "https://www.lakshmiwholesale.com/cdn/shop/files/fresh-sapota-500x500-1_1800x1800_56b7d302-1de4-44ce-b3b1-d23ac5e46855.jpg?v=1749642943",
"Thondekai": "https://5.imimg.com/data5/SELLER/Default/2020/9/RF/VZ/CA/50068616/fresh-ivy-gourd-thondekai-.jpg",
"Drumstick": "https://naturesproduce.com/wp-content/uploads/2018/08/drumsticks.png",
"Gur(Jaggery)": "https://5.imimg.com/data5/GJ/DU/GX/SELLER-80072581/jaggery-gur.jpg",
"Green Gram(Moong)(Whole)": "https://m.media-amazon.com/images/I/51-w170vUwL._AC_UF894,1000_QL80_.jpg",
"Grapes": "https://exim.stedderglobal.com/wp-content/uploads/2025/07/grapes.png",
"Cauliflower": "https://www.thespruce.com/thmb/3xv-bplva31jK5D9fYL0_5c9UB0=/4696x0/filters:no_upscale():max_bytes(150000):strip_icc()/how-to-grow-cauliflower-1403494-hero-76cf5f524a564adabb1ac6adfa311482.jpg",
"Ladies Finger": "https://khetose.com/wp-content/uploads/2025/06/lady-finger.webp",
"Pomegranate": "https://www.simplyrecipes.com/thmb/FPv4xdsPSGRseeU0-wuKdFp1vNE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/__opt__aboutcom__coeus__resources__content_migration__simply_recipes__uploads__2013__11__how-to-cut-pomegranate-horiz-a-1800-81c587bf93ab48bfb9ea7afea4d76c4c.jpg",
"Bajra(Pearl Millet/Cumbu)": "https://5.imimg.com/data5/GP/XM/ND/SELLER-75209402/cumbu.jpg",
"Safflower": "https://th-i.thgim.com/public/incoming/83n4ht/article70834751.ece/alternates/LANDSCAPE_1200/KUDSV_22-12-2012_19-34-18_DSC_6751.JPG",
"Tamarind Seed": "https://m.media-amazon.com/images/I/51vonDsdiyL._AC_UF350,350_QL80_.jpg",
"Raddish": "https://t4.ftcdn.net/jpg/08/21/85/13/360_F_821851379_t2KZkO5WgZxosEhmubbAZVYajNgew9vP.jpg",
"Chilly Capsicum": "https://images.picxy.com/cache/2019/2/20/7f73a7c30b51f94170bd4a2a7dcd5c64.jpg",
"Snakeguard": "https://cdn.britannica.com/45/190845-050-1EAF48FA/snake-gourds.jpg",
"Seemebadnekai": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1b1s8dT6TrU6fF8dowjesTrSVoRKw6AAcYA&s",
"Banana": "https://www.southernliving.com/thmb/EM-f8L_T36WluwBtBkhD4gnCKg8=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/How_To_Freeze_Bananas_023-71e81efacb6a4d87a3596b8c2c519884.jpg",
"Cashewnuts": "https://sandigeatdoors.com/wp-content/uploads/2022/12/Sandige-At-Doors-Casews-_-Godambi.jpg",
"Orange": "https://www.allrecipes.com/thmb/y_uvjwXWAuD6T0RxaS19jFvZyFU=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/GettyImages-1205638014-2000-d0fbf9170f2d43eeb046f56eec65319c.jpg",
"Beetroot": "https://www.oifood.in/files/products/c401b43a628d3c11ef07a5ba08a766ab.jpg",
"Black Gram Dal(Urd Dal)": "https://cpimg.tistatic.com/6923679/b/1/whole-black-gram-urad-dal.jpg",
"Ashgourd": "https://i.cdn.newsbytesapp.com/images/l39820250618123218.jpeg",
"Turmeric": "https://5.imimg.com/data5/JE/QF/MY-52317897/turmeric-finger-500x500-500x500.jpg",
"Tender Coconut": "https://images.unsplash.com/photo-1603779046675-2eccbab9b982?q=80&w=1333&auto=format&fit=crop",
"Cucumbar(Kheera)": "https://images.unsplash.com/photo-1604977042946-1eecc30f269e?q=80&w=1160&auto=format&fit=crop",
"Kulthi(Horse Gram)": "https://images.unsplash.com/photo-1763368392508-3d4bddfdd20a?q=80&w=1205&auto=format&fit=crop",
"Copra": "https://images.unsplash.com/photo-1683647986183-bbe4af2a38ea?q=80&w=1170&auto=format&fit=crop",
"Black pepper": "https://plus.unsplash.com/premium_photo-1726072357017-0af7b90a463d?q=80&w=1170&auto=format&fit=crop",
"Cowpea(Lobia/Karamani)": "https://plus.unsplash.com/premium_photo-1726072356922-e8c00cc78ef8?q=80&w=2070&auto=format&fit=crop",
"Black Gram(Urd Beans)(Whole)": "https://plus.unsplash.com/premium_photo-1675237625048-de2dc05e70d3?q=80&w=1770&auto=format&fit=crop",
"Ragi(Finger Millet)": "https://images.unsplash.com/photo-1653580524515-77b19c176b88?q=80&w=1674&auto=format&fit=crop",
"Castor Seed": "https://plus.unsplash.com/premium_photo-1674654419508-94925f047539?q=80&w=2070&auto=format&fit=crop",
"Tamarind Fruit": "https://images.unsplash.com/photo-1765292745796-972d34894d68?q=80&w=2072&auto=format&fit=crop",
"Tomato": "https://images.unsplash.com/photo-1561136594-7f68413baa99?q=80&w=2070&auto=format&fit=crop",
"Potato": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?q=80&w=2070&auto=format&fit=crop",
"Beans": "https://plus.unsplash.com/premium_photo-1725384940646-ef6aa8c2a091?q=80&w=2071&auto=format&fit=crop",
"Carrot": "https://images.unsplash.com/photo-1633380110125-f6e685676160?q=80&w=2071&auto=format&fit=crop",
"Sunflower": "https://images.unsplash.com/photo-1635843111961-06c71c3ed8cf?q=80&w=2070&auto=format&fit=crop",
"Brinjal": "https://images.unsplash.com/photo-1683543122945-513029986574?q=80&w=1674&auto=format&fit=crop",
"Cabbage": "https://images.unsplash.com/photo-1652860213441-6622f9fec77f?q=80&w=2073&auto=format&fit=crop",
"Sweet Pumpkin": "https://plus.unsplash.com/premium_photo-1666823706780-9c5219421d14?q=80&w=987&auto=format&fit=crop",
"Dry Chillis": "https://plus.unsplash.com/premium_photo-1675864033932-058885f9bfc2?q=80&w=3870&auto=format&fit=crop",
"Paddy(Common)": "https://plus.unsplash.com/premium_photo-1726862459894-aca62bf8a756?q=80&w=2028&auto=format&fit=crop",
"Knool Khol": "https://images.unsplash.com/photo-1659631832132-95250f19fa1d?q=80&w=2071&auto=format&fit=crop",
"Lime": "https://images.unsplash.com/photo-1578855691621-8a08ea00d1fb?q=80&w=1035&auto=format&fit=crop",
"Groundnut": "https://plus.unsplash.com/premium_photo-1667773157798-55785dd16b0a?q=80&w=1617&auto=format&fit=crop",
"Mataki": "https://images.unsplash.com/photo-1612504258838-fbf14fe4437d?q=80&w=987&auto=format&fit=crop",
"Arhar(Tur/Red Gram)(Whole)": "https://images.unsplash.com/photo-1632754223987-a6916e6e721a?q=80&w=2005&auto=format&fit=crop",
"Sesamum(Sesame,Gingelly,Til)": "https://plus.unsplash.com/premium_photo-1674654419404-667fcdd0fe13?q=80&w=2070&auto=format&fit=crop",
"Alasande Gram": "https://plus.unsplash.com/premium_photo-1670135170974-5352088c8ade?q=80&w=2070&auto=format&fit=crop",
"Suvarna Gadde": "https://www.sahajaseeds.com/wp-content/uploads/2024/03/WhatsApp-Image-2024-03-07-at-6.40.45-PM-scaled.jpeg",
"Foxtail Millet" : " https://look.jmgbb.com/images/qCn2sUiN_z.png",
"Green Peas" : "https://look.jmgbb.com/images/h7GU_a2wvk.png",
"Mustard" : "https://look.jmgbb.com/images/UYiStHlVDr.png",
"Watermelon" : "https://look.jmgbb.com/images/9QjGwGyoQW.png",
"Banana- Green" : "https://look.jmgbb.com/images/RM66RzZFvC.png",
"White Pumpkin" : "https://look.jmgbb.com/images/vXPS-Mxk26.png",
"Karbuja(Musk Melon)" : "https://look.jmgbb.com/images/dlZI3MBzhh.png",
"Bunch Beans" : "https://look.jmgbb.com/images/uDGrWhxXDF.png",
"Chapparad Avre" : "https://look.jmgbb.com/images/mtEbOXhsxy.png",
"Avare Dal" : "https://look.jmgbb.com/images/0NaQmJgabI.png",
"Coconut" : "https://look.jmgbb.com/images/ZUAhFoyADr.png",
"Papaya" : "https://look.jmgbb.com/images/MDlqrIiX6L.png",
"Green Avare(W)" : "https://look.jmgbb.com/images/Zn0vhn90NP.png",
"Elephant Yam(Suran)/Amorphophallus" : "https://look.jmgbb.com/images/0VLVYI8Ryt.png",
"Corrinder seed" : "https://look.jmgbb.com/images/dfK-FC5gLO.png",
"Honge seed" : "https://look.jmgbb.com/images/o4XHj_25Yc.png",
"Alsandikai" : "https://look.jmgbb.com/images/VbyAk6B4We.png",
"Peas Wet" : "https://look.jmgbb.com/images/cI8EPjmgcH.png",
"Bengal Gram(Gram)(Whole)" : "https://look.jmgbb.com/images/_mir6LfUR6.png",
"Soyabean" : "https://look.jmgbb.com/images/qEtK-WVQZd.png", 
"Cotton" : "https://look.jmgbb.com/images/wBgA1mzEy-.png",
"Pineapple" : "https://look.jmgbb.com/images/6i4Tdt6sOp.png",
"Onion" : "https://look.jmgbb.com/images/Rnsc5xtG22.png",
"Mousambi(Sweet Lime)" : "https://look.jmgbb.com/images/zgvCAI26c4.png",
"Bottle gourd" : "https://look.jmgbb.com/images/coo-uExPwG.png",
"Green Chilli" : "https://look.jmgbb.com/images/c9b1DBjRnf.png",
"Arecanut(Betelnut/Supari)" : "https://look.jmgbb.com/images/bMvV2aLG7Q.png",
"Sweet Potato" : "https://look.jmgbb.com/images/obaOSW8Xea.png",
"Ridgeguard(Tori)" : "https://look.jmgbb.com/images/VKTXj_opW1.png",
"Capsicum" : "https://look.jmgbb.com/images/RyokMsPJ2a.png"
}
DEFAULT_CROP_IMAGE = "https://images.unsplash.com/photo-1500595046743-cd271d694d30?w=400&h=300&fit=crop"

# Set your API key: Get a free key from https://data.gov.in
DATA_GOV_API_KEY = os.environ.get("DATA_GOV_API_KEY", "")


@app.route('/get_crop_prices')
def get_crop_prices():
    url = ""

    params = {
        "api-key": DATA_GOV_API_KEY,
        "format": "json",
        "limit": 1000,
        "filters[state.keyword]": "Karnataka"
    }

    try:
        if not DATA_GOV_API_KEY:
            raise Exception("API key not configured")

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        crops = []
        seen = set()

        for item in data.get('records', []):
            commodity = item.get('commodity')
            if commodity and commodity not in seen:
                seen.add(commodity)
                crops.append({
                    "name": commodity,
                    "price": item.get('modal_price'),
                    "market": item.get('market'),
                    "state": item.get('state'),
                    "image": CROP_IMAGES.get(commodity, DEFAULT_CROP_IMAGE)
                })

        if not crops:
            raise Exception("No data returned")

        return jsonify(crops)

    except Exception:
        return jsonify([
            # {"name": "Rice", "price": 2200, "market": "Bangalore", "state": "Karnataka",
            #  "image": CROP_IMAGES["Rice"]},
            {"name": "Wheat", "price": 2100, "market": "Mysore", "state": "Karnataka",
             "image": CROP_IMAGES["Wheat"]},
            {"name": "Maize", "price": 1800, "market": "Hubli", "state": "Karnataka",
             "image": CROP_IMAGES["Maize"]},
            {"name": "Cotton", "price": 6200, "market": "Belgaum", "state": "Karnataka",
             "image": CROP_IMAGES["Cotton"]}
        ])

# ========== FARMER COMMUNITY ==========

COMMUNITY_UPLOAD_FOLDER = "static/community"
if not os.path.exists(COMMUNITY_UPLOAD_FOLDER):
    os.makedirs(COMMUNITY_UPLOAD_FOLDER)

GROUP_CATEGORIES = [
    "General", "Organic Farming", "Crop Diseases", "Market Prices",
    "Government Schemes", "Water Management", "Seed & Fertilizer",
    "Equipment & Tools", "Livestock", "Success Stories"
]

@app.route("/community")
def community():
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")
    farmer_id = session["user_id"]

    cursor.execute("SELECT id, name FROM farmers WHERE id = %s", (farmer_id,))
    farmer = cursor.fetchone()

    # Get community feed posts (no group) + group posts from joined groups
    cursor.execute("""
        SELECT p.id, p.content, p.image, p.created_at, p.group_id,
               f.name as farmer_name, f.id as farmer_id,
               g.name as group_name,
               (SELECT COUNT(*) FROM post_likes WHERE post_id = p.id) as like_count,
               (SELECT COUNT(*) FROM post_comments WHERE post_id = p.id) as comment_count,
               (SELECT COUNT(*) FROM post_likes WHERE post_id = p.id AND farmer_id = %s) as user_liked
        FROM community_posts p
        JOIN farmers f ON p.farmer_id = f.id
        LEFT JOIN community_groups g ON p.group_id = g.id
        WHERE p.group_id IS NULL
           OR p.group_id IN (SELECT group_id FROM group_members WHERE farmer_id = %s)
        ORDER BY p.created_at DESC
        LIMIT 50
    """, (farmer_id, farmer_id))
    posts = cursor.fetchall()

    # Get groups the farmer is a member of
    cursor.execute("""
        SELECT g.id, g.name, g.category, g.description,
               (SELECT COUNT(*) FROM group_members WHERE group_id = g.id) as member_count
        FROM community_groups g
        JOIN group_members gm ON g.id = gm.group_id
        WHERE gm.farmer_id = %s
        ORDER BY g.name
    """, (farmer_id,))
    my_groups = cursor.fetchall()

    # Get groups the farmer can discover (not a member)
    cursor.execute("""
        SELECT g.id, g.name, g.category, g.description,
               (SELECT COUNT(*) FROM group_members WHERE group_id = g.id) as member_count,
               f.name as creator_name
        FROM community_groups g
        JOIN farmers f ON g.created_by = f.id
        WHERE g.id NOT IN (SELECT group_id FROM group_members WHERE farmer_id = %s)
        ORDER BY member_count DESC
        LIMIT 20
    """, (farmer_id,))
    discover_groups = cursor.fetchall()

    return render_template("community.html",
                           farmer=farmer, posts=posts,
                           my_groups=my_groups, discover_groups=discover_groups,
                           group_categories=GROUP_CATEGORIES)


@app.route("/community/post", methods=["POST"])
def community_create_post():
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")
    farmer_id = session["user_id"]
    content = request.form.get("content", "").strip()
    group_id = request.form.get("group_id") or None

    if not content:
        flash("Post content cannot be empty", "danger")
        return redirect(request.referrer or "/community")

    image_filename = None
    if "image" in request.files and request.files["image"].filename:
        file = request.files["image"]
        image_filename = secure_filename(f"{farmer_id}_{int(__import__('time').time())}_{file.filename}")
        file.save(os.path.join(COMMUNITY_UPLOAD_FOLDER, image_filename))

    cursor.execute(
        "INSERT INTO community_posts (farmer_id, group_id, content, image) VALUES (%s, %s, %s, %s)",
        (farmer_id, group_id, content, image_filename)
    )
    conn.commit()
    flash("Post shared successfully! ✅", "success")

    if group_id:
        return redirect(f"/community/group/{group_id}")
    return redirect("/community")


@app.route("/community/like/<int:post_id>", methods=["POST"])
def community_like_post(post_id):
    if "user_id" not in session or session.get("role") != "farmer":
        return jsonify({"error": "unauthorized"}), 401
    farmer_id = session["user_id"]

    cursor.execute("SELECT id FROM post_likes WHERE post_id = %s AND farmer_id = %s", (post_id, farmer_id))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("DELETE FROM post_likes WHERE post_id = %s AND farmer_id = %s", (post_id, farmer_id))
    else:
        cursor.execute("INSERT INTO post_likes (post_id, farmer_id) VALUES (%s, %s)", (post_id, farmer_id))
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM post_likes WHERE post_id = %s", (post_id,))
    count = cursor.fetchone()[0]
    liked = 0 if existing else 1
    return jsonify({"like_count": count, "liked": liked})


@app.route("/community/comment/<int:post_id>", methods=["POST"])
def community_add_comment(post_id):
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")
    farmer_id = session["user_id"]
    content = request.form.get("content", "").strip()

    if not content:
        flash("Comment cannot be empty", "danger")
        return redirect(request.referrer or "/community")

    cursor.execute(
        "INSERT INTO post_comments (post_id, farmer_id, content) VALUES (%s, %s, %s)",
        (post_id, farmer_id, content)
    )
    conn.commit()
    return redirect(request.referrer or "/community")


@app.route("/community/comments/<int:post_id>")
def community_get_comments(post_id):
    if "user_id" not in session or session.get("role") != "farmer":
        return jsonify({"error": "unauthorized"}), 401

    cursor.execute("""
        SELECT c.content, c.created_at, f.name as farmer_name
        FROM post_comments c
        JOIN farmers f ON c.farmer_id = f.id
        WHERE c.post_id = %s
        ORDER BY c.created_at ASC
    """, (post_id,))
    comments = cursor.fetchall()
    return jsonify([{
        "content": c[0],
        "created_at": c[1].strftime("%b %d, %Y %I:%M %p"),
        "farmer_name": c[2]
    } for c in comments])


@app.route("/community/create_group", methods=["POST"])
def community_create_group():
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")
    farmer_id = session["user_id"]
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    category = request.form.get("category", "General")

    if not name:
        flash("Group name is required", "danger")
        return redirect("/community")

    cursor.execute(
        "INSERT INTO community_groups (name, description, category, created_by) VALUES (%s, %s, %s, %s)",
        (name, description, category, farmer_id)
    )
    conn.commit()
    group_id = cursor.lastrowid

    # Auto-join the creator
    cursor.execute(
        "INSERT INTO group_members (group_id, farmer_id) VALUES (%s, %s)",
        (group_id, farmer_id)
    )
    conn.commit()
    flash(f"Group '{name}' created! ✅", "success")
    return redirect(f"/community/group/{group_id}")


@app.route("/community/join_group/<int:group_id>", methods=["POST"])
def community_join_group(group_id):
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")
    farmer_id = session["user_id"]

    cursor.execute("SELECT id FROM group_members WHERE group_id = %s AND farmer_id = %s", (group_id, farmer_id))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO group_members (group_id, farmer_id) VALUES (%s, %s)",
            (group_id, farmer_id)
        )
        conn.commit()
        flash("Joined group! ✅", "success")
    return redirect(f"/community/group/{group_id}")


@app.route("/community/leave_group/<int:group_id>", methods=["POST"])
def community_leave_group(group_id):
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")
    farmer_id = session["user_id"]

    cursor.execute(
        "DELETE FROM group_members WHERE group_id = %s AND farmer_id = %s",
        (group_id, farmer_id)
    )
    conn.commit()
    flash("Left the group", "info")
    return redirect("/community")


@app.route("/community/group/<int:group_id>")
def community_group_detail(group_id):
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")
    farmer_id = session["user_id"]

    # Group info
    cursor.execute("""
        SELECT g.id, g.name, g.description, g.category, g.created_by, f.name as creator_name,
               (SELECT COUNT(*) FROM group_members WHERE group_id = g.id) as member_count
        FROM community_groups g
        JOIN farmers f ON g.created_by = f.id
        WHERE g.id = %s
    """, (group_id,))
    group = cursor.fetchone()
    if not group:
        flash("Group not found", "danger")
        return redirect("/community")

    # Check membership
    cursor.execute("SELECT id FROM group_members WHERE group_id = %s AND farmer_id = %s", (group_id, farmer_id))
    is_member = cursor.fetchone() is not None

    # Group posts
    cursor.execute("""
        SELECT p.id, p.content, p.image, p.created_at, p.group_id,
               f.name as farmer_name, f.id as farmer_id,
               NULL as group_name,
               (SELECT COUNT(*) FROM post_likes WHERE post_id = p.id) as like_count,
               (SELECT COUNT(*) FROM post_comments WHERE post_id = p.id) as comment_count,
               (SELECT COUNT(*) FROM post_likes WHERE post_id = p.id AND farmer_id = %s) as user_liked
        FROM community_posts p
        JOIN farmers f ON p.farmer_id = f.id
        WHERE p.group_id = %s
        ORDER BY p.created_at DESC
    """, (farmer_id, group_id))
    posts = cursor.fetchall()

    # Members list
    cursor.execute("""
        SELECT f.id, f.name, f.state, f.city, gm.joined_at
        FROM group_members gm
        JOIN farmers f ON gm.farmer_id = f.id
        WHERE gm.group_id = %s
        ORDER BY gm.joined_at
    """, (group_id,))
    members = cursor.fetchall()

    return render_template("community_group.html",
                           group=group, posts=posts, members=members,
                           is_member=is_member, farmer_id=farmer_id)


@app.route("/community/delete_post/<int:post_id>", methods=["POST"])
def community_delete_post(post_id):
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")
    farmer_id = session["user_id"]

    cursor.execute("SELECT farmer_id, group_id, image FROM community_posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    if not post or post[0] != farmer_id:
        flash("Cannot delete this post", "danger")
        return redirect(request.referrer or "/community")

    # Delete related likes and comments first
    cursor.execute("DELETE FROM post_likes WHERE post_id = %s", (post_id,))
    cursor.execute("DELETE FROM post_comments WHERE post_id = %s", (post_id,))
    cursor.execute("DELETE FROM community_posts WHERE id = %s", (post_id,))
    conn.commit()

    # Remove image file if exists
    if post[2]:
        img_path = os.path.join(COMMUNITY_UPLOAD_FOLDER, post[2])
        if os.path.exists(img_path):
            os.remove(img_path)

    flash("Post deleted", "info")
    if post[1]:
        return redirect(f"/community/group/{post[1]}")
    return redirect("/community")



# ========== WEATHER API ==========
OPENWEATHER_API_KEY = ""

@app.route("/api/weather")
def api_weather():
    city = request.args.get("city", "Mysore")

    try:
        # Current weather
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={OPENWEATHER_API_KEY}&units=metric"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # 5-day forecast
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},IN&appid={OPENWEATHER_API_KEY}&units=metric"
        f_resp = requests.get(forecast_url, timeout=10)
        f_resp.raise_for_status()
        f_data = f_resp.json()

        forecast = []
        seen_days = set()

        from datetime import datetime

        for item in f_data.get("list", []):
            dt = datetime.fromtimestamp(item["dt"])
            day_name = dt.strftime("%a")

            if day_name not in seen_days and len(forecast) < 5:
                seen_days.add(day_name)

                forecast.append({
                    "day": day_name,
                    "temp_max": round(item["main"]["temp_max"]),
                    "temp_min": round(item["main"]["temp_min"]),
                    "condition": item["weather"][0]["description"].title(),
                    "icon": item["weather"][0]["icon"]
                })

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        if temp > 40:
            advisory = "Extreme heat! Irrigate crops early morning or evening. Provide shade for livestock."
        elif temp > 35:
            advisory = "High temperature. Ensure adequate irrigation. Mulch to retain soil moisture."
        elif humidity > 80:
            advisory = "High humidity. Watch for fungal diseases. Avoid spraying pesticides."
        elif data["weather"][0]["main"] == "Rain":
            advisory = "Rain expected. Postpone fertilizer application. Ensure proper field drainage."
        else:
            advisory = "Good weather for field work. Monitor soil moisture levels."

        result = {
            "city": data["name"],
            "temperature": round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "humidity": data["main"]["humidity"],
            "wind_speed": round(data["wind"]["speed"] * 3.6, 1),
            "condition": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "forecast": forecast,
            "advisory": advisory
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========== SOIL ANALYSIS DATA ==========
SOIL_DATA = {
    "alluvial": {
        "name": "Alluvial Soil",
        "name_kn": "ಮೆಕ್ಕಲು ಮಣ್ಣು",
        "name_hi": "जलोढ़ मिट्टी",
        "description": "Rich in potash, phosphoric acid. Found in river plains. Most fertile soil in India.",
        "description_kn": "ಪೊಟ್ಯಾಷ್, ಫಾಸ್ಫರಿಕ್ ಆಮ್ಲದಲ್ಲಿ ಸಮೃದ್ಧ. ನದಿ ಬಯಲುಗಳಲ್ಲಿ ಕಂಡುಬರುತ್ತದೆ.",
        "description_hi": "पोटाश, फॉस्फोरिक एसिड से भरपूर। नदी मैदानों में पाई जाती है।",
        "crops": ["Rice", "Wheat", "Sugarcane", "Maize", "Pulses", "Oilseeds"],
        "ph": "6.5 - 8.0",
        "tips": "Add organic matter regularly. Practice crop rotation. Good for most crops.",
        "tips_kn": "ನಿಯಮಿತವಾಗಿ ಸಾವಯವ ವಸ್ತುಗಳನ್ನು ಸೇರಿಸಿ. ಬೆಳೆ ಬದಲಾವಣೆ ಅಭ್ಯಾಸ ಮಾಡಿ.",
        "tips_hi": "नियमित रूप से जैविक पदार्थ मिलाएं। फसल चक्र अपनाएं।",
        "color": "#D4A574"
    },
    "black": {
        "name": "Black Soil (Regur)",
        "name_kn": "ಕಪ್ಪು ಮಣ್ಣು (ರೇಗರ್)",
        "name_hi": "काली मिट्टी (रेगुर)",
        "description": "Rich in calcium, magnesium, potash. High moisture retention. Self-ploughing nature.",
        "description_kn": "ಕ್ಯಾಲ್ಸಿಯಂ, ಮೆಗ್ನೀಷಿಯಂ, ಪೊಟ್ಯಾಷ್‌ನಲ್ಲಿ ಸಮೃದ್ಧ. ಹೆಚ್ಚಿನ ತೇವಾಂಶ ಧಾರಣೆ.",
        "description_hi": "कैल्शियम, मैग्नीशियम, पोटाश से भरपूर। उच्च नमी धारण क्षमता।",
        "crops": ["Cotton", "Soybean", "Sugarcane", "Wheat", "Jowar", "Sunflower", "Groundnut"],
        "ph": "7.2 - 8.5",
        "tips": "Avoid waterlogging. Add gypsum to improve drainage. Best for cotton and soybeans.",
        "tips_kn": "ನೀರು ನಿಲ್ಲುವುದನ್ನು ತಪ್ಪಿಸಿ. ಜಿಪ್ಸಂ ಸೇರಿಸಿ ಬರಿಸುವಿಕೆ ಸುಧಾರಿಸಿ.",
        "tips_hi": "जलभराव से बचें। जिप्सम मिलाकर जल निकासी सुधारें।",
        "color": "#3D3D3D"
    },
    "red": {
        "name": "Red Soil",
        "name_kn": "ಕೆಂಪು ಮಣ್ಣು",
        "name_hi": "लाल मिट्टी",
        "description": "Rich in iron oxide. Low in nitrogen, phosphorus. Found in Karnataka, Tamil Nadu, Andhra Pradesh.",
        "description_kn": "ಕಬ್ಬಿಣದ ಆಕ್ಸೈಡ್‌ನಲ್ಲಿ ಸಮೃದ್ಧ. ಸಾರಜನಕ, ರಂಜಕದಲ್ಲಿ ಕಡಿಮೆ.",
        "description_hi": "आयरन ऑक्साइड से भरपूर। नाइट्रोजन, फॉस्फोरस में कम।",
        "crops": ["Ragi", "Groundnut", "Potato", "Rice", "Maize", "Tobacco", "Millets"],
        "ph": "5.5 - 7.0",
        "tips": "Add lime to correct acidity. Apply nitrogen and phosphorus fertilizers. Use green manure.",
        "tips_kn": "ಆಮ್ಲೀಯತೆ ಸರಿಪಡಿಸಲು ಸುಣ್ಣ ಸೇರಿಸಿ. ಸಾರಜನಕ ಮತ್ತು ರಂಜಕ ಗೊಬ್ಬರ ಬಳಸಿ.",
        "tips_hi": "अम्लता ठीक करने के लिए चूना मिलाएं। नाइट्रोजन और फॉस्फोरस उर्वरक डालें।",
        "color": "#C0392B"
    },
    "laterite": {
        "name": "Laterite Soil",
        "name_kn": "ಲ್ಯಾಟರೈಟ್ ಮಣ್ಣು",
        "name_hi": "लेटराइट मिट्टी",
        "description": "Rich in iron and aluminium. Poor in nitrogen, potash, lime. Found in Western Ghats region.",
        "description_kn": "ಕಬ್ಬಿಣ ಮತ್ತು ಅಲ್ಯೂಮಿನಿಯಂನಲ್ಲಿ ಸಮೃದ್ಧ. ಪಶ್ಚಿಮ ಘಟ್ಟಗಳ ಪ್ರದೇಶದಲ್ಲಿ ಕಂಡುಬರುತ್ತದೆ.",
        "description_hi": "आयरन और एल्यूमीनियम से भरपूर। पश्चिमी घाट क्षेत्र में पाई जाती है।",
        "crops": ["Coconut", "Arecanut", "Cashew", "Rubber", "Tea", "Coffee", "Pepper"],
        "ph": "5.0 - 6.5",
        "tips": "Heavy manuring required. Add organic matter. Suitable for plantation crops with proper management.",
        "tips_kn": "ಹೆಚ್ಚಿನ ಗೊಬ್ಬರ ಅಗತ್ಯ. ಸಾವಯವ ವಸ್ತುಗಳನ್ನು ಸೇರಿಸಿ.",
        "tips_hi": "भारी मात्रा में खाद आवश्यक। जैविक पदार्थ मिलाएं।",
        "color": "#E67E22"
    },
    "sandy": {
        "name": "Sandy Soil",
        "name_kn": "ಮರಳು ಮಣ್ಣು",
        "name_hi": "रेतीली मिट्टी",
        "description": "Low water retention. Good aeration. Drains quickly. Found in Rajasthan, coastal areas.",
        "description_kn": "ಕಡಿಮೆ ನೀರು ಹಿಡಿಯುವ ಸಾಮರ್ಥ್ಯ. ಬೇಗ ಬರಿಸುತ್ತದೆ.",
        "description_hi": "कम जल धारण क्षमता। जल्दी सूख जाती है।",
        "crops": ["Groundnut", "Watermelon", "Cucumber", "Carrot", "Potato", "Bajra", "Jowar"],
        "ph": "5.5 - 7.0",
        "tips": "Add clay and organic matter to improve water retention. Use drip irrigation. Mulch heavily.",
        "tips_kn": "ನೀರಿನ ಧಾರಣೆ ಸುಧಾರಿಸಲು ಜೇಡಿಮಣ್ಣು ಮತ್ತು ಸಾವಯವ ವಸ್ತುಗಳನ್ನು ಸೇರಿಸಿ.",
        "tips_hi": "जल धारण सुधारने के लिए मिट्टी और जैविक पदार्थ मिलाएं।",
        "color": "#F5DEB3"
    },
    "clay": {
        "name": "Clay Soil",
        "name_kn": "ಜೇಡಿಮಣ್ಣು",
        "name_hi": "चिकनी मिट्टी",
        "description": "High water retention. Rich in nutrients. Heavy and sticky when wet. Cracks when dry.",
        "description_kn": "ಹೆಚ್ಚಿನ ನೀರು ಹಿಡಿಯುವ ಸಾಮರ್ಥ್ಯ. ಪೋಷಕಾಂಶಗಳಲ್ಲಿ ಸಮೃದ್ಧ.",
        "description_hi": "उच्च जल धारण क्षमता। पोषक तत्वों से भरपूर।",
        "crops": ["Rice", "Wheat", "Cotton", "Sugarcane", "Lentils", "Beans"],
        "ph": "6.0 - 8.0",
        "tips": "Improve drainage. Add sand and organic matter. Avoid working when too wet.",
        "tips_kn": "ಬರಿಸುವಿಕೆ ಸುಧಾರಿಸಿ. ಮರಳು ಮತ್ತು ಸಾವಯವ ವಸ್ತುಗಳನ್ನು ಸೇರಿಸಿ.",
        "tips_hi": "जल निकासी सुधारें। रेत और जैविक पदार्थ मिलाएं।",
        "color": "#8B7355"
    },
    "loamy": {
        "name": "Loamy Soil",
        "name_kn": "ಕಂಬಳಿ ಮಣ್ಣು",
        "name_hi": "दोमट मिट्टी",
        "description": "Perfect balance of sand, silt, and clay. Best for most crops. Good drainage and nutrient retention.",
        "description_kn": "ಮರಳು, ಕೆಸರು ಮತ್ತು ಜೇಡಿಮಣ್ಣಿನ ಸಮತೋಲನ. ಬಹುತೇಕ ಬೆಳೆಗಳಿಗೆ ಉತ್ತಮ.",
        "description_hi": "रेत, गाद और मिट्टी का सही संतुलन। अधिकांश फसलों के लिए सर्वोत्तम।",
        "crops": ["Wheat", "Maize", "Tomato", "Vegetables", "Fruits", "Sugarcane", "Cotton"],
        "ph": "6.0 - 7.5",
        "tips": "Maintain organic matter levels. This is ideal soil — practice sustainable farming to preserve it.",
        "tips_kn": "ಸಾವಯವ ವಸ್ತುಗಳ ಮಟ್ಟವನ್ನು ನಿರ್ವಹಿಸಿ. ಇದು ಆದರ್ಶ ಮಣ್ಣು.",
        "tips_hi": "जैविक पदार्थ का स्तर बनाए रखें। यह आदर्श मिट्टी है।",
        "color": "#8B6914"
    }
}

@app.route("/api/soil_analysis")
def api_soil_analysis():
    soil_type = request.args.get("type", "alluvial")
    lang = get_lang()
    soil = SOIL_DATA.get(soil_type, SOIL_DATA["alluvial"])

    name_key = "name" if lang == "en" else f"name_{lang}"
    desc_key = "description" if lang == "en" else f"description_{lang}"
    tips_key = "tips" if lang == "en" else f"tips_{lang}"

    return jsonify({
        "name": soil.get(name_key, soil["name"]),
        "description": soil.get(desc_key, soil["description"]),
        "crops": soil["crops"],
        "ph": soil["ph"],
        "tips": soil.get(tips_key, soil["tips"]),
        "color": soil["color"]
    })


# ========== GOVERNMENT SCHEMES API ==========
FARMER_SCHEMES = [
    {
        "name": "PM-KISAN Samman Nidhi",
        "name_kn": "ಪಿಎಂ-ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿ",
        "name_hi": "पीएम-किसान सम्मान निधि",
        "benefit": "₹6,000/year in 3 installments directly to bank account",
        "benefit_kn": "₹6,000/ವರ್ಷ 3 ಕಂತುಗಳಲ್ಲಿ ನೇರವಾಗಿ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ",
        "benefit_hi": "₹6,000/वर्ष 3 किस्तों में सीधे बैंक खाते में",
        "eligibility": "All landholding farmer families",
        "eligibility_kn": "ಎಲ್ಲಾ ಭೂ ಹಿಡುವಳಿ ರೈತ ಕುಟುಂಬಗಳು",
        "eligibility_hi": "सभी भूमिधारक किसान परिवार",
        "how_to_apply": "Register at pmkisan.gov.in or nearest CSC center. Call 155261",
        "how_to_apply_kn": "pmkisan.gov.in ನಲ್ಲಿ ಅಥವಾ ಹತ್ತಿರದ CSC ಕೇಂದ್ರದಲ್ಲಿ ನೋಂದಾಯಿಸಿ",
        "how_to_apply_hi": "pmkisan.gov.in या निकटतम CSC केंद्र पर पंजीकरण करें",
        "icon": "💰",
        "category": "Financial Support"
    },
    {
        "name": "PM Fasal Bima Yojana (PMFBY)",
        "name_kn": "ಪಿಎಂ ಫಸಲ್ ಬೀಮಾ ಯೋಜನಾ",
        "name_hi": "पीएम फसल बीमा योजना",
        "benefit": "Crop insurance at 2% premium (Kharif), 1.5% (Rabi). Covers natural calamities, pests & diseases",
        "benefit_kn": "ಬೆಳೆ ವಿಮೆ 2% ಪ್ರೀಮಿಯಂನಲ್ಲಿ (ಖಾರಿಫ್), 1.5% (ರಾಬಿ). ನೈಸರ್ಗಿಕ ವಿಕೋಪ, ಕೀಟ ಮತ್ತು ರೋಗಗಳನ್ನು ಒಳಗೊಂಡಿದೆ",
        "benefit_hi": "फसल बीमा 2% प्रीमियम (खरीफ), 1.5% (रबी)। प्राकृतिक आपदाओं, कीटों और रोगों को कवर करता है",
        "eligibility": "All farmers with crop loans and voluntary for others",
        "eligibility_kn": "ಬೆಳೆ ಸಾಲ ಹೊಂದಿರುವ ಎಲ್ಲಾ ರೈತರು",
        "eligibility_hi": "फसल ऋण वाले सभी किसान",
        "how_to_apply": "Through banks, CSC, or insurance company. Helpline: 1800-200-7710",
        "how_to_apply_kn": "ಬ್ಯಾಂಕ್, CSC ಅಥವಾ ವಿಮಾ ಕಂಪನಿ ಮೂಲಕ. ಸಹಾಯವಾಣಿ: 1800-200-7710",
        "how_to_apply_hi": "बैंक, CSC या बीमा कंपनी के माध्यम से। हेल्पलाइन: 1800-200-7710",
        "icon": "🛡️",
        "category": "Insurance"
    },
    {
        "name": "Kisan Credit Card (KCC)",
        "name_kn": "ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್",
        "name_hi": "किसान क्रेडिट कार्ड",
        "benefit": "Crop loans at 4% interest (with subsidy). Covers farming expenses, equipment & storage",
        "benefit_kn": "ಬೆಳೆ ಸಾಲ 4% ಬಡ್ಡಿಯಲ್ಲಿ (ಸಬ್ಸಿಡಿಯೊಂದಿಗೆ). ಕೃಷಿ ಖರ್ಚು, ಸಲಕರಣೆ ಮತ್ತು ಸಂಗ್ರಹಣೆ",
        "benefit_hi": "फसल ऋण 4% ब्याज पर (सब्सिडी के साथ)। खेती खर्च, उपकरण और भंडारण",
        "eligibility": "All farmers, sharecroppers, tenant farmers",
        "eligibility_kn": "ಎಲ್ಲಾ ರೈತರು, ಪಾಲುದಾರ ರೈತರು, ಗೇಣಿ ರೈತರು",
        "eligibility_hi": "सभी किसान, बटाईदार, किरायेदार किसान",
        "how_to_apply": "Apply at any bank with land documents. Aadhar & land records required",
        "how_to_apply_kn": "ಭೂಮಿ ದಾಖಲೆಗಳೊಂದಿಗೆ ಯಾವುದೇ ಬ್ಯಾಂಕ್‌ನಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ",
        "how_to_apply_hi": "भूमि दस्तावेजों के साथ किसी भी बैंक में आवेदन करें",
        "icon": "💳",
        "category": "Credit & Loans"
    },
    {
        "name": "Soil Health Card Scheme",
        "name_kn": "ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಕಾರ್ಡ್ ಯೋಜನೆ",
        "name_hi": "मृदा स्वास्थ्य कार्ड योजना",
        "benefit": "Free soil testing & nutrient recommendations. Helps optimize fertilizer usage",
        "benefit_kn": "ಉಚಿತ ಮಣ್ಣು ಪರೀಕ್ಷೆ ಮತ್ತು ಪೋಷಕಾಂಶ ಶಿಫಾರಸುಗಳು",
        "benefit_hi": "मुफ्त मिट्टी परीक्षण और पोषक तत्व सिफारिशें",
        "eligibility": "All farmers",
        "eligibility_kn": "ಎಲ್ಲಾ ರೈತರು",
        "eligibility_hi": "सभी किसान",
        "how_to_apply": "Contact nearest Krishi Vigyan Kendra (KVK) or Agriculture Department",
        "how_to_apply_kn": "ಹತ್ತಿರದ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರ (KVK) ಸಂಪರ್ಕಿಸಿ",
        "how_to_apply_hi": "निकटतम कृषि विज्ञान केंद्र (KVK) से संपर्क करें",
        "icon": "🧪",
        "category": "Technical Support"
    },
    {
        "name": "e-NAM (National Agriculture Market)",
        "name_kn": "ಇ-ನಾಮ್ (ರಾಷ್ಟ್ರೀಯ ಕೃಷಿ ಮಾರುಕಟ್ಟೆ)",
        "name_hi": "ई-नाम (राष्ट्रीय कृषि बाजार)",
        "benefit": "Sell produce online at best price. Transparent bidding, no middlemen",
        "benefit_kn": "ಉತ್ಪನ್ನವನ್ನು ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಉತ್ತಮ ಬೆಲೆಗೆ ಮಾರಾಟ ಮಾಡಿ",
        "benefit_hi": "उपज को ऑनलाइन सर्वोत्तम मूल्य पर बेचें",
        "eligibility": "All farmers with Aadhar & bank account",
        "eligibility_kn": "ಆಧಾರ್ ಮತ್ತು ಬ್ಯಾಂಕ್ ಖಾತೆ ಹೊಂದಿರುವ ಎಲ್ಲಾ ರೈತರು",
        "eligibility_hi": "आधार और बैंक खाता वाले सभी किसान",
        "how_to_apply": "Register at enam.gov.in or nearest APMC mandi",
        "how_to_apply_kn": "enam.gov.in ನಲ್ಲಿ ಅಥವಾ ಹತ್ತಿರದ APMC ಮಂಡಿಯಲ್ಲಿ ನೋಂದಾಯಿಸಿ",
        "how_to_apply_hi": "enam.gov.in या निकटतम APMC मंडी में पंजीकरण करें",
        "icon": "🏪",
        "category": "Market Access"
    },
    {
        "name": "PM Krishi Sinchai Yojana (PMKSY)",
        "name_kn": "ಪಿಎಂ ಕೃಷಿ ಸಿಂಚಾಯಿ ಯೋಜನಾ",
        "name_hi": "पीएम कृषि सिंचाई योजना",
        "benefit": "55-90% subsidy on drip/sprinkler irrigation. 'More crop per drop' initiative",
        "benefit_kn": "ಹನಿ/ಸ್ಪ್ರಿಂಕ್ಲರ್ ನೀರಾವರಿ ಮೇಲೆ 55-90% ಸಬ್ಸಿಡಿ",
        "benefit_hi": "ड्रिप/स्प्रिंकलर सिंचाई पर 55-90% सब्सिडी",
        "eligibility": "All farmers. Small & marginal farmers get higher subsidy",
        "eligibility_kn": "ಎಲ್ಲಾ ರೈತರು. ಸಣ್ಣ ಮತ್ತು ಅತಿ ಸಣ್ಣ ರೈತರಿಗೆ ಹೆಚ್ಚಿನ ಸಬ್ಸಿಡಿ",
        "eligibility_hi": "सभी किसान। छोटे और सीमांत किसानों को अधिक सब्सिडी",
        "how_to_apply": "Apply through State Agriculture/Horticulture Department",
        "how_to_apply_kn": "ರಾಜ್ಯ ಕೃಷಿ/ತೋಟಗಾರಿಕೆ ಇಲಾಖೆ ಮೂಲಕ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ",
        "how_to_apply_hi": "राज्य कृषि/बागवानी विभाग के माध्यम से आवेदन करें",
        "icon": "💧",
        "category": "Irrigation"
    },
    {
        "name": "Paramparagat Krishi Vikas Yojana (PKVY)",
        "name_kn": "ಪರಂಪರಾಗತ ಕೃಷಿ ವಿಕಾಸ ಯೋಜನಾ",
        "name_hi": "परंपरागत कृषि विकास योजना",
        "benefit": "₹50,000/hectare over 3 years for organic farming. Training & certification support",
        "benefit_kn": "ಸಾವಯವ ಕೃಷಿಗೆ 3 ವರ್ಷಗಳಲ್ಲಿ ₹50,000/ಹೆಕ್ಟೇರ್. ತರಬೇತಿ ಮತ್ತು ಪ್ರಮಾಣೀಕರಣ ಬೆಂಬಲ",
        "benefit_hi": "जैविक खेती के लिए 3 वर्षों में ₹50,000/हेक्टेयर। प्रशिक्षण और प्रमाणन सहायता",
        "eligibility": "Farmer groups of minimum 50 acres under cluster approach",
        "eligibility_kn": "ಕ್ಲಸ್ಟರ್ ವಿಧಾನದಲ್ಲಿ ಕನಿಷ್ಠ 50 ಎಕರೆ ರೈತ ಗುಂಪುಗಳು",
        "eligibility_hi": "क्लस्टर दृष्टिकोण में न्यूनतम 50 एकड़ किसान समूह",
        "how_to_apply": "Through District Agriculture Officer or ATMA. Form clusters with nearby farmers",
        "how_to_apply_kn": "ಜಿಲ್ಲಾ ಕೃಷಿ ಅಧಿಕಾರಿ ಅಥವಾ ATMA ಮೂಲಕ",
        "how_to_apply_hi": "जिला कृषि अधिकारी या ATMA के माध्यम से",
        "icon": "🌿",
        "category": "Organic Farming"
    },
    {
        "name": "Rashtriya Krishi Vikas Yojana (RKVY)",
        "name_kn": "ರಾಷ್ಟ್ರೀಯ ಕೃಷಿ ವಿಕಾಸ ಯೋಜನೆ",
        "name_hi": "राष्ट्रीय कृषि विकास योजना",
        "benefit": "Subsidies on farm infrastructure, equipment, technology. State-specific projects",
        "benefit_kn": "ಕೃಷಿ ಮೂಲಸೌಕರ್ಯ, ಸಲಕರಣೆ, ತಂತ್ರಜ್ಞಾನ ಮೇಲೆ ಸಬ್ಸಿಡಿಗಳು",
        "benefit_hi": "कृषि बुनियादी ढांचे, उपकरण, प्रौद्योगिकी पर सब्सिडी",
        "eligibility": "All farmers through State Government projects",
        "eligibility_kn": "ರಾಜ್ಯ ಸರ್ಕಾರದ ಯೋಜನೆಗಳ ಮೂಲಕ ಎಲ್ಲಾ ರೈತರು",
        "eligibility_hi": "राज्य सरकार की परियोजनाओं के माध्यम से सभी किसान",
        "how_to_apply": "Contact District Agriculture Office or State Agriculture Department",
        "how_to_apply_kn": "ಜಿಲ್ಲಾ ಕೃಷಿ ಕಚೇರಿ ಅಥವಾ ರಾಜ್ಯ ಕೃಷಿ ಇಲಾಖೆ ಸಂಪರ್ಕಿಸಿ",
        "how_to_apply_hi": "जिला कृषि कार्यालय या राज्य कृषि विभाग से संपर्क करें",
        "icon": "🏗️",
        "category": "Infrastructure"
    }
]

@app.route("/api/schemes")
def api_schemes():
    lang = get_lang()
    schemes = []
    for s in FARMER_SCHEMES:
        name_key = "name" if lang == "en" else f"name_{lang}"
        benefit_key = "benefit" if lang == "en" else f"benefit_{lang}"
        elig_key = "eligibility" if lang == "en" else f"eligibility_{lang}"
        apply_key = "how_to_apply" if lang == "en" else f"how_to_apply_{lang}"
        schemes.append({
            "name": s.get(name_key, s["name"]),
            "benefit": s.get(benefit_key, s["benefit"]),
            "eligibility": s.get(elig_key, s["eligibility"]),
            "how_to_apply": s.get(apply_key, s["how_to_apply"]),
            "icon": s["icon"],
            "category": s["category"]
        })
    return jsonify(schemes)


if __name__ == "__main__":
    app.run(debug=True)