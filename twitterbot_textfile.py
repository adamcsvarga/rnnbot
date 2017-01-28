# Import our Twitter credentials from credentials.py
import tweepy
from time import sleep
from credentials import *
consumer_key = 'aASpfECWNESRvTZSLr3F2QKYD'
consumer_secret = 'Qis8iBNxEoFIl9iQwlsbxgW4f32FEvbz4fcQ7nhfmLrrkcw0JV'
access_token = '822053231769612288-kNdMdHOXqgwHIJ1sJb7lWLrDc2EFnwB'
access_secret = 'ZmIITzdsPzoIgqP3NlNqGLrf6FDjgCoNUB1sCfEInNWjX'


#Tweet every 10 minutes
def tweet():
# Create a for loop to iterate over file_lines
    for line in file_lines:
    # Add try ... except block to catch and output errors
        try:
            print(line)
            if line != '\n':
                api.update_status(line)
                sleep(600)
            else:
                pass
        except tweepy.TweepError as e:
            print(e.reason)
            sleep(2)
            
# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# Open text file verne.txt (or your chosen file) for reading
my_file = open('twitterbot.txt', 'r')

# Read lines one by one from my_file and assign to file_lines variable
file_lines = my_file.readlines()

# Close file
my_file.close()

tweet()


