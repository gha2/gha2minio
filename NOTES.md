export SSL_CERT_FILE=/Users/sa/dev/g6/git/mycertauth/CA/ca2.crt

python main.py --server minio1.shared1 --accessKey minio --secretKey minio123 --ca /Users/sa/dev/g6/git/mycertauth/CA/ca2.crt --workDir /tmp --maxDownloads 1

python main.py --server minio1.shared1 --accessKey minio --secretKey minio123 --ca /Users/sa/dev/g6/git/mycertauth/CA/ca2.crt --workDir /tmp --maxDownloads 1 --waitSeconds 10



docker run -e SERVER=minio1.shared1 -e ACCESS_KEY=minio -e SECRET_KEY=minio123  -e CA=/CA/ca2.crtx -e MAX_DOWNLOADS=1  \
-v /Users/sa/dev/g6/git/mycertauth/CA:/CA -v /tmp:/data gha2/gha2minio:latest

docker run -e SERVER=minio1.shared1 -e ACCESS_KEY=minio -e SECRET_KEY=minio123  -e CA=/CA/ca2.crt -e MAX_DOWNLOADS=1  \
-v /Users/sa/dev/g6/git/mycertauth/CA:/CA -v /tmp:/data -e WAIT_ON_ERROR=10  gha2/gha2minio:latest

python main.py --server localhost:9000 --unsecure --accessKey accesskey --secretKey secretkey --workDir /tmp --maxDownloads 2 --backDays 0 --waitSeconds 10

docker run -e SERVER=bob:9000 -e UNSECURE=yes -e ACCESS_KEY=accesskey -e SECRET_KEY=secretkey -e MAX_DOWNLOADS=2 \
-e MAX_DOWNLOADS=2 -e BACK_DAYS=0 -e WAIT_SECONDS=10 \
-v /tmp:/data gha2/gha2minio:latest



