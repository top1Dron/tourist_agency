from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from .tasks import regular_backup_database, task_hello

import os
import logging
import subprocess

logger = logging.getLogger(__name__)


def index(request):
    
    # with gzip.open(f'{settings.BACKUP_DIR}\\backup.gz', 'wb') as g:
        # os.system(f'pg_dump --host=localhost --port=5432 --username=admin --password=admin tourist_agency -w --clean > {settings.BACKUP_DIR}\\1.sql')
        # g.write(backup.out.encode('utf-8'))
    # regular_backup_database.delay()
    # task_hello.delay()
    return render(request, 'base.html', {})




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