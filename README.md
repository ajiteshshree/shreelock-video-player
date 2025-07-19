# Shreelock Video Player 🎬

A professional desktop media player with advanced features, smart fullscreen controls, and automatic VLC engine management.

## ✨ Quick Start

1. **Download** `ShreelockVideoPlayer.exe` (single file - no installation needed)
2. **Double-click** to run (VLC engine downloads automatically if needed)
3. **Click "Open File"** to load a video
4. **Enjoy professional video playback!**
5. **Create shortcuts**: Options → "Create Shortcuts" (adds play button icons)
6. **Remove shortcuts**: Options → "Uninstall Shortcuts"

## 🚀 Key Features

### 📽️ Professional Video Playback

- **All Major Formats**: MP4, MKV, AVI, MOV, WMV, FLV, WebM, MPEG, 3GP
- **Advanced Codecs**: H.264, H.265, VP9, AAC, FLAC - everything VLC supports
- **Long Video Support**: Optimized for 4-5+ hour movies
- **Subtitle Support**: SRT, VTT, SSA, ASS (embedded and external)

### 🎯 Smart Fullscreen Experience

- **Borderless Interface**: Complete elimination of gray boundaries
- **Auto-hiding Controls**: Menu/controls appear when mouse moves to edges
- **Smart Cursor Management**: Auto-hide cursor after 3 seconds
- **Progress Overlay**: Visual seeking feedback during fullscreen navigation
- **Cinema Mode**: True edge-to-edge video display

### 🎛️ Advanced Controls

- **Extended Volume**: 0-200% range with OSD feedback
- **Precision Seeking**: Hold arrow keys for continuous seeking (2s per 100ms)
- **Subtitle Cycling**: Automatic detection and switching
- **Professional Shortcuts**: VLC-like keyboard controls

### 🔧 System Integration

- **Automatic VLC Management**: Downloads VLC engine if not present
- **Desktop Shortcuts**: Create shortcuts with play button icons
- **Start Menu Integration**: Professional Windows integration
- **Portable Design**: Single .exe file, run anywhere

## 🎹 Complete Keyboard Shortcuts

### Playback Controls

| Key        | Action                     |
| ---------- | -------------------------- |
| `Spacebar` | Play/Pause toggle          |
| `←` (Hold) | Continuous seek backward   |
| `→` (Hold) | Continuous seek forward    |
| `C`        | Clear/remove current video |

### Volume Controls

| Key                       | Action               |
| ------------------------- | -------------------- |
| `↑`                       | Increase volume +10% |
| `↓`                       | Decrease volume -10% |
| Range: 0% to 200% maximum |

### Interface Controls

| Key          | Action                 |
| ------------ | ---------------------- |
| `F` or `F11` | Toggle fullscreen mode |
| `Escape`     | Exit fullscreen mode   |
| `Ctrl+O`     | Open file dialog       |
| `Ctrl+Q`     | Exit application       |

### Mouse Controls

- **Click Progress Bar**: Jump to specific position
- **Mouse Movement** (fullscreen):
  - **Top area**: Reveals menu bar
  - **Bottom area**: Reveals controls
- **Auto-hide**: Everything hides after 3 seconds

## 🔧 System Requirements

- **OS**: Windows 7 or later
- **RAM**: 512MB minimum (more for large videos)
- **Storage**: 50MB for app + video files
- **VLC Engine**: Automatically downloaded if needed

## 📋 Menu Structure

### File Menu

- **Open File** (`Ctrl+O`) - Load video files
- **Exit** (`Ctrl+Q`) - Close application

### Options Menu

- **Clear Video** (`C`) - Remove current video
- **Create Shortcuts** - Add desktop/start menu shortcuts with play icons
- **Uninstall Shortcuts** - Remove shortcuts when no longer needed
- **Fullscreen** (`F`/`F11`) - Toggle fullscreen mode

## 🔄 Automatic VLC Management

**Shreelock Video Player** automatically manages the VLC engine:

1. **First Run**: Checks if VLC is installed
2. **Auto-Download**: Downloads VLC installer if missing
3. **Silent Install**: Installs VLC in background
4. **Seamless Experience**: User doesn't need to manually download anything

