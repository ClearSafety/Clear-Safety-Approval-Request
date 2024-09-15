import flet as ft
import json


def create_ListCheckbox(
        columns_to_occupy: float=None,
        field_label: str=None,
        field_option_source: dict=None,
        field_option_text: str=None,
        field_option_tooltip: str=None,
        field_option_size: int=None,
        field_disable: bool=False,
        condition: dict=None,
        field_visible: bool=True,
        mandatory: bool=False,
        data: list=[],
    ):
    '''
    Parameter
        - columns_to_occupy: float=None - Number of the columns, representing the space in Responsiverow it will occupy,
        - field_label: str=None - Text to be displayd as field title,
        - field_option_source: dict=None - Dictionary from which the options will be taken. It comes from the Method 'get_options' of the Class 'Field_Options',
        - field_option_text: str=None - Column name in the 'field_option_source' with the option name,
        - field_option_tooltip: str=None - Column name in the 'field_option_source' with the tooltip to be display in each option,
        - field_option_size: int=None - Number of the size of the label,
        - field_disable: bool=False - if True, nothing can be typed,
        - condition: dict=None - If the condition is satisfied, another field will be displayed. Template {'equal_to': 'option', 'afected_field': ['variable_for_the_field']}
        - field_visible: bool=True - if False, the field is not displayed,
        - mandatory: bool=False - if True, an * will be added in the end of the label,
        
        - field_prefix: str=None - a character to be displayed in the beginning of the text,
        - field_prefixsize: int=None - Number of the size of the prefix text,
        - field_hintsize: int=None - Number of the size of the text of the hint (a wording displayed if nothing is typed),
        - field_keyboard: str=None - property of the class ft.Keyboard. 'TEXT' is default. It defines the mobile keyboard. Main Options: TEXT, NUMBER, PHONE. For other options: https://flet.dev/docs/reference/types/keyboardtype/
        - field_multiline: bool=False - if True, it allows more than one line
        - field_maxlines: int=None - it deliminates the maximun of lines that the field may increase
        - field_disable: bool=False - if True, nothing can be typed,
        - field_filter: str=None - used to deliminate the value that can be entered. It might be INTEGER OR FLOAT,
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
    

    def checkbox_selection(e):
        status = e.control.value
        label = e.control.label
        checkbox_items = checkbox_list.data
        if status == True:
            checkbox_items.append(label)
        elif status == False:
            checkbox_items.remove(label)


    
    checkbox_list = ft.Stack(
        controls=[
            ft.Container(
                    padding=ft.padding.only(top=15, bottom=15),
                    col=columns_to_occupy,
                    border=ft.Border(
                        top=ft.BorderSide(width=1, color=getattr(ft.colors, formatting.get('field_border_color')) if formatting != None else None),
                        bottom=ft.BorderSide(width=1, color=getattr(ft.colors, formatting.get('field_border_color')) if formatting != None else None),
                        left=ft.BorderSide(width=1, color=getattr(ft.colors, formatting.get('field_border_color')) if formatting != None else None),
                        right=ft.BorderSide(width=1, color=getattr(ft.colors, formatting.get('field_border_color')) if formatting != None else None),
                    ),
                    bgcolor=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
                    border_radius=ft.border_radius.all(10),
                    disabled=field_disable,
                    visible=field_visible,
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Checkbox(
                                label=option.get(field_option_text),
                                label_style=ft.TextStyle(
                                    color=ft.colors.BLACK, 
                                    bgcolor=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
                                    size=field_option_size,
                                ),
                                active_color=ft.colors.TEAL_900,
                                tooltip=option.get(field_option_text),
                                on_change=checkbox_selection,
                            ) for option in field_option_source

                        ] if field_option_source != None else None
                    ),
            ),
            ft.Text(
                value=field_label if mandatory==False else f'{field_label} *',
                bgcolor=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
                size=11,
                offset=ft.Offset(x=0.08,y=-0.4),
                weight=ft.FontWeight.W_600
            ),
        ],
        data=[]
    )

    return checkbox_list
        
    

    


if __name__ == '__main__':
    
    def main(page: ft.Page):


        a =                     create_ListCheckbox(
                        columns_to_occupy=1,
                        field_label='Types Of External Controls On Site'
                    )
        print(type(a)=='flet_core.stack.Stack')
        page.add(
            ft.ResponsiveRow(
                columns=3,
                controls=[
                    create_ListCheckbox(
                        columns_to_occupy=1,
                        field_label='Types Of External Controls On Site'
                    )
                ]
            )
            
        )
    
    ft.app(target=main)
