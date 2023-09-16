import os
import logging
import re
import pytz
import pyautogui
import asyncio
import keyboard
import pyperclip
import configparser
import time
import random
import pandas as pd
import textwrap
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageDraw, ImageFont

# Automatic maintenance launcher
from keep_alive import keep_alive

# Determine the Kyrgyzstan timezone offset from UTC
kyrgyzstan_offset_hours = 6

# Web settings
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=800,800')

# Function to log in to Instagram
def login_to_instagram():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.instagram.com/")
    action = webdriver.ActionChains(driver)
    driver.implicitly_wait(20)

    username = driver.find_element_by_name('username').send_keys(os.environ['USERNAME'])
    password = driver.find_element_by_name('password').send_keys(os.environ['PASSWORD'])
    login = driver.find_element_by_xpath("//button[@class='_acan _acap _acas _aj1-']").click()

    return driver

# Function to perform the Instagram post
def perform_instagram_post(driver):
    post = driver.find_element_by_xpath("//*[@aria-label='New post']").click()
    select = driver.find_element_by_xpath("//button[text()='Select from computer']").click()
    time.sleep(10)
    pyautogui.typewrite("/home/runner/instagrambot/out_image/1.png")
    pyautogui.press('enter')

    time.sleep(5)
    next_button = driver.find_element_by_xpath("//div[text()='Next']").click()
    time.sleep(5)
    next_button = driver.find_element_by_xpath("//div[text()='Next']").click()
    time.sleep(5)
    next_button = driver.find_element_by_xpath("//div[text()='Share']").click()
    time.sleep(5)
    close_post = driver.find_element_by_xpath("//*[@aria-label='Close']").click()

# Function to generate and post images
def generate_and_post_image():
    # Define paths to folders and files
    image_folder = 'images'
    data_folder = 'data'
    font_folder = 'font'
    output_folder = 'out_image'

    image_path = os.path.join(image_folder, '1.png')
    data_path = os.path.join(data_folder, 'data.csv')
    font_path = os.path.join(font_folder, 'font.ttf')
    output_path = os.path.join(output_folder, '1.png')

    # Load data from CSV
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"File not found: {data_path}")
        exit(1)

    # Check if the output folder exists, create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Check if there are quotes left
    if len(df) == 0:
        print("No more quotes to generate.")
        exit(0)

    # Randomly select a quote and remove it from the DataFrame
    selected_index = random.randint(0, len(df) - 1)
    selected_quote = df.iloc[selected_index]
    df = df.drop(selected_index)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(data_path, index=False)

    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Load the font
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)

    # Define text position (centered horizontally with a 50-pixel right shift)
    text_x = 150  # X-coordinate adjusted to move the text 50 pixels to the right

    # Wrap text to fit within the image width
    max_width = image.width - text_x
    wrapped_text = textwrap.fill(selected_quote['Quote'], width=30)  # Adjust the width as needed

    # Calculate the height needed for the wrapped text
    text_height = len(wrapped_text.split('\n')) * font_size

    # Center the wrapped text vertically
    text_y = (image.height - text_height) // 2

    # Add wrapped text to the image
    draw.text((text_x, text_y), wrapped_text, fill='white', font=font)

    # Save the modified image
    image.save(output_path)

    print(f"Generated image saved to {output_path}")

# Login to Instagram
driver = login_to_instagram()

# Start the keep_alive function to keep the bot running
keep_alive()

# Schedule the Instagram post for 20:55 in Kyrgyzstan time
while True:
    current_time_kyrgyzstan = datetime.datetime.utcnow() + datetime.timedelta(hours=kyrgyzstan_offset_hours)
    if current_time_kyrgyzstan.hour == 21 and current_time_kyrgyzstan.minute == 25:
        # Perform the Instagram post
        perform_instagram_post(driver)

        # Sleep for a day to prevent multiple executions on the same day
        time.sleep(86400)  # 86400 seconds in a day (24 hours)
    else:
        # Sleep for a while before checking the time again
        time.sleep(60)  # Sleep for 60 seconds (1 minute)

# Schedule image generation and posting for 20:20 in Kyrgyzstan time
while True:
    current_time_kyrgyzstan = datetime.datetime.utcnow() + datetime.timedelta(hours=kyrgyzstan_offset_hours)
    if current_time_kyrgyzstan.hour == 21 and current_time_kyrgyzstan.minute == 20:
        # Generate and post the image
        generate_and_post_image()

        # Sleep for a day to prevent multiple executions on the same day
        time.sleep(86400)  # 86400 seconds in a day (24 hours)
    else:
        # Sleep for a while before checking the time again
        time.sleep(60)  # Sleep for 60 seconds (1 minute)