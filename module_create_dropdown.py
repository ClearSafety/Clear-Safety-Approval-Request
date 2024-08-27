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
        mandatory: bool=False
    ):
    '''
    Parameter
        - columns_to_occupy: float=None - Number of the columns, representing the space in Responsiverow it will occupy,
        - field_textsize: int=None - Number of the size of the text of the selected option,
        - field_label: str=None - Text to be displayd inside the field, if no option selected, or as field title, if option selected,
        - field_labelsize: int=None - Number of the size of the label,
        - field_option_source: dict=None - Dictionary from which the options will be taken,
        - field_option_text: str=None - Column name in the 'field_option_source' with the option name,
        - field_option_tooltip: str=None - Column name in the 'field_option_source' with the tooltip to be display in each option,
        - dropdown_onchange: any=None - Function to be triggered when the Dropdown value is changed, as result of option selection
    
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
    
    def error_text_delete(e):
        e.control.error_text=None
        e.control.update()
    
    
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
        on_change=error_text_delete if dropdown_onchange==None else dropdown_onchange,
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
        error_style=ft.TextStyle(bgcolor=ft.colors.TEAL_400)

    )

    
    

    


if __name__ == '__main__':
    
    import json
    with open('formatting.json', 'r') as file:
        formatting = json.load(file)
    


    lista = [
        {'SOR': 1, 'Description': '3 star PPM with all IOT  SASS fee and equipment charge included (vericon BCM x1 Micro dot autofill 2 switch live from controls  to be wired into BSM ) (order A)'},
        {'SOR': 2, 'Description': '3 star PPM with all IOT  SASS fee and equipment charge included (vericon BCM x1 Micro dot autofill 2 switch live from controls  to be wired into BSM ) (order B)'},
        {'SOR': 3, 'Description': '3 star PPM with all IOT  SASS fee and equipment charge included (vericon BCM x1 Micro dot autofill 2 switch live from controls  to be wired into BSM ) (order C)'},
        {'SOR': 4, 'Description': '3 star PPM with all IOT  SASS fee and equipment charge included (vericon BCM x1 Micro dot autofill 2 switch live from controls  to be wired into BSM ) (order D)'},
        {'SOR': 5, 'Description': 'D'},
        {'SOR': 6, 'Description': 'E'},
        {'SOR': 7, 'Description': 'F'},
        {'SOR': 8, 'Description': 'G'},
        {'SOR': 9, 'Description': 'H'},
        {'SOR': 10, 'Description': 'I'}
    ]
    
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


        def dropdown_onclick(e):
            for item in e.control.options:
                item.content.italic=True
            e.control.update()
        
        def option_onclick(e):
            e.control.content.italic=False
            e.control.update()
        

        page.add(
            
            ft.ResponsiveRow(
                columns=3,
                width=600,
                controls=[
                    create_Dropdown(
                        field_label='SOR Code',
                        field_labelsize=formatting.get('field_label_size'),
                        field_textsize=formatting.get('field_text_size'),
                        columns_to_occupy=1,
                        field_option_source=lista,
                        field_option_text='SOR',
                        field_option_tooltip='Description',
                        
                    ),
                    
                ]
            )
        )
    
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
