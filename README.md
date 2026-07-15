# 🔧 T&K Service Bill System

ระบบออกบิลซ่อมและติดตั้งอุปกรณ์ดีไซน์โมเดิร์น สำหรับบริษัท T&K Service

## ✨ ฟีเจอร์เด่น

- ✅ **ออกบิลอัตโนมัติ** - สร้างรูปใบเสร็จพร้อมออกแบบ
- ✅ **ส่วนต่อประสานสวยงาม** - Design responsive ใช้งานง่าย
- ✅ **คำนวณภาษี** - คำนวณภาษีมูลค่าเพิ่ม 7% อัตโนมัติ
- ✅ **เพิ่มรายการได้ไม่จำกัด** - เพิ่มรายการอะไหล่ได้ตามต้องการ
- ✅ **ดาวน์โหลดบิล** - บันทึกใบเสร็จลงเครื่องเป็นรูป PNG

## 📋 ข้อมูลลูกค้า

- ชื่อ - นามสกุล ⭐
- เบอร์โทรศัพท์ ⭐
- ที่อยู่
- ประเภทงาน
- ประเภทอุปกรณ์

## 🛠️ รายการค่าบริการ

- รายการอะไหล่ (ไม่จำกัดจำนวน)
- ราคาต่อรายการ
- รวมค่าบริการ
- ภาษีมูลค่าเพิ่ม 7%
- **รวมทั้งสิ้น**

## 🚀 การติดตั้ง

### ต้องการ
- Python 3.8+
- pip

### ขั้นตอนการติดตั้ง

```bash
# 1. Clone repository
git clone https://github.com/zapepaloxo-boop/tk-service-bill.git
cd tk-service-bill

# 2. สร้าง virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. ติดตั้ง dependencies
pip install -r requirements.txt

# 4. รัน application
python app.py
```

เปิด browser และไปที่ `http://localhost:5000`

## 📁 โครงสร้างโปรเจค

```
tk-service-bill/
├── index.html              # หน้า HTML หลัก
├── app.py                  # Backend Flask
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
└── static/
    └── bills/             # โฟลเดอร์เก็บรูปบิล
```

## 🎨 การใช้งาน

1. **กรอกข้อมูลลูกค้า**
   - ชื่อ-นามสกุลและเบอร์ติดต่อ (บังคับ)
   - ที่อยู่และรายละเอียดงาน (ตัวเลือก)

2. **เพิ่มรายการค่าบริการ**
   - กรอกชื่อรายการและราคา
   - ระบบจะคำนวณรวมเงินอัตโนมัติ
   - กดปุ่ม "เพิ่มรายการ" เพื่อเพิ่มรายการใหม่

3. **สร้างบิล**
   - กดปุ่ม "ประมวลผลและออกบิล"
   - ระบบจะสร้างรูปใบเสร็จและแสดงด้านล่าง

4. **ดาวน์โหลดบิล**
   - กดปุ่ม "บันทึกรูปบิลลงเครื่อง"
   - บิลจะบันทึกเป็นรูป PNG

## 🔧 ปรับแต่ง

แก้ไขข้อมูลบริษัท ใน `app.py`:

```python
COMPANY_INFO = {
    'name': 'T&K SERVICE SYSTEMS',
    'address': 'บ้าน 123 ซอย ลาดพร้าว กรุงเทพฯ 10230',
    'phone': '02-XXXXXXX',
    'tax_id': '1234567890123'
}
```

## 📞 ติดต่อ

- 📱 โทรศัพท์: 02-XXXXXXX
- 📧 Email: contact@tkservice.com

## 📄 ลิขสิทธิ์

© 2026 T&K Service Systems. All rights reserved.

## 🐛 รายงานปัญหา

พบปัญหา? [เปิด Issue ที่นี่](https://github.com/zapepaloxo-boop/tk-service-bill/issues)

---

**Version:** 1.0 Modern Edition  
**Last Updated:** July 15, 2026
