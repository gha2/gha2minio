export SSL_CERT_FILE=/Users/sa/dev/g6/git/mycertauth/CA/ca2.crt

python main.py --server minio1.shared1 --accessKey minio --secretKey minio123 --ca /Users/sa/dev/g6/git/mycertauth/CA/ca2.crt --workDir /tmp --maxDownloads 1

