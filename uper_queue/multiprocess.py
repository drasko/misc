import multiprocessing
import worker1, worker2
import uperd

if __name__ == '__main__':
    qin = multiprocessing.Queue()
    qout = multiprocessing.Queue()

    sem = multiprocessing.BoundedSemaphore(2)

    u = uperd.Uperd(qin, qout, sem)
    u.start() 

    p = multiprocessing.Process(target=worker1.main, args=(qin, qout, sem))
    p.start()

    p = multiprocessing.Process(target=worker2.main, args=(qin, qout, sem))
    p.start()

