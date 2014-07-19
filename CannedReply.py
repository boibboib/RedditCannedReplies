#!/usr/bin/python

import re
import sys
from ReddiWrap import ReddiWrap
from ReddiWrap import Post

reddit = ReddiWrap(user_agent='ReddiWrap/boib-CannedReply by /u/boib')

#
# - read user/pass file data
#
USERNAME = 'xxxx'
PASSWORD = 'xxxx'

if len(sys.argv) < 2:
    print ("\nMissing url of message to moderate.\nUsage: CannedReply.pl <url>\n\n")
    quit()



#
# - read previous login info (cookie) and log in
#
reddit.load_cookies('cookies.txt')

# If we had no cookies, or cookies were invalid,
# or the user we are logging into wasn't in the cookie file:
if not reddit.logged_in or reddit.user.lower() != USERNAME.lower():
	print('logging into %s' % USERNAME)
	login = reddit.login(user=USERNAME, password=PASSWORD)
	if login != 0:
		# 1 means invalid password, 2 means rate limited, -1 means unexpected error
		print('unable to log in: %d' % login)
		print('remember to change USERNAME and PASSWORD')
		exit(1)
	# Save cookies so we won't have to log in again later
	reddit.save_cookies('cookies.txt')

print('\n[logged in as %s]\n=============================\n' % reddit.user)


#
# - read file of canned replies
#
f = open('CannedReplies.txt')
CannedRepliesStr = f.read()
f.close()

s = CannedRepliesStr.split('#CR\n')
t = []

for i in s:
    if i[0] == '#' or i[0] == ' ' or i[0] == '\n':
        continue
    t.append(i)

#print CannedRepliesStr


#
#  TODO: Make GUI, get post in question by drag/drop.
#        For now, url is passed in via cmd line
#


#
# Get post from reddit
#
#postToDelete = reddit.get('http://www.reddit.com/r/boibtest/comments/27fdwk/boib_test_740pm/')
postToDelete = reddit.get(sys.argv[1])

if not postToDelete:
    print ('****** Error retrieving post ******\n')
    exit(1)
print ('Post to delete: %s\n' % postToDelete[0])


#
# TODO: Verify logged in user is a moderator in the subreddit of the URL
#


#
# - which canned reply to use.  Print choices and get user input
#
ans=True
while ans:

    x=1
    for i in t:
        print ("  %d. %s" % (x, i.splitlines()[0][:70]))
        x+=1

    print ("  0. Quit")

    ans=input("\nWhich reply do you want to use? ")

    if int(ans) > 0 and int(ans) <= len(t):
        print("\n%s" % t[int(ans)-1].splitlines()[0][:70])
        break

    elif ans=="0":
      print("\n Goodbye")
      quit()
    else:
       print("\n ***** Not Valid Choice Try again *****\n\n")


#
# post canned reply and distinguish
#
result = reddit.reply(postToDelete[0], t[int(ans)-1])

if result == {}:
    print ('****** Error replying to post ******')
else:
    #print('replied to (%s) (%s) (%s)\n' % (result['parent'], result['id'], postToDelete[0].title))
    print ('====== Reply successful        ======')

    #
    # find the 'postname' and 'postid' from the reply
    #
    m = re.search(' data-fullname=\"(.*?)\"', result['content'])
    mypostname = m.group(1)
    #print 'mypostname = %s' % mypostname
    if not mypostname:
        print ('Error finding postName in reply result')
        exit(1)

    m = re.search(' name=\"(.*?)\"', result['content'])
    mypostid = m.group(1)
    #print 'mypostid = %s' % mypostid
    if not mypostid:
        print ('Error finding postId in reply result')
        exit(1)

    #
    # distinguish reply
    #
    reply       = Post()
    reply.name  = mypostname
    reply.id    = mypostid
    if reddit.distinguish(reply):
        print ('====== Distinguish successful  ======')
    else:
        print ('****** Error distinguishing reply ******')

    #
    # remove post
    #
    if reddit.remove(postToDelete[0]):
        print ('====== Post removal successful ======')
    else:
        print ('****** Error removing post ******')


print ('\n')



