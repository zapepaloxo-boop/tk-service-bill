from flask import Flask, render_template, request, send_file, redirect
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

# ตั้งค่าตำแหน่งโฟลเดอร์สำหรับดึงไฟล์ index.html
app = Flask(__name__, template_folder='.', static_folder='.')

@app.route('/')
def index():
    last_img = request.args.get('last_img', None)
    # ส่งค่าเพื่อให้หน้า index.html แสดงผลรูปบิลล่าสุด
    return render_template('index.html', last_img=last_img)

@app.route('/create_bill', methods=['POST'])
def create_bill():
    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']
    device = request.form['device']
    job_type = request.form['job_type']
    symptom = request.form['symptom']
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    bill_id = datetime.now().strftime("%d%H%M")
    
    # ดึงค่ารายการอะไหล่และราคาสุทธิ
    items = []
    total_price = 0.0
    for i in range(1, 4):
        item_text = request.form.get(f'item{i}', '')
        item_p = request.form.get(f'p{i}', '0')
        p_val = float(item_p) if item_p else 0.0
        if item_text:
            items.append((item_text, p_val))
            total_price += p_val

    # คำนวณภาษี 7% อัตโนมัติและยอดรวมสุทธิ
    vat_price = total_price * 0.07
    grand_total = total_price + vat_price

    # สร้างรูปสลิปยาว 1250 พิกเซลเพื่อรองรับรายละเอียดและเงื่อนไข
    img = Image.new('RGB', (550, 1250), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # ระบบค้นหาฟอนต์ระบบอัตโนมัติของเครื่องแอนดรอยด์
    font_paths = [
        "/system/fonts/DroidSansThai.ttf",
        "/system/fonts/NotoSansThai-Regular.ttf",
        "/system/fonts/NotoSansThaiUI-Regular.ttf"
    ]
    font_bold = font_normal = font_small = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                font_bold = ImageFont.truetype(path, 26)
                font_normal = ImageFont.truetype(path, 20)
                font_small = ImageFont.truetype(path, 16)
                break
            except:
                continue
    if font_bold is None:
        font_bold = font_normal = font_small = ImageFont.load_default()

    y_start = 30

    # ตกแต่งหัวแถบบิลสีน้ำเงินสไตล์โมเดิร์นน่าเชื่อถือ
    draw.rectangle([(0, y_start), (550, y_start+75)], fill='#1E3A8A')
    draw.text((275, y_start+38), "T&K SERVICE SYSTEMS", fill='#FFFFFF', font=font_bold, anchor="mm")
    y_start += 110
    
    draw.text((40, y_start), "ใบแจ้งซ่อม / ใบเสร็จรับเงินดิจิทัล", fill='#0f172a', font=font_bold)
    draw.text((40, y_start+35), f"เลขที่เอกสาร: TK-{bill_id}", fill='#334155', font=font_normal)
    draw.text((40, y_start+65), f"วันที่ปฏิบัติงาน: {current_date}", fill='#64748b', font=font_normal)
    draw.line([(40, y_start+95), (510, y_start+95)], fill='#cbd5e1', width=2)
    y_start += 115
    
    draw.text((40, y_start), f"ประเภทบริการ: {job_type}", fill='#1e3a8a', font=font_bold)
    draw.text((40, y_start+35), f"ชื่อลูกค้า: {name}", fill='#334155', font=font_normal)
    draw.text((40, y_start+65), f"เบอร์โทรติดต่อ: {phone}", fill='#334155', font=font_normal)
    if address:
        draw.text((40, y_start+95), f"สถานที่ปฏิบัติงาน: {address}", fill='#334155', font=font_normal)
        y_start += 30
    draw.text((40, y_start+95), f"อุปกรณ์ที่ตรวจสอบ: {device}", fill='#334155', font=font_normal)
    draw.text((40, y_start+125), f"ลักษณะอาการเสีย: {symptom if symptom else 'ตรวจเช็กสภาพระบบทั่วไป'}", fill='#334155', font=font_normal)
    y_start += 165
    
    draw.line([(40, y_start), (510, y_start)], fill='#cbd5e1', width=2)
    draw.text((40, y_start+15), "ตารางแจกแจงรายการวัสดุ / ค่าบริการ", fill='#0f172a', font=font_bold)
    y_offset = y_start + 50
    
    if not items:
        draw.text((40, y_offset), "- ตรวจเช็กบำรุงรักษาสภาพทั่วไป -", fill='#64748b', font=font_normal)
        y_offset += 35
    else:
        for it_title, it_cost in items:
            draw.text((40, y_offset), f"• {it_title}", fill='#334155', font=font_normal)
            draw.text((510, y_offset), f"{it_cost:,.2f}", fill='#334155', font=font_normal, anchor="ra")
            y_offset += 35
            
    draw.line([(40, y_offset+10), (510, y_offset+10)], fill='#cbd5e1', width=1)
    
    # แสดงยอดคำนวณภาษี 7% แยกช่องตามใบกระดาษแบบน่าเชื่อถือ
    draw.text((40, y_offset+30), "รวมค่าบริการอะไหล่", fill='#475569', font=font_normal)
    draw.text((510, y_offset+30), f"{total_price:,.2f}", fill='#475569', font=font_normal, anchor="ra")
    
    draw.text((40, y_offset+55), "ภาษีมูลค่าเพิ่ม VAT 7%", fill='#475569', font=font_normal)
    draw.text((510, y_offset+55), f"{vat_price:,.2f}", fill='#475569', font=font_normal, anchor="ra")
    
    draw.line([(40, y_offset+85), (510, y_offset+85)], fill='#1E3A8A', width=3)
    draw.text((40, y_offset+110), "ยอดรวมทั้งสิ้นสุทธิ", fill='#0f172a', font=font_bold)
    draw.text((510, y_offset+110), f"{grand_total:,.2f} บาท", fill='#1E3A8A', font=font_bold, anchor="ra")
    draw.line([(40, y_offset+140), (510, y_offset+140)], fill='#cbd5e1', width=1)
    
    # บันทึกข้อกำหนดเงื่อนไขประกัน 30 วันติดท้ายบิลสไตล์สากล
    y_cond = y_offset + 165
    draw.text((40, y_cond), "รายละเอียดเงื่อนไขและข้อตกลงการบริการ", fill='#1e3a8a', font=font_bold)
    
    cond_lines = [
        "1. การรับประกัน: T&K รับประกันงานซ่อมและชิ้นส่วนอะไหล่เป็นเวลา 30 วัน",
        "   นับจากวันที่ส่งมอบงาน (ไม่รวมกรณีอุบัติเหตุหรือใช้งานผิดประเภท)",
        "2. การมัดจำ: กรณีสั่งซื้ออะไหล่เฉพาะทาง ลูกค้าต้องมัดจำล่วงหน้า 50%",
        "3. ความปลอดภัย: ศูนย์บริการยึดมั่นในความปลอดภัยระบบไฟฟ้าหน้างาน",
        "4. การติดต่อ: หากพบปัญหาหลังบริการ กรุณาติดต่อช่างผู้ชำนาญการโดยตรง"
    ]
    y_cond += 30
    for line_text in cond_lines:
        draw.text((40, y_cond), line_text, fill='#64748b', font=font_small)
        y_cond += 22
        
    draw.line([(40, y_cond+15), (510, y_cond+15)], fill='#cbd5e1', width=1)
    draw.text((275, y_cond+40), "ขอบพระคุณที่เลือกใช้บริการความไว้วางใจใน T&K", fill='#64748b', font=font_normal, anchor="mm")
    draw.text((275, y_cond+65), "ช่างประสงค์ นันตะบุตร | ผู้ตรวจสอบ/รับงาน", fill='#475569', font=font_normal, anchor="mm")
    draw.text((275, y_cond+90), "โทร. 0636718151 / ศูนย์บริการซ่อมติดตั้งครบวงจร", fill='#64748b', font=font_small, anchor="mm")
    
    img_name = "current_receipt.png"
    img.save(img_name)
    return redirect(f"/?last_img={img_name}")

@app.route('/get_image/<filename>')
def get_image(filename):
    return send_file(filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
