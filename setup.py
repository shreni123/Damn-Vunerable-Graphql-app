import sys
import os
import shutil
import config
import random

from ipaddress import IPv4Network
SQLALCHEMY_FILE = f"{os.getcwd()}/dvga.db"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLALCHEMY_FILE}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

from app import db
from core.models import Paste, Owner, User, Audit

from db.agents import agents
from db.owners import owners
from db.titles import titles
from db.content import content

def clean_up():
  if os.path.exists(config.WEB_UPLOADDIR):
    shutil.rmtree(config.WEB_UPLOADDIR)
    os.mkdir(config.WEB_UPLOADDIR)
  else:
    os.mkdir(config.WEB_UPLOADDIR)

  print('Reconstructing Database')
  if os.path.exists(config.SQLALCHEMY_FILE):
    try:
      os.remove(config.SQLALCHEMY_FILE)
    except OSError:
      pass
  return

def random_title():
  return random.choice(titles)

def random_content():
  return random.choice(content)

def random_owner():
  return random.choice(owners)

def random_address():
  addresses = []
  for addr in IPv4Network('215.0.2.0/24'):
    addresses.append(str(addr))
  return random.choice(addresses)

def random_password():
  weak_passwords = ['changeme', 'password54321', 'letmein', 'admin123', 'iloveyou', '00000000']
  return random.choice(weak_passwords)

def random_useragent():
  user_agents = []
  for uas in agents:
    user_agents.append(uas)
  return random.choice(user_agents)

def pump_db():
  print('Populating Database')
  db.create_all()
  admin = User(username="admin", password=random_password())
  owner = Owner(name='DVGAUser')
  audit = Audit()
  paste = Paste()
  paste.title = random_title()
  paste.content = "My First Paste"
  paste.public = False
  paste.owner_id = owner.id
  paste.owner = owner
  paste.ip_addr = '127.0.0.1'
  paste.user_agent = 'User-Agent not set'
  audit.gqloperation = 'CreatePaste'
  db.session.add(admin)
  db.session.add(owner)
  db.session.add(paste)
  db.session.add(audit)

  for _ in range(0, 10 ):
    owner = Owner(name=random_owner())
    paste = Paste()
    paste.title = random_title()
    paste.content = random_content()
    paste.public = True
    paste.owner_id = owner.id
    paste.owner = owner
    paste.ip_addr = random_address()
    paste.user_agent = random_useragent()

    db.session.add(owner)
    db.session.add(paste)

  db.session.commit()

  print('done')

if __name__ == '__main__':
  clean_up()
  pump_db()
  sys.exit()