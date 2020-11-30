import argparse
import sys
import os
import logging
import logging.config
from lib.minioclient import MinioClient
import yaml
import time
import datetime
from enum import Enum
import requests

SSL_CERT_FILE="SSL_CERT_FILE"

logger = logging.getLogger("gha2minio.main")

def error(message, *args):
    x = "" + message.format(*args)
    print("* * * * * ERROR: {}".format(x))
    exit(1)


def main():
    mydir = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', required=True)
    parser.add_argument('--accessKey', required=True)
    parser.add_argument('--secretKey', required=True)
    parser.add_argument('--bucketFormat', default="gha2minio-{year:04d}")
    parser.add_argument('--objectFormat', default="{year:04d}/{month:02d}/{day:02d}/{hour:02d}.json.gz")
    parser.add_argument('--backDays', type=int, default=1)
    parser.add_argument('--tolerationHours', type=int, default="6")
    parser.add_argument('--maxDownloads', type=int, default="1000000")
    parser.add_argument('--waitSeconds', type=int, default="0")          # Wait between exec in an infinite loop. If 0, only one shot. (To be used in cronjob)
    parser.add_argument('--ca', type=str)    # Certificate authority file path.
    parser.add_argument('--workDir', type=str, default="/data")

    params = parser.parse_args()

    logging_conf_file = os.path.join(mydir, "./logging.yml")
    logging.config.dictConfig(yaml.load(open(logging_conf_file), Loader=yaml.SafeLoader))

    if params.ca:
        os.environ[SSL_CERT_FILE] = params.ca
    if os.environ[SSL_CERT_FILE] is None or len(os.environ[SSL_CERT_FILE]) == 0:
        error("A certificate authority must be provided. Use '--ca' option or set {} environnement variable".format(SSL_CERT_FILE))
    client = MinioClient(params.server, params.accessKey, params.secretKey)
    if params.waitSeconds == 0:
        run(client, params)
    else:
        while True:
            run(client, params)
            time.sleep(params.waitSeconds)


class ObjectStatus(Enum):
    EXIST = 1
    DOWNLOADED = 2
    NOT_FOUND = 3


def run(client, params):

    now = datetime.datetime.now()
    from_ts = now + datetime.timedelta(days=-params.backDays)
    # Arrange to fetch from beginning of the first day
    from_ts = datetime.datetime(year=from_ts.year, month=from_ts.month, day=from_ts.day, hour=0, minute=0, second=0)
    # We compute a time from which a 404 can be perceived as normal
    unsure_ts = now + datetime.timedelta(hours=-params.tolerationHours)
    unsure_ts = datetime.datetime(year=unsure_ts.year, month=unsure_ts.month, day=unsure_ts.day, hour=0, minute=0, second=0)

    logger.info("Will store Github archive since {} (checked until {})".format(from_ts, unsure_ts))

    ts = from_ts
    count = 0
    while ts < now and count < params.maxDownloads:
        st = handle_file(client, params, ts, unsure_ts)
        if st == ObjectStatus.EXIST:
            ts = ts + datetime.timedelta(hours=1)
        elif st == ObjectStatus.DOWNLOADED:
            ts = ts + datetime.timedelta(hours=1)
            count += 1
        elif st == ObjectStatus.NOT_FOUND:
            logger.info("No more file to download. Exiting")
            break
        else:
            error("Unknow FileStatus '{}'!".format(st))
    if count >= params.maxDownloads:
        logger.info("Max download count ({}) has been reached. Exiting".format(params.maxDownloads))

# We download on local folder, then move on object storage. This, to ease error handling on download.
def handle_file(minoClient, params, file_ts, unsure_ts):
    bucket = params.bucketFormat.format(year=file_ts.year, month=file_ts.month, day=file_ts.day, hour=file_ts.hour)
    object = params.objectFormat.format(year=file_ts.year, month=file_ts.month, day=file_ts.day, hour=file_ts.hour)
    tmp_file_path = os.path.join(params.workDir, "downloaded.tmp")

    minoClient.ensure_bucket(bucket)
    try:
        os.remove(tmp_file_path)    # Cleanup
    except FileNotFoundError as err:
        pass

    if minoClient.object_exists(bucket, object):
        logger.info("File '{}//{} already downloaded. Skipping".format(bucket, object))
        return ObjectStatus.EXIST
    src_file_name = "{:04d}-{:02d}-{:02d}-{:d}.json.gz".format(file_ts.year, file_ts.month, file_ts.day, file_ts.hour)
    logger.debug("Will download file '{}' to '{}'".format(src_file_name, tmp_file_path))
    if get_file(src_file_name, tmp_file_path):
        logger.debug("Will move downloaded file to '{}//{}".format(bucket, object))
        minoClient.put_file(bucket, object, tmp_file_path, "application/json")
        logger.info("File '{}' has been downloaded into '{}//{}'".format(src_file_name, bucket, object))
        return ObjectStatus.DOWNLOADED
    else:
        if file_ts >= unsure_ts:
            return ObjectStatus.NOT_FOUND  # We consider we are not in error, but at the end of available archive
        else:
            error("Unable to download {}!!".format(src_file_name))
    return ObjectStatus.DOWNLOADED


def get_file(src_file_name, target_file_path):
    url = "http://data.githubarchive.org/{}".format(src_file_name)
    r = requests.get(url, allow_redirects=True)
    if r.status_code == 200:
        open(target_file_path, 'wb').write(r.content)
        logger.debug("Downloaded {}".format(url))
        return True
    elif r.status_code == 404:
        logger.debug("Unable to download {}. Not found".format(url))
        return False
    else:
        error("PB: HTTP code {} on '{}' GET".format(r.status_code, url))



if __name__ == '__main__':
    sys.exit(main())


