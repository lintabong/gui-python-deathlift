import tkinter as tk
from tkinter import messagebox, ttk
import serial.tools.list_ports
from threading import Thread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import cv2
import serial

from matplotlib import pyplot as plt
import numpy

from keras.models import load_model

labels = ['VM', 'tanpa VM']

def feature_normalize(dataset):
    mu = numpy.mean(dataset, axis=0)
    sigma = numpy.std(dataset, axis=0)
    return (dataset - mu)/sigma

def play_video(video_label):
    cap = cv2.VideoCapture('videosample.mp4')
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (400, 300))
        img = tk.PhotoImage(data=cv2.imencode('.ppm', frame)[1].tobytes())
        video_label.configure(image=img)
        video_label.image = img

        video_label.update()
        cv2.waitKey(33)
    cap.release()

def start_video_thread(video_label):
    video_thread = Thread(target=play_video, args=(video_label,))
    video_thread.daemon = True
    video_thread.start()

def scan_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def read_serial_data(serial_connection, result_entry, ax, graph_data, canvas):
    model = load_model('model.h5')

    while True:
        if serial_connection.in_waiting:
            try:
                data = serial_connection.readline().decode('utf-8').strip()
                data_list = data.split(",")

                numeric_data = [float(x) for x in data_list[:100] if x.replace('.', '', 1).isdigit()]

                data_to_predict = feature_normalize(numeric_data)

                result = model.predict(numpy.array([data_to_predict]))

                predicted_index = numpy.argmax(result)

                predicted_label = labels[predicted_index]

                result_entry.delete(0, tk.END)
                result_entry.insert(0, predicted_label)

                graph_data[:] = numeric_data
                ax.clear()
                ax.plot(graph_data)
                ax.set_title('Graph')
                ax.set_xlabel('Index')
                ax.set_ylabel('Value')
                ax.grid(True)
                ax.relim()
                ax.autoscale_view()
                canvas.draw()

            except Exception as error:
                print(error)

def show_main_page(root, selected_port, selected_baudrate, frame_width, frame_height):
    if not selected_port or not selected_baudrate:
        messagebox.showerror("Error", "Harap pilih port COM dan baudrate.")
        return

    for widget in root.winfo_children():
        widget.destroy()

    frame_top_left = tk.Frame(root, bg='lightgray')
    frame_top_right = tk.Frame(root, bg='lightblue')
    frame_bottom_left = tk.Frame(root, bg='white')
    frame_bottom_right = tk.Frame(root, bg='white')

    frame_top_left.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    frame_top_right.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
    frame_bottom_left.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
    frame_bottom_right.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    result_label = tk.Label(frame_top_right, text='Hasil:', font=('Arial', 10))
    result_label.pack(pady=5, padx=10)
    result_entry = tk.Entry(frame_top_right, font=('Arial', 10))
    result_entry.pack(pady=5, padx=10, fill='x')

    serial_connection = serial.Serial(selected_port, selected_baudrate, timeout=1)

    graph_data = numpy.zeros(100)
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.plot(graph_data)
    ax.set_title("Graph")
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")

    canvas = FigureCanvasTkAgg(fig, master=frame_bottom_right)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill="both")

    serial_thread = Thread(target=read_serial_data, args=(serial_connection, result_entry, ax, graph_data, canvas))
    serial_thread.daemon = True
    serial_thread.start()

    frame_instructions = tk.Frame(frame_top_left, bg='lightgray')
    frame_buttons = tk.Frame(frame_top_left, bg='lightgray')

    frame_instructions.pack(side='left', expand=True, fill='both', padx=5, pady=5)
    frame_buttons.pack(side='right', expand=False, padx=5, pady=5)

    instructions = (
        '1. Klik tombol MULAI\n'
        '2. Lakukan deadlift sesuai video instruksi\n'
        '3. Tunggu hingga instruksi selesai\n'
        '4. Hasil monitoring dapat dilihat\n'
        '5. Klik tombol SELESAI untuk keluar'
    )
    tk.Label(frame_instructions, text=instructions, font=("Arial", 10), justify='left', bg='lightgray').pack(pady=10, padx=10)

    video_label = tk.Label(frame_bottom_left, bg='black')
    video_label.pack(expand=True, fill='both')

    tk.Button(frame_buttons, text='MULAI', command=lambda: start_video_thread(video_label)).pack(pady=5, padx=5)
    tk.Button(frame_buttons, text='SELESAI', command=root.quit).pack(pady=5, padx=5)
    tk.Button(frame_top_right, text='Good Lift', bg='green', fg='white').pack(pady=10, padx=10)
    tk.Button(frame_top_right, text='Train Again', bg='red', fg='white').pack(pady=10, padx=10)

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

def create_initial_page(root, frame_width, frame_height):
    def update_ports():
        ports = scan_ports()

        port_listbox.delete(0, tk.END)
        for port in ports:
            port_listbox.insert(tk.END, port)

    def connect():
        selected_port_index = port_listbox.curselection()
        if selected_port_index:
            selected_port = port_listbox.get(selected_port_index)

            selected_baudrate = baudrate_combobox.get()
            show_main_page(root, selected_port, selected_baudrate, frame_width, frame_height)
        else:
            messagebox.showerror('Error', 'Harap pilih port COM.')

    tk.Label(root, text='Koneksi ke ESP32', font=('Arial', 14)).pack(pady=10)

    frame_connection = tk.Frame(root)
    frame_connection.pack(pady=10)

    tk.Label(frame_connection, text='Port COM:').grid(row=0, column=0, padx=5, pady=5)

    port_listbox = tk.Listbox(frame_connection, height=5, width=30)
    port_listbox.grid(row=1, column=0, columnspan=2, pady=10)

    tk.Label(frame_connection, text='Baudrate:').grid(row=2, column=0, padx=5, pady=5)
    baudrate_combobox = ttk.Combobox(frame_connection, state='readonly', values=[9600, 115200, 250000])
    baudrate_combobox.grid(row=2, column=1, padx=5, pady=5)
    baudrate_combobox.current(1)

    update_ports_button = tk.Button(frame_connection, text='Scan Port', command=update_ports)
    update_ports_button.grid(row=3, column=0, columnspan=2, pady=10)

    connect_button = tk.Button(root, text='Connect', command=connect)
    connect_button.pack(pady=10)

if __name__ == '__main__':
    window_width = 800
    window_height = 600

    root = tk.Tk()
    root.title('Monitoring ESP32')
    root.geometry(f'{window_width}x{window_height}')
    create_initial_page(root, int(window_width/2), int(window_height/2))
    root.mainloop()
