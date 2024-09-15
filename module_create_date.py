from datetime import datetime
import flet as ft
import json


def create_Date(
        page,
        columns_to_occupy: float=None,
        field_value: str=None,
        field_textsize: int=None,
        field_label: str=None,
        field_labelsize: int=None,
        field_hint: str=None,
        field_hintsize: int=None,
        field_disable: bool=False,
        field_visible: bool=True,
        mandatory: bool=False,
        
):
    '''
    Parameter
        - page: ft.Page element must be provided, because it's necessary to use "page.open" to open the DatePicker
        - columns_to_occupy: float=None - Number of the columns, representing the space in Responsiverow it will occupy,
        - field_value: str=None - it might be pre-defined value, that it will initially be displayed
        - field_textsize: int=None - Number of the size of the typed text,
        - field_label: str=None - Text to be displayd inside the field, if nothing is typed, or as field title, if something is typed,
        - field_labelsize: int=None - Number of the size of the label,
        - field_hint: str=None - Wording to be displayed in case of mouse hover,
        - field_hintsize: int=None - Number of the size of the text of the hint (a wording displayed if nothing is typed),
        - field_disable: bool=False - if True, nothing can be typed,
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


    def handle_change(e):
        date_field.value = datetime.strftime(e.control.value, '%d/%m/%Y')
        date_field.data = datetime.strftime(e.control.value, '%Y/%m/%d')
        date_field.update()

    def handle_dismissal(e):
        page.close(date_picker)
    
    date_picker = ft.DatePicker(
                    on_change=handle_change,
                    on_dismiss=handle_dismissal,
                )    
    
    def check_date(e):
        date = e.control.value 
        
        if date.count('/') < 2:
            date = ''.join(date.split('/'))
            if len(date) == 8:
                date = date[:2]+'/'+date[2:4]+'/'+date[4:8]
                e.control.value = date
                e.control.update()

        date = date.split('/')

        # Check if it has a date format
        if len(date) != 3:
            e.control.value = ''
        
        # Check if the parts are integer
        try:
            day = int(date[0])
            month = int(date[1])
            year = int(date[2])
            
            # Check if day, month and year are valid
            if not ((0 < day <= 31) and (0 < month <= 12) and (year > 1900)):
                e.control.value = ''

            # Check days versus months
            elif month in [4, 6, 9, 11] and day > 30:
                e.control.value = ''
            
            # Check Leap Year
            elif (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                if month == 2 and day > 29:
                    e.control.value = ''
            
            elif month == 2 and day > 28:
                e.control.value = ''

        except:
            e.control.value = ''


        e.control.update()
    
    def updateData(e):
        e.data = datetime.strftime(e.value, '%Y/%m/%d')

    date_field = ft.TextField(
        col=columns_to_occupy-0.3,
        value=field_value,
        text_style=ft.TextStyle(color=ft.colors.BLACK, overflow=ft.TextOverflow.ELLIPSIS, size=field_textsize),
        label=field_label if mandatory==False else f'{field_label} *',
        label_style=ft.TextStyle(
            color=ft.colors.BLACK, 
            bgcolor=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
            size=field_labelsize,
        ),
        on_change=updateData,

        hint_text='dd/mm/yyyy' if field_hint==None else field_hint,
        hint_style=ft.TextStyle(color=ft.colors.GREY_800, italic=True, size=field_hintsize),
        keyboard_type=ft.KeyboardType.DATETIME,
        border_width=1,
        border_color=getattr(ft.colors, formatting.get('field_border_color')) if formatting != None else None,
        bgcolor=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
        border_radius=ft.border_radius.all(10),
        cursor_color=getattr(ft.colors, formatting.get('field_cursor_color')) if formatting != None else None,
        on_submit=check_date,
        on_blur=check_date,
        disabled=field_disable,
        error_style=ft.TextStyle(bgcolor=ft.colors.TEAL_400),
        visible=field_visible
    )

    button = ft.IconButton(
                    col=0.3, 
                    icon=ft.icons.CALENDAR_MONTH, 
                    icon_color=getattr(ft.colors, formatting.get('field_bgcolor')) if formatting != None else None,
                    icon_size=25,
                    tooltip='Select a dated',
                    style=ft.ButtonStyle(elevation=1, shadow_color=ft.colors.BLACK),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(0),
                    on_click=lambda e: page.open(date_picker)
                )
    
    return ft.ResponsiveRow(col=columns_to_occupy, columns=columns_to_occupy, controls=[date_field, button])


if __name__ == '__main__':
    def main(page: ft.Page):
        test = create_Date(page=page)

        page.add(test)
    
    ft.app(target=main)