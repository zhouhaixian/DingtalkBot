import os.path
from time import sleep

import pyautogui
import pygetwindow
from rich.console import Console

pyautogui.PAUSE = 1
console = Console()

dingtalk_window_title = '钉钉'
live_window_title = dingtalk_window_title
end_window_title = ''
delay = 60
interval = 5

live_icon_path = fr"{os.path.dirname(__file__)}\resource\Live.png"
live_window_border_screenshot_path = fr"{os.path.dirname(__file__)}\resource\LiveWindowBorder.png"
end_window_screenshot_path = fr"{os.path.dirname(__file__)}\resource\End.png"
check_in_button_screenshot_path = fr"{os.path.dirname(__file__)}\resource\CheckIn.png"
close_icon_path = fr"{os.path.dirname(__file__)}\resource\Close.png"


def make_dingtalk_window_on_front_desk():
    for window in pygetwindow.getWindowsWithTitle(dingtalk_window_title):
        if window.size == (160, 28):
            window.restore()
            sleep(interval)

        if window.size == (1024, 640):
            window.activate()
            sleep(interval)
            break


def make_live_window_on_front_desk():
    for window in pygetwindow.getWindowsWithTitle(live_window_title):
        match window.size:
            case (1920, 1080):
                window.activate()
                pyautogui.press('esc')
                sleep(interval)
                break
            case (1092, 588):
                window.activate()
                sleep(interval)
                break


def make_end_window_on_front_desk():
    for window in pygetwindow.getWindowsWithTitle(end_window_title):
        if window.size == (160, 28):
            window.restore()
            sleep(interval)

        if window.size == (480, 640):
            window.activate()
            sleep(interval)
            break


def is_in_live():
    make_dingtalk_window_on_front_desk()
    return pyautogui.locateCenterOnScreen(live_icon_path) is not None


def enter_live():
    make_dingtalk_window_on_front_desk()
    enter_live_button_position = pyautogui.locateCenterOnScreen(live_icon_path)
    pyautogui.click(enter_live_button_position)


def is_watching_live():
    make_live_window_on_front_desk()
    return pyautogui.locateCenterOnScreen(live_window_border_screenshot_path) is not None


def is_live_end():
    make_end_window_on_front_desk()
    return pyautogui.locateCenterOnScreen(end_window_screenshot_path) is not None


def close_end_window():
    make_end_window_on_front_desk()
    close_button_position = pyautogui.locateCenterOnScreen(close_icon_path)
    pyautogui.click(close_button_position)


def can_check_in():
    make_live_window_on_front_desk()
    return pyautogui.locateCenterOnScreen(check_in_button_screenshot_path) is not None


def check_in():
    make_live_window_on_front_desk()
    check_in_button_position = pyautogui.locateCenterOnScreen(check_in_button_screenshot_path)
    pyautogui.click(check_in_button_position)


if __name__ == '__main__':
    console.log("[bold blue]DingtalkBot find window by its size. Please do not change it")
    while True:
        try:
            pyautogui.moveTo(1, 1)
            if is_watching_live():
                with console.status("[bold cyan]Watching live") as status:
                    while is_watching_live():
                        if can_check_in():
                            check_in()
                            console.log('[bold green]Check in')
                        sleep(delay)
            elif is_live_end():
                close_end_window()
                console.log('[bold red]Close the live end window')
                sleep(interval)
            elif is_in_live():
                enter_live()
                console.log('[bold green]Enter the live room')
                sleep(interval)
            else:
                with console.status("[bold blue]No live") as status:
                    while not is_in_live():
                        sleep(delay)
                        if is_watching_live():
                            break
        except Exception:
            console.print_exception(show_locals=True)
