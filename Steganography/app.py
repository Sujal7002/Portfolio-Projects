"""
 * Personal License
 *
 * Author: Sujal More
 * Project: Cloud Inventory Management App
 *
 * This code is provided solely for educational and
 * personal use. Unauthorized copying, distribution,
 * or commercial use of this code, in whole or in
 * part, without the explicit permission of the author
 * is strictly prohibited.
 *
 * For permissions or inquiries, please contact:
 * sujalm7200@gmail.com
 *
 * © 2025 Sujal More. All rights reserved.
"""

import streamlit as st
import os
from PIL import Image
import numpy as np

# Stego Directory
UPLOAD_FOLDER = "public_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Utility Functions
def file_to_bits(file_bytes):
    return ''.join(f'{byte:08b}' for byte in file_bytes)

def bits_to_bytes(bits):
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

# Working embed logic with header protection
def embed_message(carrier_bytes, message_bytes, S, L, C):
    S = max(S, 512)  # Avoid modifying file header
    carrier_bits = file_to_bits(carrier_bytes)
    message_bits = file_to_bits(message_bytes)

    new_bits = list(carrier_bits)
    idx = S
    mode_cycle = [8, 16, 28] if C == "cycle" else [L]
    cycle_index = 0

    for bit in message_bits:
        if idx >= len(new_bits):
            break
        new_bits[idx] = bit
        cycle_len = mode_cycle[cycle_index % len(mode_cycle)]
        cycle_index += 1
        idx += cycle_len

    return bits_to_bytes(''.join(new_bits[:len(carrier_bits)]))

# extract logic with header protection
def extract_message(stego_bytes, S, L, C, message_len_bytes):
    S = max(S, 512)  # Avoid reading from header
    stego_bits = file_to_bits(stego_bytes)
    bits_to_read = message_len_bytes * 8

    extracted_bits = []
    idx = S
    cycle = [8, 16, 28] if C == "cycle" else [L]
    cycle_index = 0

    for _ in range(bits_to_read):
        if idx >= len(stego_bits):
            break
        extracted_bits.append(stego_bits[idx])
        cycle_len = cycle[cycle_index % len(cycle)]
        cycle_index += 1
        idx += cycle_len

    return bits_to_bytes(''.join(extracted_bits))

# Upload Page
def upload_page():
    st.title("📝 Steganography File Upload")

    carrier_file = st.file_uploader("Upload Carrier File (P)", type=None)
    message_file = st.file_uploader("Upload Secret Message File (M)", type=None)
    typed_message = st.text_area("Optional Text Message to Embed")

    default_S_by_type = {
        "jpg": 32768,
        "jpeg": 32768,
        "png": 8192,
        "mp4": 65536,
        "wav": 8192,
        "doc": 16384,
        "bin": 4096,
    }

    # Auto-detect default S only if file is uploaded
    if carrier_file:
        file_ext = carrier_file.name.split(".")[-1].lower()
        default_S = default_S_by_type.get(file_ext, 8192)
    else:
        default_S = 8192

    S = st.number_input("Starting Bit (S)", min_value=0, value=default_S, step=8)
    st.caption(f"🧠 Starting Bit ≈ {S / 8:.2f} bytes ({S / 8192:.2f} KB)")
    if carrier_file and S < default_S:
        st.warning(f"⚠️ Recommended S for .{file_ext} is at least {default_S} bits to avoid corrupting the header.")

    L = st.number_input("Periodicity (L)", min_value=1, value=8)
    C = st.selectbox("Mode (C)", options=["fixed", "cycle"])

    if st.button("Hide Message") and carrier_file and (message_file or typed_message):
        carrier_bytes = carrier_file.read()
        combined_message = b""

        if message_file:
            combined_message += message_file.read()
        if typed_message:
            combined_message += typed_message.encode()

        # Message size check
        carrier_bits_len = len(carrier_bytes) * 8
        message_bits_len = len(file_to_bits(combined_message))

        if C == "fixed":
            embeddable_bits = (carrier_bits_len - S) // L
        else:
            embeddable_bits = (carrier_bits_len - S) // 17  # Average of 8, 16, 28

        if message_bits_len > embeddable_bits:
            st.error("❌ Message is too large to embed in the carrier with current parameters.")
            return

        stego = embed_message(carrier_bytes, combined_message, S, L, C)

        # Sanitize filename to prevent path traversal
        safe_name = os.path.basename(carrier_file.name)
        out_filename = os.path.join(UPLOAD_FOLDER, f"stego_{safe_name}")
        with open(out_filename, "wb") as f:
            f.write(stego)

        st.success("✅ Message embedded successfully!")
        st.download_button("Download Stego File", stego, file_name=f"stego_{safe_name}")

# Extract Page
def extract_page():
    st.title("🔓 Extract Hidden Message")
    stego = st.file_uploader("Upload Stego File")
    S = st.number_input("Starting Bit (S)", min_value=0, value=512, step=8)
    st.caption(f"🧠 Starting Bit ≈ {S / 8:.2f} bytes ({S / 8192:.2f} KB)")
    L = st.number_input("Periodicity (L)", min_value=1, value=8)
    C = st.selectbox("Mode (C)", options=["fixed", "cycle"])
    length = st.number_input("Message Length (in bytes)", min_value=1, value=10)
    st.caption(f"📦 Total bits = {length * 8} bits ({length / 1024:.2f} KB)")

    if st.button("Extract") and stego:
        stego_bytes = stego.read()
        extracted = extract_message(stego_bytes, S, L, C, length)
        st.download_button("Download Extracted Message", extracted, file_name="extracted_message.bin")

# Public Gallery
def gallery_page():
    st.title("🌍 Public Stego Gallery")
    files = [f for f in os.listdir(UPLOAD_FOLDER) if not f.startswith(".")]
    if not files:
        st.info("No files available yet.")
    for file in files:
        path = os.path.join(UPLOAD_FOLDER, file)
        st.write(f"📄 {file}")
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            st.image(path, use_container_width=True)
        with open(path, "rb") as f:
            data = f.read()
        st.download_button("Download", data, file_name=file)

# Sidebar Layout & Navigation
st.sidebar.title("🔧 Navigation")

page = st.sidebar.radio("Go to", ["Gallery", "Upload", "Extract"])

# Route pages
if page == "Gallery":
    gallery_page()
elif page == "Upload":
    upload_page()
elif page == "Extract":
    extract_page()
