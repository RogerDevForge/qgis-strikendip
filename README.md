# Strike and Dip - QGIS Plugin

A QGIS plugin designed for geologists to automate the process of adding strike and dip measurements to maps with properly oriented symbols displaying main geological features.

## Description

Strike and Dip simplifies geological mapping workflows in QGIS by providing tools to:
- Add strike and dip points to your geological maps
- Display oriented symbols with geological measurements
- Automate the visualization of structural geology data

## Installation

### From QGIS Plugin Manager
1. Open QGIS
2. Go to `Plugins` → `Manage and Install Plugins`
3. Search for "Strike and Dip"
4. Click `Install Plugin`

### Manual Installation
1. Download the plugin files
2. Copy the entire `striken_dip` directory to your QGIS plugin directory:
   - Windows: `C:/Users/[YourUser]/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins`
   - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
3. Restart QGIS
4. Enable the plugin in `Plugins` → `Manage and Install Plugins`

## Usage

1. Enable the plugin from the QGIS Plugin Manager
2. Access the Strike and Dip tools from the QGIS toolbar or menu
3. Add your strike and dip measurements
4. Symbols will be automatically oriented based on your measurements

## Development

### Requirements
- QGIS 3.x
- Python 3.x
- PyQt5

### Building Resources
Compile the resources file using:
```bash
pyrcc5 -o resources.py resources.qrc
```

### Testing
Run the tests using:
```bash
make test
```

### Customization
- Edit implementation: `striken_dip.py`
- Modify UI: Open `StrikenDip_dialog_base.ui` in Qt Designer
- Update icon: Replace `icon.png` with your custom icon

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Resources

- [QGIS Documentation](https://qgis.org/en/docs/)
- [PyQGIS Developer Cookbook](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/)

## License

Please add your license information here.

## Author

RogerDevForge

## Support

For issues, questions, or suggestions, please open an issue on the [GitHub repository](https://github.com/RogerDevForge/qgis-strikendip/issues).
