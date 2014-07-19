RedditCannedReplies
===================

Given a reddit post URL, the script will make a distinguished comment and remove the post.

Requirements:

1. ReddiWrap library.
2. Must be a moderator.
3. List of canned replies contained in CannedReplies.txt
    

Usage:

1. Edit USERNAME and PASSWORD vars in CannedReply.py.
2. Run CannedReply.py <url of post to comment/delete>

The script will validate the url supplied via the command line and print a menu of canned replies to use as a comment reply.  The comment will be distinguished and the post will be removed.

TODO:  Instead of a CLI, create a GUI and use drag/drop to supply the reddit post url.
