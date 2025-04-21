#!/usr/bin/python3
import webview
import argparse
import screeninfo

def main():
    resolution = [1920, 1080]
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', metavar='str', type=str, help='site url')
    parser.add_argument('--width', metavar='int', type=int, help='width screen',
                        default=resolution[0])
    parser.add_argument('--height', metavar='int', type=int, help='height screen',
                        default=resolution[1])
    parser.add_argument('--screen', metavar='int', type=int, help='number screen', default=0)

    args = parser.parse_args()
    if args.url == None:
        exit("use --url <site>")
    url = args.url
    s_width = args.width
    s_height = args.height


    n_screen = webview.screens[args.screen]
    print(n_screen)
    webview.create_window('Hello world', url, fullscreen=True, width=s_width, height=s_height,
                        background_color="#000000", 
                        on_top=True, screen=n_screen)
    webview.start()

main()
