from datetime import datetime
from django.core.management import call_command
import logging


logger = logging.getLogger(__name__)


def backup_database():
    try:
        call_command('dbbackup')
        logger.info(f'Created database backup at {datetime.now().strftime("%Y-%m-%d--%H-%M-%S")}')
    except:
        logger.info(f'Error in creation of database backup at {datetime.now().strftime("%Y-%m-%d--%H-%M-%S")}')


def print_message(message):
    logger.info(f'{message}')


def custom_backup_db():
    time = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    DB_NAME = 'tourist_agency'  # your db name
    DB_USER = 'admin' # you db user
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_PASSWORD = 'top1Dron'
    DB_BACKUP_FILE_NAME = f'default-{DB_USER}-{time}.psql'
    
    dump_success = 1
    logger.info(f'Backing up {DB_NAME} database')
    logger.info(os.environ['PG_DUMP'])
    command_for_dumping = f'{os.environ["PG_DUMP"]} ' \
                f'-h {DB_HOST} ' \
                f'-U {DB_USER} ' \
                f'{DB_NAME} ' \
                f'> "{os.path.join(settings.BACKUP_DIR, DB_BACKUP_FILE_NAME)}"'
    logger.info(command_for_dumping)
    try:
        proc = subprocess.Popen(command_for_dumping, shell=True, env={
                    'PGPASSWORD': f'{DB_PASSWORD}'
                    })
        proc.wait()

    except Exception as e:
            dump_success = 0
            logger.info('Exception happened during dump %s' %(e))


    if dump_success:
        logger.info('db dump successfull')