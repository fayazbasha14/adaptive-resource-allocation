from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer


class UI(QWidget):
    def __init__(self, monitor, allocator):
        super().__init__()
        self.monitor = monitor
        self.alloc = allocator

        self.setWindowTitle("Adaptive Resource Allocator (Windows)")
        layout = QVBoxLayout(self)

        self.lbl_sys = QLabel("CPU: --  MEM: --")
        layout.addWidget(self.lbl_sys)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["PID", "Type", "CPU%", "Mem(MB)"])
        layout.addWidget(self.table)

        btns = QHBoxLayout()
        self.btn_cpu = QPushButton("Start CPU Job")
        self.btn_mem = QPushButton("Start Memory Job")
        self.btn_toggle = QPushButton("Pause/Resume")
        btns.addWidget(self.btn_cpu)
        btns.addWidget(self.btn_mem)
        btns.addWidget(self.btn_toggle)
        layout.addLayout(btns)

        self.btn_cpu.clicked.connect(lambda: self.monitor.launch("CPU"))
        self.btn_mem.clicked.connect(lambda: self.monitor.launch("MEM"))
        self.btn_toggle.clicked.connect(self.toggle)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)

    def refresh(self):
        jobs, sysd = self.monitor.collect()
        self.lbl_sys.setText(f"CPU: {sysd['cpu']}%   MEM: {sysd['mem']}%")

        acts = self.alloc.decide(self.monitor, jobs, sysd)
        if acts:
            print(" | ".join(acts))

        self.table.setRowCount(len(jobs))
        for i, j in enumerate(jobs):
            self.table.setItem(i, 0, QTableWidgetItem(str(j["pid"])))
            self.table.setItem(i, 1, QTableWidgetItem(j["type"]))
            self.table.setItem(i, 2, QTableWidgetItem(f"{j['cpu']:.1f}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{j['mem']:.1f}"))

    def toggle(self):
        row = self.table.currentRow()
        if row < 0: return
        pid = int(self.table.item(row, 0).text())
        job = self.monitor.find(pid)
        if job.state == "RUNNING": job.pause()
        else: job.resume()
