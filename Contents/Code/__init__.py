VIDEO_PREFIX = "/video/einthusan"
NAME = L('Einthusan')
ART  = 'art-default.jpg'
ICON = 'icon-default.png'
NEXT = 'Next-icon.png'
PREV = 'Prev-icon.png'
TAMIL_LANG = 'Tamil'
HINDI_LANG = 'Hindi'
TELUGU_LANG= 'Telugu'
MALAYALAM_LANG = 'Malayalam'
HOMEURL = 'http://www.einthusan.com'
ListURL='http://www.einthusan.com/movies/index.php?lang=|LANG|&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=|PAGE_NO|'
#SEARCH_URL='http://www.einthusan.com/search/?search_query=|QUERY_TEXT|&lang=|LANG|'
#SEARCH_URL='http://www.einthusan.com/movies/index.php?lang=|LANG|&search=|QUERY_TEXT|'
SEARCH_URL='http://www.einthusan.com/movies/index.php?lang=|LANG|&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=|PAGE_NO|&search=|QUERY_TEXT|'
LIST_YEAR_URL='http://www.einthusan.com/movies/index.php?lang=|LANG|&organize=Year&filtered=|LIST_YEAR|&org_type=Year&page=|PAGE_NO|'
CURRENT_LANG='Tamil'
#


####################################################################################################
def Start():
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    ObjectContainer.title1 = NAME
    ObjectContainer.art = R(ART)
    DirectoryObject.thumb = R(ICON)
    HTTP.CacheTime = 0
    

####################################################################################################
def VideoMainMenu():
    dir = ObjectContainer(title2="Movies")
    dir.add(DirectoryObject(key=Callback(SecondLevelMenu, lang=TAMIL_LANG), title=TAMIL_LANG, summary="Click here to watch Tamil Movies"))
    dir.add(DirectoryObject(key=Callback(SecondLevelMenu, lang=HINDI_LANG), title=HINDI_LANG, summary="Click here to watch Hindi Movies"))
    dir.add(DirectoryObject(key=Callback(SecondLevelMenu, lang=TELUGU_LANG), title=TELUGU_LANG, summary="Click here to watch Telugu Movies"))
    dir.add(DirectoryObject(key=Callback(SecondLevelMenu, lang=MALAYALAM_LANG), title=MALAYALAM_LANG, summary="Click here to watch Malayalam Movies"))
    dir.add(InputDirectoryObject(key=Callback(SearchMovies), title="Search Movie", summary="Click here to Search for Movies by name", thumb=R(ICON), prompt="Enter Movie Name"))
    
    return dir

####################################################################################################
def SecondLevelMenu(lang):
    global CURRENT_LANG
    CURRENT_LANG=lang
    dir2 = ObjectContainer(title2=lang);
    dir2.add(DirectoryObject(key=Callback(ListMovies, lang=lang, pageNo = 1), title="Recently added", summary="Click here to List recently added Movies"))
    dir2.add(InputDirectoryObject(key=Callback(ListMoviesByYear), title="Filter by Year", summary="Click here to List Movies for a given Year",thumb=R(ICON), prompt="Enter Year"))
    dir2.add(InputDirectoryObject(key=Callback(SearchMovies), title="Search Movie", summary="Click here to Search for Movies by name", thumb=R(ICON), prompt="Enter Movie Name"))
    return dir2

