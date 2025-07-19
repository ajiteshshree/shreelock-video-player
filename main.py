"""
Shreelock Video Player
A desktop media player built with Python and VLC bindings
Supports MP4, MKV formats with volume control, subtitles, and seek functionality
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import vlc
import os
import threading
import time
from pathlib import Path
import sys
import shutil
import tempfile
import subprocess
import urllib.request
import urllib.error

def create_play_icon():
    """Create a play button icon file for shortcuts"""
    try:
        # Use custom play_icon.ico file if available
        if getattr(sys, 'frozen', False):
            # Running as compiled executable - icon should be in same directory as exe
            exe_dir = os.path.dirname(sys.executable)
            icon_path = os.path.join(exe_dir, "play_icon.ico")
        else:
            # Running as script - icon should be in same directory as script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "play_icon.ico")
        
        # Check if custom icon exists
        if os.path.exists(icon_path):
            print(f"✅ Using custom icon: {icon_path}")
            return icon_path
        
        # Fallback to Windows built-in icon if custom icon not found
        print("⚠️ Custom icon not found, using Windows built-in icon")
        icon_source = "shell32.dll,137"
        return icon_source
    except Exception as e:
        print(f"Could not create icon: {e}")
        # Fallback to Windows built-in icon
        return "shell32.dll,137"

def check_vlc_installation():
    """Check if VLC is installed on the system"""
    try:
        # Try to create a VLC instance to test if it's working
        test_instance = vlc.Instance('--quiet')
        if test_instance:
            return True
    except Exception:
        pass
    
    # Check common VLC installation paths
    vlc_paths = [
        "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
        "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe",
        os.path.join(os.environ.get('PROGRAMFILES', ''), 'VideoLAN', 'VLC', 'vlc.exe'),
        os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'VideoLAN', 'VLC', 'vlc.exe')
    ]
    
    for path in vlc_paths:
        if os.path.exists(path):
            return True
    
    return False

def download_vlc_installer(progress_callback=None):
    """Download VLC installer from official website"""
    try:
        # VLC download URL (64-bit Windows installer)
        vlc_url = "https://download.videolan.org/pub/videolan/vlc/last/win64/vlc-3.0.20-win64.exe"
        temp_dir = tempfile.gettempdir()
        installer_path = os.path.join(temp_dir, "vlc_installer.exe")
        
        def download_progress_hook(block_num, block_size, total_size):
            if progress_callback and total_size > 0:
                progress = min((block_num * block_size) / total_size * 100, 100)
                progress_callback(progress)
        
        urllib.request.urlretrieve(vlc_url, installer_path, download_progress_hook)
        return installer_path
        
    except Exception as e:
        print(f"Failed to download VLC: {e}")
        return None

def install_vlc_silently(installer_path):
    """Install VLC silently in the background"""
    try:
        # Run VLC installer with silent parameters
        result = subprocess.run([
            installer_path, 
            '/S',  # Silent installation
            '/NCRC'  # Skip CRC check
        ], capture_output=True, text=True, timeout=300)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Failed to install VLC: {e}")
        return False

def auto_install_vlc_if_needed():
    """Automatically install VLC if not present"""
    if check_vlc_installation():
        return True
    
    # Show installation dialog
    result = messagebox.askyesno(
        "VLC Engine Required",
        "Shreelock Video Player needs VLC Media Player to function.\n\n"
        "Would you like to automatically download and install VLC?\n"
        "(This will download ~40MB from the official VLC website)\n\n"
        "Click 'Yes' for automatic installation\n"
        "Click 'No' for manual installation instructions"
    )
    
    if not result:
        # Show manual installation instructions
        messagebox.showinfo(
            "Manual Installation",
            "Please download and install VLC Media Player from:\n"
            "https://videolan.org/vlc/\n\n"
            "After installation, restart Shreelock Video Player."
        )
        return False
    
    # Create progress window
    progress_window = tk.Toplevel()
    progress_window.title("Installing VLC Engine")
    progress_window.geometry("400x150")
    progress_window.resizable(False, False)
    progress_window.configure(bg='black')
    
    # Center the window
    progress_window.transient()
    progress_window.grab_set()
    
    status_label = tk.Label(
        progress_window, 
        text="Downloading VLC Media Player...", 
        bg='black', 
        fg='white',
        font=('Arial', 12)
    )
    status_label.pack(pady=20)
    
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(
        progress_window, 
        variable=progress_var, 
        maximum=100,
        length=350
    )
    progress_bar.pack(pady=10)
    
    def update_progress(progress):
        progress_var.set(progress)
        progress_window.update()
    
    try:
        # Download VLC installer
        status_label.config(text="Downloading VLC installer...")
        progress_window.update()
        
        installer_path = download_vlc_installer(update_progress)
        if not installer_path:
            raise Exception("Download failed")
        
        # Install VLC
        status_label.config(text="Installing VLC Media Player...")
        progress_var.set(100)
        progress_window.update()
        
        if install_vlc_silently(installer_path):
            status_label.config(text="Installation completed successfully!")
            progress_window.update()
            time.sleep(2)
            progress_window.destroy()
            
            # Clean up installer
            try:
                os.remove(installer_path)
            except:
                pass
                
            messagebox.showinfo(
                "Success", 
                "VLC Media Player has been installed successfully!\n"
                "Shreelock Video Player is ready to use."
            )
            return True
        else:
            raise Exception("Installation failed")
            
    except Exception as e:
        progress_window.destroy()
        messagebox.showerror(
            "Installation Failed",
            f"Failed to automatically install VLC: {str(e)}\n\n"
            "Please manually download and install VLC from:\n"
            "https://videolan.org/vlc/"
        )
        return False

class ShreelockVideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Shreelock Video Player")
        self.root.geometry("800x600")
        self.root.configure(bg='black')  # Remove gray boundaries
        
        # VLC instance and player - with auto-installation
        try:
            # Check if VLC is available, install if needed
            if not auto_install_vlc_if_needed():
                messagebox.showerror(
                    "VLC Required", 
                    "VLC Media Player is required but not available.\n"
                    "Please install VLC manually and restart the application."
                )
                self.root.destroy()
                return
            
            self.vlc_instance = vlc.Instance('--quiet')
            self.player = self.vlc_instance.media_player_new()
            
        except Exception as e:
            messagebox.showerror(
                "VLC Error", 
                f"Failed to initialize VLC engine: {str(e)}\n\n"
                "Please ensure VLC Media Player is properly installed."
            )
            self.root.destroy()
            return
        
        # Player state variables
        self.is_playing = False
        self.current_file = None
        self.volume = 50
        self.duration = 0
        self.position = 0
        self.subtitle_tracks = []
        self.current_subtitle = -1
        self.is_fullscreen = False
        self.seeking_direction = None  # For continuous seeking
        self.seek_timer = None
        
        # Fullscreen state management
        self.cursor_hide_timer = None
        self.mouse_moved = False
        self.controls_visible = True
        self.menu_visible = True
        self.osd_widgets = {}  # Store OSD pop-up widgets
        self.osd_timers = {}   # Store OSD hide timers
        
        # Progress bar overlay for seeking in fullscreen
        self.progress_overlay = None
        self.progress_hide_timer = None
        
        # Create UI components
        self.create_menu_bar()
        self.create_widgets()
        self.setup_bindings()
        
        # Start position update thread
        self.update_thread_running = True
        self.update_thread = threading.Thread(target=self.update_position, daemon=True)
        self.update_thread.start()
    
    def create_menu_bar(self):
        """Create the professional menu bar"""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File...                    Ctrl+O", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit                             Ctrl+Q", command=self.exit_application)
        
        # Options menu  
        options_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Clear Video                         C", command=self.clear_video)
        options_menu.add_separator()
        options_menu.add_command(label="Create Shortcuts", command=self.create_shortcuts)
        options_menu.add_command(label="Uninstall Shortcuts", command=self.uninstall_shortcuts)
        options_menu.add_separator()
        options_menu.add_command(label="Fullscreen                     F / F11", command=self.toggle_fullscreen)
        
        # Add keyboard shortcuts to root
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-q>', lambda e: self.exit_application())
    
    def exit_application(self):
        """Exit the application"""
        self.on_closing()
    
    def create_widgets(self):
        """Create and layout all UI widgets"""
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Video display area
        self.video_frame = tk.Frame(self.main_frame, bg='black', height=400, highlightthickness=0, bd=0)
        self.video_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        self.video_frame.pack_propagate(False)
        
        # Video info label
        self.info_label = tk.Label(
            self.video_frame, 
            text="Click 'Open File' to load a video", 
            bg='black', 
            fg='white', 
            font=('Arial', 14)
        )
        self.info_label.pack(expand=True)
        
        # Progress bar frame
        self.progress_frame = tk.Frame(self.main_frame, bg='black')
        self.progress_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Time labels and progress bar
        time_frame = tk.Frame(self.progress_frame, bg='black')
        time_frame.pack(fill=tk.X)
        
        self.current_time_label = tk.Label(time_frame, text="00:00", bg='black', fg='white')
        self.current_time_label.pack(side=tk.LEFT)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(
            time_frame, 
            from_=0, 
            to=100, 
            orient=tk.HORIZONTAL, 
            variable=self.progress_var,
            command=self.on_progress_change
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        self.total_time_label = tk.Label(time_frame, text="00:00", bg='black', fg='white')
        self.total_time_label.pack(side=tk.RIGHT)
        
        # Controls frame
        self.controls_frame = tk.Frame(self.main_frame, bg='black')
        self.controls_frame.pack(fill=tk.X)
        
        # Playback controls (center)
        playback_frame = tk.Frame(self.controls_frame, bg='black')
        playback_frame.pack(side=tk.LEFT, expand=True)
        
        self.backward_button = tk.Button(
            playback_frame, 
            text="⏪ -10s", 
            command=self.seek_backward,
            bg='#1a1a1a',
            fg='white',
            font=('Arial', 10),
            relief=tk.FLAT,
            padx=10
        )
        self.backward_button.pack(side=tk.LEFT, padx=2)
        
        self.play_button = tk.Button(
            playback_frame, 
            text="▶️ Play", 
            command=self.toggle_play_pause,
            bg='#1a1a1a',
            fg='white',
            font=('Arial', 10),
            relief=tk.FLAT,
            padx=10
        )
        self.play_button.pack(side=tk.LEFT, padx=2)
        
        self.stop_button = tk.Button(
            playback_frame, 
            text="⏹️ Stop", 
            command=self.stop_playback,
            bg='#1a1a1a',
            fg='white',
            font=('Arial', 10),
            relief=tk.FLAT,
            padx=10
        )
        self.stop_button.pack(side=tk.LEFT, padx=2)
        
        self.forward_button = tk.Button(
            playback_frame, 
            text="⏩ +10s", 
            command=self.seek_forward,
            bg='#1a1a1a',
            fg='white',
            font=('Arial', 10),
            relief=tk.FLAT,
            padx=10
        )
        self.forward_button.pack(side=tk.LEFT, padx=2)
        
        # Volume controls (right side)
        volume_frame = tk.Frame(self.controls_frame, bg='black')
        volume_frame.pack(side=tk.RIGHT)
        
        tk.Label(volume_frame, text="🔊", bg='black', fg='white').pack(side=tk.LEFT)
        
        self.volume_var = tk.IntVar(value=self.volume)
        self.volume_scale = ttk.Scale(
            volume_frame, 
            from_=0, 
            to=200,  # Increased from 100 to 200
            orient=tk.HORIZONTAL, 
            variable=self.volume_var,
            command=self.on_volume_change,
            length=150
        )
        self.volume_scale.pack(side=tk.LEFT, padx=5)
        
        self.volume_label = tk.Label(volume_frame, text="50%", bg='black', fg='white')
        self.volume_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Subtitle controls
        subtitle_frame = tk.Frame(self.controls_frame, bg='black')
        subtitle_frame.pack(side=tk.RIGHT, padx=(0, 20))
        
        tk.Label(subtitle_frame, text="📝", bg='black', fg='white').pack(side=tk.LEFT)
        
        self.subtitle_var = tk.StringVar(value="None")
        self.subtitle_combo = ttk.Combobox(
            subtitle_frame,
            textvariable=self.subtitle_var,
            state="readonly",
            width=15,
            font=('Arial', 9)
        )
        self.subtitle_combo.pack(side=tk.LEFT, padx=5)
        self.subtitle_combo.bind('<<ComboboxSelected>>', self.on_subtitle_change)
        
        # Add reload subtitles button for debugging
        self.reload_subs_button = tk.Button(
            subtitle_frame,
            text="🔄",
            command=self.load_subtitle_tracks,
            bg='#404040',
            fg='white',
            font=('Arial', 8),
            relief=tk.FLAT,
            padx=5,
            width=2
        )
        self.reload_subs_button.pack(side=tk.LEFT, padx=2)
    
    def setup_bindings(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<space>', lambda e: self.toggle_play_pause())
        
        # Enhanced seeking with key press and release
        self.root.bind('<KeyPress-Left>', self.on_left_key_press)
        self.root.bind('<KeyRelease-Left>', self.on_left_key_release)
        self.root.bind('<KeyPress-Right>', self.on_right_key_press)
        self.root.bind('<KeyRelease-Right>', self.on_right_key_release)
        
        # Volume control
        self.root.bind('<KeyPress-Up>', self.on_up_key_press)
        self.root.bind('<KeyRelease-Up>', self.on_up_key_release)
        self.root.bind('<KeyPress-Down>', self.on_down_key_press)
        self.root.bind('<KeyRelease-Down>', self.on_down_key_release)
        
        # Other shortcuts
        self.root.bind('<s>', lambda e: self.cycle_subtitles())  # 's' key for subtitles
        self.root.bind('<f>', lambda e: self.toggle_fullscreen())  # 'f' key for fullscreen
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())  # F11 for fullscreen
        self.root.bind('<Escape>', lambda e: self.exit_fullscreen())  # Escape to exit fullscreen
        self.root.bind('<c>', lambda e: self.clear_video())  # 'c' key to clear video
        
        # Mouse motion tracking for fullscreen
        self.root.bind('<Motion>', self.on_mouse_move)
        self.video_frame.bind('<Motion>', self.on_mouse_move)
        
        self.root.focus_set()  # Enable keyboard events
    
    def open_file(self):
        """Open file dialog to select video file"""
        file_types = [
            ('Video files', '*.mp4 *.mkv *.avi *.mov *.wmv *.flv'),
            ('MP4 files', '*.mp4'),
            ('MKV files', '*.mkv'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=file_types
        )
        
        if filename:
            self.load_video(filename)
    
    def load_video(self, filename):
        """Load and prepare video for playback"""
        try:
            # Stop current playback if any
            self.stop_playback()
            
            # Create media object
            self.current_file = filename
            media = self.vlc_instance.media_new(filename)
            self.player.set_media(media)
            
            # Set video output to our frame (Windows specific)
            if os.name == 'nt':  # Windows
                self.player.set_hwnd(self.video_frame.winfo_id())
            else:  # Linux/Mac
                self.player.set_xwindow(self.video_frame.winfo_id())
            
            # Update UI
            file_name = Path(filename).name
            self.info_label.configure(text=f"Loaded: {file_name}")
            self.root.title(f"My VLC Player - {file_name}")
            
            # Parse media to get duration and subtitle tracks
            media.parse()
            self.duration = media.get_duration()
            
            # Reset subtitle UI first
            self.subtitle_tracks = ["None"]
            self.subtitle_combo['values'] = self.subtitle_tracks
            self.subtitle_combo.set("None")
            
            print(f"Loaded video: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load video file:\n{str(e)}")
    
    def toggle_play_pause(self):
        """Toggle between play and pause"""
        if not self.current_file:
            messagebox.showwarning("No Video", "Please open a video file first.")
            return
        
        if self.is_playing:
            self.player.pause()
            self.play_button.configure(text="▶️ Play")
            self.is_playing = False
        else:
            self.player.play()
            self.play_button.configure(text="⏸️ Pause")
            self.is_playing = True
            
            # Load subtitles after starting playback - this is when VLC can detect them properly
            self.root.after(2000, self.load_subtitle_tracks)  # Wait 2 seconds for media to initialize
    
    def stop_playback(self):
        """Stop video playback"""
        self.player.stop()
        self.is_playing = False
        self.play_button.configure(text="▶️ Play")
        self.progress_var.set(0)
        self.current_time_label.configure(text="00:00")
        
        # Reset subtitle selection
        self.subtitle_tracks = ["None"]
        self.subtitle_combo['values'] = self.subtitle_tracks
        self.subtitle_combo.set("None")
        self.current_subtitle = -1
    
    def seek_forward(self):
        """Seek forward by 10 seconds"""
        if self.current_file and self.duration > 0:
            current_time = self.player.get_time()
            new_time = min(current_time + 10000, self.duration)  # VLC uses milliseconds
            self.player.set_time(new_time)
            
            # Show appropriate feedback based on mode
            if self.is_fullscreen:
                self.show_osd("seek", "", "⏩")
                self.show_progress_overlay()  # Show progress bar in fullscreen
    
    def seek_backward(self):
        """Seek backward by 10 seconds"""
        if self.current_file:
            current_time = self.player.get_time()
            new_time = max(current_time - 10000, 0)  # VLC uses milliseconds
            self.player.set_time(new_time)
            
            # Show appropriate feedback based on mode
            if self.is_fullscreen:
                self.show_osd("seek", "", "⏪")
                self.show_progress_overlay()  # Show progress bar in fullscreen
    
    def on_volume_change(self, value):
        """Handle volume slider changes"""
        self.volume = int(float(value))
        self.player.audio_set_volume(self.volume)
        self.volume_label.configure(text=f"{self.volume}%")
        
        # Show OSD if in fullscreen
        if self.is_fullscreen:
            volume_icon = "🔊" if self.volume > 0 else "🔇"
            self.show_osd("volume", f"Volume: {self.volume}%", volume_icon)
    
    def increase_volume(self):
        """Increase volume by 10"""
        new_volume = min(self.volume + 10, 200)  # Increased max to 200
        self.volume_var.set(new_volume)
        self.on_volume_change(new_volume)
    
    def decrease_volume(self):
        """Decrease volume by 10"""
        new_volume = max(self.volume - 10, 0)
        self.volume_var.set(new_volume)
        self.on_volume_change(new_volume)
    
    def on_progress_change(self, value):
        """Handle progress bar changes (seeking)"""
        if self.current_file and self.duration > 0:
            position = float(value) / 100.0
            new_time = int(position * self.duration)
            self.player.set_time(new_time)
    
    def load_subtitle_tracks(self):
        """Load available subtitle tracks - fixed detection method"""
        try:
            print("🔍 Searching for subtitle tracks...")
            
            # Wait a moment for VLC to fully initialize
            time.sleep(1)
            
            # Get subtitle track count
            subtitle_count = self.player.video_get_spu_count()
            print(f"VLC reports {subtitle_count} subtitle tracks")
            
            # Initialize with None option
            self.subtitle_tracks = ["None"]
            
            if subtitle_count > 0:
                try:
                    # Get subtitle track descriptions
                    subtitle_descriptions = self.player.video_get_spu_description()
                    print(f"Subtitle descriptions: {subtitle_descriptions}")
                    
                    if subtitle_descriptions:
                        for i, (track_id, description) in enumerate(subtitle_descriptions):
                            # Skip the "Disable" option (ID = -1)
                            if track_id == -1:
                                continue
                                
                            if description:
                                # Handle both string and bytes
                                if isinstance(description, bytes):
                                    description = description.decode('utf-8', errors='ignore')
                                
                                # Clean up the description
                                desc_clean = description.replace('MoviesMod.chat - ', '').strip('[]')
                                track_name = f"Track {len(self.subtitle_tracks)}: {desc_clean}"
                            else:
                                track_name = f"Track {len(self.subtitle_tracks)}"
                            
                            self.subtitle_tracks.append(track_name)
                            print(f"Added subtitle track: {track_name} (VLC ID: {track_id})")
                    
                except Exception as e:
                    print(f"Error getting subtitle descriptions: {e}")
                    # Fallback: Add numbered tracks based on count
                    for i in range(1, subtitle_count):  # Skip first one if it's "Disable"
                        track_name = f"Track {i}"
                        self.subtitle_tracks.append(track_name)
                        print(f"Added fallback track: {track_name}")
            
            # Method 2: Also check for external subtitle files
            if self.current_file:
                self.detect_external_subtitles()
            
            # Update the UI
            self.subtitle_combo['values'] = self.subtitle_tracks
            self.subtitle_combo.set("None")
            self.current_subtitle = -1
            
            total_tracks = len(self.subtitle_tracks) - 1  # -1 for "None"
            if total_tracks > 0:
                print(f"✅ Found {total_tracks} subtitle tracks total")
                
                # Auto-select first subtitle track if available
                if len(self.subtitle_tracks) > 1:
                    print("🎯 Auto-selecting first subtitle track")
                    self.subtitle_combo.set(self.subtitle_tracks[1])
                    self.on_subtitle_change()
            else:
                print("❌ No subtitle tracks found")
                
        except Exception as e:
            print(f"❌ Error loading subtitles: {e}")
            import traceback
            traceback.print_exc()
            self.subtitle_tracks = ["None"]
            self.subtitle_combo['values'] = self.subtitle_tracks
            self.subtitle_combo.set("None")
    
    def detect_external_subtitles(self):
        """Detect external subtitle files in the same directory"""
        try:
            if not self.current_file:
                return
                
            import os
            from pathlib import Path
            
            video_path = Path(self.current_file)
            video_dir = video_path.parent
            video_name = video_path.stem
            
            # Common subtitle extensions
            subtitle_extensions = ['.srt', '.vtt', '.ass', '.ssa', '.sub']
            
            external_subs = []
            for ext in subtitle_extensions:
                # Check for subtitle files with same name
                sub_file = video_dir / f"{video_name}{ext}"
                if sub_file.exists():
                    external_subs.append(str(sub_file))
                    
                # Also check for common subtitle naming patterns
                for suffix in ['', '.en', '.eng', '.english']:
                    sub_file = video_dir / f"{video_name}{suffix}{ext}"
                    if sub_file.exists() and str(sub_file) not in external_subs:
                        external_subs.append(str(sub_file))
            
            # Add external subtitles to the list
            for i, sub_file in enumerate(external_subs):
                sub_name = Path(sub_file).name
                track_name = f"External: {sub_name}"
                if track_name not in self.subtitle_tracks:
                    self.subtitle_tracks.append(track_name)
                    print(f"Found external subtitle: {sub_name}")
                    
        except Exception as e:
            print(f"Error detecting external subtitles: {e}")
    
    def on_subtitle_change(self, event=None):
        """Handle subtitle track selection - fixed for proper VLC track IDs"""
        try:
            selected = self.subtitle_combo.get()
            print(f"🎯 Selected subtitle: {selected}")
            
            if selected == "None":
                # Disable subtitles
                self.player.video_set_spu(-1)
                self.current_subtitle = -1
                print("❌ Subtitles disabled")
                
            elif selected.startswith("External:"):
                # Handle external subtitle files
                sub_filename = selected.replace("External: ", "")
                
                if self.current_file:
                    from pathlib import Path
                    video_dir = Path(self.current_file).parent
                    sub_path = video_dir / sub_filename
                    
                    if sub_path.exists():
                        try:
                            self.player.video_set_subtitle_file(str(sub_path))
                            print(f"✅ Loaded external subtitle: {sub_filename}")
                        except Exception as e:
                            print(f"❌ Error loading external subtitle: {e}")
                            messagebox.showerror("Subtitle Error", f"Could not load subtitle file:\n{sub_filename}")
                
            else:
                # Handle embedded subtitle tracks
                try:
                    # Get the track index from our list (subtract 1 for "None")
                    track_list_index = self.subtitle_tracks.index(selected)
                    
                    if track_list_index > 0:  # Skip "None" at index 0
                        # Get the actual VLC track descriptions to find the right ID
                        subtitle_descriptions = self.player.video_get_spu_description()
                        
                        if subtitle_descriptions:
                            # Find the corresponding VLC track (skip "Disable" entry)
                            vlc_track_index = 0
                            for vlc_id, description in subtitle_descriptions:
                                if vlc_id != -1:  # Skip "Disable"
                                    vlc_track_index += 1
                                    if vlc_track_index == track_list_index:
                                        # Found the matching track
                                        self.player.video_set_spu(vlc_id)
                                        self.current_subtitle = vlc_id
                                        print(f"✅ Enabled subtitle track ID {vlc_id}: {selected}")
                                        return
                        
                        # Fallback: try using the track index directly
                        fallback_index = track_list_index - 1  # Convert to 0-based for VLC
                        self.player.video_set_spu(fallback_index)
                        self.current_subtitle = fallback_index
                        print(f"✅ Enabled subtitle track (fallback) index {fallback_index}: {selected}")
                    
                except (ValueError, IndexError) as e:
                    print(f"❌ Error selecting subtitle track: {e}")
                    
        except Exception as e:
            print(f"❌ Error changing subtitles: {e}")
            import traceback
            traceback.print_exc()
    
    def cycle_subtitles(self):
        """Cycle through subtitle tracks using 's' key"""
        if len(self.subtitle_tracks) <= 1:
            return
            
        # Move to next subtitle track
        current_index = 0
        try:
            current_selection = self.subtitle_combo.get()
            current_index = self.subtitle_tracks.index(current_selection)
        except ValueError:
            current_index = 0
        
        # Cycle to next track
        next_index = (current_index + 1) % len(self.subtitle_tracks)
        next_track = self.subtitle_tracks[next_index]
        
        # Update combobox and apply change
        self.subtitle_combo.set(next_track)
        self.on_subtitle_change()
    
    def format_time(self, milliseconds):
        """Format time from milliseconds to MM:SS or HH:MM:SS"""
        if milliseconds <= 0:
            return "00:00"
        
        seconds = int(milliseconds / 1000)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def update_position(self):
        """Update progress bar and time labels (runs in separate thread)"""
        while self.update_thread_running:
            try:
                if self.current_file and self.is_playing:
                    current_time = self.player.get_time()
                    if self.duration > 0 and current_time >= 0:
                        # Update progress bar
                        position = (current_time / self.duration) * 100
                        self.progress_var.set(position)
                        
                        # Update time labels
                        current_formatted = self.format_time(current_time)
                        total_formatted = self.format_time(self.duration)
                        
                        self.root.after(0, lambda: self.current_time_label.configure(text=current_formatted))
                        self.root.after(0, lambda: self.total_time_label.configure(text=total_formatted))
                
                time.sleep(0.5)  # Update every 500ms
            except:
                break
    
    def clear_video(self):
        """Clear the currently loaded video and reset UI"""
        try:
            # Stop playback
            self.stop_playback()
            
            # Clear current file reference
            self.current_file = None
            
            # Reset UI elements
            self.info_label.configure(text="Click 'Open File' to load a video")
            self.root.title("My VLC Media Player")
            
            # Reset progress and time
            self.duration = 0
            self.position = 0
            self.progress_var.set(0)
            self.current_time_label.configure(text="00:00")
            self.total_time_label.configure(text="00:00")
            
            # Clear subtitle tracks
            self.subtitle_tracks = ["None"]
            self.subtitle_combo['values'] = self.subtitle_tracks
            self.subtitle_combo.set("None")
            self.current_subtitle = -1
            
            print("✅ Video cleared successfully")
            
        except Exception as e:
            print(f"❌ Error clearing video: {e}")
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode with menu and control hiding"""
        try:
            if not self.current_file:
                messagebox.showwarning("No Video", "Please open a video file first.")
                return
            
            self.is_fullscreen = not self.is_fullscreen
            
            if self.is_fullscreen:
                # Enter fullscreen
                self.root.attributes('-fullscreen', True)
                
                # Remove all borders and padding for true fullscreen
                self.root.configure(bg='black', highlightthickness=0, bd=0)
                
                # Hide menu bar in fullscreen
                self.root.config(menu="")
                self.menu_visible = False
                
                # Repack video frame to fill entire screen without margins
                self.video_frame.pack_forget()
                self.video_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
                self.video_frame.configure(highlightthickness=0, bd=0)
                
                # Hide controls in fullscreen
                self.hide_controls()
                print("🖼️ Entered fullscreen mode - menu and controls hidden")
                
                # Start cursor auto-hide with enhanced mouse tracking
                self.start_cursor_auto_hide()
                
            else:
                # Exit fullscreen
                self.root.attributes('-fullscreen', False)
                
                # Restore menu bar
                self.root.config(menu=self.menubar)
                self.menu_visible = True
                
                # Restore original styling
                self.root.configure(bg='black')
                
                # Repack video frame with minimal padding
                self.video_frame.pack_forget()
                self.video_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
                
                # Show controls when exiting fullscreen
                self.show_controls()
                print("🗗 Exited fullscreen mode - menu and controls restored")
                
                # Stop cursor auto-hide and show cursor
                self.stop_cursor_auto_hide()
                self.root.configure(cursor="")
                
                # Hide any visible OSD
                self.hide_all_osd()
                print("🪟 Exited fullscreen mode - controls visible, borders restored")
                
        except Exception as e:
            print(f"❌ Error toggling fullscreen: {e}")
    
    def hide_controls(self):
        """Hide progress bar and control panel"""
        self.progress_frame.pack_forget()
        self.controls_frame.pack_forget()
        self.controls_visible = False
    
    def show_controls(self):
        """Show progress bar and control panel"""
        self.progress_frame.pack(fill=tk.X, pady=(0, 5))
        self.controls_frame.pack(fill=tk.X)
        self.controls_visible = True
    
    def on_mouse_move(self, event):
        """Handle mouse movement in fullscreen with menu and control reveal"""
        if self.is_fullscreen:
            # Show cursor when mouse moves
            self.root.configure(cursor="")
            self.mouse_moved = True
            
            # Get window dimensions
            window_height = self.root.winfo_height()
            
            # Show menu bar when mouse moves to top
            if event.y < 50 and not self.menu_visible:  # Top 50 pixels
                self.root.config(menu=self.menubar)
                self.menu_visible = True
                # Hide menu after 3 seconds
                self.root.after(3000, self.auto_hide_menu)
            
            # Show controls when mouse moves to bottom
            elif event.y > window_height - 100:  # Bottom 100 pixels
                if not self.controls_visible:
                    self.show_controls()
                    # Hide controls again after 3 seconds
                    self.root.after(3000, self.auto_hide_controls)
            
            # Hide menu if mouse moves away from top
            elif event.y > 100 and self.menu_visible:
                self.root.config(menu="")
                self.menu_visible = False
            
            # Restart cursor hide timer
            self.start_cursor_auto_hide()
    
    def auto_hide_controls(self):
        """Hide controls automatically after timeout"""
        if self.is_fullscreen and self.controls_visible:
            # Only hide if mouse hasn't moved recently
            self.root.after(100, self._check_and_hide_controls)
    
    def auto_hide_menu(self):
        """Hide menu bar automatically after timeout"""
        if self.is_fullscreen and self.menu_visible:
            # Check if mouse is still at top
            x, y = self.root.winfo_pointerxy()
            root_x, root_y = self.root.winfo_rootx(), self.root.winfo_rooty()
            relative_y = y - root_y
            
            if relative_y > 100:  # Mouse moved away from top
                self.root.config(menu="")
                self.menu_visible = False
    
    def _check_and_hide_controls(self):
        """Check if we should hide controls"""
        if self.is_fullscreen:
            # Get current mouse position
            x, y = self.root.winfo_pointerxy()
            root_x, root_y = self.root.winfo_rootx(), self.root.winfo_rooty()
            root_width, root_height = self.root.winfo_width(), self.root.winfo_height()
            
            # Check if mouse is still in bottom area
            relative_y = y - root_y
            if relative_y < root_height - 100:  # Mouse moved away from bottom
                self.hide_controls()
    
    def start_cursor_auto_hide(self):
        """Start timer to hide cursor"""
        self.stop_cursor_auto_hide()  # Cancel any existing timer
        self.cursor_hide_timer = self.root.after(3000, self.hide_cursor)
    
    def stop_cursor_auto_hide(self):
        """Stop cursor auto-hide timer"""
        if self.cursor_hide_timer:
            self.root.after_cancel(self.cursor_hide_timer)
            self.cursor_hide_timer = None
    
    def hide_cursor(self):
        """Hide cursor in fullscreen"""
        if self.is_fullscreen:
            self.root.configure(cursor="none")
    
    def exit_fullscreen(self):
        """Exit fullscreen mode (called by Escape key)"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes('-fullscreen', False)
            self.fullscreen_button.configure(text="⛶ Fullscreen")
            
            # Restore original styling
            self.root.configure(bg='#2b2b2b')
            
            # Repack video frame with original padding
            self.video_frame.pack_forget()
            self.video_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            # Always show controls when exiting fullscreen
            self.show_controls()
            self.root.configure(cursor="")
            self.stop_cursor_auto_hide()
            
            # Hide any visible OSD
            self.hide_all_osd()
            print("🪟 Exited fullscreen mode (Escape) - controls restored")
    
    # Enhanced seeking methods for continuous seeking
    def on_left_key_press(self, event):
        """Handle left arrow key press for continuous seeking"""
        if self.current_file:
            self.seeking_direction = "backward"
            self.continuous_seek()
    
    def on_left_key_release(self, event):
        """Handle left arrow key release to stop seeking"""
        self.stop_continuous_seek()
    
    def on_right_key_press(self, event):
        """Handle right arrow key press for continuous seeking"""
        if self.current_file:
            self.seeking_direction = "forward"
            self.continuous_seek()
    
    def on_right_key_release(self, event):
        """Handle right arrow key release to stop seeking"""
        self.stop_continuous_seek()
    
    def continuous_seek(self):
        """Perform continuous seeking while key is held"""
        if self.seeking_direction and self.current_file:
            current_time = self.player.get_time()
            
            if self.seeking_direction == "forward":
                new_time = min(current_time + 2000, self.duration)  # 2 seconds forward
                # Show feedback if in fullscreen
                if self.is_fullscreen:
                    self.show_osd("seek", "", "⏩")
                    self.show_progress_overlay()  # Show progress bar
            else:  # backward
                new_time = max(current_time - 2000, 0)  # 2 seconds backward
                # Show feedback if in fullscreen
                if self.is_fullscreen:
                    self.show_osd("seek", "", "⏪")
                    self.show_progress_overlay()  # Show progress bar
            
            self.player.set_time(new_time)
            
            # Schedule next seek
            self.seek_timer = self.root.after(100, self.continuous_seek)  # Every 100ms
    
    def stop_continuous_seek(self):
        """Stop continuous seeking"""
        self.seeking_direction = None
        if self.seek_timer:
            self.root.after_cancel(self.seek_timer)
            self.seek_timer = None
    
    # Enhanced volume control methods
    def on_up_key_press(self, event):
        """Handle up arrow key press for volume increase"""
        self.increase_volume()
        # Start continuous volume increase if held
        self.volume_timer = self.root.after(500, self.continuous_volume_up)  # Start after 500ms
    
    def on_up_key_release(self, event):
        """Handle up arrow key release to stop volume increase"""
        if hasattr(self, 'volume_timer') and self.volume_timer:
            self.root.after_cancel(self.volume_timer)
            self.volume_timer = None
    
    def on_down_key_press(self, event):
        """Handle down arrow key press for volume decrease"""
        self.decrease_volume()
        # Start continuous volume decrease if held
        self.volume_timer = self.root.after(500, self.continuous_volume_down)  # Start after 500ms
    
    def on_down_key_release(self, event):
        """Handle down arrow key release to stop volume decrease"""
        if hasattr(self, 'volume_timer') and self.volume_timer:
            self.root.after_cancel(self.volume_timer)
            self.volume_timer = None
    
    def continuous_volume_up(self):
        """Continuous volume increase while key is held"""
        if self.volume < 200:
            self.increase_volume()
            self.volume_timer = self.root.after(100, self.continuous_volume_up)  # Every 100ms
    
    def continuous_volume_down(self):
        """Continuous volume decrease while key is held"""
        if self.volume > 0:
            self.decrease_volume()
            self.volume_timer = self.root.after(100, self.continuous_volume_down)  # Every 100ms
    
    def hide_all_osd(self):
        """Hide all OSD pop-ups"""
        for osd_type, widget in self.osd_widgets.items():
            if widget and widget.winfo_exists():
                widget.destroy()
        self.osd_widgets.clear()
        
        # Cancel all OSD timers
        for timer in self.osd_timers.values():
            if timer:
                self.root.after_cancel(timer)
        self.osd_timers.clear()
    
    def show_osd(self, osd_type, message, icon=""):
        """Show an OSD pop-up message"""
        # Hide existing OSD of same type
        if osd_type in self.osd_widgets and self.osd_widgets[osd_type]:
            try:
                self.osd_widgets[osd_type].destroy()
            except:
                pass
        
        # Cancel existing timer for this OSD type
        if osd_type in self.osd_timers and self.osd_timers[osd_type]:
            self.root.after_cancel(self.osd_timers[osd_type])
        
        # Create different OSD styles based on type
        if osd_type == "seek":
            self.show_seek_arrow(message, icon)
            return
        
        # Create regular OSD window for volume
        osd = tk.Toplevel(self.root)
        osd.attributes('-topmost', True)
        osd.attributes('-toolwindow', True)  # Remove from taskbar
        osd.overrideredirect(True)  # Remove window decorations
        osd.configure(bg='black')
        
        # Create OSD content frame with semi-transparent background
        content_frame = tk.Frame(
            osd, 
            bg='black', 
            relief=tk.RAISED, 
            bd=2, 
            highlightthickness=1, 
            highlightcolor='white'
        )
        content_frame.pack(padx=10, pady=10)
        
        # Add icon and message
        if icon:
            icon_label = tk.Label(
                content_frame,
                text=icon,
                font=('Arial', 16, 'bold'),
                fg='white',
                bg='black',
                pady=5
            )
            icon_label.pack()
        
        message_label = tk.Label(
            content_frame,
            text=message,
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='black',
            pady=5
        )
        message_label.pack()
        
        # Position OSD on screen
        self.position_osd(osd, osd_type)
        
        # Store OSD widget
        self.osd_widgets[osd_type] = osd
        
        # Auto-hide after 2 seconds
        self.osd_timers[osd_type] = self.root.after(2000, lambda: self.hide_osd(osd_type))
    
    def show_seek_arrow(self, message, icon):
        """Show small seek arrow at screen edge"""
        # Create minimal arrow OSD
        osd = tk.Toplevel(self.root)
        osd.attributes('-topmost', True)
        osd.attributes('-toolwindow', True)
        osd.overrideredirect(True)
        osd.configure(bg='black')
        
        # Create simple arrow display
        arrow_label = tk.Label(
            osd,
            text=icon,
            font=('Arial', 48, 'bold'),  # Large arrow
            fg='white',
            bg='black',
            padx=20,
            pady=20
        )
        arrow_label.pack()
        
        # Position arrow at screen edge
        self.position_seek_arrow(osd, icon)
        
        # Store OSD widget
        self.osd_widgets["seek"] = osd
        
        # Auto-hide after 1 second (shorter for arrows)
        self.osd_timers["seek"] = self.root.after(1000, lambda: self.hide_osd("seek"))
    
    def position_seek_arrow(self, osd, icon):
        """Position seek arrow at screen edge"""
        osd.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Get OSD dimensions
        osd_width = osd.winfo_reqwidth()
        osd_height = osd.winfo_reqheight()
        
        # Position based on arrow direction
        if "⏩" in icon:  # Forward arrow
            # Right edge of screen, vertically centered
            x = screen_width - osd_width - 30
            y = (screen_height - osd_height) // 2
        else:  # Backward arrow "⏪"
            # Left edge of screen, vertically centered
            x = 30
            y = (screen_height - osd_height) // 2
        
        osd.geometry(f"{osd_width}x{osd_height}+{x}+{y}")
    
    def position_osd(self, osd, osd_type):
        """Position OSD on screen based on type"""
        osd.update_idletasks()  # Ensure size is calculated
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Get OSD dimensions
        osd_width = osd.winfo_reqwidth()
        osd_height = osd.winfo_reqheight()
        
        if osd_type == "volume":
            # Volume OSD: top-right corner
            x = screen_width - osd_width - 50
            y = 50
        elif osd_type == "seek":
            # Seek arrows: handled by position_seek_arrow
            x = (screen_width - osd_width) // 2
            y = (screen_height - osd_height) // 2
        else:
            # Default: center
            x = (screen_width - osd_width) // 2
            y = (screen_height - osd_height) // 2
        
        osd.geometry(f"{osd_width}x{osd_height}+{x}+{y}")
    
    def hide_osd(self, osd_type):
        """Hide specific OSD pop-up"""
        if osd_type in self.osd_widgets and self.osd_widgets[osd_type]:
            try:
                self.osd_widgets[osd_type].destroy()
            except:
                pass
            del self.osd_widgets[osd_type]
        
        if osd_type in self.osd_timers:
            if self.osd_timers[osd_type]:
                self.root.after_cancel(self.osd_timers[osd_type])
            del self.osd_timers[osd_type]
    
    def show_progress_overlay(self):
        """Show progress bar overlay in fullscreen"""
        if not self.is_fullscreen or not self.player.get_media():
            return
            
        # Hide existing overlay
        self.hide_progress_overlay()
        
        # Create progress overlay window
        self.progress_overlay = tk.Toplevel(self.root)
        self.progress_overlay.overrideredirect(True)
        self.progress_overlay.configure(bg='black')
        self.progress_overlay.attributes('-topmost', True)
        
        # Create progress bar
        progress_frame = tk.Frame(self.progress_overlay, bg='black', padx=20, pady=10)
        progress_frame.pack()
        
        # Current time and duration
        current_time = self.player.get_time()
        total_time = self.player.get_length()
        
        if total_time > 0:
            progress_percent = (current_time / total_time) * 100
        else:
            progress_percent = 0
        
        # Time labels
        time_frame = tk.Frame(progress_frame, bg='black')
        time_frame.pack(fill=tk.X)
        
        current_str = self.format_time(current_time)
        total_str = self.format_time(total_time)
        
        tk.Label(time_frame, text=current_str, fg='white', bg='black', 
                font=('Arial', 10)).pack(side=tk.LEFT)
        tk.Label(time_frame, text=total_str, fg='white', bg='black', 
                font=('Arial', 10)).pack(side=tk.RIGHT)
        
        # Progress bar
        progress_bg = tk.Frame(progress_frame, bg='#404040', height=6)
        progress_bg.pack(fill=tk.X, pady=(5, 0))
        
        progress_fill = tk.Frame(progress_bg, bg='#0078D4', height=6)
        progress_fill.place(x=0, y=0, relwidth=progress_percent/100, relheight=1)
        
        # Position overlay at bottom center
        self.position_progress_overlay()
        
        # Auto-hide after 2 seconds
        self.progress_hide_timer = self.root.after(2000, self.hide_progress_overlay)
    
    def position_progress_overlay(self):
        """Position progress overlay at bottom center"""
        if not self.progress_overlay:
            return
            
        self.progress_overlay.update_idletasks()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        overlay_width = self.progress_overlay.winfo_reqwidth()
        overlay_height = self.progress_overlay.winfo_reqheight()
        
        x = (screen_width - overlay_width) // 2
        y = screen_height - overlay_height - 80  # 80px from bottom
        
        self.progress_overlay.geometry(f"{overlay_width}x{overlay_height}+{x}+{y}")
    
    def hide_progress_overlay(self):
        """Hide progress overlay"""
        if self.progress_overlay:
            try:
                self.progress_overlay.destroy()
            except:
                pass
            self.progress_overlay = None
        
        if self.progress_hide_timer:
            self.root.after_cancel(self.progress_hide_timer)
            self.progress_hide_timer = None
    
    def create_shortcuts(self):
        """Create desktop and start menu shortcuts for the application"""
        try:
            # Get the current executable path
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                exe_path = sys.executable
            else:
                # Running as script - this shouldn't happen in distributed version
                exe_path = os.path.abspath(__file__)
                messagebox.showwarning("Warning", "This feature is designed for the compiled executable version.")
                return
            
            # Get user directories
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            start_menu_path = os.path.join(
                os.environ.get("APPDATA", ""), 
                "Microsoft", "Windows", "Start Menu", "Programs"
            )
            
            created_shortcuts = []
            
            # Create desktop shortcut
            try:
                desktop_shortcut = os.path.join(desktop_path, "Shreelock Video Player.lnk")
                self._create_windows_shortcut(exe_path, desktop_shortcut, "Professional video player with smart controls")
                created_shortcuts.append("Desktop")
            except Exception as e:
                print(f"Failed to create desktop shortcut: {e}")
            
            # Create start menu shortcut
            try:
                start_menu_shortcut = os.path.join(start_menu_path, "Shreelock Video Player.lnk")
                self._create_windows_shortcut(exe_path, start_menu_shortcut, "Professional video player with smart controls")
                created_shortcuts.append("Start Menu")
            except Exception as e:
                print(f"Failed to create start menu shortcut: {e}")
            
            # Show success message
            if created_shortcuts:
                locations = " and ".join(created_shortcuts)
                messagebox.showinfo(
                    "Shortcuts Created", 
                    f"Successfully created shortcuts in: {locations}\n\n"
                    "You can now access Shreelock Video Player from these locations!"
                )
            else:
                messagebox.showerror(
                    "Error", 
                    "Failed to create shortcuts. Please make sure you have write permissions."
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create shortcuts: {str(e)}")
    
    def _create_windows_shortcut(self, target_path, shortcut_path, description):
        """Create a Windows shortcut (.lnk file) using PowerShell with play button icon"""
        try:
            # Get the play button icon
            icon_source = create_play_icon()
            
            # Use PowerShell to create the shortcut
            powershell_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{target_path}"
$Shortcut.Description = "{description}"
$Shortcut.WorkingDirectory = "{os.path.dirname(target_path)}"'''

            # Add icon if available
            if icon_source:
                powershell_script += f'''
$Shortcut.IconLocation = "{icon_source}"'''
            
            powershell_script += '''
$Shortcut.Save()
'''
            
            # Write the PowerShell script to a temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as temp_file:
                temp_file.write(powershell_script)
                temp_script_path = temp_file.name
            
            try:
                # Execute the PowerShell script
                import subprocess
                result = subprocess.run([
                    'powershell', '-ExecutionPolicy', 'Bypass', '-File', temp_script_path
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode != 0:
                    raise Exception(f"PowerShell execution failed: {result.stderr}")
                    
            finally:
                # Clean up temporary script file
                try:
                    os.unlink(temp_script_path)
                except:
                    pass
                    
        except Exception as e:
            raise Exception(f"Failed to create shortcut: {str(e)}")

    def uninstall_shortcuts(self):
        """Remove desktop and start menu shortcuts for the application"""
        try:
            # Get user directories
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            start_menu_path = os.path.join(
                os.environ.get("APPDATA", ""), 
                "Microsoft", "Windows", "Start Menu", "Programs"
            )
            
            # Define shortcut paths
            desktop_shortcut = os.path.join(desktop_path, "Shreelock Video Player.lnk")
            start_menu_shortcut = os.path.join(start_menu_path, "Shreelock Video Player.lnk")
            
            removed_shortcuts = []
            
            # Remove desktop shortcut
            try:
                if os.path.exists(desktop_shortcut):
                    os.remove(desktop_shortcut)
                    removed_shortcuts.append("Desktop")
            except Exception as e:
                print(f"Failed to remove desktop shortcut: {e}")
            
            # Remove start menu shortcut
            try:
                if os.path.exists(start_menu_shortcut):
                    os.remove(start_menu_shortcut)
                    removed_shortcuts.append("Start Menu")
            except Exception as e:
                print(f"Failed to remove start menu shortcut: {e}")
            
            # Show result message
            if removed_shortcuts:
                locations = " and ".join(removed_shortcuts)
                messagebox.showinfo(
                    "Shortcuts Removed", 
                    f"Successfully removed shortcuts from: {locations}\n\n"
                    "Shreelock Video Player shortcuts have been uninstalled."
                )
            else:
                messagebox.showinfo(
                    "No Shortcuts Found", 
                    "No shortcuts were found to remove.\n\n"
                    "They may have been already deleted or never created."
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to uninstall shortcuts: {str(e)}")

    def on_closing(self):
        """Handle application closing"""
        # Stop all timers and threads
        self.update_thread_running = False
        self.stop_continuous_seek()
        self.stop_cursor_auto_hide()
        self.hide_all_osd()  # Clean up OSD windows
        self.hide_progress_overlay()  # Clean up progress overlay
        
        # Stop volume timers if they exist
        if hasattr(self, 'volume_timer') and self.volume_timer:
            self.root.after_cancel(self.volume_timer)
        
        # Stop the player and destroy window
        self.player.stop()
        self.root.destroy()

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ShreelockVideoPlayer(root)
    
    # Handle window close event
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
