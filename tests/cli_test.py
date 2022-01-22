from io import StringIO
import os, sys
sys.path.insert(1, os.path.abspath('.'))
import cli

class TestCLI:

    def test_Notice(self):
        testMessages = ["test", "Hello World"] 
        testOut = StringIO()
        sys.stdout = testOut
        for Message in testMessages:
            cli.Notice(Message)
            assert testOut.getvalue().split('\n')[-2] == f"{Message}"
        sys.stdout = sys.__stdout__
    
    def test_ClearScreen(self):
        TestOut = StringIO()
        sys.stdout = TestOut
        cli.ClearScreen()
        assert TestOut.getvalue() == ""
        sys.stdout = sys.__stdout__


        

        
