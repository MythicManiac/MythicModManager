import asyncio

from ..utils.log import log_exception


class JobManager:
    def __init__(self, big_progress_bar, small_progress_bar):
        self.job_queue = []
        self.big_progress_bar = big_progress_bar
        self.small_progress_bar = small_progress_bar
        self.on_job_added_callbacks = []
        self.on_job_finished_callbacks = []
        self.current_batch_size = 0

    def bind_on_job_added(self, callback):
        self.on_job_added_callbacks.append(callback)

    def bind_on_job_finished(self, callback):
        self.on_job_finished_callbacks.append(callback)

    async def put(self, job):
        self.job_queue.append(job)
        self.current_batch_size = len(self.job_queue)
        for callback in self.on_job_added_callbacks:
            callback()

    async def update_big_progress_bar(self):
        completed_tasks = self.current_batch_size - len(self.job_queue)
        percentage = float(completed_tasks) / self.current_batch_size
        self.big_progress_bar.SetValue(percentage * 1000)

    async def worker(self):
        while True:
            try:
                await self.worker_loop()
            except Exception as e:
                log_exception(e)
            await asyncio.sleep(0.05)

    async def worker_loop(self):
        while True:
            if self.job_queue:
                job = self.job_queue.pop(0)
                self.small_progress_bar.SetValue(0)
                await job.execute(self.small_progress_bar)
                self.small_progress_bar.SetValue(1000)
                await self.update_big_progress_bar()
                for callback in self.on_job_finished_callbacks:
                    callback()
            await asyncio.sleep(0.05)
