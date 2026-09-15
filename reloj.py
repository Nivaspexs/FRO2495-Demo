import tkinter as tk
import time

def actualizar_reloj():
    # Obtiene la hora actual con milisegundos exactos
    tiempo_actual = time.strftime('%H:%M:%S')
    milisegundos = int((time.time() % 1) * 1000)
    
    # Formatea el texto (Ej: 14:30:15.452)
    texto_reloj = f"{tiempo_actual}.{milisegundos:03d}"
    etiqueta.config(text=texto_reloj)
    
    # Se actualiza cada 10 milisegundos para ser preciso
    ventana.after(10, actualizar_reloj)

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Test de Latencia - Ricoh Theta X")
ventana.geometry("700x200")
ventana.configure(bg='black')

# Diseño de los números
etiqueta = tk.Label(ventana, font=('Courier', 80, 'bold'), bg='black', fg='lime')
etiqueta.pack(expand=True)

actualizar_reloj()
ventana.mainloop()

