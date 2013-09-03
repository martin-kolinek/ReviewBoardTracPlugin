This is a simple trac plugin which creates new review groups on a review board server based on tickets.

To use it install it like any other trac plugin and then add something like:

    [reviewboardplugin]
    server = http://reviewboard:8080/
    user = hello
    password = world
	
to trac.ini.

Also there is a draft of svn post-commit hook in utils directory which would categorize commits into review groups based on referenced tickets.
