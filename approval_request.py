import flet as ft
from airtable import *
from google_cloud import *
from time import sleep
import os

os.getenv('FLET_SECRET_KEY')

#############################################################################
# DATA FROM AIRTABLE
#############################################################################

# TENURE LIST
try:
    tenure_list = get_Records('appB0phO3KnX4WexS', 'tblycaJHzyRku5gYp')
    tenure_list = list(map(lambda x: x.get('Tenure Types'), tenure_list))
except:
    tenure_list = []
#----------------------------------------------------------------------------

# SOR CODE LIST
try:
    sor_code_list = get_Records('appB0phO3KnX4WexS', 'tblFUxOPoerfAg9vN', ['SOR Code', 'SOR Description', 'SOR Cost (BSW)', 'Uplift BSW', 'Uplift'])
    sor_code_list_price = list(filter(lambda item: item.get('Uplift') == 'No' and item.get('SOR Cost (BSW)') != 0, sor_code_list))
    sor_code_list_uplift = list(filter(lambda item: item.get('Uplift') == 'Yes' and item.get('Uplift BSW') != 0, sor_code_list))

    sor_code_list_codes_price = sorted(list(map(lambda item: item.get('SOR Code'), sor_code_list_price)))
    sor_code_list_descriptions_price = sorted(list(map(lambda item: item.get('SOR Description'), sor_code_list_price)))

    sor_code_list_codes_uplift = sorted(list(map(lambda item: item.get('SOR Code'), sor_code_list_uplift)))
    sor_code_list_descriptions_uplift = sorted(list(map(lambda item: item.get('SOR Description'), sor_code_list_uplift)))
except:
    sor_code_list = []
    sor_code_list_price = []
    sor_code_list_uplift = []
    sor_code_list_codes_price = []
    sor_code_list_descriptions_price = []
    sor_code_list_codes_uplift = []
    sor_code_list_descriptions_uplift = []
    
#----------------------------------------------------------------------------


#############################################################################
# GENERAL FUNCIONS
#############################################################################

# CHECK IF THE NUMBER PASSED INTO A TEXTFIELD HAS THE PATTERN '000000.00'
def check_digit(e):
    if e.control.value != '':
        if e.control.value[0] in '.0':
            e.control.value = ''
        
        elif e.control.value[-1] == '.' and '.' in e.control.value[:-1]:
            e.control.value = e.control.value[:-1]
        
        elif len(e.control.value) >= 5:
            if e.control.value[-4] == '.':
                e.control.value = e.control.value[:-1]
    
    e.control.update()


def check_file(folder, filename):
    path = os.path.join(folder, filename)
    return os.path.isfile(path)




