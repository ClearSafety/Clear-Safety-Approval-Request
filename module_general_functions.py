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



# Function to check mandatory response
def empty_check_mandatory(page, fields, all_prices_breakdown=None):
    
    fields_with_problem = ''
    
    if all_prices_breakdown==None:
        for field in fields:
        
            if field.label[-1] == '*' and (field.value == '' or field.value == None):
                field.error_text='Mandatory field'
                field.update()
                fields_with_problem += (f'- {field.label[:-2]}\n')
    
    elif all_prices_breakdown!=None:
        if len(all_prices_breakdown.controls) == 1:
                fields_with_problem += '- Price Breakdown'
        
        else:
            for item in all_prices_breakdown.controls[:-1]:
                for subitem in item.controls:
                    try:
                        if subitem.label[:-2] in fields:
                            if subitem.label[-1] == '*' and (subitem.value == '' or subitem.value == None):
                                subitem.error_text='Mandatory field'
                                subitem.update()
                                fields_with_problem += (f'- {subitem.label[:-2]}\n')
                    except:
                        pass



    print(fields_with_problem)

    if fields_with_problem != '':
        def close_dialog(e):
            alert.open=False
            page.update()

        alert = ft.AlertDialog(
            title=ft.Text(value='Clear Safety - Approval Request'),
            content=ft.Text(f'Please, fill the mandatory fields:\n{fields_with_problem}'),
            modal=True,
            actions=[
                ft.ElevatedButton(text='Close', on_click=close_dialog)
            ]
        )
        
        page.overlay.append(alert)
        alert.open=True
        page.update()
        
        return True
    else:
        return False



if __name__ == '__main__':
    a = Filetype().safefiletype('xx.exe')
    print(a)
