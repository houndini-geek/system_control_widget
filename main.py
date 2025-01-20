from tkinter import Tk, Button, Canvas, Frame, Scrollbar, messagebox, Menu

import os
import platform
import webbrowser
import re
import psutil
import socket
from datetime import datetime, timedelta

import ctypes
import sys
sc_widget_folder = "SystemControlWidget"
widget_folder = None
#auto_start_path = 'C:\Users\Houndini\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
system_info_file = 'system_info'



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    #Re-run the script as admin
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1
    )
    sys.exit()



def create_sc_widget_dir():
    global widget_folder
    widget_folder = os.path.join(os.path.expanduser('~'),'AppData','Local',f'{sc_widget_folder}')
    if not os.path.exists(widget_folder):
        os.mkdir(widget_folder)
        print("System Control Widget  folder created!")



def set_drives_count():
  drives = ''
  for drive in os.listdrives():
    formated = drive.replace('\\','/')
    drives += formated + '|'
  return drives
    

# Helper functions
def set_drives_count():
    return len([drive for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{drive}:\\")])

def get_uptime():
    uptime_seconds = (datetime.now() - datetime.fromtimestamp(psutil.boot_time())).total_seconds()
    return str(timedelta(seconds=uptime_seconds)).split('.')[0]

def get_disk_info():
    disk = psutil.disk_usage('/')
    return f"Total: {disk.total / (1024 ** 3):.2f} GB, Used: {disk.used / (1024 ** 3):.2f} GB, Free: {disk.free / (1024 ** 3):.2f} GB ({disk.percent}%)"

def get_memory_info():
    memory = psutil.virtual_memory()
    return f"Total: {memory.total / (1024 ** 3):.2f} GB, Used: {memory.used / (1024 ** 3):.2f} GB ({memory.percent}%)"

def get_network_info():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return f"Hostname: {hostname}, IP: {ip}"


def get_uptime():
    uptime_seconds = (datetime.now() - datetime.fromtimestamp(psutil.boot_time())).total_seconds()
    return str(timedelta(seconds=uptime_seconds)).split('.')[0]

def get_disk_info():
    disk = psutil.disk_usage('/')
    return f"Total: {disk.total / (1024 ** 3):.2f} GB, Used: {disk.used / (1024 ** 3):.2f} GB, Free: {disk.free / (1024 ** 3):.2f} GB ({disk.percent}%)"

def get_memory_info():
    memory = psutil.virtual_memory()
    return f"Total: {memory.total / (1024 ** 3):.2f} GB, Used: {memory.used / (1024 ** 3):.2f} GB ({memory.percent}%)"

def get_network_info():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return f"Hostname: {hostname}, IP: {ip}"

def get_gpu_info():
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        gpu_details = [
            f"{gpu.name} ({gpu.memoryTotal:.2f} MB)" for gpu in gpus
        ]
        return ", ".join(gpu_details) if gpu_details else "No GPU detected."
    except ImportError:
        return "GPUtil not installed."

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        plugged = "Plugged in" if battery.power_plugged else "Not plugged in"
        time_left = str(timedelta(seconds=battery.secsleft)).split('.')[0] if not battery.power_plugged else "N/A"
        return f"Percentage: {battery.percent}%, {plugged}, Time left: {time_left}"
    return "No battery info available."

def get_boot_time():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    return boot_time.strftime("%Y-%m-%d %H:%M:%S")

def get_python_info():
    return f"Python {platform.python_version()} ({platform.python_implementation()})"



# Main function
def show_system_info():
    create_sc_widget_dir()
    my_system = platform.uname()
    system_info = {
        "Username": os.getlogin(),
        "CPU Count": os.cpu_count(),
        "Drives Count": set_drives_count(),
        "Processor": my_system.processor,
        "System": my_system.system,
        "Release": my_system.release,
        "Version": my_system.version,
        "Uptime": get_uptime(),
        "Memory": get_memory_info(),
        "Disk Usage": get_disk_info(),
        "Network": get_network_info(),
        "GPU": get_gpu_info(),
        "Battery": get_battery_info(),
        "Boot Time": get_boot_time(),
        "Python Info": get_python_info(),
    }

    
    # Widget folder setup
    
    # Writing CSS
    css_content = """
   *,::before,::after{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {

    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif ;
}
body{

    width:100%;
    height: 100%;
    padding: 3em;
    background-color: #F5F5F5;
}
header {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.7em;
}
header h1 {
    font-size: 2rem;
    font-weight: 800;
}

header button {
    background-color: #272727;
    color: #f3f3f3;
    padding: 0.5em 0.7em;
    font-weight: 500;
    border: none;
    border-radius: 0.3em;
    cursor: pointer;
    text-transform: capitalize;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif ;
}
.container{

    width: 50rem;
    padding: 1em;
    margin: 0 auto 0;
}

ul li{

    list-style:none;
    line-height: 30px;
    font-size: 1.1em;
    font-weight: 400;
    text-align: left;
}

ul li span {

    text-decoration: underline;
    padding-left: 0.7em;
    font-weight: 500;
    float: right;
    
}

    """
    with open(f"{widget_folder}/style.css", "w") as css_file:
        css_file.write(css_content)
    
    # Writing HTML
    with open(f"{widget_folder}/{system_info_file}.html", 'w') as html_file:
        html_file.write(f"""
         <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="style.css">
            <title>System Control Widget | System Info</title>
        </head>
        <body>
            <header>
                <h1>System Info</h1>
                <button id="print-btn">Print</button>
            </header>
            <div class="container">
                <ul>
        """)
        for key, value in system_info.items():
            html_file.write(f"<li>{key}: <span>{value}</span></li>")
        
        html_file.write("""
                </ul>
            </div>
            <script>
                document.getElementById('print-btn').addEventListener('click', () => {
                    window.print();
                });
            </script>
        </body>
        </html>
        """)
    
    # Open in browser
    webbrowser.open_new_tab(f"{widget_folder}/{system_info_file}.html")




# Define button functions
def shutdown():
    messagebox.showinfo("Notification", "Shutting down your system... Goodbye! 👋")
    os.system("shutdown /s /t 0")


def restart():
    messagebox.showinfo("Notification", "Restarting your system... Hang tight! 🔄")
    os.system("shutdown /r /t 0")

def logout():
    messagebox.showinfo("Notification", "Logging you out... See you soon! ✌️")
    os.system("shutdown -l")

def hibernate():
    messagebox.showinfo("Notification", "Hibernating... Zzz! 😴")
    os.system("shutdown /h")

def sleep():
    messagebox.showinfo("Notification", "Putting your system to sleep... 💤")
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def recovery_mode():
    answer = messagebox.askyesno(
        "Confirmation",
        "You're about to restart into recovery mode 🔧.\n\nDo you want to continue?"
    )
    if answer:
        messagebox.showinfo(
            "Notification", 
            "Restarting to recovery mode... 🔄\nGet ready to troubleshoot! 💪"
        )
        os.system("shutdown /r /o /t 0")
    else:
        messagebox.showinfo("Notification", "Action canceled! No worries. 😊")


def disable_wifi():
    try:
        # Fetch the name of the Wi-Fi adapter
        wifi_name = os.popen('netsh wlan show interfaces | findstr "Name"').read().strip().split(":")[-1].strip()
        if wifi_name:
            messagebox.showinfo("Notification", f"Disabling WiFi ({wifi_name})... 🔒")
            os.system(f'netsh interface set interface name="{wifi_name}" admin=disable')
        else:
            messagebox.showerror("Error", "No WiFi adapter found! 😕")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to disable WiFi: {e}")


def enable_wifi():
    try:
        # Fetch all network adapter names
        adapters_output = os.popen('netsh wlan show interfaces').read()
        matches = re.findall(r"Name\s*:\s*(.+)", adapters_output)
        
        if matches:
            # Assuming the first adapter is the Wi-Fi card
            wifi_name = matches[0].strip()
            messagebox.showinfo("Notification", f"Enabling WiFi... ({wifi_name}) 📶")
            os.system(f'netsh interface set interface name="{wifi_name}" admin=enable')
        else:
            messagebox.showerror("Error", "No Wi-Fi adapter found! 😕")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to enable Wi-Fi: {e}")

def flush_dns():
    messagebox.showinfo("Notification", "Flushing DNS... 🔄")
    os.system("ipconfig /flushdns")

def tsk_mngr():
    messagebox.showinfo("Notification", "Opening Task Manager... ⚙️")
    os.system("taskmgr")

def device_mngr():
    messagebox.showinfo("Notification", "Opening Device Manager... 🔧")
    os.system("devmgmt.msc")

def disk_cleanup():
    messagebox.showinfo("Notification", "Opening Disk Cleanup... 🧹")
    os.system("cleanmgr")

def clear_temp_files():
    messagebox.showinfo("Notification", "Clearing Temp Files... 🗑️")
    os.system("del /q /f /s %TEMP%\\*")

def open_disk_mgmt():
    messagebox.showinfo("Notification", "Openning Disk management...")
    os.system("diskmgmt")

# Create the main window
window = Tk()
window.title("System Control Widget")
window.config(padx=4,pady=4)
window.geometry('430x200')  # Slightly increased for better UI


# Setup Menu
menu_bar = Menu(window, font=("Helvetica", 10))
system_menu = Menu(menu_bar, tearoff=0 ,font=("Helvetica", 10))
system_menu.add_command(label="View system info",command=show_system_info)
system_menu.add_command(label="Set timeout for system shutdown (default 0s)")
system_menu.add_command(label="Set timeout for system restart (default 0s)")
system_menu.add_separator()
system_menu.add_command(label='Exit', command=lambda:exit())

menu_bar.add_cascade(label="System", menu=system_menu)

# Create a canvas for scrolling
canvas = Canvas(window, bg="#E6E6E6")
canvas.pack(side="left", fill="both", expand=True)

# Add a vertical scrollbar to the canvas
scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame inside the canvas
frame = Frame(canvas, bg="#E6E6E6")
canvas.create_window((0, 0), window=frame, anchor="nw")

# Add buttons to the frame
buttons = [
    ("Shutdown 🔻", shutdown),
    ("Restart 🔄", restart),
    ("Log Out ✌️", logout),
    ("Hibernate 😴", hibernate),
    ("Sleep 💤", sleep),
    ("Recovery Mode 🔧", recovery_mode),
    ("Disable WiFi 📴", disable_wifi),
    ("Enable WiFi 📶", enable_wifi),
    ("Flush DNS 🔄", flush_dns),
    ("Task Manager ⚙️", tsk_mngr),
    ("Device Manager 🔧", device_mngr),
    ("Disk Cleanup 🧹", disk_cleanup),
    ("Clear Temp Files 🗑️", clear_temp_files),
   ("Open Disk Management 💽", open_disk_mgmt)
]

# Style configuration for buttons
button_style = {
    "bg": "#6200ee",
    "fg": "white",
    "activebackground": "#A46BF5",
    "activeforeground": "white",
    "font": ("Helvetica", 12, "bold"),
    "width": 40,
    "height": 2,
    "cursor": "hand2",
    "relief": "raised"
}

#Dynamically create buttons in a loop
for idx, (text, command) in enumerate(buttons):
    Button(frame, text=text, command=command, **button_style).grid(row=idx, column=0, pady=8, padx=10)



window.config(menu=menu_bar)
# Prevent resizing
window.resizable(False, False)
window.mainloop()