#############################################################################
# APP FUNCTION
#############################################################################
def main(page: ft.Page):
    page.window.always_on_top=True
    page.bgcolor="#2A685A"  # Color grab from Clear Safety website
    page.adaptive=True
    page.title='Clear Safety: Approval Request'
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.vertical_alignment=ft.MainAxisAlignment.START
    page.padding=ft.padding.all(0)
    
    # GLOBAL VARIABLES
    # Background color used in all the fields
    bgcolor_page="#2A685A"
    bgcolor_field='#56BAA5'

    # List to store all the files uploaded into the form
    success_upload = []
    error_upload = []
    upload_directory = "assets/uploads"
    #----------------------------------------------------------------------------
    
    # CHECK IF DATA FROM AIRTABLE HAS SUCCESSFULY BEEN RETRIEVED (EX.: SOR CODE LIST, TENURE LIST)
    def close_dialog_error_connection(e):
        dialog_error_connection.open=False
        page.update()
        page.controls.clear()
        page.add(ft.Image(src='/images/cs_logo.png', scale=0.5))
        page.update()

    dialog_error_connection = ft.AlertDialog(
        title=ft.Text(value='Clear Safety - Error'),
        content=ft.Text('Error trying to connect to the database.\nPlease check your internect connection.\nIf the problem persists, contact Clearsafety.'),
        modal=True,
        actions=[
            ft.ElevatedButton(text='Ok', on_click=close_dialog_error_connection)
        ]
        
    )
    if len(tenure_list) == 0 and len(sor_code_list) == 0:
        page.overlay.append(dialog_error_connection)
        dialog_error_connection.open=True
        page.update()



    #############################################################################
    # INTERNAL FUNCIONS
    #############################################################################
    
    # FUNCTION TO CHECK IF THE APP IS OPENED BY MOBILE OR COMPUTER
    def check_device():
        if 'mobile' in page.client_user_agent.lower() or 'table' in page.client_user_agent.lower():
            return {
                'text_header': 25,
                'logo_header': {'height': 56, 'width': 118},
                'field_text': 13,
                'field_label': 13,
                'field_hint': 11,
                'title': 15,
                'subtitle': 13,
                'column_sor_code': 1.1,
                'column_sor_description': 1.9
            }
        else:
            return {
                'text_header': 40,
                'logo_header': {'height': 62, 'width': 130},
                'field_text': 15,
                'field_hint': 13,
                'title': 17,
                'subtitle': 15,
                'column_sor_code': 0.9,
                'column_sor_description': 2.1
            }
    
    general_sizes = check_device()
    #----------------------------------------------------------------------------


    # FUNCTION TO CREATE A NORMAL TEXTFIELD
    def create_field(field_label: str, columns_to_occupy: float=None, field_disable: bool=False, field_value: str=None, on_change_function: any=None, field_filter: str=None, field_multiline: bool=False, field_prefix: int=None,):
        return ft.TextField(
                    value=field_value,
                    border_color=ft.colors.GREY_300,
                    border_width=1,
                    capitalization=ft.TextCapitalization.SENTENCES,
                    label=field_label,
                    label_style=ft.TextStyle(color=ft.colors.BLACK, bgcolor=bgcolor_field, size=general_sizes.get('field_text')),
                    cursor_color=ft.colors.GREY_300,
                    text_style=ft.TextStyle(color=ft.colors.BLACK, overflow=ft.TextOverflow.ELLIPSIS, size=general_sizes.get('field_text')),
                    border_radius=ft.border_radius.all(10),
                    col=columns_to_occupy,
                    hint_text=f'Type the {field_label}',
                    hint_style=ft.TextStyle(color=ft.colors.GREY_800, italic=True, size=general_sizes.get('field_hint')),
                    bgcolor=bgcolor_field,
                    disabled=field_disable,
                    input_filter=field_filter,
                    on_change=on_change_function,
                    multiline=field_multiline,
                    prefix_text=field_prefix,
                    prefix_style=ft.TextStyle(color=ft.colors.BLACK, bgcolor=bgcolor_field, size=general_sizes.get('field_text')),
                    height=50,
                )
    #----------------------------------------------------------------------------
    
    # FUNCTION TO CREATE A DROPDOWN TEXTFIELD
    def create_dropdown(columns_to_occupy: int, dropbox_label: str, options_list: list, on_click_function: any=None):
        return ft.Dropdown(
                    label=dropbox_label,
                    options=[ft.dropdown.Option(text=option) for option in options_list],
                    border_color=ft.colors.GREY_300,
                    border_width=1,
                    label_style=ft.TextStyle(color=ft.colors.BLACK, bgcolor=bgcolor_field, size=general_sizes.get('field_text')),
                    border_radius=ft.border_radius.all(10),
                    text_style=ft.TextStyle(color=ft.colors.BLACK, overflow=ft.TextOverflow.FADE, size=general_sizes.get('field_text')),
                    bgcolor=bgcolor_field,
                    col=columns_to_occupy,
                    on_change=on_click_function,
                    alignment=ft.alignment.top_left,
                    padding=ft.padding.only(top=0, bottom=0),
                    height=50,
                )
    #----------------------------------------------------------------------------


    #----------------------- PRICE BREAKDOWN START -----------------------------
    # FUNCTION TO CREATE A SET OF SOR CODE DETAILS FOR THE PRICE BREAKDOWN
    def create_breakdown_price(breakdown_price_position: int):
        
        # Function to fill SOR Code / Description / Price and to creat a ToolTip
        def dropbox_option_selected(e):

            if e.control.label == 'Description':
                _sorcode.value = list(filter(lambda item: item.get('SOR Description') == e.control.value, sor_code_list_price))[0].get('SOR Code')
            
            elif e.control.label == 'SOR Code':
                _sordescription.value = list(filter(lambda item: item.get('SOR Code') == e.control.value, sor_code_list_price))[0].get('SOR Description')

            _sorprice.value = f"£{list(filter(lambda item: item.get('SOR Code') == breakdown_price.controls[0].value, sor_code_list_price))[0].get('SOR Cost (BSW)'):.2f}"
            
            _sordescription.tooltip = breakdown_price.controls[1].value
            
            individual_total()

            all_prices_breakdown.update()
        #----------------------------------------------------------------------------

        
        # Function to fill individual Total
        def individual_total(e=None):
            
            if _sorprice.value != '' and _sorqtd.value != '':
                
                try:
                    _sortotal.value = f"£{float(_sorprice.value.replace('£', '')) * int(_sorqtd.value):.2f}"
                    
                except:
                    print('error')
            
            else:
                _sortotal.value = f"£0.00"
            overal_total()
            page.update()
        #----------------------------------------------------------------------------
        

        # Object with the set of all elements and details 
        breakdown_price = ft.ResponsiveRow(
            col=3,
            columns=3,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                _sorcode := create_dropdown(columns_to_occupy=general_sizes.get('column_sor_code'), dropbox_label='SOR Code', options_list=sor_code_list_codes_price, on_click_function=dropbox_option_selected),
                _sordescription := create_dropdown(columns_to_occupy=general_sizes.get('column_sor_description'), dropbox_label='Description', options_list=sor_code_list_descriptions_price, on_click_function=dropbox_option_selected),
                _sorprice := create_field(field_label='Price', columns_to_occupy=0.9, field_disable=True, on_change_function=individual_total),
                _sorqtd := create_field(field_label='Qtd', columns_to_occupy=0.9, field_disable=False, field_filter=ft.NumbersOnlyInputFilter(), on_change_function=individual_total),
                _sortotal := create_field(field_label='Total', columns_to_occupy=0.9, field_disable=True, field_value='£0.00'),
                _delete := ft.IconButton(on_click=delete_breakdown_price, data=breakdown_price_position, col=0.3, icon=ft.icons.DELETE_FOREVER_ROUNDED, icon_color=bgcolor_field, icon_size=25, tooltip='Delete', style=ft.ButtonStyle(elevation=1, shadow_color='black'), alignment=ft.alignment.center, padding=ft.padding.all(0)),
                ft.Divider(),
                
            ]
        )

        return breakdown_price
    #----------------------------------------------------------------------------


    # FUNCTION TO ADD A SET OF SOR CODE DETAILS, CREATED BY THE FUNCTION create_breakdown_price
    def add_breakdown_price(e):
        next_position = len(all_prices_breakdown.controls)-1
        all_prices_breakdown.controls.insert(-1, create_breakdown_price(breakdown_price_position=next_position))
            
        all_prices_breakdown.update()
    #----------------------------------------------------------------------------


    # FUNCTION TO DELETE A SET OF SOR CODE DETAILS, CREATED BY THE FUNCTION create_breakdown_price
    def delete_breakdown_price(e):
        position = e.control.data
        all_prices_breakdown.controls.pop(position)
        
        for pos, item in enumerate(all_prices_breakdown.controls[:-1]):
            item.controls[-2].data=pos        
        
        overal_total()
        
        all_prices_breakdown.update()
    #----------------------------------------------------------------------------
    #----------------------- PRICE BREAKDOWN END --------------------------------



    #----------------------- UPLIFT MISCELLANEOUS START -------------------------
    # FUNCTION TO CREATE A SET OF UPLIFT MISCELLANEOUS DETAILS
    def create_uplift(uplift_position: int):
        
        # Function to fill SOR Code / Description / Price and to creat a ToolTip
        def dropbox_option_selected(e):
            
            if e.control.label == 'Description':
                _sorcode_uplift.value = list(filter(lambda item: item.get('SOR Description') == e.control.value, sor_code_list_uplift))[0].get('SOR Code')
            
            elif e.control.label == 'SOR Code':
                _sordescription_uplift.value = list(filter(lambda item: item.get('SOR Code') == e.control.value, sor_code_list_uplift))[0].get('SOR Description')

            _soruplift.value = f"{list(filter(lambda item: item.get('SOR Code') == uplift.controls[0].value, sor_code_list_uplift))[0].get('Uplift BSW')*100:.2f}%"
            
            _sordescription_uplift.tooltip = uplift.controls[1].value
            
            individual_total()

            all_uplifts_miscellaneous.update()
        #----------------------------------------------------------------------------

        
        # Function to fill individual Total
        def individual_total(e=None):
            if e:
                check_digit(e)
            
            if _soruplift.value != '' and _sorprice_uplift.value != '':
                
                try:
                    _sortotal.value = f"£{(1+float(_soruplift.value.replace('%', ''))/100) * (float(_sorprice_uplift.value)):.2f}"
                    
                except:
                    _sortotal.value = '£0.00'
            
            else:
                _sortotal.value = f"£0.00"
            overal_total()
            page.update()
        #----------------------------------------------------------------------------
        

        # Object with the set of all elements and details 
        uplift = ft.ResponsiveRow(
            col=3,
            columns=3,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                _sorcode_uplift := create_dropdown(columns_to_occupy=general_sizes.get('column_sor_code'), dropbox_label='SOR Code', options_list=sor_code_list_codes_uplift, on_click_function=dropbox_option_selected),
                _sordescription_uplift := create_dropdown(columns_to_occupy=general_sizes.get('column_sor_description'), dropbox_label='Description', options_list=sor_code_list_descriptions_uplift, on_click_function=dropbox_option_selected),
                _sordetail_uplift := create_field(field_label='Provide details', columns_to_occupy=3, field_disable=False, field_multiline=True),
                _sorprice_uplift := create_field(field_prefix='£', field_label='Price', columns_to_occupy=0.9, field_disable=False, field_filter=ft.InputFilter(regex_string=r"^[0-9.]+$"), on_change_function=individual_total),
                _soruplift := create_field(field_label='% Uplift', columns_to_occupy=0.9, field_disable=True, on_change_function=individual_total),
                _sortotal := create_field(field_label='Total', columns_to_occupy=0.9, field_disable=True, field_value='£0.00'),
                _delete := ft.IconButton(on_click=delete_uplift, data=uplift_position, col=0.3, icon=ft.icons.DELETE_FOREVER_ROUNDED, icon_color=bgcolor_field, icon_size=25, tooltip='Delete', style=ft.ButtonStyle(elevation=1, shadow_color='black'), alignment=ft.alignment.center, padding=ft.padding.all(0)),
                ft.Divider(),
                
            ]
        )

        return uplift
    #----------------------------------------------------------------------------


    # FUNCTION TO ADD A SET OF UPLIFT MISCELLANEOUS DETAILS, CREATED BY THE FUNCTION create_uplift
    def add_uplift(e):
        next_position = len(all_uplifts_miscellaneous.controls)-1
        all_uplifts_miscellaneous.controls.insert(-1, create_uplift(uplift_position=next_position))
            
        all_uplifts_miscellaneous.update()
    #----------------------------------------------------------------------------


    # FUNCTION TO DELETE A SET OF UPLIFT MISCELLANEOUS DETAILS, CREATED BY THE FUNCTION create_uplift
    def delete_uplift(e):
        position = e.control.data
        all_uplifts_miscellaneous.controls.pop(position)
        
        for pos, item in enumerate(all_uplifts_miscellaneous.controls[:-1]):
            item.controls[-2].data=pos        
        
        overal_total()
        
        all_uplifts_miscellaneous.update()
    #----------------------------------------------------------------------------
    #----------------------- UPLIFT MISCELLANEOUS END -------------------------


    # FUNCTION TO CREATE AN OVERAL TOTAL AND ADD THIS VALUE TO THE CORRESPONDING FIELD
    def overal_total():
        total = 0
        for item in all_prices_breakdown.controls[:-1]:
            for field in item.controls[:-2]:
                if field.label == 'Total' and field.value != '':
                    total += float(field.value.replace('£', ''))

        for item in all_uplifts_miscellaneous.controls[:-1]:
            for field in item.controls[:-2]:
                if field.label == 'Total' and field.value != '':
                    total += float(field.value.replace('£', ''))        
        
        _gran_total_value.value = f'£{total:.2f}'
        _gran_total_value.update()
    #----------------------------------------------------------------------------


    # FUNCTION TO CREATE A BOX DIALOG TO UPDATE FILES INTO THE FORM
    def on_files_selected(e):
        if e.files:
            next_index = len(success_upload)
            for file in e.files:
                signed_url=''
                file_to_upload=''                
                
                filename = file.name
                upload_url = page.get_upload_url(filename, 60)
                
                # Upload files into 'assets/uploads'
                file_picker.upload(
                    files=[
                        ft.FilePickerUploadFile(
                            name=filename, 
                            upload_url=upload_url, 
                            method="PUT"
                        )
                    ]
                )
                
                # Creating a signed URL
                signed_url = generate_upload_signed_url_v4(file_name=filename)
                
                # Upload file into Google Cloud Storage
                path = f'{upload_directory}/{file.name}'
                count=1
                response_upload_to_google=''
                while count < 10:
                    if signed_url=='' or signed_url==False or check_file(upload_directory, filename)==False:
                        sleep(count)
                        count+=1
                    else:
                        
                        with open(path, 'rb') as file_to_upload:
                            # Use Requests to do the upload
                            response_upload_to_google = requests.put(signed_url, data=file_to_upload)
                            
                            if response_upload_to_google.status_code == 200:
                                public_url = make_file_public_and_get_url(file_name=filename)
                                print(public_url)
                                
                                if public_url != False:
                                    success_upload.append(
                                        {
                                            'index': next_index,
                                            'name': file.name,
                                            'url': public_url,
                                        }
                                    )
                                    next_index += 1
                                    break
                                
                                else:
                                    error_upload.append({'name': filename})
                                    break

                            else:
                                error_upload.append({'name': filename})
                                break
                
                if response_upload_to_google == '':
                    error_upload.append({'name': filename})
                

            
            if len(error_upload) > 0:
                def close_dialog(e):
                    upload_error_dialog.open=False
                    error_upload.clear()
                    page.update()
                    
                
                body_error_alert = 'Error uploading these files. Please try again.\n' + '\n'.join(list(map(lambda item: f' - {item.get("name")}', error_upload)))
                upload_error_dialog = ft.AlertDialog(
                    bgcolor=bgcolor_page,
                    modal=True,
                    title=ft.Text(value='Clear Safety - Error', size=20, weight=ft.FontWeight.BOLD),
                    content=ft.Text(value=body_error_alert),
                    actions=[
                        ft.ElevatedButton(text='     OK     ', on_click=close_dialog, bgcolor=bgcolor_field, color=ft.colors.GREY_300, elevation=5)
                    ],
                    actions_alignment=ft.MainAxisAlignment.CENTER,
                )
                page.overlay.append(upload_error_dialog)
                upload_error_dialog.open=True
                page.update()
                
 

            
            if len(success_upload) > 0:
                card_list_files.content.controls.clear()
                for item in success_upload:
                    card_list_files.content.controls.append(ft.ResponsiveRow(
                            columns=5,
                            spacing=0,
                            run_spacing=0,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(col=1, name=ft.icons.FILE_COPY),
                                ft.Text(col=3, value=item.get('name')),
                                ft.IconButton(col=1, icon=ft.icons.DELETE),
                                ft.Divider(height=1, visible=True if len(success_upload) > 1 else False)
                            ],
                        )
                    )
                card_list_files.update()
        
    file_picker = ft.FilePicker(on_result=on_files_selected)


    # SUBMIT FORM
    def submit_form(e):
        allevidences =[]
        if len(success_upload) > 0:
            allevidences = list(map(lambda item: {'url': item.get('url'), 'filename': item.get('name')}, success_upload))

        breakdownAnduplifts = ''
        if len(all_prices_breakdown.controls) > 0:
            for item in all_prices_breakdown.controls[:-1]:
                sor_code = item.controls[0].value
                sor_description = item.controls[1].value
                sor_price = item.controls[2].value
                sor_qtd = item.controls[3].value
                sor_total = item.controls[4].value
                breakdownAnduplifts += f'SOR Code: {sor_code}, SOR Description: {sor_description}, Price: {sor_price}, Quantity: {sor_qtd}, Total: {sor_total}\n'
        
        if len(all_uplifts_miscellaneous.controls) > 0:
            breakdownAnduplifts += '\n UPLIFTS\n'
            

            for item in all_uplifts_miscellaneous.controls[:-1]:
                up_code = item.controls[0].value
                up_description = item.controls[1].value
                up_details = item.controls[2].value
                up_price = item.controls[3].value
                up_percentage = item.controls[4].value
                up_total = item.controls[5].value
                breakdownAnduplifts += f'SOR Code: {up_code}, SOR Description: {up_description}, Details: {up_details}, Price: {up_price}, Percentage: {up_percentage}, Total: {up_total}\n'
        
        new_record = create_Record(
            baseID='appnACNlBdniubvWe',
            tableID='tblE5yfkwLy3HyOHC',
            content={
                'Address': address.value,
                'UPRN': uprn.value,
                'Postcode': postcode.value,
                'Tenure': tenure.value,
                'Description of work': work_description.value,
                'Price breakdown': breakdownAnduplifts,
                'Total': float(_gran_total_value.value.replace('£', '')) if _gran_total_value.value != '' else None,
                'Evidences': allevidences
            }
        )

        if new_record == 'Successful':
            def close_dialog_submission_success(e):
                    dialog_submission_success.open=False
                    page.update()
                    
                    if e.control.text=='Close':
                        page.controls.clear()
                        page.add(ft.Image(src='/images/cs_logo.png', scale=0.5))
                    else:
                        address.value=''
                        uprn.value=''
                        postcode.value=''
                        tenure.value=None
                        work_description.value=''
                        all_prices_breakdown.controls=[
                                create_breakdown_price(breakdown_price_position=0),
                                ft.Row(alignment=ft.MainAxisAlignment.END, col=3, controls=[ft.FloatingActionButton(tooltip='New SOR Code', col=0.3, icon=ft.icons.ADD, mini=True, shape=ft.CircleBorder('circle'), bgcolor=bgcolor_field, on_click=add_breakdown_price)]),
                            ]
                        all_uplifts_miscellaneous.controls=[
                                create_uplift(uplift_position=0),
                                ft.Row(alignment=ft.MainAxisAlignment.END, col=3, controls=[ft.FloatingActionButton(tooltip='New SOR Code', col=0.3, icon=ft.icons.ADD, mini=True, shape=ft.CircleBorder('circle'), bgcolor=bgcolor_field, on_click=add_uplift)]),
                            ]
                        _gran_total_value.value=''
                        card_list_files.content.controls.clear()
                    page.update()

            dialog_submission_success = ft.AlertDialog(
                title=ft.Text(value='Clear Safety - Approval Request'),
                content=ft.Text('Form submitted successfully.'),
                modal=True,
                actions=[
                    ft.ElevatedButton(text='Submit another request', on_click=close_dialog_submission_success),
                    ft.ElevatedButton(text='Close', on_click=close_dialog_submission_success)
                ]
            )
            
            page.overlay.append(dialog_submission_success)
            dialog_submission_success.open=True
            page.update()


        else:
            def close_dialog_submission_error(e):
                dialog_submission_error.open=False
                page.update()
            
            dialog_submission_error = ft.AlertDialog(
                title=ft.Text(value='Clear Safety - Approval Request'),
                content=ft.Text('Error trying to submit the form. Please try again.\nIf the error persists, contact Clear Safety.'),
                modal=True,
                actions=[
                    ft.ElevatedButton(text='Ok', on_click=close_dialog_submission_error),
                ]
            )
            page.overlay.append(dialog_submission_error)
            dialog_submission_error.open=True
            page.update()

    


    #############################################################################
    # FORM
    #############################################################################

    # HEADER
    header=ft.Container(
        padding=ft.padding.symmetric(vertical=20, horizontal=40),
        bgcolor=ft.colors.GREY_100,
        content=ft.ResponsiveRow(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                columns=2,
                controls=[
                    ft.Container(
                        col=1, 
                        alignment=ft.alignment.center_left,
                        content=ft.Image(src='images/cs_logo.png', height=general_sizes.get('logo_header').get('height'), width=general_sizes.get('logo_header').get('width'), col=6),
                    ),
                    
                    ft.Container(
                        col=1, 
                        alignment=ft.alignment.center_right,
                        content=ft.Column(
                            controls=[
                                ft.Text(value='Approval Request', size=general_sizes.get('text_header'), color=ft.colors.GREY_700, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT),
                            ],
                        )
                    ),
                ],
            )
    )
    #----------------------------------------------------------------------------
    
    # FIELDS
    form=ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
        width=600,
        controls=[
            ft.Container(
                padding=ft.padding.all(20),
                content=ft.ResponsiveRow(
                    columns=3,
                    controls=[
                        address := create_field('Address', 3),
                        uprn := create_field('UPRN', 1),
                        postcode := create_field('Postcode', 1),
                        tenure := create_dropdown(1, 'Tenure', tenure_list),
                        work_description := create_field('Description of Work', 3, field_multiline=True),
                        ft.Divider(color="#2A685A"),
                        
                        ft.Text(value='Price Breakdown', size=general_sizes.get('title'), color=ft.colors.GREY_300),
                        all_prices_breakdown := ft.ResponsiveRow(
                            col=3,
                            columns=3,
                            controls=[
                                create_breakdown_price(breakdown_price_position=0),
                                ft.Row(alignment=ft.MainAxisAlignment.END, col=3, controls=[ft.FloatingActionButton(tooltip='New SOR Code', col=0.3, icon=ft.icons.ADD, mini=True, shape=ft.CircleBorder('circle'), bgcolor=bgcolor_field, on_click=add_breakdown_price)]),
                            ]
                        ),
                        
                        ft.Text(value='Uplift - Miscellaneous', size=general_sizes.get('title'), color=ft.colors.GREY_300),
                        all_uplifts_miscellaneous := ft.ResponsiveRow(
                            col=3,
                            columns=3,
                            controls=[
                                create_uplift(uplift_position=0),
                                ft.Row(alignment=ft.MainAxisAlignment.END, col=3, controls=[ft.FloatingActionButton(tooltip='New SOR Code', col=0.3, icon=ft.icons.ADD, mini=True, shape=ft.CircleBorder('circle'), bgcolor=bgcolor_field, on_click=add_uplift)]),
                            ]
                        ),
                                                
                        gran_total := ft.ResponsiveRow(
                            col=3,
                            columns=3,
                            alignment=ft.MainAxisAlignment.END,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(value='Overal Total: ', size=general_sizes.get('subtitle'), color=ft.colors.GREY_300, col=2, text_align=ft.TextAlign.END), 
                                _gran_total_value := create_field(field_value='£0.00', field_label='Overal Total', field_disable=True, columns_to_occupy=1)
                            ], 
                        ),

                        ft.Text(value='Evidences, including photos', size=general_sizes.get('title'), color=ft.colors.GREY_300),
                        ft.ElevatedButton(
                            col=1,
                            text="Upload Files",
                            on_click=lambda _: file_picker.pick_files(dialog_title='Clear Safety - Select Evidences', allow_multiple=True),
                            height=50,
                            style=ft.ButtonStyle(color=ft.colors.BLACK, bgcolor=bgcolor_field, elevation=10, overlay_color=ft.colors.TEAL_ACCENT_700),
                        ),
                        
                        card_list_files := ft.Card(
                            col=2,
                            content=ft.Column(
                                spacing=0,
                                height=120,
                                scroll=ft.ScrollMode.ALWAYS,
                            ),
                        ),
                        
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.ElevatedButton(
                                    col=1,
                                    text="Submit",
                                    on_click=submit_form,
                                    height=50,
                                    style=ft.ButtonStyle(color=ft.colors.BLACK, bgcolor=bgcolor_field, elevation=10, overlay_color=ft.colors.TEAL_ACCENT_700),
                                ),
                            ]
                        ),
                    ]
                )
            )
        ],
    )
    #----------------------------------------------------------------------------

    
    
    page.add(header, form, file_picker)


ft.app(target=main, assets_dir='assets', upload_dir='assets/uploads')


#SEARCH BAR https://www.youtube.com/watch?v=S0DfmuCHYGY