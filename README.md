# ⚡ TitanHash

**TitanHash** is an ultra-high-performance hashing engine written in Python, engineered to fully leverage the Multi-Core architecture of modern processors and eliminate traditional disk I/O bottlenecks.

## 🚀 Features
- **Asynchronous Multi-Core Architecture:** Utilizes Multi-Threading and a Producer-Consumer queue pattern to parallelize cryptographic calculations.
- **Zero Disk Bottlenecks:** Your hard drive or SSD reads massive files at its maximum rated speed (using optimal 8MB chunks) without ever pausing to wait for CPU calculations.
- **3-in-1 Hashing (No Slowdowns):** Computes **MD5, SHA-1, and SHA-256** simultaneously. Because they run in parallel on separate CPU cores, adding multiple complex algorithms has zero impact on disk read times.
- **Drag-and-Drop Support (Windows):** Simply drag and drop any massive file (tens or hundreds of gigabytes) directly onto the script icon to begin hashing instantly.
- **Smart UI:** Features a highly optimized, non-blocking progress bar that updates in real-time without flooding the console, preserving top-tier performance.

## ⚙️ How to Use
1. Download or clone this repository.
2. Drag and drop any large file over the `TitanHash.py` icon.
3. Alternatively, launch the script from your terminal or double-click it to manually paste the file path.

## 🛠️ Technical Details
Implemented entirely in **Python**, the system bypasses the limitations of the Global Interpreter Lock (GIL) by offloading `hashlib.update` calls to dedicated background threads. RAM usage is strictly capped at a 32MB buffer, preventing memory saturation even if your SSD read speed outpaces your CPU computation speed.
