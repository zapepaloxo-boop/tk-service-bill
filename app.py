from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import os
from pathlib import Path

app = Flask(__name__)

# สร้างโฟลเดอร์ถ้าไม่มี
os.makedirs('static/bills', exist_ok=True)

# ข้อมูลบริษัท
COMPANY_INFO = {
    'name': 'T&K SERVICE SYSTEMS',
    'address': 'บ้าน 123 ซอย ลาดพร้าว กรุงเทพฯ 10230',
    'phone': '02-XXXXXXX',
    'tax_id': '1234567890123'
}

def create_bill_image(data):
    """สร้างรูปใบเสร็จแบบ PDF-like"""
    # กำหนดขนาดภาพ
    width, height = 850, 1200
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # พยายามโหลด font สำหรับภาษาไทย (ถ้าไม่มีให้ใช้ default)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 28)
        header_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 16)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 12)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 11)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 9)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # สีต่างๆ
    dark_blue = '#1e3a8a'
    light_gray = '#f1f5f9'
    border_color = '#cbd5e1'
    
    # วาด header
    draw.rectangle([(0, 0), (width, 100)], fill='#1e3a8a')
    draw.text((50, 20), 'T&K SERVICE SYSTEMS', fill='white', font=title_font)
    draw.text((50, 55), 'ใบแจ้งซ่อม / ใบเสร็จรับเงิน', fill='white', font=label_font)
    
    # วาด border
    draw.rectangle([(30, 100), (width-30, height-30)], outline=border_color, width=2)
    
    y_pos = 120
    
    # ข้อมูลบริษัท
    draw.text((50, y_pos), 'บริษัท: ' + COMPANY_INFO['name'], fill=dark_blue, font=label_font)
    y_pos += 25
    draw.text((50, y_pos), 'ที่อยู่: ' + COMPANY_INFO['address'], fill='#334155', font=text_font)
    y_pos += 20
    draw.text((50, y_pos), 'โทรศัพท์: ' + COMPANY_INFO['phone'], fill='#334155', font=text_font)
    y_pos += 20
    draw.text((50, y_pos), 'เลขประจำตัวผู้เสียภาษี: ' + COMPANY_INFO['tax_id'], fill='#334155', font=text_font)
    
    y_pos += 40
    
    # วาดเส้นแบ่ง
    draw.line([(50, y_pos), (width-50, y_pos)], fill=border_color, width=1)
    
    y_pos += 20
    
    # ข้อมูลลูกค้า
    draw.text((50, y_pos), 'ข้อมูลลูกค้า', fill=dark_blue, font=header_font)
    y_pos += 30
    
    draw.text((50, y_pos), 'ชื่อ: ' + data.get('name', 'N/A'), fill='#334155', font=text_font)
    y_pos += 20
    draw.text((50, y_pos), 'เบอร์ติดต่อ: ' + data.get('phone', 'N/A'), fill='#334155', font=text_font)
    y_pos += 20
    draw.text((50, y_pos), 'ที่อยู่: ' + data.get('address', '-'), fill='#334155', font=text_font)
    y_pos += 20
    draw.text((50, y_pos), 'ประเภทงาน: ' + data.get('job_type', 'N/A'), fill='#334155', font=text_font)
    y_pos += 20
    draw.text((50, y_pos), 'อุปกรณ์: ' + data.get('device', 'N/A'), fill='#334155', font=text_font)
    y_pos += 20
    draw.text((50, y_pos), 'อาการชำรุด: ' + data.get('symptom', '-'), fill='#334155', font=text_font)
    
    y_pos += 40
    
    # วาดเส้นแบ่ง
    draw.line([(50, y_pos), (width-50, y_pos)], fill=border_color, width=1)
    
    y_pos += 20
    
    # ส่วนรายการ
    draw.text((50, y_pos), 'รายการค่าบริการและวัสดุ', fill=dark_blue, font=header_font)
    y_pos += 30
    
    # Header ของตาราง
    draw.rectangle([(50, y_pos), (width-50, y_pos+30)], fill='#e2e8f0')
    draw.text((60, y_pos+8), 'รายการ', fill='#0f172a', font=label_font)
    draw.text((550, y_pos+8), 'จำนวน (บาท)', fill='#0f172a', font=label_font)
    
    y_pos += 35
    
    # รวมเงิน
    total_price = 0
    item_count = 0
    
    for i in range(1, 10):
        item_name = data.get(f'item{i}', '').strip()
        item_price = data.get(f'price{i}', 0)
        
        if item_name and item_price:
            try:
                price_value = float(item_price)
                total_price += price_value
                item_count += 1
                
                # ตัดชื่อยาวเกินไป
                display_name = item_name[:50] if len(item_name) <= 50 else item_name[:47] + '...'
                
                draw.text((60, y_pos), display_name, fill='#334155', font=text_font)
                draw.text((550, y_pos), f'{price_value:.2f}', fill='#334155', font=text_font)
                y_pos += 25
            except (ValueError, TypeError):
                continue
    
    # ถ้าไม่มีรายการ
    if item_count == 0:
        draw.text((60, y_pos), '(ไม่มีรายการ)', fill='#94a3b8', font=text_font)
        y_pos += 25
    
    y_pos += 15
    
    # วาดเส้นแบ่ง
    draw.line([(50, y_pos), (width-50, y_pos)], fill=border_color, width=2)
    
    y_pos += 20
    
    # คำนวณภาษี
    vat = total_price * 0.07
    grand_total = total_price + vat
    
    # สรุปยอดเงิน
    draw.text((450, y_pos), 'รวมค่าบริการ:', fill='#334155', font=label_font)
    draw.text((550, y_pos), f'{total_price:.2f}', fill='#334155', font=label_font)
    
    y_pos += 25
    
    draw.text((450, y_pos), 'ภาษีมูลค่าเพิ่ม (7%):', fill='#334155', font=label_font)
    draw.text((550, y_pos), f'{vat:.2f}', fill='#334155', font=label_font)
    
    y_pos += 30
    
    # วาดเส้นแบ่ง
    draw.line([(450, y_pos), (width-50, y_pos)], fill=border_color, width=2)
    
    y_pos += 15
    
    draw.rectangle([(450, y_pos), (width-50, y_pos+35)], fill='#059669')
    draw.text((460, y_pos+8), 'รวมทั้งสิ้น:', fill='white', font=header_font)
    draw.text((550, y_pos+8), f'{grand_total:.2f} บาท', fill='white', font=header_font)
    
    y_pos += 60
    
    # วัสดุและอะไหล่ (ถ้ามี)
    y_pos += 20
    draw.text((50, y_pos), 'หมายเหตุ:', fill=dark_blue, font=label_font)
    y_pos += 25
    
    # วันที่และเวลา
    now = datetime.now()
    date_str = now.strftime('%d/%m/%Y %H:%M:%S')
    draw.text((50, height-80), 'วันที่ออกบิล: ' + date_str, fill='#64748b', font=small_font)
    draw.text((50, height-60), 'ขอบคุณที่ใช้บริการ T&K Service Systems', fill='#64748b', font=small_font)
    draw.text((50, height-40), 'ติดต่อเรา โทรศัพท์: ' + COMPANY_INFO['phone'], fill='#64748b', font=small_font)
    
    return img

