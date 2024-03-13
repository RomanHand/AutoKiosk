#!/usr/bin/python3
import webview
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', metavar='str', type=str, help='site url')
    parser.add_argument('--width', metavar='int', type=int, help='width screen', default=1920)
    parser.add_argument('--height', metavar='int', type=int, help='height screen', default=1080)

    args = parser.parse_args()
    if args.url == None:
        exit("use --url <site>")
    url = args.url
    s_width = args.width
    s_height = args.height
    webview.create_window('Hello world', url, fullscreen=True, width=s_width, height=s_height,  background_color="#000000" )
    webview.start()

main()