####################################################################################################
def ListMovies(lang, pageNo, listweburl=ListURL, query=None):
    dir = ObjectContainer(title2=lang)
    Log(listweburl)
    listwebrulorig = listweburl 
    #if (pageNo > 1):
    #    #dir.add(DirectoryObject(key=Callback(ListMovies, listweburl=listwebrulorig, pageNo=pageNo-1, lang=lang, query=query), title="Previous Set of Movies", thumb=R(PREV)))
    listweburl = listweburl.replace('|PAGE_NO|', str(pageNo))
    listweburl = listweburl.replace('|LANG|', lang)
    if (query is not None):
        listweburl = listweburl.replace('|QUERY_TEXT|', query)
        listweburl = listweburl.replace('|LIST_YEAR|', query)
    page = HTML.ElementFromURL(listweburl)
    videoListing = page.xpath('//div[@class="video-listing"]')[0]
    videoObjectWrappers = videoListing.xpath('div[@class="video-object-wrapper"]')
    duration = 0
    for videoObjectWrapper in videoObjectWrappers:
        videoObjectDetails  = videoObjectWrapper.xpath('div[@class="video-object-details"]')[0]
        videodetails = videoObjectDetails.xpath('div[@class="movie-title-wrapper"]//a')[0]
        videoObjectThumbs = videoObjectWrapper.xpath('div[@class="video-object-thumb"]//a')[0]
        title = videodetails.text
        movieUrl = videodetails.xpath('@href')[0].replace("..", HOMEURL)
        #imageUrl = videoObjectThumbs.xpath('img//@src')[0].replace("..",  HOMEURL)
        summaryelement = videoObjectDetails.xpath('.//div[@class="movie-description"]//p[@class="desc_body"]')[0]
        summaryspan = summaryelement.xpath('.//span')[0]
        summary = summaryelement.text + summaryspan.text
        imageUrl = videoObjectWrapper.xpath('.//a[@class="movie-cover-wrapper"]//img//@src')[0].replace("..",HOMEURL)
        dir.add(VideoClipObject(
                key=Callback(VideoDetail2, title=title, summary=summary, thumb=imageUrl, vidUrl=movieUrl),
                rating_key=movieUrl,
                title=title,
                summary=summary,
                duration=duration,
                thumb=imageUrl,
                items=[
                MediaObject(
                    container = Container.MP4,
                    audio_codec = AudioCodec.AAC,
                    parts = [PartObject(key=Callback(PlayVideo, url=movieUrl))],
                    optimized_for_streaming = True
                )
                ]
            ))
        continue
    #dir.add(NextPageObject(key=Callback(ListMovies, listweburl=listwebrulorig, pageNo = pageNo + 1, lang=lang, query=query), title="Next Set of Movies", thumb=R(NEXT)))
    dir.add(NextPageObject(key=Callback(ListMovies, listweburl=listwebrulorig, pageNo = pageNo + 1, lang=lang, query=query)))

    return dir

####################################################################################################
def SearchMovies(query=None):
    return ListMovies(lang = CURRENT_LANG, pageNo = 1, listweburl = SEARCH_URL, query=query);


####################################################################################################
def ListMoviesByYear(query=None):
    return ListMovies(lang = CURRENT_LANG, pageNo = 1, listweburl = LIST_YEAR_URL, query=query);

####################################################################################################
def VideoDetail2(title, summary, thumb, vidUrl):
    oc = ObjectContainer(title2 = title)
    Log(vidUrl)
    duration = 0
    oc.add(VideoClipObject(
        key=Callback(VideoDetail2, title=title, summary=summary, thumb=thumb, vidUrl=vidUrl),
        rating_key=vidUrl,
        title=title,
        summary=summary,
        duration=duration,
        thumb=thumb,
        items=[
        MediaObject(
            container = Container.MP4,
            audio_codec = AudioCodec.AAC,
            parts = [PartObject(key=Callback(PlayVideo, url=vidUrl))],
            optimized_for_streaming = True
        )
        ]
    ))

    return oc


####################################################################################################
@indirect
def PlayVideo(url):

        m3u8_url = GetDirectURL(url)
        return IndirectResponse(VideoClipObject,
                key = m3u8_url,
                #rating_key = m3u8_url,
                #http_cookies = cookie
                )
    

  
####################################################################################################
def GetDirectURL(vidUrl):
        page = HTML.ElementFromURL(vidUrl)
        url = vidUrl
        scripts = page.xpath('//script[@type="text/javascript"]');
        playerStr = 'jwplayer("mediaplayer").setup('
        for script in scripts:
            if (script.text is not None):
                if playerStr in script.text:
                    start = script.text.find(playerStr) + len(playerStr)
                    end = script.text.find(')', start)
                    jscript = script.text[start:end]
                    start = jscript.find("'file': '") + len ("'file': '")
                    end = jscript.find("'", start)
                    url = jscript[start:end]
                    Log(url)
                    break
        return url





