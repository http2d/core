# Macros
#
INTERNAL_ISSUE = """The server found an internal problem.
"""

CODING_BUG = """Looks like a bug in the plug-in that you're trying to
use. Please report it to its author or maintainer so he can fix it
up."""

SYSTEM_ISSUE = """The issue seems to be related to your system."""

UNKNOWN_CAUSE = """We are not sure why this happened. (To-do)."""

BROKEN_CONFIG = """The configuration file seems to be broken."""


# cherokee/source.c
#
e('SOURCE_NONBLOCK',
  title = "Failed to set nonblocking (fd=%d): ${errno}",
  desc  = SYSTEM_ISSUE)



# cherokee/rrd_tools.c
#
e('RRD_NO_BINARY',
  title = "Couldn't find the rrdtool binary.",
  desc  = "A custom rrdtool binary has not been defined, and the server could not find one in the $PATH.",
  debug = "PATH=%s")

e('RRD_EXECV',
  title = "execv failed cmd='%s': ${errno}",
  desc  = SYSTEM_ISSUE)

e('RRD_FORK',
  title = "Fork failed pid=%d: ${errno}",
  desc  = SYSTEM_ISSUE)

e('RRD_WRITE',
  title = "Cannot write in %s: ${errno}",
  desc  = SYSTEM_ISSUE)

e('RRD_MKDIR_WRITE',
  title = "Cannot write in the '%s' directory",
  desc  = SYSTEM_ISSUE)


# cherokee/balancer_round_robin.c
#
e('BALANCER_IP_REACTIVE',
  title = "Taking source='%s' back on-line: %d active.",
  desc  = "The server is re-enabling one of the Information Sources.")

e('BALANCER_IP_DISABLE',
  title = "Taking source='%s' off-line. Active %d.",
  desc  = "The server is disabling one of the Information Sources.")

e('BALANCER_IP_EXHAUSTED',
  title = "Sources exhausted: re-enabling one.",
  desc  = "All the information sources are disabled at this moment. Cherokee needs to re-enable at least one.")


# cherokee/resolv_cache.c
#
e('RESOLVE_TIMEOUT',
  title = "Timed out while resolving '%s'",
  desc  = "For some reason, Cherokee could not resolve the hostname.")


# cherokee/validator_pam.c
#
e('VALIDATOR_PAM_DELAY',
  title = "Setting pam fail delay failed",
  desc  = "Cherokee could not configure PAM propertly. Most likely you have found an incompatibility issue between Cherokee and your system PAM library.")

e('VALIDATOR_PAM_AUTH',
  title = "User '%s' - not authenticated: %s",
  desc  = "(to-do)")

e('VALIDATOR_PAM_ACCOUNT',
  title = "User '%s' - invalid account: %s",
  desc  = "The specified user does not exist on the sytem.")


# cherokee/validator_ldap.c
#
e('VALIDATOR_LDAP_PROPERTY',
  title = "The LDAP validation module requires a '%s' property",
  desc  = "It looks like you did not fill a required property, please.. (to-do)")

e('VALIDATOR_LDAP_SECURITY',
  title = "Security problem found in LDAP validation config",
  desc  = "LDAP validator: Potential security problem found: anonymous bind validation. Check (RFC 2251, section 4.2.2)")

e('VALIDATOR_LDAP_CONNECT',
  title = "Could not connect to LDAP: %s:%d: '${errno}'",
  desc = SYSTEM_ISSUE)

e('VALIDATOR_LDAP_V3',
  title = "Could not set the LDAP version 3: %s",
  desc = SYSTEM_ISSUE)

e('VALIDATOR_LDAP_CA',
  title = "Could not set CA file %s: %s",
  desc = SYSTEM_ISSUE)

e('VALIDATOR_LDAP_STARTTLS',
  title = "Can't StartTLS, it isn't supported by LDAP client libraries",
  desc = SYSTEM_ISSUE)

e('VALIDATOR_LDAP_BIND',
  title = "Could not bind (%s:%d): %s:%s : %s",
  desc = SYSTEM_ISSUE)

e('VALIDATOR_LDAP_SEARCH',
  title = "Could not search in LDAP server: %s",
  desc = SYSTEM_ISSUE)


# cherokee/validator_file.c
#
e('VALIDATOR_FILE',
  title = "Unknown path type '%s'",
  desc  = BROKEN_CONFIG)

e('VALIDATOR_FILE_NO_FILE',
  title = "File based validators need a password file",
  desc  = "This validation modules reads a local file in order to get the authorizated user list. The configuration specifies no file, bla, bla (to-do).")


# cherokee/downloader.c
#
e('DOWNLOADER_OVERWRITE_POST',
  title = "Overwriting post info",
  desc  = CODING_BUG)


# cherokee/admin_client.c
#
e('ADMIN_CLIENT_INTERNAL',
  title = "Internal error",
  desc  = CODING_BUG)

e('ADMIN_CLIENT_BAD_RESPONSE',
  title = "Uknown response len(%d): '%s'",
  desc  = CODING_BUG)

