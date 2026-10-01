import requests
from vpython import *
import time

# --- הגדרות ---
# שים לב לשינוי בכתובת בסוף: אנחנו עכשיו מבקשים gyr במקום acc
URL = "http://192.168.68.117:8081/get?gyrX&gyrY&gyrZ"

# יצירת הסביבה
scene = canvas(title='RoboPhysics - Gyroscope Sync', width=800, height=600, background=vector(0.2, 0.2, 0.2))

palm = box(size=vector(4, 0.5, 5), color=color.orange)
fingers = box(pos=vector(0, 0, -3.5), size=vector(4, 0.4, 2), color=color.cyan)
hand = compound([palm, fingers])
floor = box(pos=vector(0, -4, 0), size=vector(15, 0.1, 15), color=color.white, opacity=0.3)

print("מתחבר לחיישן הג'יירוסקופ בנייד...")

# משתנה לשמירת הזמן הקודם (כדי לחשב כמה זמן עבר)
last_time = time.time()

while True:
    rate(30)
    
    try:
        response = requests.get(URL, timeout=1.0)
        if response.status_code != 200:
            continue
            
        data = response.json()
        
        # משיכת מהירות הסיבוב מהג'יירו (הערכים מגיעים ברדיאנים לשנייה)
        gx = data['buffer']['gyrX']['buffer'][0]
        gy = data['buffer']['gyrY']['buffer'][0]
        gz = data['buffer']['gyrZ']['buffer'][0]
        
        # מתמטיקה/פיזיקה: חישוב הזמן שעבר (dt)
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        # סיבוב האובייקט לפי מהירות הסיבוב כפול הזמן שעבר (זווית = מהירות * זמן)
        # ייתכן שתצטרך לשחק עם המינוסים כאן כדי שזה יתאים בדיוק לכיוונים של הטלפון שלך
        hand.rotate(angle=gx * dt, axis=vector(1, 0, 0)) # סיבוב בציר X (עלרוד / Pitch)
        hand.rotate(angle=gy * dt, axis=vector(0, 1, 0)) # סיבוב בציר Y (סבסוב / Yaw)
        hand.rotate(angle=gz * dt, axis=vector(0, 0, 1)) # סיבוב בציר Z (גלגול / Roll)
        
    except Exception as e:
        # במקרה של שגיאה או עיכוב ברשת, נמשיך הלאה ונעדכן את הזמן
        last_time = time.time()