@app.route('/')
def index():
    """แสดงหน้าหลัก"""
    return render_template('index.html') if os.path.exists('templates/index.html') else open('index.html').read()

@app.route('/api/create_bill', methods=['POST'])
def create_bill():
    """สร้างบิล API"""
    try:
        # รับข้อมูลจาก form
        data = request.form.to_dict()
        
        # ตรวจสอบข้อมูลที่จำเป็น
        if not data.get('name') or not data.get('phone'):
            return jsonify({'error': 'ข้อมูลไม่ครบถ้วน กรุณากรอก ชื่อและเบอร์โทรศัพท์'}), 400
        
        # สร้างรูปบิล
        bill_image = create_bill_image(data)
        
        # บันทึกรูป
        filename = f"bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join('static/bills', filename)
        bill_image.save(filepath, 'PNG')
        
        return jsonify({
            'status': 'success',
            'message': 'สร้างบิลสำเร็จ',
            'image_url': f'/static/bills/{filename}',
            'filename': filename
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'เกิดข้อผิดพลาด: {str(e)}'}), 500

@app.route('/get_image/<filename>')
def get_image(filename):
    """ดาวน์โหลดรูปบิล"""
    try:
        filepath = os.path.join('static/bills', filename)
        if os.path.exists(filepath):
            return send_file(filepath, mimetype='image/png')
        return jsonify({'error': 'ไฟล์ไม่พบ'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
