'''
Created on 21.01.2010

@author: Riivo
'''
import config

class Ouput:
  
  def __init__(self):
    self.head = "<html><head><title>clickstream apriori</title></head><body>"
    self.footer = "</body></html>"
    self.content = ""
    
  def to_file(self):
    out_file = open(config.OUTPUT, "w+")
    out_file.write(self.head)
    out_file.write(self.content)
    out_file.write(self.footer)
    out_file.close()
    
    
  def p(self, title):
    self.content += "{0}<br/>".format(title)
         
  def h1(self, title):
    self.content += "<h1>{0}</h1>".format(title)
    
  def hr(self):
    self.content += "<hr />"
    
  def tbl(self):
    self.content += "<table border='1'>"
    
  def e_tbl(self):
    self.content += "</table>"
    

  def tr(self, cells):
    self.content += "<tr>"
    for c in cells:
      self.content += "<td>{0}</td>".format(c)
    self.content += "<td>"
    
  
    