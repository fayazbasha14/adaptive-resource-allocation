import sys
import multiprocessing as mp
from PyQt6.QtWidgets import QApplication
from monitor import Monitor
from allocator import Allocator
from ui import UI


if __name__ == "__main__":
    mp.set_start_method("spawn")  

    app = QApplication(sys.argv)
    monitor = Monitor()
    allocator = Allocator()
    gui = UI(monitor, allocator)
    gui.show()
    sys.exit(app.exec())
