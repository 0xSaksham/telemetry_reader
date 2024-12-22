## Installation and System Integration

### 1. Basic Installation

```bash
# Navigate to the Cursor User directory
cd $HOME/.config/Cursor/User/

# Clone the repository
git clone <repository-url> telemetry_reader
cd telemetry_reader

# Make the script executable
chmod +x telemetry_reader.py
```

### 2. System-wide Integration

The script needs to access the storage.json file in the Cursor configuration directory. Choose one of the following methods to run the script from anywhere:

#### Method 1: Create a Symbolic Link (Recommended)

```bash
# Create symbolic link with absolute path
sudo ln -s "$HOME/.config/Cursor/User/telemetry-tools/telemetry_reader.py" /usr/local/bin/telemetry-reader

# Now you can run from anywhere using:
telemetry-reader
```

#### Method 2: Create Shell Alias

For Bash users (add to ~/.bashrc):

```bash
# Add alias to .bashrc with absolute path
echo "alias telemetry-reader='python3 $HOME/.config/Cursor/User/telemetry-tools/telemetry_reader.py'" >> ~/.bashrc

# Reload bash configuration
source ~/.bashrc
```

For Zsh users (add to ~/.zshrc):

```bash
# Add alias to .zshrc with absolute path
echo "alias telemetry-reader='python3 $HOME/.config/Cursor/User/telemetry-tools/telemetry_reader.py'" >> ~/.zshrc

# Reload zsh configuration
source ~/.zshrc
```

#### Method 3: Create Desktop Entry

```bash
# Create desktop entry with absolute path
sudo tee /usr/share/applications/telemetry-reader.desktop > /dev/null << EOL
[Desktop Entry]
Name=Telemetry Reader
Comment=Read and update telemetry data
Exec=python3 $HOME/.config/Cursor/User/telemetry-tools/telemetry_reader.py
Terminal=true
Type=Application
Categories=Utility;
EOL

# Make it executable
sudo chmod +x /usr/share/applications/telemetry-reader.desktop
```

### Important Notes

1. The script must be installed in the Cursor User directory to access storage.json
2. The tool expects storage.json to be in `$HOME/.config/Cursor/User/`
3. The `$HOME` variable will automatically expand to your home directory

### Verifying Installation

After setting up any of the above methods:

1. Open a new terminal
2. Type `telemetry-reader` and press Enter
3. The script should run and find storage.json automatically

### Troubleshooting

If you encounter issues:

- Verify the correct path: `ls -l $HOME/.config/Cursor/User/storage.json`
- Check symbolic link: `ls -l /usr/local/bin/telemetry-reader`
- Ensure correct permissions: `ls -l $HOME/.config/Cursor/User/telemetry-tools/telemetry_reader.py`
- Verify your home directory: `echo $HOME`
