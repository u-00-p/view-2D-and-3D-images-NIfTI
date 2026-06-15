from vedo import Volume, show, Text2D

# 1. Cargar el escaneo y la máscara del tumor
scan = Volume("NIfTI/Brats18_CBICA_AXJ_1_t1.nii.gz")
tumor_mask = Volume("NIfTI/Brats18_CBICA_AXJ_1_seg.nii.gz")

# 2. Configurar el cerebro para que el fondo sea transparente
scan.cmap("bone").alpha([0.0, 0.05, 0.3, 0.8])

# 3. Extraer el tumor en 3D (suavizado)
tumor_mesh = tumor_mask.isosurface(value=0.5).color("red").alpha(1.0)

# 4. Crear el texto informativo fijado en la esquina superior izquierda
# SE CORRIGE: pos="top-left" en lugar de pos=1 para evitar el TypeError
txt = Text2D("Cerebro: VISIBLE (Presiona 'b' para ocultar)", pos="top-left", s=1.0, c="white")

# Variable global para rastrear el estado de visibilidad del cerebro
cerebro_visible = True

# 5. Lógica de interacción (Función Callback)
def al_presionar_tecla(event):
    global cerebro_visible
    
    # Si el usuario presiona la tecla 'b' (de Brain)
    if event.keypress == "b":
        if cerebro_visible:
            # Ocultar el cerebro bajando su opacidad a cero
            scan.alpha(0.0) 
            cerebro_visible = False
            txt.text("Cerebro: OCULTO (Presiona 'b' para mostrar)")
        else:
            # Restaurar la opacidad original del escaneo
            scan.alpha([0.0, 0.05, 0.3, 0.8])
            cerebro_visible = True
            txt.text("Cerebro: VISIBLE (Presiona 'b' para ocultar)")
            
        # Forzar a Vedo a redibujar los cambios en la ventana activa
        plt.render()

# 6. Inicializar la ventana pasando el volumen, el tumor y la etiqueta de texto
# Cambiamos bg="black" para resaltar el tumor rojo y la escala de grises del cerebro
plt = show(scan, tumor_mesh, txt, bg="black", axes=1, interactive=False)

# Conectar el teclado con nuestra función lógica
plt.add_callback("key press", al_presionar_tecla)

# Iniciar la interactividad manual en la terminal
plt.interactive().close()
