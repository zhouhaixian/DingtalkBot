import os.path
from time import sleep

import pyautogui
from rich.console import Console

pyautogui.PAUSE = 1
console = Console()

dingtalk_window_title = '钉钉'
delay = 60

live_icon_path = fr"{os.path.dirname(__file__)}\assets\Live.png"
live_window_border_screenshot_path = fr"{os.path.dirname(__file__)}\assets\LiveWindowBorder.png"
end_window_screenshot_path = fr"{os.path.dirname(__file__)}\assets\End.png"
close_icon_path = fr"{os.path.dirname(__file__)}\assets\Close.png"


def is_in_live():
    pyautogui.locateOnWindow(title=dingtalk_window_title, image=live_icon_path)  # 将钉钉窗口置于前台，否则下面的代码会得出None
    return pyautogui.locateOnWindow(title=dingtalk_window_title, image=live_icon_path) is not None


def enter_live():
    enter_live_button_position = pyautogui.locateOnWindow(title=dingtalk_window_title, image=live_icon_path)
    enter_live_button_center_position = pyautogui.center(enter_live_button_position)
    pyautogui.click(enter_live_button_center_position)


def is_watching_live():
    return pyautogui.locateCenterOnScreen(image=live_window_border_screenshot_path) is not None


def is_live_end():
    return pyautogui.locateCenterOnScreen(image=end_window_screenshot_path) is not None


def close_end_window():
    close_button_position = pyautogui.locateCenterOnScreen(close_icon_path)
    pyautogui.click(close_button_position)


if __name__ == '__main__':
    console.log("[bold blue]Please keep Dingtalk window at the front desk")
    while True:
        try:
            if is_watching_live():
                with console.status("[bold cyan]Watching Live") as status:
                    while is_watching_live():
                        sleep(delay)
            elif is_live_end():
                close_end_window()
                console.log('[bold red]Close the live end window')
                sleep(5)
            elif is_in_live():
                enter_live()
                console.log('[bold green]Enter the live room')
                sleep(5)
            else:
                with console.status("[bold blue]No live") as status:
                    while not is_in_live():
                        sleep(delay)
                        if is_watching_live():
                            break
        except Exception:
            console.print_exception(show_locals=True)