e('ADMIN_CLIENT_LITERAL',
  title = "Could not find len(%d):'%s' in len(%d):'%s'",
  desc  = CODING_BUG)


# cherokee/handler_*.c
#
e('HANDLER_REGEX_GROUPS',
  title = "Too many groups in the regex",
  desc  = "(to-do)")

e('HANDLER_NO_BALANCER',
  title = "The handler needs a balancer",
  desc  = BROKEN_CONFIG)


# cherokee/handler_secdownload.c
#
e('HANDLER_SECDOWN_SECRET',
  title = "Handler secdownload needs a secret",
  desc  = "You must define a passphrase. .. (to-do).")


# cherokee/handler_server_info.c
#
e('HANDLER_SRV_INFO_MOD',
  title = "Unknown module type (%d)",
  desc  = CODING_BUG)

e('HANDLER_SRV_INFO_TYPE',
  title = "Unknown ServerInfo type: '%s'",
  desc  = "(to-do)")


# cherokee/handler_file.c
#
e('HANDLER_FILE_TIME_PARSE',
  title = "Unparseable time '%s'")


# cherokee/handler_fcgi.c
#
e('HANDLER_FCGI_VERSION',
  title = "Parsing error: unknown version")

e('HANDLER_FCGI_PARSING',
  title = "Parsing error: unknown type")

e('HANDLER_FCGI_STDERR',
  title = "%s")

e('HANDLER_FCGI_BALANCER',
  title = "Found a FastCGI handler without a Load Balancer",
  desc  = BROKEN_CONFIG)



# cherokee/handler_error_redir.c
#
e('HANDLER_ERROR_REDIR_CODE',
  title = "Wrong error code: '%s'",
  desc  = BROKEN_CONFIG)

e('HANDLER_ERROR_REDIR_URL',
  title = "HTTP Error %d redirection: An 'url' property is required",
  desc  = BROKEN_CONFIG)


# cherokee/handler_dirlist.c
#
e('HANDLER_DIRLIST_THEME',
  title = "Couldn't load theme '%s': %s",
  desc  = "(to-do).")

e('HANDLER_DIRLIST_BAD_THEME',
  title = "The theme is incomplete",
  desc  = "(to-do).")


# cherokee/handler_dbslayer.c
#
e('HANDLER_DBSLAYER_LANG',
  title = "Unrecognized language '%s'",
  desc  = "Cherokee's DBSlayer supports a number of output languages and formats, including: ..(to-do).")

e('HANDLER_DBSLAYER_BALANCER',
  title = "DBSlayer handler needs a balancer",
  desc  = "(to-do).")


# cherokee/handler_custom_error.c
#
e('HANDLER_CUSTOM_ERROR_HTTP',
  title = "Handler custom error needs an HTTP error value.",
  desc  = BROKEN_CONFIG)


# cherokee/handler_cgi.c
#
e('HANDLER_CGI_SET_PROP',
  title = "Setting pipe properties fd=%d: '${errno}'",
  desc  = SYSTEM_ISSUE)

e('HANDLER_CGI_SETID',
  title = "%s: couldn't set UID %d",
  desc  = "Most probably the server isn't running as root, and therefore it cannot switch to a new user. If you want Cherokee to be able to change use UID to execute CGIs, you'll have to run it as root.")

e('HANDLER_CGI_EXECUTE',
  title = "Could not execute '%s': %s",
  desc  = SYSTEM_ISSUE)

e('HANDLER_CGI_CREATEPROCESS',
  title = "CreateProcess error: error=%d",
  desc  = SYSTEM_ISSUE)

e('HANDLER_CGI_GET_HOSTNAME',
  title = "Error getting host name.",
  desc  = SYSTEM_ISSUE)



# cherokee/config_entry.c
#
e('CONFIG_ENTRY_BAD_TYPE',
  title = "Wrong plug-in: The module must implement a handler.",
  desc  = "The server tried to set a handler, but the loaded plug-in contained another sort of module.")


# cherokee/balancer_*.c
#
e('BALANCER_EMPTY',
  title = "The Load Balancer cannot be empty",
  desc  = BROKEN_CONFIG)

e('BALANCER_UNDEFINED',
  title = "Balancer defined without a value",
  desc  = BROKEN_CONFIG)

e('BALANCER_NO_KEY',
  title = "Balancer: No '%s' log has been defined.",
  desc  = BROKEN_CONFIG)

e('BALANCER_BAD_SOURCE',
  title = "Could not find source '%s'",
  desc  = "For some reason the load balancer module is using a missing Information Source. Please.. (to-do).")

e('BALANCER_ONLINE_SOURCE',
  title = "Taking source='%s' back on-line",
  desc  = "The information source is being re-enabled.")

e('BALANCER_OFFLINE_SOURCE',
  title = "Taking source='%s' back on-line",
  desc  = "The information source is being disabled.")

e('BALANCER_EXHAUSTED',
  title = "Sources exhausted: re-enabling one.",
  desc  = "All the Information Sources have been off-lined. The server needs to re-enable at least one of them.")


