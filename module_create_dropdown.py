import flet as ft
import json


def create_Dropdown(
        columns_to_occupy: float=None,
        field_value: str=None,
        field_textsize: int=None,
        field_label: str=None,
        field_labelsize: int=None,
        field_option_source: dict=None,
        field_option_text: str=None,
        field_option_tooltip: str=None,
        dropdown_onchange: any=None,
        condition: dict=None,
        field_visible: bool=True,
        mandatory: bool=False,
    ):
    '''
    Parameter
        - columns_to_occupy: float=None - Number of the columns, representing the space in Responsiverow it will occupy,
        - field_textsize: int=None - Number of the size of the text of the selected option,
        - field_label: str=None - Text to be displayd inside the field, if no option selected, or as field title, if option selected,
        - field_labelsize: int=None - Number of the size of the label,
        - field_option_source: dict=None - Dictionary from which the options will be taken. It comes from the Method 'get_options' of the Class 'Field_Options',
        - field_option_text: str=None - Column name in the 'field_option_source' with the option name,
        - field_option_tooltip: str=None - Column name in the 'field_option_source' with the tooltip to be display in each option,
        - dropdown_onchange: any=None - Function to be triggered when the Dropdown value is changed, as result of option selection
        - condition: dict=None - If the condition is satisfied, another field will be displayed. Template {'equal_to': 'option', 'afected_field': ['variable_for_the_field']}
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


    ##############################################################################################
    # FUNCTIONS USED IN DROPDOWN CONTROL AND OPTIONS
    ##############################################################################################
    def dropdown_onclick(e):
        '''
        Parameter: e
        -
        This function is called by 'Dropdown' event on_click.
        Each option of the Dropdown is involved by a Container. This function add a bottom_border
        to the Container, so it's possible to have a division line between each option.
        '''

        for item in e.control.options:
            item.content.border = ft.Border(bottom=ft.BorderSide(width=0.5, color=ft.colors.TEAL_600))
            e.control.update()
    

    def option_onclick(e):
        '''
        Parameter: e
        -
        This function is called by 'dropdown.Option' event on_click.
        When an option is selected, this function eliminates the bottom_border added by the function 
        'dropdown_onclick'.
        It is needed otherwise the selected item will have a line in the field.
        '''

        e.control.content.border=None
        e.control.update()
    ##############################################################################################
    
    def internal_onchange(e):
        e.control.error_text=None
        e.control.update()

        if condition != None:
            if e.control.value==condition.get('equal_to'):
                for item in condition.get('afected_field'):
                    item.visible=True
                    item.update()
            
            elif e.control.value!=condition.get('equal_to'):
                for item in condition.get('afected_field'):
                    item.visible=False
                    item.update()

    
    
    return ft.Dropdown(
        col=columns_to_occupy,
        text_style=ft.TextStyle(
            color=ft.colors.BLACK, 
            overflow=ft.TextOverflow.FADE, 
            size=field_textsize
        ),
        label=field_label if mandatory==False else f'{field_label} *',
        label_style=ft.TextStyle(
            color=ft.colors.BLACK, 
            bgcolor=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
            size=field_labelsize,
        ),

        tooltip='Select an option',
        border_width=1,
        border_color=getattr(ft.colors, formatting.get('field_border_color')) if formatting != None else None,
        bgcolor=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
        border_radius=ft.border_radius.all(10),
        alignment=ft.alignment.top_left,
        on_click=dropdown_onclick,
        on_change=internal_onchange if dropdown_onchange==None else dropdown_onchange,
        options=[
            ft.dropdown.Option(
                text=option.get(field_option_text),
                on_click=option_onclick,
                data=index,
                content=ft.Container(
                    height=45,
                    width=1000,
                    alignment=ft.alignment.center_left,
                    tooltip=option.get(field_option_tooltip) if field_option_tooltip != None else None,
                    content=ft.Text(
                        value=option.get(field_option_text), 
                        overflow=ft.TextOverflow.ELLIPSIS
                    )
            ),
            ) for index, option in enumerate(field_option_source)
        ] if field_option_source != None else None,
        # error_text='Mandatory field',
        error_style=ft.TextStyle(bgcolor=ft.colors.TEAL_400),
        visible=field_visible,

    )

    
    

    


if __name__ == '__main__':
    
    def main(page: ft.Page):
        
        def imprimir(e):
            x.value=''
            x.update()
        
        x = ft.Dropdown(
            value=None,
            label='xxx',
            options=[
                ft.dropdown.Option(text='Op 1'),
                ft.dropdown.Option(text='Op 2')
            ],
            #on_change=imprimir
        )

        btn = ft.ElevatedButton(on_click=imprimir)

        page.add(x, btn)
    
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
