# NMEA 0183 Bandwidth Calculator Help

## Overview
This console application helps you work with NMEA 0183 sentences. It provides two main functions:
1. Viewing detailed information about NMEA sentences
2. Calculating bandwidth usage for NMEA data streams

## Main Menu Options
1. Show sentence details
2. Calculate bandwidth
3. Show Help
4. Exit

## Sentence Information
- Displays a list of all available NMEA sentences
- Select a sentence by entering its ID
- Shows detailed information including:
  - Description
  - Sentence structure
  - Field details
  - Standard information
- Enter 'q' to return to main menu

## Bandwidth Calculator
- Select baud rate (4800 or 38400)
- Choose update rate (0.5Hz to 20Hz)
- Add sentences by entering their IDs
- Available commands:
  - Enter sentence ID to add it
  - 'r' to reset all selections
  - 'b' to change baud/update rates
  - 'c' to calculate final results
  - 'q' to return to main menu
- Real-time bandwidth display shows:
  - Selected sentences and lengths
  - Total bytes
  - Bandwidth usage percentage
  - Warning indicators for high usage

## Tips
- The bandwidth calculator shows real-time updates
- Progress bar colors indicate usage status:
  - Green: Normal usage
  - Yellow: High usage (>80%)
  - Red: Exceeded maximum (>100%)
- You can reset and recalculate with different rates
- Use 'q' to return to main menu from any screen 