# cherokee/encoder_*.c
#
e('ENCODER_DEFLATEINIT2',
  title = "deflateInit2(): %s",
  desc  = SYSTEM_ISSUE)

e('ENCODER_DEFLATEEND',
  title = "deflateEnd(): %s",
  desc  = SYSTEM_ISSUE)

e('ENCODER_DEFLATE',
  title = "deflate(): err=%s, avail=%d",
  desc  = SYSTEM_ISSUE)


# cherokee/logger_*.c
#
e('LOGGER_NO_KEY',
  title = "Logger: No '%s' log has been defined.",
  desc  = BROKEN_CONFIG)


# cherokee/logger_custom.c
#
e('LOGGER_CUSTOM_NO_TEMPLATE',
  title = "A template is needed for logging connections: %s",
  desc  = "You have to write a template for the server to... (to-do)")

e('LOGGER_CUSTOM_TEMPLATE',
  title = "Couldn't parse custom log: '%s'",
  desc  = "The server found a problem while processing the logging template. Please, check it and.. (to-do).")


# cherokee/fdpoll-epoll.c
#

e('FDPOLL_EPOLL_CTL_ADD',
  title = "epoll_ctl: ep_fd %d, fd %d: '${errno}'",
  desc  = SYSTEM_ISSUE)

e('FDPOLL_EPOLL_CTL_DEL',
  title = "epoll_ctl: ep_fd %d, fd %d: '${errno}'",
  desc  = SYSTEM_ISSUE)

e('FDPOLL_EPOLL_CTL_MOD',
  title = "epoll_ctl: ep_fd %d, fd %d: '${errno}'",
  desc  = SYSTEM_ISSUE)

e('FDPOLL_EPOLL_CREATE',
  title = "epoll_create: %d: '${errno}'",
  desc  = SYSTEM_ISSUE)

e('FDPOLL_EPOLL_CLOEXEC',
  title = "Could not set CloseExec to the epoll descriptor: fcntl: '${errno}'",
  desc  = SYSTEM_ISSUE)

# cherokee/fdpoll-port.c
#
e('FDPOLL_PORTS_FD_ASSOCIATE',
  title = "fd_associate: fd %d: '${errno}'",
  desc  = SYSTEM_ISSUE)

e('FDPOLL_PORTS_ASSOCIATE',
  title = "port_associate: fd %d: '${errno}'",
  desc  = SYSTEM_ISSUE)

e('FDPOLL_PORTS_GETN',
  title = "port_getn: '${errno}'",
  desc  = SYSTEM_ISSUE)


# cherokee/fdpoll-poll.c
#
e('FDPOLL_POLL_FULL',
  title = "The FD Poll is full",
  desc  = "The server reached the file descriptor limit. That is usually due to..(to-do). Try to increase the limit..(to-do)")

e('FDPOLL_POLL_DEL',
  title = "Could not remove fd %d (idx=%d) from the poll",
  desc  = CODING_BUG)


# cherokee/fdpoll-kqueue.c
#
e('FDPOLL_KQUEUE',
  title = "kevent returned: '${errno}'",
  desc  = SYSTEM_ISSUE)


# cherokee/gen_evhost.c
#
e('GEN_EVHOST_TPL_DROOT',
  title = "EvHost needs a 'tpl_document_root property'",
  desc  = BROKEN_CONFIG)

e('GEN_EVHOST_PARSE',
  title = "EvHost: Couldn't parse template '%s'",
  desc  = "Could not parse the template definining how virtual servers are located. (to-do).")


# cherokee/vrule_*.c
#
e('VRULE_NO_PROPERTY',
  title = "Virtual Server Rule prio=%d needs a '%s' property",
  desc  = BROKEN_CONFIG)


# cherokee/vrule_target_ip.c
#
e('VRULE_TARGET_IP_PARSE',
  title = "Couldn't parse 'to' entry: '%s'",
  desc  = BROKEN_CONFIG)


# cherokee/vrule_rehost.c
#
e('VRULE_REHOST_NO_DOMAIN',
  title = "Virtual Server '%s' regex vrule needs a 'domain' entry",
  desc  = BROKEN_CONFIG)


# cherokee/rule_*.c
#
e('RULE_NO_PROPERTY',
  title = "Rule prio=%d needs a '%s' property",
  desc  = BROKEN_CONFIG)


# cherokee/rule_request.c
#
e('RULE_REQUEST_NO_TABLE',
  title = "Could not access to the RegEx table",
  desc  = CODING_BUG)

e('RULE_REQUEST_NO_PCRE_PTR',
  title = "RegExp rule has null pcre",
  desc  = CODING_BUG)


# cherokee/rule_method.c
#
e('RULE_METHOD_UNKNOWN',
  title = "Could not recognize HTTP method '%s'",
  desc  = "The rule found an entry with an unsupported HTTP method. Probably this is due to... (to-do).")


# cherokee/rule_header.c
#
e('RULE_HEADER_UNKNOWN',
  title = "Unknown header '%s'",
  desc  = "The rule found an entry with an unsupported header. Probably this is due to... (to-do).")


