import twitter,dropbox, requests, time, random, math

consumerKey = 'CONSUMERKEY'
consumerSecret = 'CONSUMERSECRET'
accessTokenKey = 'ACESSTOKENKEY'
accessTokenSecret = 'ACESSTOKENSECRET'
api = twitter.Api(consumer_key = consumerKey, consumer_secret = consumerSecret, access_token_key = accessTokenKey, access_token_secret = accessTokenSecret)
client = dropbox.Dropbox('DROPBOXKEY')

def postMoe():
	postnubmer = 0
	moeFolder = client.files_list_folder('').entries
	randomIndex = math.floor(random.random() * len(moeFolder))
	randomImage = client.sharing_create_shared_link('/' + moeFolder[randomIndex].name).url[:-1] + '1'
	api.PostUpdate('', randomImage)
	postnumber += 1
	print("Post {0} successfull!".format(postnumber))

while True:
    postMoe()
    time.sleep(3600) #waits 1 hour
