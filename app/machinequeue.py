import queue
import threading


class MachineQueue():
    def __init__(self, thread_num: int, callback_func):
        self.m_queue = queue.Queue()
        for i in range(thread_num):
            print("Creating thread")
            t = threading.Thread(target=process_queue, args=(self.m_queue, callback_func), daemon=True)
            # iterable as args, daemon threads will exit when program exits
            t.start()

    def put(self, machine_info):
        print("Put new machine into queue")
        self.m_queue.put(machine_info)

    def join(self):
        self.m_queue.join()


def process_queue(m_queue, cb):
    while True:
        machine_info = m_queue.get()
        cb(machine_info)
        m_queue.task_done()