# cherokee/rule_from.c
#
e('RULE_FROM_ENTRY',
  title = "Couldn't parse 'from' entry: '%s'",
  desc  = "The entries of this rule must be either IP address or network masks. Both IPv4 and IPv6 addresses and masks are supported.")

# cherokee/rule_bind.c
#
e('RULE_BIND_PORT',
  title = "Rule prio=%d type='bind', invalid port='%s'",
  desc  = BROKEN_CONFIG)


# cherokee/server.c
#
e('SERVER_INITGROUPS',
  title = "initgroups: Unable to set groups for user `%s' and GID %d",
  desc  = SYSTEM_ISSUE)

e('SERVER_SETGID',
  title = "Can't change group to GID %d, running with GID=%d",
  desc  = "Most probably you the server did not have enough permissions to change its execution group.")

e('SERVER_SETUID',
  title = "Can't change group to UID %d, running with UID=%d",
  desc  = "Most probably you the server did not have enough permissions to change its execution user.")

e('SERVER_GET_FDLIMIT',
  title = "Could not get File Descriptor limit",
  desc  = SYSTEM_ISSUE,
  debug = "poll_type = %d")

e('SERVER_FDS_SYS_LIMIT',
  title = "The server FD limit seems to be higher than the system limit",
  desc  = "The opened file descriptor limit of the server is %d, while the limit of the system is %d. This is an unlikely situation. You could try to raise the opened file descriptor limit of your system.")

e('SERVER_THREAD_POLL',
  title = "The FD limit of the thread is greater than the limit of the poll",
  desc  = "It seems that an internal server thread assumed a file descriptor limit of %d. However, its FD poll has a lower limit of %d descriptors. The limit has been reduced to the poll limit.")

e('SERVER_NEW_THREAD',
  title = "Could not create a cherokee_thread_t",
  desc  = "This is a extremely unusual error. For some reason the server could not create a thread while launching the server.",
  debug = "ret = %d")

e('SERVER_TLS_INIT',
  title = "Can not initialize TLS for `%s' virtual host",
  desc  = "(To-Do)")

e('SERVER_FD_SET',
  title = "Unable to raise file descriptor limit to %d",
  desc  = SYSTEM_ISSUE)

e('SERVER_FD_GET',
  title = "Unable to read the file descriptor limit of the system",
  desc  = SYSTEM_ISSUE)

e('SERVER_LOW_FD_LIMIT',
  title = "The number of available file descriptors is too low",
  desc  = "The number of available file descriptors: %d, is too low. At least there should be %d available. Please, try to raise your system file descriptor limit.")

e('SERVER_UID_GET',
  title = "Could not get information about the UID %d",
  desc  = SYSTEM_ISSUE)

e('SERVER_CHROOT',
  title = "Could not chroot() to '%s': '${errno}'",
  desc  = SYSTEM_ISSUE)

e('SERVER_CHDIR',
  title = "Could not chdir() to '%s': '${errno}'",
  desc  = SYSTEM_ISSUE)

e('SERVER_SOURCE',
  title = "Invalid Source entry '%s'",
  desc  = BROKEN_CONFIG)

e('SERVER_SOURCE_TYPE',
  title = "Source %d: An entry 'type' is required",
  desc  = BROKEN_CONFIG)

e('SERVER_SOURCE_TYPE_UNKNOWN',
  title = "Source %d has an unknown type: '%s'",
  desc  = BROKEN_CONFIG)

e('SERVER_VSERVER_PRIO',
  title = "Invalid Virtual Server entry '%s'",
  desc  = BROKEN_CONFIG)

e('SERVER_NO_VSERVERS',
  title = "No virtual hosts have been configured",
  desc  = "There should exist at least one virtual server.")

e('SERVER_NO_DEFAULT_VSERVER',
  title = "Lowest priority virtual server must be 'default'",
  desc  = "The lowest priority virtual server should be named 'default'.")

e('SERVER_FORK',
  title = "Could not fork()",
  desc  = SYSTEM_ISSUE)

e('SERVER_PANIC',
  title = "Could not execute the Panic handler: '%s', status %d",
  desc  = "Something happened with the server, and it felt panic. It tried to call an external program to report it to the administrator, but it failed.")


# cherokee/source_interpreter.c
#
e('SRC_INTER_NO_USER',
  title = "User '%s' not found in the system",
  desc  = "The server is configured to execute an interpreter as a different user. However, it seems that the user does not exist in the system.",
  admin = "/source/%d")

e('SRC_INTER_NO_GROUP',
  title = "Group '%s' not found in the system",
  desc  = "The server is configured to execute an interpreter as a different group. However, it seems that the group does not exist in the system.",
  admin = "/source/%d")

e('SRC_INTER_EMPTY_INTERPRETER',
  title = "There is a 'Interpreter Source' witout an interpreter.",
  desc  = "The server configuration defines an 'interpreter' information source that does not specify an interpreter.",
  admin = "/source/%d")

e('SRC_INTER_NO_INTERPRETER',
  title = "Couldn't find interpreter '%s'",
  desc  = "The server configuration refers to an interpreter that is not installed in this system.",
  admin = "/source/%d")

