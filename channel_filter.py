__module_name__ = "ChannelFilter" 
__module_version__ = "0.1" 
__module_description__ = "Filters channel messages" 

 
import xchat
import re
from configobj import ConfigObj


def ignore_channel (word, word_eol, userdata):
	"""
		Checks if message should be ignored:
		-full ignore means that the message won't be printed at all
		-soft ignore means that the message will be printed but won't be send
		  to any other plugins thus preventing any notification that the xchat might send
	"""
	nickname = remove_colours_from_nickname(word[0])
	if full_ignore(nickname):
		return xchat.EAT_ALL
	elif soft_ignore(nickname):		
		return xchat.EAT_PLUGIN

	return xchat.EAT_NONE


def soft_ignore(nick):
	"""
		Checks if message should be soft ignored
	"""
	global _ignore_list
	if (xchat.get_info('channel') in _ignore_list['soft']['channels']) or (nick in _ignore_list['soft']['users']):
		return True
	return False


def full_ignore(nick):
	"""
		Checks if message should be fully ignored
	"""
	global _ignore_list
	if (xchat.get_info('channel') in _ignore_list['full']['channels']) or (nick in _ignore_list['full']['users']):
		return True
	return False


def remove_colours_from_nickname(nickname):
	"""
		Removes the colors from the nickname
	"""
	p = re.compile('\\x02|\\x16|\\x1f|\\x03(([0-9]{1,2})?(,[0-9]{1,2})?)?')
	return p.sub('',nickname)


#keeps the information with channels and users 
#for ignore read from the config
_ignore_list = {
	'full' : {
		'channels' : set(),
		'users' : set()
	},
	'soft' : {
		'channels' : set(),
		'users' : set()
	}
}

try:
	config = ConfigObj(xchat.get_info('xchatdir') + '/channel_filter.conf')
except:
	print "[ChannelFilter] Couldn't parse the config file!"
	config = {}

has_anything_to_filter = False

#get full ignore
if 'FullIgnore' in  config:

	#get full ignore channels
	if 'channels' in config['FullIgnore']:
		if type(config['FullIgnore']['channels']) is list:
			# prepend # to channel names
			channels = ['#' + channel for channel in config['FullIgnore']['channels']]
			_ignore_list['full']['channels'] = set(channels)
		else:
			_ignore_list['full']['channels'].add('#' + config['FullIgnore']['channels'])
		print "[ChannelFilter] channels to fully filter: " + ', '.join(_ignore_list['full']['channels'])
		has_anything_to_filter = True

	#get full ignore users
	if 'users' in config['FullIgnore']:
		if type(config['FullIgnore']['users']) is list:
			_ignore_list['full']['users'] = set(config['FullIgnore']['users'])
		else:
			_ignore_list['full']['users'].add(config['FullIgnore']['users'])
		print "[ChannelFilter] users to fully filter: " + ', '.join(_ignore_list['full']['users'])		
		has_anything_to_filter = True

#get soft ignore
if 'SoftIgnore' in  config:

	#get soft ignore channels
	if 'channels' in config['SoftIgnore']:
		if type(config['SoftIgnore']['channels']) is list:
			# prepend # to channel names
			channels = ['#' + channel for channel in config['SoftIgnore']['channels']]
			_ignore_list['soft']['channels'] = set(channels)
		else:
			_ignore_list['soft']['channels'].add('#' + config['SoftIgnore']['channels'])
		print "[ChannelFilter] channels to soft filter: " + ', '.join(_ignore_list['soft']['channels'])
		has_anything_to_filter = True

	#get soft ignore users
	if 'users' in config['SoftIgnore']:
		if type(config['SoftIgnore']['users']) is list:
			_ignore_list['soft']['users'] = set(config['SoftIgnore']['users'])
		else:
			_ignore_list['soft']['users'].add(config['SoftIgnore']['users'])
		print "[ChannelFilter] users to soft filter: " + ', '.join(_ignore_list['soft']['users'])
		has_anything_to_filter = True


if (has_anything_to_filter) :
	xchat.hook_print("Channel Message", ignore_channel)
else:
	print "[ChannelFilter]: No channels or users to filter."

print __module_name__ + " v" + __module_version__ + " loaded"
