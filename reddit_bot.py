from selenium import webdriver
import requests
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests, re, os


############# YOU NEED TO FILL ALL OF THIS TO RUN THIS PROGRAM  ##################

username = ''                                       ########## WRITE YOUR REDDIT USERNAME  
password = ''                                       ########## WRITE YOUR REDDIT PASSWORD 
location = f"C:/"                                   ########## it will make a folder in this location By name 
secret = ''                                         ##########  Add the secret from reddit.com/prefs
identity = ''                                       ##########  Add the id from the reddit.com/prefs
webdriver_path = ''                                 ########## Chrome web driver is required


################# don't forget to uncomment the function you want to run #######################

####### if you using multiple download from the subreddit the uncomment the get_files in main function
listing = [
    '/r/ContagiousLaughter/',
    '/r/MadeMeSmile/',
    '/r/therewasanattempt/',
    '/r/funny/',
    '/r/NatureIsFuckingLit/',
    '/r/instant_regret/',
    '/r/holdmyredbull/',
    '/r/nextfuckinglevel/',
    '/r/CatastrophicFailure/',
    '/r/Whatcouldgowrong/',
    '/r/interestingasfuck',
    '/r/Unexpected/',
    '/r/BeAmazed/',
    '/r/whatcouldgoright/',
    '/r/natureismetal/',
    '/r/Damnthatsinteresting/'
]

############ To download from the specific url  Uncomment the specific_url function in the main
links = [
]            
country = 'GLOBAL'       # FILL THE CODE OF THE COUNTRY  
pages = 10                # NUMBER OF PAGES YOU NEED TO EXTRACT
file = "PICTURE"         # WHAT YOU NEED VIDEO OR PICTURE ( ONLY UPPERCASE ) 
with_links = True        # If you need the url of the downloaded files ( True / False)


# [+] SUBREDDITS OR TOP ADD THIS IN "LISTING" AS SHOWN ABOVE
# trending_subreddits
# hot
# new
# random
# rising
# You can also add any subreddit in the listing like :-
        # '/r/ContagiousLaughter/',
        # '/r/MadeMeSmile/',
        # '/r/therewasanattempt/',
        # '/r/IdiotsFightingThings/',
        # '/r/Stepdadreflexes/',
        # '/r/funny/',
        # '/r/NatureIsFuckingLit/',
        # '/r/instant_regret/',
        # '/r/holdmyredbull/',
        # '/r/PraiseTheCameraMan/',
        # '/r/nextfuckinglevel/',
        # '/r/CatastrophicFailure/',
        # '/r/Whatcouldgowrong/',
        # '/r/interestingasfuck',
        # '/r/Unexpected/',
        # '/r/blackmagicfuckery/',
        # '/r/BeAmazed/',
        # '/r/whatcouldgoright/',
        # '/r/natureismetal/',
        # '/r/Damnthatsinteresting/'

# [+] COUNTRY
# (GLOBAL, US, AR, AU, BG, CA, CL, CO, HR, CZ, FI, GR, HU, IS, IN, IE, JP, MY, 
# MX, NZ, PH, PL, PT, PR, RO, RS, SG, SE, TW, TH, TR, GB, US_WA, US_DE, US_DC,
# US_WI, US_WV, US_HI, US_FL, US_WY, US_NH, US_NJ, US_NM, US_TX, US_LA, US_NC,
# US_ND, US_NE, US_TN, US_NY, US_PA, US_CA, US_NV, US_VA, US_CO, US_AK, US_AL,
# US_AR, US_VT, US_IL, US_GA, US_IN, US_IA, US_OK, US_AZ, US_ID, US_CT, US_ME,
# US_MD, US_MA, US_OH, US_UT, US_MO, US_MN, US_MI, US_RI, US_KS, US_MT, US_MS,
# US_SC, US_KY, US_OR, US_SD)

path = os.path.join(location,'reddit')