e('SRC_INTER_SPAWN',
  title = "Could not spawn '%s'",
  desc  = SYSTEM_ISSUE)


# cherokee/config_reader.c
#
e('CONF_READ_ACCESS_FILE',
  title = "Could not access file",
  desc  = "The configuration file '%s' could not be accessed. Most probably the server user doesn't have enough permissions to read it.")

e('CONF_READ_CHILDREN_SAME_NODE',
  title = "'%s' and '%s' as child of the same node",
  desc  = CODING_BUG)

e('CONF_READ_PARSE',
  title = "Parsing error",
  desc  = "The server could not parse the configuration. Something must be wrong with formation. At this stage the lexical is checked.",
  debug = "%s")


# cherokee/post.c
#
e('POST_REMOVE_TEMP',
  title = "Could not remove temporal file",
  desc  = "The temporal file '%s' could not be removed.")


# cherokee/template.c
#
e('TEMPLATE_NO_TOKEN',
  title = "Token not found '%s'",
  desc  = "It seems that the template uses an undefined token.")


# cherokee/spawner.c
#
e('SPAWNER_SHM_INIT',
  title = "Couldn't initialize SHM '%s': ${errno}",
  desc  = SYSTEM_ISSUE)

e('SPAWNER_UNLOCK_SEMAPHORE',
  title = "Couldn't unlock spawning semaphore",
  desc  = SYSTEM_ISSUE)


# cherokee/http.c
#
e('HTTP_UNKNOWN_CODE',
  title = "Unknown HTTP status code %d")


# cherokee/icons.c
#
e('ICONS_NO_DEFAULT',
  title = "A default icon is needed",
  desc  = "Please, specify a default icon. It is the icon that Cherokee will use whenever no other icon is used.",
  admin = "/icons")

e('ICONS_ASSIGN_SUFFIX',
  title = "Couldn't assign suffix '%s' to file '%s'",
  desc  = UNKNOWN_CAUSE,
  admin = "/icons")

e('ICONS_DUP_SUFFIX',
  title = "Duped suffix (case insensitive) '%s', pointing to '%s'",
  desc  = UNKNOWN_CAUSE,
  admin = "/icons")


# cherokee/header.c
#
e('HEADER_EMPTY',
  title = "Calling cherokee_header_parse() with an empty header",
  desc  = CODING_BUG)

e('HEADER_NO_EOH',
  title = "Could not find the End Of Header",
  desc  = CODING_BUG,
  debug = "len=%d, buf=%s")

e('HEADER_TOO_MANY_CRLF',
  title = "Too many initial CRLF",
  desc  = CODING_BUG)

e('HEADER_ADD_HEADER',
  title = "Failed to store a header entry while parsing",
  desc  = CODING_BUG)


# cherokee/socket.c
#
e('SOCKET_NEW_SOCKET',
  title = "Could not create socket: ${errno}",
  desc  = SYSTEM_ISSUE)

e('SOCKET_SET_KEEPALIVE',
  title = "Could not set SO_KEEPALIVE on fd=%d: ${errno}",
  desc  = CODING_BUG)

e('SOCKET_SET_LINGER',
  title = "Could not set SO_LINGER on fd=%d: ${errno}",
  desc  = CODING_BUG)

e('SOCKET_RM_NAGLES',
  title = "Could not disable Nagle's algorithm",
  desc  = SYSTEM_ISSUE)

e('SOCKET_NON_BLOCKING',
  title = "Could not set non-blocking, fd %d",
  desc  = CODING_BUG)

e('SOCKET_NO_SOCKET',
  title = "%s isn't a socket",
  desc  = "The file is supposed to be a Unix socket, although it does not look like one.")

e('SOCKET_REMOVE',
  title = "Could not remove %s",
  desc  = "Could not remove the Unix socket because: ${errno}")

e('SOCKET_WRITE',
  title = "Could not write to socket: write(%d, ..): '${errno}'",
  desc  = CODING_BUG)

e('SOCKET_READ',
  title = "Could not read from socket: read(%d, ..): '${errno}'",
  desc  = CODING_BUG)

e('SOCKET_WRITEV',
  title = "Could not write a vector to socket: writev(%d, ..): '${errno}'",
  desc  = CODING_BUG)

e('SOCKET_CONNECT',
  title = "Could not connect: ${errno}",
  desc  = SYSTEM_ISSUE)

e('SOCKET_BAD_FAMILY',
  title = "Unknown socket family: %d",
  desc  = CODING_BUG)

e('SOCKET_SET_NODELAY',
  title = "Could not set TCP_NODELAY to fd %d: ${errno}",
  desc  = CODING_BUG)

e('SOCKET_RM_NODELAY',
  title = "Could not remove TCP_NODELAY from fd %d: ${errno}",
  desc  = CODING_BUG)

e('SOCKET_SET_CORK',
  title = "Could not set TCP_CORK to fd %d: ${errno}",
  desc  = CODING_BUG)

e('SOCKET_RM_CORK',
  title = "Could not set TCP_CORK from fd %d: ${errno}",
  desc  = CODING_BUG)


