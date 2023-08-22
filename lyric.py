import requests
from bs4 import BeautifulSoup

LYRICIST = "xxxx"
FILENAME = f"{LYRICIST}_lyric.txt"

def CountPageNumber(title="", artist_name="", lyricist=""):
    URL = f"https://utaten.com/search?title={title}&artist_name={artist_name}&sub_title=&lyricist={lyricist}&composer=&beginning=&body=&tag=&sort=popular_sort_asc&page=1"
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    ls = soup.select("ul.pager__inner > li.pager__item")
    count = len(ls)//2 - 2
    if count > 0:
        return count
    else:
        return 1

def MakeLyricList(title="", artist_name="", lyricist="", num=1):
    URL = f"https://utaten.com/search?title={title}&artist_name={artist_name}&sub_title=&lyricist={lyricist}&composer=&beginning=&body=&tag=&sort=popular_sort_asc&page={num}"
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    ls_a = soup.select("td > a")
    links = [a.get("href") for a in ls_a]
    return links

def Lyric(link):
    URL = f"https://utaten.com/{link}"
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    lyric = "".join([chars.get_text(strip=True) for chars in soup.select("div.romaji")])
    ls_1 = [chars.get_text(strip=True) for chars in soup.select("div.romaji > span.ruby")]
    ls_2 = [chars.get_text(strip=True) for chars in soup.select("div.romaji > span.ruby > span.rb")]

    for i in range(len(ls_1)):
        lyric = lyric.replace(ls_1[i], ls_2[i])
    return lyric

if __name__ == "__main__":
    cnt = CountPageNumber(lyricist=LYRICIST)
    with open(FILENAME, 'w', encoding="utf-8") as f:
        for i in range(cnt):
            links = MakeLyricList(lyricist=LYRICIST, num=i+1)
            for link in links:
                lyric = Lyric(link)
                f.write(lyric + "\n")
