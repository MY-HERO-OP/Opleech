import sys

from base64 import b64decode
from dotenv import load_dotenv, dotenv_values
from logging import FileHandler, StreamHandler, basicConfig, error as log_error, info as log_info, INFO
from os import path as ospath, environ, remove
from pymongo import MongoClient
from re import sub as resub
from requests import get as rget
from subprocess import run as srun


if ospath.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

if ospath.exists('rlog.txt'):
    remove('rlog.txt')

basicConfig(format='%(asctime)s: [%(levelname)s: %(filename)s - %(lineno)d] ~ %(message)s',
            handlers=[FileHandler('log.txt'), StreamHandler()],
            datefmt='%d-%b-%y %I:%M:%S %p',
            level=INFO)

load_dotenv('config.env', override=True)

BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

bot_id = BOT_TOKEN.split(':', 1)[0]

DATABASE_URL = environ.get('DATABASE_URL', '')
if len(DATABASE_URL) == 0:
    DATABASE_URL = None

if DATABASE_URL:
    conn = MongoClient(DATABASE_URL)
    db = conn.luna
    if config_dict := db.settings.config.find_one({'_id': bot_id}):
        environ['UPSTREAM_REPO'] = config_dict['UPSTREAM_REPO']
        environ['UPSTREAM_BRANCH'] = config_dict['UPSTREAM_BRANCH']
    conn.close()

UPSTREAM_REPO = environ.get('UPSTREAM_REPO', '')
if len(UPSTREAM_REPO) == 0:
    UPSTREAM_REPO = 'https://github.com/MY-HERO-OP/test'

UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', '')
if len(UPSTREAM_BRANCH) == 0:
    UPSTREAM_BRANCH = 'main'

if path.exists('.git'):
    run(["rm", "-rf", ".git"])

update = run([f"git init -q \
                 && git config --global user.email yesiamshojib@gmail.com \
                 && git config --global user.name 5hojib \
                 && git add . \
                 && git commit -sm update -q \
                 && git remote add origin {UPSTREAM_REPO} \
                 && git fetch origin -q \
                 && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)

if update.returncode == 0:
    info('Successfully updated with latest commit from UPSTREAM_REPO')
else:
    error('Something went wrong while updating, check UPSTREAM_REPO if valid or not!')