# cherokee/thread.c
#
e('THREAD_RM_FD_POLL',
  title = "Couldn't remove fd(%d) from fdpoll",
  desc  = CODING_BUG)

e('THREAD_HANDLER_RET',
  title = "Unknown ret %d from handler %s",
  desc  = CODING_BUG)

e('THREAD_OUT_OF_FDS',
  title = "Run out of file descriptors",
  desc  = "The server is under heavy load and it has run out of file descriptors. It can be fixed by raising the file descriptor limit and restarting the server.",
  admin = "/advanced")

e('THREAD_GET_CONN_OBJ',
  title = "Trying to get a new connection object",
  desc  = "Either the system run out of memory, or you've hit a bug in the code.")

e('THREAD_SET_SOCKADDR',
  title = "Could not set sockaddr",
  desc  = CODING_BUG);


# cherokee/connection.c
#
e('CONNECTION_AUTH',
  title = "Unknown authentication method",
  desc  = "To-do")

e('CONNECTION_LOCAL_DIR',
  title = "Could not build the local directory string",
  desc  = "To-do")

e('CONNECTION_GET_VSERVER',
  title = "Couldn't get virtual server: '%s'",
  desc  = "To-do")


# cherokee/ncpus.c
#
e('NCPUS_PSTAT',
  title = "pstat_getdynamic() failed: '${errno}'",
  desc  = SYSTEM_ISSUE)

e('NCPUS_HW_NCPU',
  title = "sysctl(CTL_HW:HW_NCPU) failed: '${errno}'",
  desc  = SYSTEM_ISSUE)

e('NCPUS_SYSCONF',
  title = "sysconf(_SC_NPROCESSORS_ONLN) failed: '${errno}'",
  desc  = SYSTEM_ISSUE)


# cherokee/init.c
#
e('INIT_CPU_NUMBER',
  title = "Couldn't figure the CPU/core number of your server. Read %d, set to 1")

e('INIT_GET_FD_LIMIT',
  title = "Couldn't get the file descriptor limit of your system",
  desc  = SYSTEM_ISSUE)
  

# cherokee/utils.c
#
e('UTIL_F_GETFL',
  title = "fcntl (F_GETFL, fd=%d, 0): ${errno}",
  desc  = CODING_BUG)

e('UTIL_F_SETFL',
  title = "fcntl (F_GETFL, fd=%d, flags=%d (+%s)): ${errno}",
  desc  = CODING_BUG)

e('UTIL_F_GETFD',
  title = "fcntl (F_GETFD, fd=%d, 0): ${errno}",
  desc  = CODING_BUG)

e('UTIL_F_SETFD',
  title = "fcntl (F_GETFD, fd=%d, flags=%d (+%s)): ${errno}",
  desc  = CODING_BUG)

e('UTIL_MKDIR',
  title = "Could not mkdir '%s': ${errno}",
  desc  = "Most probably there you have to adjust some permissions.")


# cherokee/avl.c
#
e('AVL_PREVIOUS',
  title = "AVL Tree inconsistency: Right child",
  desc  = CODING_BUG)

e('AVL_NEXT',
  title = "AVL Tree inconsistency: Left child",
  desc  = CODING_BUG)

e('AVL_BALANCE',
  title = "AVL Tree inconsistency: Balance",
  desc  = CODING_BUG)


# cherokee/buffer.c
#
e('BUFFER_NEG_ESTIMATION',
  title = "Buffer: Bad memory estimation. The format '%s' estimated a negative length: %d.",
  desc  = CODING_BUG)

e('BUFFER_NO_SPACE',
  title = "Buffer: No target memory. The format '%s' got a free size of %d (estimated %d).",
  desc  = CODING_BUG)

e('BUFFER_BAD_ESTIMATION',
  title = "Buffer: Bad estimation. Too few memory: '%s' -> '%s', esti=%d real=%d size=%d.",
  desc  = CODING_BUG)

e('BUFFER_AVAIL_SIZE',
  title = "Buffer: Bad estimation: Estimation=%d, needed=%d available size=%d: %s.",
  desc  = CODING_BUG)

e('BUFFER_OPEN_FILE',
  title = "Couldn't open the file: %s, ${errno}",
  desc  = "Please check that the file exists and the server has read access.")

e('BUFFER_READ_FILE',
  title = "Could not read from fd: read(%d, %d, ..) = ${errno}",
  desc  = "Please check that the file exists and the server has read access.")


# cherokee/plugin_loader.c
#
UNAVAILABLE_PLUGIN = """Either you are trying to use an unavailable
(uninstalled?) plugin, or there is a installation issue."""

e('PLUGIN_LOAD_NO_SYM',
  title = "Couldn't get simbol '%s': %s",
  desc  = INTERNAL_ISSUE)

e('PLUGIN_DLOPEN',
  title = "Something just happened while opening a plug-in file",
  desc  = "The operating system reported '%s' while trying to load '%s'.")

e('PLUGIN_NO_INIT',
  title = "The plug-in initialization function (%s) could not be found",
  desc  = CODING_BUG)

