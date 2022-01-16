class SocialMedia:
    def __init__(self):
        pass
    
    def SocialMedia(self):
        return {
            'email':'EMail',
            'facebook':'FaceBook',
            'linkedin':'LinkedIn',
            'gmail':'GMail',
            'twitter':'Twitter',
            'whatsapp':'WhatsApp',
        }

    def ShareLinks(self):
        return [
            'facebook',
            'whatsapp',
            'twitter',
            'linkedin',
            'email',
            'gmail',
        ]
    
    def WithLinksByOrder(self):
        socialmediasites = self.SocialMedia().keys()
        socialmediasites.sort()
        return socialmediasites
    
    def RefLinks(self, args):
        safeargs = [
            'url',
            'title',
            'image',
            'desc',
            'appid',
            'redirecturl',
            'via',
            'hash_tags',
            'provider',
            'language',
            'user_id',
            'category',
            'phone_number',
            'email_address',
            'cc_email_address',
            'bcc_email_address',
        ]
        
        for safearg in safeargs:
            if not args.get(safearg):
                args[safearg] = ''
        
        text = args['title']
        
        if len(args['desc']):
            text += '%20%3A%20' + args['desc']

        return {
            'email':'mailto:' + args['email_address'] + '?subject=' + args['title'] + '&body=' + args['desc'],
            'facebook':'http://www.facebook.com/sharer.php?u=' + args['url'],
            'gmail':'https://mail.google.com/mail/?view=cm&to=' + args['email_address'] + '&su=' + args['title'] + '&body=' + args['url'] + '&bcc=' + args['bcc_email_address'] + '&cc=' + args['cc_email_address'],
            'linkedin':'https://www.linkedin.com/sharing/share-offsite/?url=' + args['url'],
            'twitter':'https://twitter.com/intent/tweet?url=' + args['url'] + '&text=' + text + '&via=' + args['via'] + '&hashtags=' + args['hash_tags'],
            'whatsapp':'https://api.whatsapp.com/send?text=' + text + '%20' + args['url'],
        }

sm = SocialMedia()
socialmediasites = sm.ShareLinks()
socialmediaurls = sm.RefLinks({
    'url':'http://sanjivani.org/', #The link Goes here.
    'title':'SanjivaniNGOTest', #The Title of Share goes here.
})

for socialmediasite in socialmediasites:
    print(socialmediasite + " : " + socialmediaurls[socialmediasite])
    pass