### What happens automatically:

- ✅ VLC detection on startup
- ✅ Automatic download from official VLC website
- ✅ Background installation process
- ✅ Progress notifications to user
- ✅ Fallback to manual instructions if auto-install fails

## 🏗️ Technical Architecture

- **Media Engine**: VLC backend for maximum format compatibility
- **GUI Framework**: Python tkinter for cross-platform support
- **Threading**: Separate threads for smooth UI updates
- **OSD System**: Custom on-screen display with smart timers
- **Memory Optimization**: Efficient handling of large video files

## 📁 Project Structure

```
My VLC/
├── ShreelockVideoPlayer.exe    # Main executable (11.3MB)
├── README.md                   # This documentation
├── main.py                     # Source code (development)
└── build.py                    # Build script (development)
```

## 🚀 Distribution Files

### Single Download Option

- **`ShreelockVideoPlayer.exe`** (11.3MB)
  - Complete standalone application
  - Automatic VLC management
  - No installation required
  - Run from anywhere (USB, Downloads, etc.)

## 🔧 Advanced Features

### Enhanced Fullscreen

- **True Borderless**: No gray boundaries or window chrome
- **Smart Reveals**: Controls appear only when needed
- **Progressive Hiding**: Menu → Controls → Cursor fade sequence
- **Visual Feedback**: Progress overlays and OSD indicators

### Professional Seeking

- **Multiple Modes**: Single jump (10s) or continuous hold
- **Visual Progress**: Overlay bar shows position during seeking
- **Long Video Optimized**: Precise positioning for movies
- **Smooth Navigation**: Real-time position updates

### Subtitle Intelligence

- **Auto-Detection**: Finds embedded subtitle tracks
- **Language Switching**: Cycle through available options
- **Timing Sync**: Proper loading after playback starts
- **Format Support**: All VLC-compatible subtitle formats

## 🛠️ Development Information

### Building from Source

```bash
# Install dependencies
pip install -r requirements.txt

# Run from source
python main.py

# Build executable
python build.py
```

### Dependencies

- `python-vlc`: VLC Python bindings
- `tkinter`: GUI framework (built-in)
- `threading`: Multi-threading support
- `PyInstaller`: Executable packaging

## 🔍 Troubleshooting

### Common Issues

**"Failed to create VLC instance"**

- Solution: VLC will be automatically downloaded and installed
- Manual: Download VLC from https://videolan.org

**Video won't play**

- Check file format compatibility
- Ensure VLC engine is properly installed
- Try different video file

**Controls not appearing in fullscreen**

- Move mouse to top (menu) or bottom (controls) of screen
- Press `F11` or `Escape` to exit fullscreen

**Shortcuts not created**

- Ensure you have write permissions to Desktop/Start Menu
- Try running as administrator
- Check Windows security settings

## 📈 Performance

- **Startup Time**: < 3 seconds
- **Memory Usage**: ~50-100MB (varies by video size)
- **CPU Usage**: Low (VLC handles heavy lifting)
- **File Size**: 11.3MB standalone executable

## 🎯 Target Users

- **Media Enthusiasts**: Advanced playback features
- **Professionals**: Clean, distraction-free viewing
- **Students**: Long-form educational content
- **Casual Users**: Simple, no-setup video player

## 📝 Version History

- **v1.0**: Basic VLC integration and playback
- **v2.0**: Smart fullscreen and borderless interface
- **v3.0**: Advanced seeking and OSD system
- **v4.0**: Shortcut management with play icons
- **v5.0**: Automatic VLC management and installation

---

## 💡 Why Choose Shreelock Video Player?

1. **Zero Setup**: Single file download, auto-manages dependencies
2. **Professional Experience**: Cinema-quality fullscreen viewing
3. **Maximum Compatibility**: Plays everything VLC supports
4. **Smart Interface**: Controls appear only when needed
5. **User Control**: Create/remove shortcuts at will
6. **Portable**: Run from anywhere, no installation needed

---

**© 2025 Shreelock Video Player** - Professional media playback with intelligence

_Built with ❤️ using Python, VLC, and modern UI principles_