e('PLUGIN_NO_OPEN',
  title = "Could not open the '%s' module",
  desc  = UNAVAILABLE_PLUGIN)

e('PLUGIN_NO_INFO',
  title = "Could not access the 'info' entry of the %s plug-in",
  desc  = UNAVAILABLE_PLUGIN)


# cherokee/virtual_server.c
#
e('VSERVER_BAD_METHOD',
  title = "Unsupported method '%s'",
  admin = "/vserver/%d/rule/%d",
  desc  = "(TO DO)")

e('VSERVER_TIME_MISSING',
  title = "Expiration time without a 'time' property",
  admin = "/vserver/%d/rule/%d",
  desc  = "(TO DO)")

e('VSERVER_RULE_UNKNOWN_KEY',
  title = "Virtual Server Rule, Unknown key '%s'",
  admin = "/vserver/%d/rule/%d",
  desc  = "(TO DO)")

e('VSERVER_TYPE_MISSING',
  title = "Rule matches must specify a 'type' property",
  admin = "/vserver/%d/rule/%d",
  desc  = "(TO DO)")

e('VSERVER_LOAD_MODULE',
  title = "Could not load rule module '%s'",
  admin = "/vserver/%d",
  desc  = "The server could not load a plug-in file. This might be due to some problem in the installation.")

e('VSERVER_BAD_PRIORITY',
  title = "Invalid priority '%s'",
  admin = "/vserver/%d",
  desc  = "(TO DO)")

e('VSERVER_RULE_MATCH_MISSING',
  title = "Rules must specify a 'match' property",
  admin = "/vserver/%d/rule/%d",
  desc  = "(TO DO)")
  
e('VSERVER_MATCH_MISSING',
  title = "Virtual Server must specify a 'match' property",
  admin = "/vserver/%d",
  desc  = "(TO DO)")

e('VSERVER_UNKNOWN_KEY',
  title = "Virtual Server, Unknown key '%s'",
  admin = "/vserver/%d",
  desc  = "(TO DO)")

e('VSERVER_NICK_MISSING',
  title = "Virtual Server  without a 'nick' property",
  admin = "/vserver/%d",
  desc  = "(TO DO)")

e('VSERVER_DROOT_MISSING',
  title = "Virtual Server  without a 'document_root' property",
  admin = "/vserver/%d",
  desc  = "(TO DO)")


# cherokee/regex.c
#
e('REGEX_COMPILATION',
  title = "Could not compile <<%s>>: %s (offset=%d)",
  desc  = "For some reason, PCRE could not compile the regular expression. Please modify the regular expression in order to solve this problem.")


# cherokee/access.c
#
e('ACCESS_IPV4_MAPPED',
  title = "This IP '%s' is IPv6-mapped IPv6 address",
  desc  = "It can be solved by specifying the IP in IPv4 style: a.b.c.d, instead of IPv6 style: ::ffff:a.b.c.d style")

e('ACCESS_INVALID_IP',
  title = "The IP address '%s' seems to be invalid",
  desc  = "You must have made a mistake. Please, try to fix the IP and try again.")

e('ACCESS_INVALID_MASK',
  title = "The network mask '%s' seems to be invalid",
  desc  = "You must have made a mistake. Please, try to fix the IP and try again.")


# cherokee/bind.c
#
e('BIND_PORT_NEEDED',
  title = "A port entry is need",
  desc  = "It seems that the configuration file includes a port listening entry with the wrong format. It should contain one port specification, but it does not in this case.")

e('BIND_COULDNT_BIND_PORT',
  title = "Could not bind() port=%d (UID=%d, GID=%d)",
  desc  = "Most probably there is another web server listening to the same port. You'll have to shut it down before launching Cherokee. It could also be a permissions issue. Remember that non-root user cannot listen to ports < 1024.")


# cherokee/handler_rrd.c
#
e('HANDLER_RENDER_RRD_EXEC',
  title = "Could not execute RRD command: %s",
  desc  = SYSTEM_ISSUE)

e('HANDLER_RENDER_RRD_EMPTY_REPLY',
  title = "RRDtool empty response",
  desc  = SYSTEM_ISSUE)

e('HANDLER_RENDER_RRD_MSG',
  title = "RRDtool replied an error message: %s",
  desc  = SYSTEM_ISSUE)

e('HANDLER_RENDER_RRD_INVALID_REQ',
  title = "Invalid request: %s",
  desc  = SYSTEM_ISSUE)


# cherokee/collector_rrd.c
#
e('COLLECTOR_COMMAND_EXEC',
  title = "Could not execute RRD command: %s",
  desc  = SYSTEM_ISSUE)

e('COLLECTOR_NEW_THREAD',
  title = "Couldn't create the RRD working thread: error=%d",
  desc  = SYSTEM_ISSUE)

e('COLLECTOR_NEW_MUTEX',
  title = "Couldn't create the RRD working mutex: error=%d",
  desc  = SYSTEM_ISSUE)


# cherokee/validator_mysql.c
#
e('VALIDATOR_MYSQL_HASH',
  title = "Validator MySQL: Unknown hash type: '%s'",
  desc  = CODING_BUG)

