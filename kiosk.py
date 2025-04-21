#!/usr/bin/python3

"""Script for running a webview window with a URL."""
import webview
import argparse
from screeninfo import get_monitors

def get_screen_resolution(n_screen):
    screen_info = get_monitors()[n_screen]
    return [screen_info.width, screen_info.height, screen_info.x, screen_info.y]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', metavar='str', type=str, help='site url')
    parser.add_argument('--urls', metavar='str', nargs='+', help='list of site urls')
    parser.add_argument('--screen', metavar='int', type=int, help='screen number', default=0)
    args = parser.parse_args()

    # Сбор url'ов
    if args.url:
        urls = [args.url]
    elif args.urls:
        urls = args.urls
    else:
        exit("use --url <site> or --urls <site1> <site2> ...")

    n_screen = args.screen
    width, height, x_offset, y_offset = get_screen_resolution(n_screen)

    tile_width = width // len(urls)

    for i, url in enumerate(urls):
        x = x_offset + i * tile_width
        webview.create_window(
            f'Window {i+1}',
            url,
            fullscreen=False,
            width=tile_width,
            height=height,
            x=x,
            y=y_offset,
            background_color="#000000",
            on_top=False,
            frameless=True
        )
    webview.start()
main()
