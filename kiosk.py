#!/usr/bin/python3
"""Script for running a webview window with a URL."""

import argparse
import sys
import webview

def main():
    # Default screen resolution
    resolution = [1920, 1080]
    
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', metavar='str', type=str, help='Site URL')
    parser.add_argument('--width', metavar='int', type=int, help='Screen width', default=resolution[0])
    parser.add_argument('--height', metavar='int', type=int, help='Screen height', default=resolution[1])
    parser.add_argument('--screen', metavar='int', type=int, help='Number of the screen', default=0)

    args = parser.parse_args()

    # Check if URL is provided
    if args.url is None:
        sys.exit("Error: You must provide a URL using --url <site>")

    url = args.url
    s_width = args.width
    s_height = args.height

    # Get the selected screen
    n_screen = webview.screens[args.screen]
    print(f"Using screen: {n_screen}")

    # Create and start the webview window
    webview.create_window('Hello world', url, fullscreen=True, width=s_width, height=s_height,
                        background_color="#000000", on_top=True, screen=n_screen)
    webview.start()

if __name__ == "__main__":
    main()
