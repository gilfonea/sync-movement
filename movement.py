import requests
from vpython import *
import time

# --- הגדרות ---
URL = "http://192.168.68.117:8081/get?gyrX&gyrY&gyrZ"

# יצירת הסביבה - רקע שחור עמוק כדי שהכל יבלוט
scene = canvas(title='RoboPhysics - Missile Telemetry Sync', width=800, height=600, background=color.black)

# --- יצירת מודל הטיל (מיירט) ---
# 1. גוף הטיל (גליל לבן)
body = cylinder(pos=vector(0, -3, 0), axis=vector(0, 6, 0), radius=0.4, color=color.white)

# 2. חרטום/ראש קרב (חרוט אפור בהיר)
nose = cone(pos=vector(0, 3, 0), axis=vector(0, 1.5, 0), radius=0.4, color=color.gray(0.6))

# 3. כנפוני ניהוג (סנפירים בתחתית) - צבע אדום בולט
fin_color = color.red
fin1 = box(pos=vector(0.4, -2.5, 0), size=vector(1.5, 1.5, 0.05), color=fin_color)
fin2 = box(pos=vector(-0.4, -2.5, 0), size=vector(1.5, 1.5, 0.05), color=fin_color)
fin3 = box(pos=vector(0, -2.5, 0.4), size=vector(0.05, 1.5, 1.5), color=fin_color)
fin4 = box(pos=vector(0, -2.5, -0.4), size=vector(0.05, 1.5, 1.5), color=fin_color)

# איחוד כל החלקים לאובייקט אחד שנוכל לסובב יחד
missile = compound([body, nose, fin1, fin2, fin3, fin4])

# משטח קרקע - ציאן חצי שקוף למראה טכנולוגי
floor = box(pos=vector(0, -5, 0), size=vector(20, 0.1, 20), color=color.cyan, opacity=0.2)

# --- הוספת צירי מערכת (X, Y, Z) למרחב ---
axis_len = 6

# ציר X (אדום)
arrow(pos=vector(0,0,0), axis=vector(axis_len, 0, 0), color=color.red, shaftwidth=0.05)
label(pos=vector(axis_len, 0, 0), text='X', box=False, color=color.red, yoffset=10)

# ציר Y (ירוק)
arrow(pos=vector(0,0,0), axis=vector(0, axis_len, 0), color=color.green, shaftwidth=0.05)
label(pos=vector(0, axis_len, 0), text='Y', box=False, color=color.green, xoffset=10)

# ציר Z (כחול)
arrow(pos=vector(0,0,0), axis=vector(0, 0, axis_len), color=color.blue, shaftwidth=0.05)
label(pos=vector(0, 0, axis_len), text='Z', box=False, color=color.blue, yoffset=10)


print("מתחבר לחיישן הג'יירוסקופ בנייד...")

last_time = time.time()

# --- לולאת הזמן אמת ---
while True:
    rate(30)
    
    try:
        response = requests.get(URL, timeout=1.0)
        if response.status_code != 200:
            continue
            
        data = response.json()
        
        gx = data['buffer']['gyrX']['buffer'][0]
        gy = data['buffer']['gyrY']['buffer'][0]
        gz = data['buffer']['gyrZ']['buffer'][0]
        
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        # סיבוב הטיל במרחב
        missile.rotate(angle=gx * dt, axis=vector(1, 0, 0)) # עלרוד (Pitch)
        missile.rotate(angle=gy * dt, axis=vector(0, 1, 0)) # סבסוב (Yaw)
        missile.rotate(angle=gz * dt, axis=vector(0, 0, 1)) # גלגול (Roll)
        
    except Exception as e:
        last_time = time.time()