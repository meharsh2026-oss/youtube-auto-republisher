"""Scheduler service for automatic uploads"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    """Service for scheduling uploads"""
    
    def __init__(self):
        """Initialize scheduler"""
        self.scheduler = BackgroundScheduler()
    
    def start(self):
        """Start scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info('Scheduler started')
    
    def stop(self):
        """Stop scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info('Scheduler stopped')
    
    def add_job(self, func, interval_hours, job_id=None):
        """Add scheduled job"""
        try:
            self.scheduler.add_job(
                func,
                IntervalTrigger(hours=interval_hours),
                id=job_id,
                replace_existing=True
            )
            logger.info(f'Job added: {job_id}')
        except Exception as e:
            logger.error(f'Error adding job: {str(e)}')
    
    def remove_job(self, job_id):
        """Remove scheduled job"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f'Job removed: {job_id}')
        except Exception as e:
            logger.error(f'Error removing job: {str(e)}')
