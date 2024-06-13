# 🌱Bio-Bubble🫧

## Overview
BioBubble.py is a Python script designed to manage and monitor the environmental conditions of plants under a protective cover, referred to as the "Bio Bubble". This project is part of the Smart Agriculture domain, focusing on optimizing conditions in greenhouses through IoT technologies.

### 📽️ Watch our DEMO video!!
Follow this link

## 🗒️ Features
- **Data Collection**: Gathers real-time data on temperature, humidity, and light levels.
- **Display Output**: Information is displayed on an LCD screen for easy monitoring.
- **Remote Monitoring**: Integrates with ThingsBoard for remote data visualization and management.
- **Alert System**: Notifies the user with visual and audible alerts when the plant requires watering.

## ⚒️ System Requirements
To run BioBubble.py, ensure that the following Python libraries and modules are installed:

- time
- sys
- os
- grovepi
- math
- json
- grove.factory
- paho.mqtt
- grove_rgb_lcd


## 📐Hardware Requirements
• 𝗜𝗻𝗽𝘂𝘁 𝗡𝗼𝗱𝗲𝘀: Grove Temperature & Humidity Sensor, Grove-Light Sensor v1.2, and Grove-Red LED Button.

• 𝗢𝘂𝘁𝗽𝘂𝘁 𝗡𝗼𝗱𝗲𝘀: Grove-Buzzer and Grove-LCD RGB Backlight.


## 👩🏽‍💻 Installation
1. Clone the repository to your local machine or directly to your IoT device (RasberryPi).
2. Install required dependencies:
   
   ```bash
   pip install grovepi
   ```
   
3. Connect the hardware sensors and actuators according to the Grove system specifications.
4. Configure the ThingsBoard access token and host details in the script.

## 🗃️ Project Structure
- **bioBubble.py**: Main Python script for system operation including data collection, user interface, and remote communication.
- **config.json**: Configuration file for storing sensitive information like ThingsBoard credentials (optional for enhanced security).

## 🌱 IoT System Description
The Bio Bubble IoT system encapsulates a plant under a plastic dome, creating a controlled micro-environment that simulates ideal growing conditions. This system includes:

- **Input Nodes**: Sensors for monitoring environmental conditions.
- **Output Nodes**: Devices for user interaction and alerts.

Data is cyclically displayed on the LCD, switching between temperature, humidity, and light levels. Light levels are displayed using predefined thresholds to indicate sufficient or insufficient light. A push button allows users to reset the watering timer, which prompts alerts when the plant hasn't been watered in two weeks.
