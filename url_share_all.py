def siteShare(url,title,site):

     url=url
     title=title
     site=site
     if(site=='facebook'):
         return('http://www.facebook.com/sharer.php?u=' + url)
     elif(site=='twitter'):
         return('https://twitter.com/intent/tweet?url=' + url + '&text=' + title + '&via=' + "" + '&hashtags=' + title)
     elif(site=='linkedin'):
         return('https://www.linkedin.com/sharing/share-offsite/?url=' +url)
     elif(site=='pinterest'):
         return('http://pinterest.com/pinthis?url='+url)
     elif(site=='whatsapp'):
         return('https://web.whatsapp.com/send?text=' + title + '%20' + url)

    
    