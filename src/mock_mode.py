"""
This module is for minicing Vercel environment.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/05/07 (initial version) ~ 2023/05/08 (last revision)"

import os


def init_environ_variables():
    print('init_environ_variables')

    os.environ[
        'SERVICE_ACCOUNT_INFO'] = 'SERVICE_ACCOUNT_INFO_TO_ACCESS_GOOGLE_DRIVE'

    os.environ['FOLDER_ID'] = 'ID_OF_THE_FOLDER_ON_THE_GOOGLE_DRIVE'

