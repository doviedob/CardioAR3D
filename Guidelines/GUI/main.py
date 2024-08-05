import tkinter as tk
from tkinter import scrolledtext, messagebox, font, filedialog
from PIL import Image, ImageTk, ImageFilter
import paramiko
import threading

class SSHClient:
    def __init__(self, hostname, username, key_filename):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname, username=username, key_filename=key_filename)
            self.channel = self.client.invoke_shell()
        except Exception as e:
            raise e

    def send_command(self, command):
        self.channel.send(command + '\n')

    def receive_output(self):
        output = ''
        while self.channel.recv_ready():
            output += self.channel.recv(1024).decode('utf-8')
        return output

    def close(self):
        self.client.close()

class CommandExecutor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SSH Connect - MONAI Label Start")
        self.configure(bg='#f0f0f0')  # Light gray background for the main window

        # Configure a custom font
        custom_font = font.Font(family="Helvetica", size=10)
        
        # Common style for widgets
        common_style = {'font': custom_font, 'bg': '#f0f0f0'}
        entry_style = {'font': custom_font, 'bg': 'white', 'relief': 'flat', 'bd': 1}
        button_style = {'font': custom_font, 'bg': '#4CAF50', 'fg': 'white', 'relief': 'flat', 'bd': 0}

        # Main frame
        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(pady=20, padx=20)

        # Frame for IPv4 input and PEM file selection
        ip_pem_frame = tk.Frame(main_frame, bg='#f0f0f0')
        ip_pem_frame.grid(row=0, column=1, pady=10, sticky='n')

        self.ip_label = tk.Label(ip_pem_frame, text="Public IPv4:", **common_style)
        self.ip_label.pack(pady=5)
        
        self.ip_entry = tk.Entry(ip_pem_frame, width=30, **entry_style)
        self.ip_entry.pack(pady=5)
        self.ip_entry.bind("<KeyRelease>", self.check_entries)

        self.pem_file_button = tk.Button(ip_pem_frame, text="Select PEM File", command=self.select_pem_file, **button_style)
        self.pem_file_button.pack(pady=5)

        self.pem_file_path = ""

        # Frame for buttons
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.grid(row=0, column=2, padx=20, sticky='ne')

        self.connect_button = tk.Button(buttons_frame, text="1. Connect", command=self.connect_to_server, **button_style)
        self.connect_button.pack(pady=5)
        self.connect_button.config(state=tk.DISABLED)

        self.command_button = tk.Button(buttons_frame, text="2. Activate Environment", command=self.activate_environment, **button_style)
        self.command_button.pack(pady=5)
        self.command_button.config(state=tk.DISABLED)

        self.server_button = tk.Button(buttons_frame, text="3. Start Server", command=self.start_server, **button_style)
        self.server_button.pack(pady=5)
        self.server_button.config(state=tk.DISABLED)

        # Space for logo
        logo_frame = tk.Frame(main_frame, bg='#f0f0f0', width=200, height=200)
        logo_frame.grid(row=0, column=0, padx=20, sticky='nw')

        self.output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=100, height=20, bg='white')
        self.output_text.grid(row=1, column=0, columnspan=3, pady=10)

        self.ssh_client = None

        self.update_output()

    def select_pem_file(self):
        # Open a file dialog to select the PEM file
        self.pem_file_path = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
        self.output_text.insert(tk.END, f"Selected PEM file: {self.pem_file_path}\n")
        self.check_entries()

    def check_entries(self, event=None):
        # Enable the connect button if both IP and PEM file are provided
        if self.ip_entry.get() and self.pem_file_path:
            self.connect_button.config(state=tk.NORMAL)
        else:
            self.connect_button.config(state=tk.DISABLED)

    def connect_to_server(self):
        # Establish SSH connection to the server
        ip_publica = self.ip_entry.get()
        hostname = f"ec2-{ip_publica.replace('.', '-')}.compute-1.amazonaws.com"

        def connect():
            try:
                self.ssh_client = SSHClient(hostname, "ubuntu", self.pem_file_path) #Considered your EC2 Instances. The linux instances use 'ubuntu' for username
                self.output_text.insert(tk.END, f"Connected to server: {hostname}\n")
                self.command_button.config(state=tk.NORMAL, bg="lightgreen")
                self.server_button.config(state=tk.NORMAL)
                self.connect_button.config(bg="SystemButtonFace")
            except Exception as e:
                self.output_text.insert(tk.END, f"Failed to connect: {e}\n")
                messagebox.showerror("Connection Error", f"Failed to connect: {e}")

        thread = threading.Thread(target=connect)
        thread.start()

    def activate_environment(self):
        # Activate the conda environment on the server
        if self.ssh_client:
            self.ssh_client.send_command('conda activate monailabel-env')
            self.output_text.insert(tk.END, "Sent: conda activate monailabel-env\n")
            self.output_text.see(tk.END)
            self.command_button.config(bg="SystemButtonFace")
            self.server_button.config(bg="lightgreen")

    def start_server(self):
        # Start the MONAI Label server
        if self.ssh_client:
            # Note: Modify this command to select your datasets and model name
            command = 'monailabel start_server --app apps/radiology --studies datasets/Task02_Heart/imagesTr --conf models segmentation_heart'
            self.ssh_client.send_command(command)
            self.output_text.insert(tk.END, f"Sent: {command}\n")
            self.output_text.see(tk.END)
            self.server_button.config(bg="SystemButtonFace")

    def update_output(self):
        # Update the output text widget with server responses
        if self.ssh_client:
            output = self.ssh_client.receive_output()
            if output:
                self.output_text.insert(tk.END, output)
                self.output_text.see(tk.END)
        self.after(1000, self.update_output)

if __name__ == "__main__":
    app = CommandExecutor()
    app.mainloop()






















