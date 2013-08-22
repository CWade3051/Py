# This is example code for use with the Wing IDE tutorial, which
# is accessible from the Help menu of the IDE

import time
import unittest
import example1


class CWindowTests(unittest.TestCase):
  """ Tests for example1.py. """

  #-----------------------------------------------------------------------
  def setUp(self):

    self.start_time = time.time()
    
  #-----------------------------------------------------------------------
  def tearDown(self):

    print("Time elapsed:", time.time()-self.start_time)

  #-----------------------------------------------------------------------
  def testGetItemCount(self):

    assert example1.GetItemCount() == 5

  #----------------------------------------------------------------------
  def testReadPythonNews(self):
    
    
    news = example1.ReadPythonNews(5)
    assert len(news) == 5
    
    for news_item in news:
      assert len(news_item) == 3 and isinstance(news_item, list)
      for field in news_item:
        assert field is not None
        
  #----------------------------------------------------------------------
  def testFailure(self):

    print("testing")
    print("about to fail")
    
    assert 0, "Mock test failure"
    