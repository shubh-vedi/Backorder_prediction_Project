import os
import sys
import traceback

class backorderException(Exception):
    
    def __init__(self, error_message:Exception,error_detail:sys): #passed object here one from system module and one to get error message
        super().__init__(error_message) #super to call for pARENT CLASS OBJECT EXCEPTION I.E Exception(error_message)
        self.error_message=backorderException.get_detailed_error_message(error_message=error_message,
                                                                       error_detail=error_detail
                                                                        )


    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_detail:sys)->str:
        """
        error_message: Exception object
        error_detail: object of sys module
        """
        try:
           _,_ ,exec_tb = error_detail.exc_info() #to traceback which line causing error first to blank spaces for type and value given in exc.info
           exception_block_line_number = exec_tb.tb_frame.f_lineno #error for exception block
           try_block_line_number = exec_tb.tb_lineno    #error for which try block (connected above exception block)
           file_name = exec_tb.tb_frame.f_code.co_filename
        except Exception:
            exception_block_line_number = -1
            try_block_line_number = -1
            file_name = "Unknown"

        error_message = f"""
        Error occured in script: 
        [ {file_name} ] at 
        try block line number: [{try_block_line_number}] and exception block line number: [{exception_block_line_number}] 
        error message: [{error_message}]
        """
        return error_message

    def __str__(self): #when we print  object of any calss what that object should print given dunder method
        return self.error_message


    def __repr__(self) -> str:
        return backorderException.__name__
