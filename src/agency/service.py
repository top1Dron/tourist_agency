from django.core.management import call_command
import logging

def backup_database():
    try:
        call_command('dbbackup')
        logger.info(f'Created database backup at {datetime.now().strftime("%Y-%m-%d--%H-%M-%S")}')
    except:
        logger.info(f'Error in creation of database backup at {datetime.now().strftime("%Y-%m-%d--%H-%M-%S")}')


def print_message(message):
    logger.info(f'{message}')