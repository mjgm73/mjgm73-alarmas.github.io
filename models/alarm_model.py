import sqlite3
import datetime

class AlarmModel:
    def __init__(self, db_name='alarms.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.c = self.conn.cursor()
        self.create_table()
        self.days_of_week = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    
    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS alarms
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      hour INTEGER NOT NULL,
                      minute INTEGER NOT NULL,
                      active INTEGER DEFAULT 1,
                      label TEXT,
                      repeat TEXT DEFAULT '0000000',
                      snooze INTEGER DEFAULT 0)''')
        self.conn.commit()
    
    def load_alarms(self):
        self.c.execute("SELECT * FROM alarms ORDER BY hour, minute")
        return self.c.fetchall()
    
    def add_alarm(self, hour, minute, label, repeat_pattern):
        self.c.execute("INSERT INTO alarms (hour, minute, label, repeat) VALUES (?, ?, ?, ?)",
                      (hour, minute, label, repeat_pattern))
        self.conn.commit()
        return self.c.lastrowid
    
    def update_alarm(self, alarm_id, hour, minute, label, repeat_pattern):
        self.c.execute("UPDATE alarms SET hour=?, minute=?, label=?, repeat=? WHERE id=?",
                      (hour, minute, label, repeat_pattern, alarm_id))
        self.conn.commit()
    
    def toggle_alarm(self, alarm_id):
        self.c.execute("SELECT active FROM alarms WHERE id=?", (alarm_id,))
        current = self.c.fetchone()[0]
        new_state = 0 if current else 1
        self.c.execute("UPDATE alarms SET active=? WHERE id=?", (new_state, alarm_id))
        self.conn.commit()
        return new_state
    
    def delete_alarm(self, alarm_id):
        self.c.execute("DELETE FROM alarms WHERE id=?", (alarm_id,))
        self.conn.commit()
    
    def set_snooze(self, alarm_id, snooze):
        self.c.execute("UPDATE alarms SET snooze=? WHERE id=?", (snooze, alarm_id))
        self.conn.commit()
    
    def close(self):
        self.conn.close()
    
    def get_days_text(self, repeat_pattern):
        days = []
        for i, day in enumerate(repeat_pattern):
            if day == '1':
                days.append(self.days_of_week[i])
        return ', '.join(days)