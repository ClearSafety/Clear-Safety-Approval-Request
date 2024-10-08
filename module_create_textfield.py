import flet as ft
import json


def create_Textfield(
        columns_to_occupy: float=None,
        field_value: str=None,
        field_textsize: int=None,
        field_label: str=None,
        field_labelsize: int=None,
        field_prefix: str=None,
        field_prefixsize: int=None,
        field_hintsize: int=None,
        field_keyboard: str=None,
        field_multiline: bool=False,
        field_maxlines: int=None,
        field_minlines: int=None,
        field_disable: bool=False,
        field_filter: str=None,
        textfield_onchange: any=None,
        condition: dict=None,
        field_visible: bool=True,
        mandatory: bool=False,
        no_capitalization: bool=False
    ):
    '''
    Parameter
        - columns_to_occupy: float=None - Number of the columns, representing the space in Responsiverow it will occupy,
        - field_value: str=None - it might be pre-defined value, that it will initially be displayed, like £0.00
        - field_textsize: int=None - Number of the size of the typed text,
        - field_label: str=None - Text to be displayd inside the field, if nothing is typed, or as field title, if something is typed,
        - field_labelsize: int=None - Number of the size of the label,
        - field_prefix: str=None - a character to be displayed in the beginning of the text,
        - field_prefixsize: int=None - Number of the size of the prefix text,
        - field_hintsize: int=None - Number of the size of the text of the hint (a wording displayed if nothing is typed),
        - field_keyboard: str=None - property of the class ft.KeyboardType. 'TEXT' is default. It defines the mobile keyboard. Main Options: TEXT, NUMBER, PHONE. For other options: https://flet.dev/docs/reference/types/keyboardtype/
        - field_multiline: bool=False - if True, it allows more than one line
        - field_maxlines: int=None - it deliminates the maximun of lines that the field may increase
        - field_disable: bool=False - if True, nothing can be typed,
        - field_filter: str=None - used to deliminate the value that can be entered. It might be INTEGER OR FLOAT,
        - condition: dict=None - If the condition is satisfied, another field will be displayed. Template {'equal_to': 'option', 'afected_field': ['variable_for_the_field']}
        - field_visible: bool=True - if False, the field is not displayed,
        - mandatory: bool=False - if True, an * will be added in the end of the label,
        - no_capitalization: bool=False - if True, Capitalization is not applied
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


    ##############################################################################################
    # FUNCTIONS
    ##############################################################################################
    # Based on the parameter "field_filter", it's applyed a filter to the field.    
    if field_filter != None:
        if field_filter.upper() == 'INTEGER':
            field_filter = ft.NumbersOnlyInputFilter()
            
        elif field_filter.upper() == 'FLOAT':
            field_filter = ft.InputFilter(regex_string=r'^\d*(\.\d{0,2})?$')#, allow=True)#, replacement_string='')
        
        else:
            field_filter=None

    def error_text_delete(e):
        e.control.error_text=None
        
        if condition != None:
            if e.control.value!=condition.get('equal_to'):
                for item in condition.get('afected_field'):
                    item.visible=False
                    item.update()
            
            elif e.control.value==condition.get('equal_to'):
                for item in condition.get('afected_field'):
                    item.visible=True
                    item.update()
        
        
        e.control.update()
    ##############################################################################################
    
    
    return ft.TextField(
        col=columns_to_occupy,
        value=field_value,
        text_style=ft.TextStyle(color=ft.colors.BLACK, overflow=ft.TextOverflow.ELLIPSIS, size=field_textsize),
        label=field_label if mandatory==False else f'{field_label} *',
        label_style=ft.TextStyle(
            color=ft.colors.BLACK, 
            bgcolor=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
            size=field_labelsize,
        ),
        prefix_text=field_prefix,
        prefix_style=ft.TextStyle(color=ft.colors.BLACK, bgcolor=getattr(ft.colors, formatting.get('field_bgcolor')), size=field_prefixsize) if formatting != None else None,
        hint_text=f'Type the {field_label}' if field_label != None else None,
        hint_style=ft.TextStyle(color=ft.colors.GREY_800, italic=True, size=field_hintsize),
        keyboard_type=getattr(ft.KeyboardType, field_keyboard.upper()) if field_keyboard!=None and field_keyboard.upper() in ['TEXT', 'MULTILINE', 'NUMBER', 'PHONE', 'DATETIME', 'EMAIL', 'URL', 'VISIBLE_PASSWORD', 'NAME', 'STREET_ADDRESS', 'NONE'] else None,
        multiline=field_multiline,
        min_lines=field_minlines,
        max_lines=field_maxlines,
        border_width=1,
        border_color=getattr(ft.colors, formatting.get('field_border_color')) if formatting != None else None,
        bgcolor=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
        border_radius=ft.border_radius.all(10),
        capitalization=ft.TextCapitalization.SENTENCES if no_capitalization == False else None,
        cursor_color=getattr(ft.colors, formatting.get('field_cursor_color')) if formatting != None else None,
        disabled=field_disable,
        input_filter=field_filter,
        on_change=error_text_delete if textfield_onchange==None else textfield_onchange,
        #error_text='Mandatory field',
        error_style=ft.TextStyle(bgcolor=ft.colors.TEAL_400),
        visible=field_visible,
        #height=100
    )

    
    
    

    


if __name__ == '__main__':
    
    import json
    with open('formatting.json', 'r') as file:
        formatting = json.load(file)
       
    def main(page: ft.Page):
        
        #####################################################################################################
        # ACCESS FORMATTING
        #####################################################################################################
        with open('formatting.json', 'r') as file:
            formatting = json.load(file)
        
        general_formatting = formatting.get('general')
        
        if 'mobile' in page.client_user_agent.lower() or 'table' in page.client_user_agent.lower():
            formatting = formatting.get('mobile')
        else:
            formatting = formatting.get('computer')
        ######################################################################################################
        
        
        page.bgcolor=getattr(ft.colors, general_formatting.get('page_bgcolor'))
        

        page.add(
            
            ft.ResponsiveRow(
                columns=3,
                width=600,
                controls=[
                    create_Textfield(
                        field_label='Total',
                        field_labelsize=formatting.get('field_label_size'),
                        field_textsize=formatting.get('field_text_size'),
                        field_multiline=True,
                        field_maxlines=5,
                        field_prefix='£',
                        field_prefixsize=10,
                        textfield_onchange=lambda e: print(e.control.value)
                    ),
                
                    
                ]
            )
        )
    
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
