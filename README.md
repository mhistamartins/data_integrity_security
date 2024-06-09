# data_integrity_security

This project implements a secure communication protocol for Arduino using RSA, AES, and HMAC for encryption, decryption, and message integrity verification. The protocol ensures secure key exchange and message transmission between the server (Arduino) and the client.

## Table of Contents

- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)

## Features

- **RSA-2048**: Asymmetric encryption for secure key exchange.
- **AES-256**: Symmetric encryption for secure data transmission.
- **HMAC-SHA256**: Message authentication code for ensuring message integrity.
- **LED Indicators**: Error indication using an LED connected to pin 21.
- **Random Number Generation**: Secure random number generation using mbedtls for keys and IVs.

## Hardware Requirements

- Arduino board (e.g., Arduino Uno, Arduino Mega)
- LED connected to pin 21 for error indication

## Software Requirements

- Arduino IDE
- mbedtls library

## Installation
