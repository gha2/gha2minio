#!/bin/sh

# Mandatory parameters

OPTS="--server $SERVER"
OPTS="$OPTS --accessKey $ACCESS_KEY"
OPTS="$OPTS --secretKey $SECRET_KEY"

if [ -n "$UNSECURE" ] && [ "$UNSECURE" = "yes" ]; then
  OPTS="$OPTS --unsecure"
fi

if [ -n "$BUCKET_FORMAT" ]; then
  OPTS="$OPTS --bucketFormat $BUCKET_FORMAT"
fi

if [ -n "$OBJECT_FORMAT" ]; then
  OPTS="$OPTS --objectFormat $OBJECT_FORMAT"
fi

if [ -n "$BACK_DAYS" ]; then
  OPTS="$OPTS --backDays $BACK_DAYS"
fi

if [ -n "$TOLERATION_HOURS" ]; then
  OPTS="$OPTS --tolerationHours $TOLERATION_HOURS"
fi

if [ -n "$MAX_DOWNLOADS" ]; then
  OPTS="$OPTS --maxDownloads $MAX_DOWNLOADS"
fi

if [ -n "$WAIT_SECONDS" ]; then
  OPTS="$OPTS --waitSeconds $WAIT_SECONDS"
fi

if [ -n "$CA" ]; then
  OPTS="$OPTS --ca $CA"
fi

if [ -n "$WORK_DIR" ]; then
  OPTS="$OPTS --workDir $WORK_DIR"
fi

if [ -n "$SET_X" ] && [ "$SET_X" = "yes" ]; then
  set -x
fi

python3 main.py $OPTS
err=$?

if [ -n "$WAIT_ON_ERROR" ]; then
  if [ $err -ne 0 ]; then
    echo "ERROR: rc=$err. Will wait $WAIT_ON_ERROR sec...."
    sleep $WAIT_ON_ERROR
  fi
fi

return $err

