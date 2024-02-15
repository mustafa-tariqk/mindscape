import requests
import json

# Remember to disable role required first

response = requests.get('http://localhost:8080/start_chat/1')
print(response.text)

response = requests.post('http://localhost:8080/converse/', json={
    'chat_id': 2,
    'message': "Hi. I've been. struggling. I had a really bad experience with psychedelics. It was terrifying. I thought I was losing my mind. Everything was distorted, and I couldn't tell what was real and what wasn't. I felt trapped in a nightmare. I've been having nightmares. and I can't shake this feeling of dread. I'm scared that I've damaged my mind permanently. I'm not sure everything just felt so chaotic and out of control I couldn't make sense of anything, and it felt like I was spiraling into darkness. I guess. I just don't want to feel that way ever again. It was the worst thing I've ever experienced. Yeah, I think that could help. I just don't want to feel so alone and helpless anymore. I suppose. I've always struggled with anxiety and self-doubt, but this experience just amplified everything. Thank you. I really needed to hear that. I've been feeling so lost and hopeless, but talking to you has given me a glimmer of hope."
})
print(response.text)

response = requests.get('http://localhost:8080/analytics/get_frequent_words/', {
    'chat_id': 2,
    'k': 10
})
print(json.loads(response.text))