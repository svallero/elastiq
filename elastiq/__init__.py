import sys, os
import logging, logging.handlers

from elastiq.config import Config, ConfigError


def config_log(log_directory):
  """Configures logging. Outputs log to the console and, optionally, to a file.
  File name is automatically selected. Returns the file name, or None if it
  cannot write to a file.
  """

  #format = '%(asctime)s [%(name)s.%(funcName)s] %(levelname)s %(message)s'
  format = '%(asctime)s [%(name)s] %(levelname)s %(message)s'
  datefmt = '%Y-%m-%d %H:%M:%S'
  level = 0

  # log to console
  logging.basicConfig(level=level, format=format, datefmt=datefmt, stream=sys.stdout)

  # silence boto errors
  #logging.getLogger('boto').setLevel(logging.CRITICAL)

  # log to file as well
  if log_directory is not None:
    filename = '%s/elastiq.log' % log_directory

    if not os.path.isdir(log_directory):
      os.makedirs(log_directory, 0755)

    log_file = logging.handlers.RotatingFileHandler(filename, mode='a', maxBytes=1000000, backupCount=30)
    log_file.setLevel(level)
    log_file.setFormatter( logging.Formatter(format, datefmt) )
    logging.getLogger('').addHandler(log_file)
    log_file.doRollover()  # rotate now: start from a clean slate
    return filename

  return None


def main(argv):

  config_defaults = {

    'elastiq': {

      # Main loop
      'sleep_s': 5,
      'check_queue_every_s': 15,
      'check_vms_every_s': 45,
      'check_vms_in_error_every_s': 20,
      'estimated_vm_deploy_time_s': 600,

      # Conditions to start new VMs
      'waiting_jobs_threshold': 0,
      'waiting_jobs_time_s': 40,
      'n_jobs_per_vm': 4,

      # Conditions to stop idle VMs
      'idle_for_time_s': 3600,

      # Batch plugin
      'batch_plugin': 'htcondor',

      # Log level (lower is more verbose)
      'log_level': 0

    },

    'substitute': {

      # Variables substituted in the user-data template.
      # If set, they have precedence on automatic detection.
      # In most cases you do not need to set them manually.
      'ipv4': None,
      'ipv6': None,
      'fqdn': None

    }

  }

  # logger for this module
  logger = logging.getLogger(__name__)

  # configures logging for all
  logdir = '/tmp/elastiq_log'
  try:
    config_log(logdir)
  except (OSError, IOError) as e:
    logger.warn('Cannot log to dir %s: %s' % (logdir, e))

  # config
  cffile = 'etc/elastiq.conf.example'
  try:
    cf = Config(cffile, config_defaults)
  except ConfigError as e:
    logger.critical( e )
    return 1

  # smooth exit
  return 0