import flet as ft

class Filetype:
    def __init__(self):
        self.forbbiden_extensions = [
        '.exe', '.bat', '.com', '.scr', '.cmd', '.vbs', '.js', '.ps1', 
        '.py', '.wsf', '.iso', '.url', '.lnk', '.dll', '.sys', '.jar']
    
    def safefiletype(self, filename: str) -> bool:
        '''
        This function aims to return a boolean value resulting of checking if the extension file bellongs to 
        one of the extensions listed as forbbiden, because they could be dangerous, like .exe. 
        If the extension belongs to it, it returns False, meaning that the file cannot be used.
        Otherwise, it returns True, meaning it can be used

        Parameter:
        - filename: str - a filename of the format 'name.extension'
        
        Return: 
            - bool - True | False
        ------------
        forbbiden_extensions = ['.exe', '.bat', '.com', '.scr', '.cmd', '.vbs', '.js', '.ps1', '.py', '.wsf', '.iso', '.url', '.lnk', '.dll', '.sys', '.jar']
        '''
        
        extension = '.'+filename.split('.')[-1]
        return extension not in self.forbbiden_extensions

if __name__ == '__main__':
    print(', '.join(Filetype().forbbiden_extensions))
