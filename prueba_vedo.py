from vedo import Volume, show, Text2D

scan = Volume("NIfTI/Brats18_2013_11_1_t1ce.nii.gz")
tumor_mask = Volume("NIfTI/prueba01.nii.gz")


tumor_parte_activa=Volume()
tumor_nucleo=Volume()
tumor_edema=Volume()

scan.cmap("bone").alpha([0.0, 0.05, 0.3, 0.8])

tumor_mesh = tumor_mask.isosurface(value=0.5).color("red").alpha(1.0)

txt_cer = Text2D("Presiona 'b' para ocultar el Cerebro", pos="top-left", s=1.0, c="white")
txt_pac = Text2D("Presiona '1' para ocultar el Nucleo", pos="top-left", s=1.0, c="white")
txt_nuc = Text2D("Presiona '1' para ocultar el Nucleo", pos="top-left", s=1.0, c="white")
txt_ede = Text2D("Presiona '2' para ocultar el Edema", pos="top-left", s=1.0, c="white")


cerebro_visible = True #Todo el cerebro
 
parte_activa = True #La parte activa 

nucleo_visible = True #Nucleo del tumro (Parte activa y necrosis)

edema_visible = True #Edema

def al_presionar_tecla(event):
    global cerebro_visible
    global nucleo_visible
    global edema_visible

    #CEREBRO
    if event.keypress == "b":
        if cerebro_visible:
            scan.alpha(0.0) 
            cerebro_visible = False
            txt_cer.text("Cerebro: OCULTO (Presiona 'b' para mostrar)")
        else:
            scan.alpha([0.0, 0.05, 0.3, 0.8])
            cerebro_visible = True
            txt_cer.text("Cerebro: VISIBLE (Presiona 'b' para ocultar)")
        plt.render()

    #PARTE ACTIVA
    elif event.keypress == "1":
        if parte_activa:
            scan.alpha(0.0) 
            parte_activa = False
            txt_pac.text("Parte activa: OCULTO (Presiona '1' para mostrar)")
        else:
            scan.alpha([0.0, 0.05, 0.3, 0.8])
            parte_activa = True
            txt_pac.text("Parte activa: VISIBLE (Presiona '1' para ocultar)")
        plt.render()


    #NUCLEO
    elif event.keypress == "2":
        if nucleo_visible:
            scan.alpha(0.0) 
            nucleo_visible = False
            txt_nuc.text("Nucleo: OCULTO (Presiona '1' para mostrar)")
        else:
            scan.alpha([0.0, 0.05, 0.3, 0.8])
            nucleo_visible = True
            txt_nuc.text("Nucleo: VISIBLE (Presiona '1' para ocultar)")
        plt.render()
    
    #EDEMA
    elif event.keypress == "3":
        if edema_visible:
            scan.alpha(0.0) 
            edema_visible = False
            txt_ede.text("Edema: OCULTO (Presiona '1' para mostrar)")
        else:
            scan.alpha([0.0, 0.05, 0.3, 0.8])
            edema_visible = True
            txt_ede.text("Edema: VISIBLE (Presiona '1' para ocultar)")
        plt.render()
    




plt = show(scan, tumor_mesh, txt_cer, bg="black", axes=1, interactive=False)
plt = show(scan, tumor_mesh, txt_pac, bg="black", axes=0, interactive=False)
plt = show(scan, tumor_mesh, txt_nuc, bg="black", axes=0, interactive=False)
plt = show(scan, tumor_mesh, txt_ede, bg="black", axes=0, interactive=False)

plt.add_callback("key press", al_presionar_tecla)
plt.interactive().close()
