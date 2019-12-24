import json as j
import _thread as thread
import tweepy
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

def load_monitoring(as_dict = False):
    with open('monitoring.json', 'r') as file:
        info = file.read()
        info = j.loads(info)
        if as_dict:
            return info
    to_monitor = []
    for key in info:
        account_info = info[key]
        to_monitor.append([key, account_info])
    return to_monitor

RELOAD = True
monitoring = load_monitoring()
SAVE = False
DISCORD_URL = ""

def twitter_login(a,b,c,d):
    auth = tweepy.OAuthHandler(a, b)
    auth.set_access_token(c, d)
    return auth

def get_lowest_amnt(api_list):
    index = 0
    lowest = 1000000
    for api in range(len(api_list)):
        if len(api_list[api][1]) < lowest:
            index = api
            lowest = len(api_list[api][1])
    return index

def load_accounts():
    with open('accounts.json', 'r') as file:
        info = file.read()
        info = j.loads(info)
    return info["accounts"]

def save_monitoring(monitoring):
    dict_ = {}
    for account in monitoring:
        dict_[account[0]] = account[1]
    with open('monitoring.json', 'w') as file:
        j.dump(dict_, file)

def check_bio(account, user, account_index):
    global monitoring
    global SAVE
    global DISCORD_URL
    old_bio = account[1][0]
    new_bio = user.description
    if old_bio != new_bio:
        monitoring[account_index][1][0] = new_bio
        try:
            urls = ""
            for url in user.entities['description']['urls']:
                urls += url['expanded_url'].lower() + "\n"
        except:
            urls = False
            pass
        screen_name = user.screen_name
        user_url = "https://www.twitter.com/{}".format(screen_name)
        webhook = DiscordWebhook(url=DISCORD_URL)
        embed = DiscordEmbed(color =0xFF8F00)
        embed.set_author(name="{} changed their description...".format(screen_name), url=user_url, icon_url=user.profile_image_url_https)
        embed.add_embed_field(name='**OLD BIO**', value="**{}**".format(old_bio), inline = False)
        embed.add_embed_field(name='**NEW BIO**', value="**{}**".format(new_bio), inline = False)
        if urls:
            embed.add_embed_field(name="**LINKS IN BIO**", value="**{}**".format(urls), inline = False)
        webhook.add_embed(embed)
        webhook.execute()
        SAVE = True

def check_url(account, user, account_index):
    global monitoring
    global SAVE
    global DISCORD_URL
    old_url = account[1][1]
    try: 
        new_url = user.entities['url']['urls'][0]['expanded_url'].lower()
        if old_url != new_url:
            monitoring[account_index][1][1] = new_url
            screen_name = user.screen_name
            user_url = "https://www.twitter.com/{}".format(screen_name)
            webhook = DiscordWebhook(url=DISCORD_URL)
            embed = DiscordEmbed(color =0xE800FF)
            embed.set_author(name="{} changed their BIO URL...".format(screen_name), url=user_url, icon_url=user.profile_image_url_https)
            embed.add_embed_field(name='**OLD BIO URL**', value="**{}**".format(old_url), inline = True)
            embed.add_embed_field(name='**NEW BIO URL**', value="**{}**".format(new_url), inline = True)
            webhook.add_embed(embed)
            webhook.execute()    
            SAVE = True
    except:
        pass

def get_bios(user_id, API):
    global DISCORD_URL
    user = API.get_user(user_id)
    user_bio = user.description
    try:
        urls = ""
        description_urls = user.entities['description']['urls']
        for url in description_urls:
            urls += url['expanded_url'].lower() + "\n"
    except:
        urls = False
        pass
    try:
        bio_url = user.entities['url']['urls'][0]['expanded_url'].lower()
    except:
        bio_url = False
        pass

    screen_name = user.screen_name
    user_url = "https://www.twitter.com/{}".format(screen_name)
    webhook = DiscordWebhook(url=DISCORD_URL)
    embed = DiscordEmbed(color =0x00FFCD)    
    embed.set_author(name="{} was mentioned in a tweet...".format(screen_name), url="{}".format(user_url), icon_url=user.profile_image_url_https)
    embed.set_footer(text='Made with love by Will')
    embed.add_embed_field(name='**USER DESCRIPTION**', value=user_bio, inline=False)
    if bio_url:
        embed.add_embed_field(name='**BIO URL**', value="**{}**".format(bio_url), inline = True)
    embed.add_embed_field(name='**QUICK LINKS**', value="[**PROFILE**]({})".format(user_url), inline = True)        
    if urls:
        embed.add_embed_field(name='**URLS IN BIO**', value="**{}**".format(urls), inline = False)        
    webhook.add_embed(embed)
    webhook.execute()