class Reddit:

    def __init__(self):
        self.access_token = ""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": path,
            "download.directory_upgrade": True
        })
        self.bot = webdriver.Chrome(
            executable_path=webdriver_path,
            options=chrome_options)
        print(f'Pages {pages}, filetype "{file}", Country "{country}"')

    def auth(self):
        try:
            client_auth = requests.auth.HTTPBasicAuth(secret, identity)
            post_data = {"grant_type": "password", "username": username, "password": password}
            headers = {"User-Agent": f'ChangeMeClient/0.1 by {username}'}
            response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
                                    headers=headers).json()
        except Exception as e:
            print(f"Authentication failure {e}")
            return
        self.access_token = f"bearer {response['access_token']}"


    def get_files(self):
        for i in listing:
            post = []
            posts = self.retrive_post(i,pages)
            print(f"Downloading from {i}")
            if file == "VIDEO":
                video_post = self.videos(posts)
                self.repeat(video_post)
            elif file == "PICTURE":
                self.picture(posts)


    ###make a file name post store the title and url of the downloaded post            
    def repeat(self,posts):
        for i in posts:
            if with_links:
                open('posts','wb').write(posts+"\n")
            self.download_media(i['url'],i['title'])


    ### retireve picture posts from all the post
    def picture(self,data):
            for i in data:
                title = i['data']['title']
                title = re.sub('[^A-Za-z]+', ' ', title).strip()
                url = i['data']['url']
                if '.png' in url:
                    extension = '.png'
                elif '.jpg' in url:
                    extension = '.jpeg'
                elif '.jpeg' in url:
                    extension = '.jpeg'
                else:
                    return
                r = requests.get(url,stream=True)
                d = os.listdir(location)
                if "reddit" not in d:
                    os.mkdir(path)
                p = os.path.join(path,title[:40])
                p += extension
                if r.status_code == 200:
                    open(p,'wb').write(r.content)
                
    ### Get the post from the reddit api
    def retrive_post(self,subreddit,pages):
        try:
            headers = {"Authorization": self.access_token, "User-Agent": "ChangeMeClient/0.1 by "+username}
            url = f"https://oauth.reddit.com{subreddit}?limit=5&g={country}"
            response = requests.get(url, headers=headers).json()
            data = response['data']['children']
            after = response['data']['after']
            if pages > 1:
                for i in range(pages):
                    url = f"https://oauth.reddit.com{subreddit}?limit=100&g=GLOBAL&after={after}"
                    response = requests.get(url + after,headers=headers).json()
                    data += response['data']['children']
            return data
        except Exception as e:
            print(f"Retrive post failure {e}")
    
    ### Retrieve the videos url and title from the posts
    def videos(self,data):
        video_post = []
        for d in data:
            if d['data']['is_video']:
                title = re.sub('[^A-Za-z]+', ' ', d['data']['title']).strip()
                video = {
                    "title": title,
                    "url": 'https://reddit.com'+d['data']['permalink']
                }
                video_post.append(video)
        print(f" No of video {len(video_post)}")
        return video_post
    
    ### download the videos
    def download_media(self,url,title):
        d = os.listdir(location)
        if "reddit" not in d:
            os.mkdir(path)

        if title == 'none':
                    title = url.split('/')[-2]
                    title = re.sub('[^A-Za-z]+', ' ', title).strip()

        bot = self.bot
        if self.check_dir(title,path): # Comment this if you want dulplicates
            return
        else:
            try:
                print(f"[+] Started Downloading {title}")
                bot.get('https://viddit.red/?url='+url)
                bot.refresh()
                sleep(4) # You change the Second(s) here if you have slow internet connection or page is taking time
                link = bot.find_element_by_id('dlbutton').get_attribute('href')
                r = requests.get(link)
                filename = r'{}\{}.mp4'.format(path,title)
                open(filename, "wb").write(r.content)
                print(f'[-] Completed {title}')
            except Exception as e:
                print(e)
    
    def check_dir(self,title,path):
        directory = [ d.split('.')[0] for d in os.listdir(path) ]
        for i in directory:
            if title == i:
                return True
        return False

    def specific(self):
        if file == 'VIDEO':
            self.specific_videos()
        elif file == 'GIF':
            self.specific_gif()

    def specific_videos(self):
        if len(links) == 0:
            print("The list is empty")
            return
        for i in links:
            self.download_media(i,"none")
    


if __name__ == '__main__':
    reddit = Reddit()
    reddit.auth();
    reddit.get_files() # Uncomment to download multiple video files  ( set pages and type )
    # reddit.specific() # Uncomment to download files from a provide url
