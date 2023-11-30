docker build -t Feishu-bot .
docker run --env-file ../config/.env -p 3000:3000 -it Feishu-bot
