import customtkinter as ctk
from views.alarm_view import AlarmView
from controllers.alarm_controller import AlarmController

def main():
    app = AlarmView()
    controller = AlarmController(app)
    
    # Configurar actualización de tiempo
    controller.update_time()
    
    # Configurar cierre
    app.protocol("WM_DELETE_WINDOW", controller.on_closing)
    
    app.mainloop()

if __name__ == "__main__":
    main()