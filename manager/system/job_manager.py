import asyncio

from ..utils.log import log_exception


class JobManager:
    def __init__(self):
        self.job_queue = []
        self.on_job_added_callbacks = []
        self.on_job_finished_callbacks = []

    def bind_on_job_added(self, callback):
        self.on_job_added_callbacks.append(callback)

    def bind_on_job_finished(self, callback):
        self.on_job_finished_callbacks.append(callback)

    async def put(self, job):
        self.job_queue.append(job)
        for callback in self.on_job_added_callbacks:
            callback()

    async def worker(self):
        while True:
            if self.job_queue:
                job = self.job_queue.pop(0)
                try:
                    await job.execute()
                except Exception as e:
                    log_exception(e)
                try:
                    for callback in self.on_job_finished_callbacks:
                        callback()
                except Exception as e:
                    log_exception(e)
            await asyncio.sleep(0.05)
