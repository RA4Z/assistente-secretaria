# Automated Indicator Update System

## Overview

This Python-based system is designed to streamline and automate the process of updating daily, weekly, and monthly indicators for PPC WEG Energy department secretaries.  By leveraging the Flet framework for the GUI and integrating AI for intelligent automation, this system aims to significantly enhance efficiency and minimize manual effort.

## Key Features

- **User-Friendly Interface:** An intuitive graphical user interface built with Flet allows secretaries to easily navigate and select the indicators they need to update.
- **AI-Powered Procedure Retrieval:**  Upon indicator selection, the system's AI engine automatically retrieves and parses the corresponding procedure document.
- **Dynamic Checklist Generation:** The AI converts the extracted procedure into a standardized format and dynamically generates a checklist of actionable steps, presented as checkboxes within the Flet interface.
- **Real-time Status Visualization:**  Color-coding provides clear visual feedback on the update status. Completed indicators are marked green, while pending ones are highlighted in yellow.
- **Confirmation Mechanism:**  A dedicated button allows secretaries to confirm the completion of all steps, ensuring accurate tracking and management of indicator updates.

## Technology Stack

- **Python:**  Core system logic and functionality.
- **Flet:**  GUI development framework for a responsive and user-friendly interface.
- **AI Studio:**  AI that manipulates the procedures and give a formated string to the code

## Installation and Setup

1. **Clone the Repository:** `git clone https://github.com/RA4Z/assistente-secretaria.git`
2. **Navigate to Project Directory:** `cd assistente-secretaria`
3. **Install Dependencies:** `pip install ...`
4. **(AI Setup):** Create an Environment Variable called "GEMINI_API" and put your Gemini API Key https://aistudio.google.com/app/apikey

## Usage

1. **Run the Application:** `python main.py`
2. **Select Indicator:** Choose the desired indicator from the Flet GUI.
3. **Follow Checklist:**  The system will present a dynamic checklist of steps for updating the selected indicator. Mark each step as complete.
4. **Confirm Completion:** Click the confirmation button once all steps are finished. 
