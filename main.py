import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import re
from PIL import Image

class WebpConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WebP Sequence Converter")
        self.geometry("500x700")
        
        self.sequences_map = {} # holds sequence_name -> list of files
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="WebP Sequence Converter", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10))

        # Input Directory
        self.input_label = ctk.CTkLabel(self, text="Input Directory:")
        self.input_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.input_var = ctk.StringVar()
        self.input_entry = ctk.CTkEntry(self, textvariable=self.input_var, state="readonly")
        self.input_entry.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.input_btn = ctk.CTkButton(self, text="Browse", command=self.browse_input, width=80)
        self.input_btn.grid(row=1, column=2, padx=(0, 20), pady=10)

        # Sequence Dropdown
        self.seq_label = ctk.CTkLabel(self, text="Select Sequence:")
        self.seq_label.grid(row=2, column=0, padx=20, pady=10, sticky="e")
        self.seq_var = ctk.StringVar(value="No folder selected")
        self.seq_combo = ctk.CTkComboBox(self, variable=self.seq_var, values=["No folder selected"], state="readonly", command=self.on_sequence_selected)
        self.seq_combo.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="ew")

        # Output File
        self.output_label = ctk.CTkLabel(self, text="Output File (.webp):")
        self.output_label.grid(row=3, column=0, padx=20, pady=10, sticky="e")
        self.output_var = ctk.StringVar()
        self.output_entry = ctk.CTkEntry(self, textvariable=self.output_var, state="readonly")
        self.output_entry.grid(row=3, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.output_btn = ctk.CTkButton(self, text="Browse", command=self.browse_output, width=80)
        self.output_btn.grid(row=3, column=2, padx=(0, 20), pady=10)

        # FPS
        self.fps_label = ctk.CTkLabel(self, text="FPS (Frames/Sec):")
        self.fps_label.grid(row=4, column=0, padx=20, pady=10, sticky="e")
        self.fps_var = ctk.StringVar(value="10")
        self.fps_entry = ctk.CTkEntry(self, textvariable=self.fps_var)
        self.fps_entry.grid(row=4, column=1, padx=(0, 10), pady=10, sticky="w", ipadx=20)

        # Quality
        self.quality_label = ctk.CTkLabel(self, text="Quality (1-100):")
        self.quality_label.grid(row=5, column=0, padx=20, pady=10, sticky="e")
        self.quality_var = ctk.IntVar(value=80)
        self.quality_slider = ctk.CTkSlider(self, from_=1, to=100, variable=self.quality_var, command=self.update_quality_label)
        self.quality_slider.grid(row=5, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.quality_val_label = ctk.CTkLabel(self, text="80")
        self.quality_val_label.grid(row=5, column=2, padx=(0, 20), pady=10, sticky="w")

        # Size Settings Frame
        self.size_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.size_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        self.resize_var = ctk.BooleanVar(value=False)
        self.resize_cb = ctk.CTkCheckBox(self.size_frame, text="Resize Output?", variable=self.resize_var, command=self.toggle_resize)
        self.resize_cb.grid(row=0, column=0, columnspan=4, pady=(0, 10))

        self.width_label = ctk.CTkLabel(self.size_frame, text="Width:")
        self.width_label.grid(row=1, column=0, padx=(0, 5))
        self.width_var = ctk.StringVar()
        self.width_entry = ctk.CTkEntry(self.size_frame, textvariable=self.width_var, state="disabled", width=80)
        self.width_entry.grid(row=1, column=1, padx=(0, 20))

        self.height_label = ctk.CTkLabel(self.size_frame, text="Height:")
        self.height_label.grid(row=1, column=2, padx=(0, 5))
        self.height_var = ctk.StringVar()
        self.height_entry = ctk.CTkEntry(self.size_frame, textvariable=self.height_var, state="disabled", width=80)
        self.height_entry.grid(row=1, column=3)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_label.grid(row=7, column=0, columnspan=3, pady=(20, 5))

        # Convert Button
        self.convert_btn = ctk.CTkButton(self, text="Convert to WebP", command=self.start_conversion, height=40, font=ctk.CTkFont(weight="bold"))
        self.convert_btn.grid(row=8, column=0, columnspan=3, padx=20, pady=(10, 5), sticky="ew")

        # Credentials Label
        self.credentials_label = ctk.CTkLabel(self, text="Created by Carlos Oliveira (cadudatoro@gmail.com) | datoro.com", font=ctk.CTkFont(size=10, slant="italic"), text_color="gray")
        self.credentials_label.grid(row=9, column=0, columnspan=3, pady=(0, 10))


    def update_quality_label(self, value):
        self.quality_val_label.configure(text=str(int(value)))

    def toggle_resize(self):
        state = "normal" if self.resize_var.get() else "disabled"
        self.width_entry.configure(state=state)
        self.height_entry.configure(state=state)

    def scan_directory(self, directory):
        self.sequences_map.clear()
        valid_exts = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff')
        
        try:
            files = [f for f in os.listdir(directory) if f.lower().endswith(valid_exts)]
        except Exception as e:
            messagebox.showerror("Error Reading Directory", f"Could not read directory:\n{str(e)}\n\nThis may be a macOS Permissions issue. Try running via terminal or allow folder access in System Settings.")
            files = []
            
        # Regex to capture the prefix string up until numbers followed by extension
        # e.g., "walk_001.png" -> group 1 matches "walk_"
        pattern = re.compile(r'^(.*?)(\d+)\.[^.]+$')
        
        for f in files:
            match = pattern.match(f)
            if match:
                prefix = match.group(1)
                seq_name = prefix if prefix else "Sequence (No Prefix)"
            else:
                seq_name = "Singles / Unsequenced"
                
            if seq_name not in self.sequences_map:
                self.sequences_map[seq_name] = []
            self.sequences_map[seq_name].append(f)
            
        # Sort files inside each sequence
        for seq in self.sequences_map:
            self.sequences_map[seq].sort()
            
        if not self.sequences_map:
            self.seq_combo.configure(values=["No valid images found"])
            self.seq_var.set("No valid images found")
            self.output_var.set("")
            return
            
        # Create display names with frame counts
        display_values = []
        for seq_name, seq_files in self.sequences_map.items():
            display_values.append(f"{seq_name} ({len(seq_files)} frames)")
            
        display_values.sort()
        self.seq_combo.configure(values=display_values)
        self.seq_var.set(display_values[0])
        self.on_sequence_selected(display_values[0])

    def on_sequence_selected(self, choice):
        # Extract the sequence name from choice like "walk_ (5 frames)"
        # Note: choice might contain "(No Prefix)" or "Singles" so we split by " (" and rejoin if needed
        # Or safely finding the last " (" 
        idx = choice.rfind(" (")
        if idx != -1:
            seq_name = choice[:idx]
        else:
            seq_name = choice
            
        input_dir = self.input_var.get()
        if input_dir and seq_name:
            # Output file named exactly like the sequence prefix
            safe_name = "animated" if "Unsequenced" in seq_name else seq_name
            if not safe_name: safe_name = "sequence"
            # Place it in the selected directory next to the images
            default_out = os.path.join(input_dir, f"{safe_name}.webp")
            self.output_var.set(default_out)

    def browse_input(self):
        directory = filedialog.askdirectory()
        if directory:
            self.input_var.set(directory)
            self.scan_directory(directory)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".webp",
            filetypes=[("WebP files", "*.webp"), ("All files", "*.*")]
        )
        if file_path:
            self.output_var.set(file_path)

    def start_conversion(self):
        input_dir = self.input_var.get()
        output_file = self.output_var.get()

        if not input_dir or not output_file:
            messagebox.showerror("Error", "Please select input directory and output file.")
            return

        try:
            fps = float(self.fps_var.get())
            if fps <= 0: raise ValueError
            duration = int(1000 / fps) # Duration per frame in ms
        except ValueError:
            messagebox.showerror("Error", "FPS must be a positive number.")
            return

        quality = self.quality_var.get()

        resize = self.resize_var.get()
        target_size = None
        if resize:
            try:
                w = int(self.width_var.get())
                h = int(self.height_var.get())
                if w <= 0 or h <= 0: raise ValueError
                target_size = (w, h)
            except ValueError:
                messagebox.showerror("Error", "Width and Height must be positive integers.")
                return

        self.status_label.configure(text="Processing...", text_color="blue")
        self.update()

        try:
            # Determine which sequence was selected
            choice = self.seq_var.get()
            if choice == "No folder selected" or choice == "No valid images found":
                messagebox.showerror("Error", "No valid sequence selected.")
                return
                
            idx = choice.rfind(" (")
            seq_name = choice[:idx] if idx != -1 else choice
            
            files = self.sequences_map.get(seq_name, [])
            
            if not files:
                messagebox.showerror("Error", "Selected sequence contains no files.")
                self.status_label.configure(text="Ready")
                return

            frames = []
            for i, f in enumerate(files):
                self.status_label.configure(text=f"Loading image {i+1}/{len(files)}")
                self.update()
                
                path = os.path.join(input_dir, f)
                img = Image.open(path)
                
                if target_size:
                    # LANCZOS is high quality filter
                    img = img.resize(target_size, Image.Resampling.LANCZOS)
                
                frames.append(img)

            self.status_label.configure("Saving WebP animation...")
            self.update()

            frames[0].save(
                output_file,
                format="WebP",
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=0, # loop forever
                quality=quality
            )

            self.status_label.configure(text="Success!", text_color="green")
            messagebox.showinfo("Success", f"Animated WebP successfully saved to:\n{output_file}")
            
        except Exception as e:
            self.status_label.configure(text="Error occurred", text_color="red")
            messagebox.showerror("Error", f"An error occurred during conversion:\n{str(e)}")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = WebpConverterApp()
    app.mainloop()
