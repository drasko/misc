import multiprocessing
import worker

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker.main)
        jobs.append(p)
        p.start()
