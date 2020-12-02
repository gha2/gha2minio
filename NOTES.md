export SSL_CERT_FILE=/Users/sa/dev/g6/git/mycertauth/CA/ca2.crt

python main.py --server minio1.shared1 --accessKey minio --secretKey minio123 --ca /Users/sa/dev/g6/git/mycertauth/CA/ca2.crt --workDir /tmp --maxDownloads 1

python main.py --server minio1.shared1 --accessKey minio --secretKey minio123 --ca /Users/sa/dev/g6/git/mycertauth/CA/ca2.crt --workDir /tmp --maxDownloads 1 --waitSeconds 10



docker run -e SERVER=minio1.shared1 -e ACCESS_KEY=minio -e SECRET_KEY=minio123  -e CA=/CA/ca2.crtx -e MAX_DOWNLOADS=1  \
-v /Users/sa/dev/g6/git/mycertauth/CA:/CA -v /tmp:/data gha2/gha2minio:latest

docker run -e SERVER=minio1.shared1 -e ACCESS_KEY=minio -e SECRET_KEY=minio123  -e CA=/CA/ca2.crt -e MAX_DOWNLOADS=1  \
-v /Users/sa/dev/g6/git/mycertauth/CA:/CA -v /tmp:/data -e WAIT_ON_ERROR=10  gha2/gha2minio:latest


echo "minio" | base64
echo "minio123" | base64
echo "minio.minio1.svc.kspray2.local" | base64

