import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os
from datetime import datetime
from export_log import log
import logging
import pyscreenshot as ImageGrab
from pypylon import pylon
from functools import partial
import time as tm

folder_path = '/media/archiv/sber_fotek/'

def akce():
    screenshot_button.config(text="Cekam")
    root.after(500, take_screenshot)

#--------------------------------------------------------------------------
# Funkce pro sběr fotek
#--------------------------------------------------------------------------
def take_screenshot():   
    # Ask the user for the directory to save the screenshot
    #folder_path = filedialog.askdirectory()
    
    
    #curr_date = datetime.now()
    #current_date = curr_date.strftime('%Y_%m_%d')

    #folder = os.path.join(folder_path, current_date)

    #if not os.path.exists(folder):
    #    os.makedirs(folder)

    curr_time = datetime.now()
    current_time = curr_time.strftime('%Y_%m_%d__%H_%M_%S_%f')

    path_list = []
    ok = False

    for ser in sern_list:
        path_list.append(foto_z_kamery(ser, current_time))

    '''
    path_list.append(foto_z_kamery(24548200,current_time))
    path_list.append(foto_z_kamery(24548195,current_time))
    '''

    for path in path_list:
        if os.path.exists(path):
            ok = True
        else:
            ok = False

    if ok == True:
        root.configure(background='green')
    else:
        root.configure(background='red')

    root.after(2000, partial(update, '#d9d9d9'))
    #root.after(2000, partial(update, '#F0E68C'))
    #root.after(2000, update)

    screenshot_button.config(text="Vyfotit vadu")

#--------------------------------------------------------------------------
# Funkce pro foto z kamery
#--------------------------------------------------------------------------
def foto_z_kamery(camera_index,time):
    tl_factory = pylon.TlFactory.GetInstance()
    devices = tl_factory.EnumerateDevices()

    '''
    for device in devices:
        print(f"Camera Serial Number: {device.GetSerialNumber()}")
    '''
    vstup_serial_number = str(camera_index)
    cesta_foto_ulozeni = folder_path + vstup_serial_number +"/"+time +".jpg"
    camera = None

    #for device in devices:
    #    serial_number = device.GetSerialNumber()

     #   if serial_number == vstup_serial_number:

    
   # watch = stopwatch()
   # next(watch) 
    try:
        device_info = pylon.DeviceInfo()
        #device_info.SetSerialNumber(serial_number)
        device_info.SetSerialNumber(camera_index)


        tl_factory = pylon.TlFactory.GetInstance()

        camera_device = tl_factory.CreateDevice(device_info)

        camera = pylon.InstantCamera(camera_device)
        

    except Exception as ex:
        print(f"chyba: {ex}")  
    #    break     

   # next(watch)

    if camera is not None:
        camera.Open()
        print(f"Kamera se seriovým číslem {vstup_serial_number} otevrena.")
    else:
        print(f"Kamera nenalezena: {vstup_serial_number}.")

   # watch2 = stopwatch()
   # next(watch2) 
    camera.StartGrabbingMax(1)




    #grab_result = camera.GrabOne(4000)
    #grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    converter = pylon.ImageFormatConverter()
    #converter.OutputPixelFormat = pylon.PixelType_RGB8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    #if grab_result.GrabSucceded():
    #    img = grab_result.Array
    grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    
   # next(watch2) 
    if grab_result.GrabSucceeded():
        image = converter.Convert(grab_result)
        img_array = image.GetArray()

        img = Image.fromarray(img_array)
    
        img.save(cesta_foto_ulozeni)
       


    #img_pil.save("/home/ubuntu/prog/take_images/foto/{time}.jpg")    
    #img_pil.save(cesta_foto_ulozeni,format ='JPEG',quality=85)

    grab_result.Release()
    camera.StopGrabbing()
    camera.Close()

    return cesta_foto_ulozeni

def stopwatch():
    start_time = tm.time()
    yield
    elapsed_time = tm.time() - start_time
    print(f"Čas:{elapsed_time:.3f} sekund  ")

def update(color):
    root.configure(background=color)
    #root.configure(background='#d9d9d9')
#--------------------------------------------------------------------------
# Keyhandler pro snimání zmáčknutých kláves
#--------------------------------------------------------------------------
def key_handler(event): 
    # Allow only space key and Ctrl+F10 
    print(event.keysym)

    if event.keysym == 'space':
        #take_screenshot()
        akce()
        return 
    elif event.keysym == 'F12':
        root.quit()
    else: 
        return "break"
#--------------------------------------------------------------------------
# Hlavní běh programu
#--------------------------------------------------------------------------
if __name__ == "__main__":

    log_file_name = 'take_images'
    log_target_directory = os.path.join('/home/ubuntu/prog/take_images', 'log')

    logger_full_file_name = log.create_log_file(log_file_name, log_target_directory, 10)

    logger = logging.getLogger(log_file_name)
    logging.basicConfig(filename=logger_full_file_name, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')
    try:
        os.chmod(logger_full_file_name, 0o775)
    except Exception as error:
        print(error)
        pass

    tl_factory = pylon.TlFactory.GetInstance()
    devices = tl_factory.EnumerateDevices()

    for device in devices:
        print(device.GetSerialNumber())

    logger.debug('Start')
    # Create the main window
    try:

        sern_list = []
        for device in devices:
            sern_list.append(device.GetSerialNumber())

        root = tk.Tk()
        root.title("Vyfotit vadu")

        # Remove window decorations 
        root.wm_attributes('-type', 'splash')

        # Get the screen width and height 
        #screen_width = root.winfo_screenwidth()      
        #screen_height = root.winfo_screenheight() 

        screen_width = 300      
        screen_height = 100

        # Set the window geometry to full size 
        root.geometry(f"{screen_width}x{screen_height}")

        # Force focus on the window to ensure it receives key events 
        root.focus_force()   

        # Bind key events to the handler 
        root.bind_all('<KeyPress>', key_handler)

        # Create a button
        #screenshot_button = tk.Button(root, text="Vyfotit vadu", command=take_screenshot, font=("Arial", 24))
        screenshot_button = tk.Button(root, text="Vyfotit vadu", command=akce, font=("Arial", 24))
        screenshot_button.pack(expand=True)

        #defaultbg = root.cget('bg')

        # Run the application
        root.mainloop()
    except Exception as error:
        logger.debug(error)
#--------------------------------------------------------------------------
