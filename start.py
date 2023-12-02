"""
    Файл запуска бота для отладки, 
    чтобы шла перезагрузка проекта при каждом сохраненном изменении
"""
import logging
import subprocess
import sys
import signal

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.getLogger(__name__)


class PyHandler(FileSystemEventHandler):
    """Класс контроля изменений .py файлов  """

    def __init__(self):
        self.running_process = None
        self.start_script()

    def start_script(self):
        """Метод запуска скрипта"""
        if self.running_process:
            self.running_process.send_signal(signal.SIGINT)  # Завершение предыдущего процесса
        self.running_process = subprocess.Popen([sys.executable, 'bot.py'])  # Запуск нового процесса

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            self.start_script()


if __name__ == '__main__':
    event_handler = PyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    try:
        event_handler.start_script()
        observer.start()
    except (KeyboardInterrupt, SystemExit):
        observer.stop()

    observer.join()
