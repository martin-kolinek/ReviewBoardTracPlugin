from trac.core import Component, implements
from trac.ticket.api import ITicketChangeListener
from trac.config import Option
import urlparse
import requests, urlparse

class ReviewBoardAPI:
	def __init__(self, url, user, password):
		if not url.endswith('/'):
			url = url + '/'
		self.url = url
		self.user = user
		self.password = password
	
	def create_group(self, disp_name, name):
		requests.post(urlparse.urljoin(self.url, "api/groups/"), data={"display_name": disp_name, "name": name}, auth = (self.user, self.password))
		
	def finish_group(self, name):
		resp = requests.put(urlparse.urljoin(self.url, "api/review-requests"), params={"to-groups": name}, auth = (self.user, self.password))
		for id in (x['id'] for x in resp.json()['review_requests']):
			requests.put(urlparse.urljoin(self.url, "api/review-requests/{0}/".format(id)), data={"status":"submitted"}, auth = (self.user, self.password))
		

class ReviewBoard(Component):
	implements(ITicketChangeListener)
	
	rb_server = Option('reviewboardplugin', 'server', None, doc="""Review Board server url""")
	rb_user = Option('reviewboardplugin', 'user', None, doc="""Review Board user name (needs to be able to create groups and modify review requests""")
	rb_pass = Option('reviewboardplugin', 'password', None, doc="""Review Board password""")
	closed_status = Option('reviewboardplugin', 'closestatus', "closed", doc="""Status of ticket which causes all pending review boards to be submitted (default: closed)""")
	
	def __init__(self):
		self.rb = ReviewBoardAPI(self.rb_server, self.rb_user, self.rb_pass)
	
	def ticket_group(self, ticket):
		return "tracticket{0}".format(ticket.id);
	
	def ticket_created(self, ticket):
		self.rb.create_group(u"Trac ticket #{0}: {1}".format(ticket.id, ticket['summary']), self.ticket_group(ticket))
		link = urlparse.urljoin(self.rb.url, "groups/{0}".format(self.ticket_group(ticket)))
		ticket.save_changes(comment="'''[{0} Code reviews]'''".format(link))
	
	def ticket_changed(self, ticket, comment, author, old_values):
		if ticket['status'] == self.closed_status:
			self.rb.finish_group(self.ticket_group(ticket))
	
	def ticket_deleted(self, ticket):
		self.rb.finish_group(self.ticket_group(ticket))

