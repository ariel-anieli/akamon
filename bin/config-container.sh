img=cmon
cmd='sudo docker'
pid=sqvalcmon`jq -r '.id' $1`
tag=`$cmd images $img --format "{{.Tag}}" | head -n1`

run="$cmd run -d -it --name $pid -h $pid $img:$tag"
id=`$run`

jq --arg id  $id \
   --arg pid $pid \
   --arg img "$img:$tag" \
   '{container: {id: $id, image: $img, name: $pid, host: $pid}} + .' $1
