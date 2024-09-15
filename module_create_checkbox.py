import flet as ft
import json


def create_Checkbox(
        columns_to_occupy: float=None,
        field_label: str=None,
        field_labelsize: int=None,
        field_disable: bool=False,
        field_visible: bool=True,
        mandatory: bool=False,
        
    ):
    '''
    Parameter
        - columns_to_occupy: float=None - Number of the columns, representing the space in Responsiverow it will occupy,
        - field_label: str=None - Text to be displayd inside the field, if nothing is typed, or as field title, if something is typed,
        - field_labelsize: int=None - Number of the size of the label,
        - field_disable: bool=False - if True, nothing can be selected,
        - field_visible: bool=True - if False, the field is not displayed,
        - mandatory: bool=False - if True, an * will be added in the end of the label,
    '''
    

    ##############################################################################################
    # PULL FILE WITH FORMATTING: get static formatting, which does not change according to device
    ##############################################################################################
    try:
        with open('formatting.json', 'r') as file:
            formatting = json.load(file)
            formatting = formatting.get('general')
    except:
        formatting=None
    ##############################################################################################
    
    
    return ft.Container(
        col=columns_to_occupy,
        border=ft.Border(
            top=ft.BorderSide(width=1, color=getattr(ft.colors, formatting.get('field_border_color')) if formatting != None else None),
            bottom=ft.BorderSide(width=1, color=getattr(ft.colors, formatting.get('field_border_color')) if formatting != None else None),
            left=ft.BorderSide(width=1, color=getattr(ft.colors, formatting.get('field_border_color')) if formatting != None else None),
            right=ft.BorderSide(width=1, color=getattr(ft.colors, formatting.get('field_border_color')) if formatting != None else None),
        ),
        bgcolor=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
        border_radius=ft.border_radius.all(10),
        height=49,
        disabled=field_disable,
        visible=field_visible,
        content=ft.Checkbox(
            label=field_label if mandatory==False else f'{field_label} *',
            label_style=ft.TextStyle(
                color=ft.colors.BLACK, 
                bgcolor=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
                size=field_labelsize,
            ),
            active_color=ft.colors.TEAL_900,
            adaptive=True,
        ),
        adaptive=True
    )
    
    
    

    


if __name__ == '__main__':
    
    import json
    # with open('formatting.json', 'r') as file:
    #     formatting = json.load(file)
       
    # def main(page: ft.Page):
        
    #     #####################################################################################################
    #     # ACCESS FORMATTING
    #     #####################################################################################################
    #     with open('formatting.json', 'r') as file:
    #         formatting = json.load(file)
        
    #     general_formatting = formatting.get('general')
        
    #     if 'mobile' in page.client_user_agent.lower() or 'table' in page.client_user_agent.lower():
    #         formatting = formatting.get('mobile')
    #     else:
    #         formatting = formatting.get('computer')
    #     ######################################################################################################
        
        
    #     page.bgcolor=getattr(ft.colors, general_formatting.get('page_bgcolor'))
        

        
    
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER)