e('VALIDATOR_MYSQL_KEY',
  title = "Validator MySQL: Unknown key: '%s'",
  desc  = CODING_BUG)

e('VALIDATOR_MYSQL_USER',
  title = "MySQL validator: a 'user' entry is needed",
  desc  = "Make sure that a valid MySQL user-name has been provided.")

e('VALIDATOR_MYSQL_DATABASE',
  title = "MySQL validator: a 'database' entry is needed",
  desc  = "Make sure that a valid MySQL database-name has been provided.")

e('VALIDATOR_MYSQL_QUERY',
  title = "MySQL validator: a 'query' entry is needed",
  desc  = "Make sure that a MySQL query has been provided.")

e('VALIDATOR_MYSQL_SOURCE',
  title = "MySQL validator misconfigured: A Host or Unix socket is needed.",
  desc  = "Make sure that a working database host is specified for MySQL validation.")

e('VALIDATOR_MYSQL_NOCONN',
  title = "Unable to connect to MySQL server: %s:%d %s",
  desc  = "Most probably the MySQL server is down or you've mistyped a connetion parameter")


# cherokee/error_log.c
#
e('ERRORLOG_PARAM',
  title = "Unknown parameter type '%c'",
  desc  = "Accepted parameter are 's' and 'd'")

# cherokee/cryptor_libssl.c
#
e('SSL_SOCKET',
  title = "Could not get the socket struct: %p",
  desc  = SYSTEM_ISSUE)

e('SSL_SRV_MATCH',
  title = "Servername did not match: '%s'",
  desc  = "(to-do)")

e('SSL_CHANGE_CTX',
  title = "Couldn't change the SSL context: servername='%s'",
  desc  = SYSTEM_ISSUE)

e('SSL_ALLOCATE_CTX',
  title = "OpenSSL: Couldn't allocate OpenSSL context",
  desc  = SYSTEM_ISSUE)

e('SSL_CIPHER',
  title = "OpenSSL: Can not set cipher list '%s': %s",
  desc  = SYSTEM_ISSUE)

e('SSL_CERTIFICATE',
  title = "OpenSSL: Can not use certificate file '%s':  %s",
  desc  = "(to-do)")

e('SSL_KEY',
  title = "OpenSSL: Can not use private key file '%s': %s",
  desc  = "(to-do)")

e('SSL_KEY_MATCH',
  title = "OpenSSL: Private key does not match the certificate public key",
  desc  = "(to-do)")

e('SSL_CA_READ',
  title = "OpenSSL: Can't read trusted CA list '%s': %s",
  desc  = "(to-do)")

e('SSL_CA_LOAD',
  title = "SSL_load_client_CA_file '%s': %s",
  desc  = "(to-do)")

e('SSL_SESSION_ID',
  title = "Unable to set SSL session-id context for '%s': %s",
  desc  = SYSTEM_ISSUE)

e('SSL_SNI',
  title = "Couldn't activate TLS SNI for '%s': %s",
  desc  = SYSTEM_ISSUE)

e('SSL_CONNECTION',
  title = "OpenSSL: Unable to create a new SSL connection from the SSL context: %s",
  desc  = SYSTEM_ISSUE)

e('SSL_FD',
  title = "OpenSSL: Can not set fd(%d): %s",
  desc  = SYSTEM_ISSUE)

e('SSL_INIT',
  title = "Init OpenSSL: %s",
  desc  = SYSTEM_ISSUE)

e('SSL_SW_DEFAULT',
  title = "SSL_write: unknown errno: ${errno}",
  desc  = SYSTEM_ISSUE)

e('SSL_SW_ERROR',
  title = "SSL_write (%d, ..) -> err=%d '%s'",
  desc  = SYSTEM_ISSUE)

e('SSL_SR_DEFAULT',
  title = "SSL_read: unknown errno: ${errno}",
  desc  = SYSTEM_ISSUE)

e('SSL_SR_ERROR',
  title = "OpenSSL: SSL_read (%d, ..) -> err=%d '%s'",
  desc  = SYSTEM_ISSUE)

e('SSL_CREATE_CTX',
  title = "OpenSSL: Unable to create a new SSL context: %s",
  desc  = SYSTEM_ISSUE)

e('SSL_CTX_LOAD',
  title = "OpenSSL: '%s': %s",
  desc  = SYSTEM_ISSUE)

e('SSL_CTX_SET',
  title = "OpenSSL: cannot set certificate verification paths: %s",
  desc  = SYSTEM_ISSUE)

e('SSL_SNI_SRV',
  title = "OpenSSL: Couldn't set SNI server name: %s",
  desc  = "(to-do)")

e('SSL_CONNECT',
  title = "OpenSSL: Can not connect: %s",
  desc  = SYSTEM_ISSUE)

e('SSL_PKCS11',
  title = "Could not init pkcs11 engine",
  desc  = SYSTEM_ISSUE)

e('SSL_DEFAULTS',
  title = "Could not set all defaults",
  desc  = SYSTEM_ISSUE)
