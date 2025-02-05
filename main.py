import os
import psutil
import shutil
import logging
import schedule
import time
import requests
from datetime import datetime

class DevOpsAutomation:
    def __init__(self, log_file='devops_automation.log'):
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger()

    def system_health_check(self):
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            self.logger.info(f"CPU Usage: {cpu_usage}%")

            memory = psutil.virtual_memory()
            self.logger.info(f"Memory Usage: {memory.percent}%")

            disk = psutil.disk_usage('/')
            self.logger.info(f"Disk Usage: {disk.percent}%")

            net_connections = len(psutil.net_connections())
            self.logger.info(f"Active Network Connections: {net_connections}")

            return {
                'cpu_usage': cpu_usage,
                'memory_usage': memory.percent,
                'disk_usage': disk.percent,
                'network_connections': net_connections
            }
        except Exception as e:
            self.logger.error(f"System health check failed: {e}")
            return None

    def backup_directory(self, source_dir, backup_dir):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
            
            shutil.copytree(source_dir, backup_path)
            self.logger.info(f"Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
            return None

    def monitor_log_files(self, log_directory, error_threshold=10):
        try:
            error_count = 0
            for filename in os.listdir(log_directory):
                if filename.endswith('.log'):
                    with open(os.path.join(log_directory, filename), 'r') as log_file:
                        error_count += sum(1 for line in log_file if 'ERROR' in line)
            
            if error_count > error_threshold:
                self.logger.warning(f"High error count detected: {error_count} errors")
            
            return error_count
        except Exception as e:
            self.logger.error(f"Log monitoring failed: {e}")
            return None

    def check_external_service(self, url, timeout=5):
        try:
            response = requests.get(url, timeout=timeout)
            status = response.status_code == 200
            self.logger.info(f"Service {url} status: {'Online' if status else 'Offline'}")
            return status
        except requests.RequestException as e:
            self.logger.error(f"Service check failed for {url}: {e}")
            return False

def main():
    devops_automation = DevOpsAutomation()

    devops_automation.system_health_check()

    schedule.every(1).hour.do(devops_automation.system_health_check)
    schedule.every(6).hours.do(devops_automation.backup_directory, 
                                source_dir='/path/to/important/data', 
                                backup_dir='/path/to/backup/location')
    schedule.every(1).day.do(devops_automation.monitor_log_files, 
                              log_directory='/var/log')
    schedule.every(15).minutes.do(devops_automation.check_external_service, 
                                   url='https://example.com')

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
