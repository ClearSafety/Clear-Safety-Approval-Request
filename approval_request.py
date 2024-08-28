import flet as ft
from time import sleep
import os
import json
from module_airtable import *
from module_azure_cloud import *
from module_general_functions import *
from module_create_dropdown import create_Dropdown
from module_create_textfield import create_Textfield
from module_create_pricebreakdown import create_PriceBreakdownGroup
from module_create_uplift import create_UpliftGroup
from module_fields_options import *

os.getenv('FLET_SECRET_KEY')




###############################################################################################################################################################################################
# ACCESS FORMATTING BASE ON THE TYPE OF USER DEVICE: MOBILE OR COMPUTER
###############################################################################################################################################################################################

try:
    with open('formatting.json', 'r') as file:
        formatting_file = json.load(file)
    
    general_formatting = formatting_file.get('general')
    
except:
    general_formatting=None
    formatting_file=None

###############################################################################################################################################################################################




###############################################################################################################################################################################################
###############################################################################################################################################################################################
# APP FUNCTION
###############################################################################################################################################################################################
def main(page: ft.Page):
    page.window.always_on_top=True
    page.bgcolor=getattr(ft.colors, general_formatting.get('page_bgcolor'))  # Color grab from Clear Safety website
    page.adaptive=True
    page.title='Clear Safety: Approval Request'
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.vertical_alignment=ft.MainAxisAlignment.START
    page.padding=ft.padding.all(0)
    

    ###############################################################################################################################################################################################
    # DATA FROM AIRTABLE
    ###############################################################################################################################################################################################
    # ALL FIELDS OPTIONS
    field_Options = Field_Options(
        baseID='appB0phO3KnX4WexS', 
        tableID='tblycaJHzyRku5gYp',
        fields=[
            'Gas/Electrical ETC',
            'Request Type',
            'Is this on the Planned list?',
            'Request Category',
            'Tenure',
            'Service Level',
            'Does The Property Have Functioning Heating?',
            'Does The Property Have Functioning Hot Water?',
            'Has The Property Been Left With Temporary Heating?',
            'Condensing or Non-Condensing',
            'Types Of External Controls On Site',
            'Is There A Need For Additional Flueing?',
            'Is There Any Requirement To Update The Gas Supply?',
            'Is There Any Requirement To Update The Condese?'
        ]
    )
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    # SOR CODE LIST
    try:
        sor_code_list = get_Records('appB0phO3KnX4WexS', 'tblFUxOPoerfAg9vN', ['SOR Code', 'SOR Description', 'SOR Cost (BSW)', 'Uplift BSW', 'Uplift'])
        sor_code_list_price = list(filter(lambda item: item.get('Uplift') == 'No' and item.get('SOR Cost (BSW)') != 0, sor_code_list))
        sor_code_list_uplift = list(filter(lambda item: item.get('Uplift') == 'Yes' and item.get('Uplift BSW') != 0, sor_code_list))

    except:
        sor_code_list = []
        sor_code_list_price = []
        sor_code_list_uplift = []  
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    ###############################################################################################################################################################################################



    ###########################################################################################################################################################################################
    # GLOBAL VARIABLES
    ###########################################################################################################################################################################################
    # List to store all the files uploaded into the form
    success_upload = []
    error_upload = []
    upload_directory = "assets/uploads"
    upload_file_progress=ft.AlertDialog(
                title=ft.Text('Uploading files...'),
                content=ft.ProgressBar(
                width=200,
                height=30,
                value=0
                )
            )
    ###########################################################################################################################################################################################
    

    
    
    ###########################################################################################################################################################################################
    # INITIAL CHECKS
    ###########################################################################################################################################################################################
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
    
    if len(field_Options.records) == 0 and len(sor_code_list) == 0:
        page.overlay.append(dialog_error_connection)
        dialog_error_connection.open=True
        page.update()
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    # CHECK TYPE OF DEVICE USING BY THE USER AND DEFINE FORMATTING
    if formatting_file != None:
        if 'mobile' in page.client_user_agent.lower() or 'table' in page.client_user_agent.lower():
            formatting = formatting_file.get('mobile')
        else:
            formatting = formatting_file.get('computer')
    else:
        formatting = None
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    ###########################################################################################################################################################################################
    
    


    ###########################################################################################################################################################################################
    # INTERNAL FUNCIONS
    ###########################################################################################################################################################################################
    # Function to add a new group of Price Breakdown or a new group of Uplip - Miscellaneous
    def add_group(e):
        if e.control.data == 'Price Breakdown':
            next_position = len(all_prices_breakdown.controls)-1
            all_prices_breakdown.controls.insert(
                -1,
                create_PriceBreakdownGroup(
                    page=page,
                    position=next_position,
                    field_textsize=formatting.get('field_text_size') if formatting != None else None,
                    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
                    field_option_source=sor_code_list_price,
                    field_column_price='SOR Cost (BSW)',
                    delete=delete_breakdown_price,
                    overal_total=overal_total
                )
            )
                
            all_prices_breakdown.update()
        
        elif e.control.data == 'Uplift':
            next_position = len(all_uplifts_miscellaneous.controls)-1
            all_uplifts_miscellaneous.controls.insert(
                -1,
                create_UpliftGroup(
                    page=page,
                    position=0,
                    field_textsize=formatting.get('field_text_size') if formatting != None else None,
                    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
                    field_option_source=sor_code_list_uplift,
                    field_column_uplift='Uplift BSW',
                    delete=delete_uplift,
                    overal_total=overal_total
                ),
            )
                
            all_uplifts_miscellaneous.update()

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    # Function to delete a group of Price Breakdown
    def delete_breakdown_price(e):
        position = e.control.data
        all_prices_breakdown.controls.pop(position)
        
        for pos, item in enumerate(all_prices_breakdown.controls[:-1]):
            item.controls[-2].data=pos        
        
        overal_total()
        
        all_prices_breakdown.update()
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    

    # Function to delete a group of Uplift - Miscellaneous
    def delete_uplift(e):
        position = e.control.data
        all_uplifts_miscellaneous.controls.pop(position)
        
        for pos, item in enumerate(all_uplifts_miscellaneous.controls[:-1]):
            item.controls[-2].data=pos        
        
        overal_total()
        
        all_uplifts_miscellaneous.update()
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    

    # Function to update the Overal Total and add this value to the corresponding field
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
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    # Function to delete the uploaded file
    def delete_file(e):
        blob_name = e.control.data
        #Deleting from Card where the upload files are shown
        card_list_files.content.controls = list(filter(lambda item: item.data != blob_name, card_list_files.content.controls))
        card_list_files.update()

        #Delete from the list where there are all updated files data that is used to create record in Airtable
        for idx, item in enumerate(success_upload):
            if item.get('blob_name') == blob_name:
                success_upload.pop(idx)
        
        #Deleting from Azure
        try:
            deletefile_azure(blob_name=blob_name)
        except:
            ...
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    

    # FUNCTION TO CREATE A BOX DIALOG TO UPDATE FILES INTO THE FORM, UPLOAD INTO AZURE CLOUD AND RETRIEVE PUBLIC_URL
    def on_files_selected(e):
        if e.files:
            # Open progress bar
            page.open(upload_file_progress) 
            
            # Iterate over all files selected by the user
            for file in e.files:
                
                filename = file.name
                
                # Check the the selected file has suspicious extension, like '.dll', '.exe' etc
                
                if not Filetype().safefiletype(filename):
                    error_upload.append({'name': filename})
                else:
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
                    
                    # Upload file into Azure Cloud Storage and retrieve public URL. It will try 5 times.
                    count = 1
                    public_url = ''
                    while count <= 5:
                        try:
                            public_url=uploadfile_azure(
                                file_name=filename,
                                path_file=upload_directory
                            )
                            sleep(1)
                        except:
                            sleep(1)
                            count += 1

                        if public_url==None or public_url=='':
                            sleep(1)
                            count += 1
                        else:
                            success_upload.append(
                                {
                                    'blob_name': public_url.get('blob_name'),
                                    'name': file.name,
                                    'url': public_url.get('url'),
                                }
                            )
                            break
                    
                    if public_url==None or public_url=='':
                        error_upload.append({'name': filename})
                
                upload_file_progress.content.value += 1/len(e.files)  # UPDATE PROGRESS BAR
                upload_file_progress.update()  # UPDATE PROGRESS BAR
            
            # If error happens with the upload file process, a dialog window will be displayed with the file name
            if len(error_upload) > 0:
                def close_dialog(e):
                    upload_error_dialog.open=False
                    error_upload.clear()
                    page.update()
                
                list_upload_errors = '\n'.join(list(map(lambda item: f' - {item.get("name")}', error_upload)))
                body_error_alert = f'Error uploading these files. Please try again.\n {list_upload_errors} \n\nThe file types below are not allowed:\n - {", ".join(Filetype().forbbiden_extensions)}'
                upload_error_dialog = ft.AlertDialog(
                    bgcolor=getattr(ft.colors, general_formatting.get('page_bgcolor')) if general_formatting != None else None,
                    modal=True,
                    title=ft.Text(value='Clear Safety - Error', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_300),
                    content=ft.Text(value=body_error_alert, color=ft.colors.GREY_300),
                    actions=[
                        ft.ElevatedButton(
                            text='     OK     ',
                            on_click=close_dialog, 
                            bgcolor=getattr(ft.colors, general_formatting.get('page_bgcolor')) if general_formatting != None else None, 
                            color=ft.colors.GREY_300, 
                            elevation=5)
                    ],
                    actions_alignment=ft.MainAxisAlignment.CENTER,
                )
                page.overlay.append(upload_error_dialog)
                upload_error_dialog.open=True
                page.update()
            
            # If the upload is successful, it will be added to a Card to be displayed to the user
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
                                ft.TextButton(
                                    col=4.5,
                                    tooltip=item.get('name'),
                                    on_click=lambda _: page.launch_url(item.get('url')),
                                    content=ft.ResponsiveRow(
                                        columns=2,
                                        alignment=ft.MainAxisAlignment.START,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Icon(col=0.2, scale=0.7, name=ft.icons.FILE_COPY, color=getattr(ft.colors, general_formatting.get('page_bgcolor')) if general_formatting != None else None),
                                            ft.Text(col=1.8, value=item.get('name'), overflow=ft.TextOverflow.ELLIPSIS),
                                        ]
                                    )
                                ),
                                ft.IconButton(col=0.5, scale=0.7, icon=ft.icons.DELETE, icon_color=ft.colors.RED_500, on_click=delete_file, data=item.get('blob_name')),
                                ft.Divider(height=1, visible=True if len(success_upload) > 1 else False)
                            ],
                            data=item.get('blob_name')
                        )
                    )
                card_list_files.update()
            
            # Close the progress bar when the upload processo is concluded
            page.close(upload_file_progress)  # CLOSE PROGRESS BAR
            upload_file_progress.content.value=0 # RESET PROGRESS BAR
        
    file_picker = ft.FilePicker(on_result=on_files_selected)


    # SUBMIT FORM
    def submit_form(e):
        # Collect all uploaded files and store them into the list 'allevidences'
        allevidences = []
        if len(success_upload) > 0:
            allevidences = list(map(lambda item: {'url': item.get('url'), 'filename': item.get('name')}, success_upload))

        # Collect all Prices Breakdown and Uplifts created by the user and store them into the string 'breakdownAnduplifts'
        breakdownAnduplifts = ''
        if len(all_prices_breakdown.controls) > 1:
            for item in all_prices_breakdown.controls[:-1]:
                sor_code = item.controls[0].value
                if sor_code:
                    sor_description = item.controls[1].value
                    sor_price = item.controls[2].value
                    sor_qtd = item.controls[3].value
                    sor_total = item.controls[4].value
                    breakdownAnduplifts += f'SOR Code: {sor_code}, SOR Description: {sor_description}, Price: {sor_price}, Quantity: {sor_qtd}, Total: {sor_total}\n'
                
        
        if len(all_uplifts_miscellaneous.controls) > 1:
            breakdownAnduplifts += '\nUPLIFTS\n'

            for item in all_uplifts_miscellaneous.controls[:-1]:
                up_code = item.controls[0].value
                if up_code:
                    up_description = item.controls[1].value
                    up_details = item.controls[2].value
                    up_price = item.controls[3].value
                    up_percentage = item.controls[4].value
                    up_total = item.controls[5].value
                    breakdownAnduplifts += f'SOR Code: {up_code}, SOR Description: {up_description}, Details: {up_details}, Price: {up_price}, Percentage: {up_percentage}, Total: {up_total}\n'
        
        if breakdownAnduplifts == '\nUPLIFTS\n':
            breakdownAnduplifts = ''


        # CHECK MANDATORY FIELDS
        # Normal fields
        if empty_check_mandatory(
            page=page,
            fields=[
                address, 
                uprn,
                postcode,
                tenure,
                work_description
                ]
            ):
            return
        
        #Price breakdown
        if empty_check_mandatory(
            page=page,
            all_prices_breakdown=all_prices_breakdown,
            fields=['SOR Code', 'Description', 'Qty']
            ):
            return

        # Create the record
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

                    # Delete all files from Azure Cloud Service
                    try:
                        for item in success_upload:
                            deletefile_azure(item.get('blob_name'))
                    except:
                        ...
                    
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
                            create_PriceBreakdownGroup(
                                page=page,
                                position=0,
                                field_textsize=formatting.get('field_text_size') if formatting != None else None,
                                field_labelsize=formatting.get('field_label_size') if formatting != None else None,
                                field_option_source=sor_code_list_price,
                                field_column_price='SOR Cost (BSW)',
                                delete=delete_breakdown_price,
                                overal_total=overal_total
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END, 
                                col=3, 
                                controls=[
                                    ft.FloatingActionButton(
                                        tooltip='New SOR Code', 
                                        col=0.3, 
                                        icon=ft.icons.ADD, 
                                        mini=True, 
                                        shape=ft.CircleBorder('circle'), 
                                        bgcolor=getattr(ft.colors, general_formatting.get('field_bgcolor')),
                                        on_click=add_group,
                                        data='Price Breakdown'
                                    )
                                ]
                            ),
                        ]
                        all_uplifts_miscellaneous.controls=[
                            create_UpliftGroup(
                                page=page,
                                position=0,
                                field_textsize=formatting.get('field_text_size') if formatting != None else None,
                                field_labelsize=formatting.get('field_label_size') if formatting != None else None,
                                field_option_source=sor_code_list_uplift,
                                field_column_uplift='Uplift BSW',
                                delete=delete_uplift,
                                overal_total=overal_total
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END, 
                                col=3, 
                                controls=[
                                    ft.FloatingActionButton(
                                        tooltip='New Uplift', 
                                        col=0.3, 
                                        icon=ft.icons.ADD, 
                                        mini=True, 
                                        shape=ft.CircleBorder('circle'), 
                                        bgcolor=getattr(ft.colors, general_formatting.get('field_bgcolor')),
                                        on_click=add_group,
                                        data='Uplift'
                                    )
                                ]
                            ),
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
                        content=ft.Image(
                            src='images/cs_logo.png', 
                            height=formatting.get('logo_header').get('height') if formatting != None else None,
                            width=formatting.get('logo_header').get('width') if formatting != None else None, 
                            col=6
                        ),
                    ),
                    
                    ft.Container(
                        col=1, 
                        alignment=ft.alignment.center_right,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    value='Approval Request', 
                                    size=formatting.get('text_header') if formatting != None else None,
                                    color=ft.colors.GREY_700, 
                                    weight=ft.FontWeight.BOLD, 
                                    text_align=ft.TextAlign.RIGHT
                                ),
                            ],
                        )
                    ),
                ],
            )
    )
    #----------------------------------------------------------------------------
    
    # FIELDS: body of the form, where all fields are created
    form=ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
        width=600,
        controls=[
            ft.Container(
                padding=ft.padding.only(left=20, right=20, bottom=20),
                content=ft.ResponsiveRow(
                    columns=3,
                    controls=[
                        ft.Text(value='*Mandatory fields', color=ft.colors.WHITE, size=10, col=3),
                        
                        address := create_Textfield(
                            columns_to_occupy=3, 
                            field_textsize=formatting.get('field_text_size') if formatting != None else None,
                            field_label='Address',
                            field_labelsize=formatting.get('field_label_size') if formatting != None else None,
                            field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
                            mandatory=True
                        ),

                        uprn := create_Textfield(
                            columns_to_occupy=1, 
                            field_textsize=formatting.get('field_text_size') if formatting != None else None,
                            field_label='UPRN',
                            field_labelsize=formatting.get('field_label_size') if formatting != None else None,
                            field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
                            mandatory=True
                        ),

                        postcode := create_Textfield(
                            columns_to_occupy=1,
                            field_textsize=formatting.get('field_text_size') if formatting != None else None,
                            field_label='Postcode',
                            field_labelsize=formatting.get('field_label_size') if formatting != None else None,
                            field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
                            mandatory=True
                        ),
                        
                        tenure := create_Dropdown(
                            columns_to_occupy=1,
                            field_label='Tenure', 
                            field_labelsize=formatting.get('field_label_size') if formatting != None else None,
                            field_textsize=formatting.get('field_text_size') if formatting != None else None,
                            field_option_source=field_Options.get_options('Tenure'),
                            field_option_text='Tenure',
                            field_option_tooltip='Tenure',
                            mandatory=True,
                        ),

                        work_description := create_Textfield(
                            columns_to_occupy=3, 
                            field_textsize=formatting.get('field_text_size') if formatting != None else None,
                            field_label='Description of Work', 
                            field_labelsize=formatting.get('field_label_size') if formatting != None else None,
                            field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
                            field_multiline=True, 
                            field_maxlines=5,
                            mandatory=True,
                        ),
                        
                        ft.Divider(color="#2A685A"),
                        
                        ft.Text(
                            value='Price Breakdown',
                            size=formatting.get('title') if formatting != None else None,
                            color=ft.colors.GREY_300
                        ),
                        all_prices_breakdown := ft.ResponsiveRow(
                            col=3,
                            columns=3,
                            controls=[
                                create_PriceBreakdownGroup(
                                    page=page,
                                    position=0,
                                    field_textsize=formatting.get('field_text_size') if formatting != None else None,
                                    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
                                    field_option_source=sor_code_list_price,
                                    field_column_price='SOR Cost (BSW)',
                                    delete=delete_breakdown_price,
                                    overal_total=overal_total
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.END, 
                                    col=3, 
                                    controls=[
                                        ft.FloatingActionButton(
                                            tooltip='New SOR Code', 
                                            col=0.3, 
                                            icon=ft.icons.ADD, 
                                            mini=True, 
                                            shape=ft.CircleBorder('circle'), 
                                            bgcolor=getattr(ft.colors, general_formatting.get('field_bgcolor')),
                                            on_click=add_group,
                                            data='Price Breakdown'
                                        )
                                    ]
                                ),
                            ]
                        ),
                        
                        ft.Text(
                            value='Uplift - Miscellaneous',
                            size=formatting.get('title') if formatting != None else None,
                            color=ft.colors.GREY_300
                        ),
                        all_uplifts_miscellaneous := ft.ResponsiveRow(
                            col=3,
                            columns=3,
                            controls=[
                                create_UpliftGroup(
                                    page=page,
                                    position=0,
                                    field_textsize=formatting.get('field_text_size') if formatting != None else None,
                                    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
                                    field_option_source=sor_code_list_uplift,
                                    field_column_uplift='Uplift BSW',
                                    delete=delete_uplift,
                                    overal_total=overal_total
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.END, 
                                    col=3, 
                                    controls=[
                                        ft.FloatingActionButton(
                                            tooltip='New Uplift', 
                                            col=0.3, 
                                            icon=ft.icons.ADD, 
                                            mini=True, 
                                            shape=ft.CircleBorder('circle'), 
                                            bgcolor=getattr(ft.colors, general_formatting.get('field_bgcolor')),
                                            on_click=add_group,
                                            data='Uplift'
                                        )
                                    ]
                                ),
                            ]
                        ),
                                                
                        gran_total := ft.ResponsiveRow(
                            col=3,
                            columns=3,
                            alignment=ft.MainAxisAlignment.END,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    value='Overal Total: ',
                                    size=formatting.get('subtitle') if formatting != None else None,
                                    color=ft.colors.GREY_300,
                                    col=2,
                                    text_align=ft.TextAlign.END
                                ),
                                _gran_total_value := create_Textfield(
                                    columns_to_occupy=1,
                                    field_value='£0.00',
                                    field_textsize=formatting.get('field_text_size') if formatting != None else None,
                                    field_label='Overal Total',
                                    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
                                    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
                                    field_disable=True,
                                ),
                            ], 
                        ),

                        ft.Text(
                            value='Evidences, including photos', 
                            size=formatting.get('title') if formatting != None else None,
                            color=ft.colors.GREY_300
                        ),
                        ft.ElevatedButton(
                            col=1,
                            text="Upload Files",
                            on_click=lambda _: file_picker.pick_files(dialog_title='Clear Safety - Select Evidences', allow_multiple=True),
                            height=50,
                            style=ft.ButtonStyle(
                                color=ft.colors.BLACK, 
                                bgcolor=getattr(ft.colors, general_formatting.get('field_bgcolor')) if formatting != None else None,
                                elevation=10, 
                                overlay_color=ft.colors.TEAL_ACCENT_700
                            ),
                        ),
                        
                        card_list_files := ft.Card(
                            col=2,
                            color=getattr(ft.colors, general_formatting.get('card_bgcolor')) if general_formatting != None else None,
                            elevation=10,
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
                                    style=ft.ButtonStyle(
                                        color=ft.colors.BLACK, 
                                        bgcolor=getattr(ft.colors, general_formatting.get('field_bgcolor')) if formatting != None else None,
                                        elevation=10, 
                                        overlay_color=ft.colors.TEAL_ACCENT_700
                                    ),
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


ft.app(target=main, assets_dir='assets', upload_dir='assets/uploads', view=ft.AppView.WEB_BROWSER)


#SEARCH BAR https://www.youtube.com/watch?v=S0DfmuCHYGY