# Cryptographic Utility Platform

The Cryptographic Utility Platform is an educational web-based application that integrates multiple cryptographic tools into a single, easy-to-use interface. It is designed to help students, developers, and security enthusiasts experiment with core cryptography concepts such as symmetric and asymmetric encryption, hashing, key management, and integrity verification without requiring deep command-line expertise. Built with Streamlit, the platform supports real-time encryption and decryption of files using AES, 3DES, and RSA; secure hash generation and comparison with SHA-3; automated password generation; and key exchange via Diffie–Hellman or RSA-2048.

The project provides a practical sandbox for understanding how different cryptographic primitives function in practice, demonstrating secure file handling workflows, and showcasing how complex cryptographic processes can be simplified with an intuitive interface.

> ⚠️ **Disclaimer:** This project is for **learning and demonstration** purposes only. Do not use it for production-grade security.

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Screens & Flow](#screens--flow)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Security Notes & TODOs](#security-notes--todos)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview
The **Cryptographic Utility Platform** offers:
- 🔐 File encryption/decryption with **AES, 3DES, and RSA**.
- 🔍 File hashing with **SHA-3** and hash comparison.
- 🔑 Key generation and sharing (RSA-2048, Diffie–Hellman).

---

## Key Features
- **Encryption/Decryption** — Encrypt files with AES (16/24/32-byte keys), 3DES (3×8-byte keys), or RSA.
- **Hashing & Integrity** — Generate SHA-3 hashes, compare file hashes, or verify file vs expected hash.
- **Key Management** — Generate RSA-2048 key pairs and perform Diffie–Hellman key exchange with shared key derivation (HKDF-SHA256).
- **Password Utility** — Generate strong random passwords and export them for reuse.
- **UI Simplicity** — Streamlit tabs separate functionality (Encryption, Decryption, Hashing, Key Generation, Comparison).

---

## How It Works
### Symmetric Encryption (AES/3DES)
- User provides a key (or generates one) and optionally an IV (for CBC mode).
- File data is padded, encrypted with the chosen cipher and mode, then offered for download.

### Asymmetric Encryption (RSA)
- Upload a `.pem` public key to encrypt a file.
- Upload a `.pem` private key to decrypt files.
- Uses RSA with OAEP + SHA-256 padding for secure operations.

### Hashing
- Compute **SHA3-256** digest of a file.
- Compare two files' hashes or file vs. a manually provided hash string.

### Key Generation
- **RSA**: Generate a 2048-bit key pair, download public/private PEM files.
- **Diffie–Hellman**: Generate private/public pairs, exchange, and compute a shared secret.

---

## Screens & Flow
1. **Encryption Tab** — Choose method, upload file, set keys/IV, encrypt.
2. **Decryption Tab** — Mirror of encryption; decrypt with provided keys.
3. **Hash Tab** — Upload file, compute SHA3-256 hash.
4. **Compare Tab** — Compare file vs. file or file vs. manual hash.
5. **Key Generation Tab** — Generate RSA or DH keys, export, and compute shared keys.

---

## Usage Guide
### Encryption
- Choose AES, 3DES, or RSA.
- Provide/generate a key and IV (for CBC).
- Upload file → encrypt → download.

### Decryption
- Mirror process: supply correct key/IV (or private key for RSA).

### Hashing
- Upload a file → compute SHA3-256 digest.
- Compare results to verify integrity.

### Key Generation
- Generate RSA key pair or DH keys.
- For DH, upload private/public pairs to compute a shared session key (via HKDF-SHA256).

---

## Project Structure
```
app.py                 # Streamlit application
requirements.txt       # Dependencies: streamlit, cryptography
```

---

## Tech Stack
- **Frontend/UX**: Streamlit
- **Backend**: Python
- **Crypto**: `cryptography` package (AES, 3DES, RSA, DH, HKDF, SHA3)

---

## Security Notes & TODOs
- 🔑 **Key export**: PEM files generated are not encrypted — add password protection for production use.
- 📦 **File size**: No enforced limits; add checks to avoid memory overload.
- 🚧 **Production hardening**: Add rate limiting and logging before any real deployment.

---

## Roadmap
- [ ] Extend hashing algorithms (SHA-2 family, BLAKE2)
- [ ] Add digital signatures (RSA/ECDSA)
- [ ] Support authenticated encryption modes (AES-GCM)
- [ ] Dockerfile + CI pipeline

---

## License
**Personal License** — Unauthorized copying, distribution, or commercial use is prohibited. For permissions, contact [sujalm7200@gmail.com](mailto:sujalm7200@gmail.com).
