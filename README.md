<div align="center">

<p align="center">
   <img src="docs/images/logo.png" alt="DaiNam University Logo" width="200"/>
</p>

[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-red?style=for-the-badge)](https://dainam.edu.vn)

</div>

# 🔐 Secure Email Transmission System

A robust cryptographic solution for secure email transmission using hybrid encryption combining RSA and AES algorithms. This system ensures data confidentiality, integrity, and authenticity when sending sensitive email content.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Security Architecture](#security-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements a **hybrid cryptographic system** that combines the security of RSA public-key cryptography with the efficiency of AES symmetric encryption. The system is designed to securely transmit email content between parties while ensuring:

- **Confidentiality**: Data is encrypted and can only be read by intended recipients
- **Integrity**: Detection of any tampering or corruption during transmission
- **Authenticity**: Verification of sender identity through digital signatures
- **Non-repudiation**: Cryptographic proof of message origin

## ✨ Features

### 🔒 Hybrid Encryption
- **RSA-2048** for secure key exchange
- **AES-256-CBC** for efficient data encryption
- Automatic session key generation for each transmission

### 🛡️ Security Mechanisms
- **Digital Signatures** using RSA with SHA-512 hashing
- **Message Authentication** through SHA-512 hash verification
- **Timestamp Validation** with configurable expiration periods
- **PKCS#1 v1.5 Padding** for RSA operations

### 📦 Packet Structure
- JSON-based secure packet format
- Base64 encoding for binary data transport
- Metadata embedding with timestamp information
- Comprehensive error handling and validation

## 🏗️ Security Architecture

### Encryption Flow
```
1. Generate RSA key pairs for sender and receiver
2. Create AES session key + IV for each message
3. Encrypt email content with AES-CBC
4. Encrypt session key with receiver's RSA public key
5. Sign metadata with sender's RSA private key
6. Create integrity hash of encrypted data
7. Package everything into secure JSON packet
```

### Decryption Flow
```
1. Verify packet expiration timestamp
2. Validate sender's digital signature
3. Decrypt session key using receiver's private key
4. Verify data integrity through hash comparison
5. Decrypt email content using AES session key
6. Send acknowledgment (ACK/NACK) to sender
```

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- `cryptography` library

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/secure-email-transmission.git
cd secure-email-transmission

# Install dependencies
pip install cryptography

# Generate RSA key pairs
python generate_keys.py
```

## 🚀 Usage

### 1. Generate Cryptographic Keys
```bash
python generate_keys.py
```
This creates four key files:
- `sender_private.pem` - Sender's private key
- `sender_public.pem` - Sender's public key  
- `receiver_private.pem` - Receiver's private key
- `receiver_public.pem` - Receiver's public key

### 2. Prepare Email Content
Create an `email.txt` file with your message content:
```
Subject: Confidential Business Proposal
Dear Recipient,
This is a secure email transmission...
```

### 3. Send Encrypted Email
```bash
python sender.py
```
This will:
- Encrypt your email content
- Create a secure packet (`packet.json`)
- Display transmission status

### 4. Receive and Decrypt
```bash
python receiver.py
```
This will:
- Validate the received packet
- Decrypt the email content
- Save to `received_email.txt`
- Send ACK/NACK response

## 📁 File Structure

```
secure-email-transmission/
├── generate_keys.py      # RSA key pair generation
├── sender.py            # Email encryption and transmission
├── receiver.py          # Email decryption and validation
├── email.txt           # Original email content (input)
├── packet.json         # Encrypted transmission packet
├── received_email.txt  # Decrypted email content (output)
├── sender_private.pem  # Sender's private key
├── sender_public.pem   # Sender's public key
├── receiver_private.pem # Receiver's private key
├── receiver_public.pem # Receiver's public key
└── README.md          # This documentation
```

### Key Components

#### `generate_keys.py`
- Generates RSA-2048 key pairs for both sender and receiver
- Saves keys in PEM format for cross-platform compatibility
- Uses secure random number generation

#### `sender.py`
- Implements hybrid encryption workflow
- Performs digital signing for authentication
- Creates timestamped, integrity-protected packets
- Handles session key generation and encryption

#### `receiver.py`
- Validates packet expiration and integrity
- Verifies digital signatures for authenticity
- Decrypts session keys and message content
- Provides comprehensive error handling with specific NACK codes

## 🔐 Security Considerations

### Cryptographic Strengths
- **RSA-2048**: Provides robust public-key security
- **AES-256**: Industry-standard symmetric encryption
- **SHA-512**: Strong cryptographic hashing
- **CBC Mode**: Secure block cipher mode with IV

### Best Practices Implemented
- ✅ Unique session keys for each transmission
- ✅ Random IV generation for each encryption
- ✅ Timestamp-based expiration validation
- ✅ Comprehensive integrity checking
- ✅ Digital signature verification

### Security Recommendations
- 🔒 Store private keys securely (consider HSM for production)
- 🔄 Implement regular key rotation policies
- 📊 Monitor and log all cryptographic operations
- 🛡️ Use secure channels for public key distribution
- ⏰ Set appropriate expiration timeframes

### Known Limitations
- Uses PKCS#1 v1.5 padding (consider upgrading to OAEP)
- No forward secrecy (consider implementing ephemeral keys)
- Basic timestamp validation (consider NTP synchronization)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive tests for new features
- Update documentation for any changes
- Ensure backward compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with the excellent [cryptography](https://cryptography.io/) library
- Inspired by modern secure communication protocols
- Thanks to the open-source cryptography community

## 📞 Support

For questions, issues, or contributions:
- 📧 Contact: khuongdang.pham04@gmail.com

---

**⚠️ Security Notice**: This implementation is for educational and development purposes. For production use, please conduct thorough security audits and consider additional enterprise-grade security measures.
