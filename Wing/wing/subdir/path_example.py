# This file is located in a sub-directory to illustrate setting 
# PYTHONPATH in the tutorial, which is accessible from the 
# Help menu in Wing IDE

import xml.sax
import xml.sax.handler

#-----------------------------------------------------------------------
class CHandler(xml.sax.handler.ContentHandler):
  """Parser handler class for parsing news from python.org"""
  
  def __init__(self):
    xml.sax.handler.ContentHandler.__init__(self)
    self.fItems = []
    self.__fCurItem = None
    self.__fText = []
    
  def startElement(self, name, attrs):
    if name == 'item':
      self.__fCurItem = {}
    self.__fText = []
    
  def endElement(self, name):
    if name == 'item':
      self.fItems.append(self.__fCurItem)
      self.__fCurItem = None
    elif self.__fCurItem is not None:
      self.__fCurItem[name] = ''.join(self.__fText).strip()
      
  def characters(self, content):
      self.__fText.append(content)
    
#-----------------------------------------------------------------------
def ParseRDFNews(txt):
  """Utility to parse XML from the python.org RDF news feed"""
  
  news = []
  
  try:
    try:
      h = CHandler()
      p = xml.sax.parseString(txt, h)
    except:
      # This is a common formatting error
      txt = txt.replace('&', '&amp;')
      h = CHandler()
      p = xml.sax.parseString(txt, h)    
  except:
    return kCannedData
  
  for item in h.fItems:
    d = ' '.join(item['pubDate'].split()[:4])
    news.append([d, item['title'], item['guid']])
    
  return news

#-----------------------------------------------------------------------
# Canned data to use when no internet connection is available
kCannedData = [
  ['June 13, 2013 11:43 AM', 'EuroPython 2014/2015 Conference Team Call for Site Proposals', 'http://www.python.org/news/index.html#Thu13June20131143-0400'],
  ['May 15, 2013 5:30 PM', 'Python 3.2.5 and Python 3.3.2 have been released', 'http://www.python.org/news/index.html#Wed15May201322300100'], 
  ['May 15, 2013 1:00 PM', 'Python 2.7.5 released', 'http://www.python.org/news/index.html#Wed15May20131100-0600'], 
  ['May 10, 2013 4:15 PM', 'PyOhio 2013 Call for Proposals due June 1st', 'http://www.python.org/news/index.html#Fri10May20131615-0400'], 
  ['April 6, 2013 4:30 PM', 'Python 3.2.4 and 3.3.1 have been released', 'http://www.python.org/news/index.html#Sat6April201322300200'], 
]

