xchat-plugins
=============
Channel Filter:
--------------
  This plugin fillters channel messages (either all messages in a channel or only messages of a list of users)
  
  There are two types of filterig:
  + *full* - doesn't show the message at all
  + *soft* - shows the message but prevent the emmiting of the message to other plugins and thus prevents notifications by the notification plugin
   
  The modes and the channels and users for ignore can be configured in the channel_filter.conf file

####Instalation
Copy channel\_filter.py and channel\_filter.conf to your /.xchat2 directory.
Requires module *re* and *configobj*
