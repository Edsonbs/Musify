import re
def obtenerPlataforma(url):
        patronYoutube1 = re.search(r'\byoutube.com\b', url)
        patronYoutube2 = re.search(r'\byoutu.be\b', url)
        patronSpotify = re.search(r'\bspotify.com\b', url)
        patronTwitter1 = re.search(r'\btwitter.com\b', url)
        patronTwitter2 = re.search(r'\bx.com\b', url)
        patronInstagram = re.search(r'\binstagram.com\b', url)
        patronTiktok = re.search(r'\btiktok.com\b', url)
        patronTwitch = re.search(r'\btwitch.tv\b', url)

        if (patronYoutube1 != None and patronYoutube1.group() == "youtube.com") or (patronYoutube2 != None and patronYoutube2.group() == "youtu.be"):
            return "YouTube", "#FA0404"
        elif patronSpotify != None and patronSpotify.group() == "spotify.com":
            return "Spotify", "#1DE33E"
        elif (patronTwitter1 != None and patronTwitter1.group() == "twitter.com") or (patronTwitter2 != None and patronTwitter2.group() == "x.com"):
            return "Twitter", "#1DB6E3"
        elif patronInstagram != None and patronInstagram.group() == "instagram.com":
            return "Instagram", "#CE21DF"
        elif patronTiktok != None and patronTiktok.group() == "tiktok.com":
            return "TikTok", "#F8F8F8"
        elif patronTwitch != None and patronTwitch.group() == "twitch.tv":
            return "Twitch", "#BB68DF"
        else:
            return "Plataforma", "#F09C20"

print(obtenerPlataforma("https://www.youtube.com/watch?v=JGhoLcsr8GA"))