import customtkinter as ctk
from PIL import Image
from utils import centrar_ventana
from datetime import datetime
import locale

class AlarmView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Alarmas Agenda Personal")
        self.geometry("400x600")
        self.resizable(False, False)
        ventana=centrar_ventana
        #self.cv=centrar_ventana
        locale.setlocale(locale.LC_TIME, 'spanish')    # Windows
        self.fecha_actual = datetime.now().date()
        #print(fecha_actual.strftime("%d/%m/%Y"))
        #print(fecha_actual.strftime("%A, %d de %B de %Y"))  
        #print(fecha_actual .strftime("%A, %d de %B de %Y"))  
        # Variables
        self.current_time = ctk.StringVar()
        
        # Configuración de tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Crear widgets
        self.create_header()
        self.create_alarms_frame()
        self.create_snooze_frame()
        self.create_bottom_buttons()
        #self.self.cv(400, 600)
        ventana.centrar_ventana(self, 400, 600)
        
    
    """ def centrar_ventana(self, ancho=None, alto=None):
        #Centra la ventana en la pantalla
        self.update_idletasks()
        
        if ancho is None:
            ancho = self.winfo_width()
        if alto is None:
            alto = self.winfo_height()
        
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        
        self.geometry(f'{ancho}x{alto}+{x}+{y}') """
    
    def create_header(self):
        self.header_frame = ctk.CTkFrame(self, height=100, corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        
        # --- Nueva Label ENCIMA de time_label ---
        self.top_label = ctk.CTkLabel(
            self.header_frame, 
            text=self.fecha_actual .strftime("%A, %d de %B de %Y"), 
            font=("Arial", 24),  # Puedes ajustar el tamaño y estilo
            fg_color="transparent"
        )
        self.top_label.pack(pady=(5, 5))  # pady=(arriba, abajo)

        
        self.time_label = ctk.CTkLabel(self.header_frame, textvariable=self.current_time, 
                                     font=("Arial", 45), fg_color="transparent")
        self.time_label.pack(pady=20)
    
    def create_alarms_frame(self):
        self.alarms_frame = ctk.CTkScrollableFrame(self, width=350, height=350)
        self.alarms_frame.pack(pady=(10, 10), padx=20)
    
    def create_snooze_frame(self):
        self.snooze_frame = ctk.CTkFrame(self, height=50)
        self.snooze_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.snooze_frame, text="Snooze:", font=("Arial", 14)).pack(side="left", padx=(10, 5))
        
        self.snooze_var = ctk.StringVar(value="5")
        snooze_options = ["5", "10", "15", "30"]
        self.snooze_menu = ctk.CTkOptionMenu(self.snooze_frame, 
                                           values=snooze_options,
                                           variable=self.snooze_var,
                                           width=60)
        self.snooze_menu.pack(side="left", padx=5)
        ctk.CTkLabel(self.snooze_frame, text="min", font=("Arial", 14)).pack(side="left", padx=5)
    
    def create_bottom_buttons(self):
        self.bottom_frame = ctk.CTkFrame(self, height=60, fg_color="transparent")
        self.bottom_frame.pack(fill="x", padx=20, pady=10)
        
        self.add_button = ctk.CTkButton(self.bottom_frame, text="+", width=60, height=60,
                                      corner_radius=30, font=("Arial", 24))
        self.add_button.pack(side="right")
        """ self.add_button = ctk.CTkButton(self.bottom_frame, text="Salir", width=60, height=60,
                                      corner_radius=30, font=("Arial", 24), fg_color="#ff4444",
                                        command=lambda: cerrar(self))
        self.add_button.pack(side="right") """
        
         #Botón para salir
        self.exit_button = ctk.CTkButton(
            self.bottom_frame, 
            text="Salir", 
            width=60, 
            height=60,
            corner_radius=30, 
            font=("Arial", 24), 
            fg_color="#ff4444",
            command=self.cerrar  # Directamente llama al método cerrar
        )
        self.exit_button.pack(side="right")

        # Icono de alarma
        try:
            self.alarm_icon = ctk.CTkImage(light_image=Image.new('RGBA', (30, 30), (0,0,0,0)), 
                                         dark_image=Image.new('RGBA', (30, 30), (0,0,0,0)),
                                         size=(24, 24))
            self.icon_label = ctk.CTkLabel(self.bottom_frame, image=self.alarm_icon, text="⏰", 
                                         font=("Arial", 24), compound="left")
            self.icon_label.pack(side="left")
        except:
            self.icon_label = ctk.CTkLabel(self.bottom_frame, text="⏰", font=("Arial", 24))
            self.icon_label.pack(side="left")
    
    def refresh_alarms_list(self, alarms, on_edit, on_toggle, on_delete):
        for widget in self.alarms_frame.winfo_children():
            widget.destroy()
            
        if not alarms:
            empty_label = ctk.CTkLabel(self.alarms_frame, text="No hay alarmas programadas\nPresiona + para agregar una",
                                     font=("Arial", 14), text_color="gray")
            empty_label.pack(pady=40)
            return
            
        for alarm in alarms:
            alarm_id, hour, minute, active, label, repeat, snooze = alarm
            self.create_alarm_widget(alarm_id, hour, minute, active, label, repeat, snooze, 
                                   on_edit, on_toggle, on_delete)
    
    def create_alarm_widget(self, alarm_id, hour, minute, active, label, repeat, snooze, 
                          on_edit, on_toggle, on_delete):
        alarm_time = f"{hour:02d}:{minute:02d}"
        alarm_text = f"{alarm_time}  {label}" if label else alarm_time
        snooze_text = " (Snooze)" if snooze else ""
        
        alarm_frame = ctk.CTkFrame(self.alarms_frame, corner_radius=10)
        alarm_frame.pack(fill="x", pady=5, padx=5)
        
        fg_color = "#2a2a2a" if snooze else "transparent"
        text_color = "#aaaaaa" if snooze else None
        
        # Contenedor de texto
        text_frame = ctk.CTkFrame(alarm_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(text_frame, text=alarm_text + snooze_text, 
                    font=("Arial", 20), text_color=text_color).pack(anchor="w")
        
        # Etiqueta de días repetidos
        if repeat != '0000000':
            days_text = self.get_days_text(repeat)
            ctk.CTkLabel(text_frame, text=days_text, 
                         font=("Arial", 12), text_color="#4fc3f7").pack(anchor="w")
        
        # Botones de acción
        action_frame = ctk.CTkFrame(alarm_frame, fg_color="transparent")
        action_frame.pack(side="right", padx=5)
        
        # Botón de editar
        edit_btn = ctk.CTkButton(action_frame, text="✎", width=30, height=30,
                               corner_radius=15, fg_color="#ff9800",
                               command=lambda id=alarm_id: on_edit(id))
        edit_btn.grid(row=0, column=0, padx=2)
        
        # Switch de activación
        switch = ctk.CTkSwitch(action_frame, text="", width=40,
                             command=lambda id=alarm_id: on_toggle(id))
        switch.grid(row=0, column=1, padx=2)
        switch.select() if active else switch.deselect()
        
        # Botón de eliminar
        delete_btn = ctk.CTkButton(action_frame, text="✕", width=30, height=30,
                                 corner_radius=15, fg_color="#ff4444",
                                 command=lambda id=alarm_id: on_delete(id))
        delete_btn.grid(row=0, column=2, padx=2)
    
    def get_days_text(self, repeat_pattern):
        days_of_week = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        days = []
        for i, day in enumerate(repeat_pattern):
            if day == '1':
                days.append(days_of_week[i])
        return ', '.join(days)
    
    def update_time_display(self, time_str):
        self.current_time.set(time_str)
    
    def cerrar(self):
        """Cierra la ventana principal"""
        self.destroy()
    