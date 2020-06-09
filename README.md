you might think 'i could concatenate this into one script' but i would caution you two things

sometimes spot shits the bed on an api query, you get unparseable nonsense

"oh but i can use try"

you need some sort of memory between invocations

because you're updating a message in a channel

it provides a live location object

if you want to write a json or pickle to disk, you could

but some persistent storage is necessary to track when you need to create a new location message

and when you can update the old one

see the telegram location api for detail

i also track to ensure no matter how many times i invoke it, i don't pull an api from spot more than once every 3 minutes

they ask you to limit your polling requests

esp since i run this 24/7

once a minute in cron
