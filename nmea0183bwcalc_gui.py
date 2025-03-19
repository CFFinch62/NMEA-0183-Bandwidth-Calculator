#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path
from tkinter import colorchooser

class NMEA0183Toolkit:
    def __init__(self, master):
        self.master = master
        self.master.title("NMEA 0183 Bandwidth Calculator")
        
        # Load configuration
        self.config_path = Path(__file__).parent / 'config.json'
        self.load_config()
        
        # Create menu bar
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        
        # Create File menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.master.quit)
        
        # Create Help menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Show Help", command=self.show_help)
        
        # Load the database
        self.load_database()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tabs
        self.info_frame = ttk.Frame(self.notebook)
        self.calc_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.info_frame, text="Sentence Information")
        self.notebook.add(self.calc_frame, text="Bandwidth Calculator")
        
        self.create_info_tab()
        self.create_calc_tab()
        
    def load_database(self):
        """Load NMEA sentence database from JSON"""
        try:
            db_path = Path(__file__).parent / 'nmea_sentences.json'
            with open(db_path, 'r') as f:
                data = json.load(f)
            self.database = data['sentences']
        except Exception as e:
            print(f"Error loading database: {str(e)}")
            self.database = {}

    def load_config(self):
        """Load configuration from JSON file"""
        default_config = {
            'font_size': 14,
            'text_color': 'white',
            'bg_color': 'navy'
        }
        
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            self.config = default_config

    def save_config(self):
        """Save current configuration to JSON file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {str(e)}")

    def create_info_tab(self):
        """Create the Sentence Information tab"""
        # Create frames
        left_frame = ttk.Frame(self.info_frame)
        left_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        right_frame = ttk.Frame(self.info_frame)
        right_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Add font and color control frame at the top of right frame
        control_frame = ttk.Frame(right_frame)
        control_frame.pack(fill='x', pady=5)
        
        # Add font size controls
        ttk.Label(control_frame, text="Font Size:").pack(side='left', padx=5)
        ttk.Button(control_frame, text="-", width=3,
                   command=self.decrease_font).pack(side='left', padx=2)
        ttk.Button(control_frame, text="+", width=3,
                   command=self.increase_font).pack(side='left', padx=2)
        
        # Add color controls
        ttk.Label(control_frame, text="Colors:").pack(side='left', padx=(20,5))
        ttk.Button(control_frame, text="Text",
                   command=self.change_text_color).pack(side='left', padx=2)
        ttk.Button(control_frame, text="Background",
                   command=self.change_bg_color).pack(side='left', padx=2)
        
        # Create sentence listbox
        self.info_list = tk.Listbox(left_frame, width=10, height=15,
                                   font=('Verdana', 18),
                                   bg='black', fg='yellow',
                                   selectmode='single',
                                   selectbackground='yellow',
                                   selectforeground='black')
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical",
                                command=self.info_list.yview)
        self.info_list.configure(yscrollcommand=scrollbar.set)
        
        self.info_list.pack(side='left', fill='both')
        scrollbar.pack(side='right', fill='y')
        
        # Create info display with configured settings
        self.info_text = tk.Text(right_frame, wrap=tk.WORD,
                                font=('Courier', self.config['font_size'], 'bold'),
                                bg=self.config['bg_color'],
                                fg=self.config['text_color'])
        self.info_text.pack(fill='both', expand=True)
        
        # Populate listbox
        for sentence in sorted(self.database.keys()):
            self.info_list.insert(tk.END, sentence)
        
        # Bind selection event
        self.info_list.bind('<<ListboxSelect>>', self.show_sentence_info)

    def create_calc_tab(self):
        """Create the Bandwidth Calculator tab"""
        # Initialize calculator variables
        self.baud_rate = tk.StringVar(value="4800")
        self.update_rate = tk.StringVar(value="1")
        
        # Create frames
        left_frame = ttk.Frame(self.calc_frame)
        left_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        right_frame = ttk.Frame(self.calc_frame)
        right_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Create sentence listbox
        self.calc_list = tk.Listbox(left_frame, width=10, height=15,
                                   font=('Verdana', 18),
                                   bg='black', fg='yellow',
                                   selectmode='multiple',
                                   selectbackground='yellow',
                                   selectforeground='black')
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical",
                                command=self.calc_list.yview)
        self.calc_list.configure(yscrollcommand=scrollbar.set)
        
        self.calc_list.pack(side='left', fill='both')
        scrollbar.pack(side='right', fill='y')
        
        # Create controls
        controls_frame = ttk.Frame(right_frame)
        controls_frame.pack(fill='x', pady=20)
        
        # Baud rate selection
        ttk.Label(controls_frame, text="Baud Rate:",
                 font=('Verdana', 16)).pack(side='left', padx=10)
        baud_combo = ttk.Combobox(controls_frame, textvariable=self.baud_rate,
                                 values=["4800", "38400"],
                                 state='readonly', width=10,
                                 font=('Verdana', 16))
        baud_combo.pack(side='left', padx=10)
        
        # Update rate selection
        ttk.Label(controls_frame, text="Update Rate:",
                 font=('Verdana', 16)).pack(side='left', padx=10)
        update_combo = ttk.Combobox(controls_frame, textvariable=self.update_rate,
                                   values=["2", "1", "0.5", "0.2", "0.1", "0.05"],
                                   state='readonly', width=10,
                                   font=('Verdana', 16))
        update_combo.pack(side='left', padx=10)
        
        # Add Reset button
        reset_button = ttk.Button(controls_frame, text="Reset",
                                 command=self.reset_calculator)
        reset_button.pack(side='left', padx=20)
        
        # Progress bar and labels
        progress_frame = ttk.Frame(right_frame)
        progress_frame.pack(fill='x', pady=20)
        
        self.usage_label = ttk.Label(progress_frame, text="Bandwidth Usage: 0%",
                                    font=('Verdana', 20))
        self.usage_label.pack()
        
        self.progress = ttk.Progressbar(progress_frame, length=400,
                                      mode='determinate')
        self.progress.pack(fill='x', padx=5, pady=10)
        
        # Populate listbox
        for sentence in sorted(self.database.keys()):
            self.calc_list.insert(tk.END, sentence)
        
        # Bind events
        self.calc_list.bind('<<ListboxSelect>>', self.update_bandwidth)
        baud_combo.bind('<<ComboboxSelected>>', self.update_bandwidth)
        update_combo.bind('<<ComboboxSelected>>', self.update_bandwidth)

    def show_sentence_info(self, event=None):
        """Display information about the selected sentence"""
        selection = self.info_list.curselection()
        if not selection:
            return
        
        sentence_id = self.info_list.get(selection[0])
        try:
            sentence = self.database[sentence_id]
            
            # Clear previous info
            self.info_text.delete('1.0', tk.END)
            
            # Build and display sentence information
            info = []
            info.append(f"{sentence_id} is {len(sentence['sentence_structure'])} bytes long")
            info.append(f"\nDescription: {sentence['sentence_name']}")
            
            # Sentence structure - moved up after description
            info.append("\nSentence Structure:")
            info.append(f"  {sentence['sentence_structure']}")
            
            # Field information
            info.append(f"\nNumber of Fields: {sentence['num_fields']}")
            info.append("\nField Details:")
            for i, (name, length) in enumerate(zip(sentence['field_names'], 
                                                 sentence['chars_per_field'])):
                info.append(f"  Field {i+1}: {name}, {length}")
            
            # Standard and version information - moved to bottom
            info.append("\nStandard Information:")
            if sentence['standard'] == 'N':
                info.append("  Standard: NMEA 0183")
                if sentence['version']['nmea']:
                    info.append(f"  First Version: {sentence['version']['nmea'][0]}")
                    if sentence['version']['nmea'][1]:
                        info.append(f"  Current Version: {sentence['version']['nmea'][1]}")
            elif sentence['standard'] == 'I':
                info.append("  Standard: IEC 61162-1")
                if sentence['version']['iec']:
                    info.append(f"  Current Version: {sentence['version']['iec']}")
            elif sentence['standard'] == 'B':
                info.append("  Standards: NMEA 0183 and IEC 61162-1")
                if sentence['version']['nmea']:
                    info.append(f"  First NMEA Version: {sentence['version']['nmea'][0]}")
                    info.append(f"  Current NMEA Version: {sentence['version']['nmea'][1]}")
                if sentence['version']['iec']:
                    info.append(f"  Current IEC Version: {sentence['version']['iec']}")
            
            self.info_text.insert('1.0', "\n".join(info))
            
        except Exception as e:
            self.info_text.delete('1.0', tk.END)
            self.info_text.insert('1.0', f"Error displaying information for {sentence_id}: {str(e)}")

    def update_bandwidth(self, event=None):
        """Calculate and display bandwidth usage"""
        selections = self.calc_list.curselection()
        if not selections:
            self.progress['value'] = 0
            self.usage_label['text'] = "Bandwidth Usage: 0%"
            return
        
        total_bytes = 0
        for index in selections:
            sentence_id = self.calc_list.get(index)
            try:
                structure = self.database[sentence_id]['sentence_structure']
                total_bytes += len(structure)
            except (KeyError, IndexError):
                print(f"Error processing sentence {sentence_id}")
        
        baud = float(self.baud_rate.get())
        update = float(self.update_rate.get())
        
        transmission_time = (total_bytes * 10) / baud
        bandwidth = (transmission_time / update) * 100
        
        self.progress['value'] = min(bandwidth, 100)
        self.usage_label['text'] = f"Bandwidth Usage: {bandwidth:.1f}%"
        
        if bandwidth > 100:
            self.usage_label.configure(foreground='red')
        elif bandwidth > 80:
            self.usage_label.configure(foreground='orange')
        else:
            self.usage_label.configure(foreground='green')

    def reset_calculator(self):
        """Reset the bandwidth calculator to initial state"""
        self.calc_list.selection_clear(0, tk.END)
        self.progress['value'] = 0
        self.usage_label['text'] = "Bandwidth Usage: 0%"
        self.usage_label.configure(foreground='black')  # Reset color
        self.baud_rate.set("4800")  # Reset to default baud rate
        self.update_rate.set("1")   # Reset to default update rate

    def increase_font(self):
        """Increase the font size of the info display"""
        current_font = self.info_text['font'].split()
        size = int(current_font[1])
        if size < 24:  # Maximum size limit
            new_size = size + 2
            new_font = ('Courier', new_size, 'bold')
            self.info_text.configure(font=new_font)
            self.config['font_size'] = new_size
            self.save_config()

    def decrease_font(self):
        """Decrease the font size of the info display"""
        current_font = self.info_text['font'].split()
        size = int(current_font[1])
        if size > 8:  # Minimum size limit
            new_size = size - 2
            new_font = ('Courier', new_size, 'bold')
            self.info_text.configure(font=new_font)
            self.config['font_size'] = new_size
            self.save_config()

    def change_text_color(self):
        """Change the text color of the info display"""
        color = colorchooser.askcolor(title="Choose Text Color")
        if color[1]:  # color is ((r,g,b), hex_code)
            self.info_text.configure(fg=color[1])
            self.config['text_color'] = color[1]
            self.save_config()

    def change_bg_color(self):
        """Change the background color of the info display"""
        color = colorchooser.askcolor(title="Choose Background Color")
        if color[1]:  # color is ((r,g,b), hex_code)
            self.info_text.configure(bg=color[1])
            self.config['bg_color'] = color[1]
            self.save_config()

    def show_help(self):
        """Display help documentation from markdown file"""
        try:
            help_path = Path(__file__).parent / 'gui_help.md'
            with open(help_path, 'r') as f:
                help_text = f.read()
            
            # Create help window
            help_window = tk.Toplevel(self.master)
            help_window.title("NMEA 0183 Toolkit Help")
            help_window.geometry("600x400")
            
            # Create text widget with scrollbar
            help_text_widget = tk.Text(help_window, wrap=tk.WORD,
                                     font=('Courier', 12),
                                     padx=10, pady=10)
            scrollbar = ttk.Scrollbar(help_window, orient="vertical",
                                    command=help_text_widget.yview)
            help_text_widget.configure(yscrollcommand=scrollbar.set)
            
            help_text_widget.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Insert help text
            help_text_widget.insert('1.0', help_text)
            help_text_widget.configure(state='disabled')  # Make read-only
            
            # Center the help window
            help_window.update_idletasks()
            width = help_window.winfo_width()
            height = help_window.winfo_height()
            x = (help_window.winfo_screenwidth() // 2) - (width // 2)
            y = (help_window.winfo_screenheight() // 2) - (height // 2)
            help_window.geometry(f'+{x}+{y}')
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not load help file: {str(e)}")

def main():
    root = tk.Tk()
    app = NMEA0183Toolkit(root)
    
    # Center the window on screen
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Set a default window size if you want (optional)
    window_width = 1024
    window_height = 600
    
    # Calculate position coordinates
    x = (screen_width/2) - (window_width/2)
    y = (screen_height/2) - (window_height/2)
    
    # Set the position of the window
    root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
    
    root.mainloop()

if __name__ == "__main__":
    main()