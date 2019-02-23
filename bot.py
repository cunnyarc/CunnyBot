import twitter, json, requests, time, os

consumer_key = "CONSUMERKEY"
consumer_secret = "SONSUMERSECRET"
access_token_key = "ACCESSTOKENKEY"
access_token_secret = "ACCESSTOKENSECRET"

api = twitter.Api(consumer_key,consumer_secret,access_token_key,access_token_secret)
lastImageUrl = ""

def postMoe():
	global lastImageUrl
	if lastImageUrl == "":
		print("I'm Running")
	with requests.get('https://www.reddit.com/r/awwnime/new.json', headers={'user-agent': 'OreganoMoeBot'}) as url:
		moeData = json.loads(url.content)['data']['children'][0]['data']
		moeImage = moeData['url']
		moeLink = "https://www.reddit.com" + moeData['permalink']
		if (moeImage != lastImageUrl):
			api.PostUpdate("#moe | " + moeLink, moeImage)
			lastImageUrl = moeImage
			time.sleep(3600)
			postMoe()

postMoe()
