import os
import sys  # Needed to access exception info like line numbers and filenames

class TradingBotException(Exception):  # Inherit from Python's built-in Exception class
    def __init__(self,error_message,error_details:sys):
        self.error_message = error_message  # Store the original error message

         # Extract traceback details using sys module to get line number and filename
        _,_,exc_tb = error_details.exc_info()
        
        # Capture the line number where the exception occurred
        self.lineno=exc_tb.tb_lineno

         # Capture the file name where the exception occurred
        self.file_name=exc_tb.tb_frame.f_code.co_filename 
    
    def __str__(self):
        
        # Custom string representation for logging/debugging
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.lineno, str(self.error_message))
        
        
if __name__ == '__main__':
    try:
        a=1/0  # This will raise a ZeroDivisionError
        print("This will not be printed",a)
    except Exception as e:
        raise TradingBotException(e,sys)  # Converts into your custom error with context
    


