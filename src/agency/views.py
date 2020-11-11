from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from .tasks import regular_backup_database, task_hello

import delegator
import gzip
import os
import logging
import subprocess

logger = logging.getLogger(__name__)


def index(request):
    time = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    # with gzip.open(f'{settings.BACKUP_DIR}\\backup.gz', 'wb') as g:
        # os.system(f'pg_dump --host=localhost --port=5432 --username=admin --password=admin tourist_agency -w --clean > {settings.BACKUP_DIR}\\1.sql')
        # g.write(backup.out.encode('utf-8'))

    # _backup_db(time)
    # regular_backup_database.delay()
    task_hello.delay(time)
    return render(request, 'base.html', {})





def _backup_db(time):
    DB_NAME = 'tourist_agency'  # your db name
    DB_USER = 'admin' # you db user
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_PASSWORD = 'admin'
    # your db password
    # pg_dump -h localhost -U admin tourist_agency > backup.sql
    dump_success = 1
    logger.info(f'Backing up {DB_NAME} database')
    logger.info(os.environ['PG_DUMP'])
    command_for_dumping = f'{os.environ["PG_DUMP"]} ' \
                f'-h {DB_HOST} ' \
                f'-U {DB_USER} ' \
                f'{DB_NAME} ' \
                f'> "{settings.BACKUP_DIR}\\{time}.sql"'
    logger.info(command_for_dumping)
    try:
        proc = subprocess.Popen(command_for_dumping, shell=True, env={
                    'PGPASSWORD': 'top1Dron'
                    })
        proc.wait()

    except Exception as e:
            dump_success = 0
            logger.info('Exception happened during dump %s' %(e))


    if dump_success:
        logger.info('db dump successfull')
#  print(' restoring to a new database database')

#  """database to restore dump must be created with 
# the same user as of previous db (in my case user is 'postgres'). 
# i have #created a db called ReplicaDB. no need of tables inside. 
# restore process will #create tables with data.
# """

# backup_file = '/home/Downloads/BlogTemplate/BlogTemplate/backup.dmp' 
# """give absolute path of your dump file. This script will create the backup.dmp in the same directory from which u are running the script """



# if not dump_success:
#     print('dump unsucessfull. retsore not possible')
#  else:
#     try:
#         process = subprocess.Popen(
#                         ['pg_restore',
#                          '--no-owner',
#                          '--dbname=postgresql://{}:{}@{}:{}/{}'.format('postgres',#db user
#                                                                        'sarath1996', #db password
#                                                                        'localhost',  #db host
#                                                                        '5432', 'ReplicaDB'), #db port ,#db name
#                          '-v',
#                          backup_file],
#                         stdout=subprocess.PIPE
#                     )
#         output = process.communicate()[0]

#      except Exception as e:
#            print('Exception during restore %e' %(e) )