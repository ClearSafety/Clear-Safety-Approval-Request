import flet as ft
import json
from module_create_textfield import create_Textfield
from module_create_dropdown import create_Dropdown



def create_UpliftGroup(
        page: ft.Page,
        position: int,
        field_textsize: int=None,
        field_labelsize: int=None,
        field_option_source: dict=None,
        field_column_uplift: str=None,
        delete: any=None,
        overal_total: any=None
    ):
    '''
    Parameter
        - page: ft.Page - page object to enable this function update the page where this function has been called,
        - position: int - position of the group to be attributed when it is called. It is useful to find the group to delete,
        - field_textsize: int=None - Number of the size of the text displayed in the field,
        - field_labelsize: int=None - Number of the size of the label,
        - field_option_source: dict=None - Dictionary from which the options of the dropdown fields will be taken (by default, must have the fields 'SOR Code' and 'SOR Description'),
        - field_column_price: str=None - Column name of the field_option_source that has the price,
        - delete: any=None - each group created by this function has a delete button. "delete" as parameter is a function to be created in the main app to be used by this button.
        - overal_total: any=None - This function must be created withing the main app to add up the Total based on the PriceBreakDown. Change the SOR code or quantity is a trigger for this function.
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
    
    # Function to fill SOR Code / Description / Price and to creat a ToolTip
    def dropdown_onchange(e):
        '''
        When an option is selected, this function will search the corresponding selected value in the SOR Code list provided and it will fill
        in the other fields the other values. 
        If "SOR Code" is selected, it will fill "Description" and "Price".
        If "Description" is selected, it will fill "SOR Code" and "Price"
        '''
        
        _sorcode.error_text=None
        _sordescription.error_text=None

        if e.control.label == 'Description':
            try:
                _sorcode.value = list(filter(lambda item: item.get('SOR Description') == e.control.value, field_option_source))[0].get('SOR Code')
                for item in _sorcode.options:
                    item.content.border = None
            except:
                _sorcode.value=None

        elif e.control.label == 'SOR Code':
            try:
                _sordescription.value = list(filter(lambda item: item.get('SOR Code') == e.control.value, field_option_source))[0].get('SOR Description')
                for item in _sordescription.options:
                    item.content.border = None
            except:
                _sordescription.value=None
        
        try: 
            _soruplift.value = f"{list(filter(lambda item: item.get('SOR Code') == pricebreakdown.controls[0].value, field_option_source))[0].get(field_column_uplift)*100:.2f}%"
        except:
            _soruplift.value=None
        
        _sordescription.tooltip = _sordescription.value
        
        # Calling the function that will create a total for the group, by multiplying Price and quantity, and fill the Individual Total
        individual_total()
    #------------------------------------------------------------------------------------------------

        
    # Function to fill individual Total
    def individual_total(e=None):
        '''
        It calculate the Total of the individual pricebreakdown group and display its value in the "Total" field.
        '''
        _sorprice.error_text=None

        if _sorprice.value != '' and _soruplift.value != '':
            try:
                _sortotal.value = f"£{float(_sorprice.value) * (1+float(_soruplift.value.replace('%', ''))/100):.2f}"
                
            except:
                print('error')
        
        else:
            _sortotal.value = f"£0.00"
        
        # Calling the function that is passed as parameter for "create_PriceBreakdownGroup" function. It will sum all the breakdown created and displays the value in na Total Field.
        # This Total Field is not created by the funcion "create_PriceBreakdownGroup".
        if overal_total != None:
            overal_total()
        
        page.update()
    #------------------------------------------------------------------------------------------------

    ##############################################################################################
    

    ##############################################################################################
    # SORT FIELD OPTION SOURCE
    ##############################################################################################    
    try:
        field_option_source_SORCODE = sorted(field_option_source, key=lambda item: item.get('SOR Code'))
        field_option_source_DESCRIPTION = sorted(field_option_source, key=lambda item: item.get('SOR Description'))
    except:
        field_option_source_SORCODE = None
        field_option_source_DESCRIPTION = None


    pricebreakdown = ft.ResponsiveRow(
        col=3,
        columns=3,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            _sorcode := create_Dropdown(
                columns_to_occupy=0.9,
                field_label='SOR Code',
                field_labelsize=field_labelsize,
                field_textsize=field_textsize,
                field_option_source=field_option_source_SORCODE,
                field_option_text='SOR Code',
                field_option_tooltip='SOR Description',
                dropdown_onchange=dropdown_onchange,     #This function changes the _sordescription and call the function "individual_total"
                mandatory=False,
            ),

            _sordescription := create_Dropdown(
                columns_to_occupy=2.1,
                field_label='Description',
                field_labelsize=field_labelsize,
                field_textsize=field_textsize,
                field_option_source=field_option_source_DESCRIPTION,
                field_option_text='SOR Description',
                field_option_tooltip='SOR Description',
                dropdown_onchange=dropdown_onchange,     #This function changes the _sorcode and call the function "individual_total"
                mandatory=False,
            ),

            _sordetail := create_Textfield(
                columns_to_occupy=3,
                field_label='Provide details',
                field_labelsize=field_labelsize,
                field_textsize=field_textsize,
                field_multiline=True,
                field_maxlines=5,
                field_minlines=2,
                mandatory=False,
            ),

            _sorprice := create_Textfield(
                columns_to_occupy=0.9,
                field_label='Price',
                field_labelsize=field_labelsize,
                field_textsize=field_textsize,
                field_prefix='£',
                field_prefixsize=field_textsize,
                field_filter='FLOAT',
                field_keyboard='NUMBER',
                textfield_onchange=individual_total,
                mandatory=False,
            ),

            _soruplift := create_Textfield(
                columns_to_occupy=0.9,
                field_label='% Uplift',
                field_labelsize=field_labelsize,
                field_textsize=field_textsize,
                field_disable=True,  
            ),

            _sortotal := create_Textfield(
                columns_to_occupy=0.9,
                field_value='£0.00',
                field_label='Total',
                field_labelsize=field_labelsize,
                field_textsize=field_textsize,
                field_disable=True,
            ),

            _delete := ft.IconButton(
                col=0.3, 
                icon=ft.icons.DELETE_FOREVER_ROUNDED, 
                icon_color=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
                icon_size=25, 
                tooltip='Delete', 
                style=ft.ButtonStyle(elevation=1, shadow_color=ft.colors.BLACK), 
                alignment=ft.alignment.center, 
                padding=ft.padding.all(0),
                data=position,
                on_click=delete
            ),

            ft.Divider(),
        ]
    )

    return pricebreakdown

    
    
    

    


if __name__ == '__main__':
    
    import json
    with open('formatting.json', 'r') as file:
        formatting = json.load(file)

    sorcode = [
        {'SOR Code': '789', 'SOR Description': 'EITA', 'Price': 150, 'Uplift': 0.1},
        {'SOR Code': '123', 'SOR Description': 'DO IT', 'Price': 50, 'Uplift': 0.5},
        {'SOR Code': '456', 'SOR Description': 'DO THAT', 'Price': 100, 'Uplift': 1}
        
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
        
        def overal_total():
            total = 0
            
            for item in all_prices_breakdown.controls:
              
                for field in item.controls[:-2]:
                    if field.label == 'Total' and field.value != '':
                        total += float(field.value.replace('£', ''))     
            
            _gran_total_value.value = f'£{total:.2f}'
            _gran_total_value.update()


        page.bgcolor=getattr(ft.colors, general_formatting.get('page_bgcolor'))
        
        general_total = None
        page.add(
            
            all_prices_breakdown := ft.ResponsiveRow(
                columns=3,
                width=600,
                controls=[

                    create_UpliftGroup(
                        page=page,
                        position=0,
                        field_option_source=sorcode,
                        field_column_uplift='Uplift',
                        field_textsize=formatting.get('field_text_size'),
                        field_labelsize=formatting.get('field_label_size'),
                        overal_total=overal_total
                    ),

                    create_UpliftGroup(
                        page=page,
                        position=0,
                        field_option_source=sorcode,
                        field_column_uplift='Uplift',
                        field_textsize=formatting.get('field_text_size'),
                        field_labelsize=formatting.get('field_label_size'),
                        overal_total=overal_total
                    ),
                ]
            ),
            _gran_total_value := create_Textfield()
        )
    
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
