docker run -d -p 9200:9200 -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms512m -Xmx512m" -v esdata:/usr/share/elasticsearch/data  docker.elastic.co/elasticsearch/elasticsearch:6.4.2

# FIX permission error
curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'


 # permament database
 docker run -d -p 27017:27017 -v /home/carlosb/data:/data/db mongo
 
 # redis to set up batch tasks
docker run -p 6379:6379 --name some-redis -d redis

# Setting up nltk
  >>> import nltk
  >>> nltk.download('punkt')

