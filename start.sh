docker rm -f mj-server mj-bot
#docker rmi kunyu/midjourney-api:1.0

docker network create mjapi
docker run -d --net mjapi --name mj-server -p 8062:8062 \
	-e TZ=Asia/Shanghai \
	-e LOG_LEVEL=DEBUG \
	-e USER_TOKEN="" \
	-e GUILD_ID="" \
	-e CHANNEL_ID="" \
	-e CONCUR_SIZE=3 \
	-e WAIT_SIZE=10 \
	kunyu/midjourney-api:1.0

docker run -d --net mjapi --name mj-bot \
	-e TZ=Asia/Shanghai \
	-e LOG_LEVEL=DEBUG \
	-e USER_TOKEN="" \
	-e BOT_TOKEN="" \
	-e GUILD_ID="" \
	-e CHANNEL_ID="" \
	-e CALLBACK_URL="" \
	-e QUEUE_RELEASE_API="http://mj-server:8062/v1/api/trigger/queue/release" \
	kunyu/midjourney-api:1.0 bot
