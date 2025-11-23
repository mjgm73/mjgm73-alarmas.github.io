import tkinter as tk

def centrar_ventana(self, ancho=None, alto=None):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        
        if ancho is None:
            ancho = self.winfo_width()
        if alto is None:
            alto = self.winfo_height()
        
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        
        self.geometry(f'{ancho}x{alto}+{x}+{y}')