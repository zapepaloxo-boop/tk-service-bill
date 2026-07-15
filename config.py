import os
from dotenv import load_dotenv

# โหลด environment variables จาก .env file
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', False)
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Company Information
    COMPANY_INFO = {
        'name': os.getenv('COMPANY_NAME', 'T&K SERVICE SYSTEMS'),
        'address': os.getenv('COMPANY_ADDRESS', 'บ้าน 123 ซอย ลาดพร้าว กรุงเทพฯ 10230'),
        'phone': os.getenv('COMPANY_PHONE', '02-XXXXXXX'),
        'tax_id': os.getenv('COMPANY_TAX_ID', '1234567890123')
    }
    
    # Bill Settings
    VAT_RATE = 0.07  # ภาษีมูลค่าเพิ่ม 7%
    BILL_FOLDER = 'static/bills'
    MAX_ITEMS = 20  # จำนวนรายการสูงสุดต่อบิล

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # ต้องระบุใน .env

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# เลือก config ตามสภาพแวดล้อม
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """ได้ config object ตามสภาพแวดล้อม"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
