import tkinter as tk
from tkinter import colorchooser
import asyncio
from kasa import Discover, SmartBulb

def async_run(coro):
    """Run the given coroutine in an asyncio event loop."""
    asyncio.run(coro)

async def discover_devices():
    """Discover and list Kasa smart devices."""
    devices = await Discover.discover()
    for addr, dev in devices.items():
        if isinstance(dev, SmartBulb):
            bulbs_listbox.insert(tk.END, dev.alias)

async def toggle_power():
    """Toggle the power state of the selected bulb."""
    selected_device = bulbs_listbox.get(tk.ANCHOR)
    devices = await Discover.discover()
    for addr, dev in devices.items():
        if dev.alias == selected_device and isinstance(dev, SmartBulb):
            await dev.update()
            await dev.turn_on() if not dev.is_on else await dev.turn_off()

async def change_color():
    """Change the color of the selected bulb."""
    color = colorchooser.askcolor(title="Choose color")[0]
    if color:
        selected_device = bulbs_listbox.get(tk.ANCHOR)
        devices = await Discover.discover()
        for addr, dev in devices.items():
            if dev.alias == selected_device and isinstance(dev, SmartBulb):
                await dev.update()
                if dev.is_color:
                    await dev.set_hsv(int(color[0]), int(color[1] / 2.55), int(color[2] / 2.55))

# Set up the main window
root = tk.Tk()
root.title("Kasa Smart Light Control")

# Listbox to display discovered devices
bulbs_listbox = tk.Listbox(root, height=10, width=50)
bulbs_listbox.pack(pady=20)

# Discover devices button
discover_btn = tk.Button(root, text="Discover Devices", command=lambda: async_run(discover_devices()))
discover_btn.pack(pady=10)

# Toggle power button
toggle_btn = tk.Button(root, text="Toggle Power", command=lambda: async_run(toggle_power()))
toggle_btn.pack(pady=10)

# Change color button
color_btn = tk.Button(root, text="Change Color", command=lambda: async_run(change_color()))
color_btn.pack(pady=10)

# Start the GUI event loop
root.mainloop()