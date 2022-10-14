import queue
import threading


class MachineQueue():
    def __init__(self, thread_num: int, callback_func):
        self.m_queue = queue.Queue()
        self.m_threads = []
        self.stop_threads = threading.Event()
        for i in range(thread_num):
            print("Creating thread")
            t = threading.Thread(target=self.process_queue, args=(callback_func,), daemon=True)
            # iterable as args, daemon threads will exit when program exits
            t.start()
            self.m_threads.append(t)

    def put(self, machine_info):
        print("Put new machine into queue")
        self.m_queue.put(machine_info)

    def join(self):
        self.m_queue.join()
        print("Queue done")
        self.stop_threads.set()
        for t in self.m_threads:
            t.join()
        print("Threads terminated")

    def process_queue(self, cb):
        while not self.stop_threads.is_set():
            try:
                machine_info = self.m_queue.get(block=True, timeout=3)
            except queue.Empty:
                continue
            cb(machine_info)
            self.m_queue.task_done()