def check_quoted(quoted_id, API):
    global DISCORD_URL
    tweet = API.get_status(quoted_id)
    user = tweet.user
    try:
        bio_url = user.entities['url']['urls'][0]['expanded_url'].lower()
    except:
        bio_url = False
    try:
        description_urls = ""
        for url in user.entities['description']['urls']:
            description_urls += url['expanded_url'].lower()
    except:
        description_urls = False
    try:
        urls = ""
        for url in tweet.entities['urls']:
            urls += url['expanded_url'].lower() + "\n"
    except:
        urls = False

    screen_name = user.screen_name
    user_url = "https://www.twitter.com/{}".format(screen_name)
    webhook = DiscordWebhook(url=DISCORD_URL)
    embed = DiscordEmbed(color =0xA200FF)
    embed.set_author(name="{} was quoted...".format(screen_name), url="{}".format(user_url), icon_url=user.profile_image_url_https)
    embed.add_embed_field(name="**USER BIO**", value=user.description, inline=False)
    if description_urls:
        embed.add_embed_field(name="**DESCRIPTION URLS**", value="**{}**".format(description_urls), inline=True)
    if bio_url:
        embed.add_embed_field(name="**BIO URL**", value="**{}**".format(bio_url), inline=True)
    embed.add_embed_field(name='**TWEET CONTENT**', value="**{}**".format(tweet.text), inline=False)
    if urls:
        embed.add_embed_field(name='**QUOTED TWEET URLS**', value="**{}**".format(urls), inline=False)
    webhook.add_embed(embed)
    webhook.execute()  

def check_tweets(account, user, account_index, API):
    global monitoring
    global SAVE
    global DISCORD_URL
    status = user.status
    new_id = status.id
    old_id = account[1][2]

    if old_id != new_id:
        if not new_id < old_id:
            monitoring[account_index][1][2] = new_id
            entities = status.entities
            try:
                quoted_id = status.quoted_status_id
                thread.start_new_thread(check_quoted, (quoted_id, API))
            except:
                pass
            try:
                for user_ in entities['user_mentions']:
                    thread.start_new_thread(get_bios, (user_['id'], API))
            except: 
                pass
            try:
                urls = ""
                for url in entities['urls']:
                    if 'twitter' not in url['expanded_url']:
                        urls += url['expanded_url'].lower() + "\n"
            except:
                urls = False
            
            screen_name = user.screen_name
            user_url = "https://www.twitter.com/{}".format(screen_name)
            tweet_url = user_url + "/status/" + str(new_id)
            webhook = DiscordWebhook(url=DISCORD_URL)
            embed = DiscordEmbed(color =242424)
            embed.set_author(name="{} tweeted...".format(screen_name), url=tweet_url, icon_url=user.profile_image_url_https)
            embed.set_footer(text='Made with love by Will')
            embed.add_embed_field(name='**TWEET CONTENT**', value=user.status.text, inline=False)
            embed.add_embed_field(name='**QUICK LINKS**', value="[**PROFILE**]({}) -- [**TWEET**]({})".format(user_url, tweet_url), inline = False)        
            if urls:   
                embed.add_embed_field(name='**TWEET URLS**', value="**{}**".format(urls), inline = False)        
            webhook.add_embed(embed)
            webhook.execute()
            SAVE = True

def check_mointoring(account_index, API, delay):
    global RELOAD
    global monitoring
    while True and not RELOAD:

        account = monitoring[account_index]
        user = API.get_user(account[0])
        screen_name = user.screen_name
        print('Checking {}...'.format(screen_name))

        # CHECKING LATEST TWEETS
        thread.start_new_thread(check_tweets, (account, user, account_index, API))
        # CHECKING USER BIO
        thread.start_new_thread(check_bio, (account, user, account_index))
        # CHECKING USER BIO URL
        thread.start_new_thread(check_url, (account, user, account_index))
       
def check_if_save():
    global monitoring
    global SAVE
    while True:
        if SAVE:
            save_monitoring(monitoring)
            SAVE = False

def start():
    global monitoring
    accounts = load_accounts()
    api_list = []
    
    thread.start_new_thread(check_if_save, ())

    for account in accounts:
        auth = twitter_login(account[0], account[1], account[2], account[3])
        API = tweepy.API(auth)
        api_list.append([API, []])

    for user in range(len(monitoring)):
        index = get_lowest_amnt(api_list)
        api_list[index][1].append(user)
    
    for api in api_list:
        if len(api[1]) > 0:
            delay = len(api[1])
            for user in api[1]:
                thread.start_new_thread(check_mointoring, (user, api[0], delay,))
while True:
    if RELOAD == True:
        time.sleep(3)
        start()
        RELOAD = False
    pass


