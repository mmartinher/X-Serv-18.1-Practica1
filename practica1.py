#!/usr/bin/python

import webapp
import urllib

class practica1(webapp.webApp):

	dic_urls = {}
	dic_urls_inv = {}
	seq_number = 0

	def parse (self, request):

		method = request.split(" ", 2)[0]
  
		if method == "GET":
		    	body = request.split(" ",2)[1][1:]
		elif method == "POST":
			body = request.split("\r\n\r\n")[-1]
			body = body.split("url=",2)[-1]
			body = body.split("http%3A%2F%2F",2)[-1]
			body = "http://" + body
		return (method, body)

	def process(self, resourceName):
		(method,body) = resourceName
		if method == "GET":
			if body in self.dic_urls_inv:
				httpCode = "300 Redirect"
				htmlBody = "<html><head><meta http-equiv='refresh' content='0;url=" \
					+ str(self.dic_urls_inv[body]) + "'></head></html>"
			elif body == "":
				httpCode = "200 OK"
				htmlBody = "<html>""<head></head><body>" + str(self.dic_urls) + "<h3>Urls acortadas</h3><form method=post action=http://localhost:1234>" + "url para acortar:<input type = name name = url original></body>"

				return (httpCode, htmlBody)
			else:
				httpCode = "400 ERROR"
				httpBody = "<html>""<head></head><body> resource not found</body>"
		elif method == "POST":
			if body in self.dic_urls:
				httpCode = "200 OK"
				htmlBody = "<html><head></head><h1><a href='" + str(body) + "'>" \
+ "http://localhost:1234/" + str(self.dic_urls[body]) + "-->" \
+ str(body) + "</a></h1></body></html>"
				return (httpCode, htmlBody)
			else:
				try:
					pag = urllib.urlopen(body)
				except IOError:
					httpCode = "400 ERROR"
					htmlBody = "<html><head>Origin page not found</head><body></body>"
					return (httpCode, htmlBody)

				self.dic_urls[body] = self.seq_number
				self.dic_urls_inv[str(self.seq_number)] = body
				self.seq_number += 1
				httpCode = "200 OK"
				htmlBody = "<html><head></head><h1><a href='" + str(body) + "'>" + str(body)+ "-->" + "http://localhost:1234/" + str(self.dic_urls[body]) + "</a></h1></body></html>"
		return (httpCode, htmlBody)

if __name__ == "__main__":
	testWebApp = practica1("localhost", 1234)
