"""
    Launcher
"""

import subprocess
import signal

class Launch:
    def __init__(self, command):
        self.command = command
        self.shell = False  # or True?? is it needed?

    def start(self):
        self.running = subprocess.Popen(self.command, shell=self.shell)

    def quit(self):
        self.running.send_signal(signal.SIGINT)
        try:
            self.running.wait(1)
        except subprocess.TimeoutExpired:
            command = self.command if isinstance(self.command, str) else " ".join(self.command)
            print(f"'{command}' still running, terminating")
            self.running.terminate()
            try:
                self.running.wait(1)
            except subprocess.TimeoutExpired:
                print(f"'{command}' ignoring SIGTERM, killing")
                self.running.kill()
                self.running.wait()

        return self.running.poll()

if __name__ == "__main__":
    import time
    test_quit = Launch(['sleep', '10'])
    test_quit.start()
    print("To be terminated...")
    time.sleep(2)
    test_quit.quit()
    
