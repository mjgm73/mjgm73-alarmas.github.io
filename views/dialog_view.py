import customtkinter as ctk
from tkinter import messagebox
from utils import centrar_ventana

class DialogView:
    @staticmethod
    def show_alarm_dialog(parent, alarm_data=None, days_of_week=None):
        dialog = ctk.CTkToplevel(parent)
        dialog.title("Nueva Alarma" if alarm_data is None else "Editar Alarma")
        dialog.geometry("700x350")
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()
        ventana=centrar_ventana
        ventana.centrar_ventana(dialog, 700, 350)
        
        # Variables
        hour_var = ctk.StringVar(value="08" if alarm_data is None else str(alarm_data[1]))
        minute_var = ctk.StringVar(value="00" if alarm_data is None else str(alarm_data[2]))
        
        # Contenedor de tiempo
        time_frame = ctk.CTkFrame(dialog)
        time_frame.pack(pady=(20, 10), padx=20, fill="x")
        
        ctk.CTkLabel(time_frame, text="Hora:", font=("Arial", 16)).grid(row=0, column=0, padx=5, pady=5)
        hour_entry = ctk.CTkEntry(time_frame, textvariable=hour_var, width=60)
        hour_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(time_frame, text="Minutos:", font=("Arial", 16)).grid(row=0, column=2, padx=5, pady=5)
        minute_entry = ctk.CTkEntry(time_frame, textvariable=minute_var, width=60)
        minute_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Etiqueta
        ctk.CTkLabel(dialog, text="Etiqueta:", font=("Arial", 16)).pack(pady=(10, 5))
        label_entry = ctk.CTkEntry(dialog, width=200)
        label_entry.pack()
        if alarm_data:
            label_entry.insert(0, alarm_data[4] if alarm_data[4] else "")
        else:
            label_entry.insert(0, "Alarma")
        
        # Días de repetición
        ctk.CTkLabel(dialog, text="Repetir:", font=("Arial", 16)).pack(pady=(15, 5))
        
        repeat_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        repeat_frame.pack()
        
        repeat_vars = []
        repeat_btns = []
        
        repeat_pattern = '0000000'
        if alarm_data and alarm_data[5]:
            repeat_pattern = alarm_data[5]
        
        for i, day in enumerate(days_of_week):
            var = ctk.IntVar(value=1 if repeat_pattern[i] == '1' else 0)
            repeat_vars.append(var)
            
            btn = ctk.CTkCheckBox(repeat_frame, text=day, variable=var, 
                                 onvalue=1, offvalue=0)
            btn.grid(row=0, column=i, padx=3)
            repeat_btns.append(btn)
        
        # Recordatorio de formato
        ctk.CTkLabel(dialog, text="Formato: 24 horas", font=("Arial", 12), 
                    text_color="gray").pack(pady=5)
        
        # Etiqueta de error
        error_label = ctk.CTkLabel(dialog, text="", text_color="red")
        error_label.pack(pady=5)
        
        return dialog, hour_var, minute_var, label_entry, repeat_vars, error_label
    
    @staticmethod
    def show_confirm_dialog(parent, title, message):
        confirm_dialog = ctk.CTkToplevel(parent)
        confirm_dialog.title(title)
        confirm_dialog.geometry("350x200")
        confirm_dialog.resizable(False, False)
        confirm_dialog.transient(parent)
        confirm_dialog.grab_set()
        
        ctk.CTkLabel(confirm_dialog, text=message, 
                     font=("Arial", 18)).pack(pady=30)
        
        return confirm_dialog
    
    @staticmethod
    def show_alarm_trigger_dialog(parent, label):
        alarm_dialog = ctk.CTkToplevel(parent)
        alarm_dialog.title("¡Alarma!")
        alarm_dialog.geometry("450x450")
        alarm_dialog.resizable(False, False)
        alarm_dialog.transient(parent)
        alarm_dialog.grab_set()
        alarm_dialog.attributes('-topmost', True)
        ventana=centrar_ventana
        ventana.centrar_ventana(alarm_dialog,450,450)
        # Icono de alarma grande
        alarm_icon = ctk.CTkLabel(alarm_dialog, text="⏰", font=("Arial", 64))
        alarm_icon.pack(pady=20)
        
        ctk.CTkLabel(alarm_dialog, text="¡Alarma!", 
                    font=("Arial", 28, "bold")).pack(pady=10)
        
        if label:
            ctk.CTkLabel(alarm_dialog, text=label, 
                        font=("Arial", 20)).pack(pady=5)
        
        # Handle window close (X button)
        """ def on_close():
            alarm_dialog.destroy()
        
        alarm_dialog.protocol("WM_DELETE_WINDOW", on_close) """
        
        return alarm_dialog
    
    @staticmethod
    def show_notification(parent, message):
        notification = ctk.CTkToplevel(parent)
        notification.geometry("300x60+50+50")
        notification.overrideredirect(1)
        notification.attributes('-alpha', 0.9)
        notification.lift()
        #ventana=centrar_ventana
        #ventana.centrar_ventana(notification,300,60)
        
        frame = ctk.CTkFrame(notification, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(frame, text=message, font=("Arial", 14)).pack(pady=15)
        notification.after(3000, notification.destroy)