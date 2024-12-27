import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import cv2
from threading import Thread

# Placeholder for video playback function
def play_video(video_label):
    cap = cv2.VideoCapture('videosample.mp4')  # Replace with your video path

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to an image compatible with Tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (400, 300))
        img = tk.PhotoImage(data=cv2.imencode('.ppm', frame)[1].tobytes())
        video_label.configure(image=img)
        video_label.image = img

        # Pause for a short time to simulate video frame rate
        video_label.update()
        cv2.waitKey(33)  # Approximately 30 FPS

    cap.release()

def start_video_thread(video_label):
    video_thread = Thread(target=play_video, args=(video_label,))
    video_thread.daemon = True
    video_thread.start()

def create_gui():
    root = tk.Tk()
    root.title("Monitoring Kondisi Valsalva Maneuver dan Detak Jantung pada Gerakan Deadlift")

    # Define frame layout
    frame_top_left = tk.Frame(root, width=200, height=150, bg="lightgray")
    frame_top_right = tk.Frame(root, width=200, height=150, bg="lightblue")
    frame_bottom_left = tk.Frame(root, width=400, height=300, bg="white")
    frame_bottom_right = tk.Frame(root, width=400, height=300, bg="white")

    frame_top_left.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    frame_top_right.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    frame_bottom_left.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    frame_bottom_right.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    # Top Left Frame with subframes
    frame_instructions = tk.Frame(frame_top_left, bg="lightgray")
    frame_buttons = tk.Frame(frame_top_left, bg="lightgray")

    frame_instructions.pack(side="left", expand=True, fill="both", padx=5, pady=5)
    frame_buttons.pack(side="right", expand=False, padx=5, pady=5)

    # Instructions
    instructions = (
        "1. Klik tombol MULAI\n"
        "2. Lakukan deadlift sesuai video instruksi\n"
        "3. Tunggu hingga instruksi selesai\n"
        "4. Hasil monitoring dapat dilihat\n"
        "5. Klik tombol SELESAI untuk keluar"
    )
    tk.Label(frame_instructions, text=instructions, font=("Arial", 10), justify="left", bg="lightgray")\
        .pack(pady=10, padx=10)

    # Buttons
    tk.Button(frame_buttons, text="MULAI", command=lambda: start_video_thread(video_label))\
        .pack(pady=5, padx=5)
    tk.Button(frame_buttons, text="SELESAI", command=root.quit).pack(pady=5, padx=5)

    # Bottom Left Frame (Video Display)
    video_label = tk.Label(frame_bottom_left, bg="black")
    video_label.pack(expand=True, fill="both")

    # Top Right Frame
    tk.Button(frame_top_right, text="Good Lift", bg="green", fg="white", command=lambda: messagebox.showinfo("Action", "Good Lift clicked"))\
        .pack(pady=10, padx=10)
    tk.Button(frame_top_right, text="Train Again", bg="red", fg="white", command=lambda: messagebox.showinfo("Action", "Train Again clicked"))\
        .pack(pady=10, padx=10)

    # Bottom Right Frame (Graph Display)
    graph_data = np.array([-1.3285, -1.12486, -1.101587, -0.8514, -0.327754, 0.23662, 0.533352,
                           0.667173, 0.620627, 0.515897, 0.486806, 0.725356, 1.185001, 1.417732,
                           1.505006, 1.557371, 1.580644, 1.609736, 1.62719, 1.603917, 1.598099,
                           1.615554, 1.592281, 1.580644, 1.563189, 1.534098, 1.574826, 1.569008,
                           1.539916, 1.534098, 1.499188, 1.45846, 1.45846, 1.42355, 1.377004,
                           1.400277, 1.394459, 1.353731, 1.330458, 1.185001, 1.05118, 0.952269,
                           0.969724, 0.923178, 0.88245, 0.841722, 0.806812, 0.789357, 0.783539,
                           0.766084, 0.760266, 0.806812, 0.806812, 0.859176, 0.84754, 0.84754,
                           0.853358, 0.876631, 0.876631, 0.859176, 0.853358, 0.841722, 0.830085,
                           0.841722, 0.84754, 0.870813, 0.888268, 0.876631, 0.899904, 0.894086,
                           0.841722, 0.84754, 0.818448, 0.800994, 0.667173, 0.690446, 0.719537,
                           0.783539, 0.818448, 0.81263, 0.789357, 0.77772, 0.81263, 0.84754,
                           0.835903, 0.992997, 0.952269, 0.923178, 0.917359, 1.033725, 1.033725,
                           1.027907, 1.022088, 1.01627, 0.958087, 0.917359, 0.934814, -0.060113,
                           -0.618669, -0.92122])

    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.plot(graph_data)
    ax.set_title("Graph")
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")

    canvas = FigureCanvasTkAgg(fig, master=frame_bottom_right)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill="both")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
