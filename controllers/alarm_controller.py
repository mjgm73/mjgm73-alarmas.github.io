import threading
import time
import datetime
import winsound
from models.alarm_model import AlarmModel
from views.dialog_view import DialogView
import customtkinter as ctk
from tkinter import messagebox
from utils import centrar_ventana
#from qgis.PyQt.QtWidgets import QMessageBox

class AlarmController:
    def __init__(self, view):
        self.view = view
        self.model = AlarmModel()
        self.snooze_time = None
        self.snooze_duration = 5
        self.ventana=centrar_ventana
        self.vent=DialogView
        
        # Configurar eventos
        self.view.add_button.configure(command=self.add_alarm_dialog)
        self.view.snooze_var.trace_add("write", self.update_snooze_duration)
        
        # Cargar alarmas iniciales
        self.refresh_alarms()
        self.start_alarm_checker()
    
    def update_snooze_duration(self, *args):
        try:
            self.snooze_duration = int(self.view.snooze_var.get())
        except:
            self.snooze_duration = 5
    
    def refresh_alarms(self):
        alarms = self.model.load_alarms()
        self.view.refresh_alarms_list(alarms, self.edit_alarm, self.toggle_alarm, self.confirm_delete)
    
    def add_alarm_dialog(self, alarm_id=None):
        alarm_data = None
        if alarm_id:
            for alarm in self.model.load_alarms():
                if alarm[0] == alarm_id:
                    alarm_data = alarm
                    break
        
        dialog, hour_var, minute_var, label_entry, repeat_vars, error_label = DialogView.show_alarm_dialog(
            self.view, alarm_data, self.model.days_of_week
        )
        
        def save_alarm():
            try:
                hour = int(hour_var.get())
                minute = int(minute_var.get())
                label = label_entry.get()
                repeat_pattern = ''.join(str(var.get()) for var in repeat_vars)
                
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    if alarm_id:
                        self.model.update_alarm(alarm_id, hour, minute, label, repeat_pattern)
                    else:
                        self.model.add_alarm(hour, minute, label, repeat_pattern)
                    
                    self.refresh_alarms()
                    dialog.destroy()
                else:
                    error_label.configure(text="Hora inválida! Use formato 24h")
            except ValueError:
                error_label.configure(text="Ingrese números válidos")
        
        # Botón de guardado
        save_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        save_frame.pack(pady=20)
        
        ctk.CTkButton(save_frame, text="Cancelar", 
                     command=dialog.destroy).pack(side="left", padx=10)
        ctk.CTkButton(save_frame, text="Guardar", 
                     command=save_alarm).pack(side="right", padx=10)
    
    def edit_alarm(self, alarm_id):
        self.add_alarm_dialog(alarm_id)
    
    def confirm_delete(self, alarm_id):
        confirm_dialog = DialogView.show_confirm_dialog(
            self.view, "Confirmar eliminación", "¿Eliminar esta alarma?"
        )
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(confirm_dialog, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="Cancelar", 
                     command=confirm_dialog.destroy).pack(side="left", padx=20)
        ctk.CTkButton(btn_frame, text="Eliminar", fg_color="#d32f2f",
                     command=lambda: self.delete_alarm(alarm_id, confirm_dialog)).pack(side="right", padx=20)
    
    def toggle_alarm(self, alarm_id):
        self.model.toggle_alarm(alarm_id)
        self.refresh_alarms()
    
    def delete_alarm(self, alarm_id, dialog=None):
        self.model.delete_alarm(alarm_id)
        self.refresh_alarms()
        if dialog:
            dialog.destroy()
    
    def check_alarms(self):
        while True:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            current_weekday = now.weekday()  # Lunes=0, Domingo=6
            
            # Verificar alarmas snooze primero
            if self.snooze_time and self.snooze_time.strftime("%H:%M") == current_time:
                self.trigger_alarm(None, "Alarma Snooze", is_snooze=True)
                #self.trigger_alarm(alarm_id, "Alarma Snooze", is_snooze=True)
                self.snooze_time = None
            
            # Verificar alarmas regulares
            for alarm in self.model.load_alarms():
                alarm_id, hour, minute, active, label, repeat, snooze = alarm
                alarm_time = f"{hour:02d}:{minute:02d}"
                
                repeat_today = repeat[current_weekday] == '1' if repeat else False
                
                if active and not snooze and current_time == alarm_time:
                    if repeat == '0000000' or repeat_today:
                        self.trigger_alarm(alarm_id, label, repeat != '0000000')
            
            time.sleep(30)  # Verificar cada 30 segundos
    
    def trigger_alarm2(self, alarm_id, label, is_repeating=False):
        if not is_repeating:
            self.model.toggle_alarm(alarm_id)
        
        alarm_dialog = DialogView.show_alarm_trigger_dialog(self.view, label)
        
        # Botones de snooze
        snooze_frame = ctk.CTkFrame(alarm_dialog, fg_color="transparent")
        snooze_frame.pack(pady=15)
        
        snooze_times = [5, 10, 15, 30]
        for minutes in snooze_times:
            ctk.CTkButton(snooze_frame, text=f"Snooze ({minutes} min)", 
                         width=120, height=40,
                         command=lambda m=minutes: self.set_snooze(m, alarm_dialog)
                         ).grid(row=(minutes-1)//15, column=(minutes%15)//5, 
                                padx=5, pady=5) 
        
        
        for minutes in snooze_times:
            ctk.CTkButton(
                snooze_frame, 
                text=f"Snooze ({minutes} min)", 
                width=120, 
                height=40,
                command=lambda m=minutes, dialog=alarm_dialog: self.set_snooze(m, dialog)
            ).grid(
                row=(minutes-1)//15, 
                column=(minutes%15)//5, 
                padx=5, 
                pady=5
            ) 
        
        # Botón para detener
        ctk.CTkButton(alarm_dialog, text="Detener", 
                     width=150, height=50, font=("Arial", 16, "bold"),
                     command=lambda: self.stop_alarm(alarm_dialog)).pack(pady=20)
        
        # Handle window close (X button)
        def on_close():
            alarm_dialog.destroy() 
        
        #alarm_dialog.protocol("WM_DELETE_WINDOW", self.stop_alarm(alarm_dialog))
        alarm_dialog.protocol("WM_DELETE_WINDOW", lambda: self.stop_alarm(alarm_dialog))
        
        
        # Reproducir sonido
        self.play_alarm_sound(alarm_dialog) 
    
    def trigger_alarm(self, alarm_id, label, is_repeating=False, is_snooze=False):
        # Si no es una alarma snooze y no es repetitiva, toggleamos el estado
        if not is_repeating and not is_snooze:
            self.model.toggle_alarm(alarm_id)
        
        # Mostramos el diálogo de alarma
        
        #if self.view.iconify():
        if not self.view.winfo_ismapped():  # Si la ventana está minimizada
            #print("La ventana está minimizada")
            self.view.deiconify()  # Restaura la ventana principal
            self.view.focus_force()         # Opcional: Dar foco a la ventana
        else:
            pass
            #print("La ventana está visible o maximizada")
            
        #self.view.deiconify()  # Restaura la ventana principal

        alarm_dialog = DialogView.show_alarm_trigger_dialog(self.view, label)
        
        # Configuramos el frame para los botones de snooze
        snooze_frame = ctk.CTkFrame(alarm_dialog, fg_color="transparent")
        snooze_frame.pack(pady=15)
        
        # Opciones de snooze
        snooze_times = [5, 10, 15, 30]
        for minutes in snooze_times:
            ctk.CTkButton(
                snooze_frame, 
                text=f"Snooze ({minutes} min)", 
                width=120, 
                height=40,
                command=lambda m=minutes: self.set_snooze(m, alarm_dialog)
            ).grid(
                row=(minutes-1)//15, 
                column=(minutes%15)//5, 
                padx=5, 
                pady=5
            )
        
        # Botón para detener la alarma
        ctk.CTkButton(
            alarm_dialog, 
            text="Detener", 
            width=150, 
            height=50, 
            font=("Arial", 16, "bold"),
            command=lambda: self.stop_alarm(alarm_dialog)
        ).pack(pady=20)
        
        # Manejar el cierre de la ventana
        alarm_dialog.protocol("WM_DELETE_WINDOW", lambda: self.stop_alarm(alarm_dialog))
        
        # Reproducir sonido de alarma (con lógica diferente para snooze si es necesario)
        #self.play_alarm_sound(alarm_dialog, is_snooze=is_snooze)
        # Reproducir sonido
        self.play_alarm_sound(alarm_dialog) 
    
    def play_alarm_sound(self, dialog):
        def sound_thread():
            try:
                duration = 1000  # 1 segundo
                for _ in range(60):  # Máximo 60 segundos
                    if hasattr(dialog, 'sound_active') and not dialog.sound_active:
                        return
                    winsound.Beep(1000, duration)
                    time.sleep(1)
            except:
                pass
        
        dialog.sound_active = True
        threading.Thread(target=sound_thread, daemon=True).start()
    
    def stop_alarm_sound(self, dialog):
        if hasattr(dialog, 'sound_active'):
            dialog.sound_active = False
    
    def set_snooze2(self, minutes, dialog):
        #messagebox.showinfo("M","Miguel")
        if not dialog.winfo_exists():  # Si la ventana ya fue destruida
            print("La ventana de alarma ya está cerrada")
            return
        """ self.snooze_duration = minutes
        now = datetime.datetime.now()
        self.snooze_time = now + datetime.timedelta(minutes=minutes)
        
        DialogView.show_notification(self.view, f"Snooze activado: {minutes} minutos")
        #if dialog.winfo_exists():  # Check if window still exists
        self.stop_alarm_sound(dialog)
        dialog.destroy() """
        
        # Bloquea la ventana principal para evitar cierre accidental
        dialog.grab_set_global()  # Opcional: Evita interacciones con otras ventanas
        
        try:
            self.snooze_duration = minutes
            now = datetime.datetime.now()
            self.snooze_time = now + datetime.timedelta(minutes=minutes)
            
            DialogView.show_notification(self.view, f"Snooze activado: {minutes} minutos")
            
           # DialogView.show_notification(self.vent.show_alarm_trigger_dialog, f"Snooze activado: {minutes} minutos")
            #messagebox.showinfo("Snooze",f"Snooze activado: {minutes} minutos")
            #self.ventana(ven,200,200)
            #show_temporary_notification("Notificación", f"Snooze activado: {minutes} minutos")
            self.stop_alarm_sound(dialog)
            # Configurar el cierre automático
            duration=5000
            def close_dialog():
                dialog.destroy()
            
            
        finally:
            # Asegura que la ventana se cierre incluso si hay errores
            if dialog.winfo_exists():
                #self.stop_alarm_sound(dialog)
                Timer(duration/1000, close_dialog).start()  # Convertir ms a segundos
            
                #dialog2.destroy()
                
                #pass
    def set_snooze(self, minutes, dialog):
        # Verificar si el diálogo sigue existiendo
        if not dialog.winfo_exists():
            print("La ventana de alarma ya está cerrada")
            return
        
        try:
            # Configurar el tiempo de snooze
            self.snooze_duration = minutes
            self.snooze_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            
            # Mostrar notificación
            DialogView.show_notification(self.view, f"Snooze activado: {minutes} minutos")
            
            # Detener el sonido de la alarma
            self.stop_alarm_sound(dialog)
            
            # Programar el cierre del diálogo después de 5 segundos
            duration_ms = 5000  # 5 segundos
            def close_dialog():
                if dialog.winfo_exists():
                    dialog.destroy()
            
            # Usar after() en lugar de Timer para mejor integración con Tkinter
            dialog.after(duration_ms, close_dialog)
            
        except Exception as e:
            print(f"Error al configurar snooze: {str(e)}")
            if dialog.winfo_exists():
                dialog.destroy()
            
    def stop_alarm(self, dialog):
        self.stop_alarm_sound(dialog)
        self.refresh_alarms()
        dialog.destroy()
    
    def start_alarm_checker(self):
        thread = threading.Thread(target=self.check_alarms, daemon=True)
        thread.start()
    
    def update_time(self):
        now = datetime.datetime.now()
        self.view.update_time_display(now.strftime("%H:%M:%S"))
        self.view.after(1000, self.update_time)
    
    def on_closing(self):
        self.model.close()
        self.view.destroy()
    
    import customtkinter as ctk
from threading import Timer

def show_temporary_notification(title, message, duration=5000):
    """Muestra un mensaje que se cierra automáticamente después de duration milisegundos"""
    # Crear la ventana de notificación
    dialog2 = ctk.CTkToplevel()
    dialog2.title(title)
    dialog2.geometry("300x150")
    dialog2.attributes('-topmost', True)  # Mantener sobre otras ventanas
    
    # Añadir contenido
    label = ctk.CTkLabel(dialog2, text=message)
    label.pack(pady=20)
    
    # Configurar el cierre automático
    def close_dialog():
        dialog2.destroy()
    
    Timer(duration/1000, close_dialog).start()  # Convertir ms a segundos
    
    return dialog2

# Ejemplo de uso
#minutes = 10


# Ejemplo de uso
