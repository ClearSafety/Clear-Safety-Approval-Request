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
from module_create_date import create_Date
from module_create_checkbox import create_Checkbox
from module_create_listcheckbox import create_ListCheckbox
from module_create_filepicker import create_Filepicker
from module_fields_options import *

os.getenv('FLET_SECRET_KEY')


contractor = 'BSW'

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
    # ALL FIELDS OPTIONS TO BE USED IN DROPDOWN FIELD
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


    # SOR CODE LIST TO BE USED IN PRICEBREAKDOWN AND UPLIFT DROPDOWN FIELD
    try:
        sor_code_list = get_Records('appB0phO3KnX4WexS', 'tblFUxOPoerfAg9vN', ['SOR Code', 'SOR Description', f'SOR Cost ({contractor})', f'Uplift {contractor}', 'Uplift'])
        sor_code_list_price = list(filter(lambda item: item.get('Uplift') == 'No' and item.get(f'SOR Cost ({contractor})') != 0, sor_code_list))
        sor_code_list_uplift = list(filter(lambda item: item.get('Uplift') == 'Yes' and item.get(f'Uplift {contractor}') != 0, sor_code_list))

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
    upload_directory = "assets/uploads"
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
        if 'mobile' in page.client_user_agent.lower() or 'table' in page.client_user_agent.lower() or 'android' in page.client_user_agent.lower():
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


    
    
    # SUBMIT FORM
    def submit_form(e):
        # Collect all uploaded files and store them into the list 'allevidences'
        allevidences = []
        if len(evidences.data) > 0:
            allevidences = list(map(lambda item: {'url': item.get('url'), 'filename': item.get('name')}, evidences.data))

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
                contractor_name,
                address, uprn, postcode, work_description, property_type, property_level, meter_location, appliance_type, appliance_make, appliance_model, reason_no_serial_number, reason_no_gc_number, serial_number, gc_number, age_appliance, appliance_failures, engineers_comments, fault_history, current_location, number_radiators, water_flow_rate, reason_no_evidence, make_new_appliance, model_new_appliance, location_new_appliance, time_to_complete, email,
                planned_list, request_type, request_category, gas_elec_etc, tenure, service_level, functioning_heating, functioning_hot_water, temporary_heating, condensing_noncondensing, additional_flueing, update_gas_supply, update_condese,
                date_reported.controls[0], date_to_complete.controls[0],
                ]
            ):
            return

        # ListCheckbox fields
        if empty_check_mandatory(
            page=page,
            listcheckbox=True,
            fields=[
                types_of_control
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
            baseID='appkaWXXjd1UyTbUk',
            tableID='tblqO3PiLIuy6yRwZ',
            content={
                'Contractor': contractor_name.value if contractor_name.value != '' else None,
                'Address': address.value,
                'UPRN': uprn.value,
                'Post Code': postcode.value,
                'Description Of Works Required': work_description.value,
                'Property Type': property_type.value,
                'Property Level': property_level.value,
                'Meter Location': meter_location.value,
                'Type Of Appliance': appliance_type.value,
                'Current Appliance Make': appliance_make.value,
                'Current Appliance Model': appliance_model.value,
                'Reason For No Serial Number': reason_no_serial_number.value,
                'Reason For No GC Number': reason_no_gc_number.value,
                'Serial Number': serial_number.value,
                'GC Number': gc_number.value,
                'Estimated Age Of Appliance': age_appliance.value,
                'Description Of Appliance Failures': appliance_failures.value,
                'Engineers Comments/Recommendations': engineers_comments.value,
                'Appliance Fault History & Previous Attendance': fault_history.value,
                'Current Location': current_location.value,
                'No. Of Radiators': number_radiators.value,
                'Flow Rate': water_flow_rate.value,
                'Reason For Lack Of Attached Evidence': reason_no_evidence.value,
                'Make Of New Appliance': make_new_appliance.value,
                'Model Of New Appliance': model_new_appliance.value,
                'New Appliance Location': location_new_appliance.value,
                'Estimated Time To Complete Works': time_to_complete.value,
                'Email To Communicate With': email.value,
                
                'Is this on the Planned list?': planned_list.value if planned_list.value != '' else None,
                'Request Type': request_type.value if request_type.value != '' else None,
                'Request Category': request_category.value if request_category.value != '' else None,
                'Gas/Electrical ETC': gas_elec_etc.value if gas_elec_etc.value != '' else None,
                'Tenure': tenure.value if tenure.value != '' else None,
                'Service Level': service_level.value if service_level.value != '' else None,
                'Does The Property Have Functioning Heating?': functioning_heating.value if functioning_heating.value != '' else None,
                'Does The Property Have Functioning Hot Water?': functioning_hot_water.value if functioning_hot_water.value != '' else None,
                'Has The Property Been Left With Temporary Heating?': temporary_heating.value if temporary_heating.value != '' else None,
                'Condensing or Non-Condensing': condensing_noncondensing.value if condensing_noncondensing.value != '' else None,
                'Is There A Need For Additional Flueing?': additional_flueing.value if additional_flueing.value != '' else None,
                'Is There Any Requirement To Update The Gas Supply?': update_gas_supply.value if update_gas_supply.value != '' else None,
                'Is There Any Requirement To Update The Condese?': update_condese.value if update_condese.value != '' else None,

                'Private Landlord?': private_landlord.content.value,
                'Void Property?': void_property.content.value,

                'Date Reported': date_reported.controls[0].data,
                'Date of Works to be carried out': date_to_complete.controls[0].data,
                
                'Types Of External Controls On Site': types_of_control.data,
                
                'Work Quotation Cost Breakdown With SOR Codes': breakdownAnduplifts,
                'Total Cost': float(_gran_total_value.value.replace('£', '')) if _gran_total_value.value != '' else None,
                'Pre-works Evidence (Inc Photos)': allevidences
            }
        )

        if new_record == 'Successful':
            def close_dialog_submission_success(e):
                    dialog_submission_success.open=False
                    page.update()

                    # Delete all files from Azure Cloud Service
                    try:
                        for item in evidences.data:
                            deletefile_azure(item.get('blob_name'))
                    except:
                        ...
                    
                    if e.control.text=='Close':
                        page.controls.clear()
                        page.add(ft.Image(src='/images/cs_logo.png', scale=0.5))
                    else:
                        contractor_name.value=None
                        address.value=None
                        uprn.value=None
                        postcode.value=None
                        work_description.value=None
                        property_type.value=None
                        property_level.value=None
                        meter_location.value=None
                        appliance_type.value=None
                        appliance_make.value=None
                        appliance_model.value=None
                        reason_no_serial_number.value=None
                        reason_no_gc_number.value=None
                        serial_number.value=None
                        gc_number.value=None
                        age_appliance.value=None
                        appliance_failures.value=None
                        engineers_comments.value=None
                        fault_history.value=None
                        current_location.value=None
                        number_radiators.value=None
                        water_flow_rate.value=None
                        reason_no_evidence.value=None
                        make_new_appliance.value=None
                        model_new_appliance.value=None
                        location_new_appliance.value=None
                        time_to_complete.value=None
                        email.value=None
                        planned_list.value=None
                        request_type.value=None
                        request_category.value=None
                        gas_elec_etc.value=None
                        tenure.value=None
                        service_level.value=None
                        functioning_heating.value=None
                        functioning_hot_water.value=None
                        temporary_heating.value=None
                        condensing_noncondensing.value=None
                        additional_flueing.value=None
                        update_gas_supply.value=None
                        update_condese.value=None
                        private_landlord.content.value=False
                        void_property.content.value=False
                        date_reported.controls[0].data=None
                        date_to_complete.controls[0].data=None
                        date_reported.controls[0].value=None
                        date_to_complete.controls[0].value=None
                        for item in types_of_control.controls[0].content.controls:
                            item.value=False
                        
                        
                        
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
                        
                        #card_list_files.content.controls.clear()
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
    
    
    # FIELDS
    contractor_name = create_Textfield(
        columns_to_occupy=0.7, 
        field_value=contractor,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_label='Contractor',
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
        field_disable=True
    )

    planned_list = create_Dropdown(
        columns_to_occupy=3,
        field_label='Is this on the Planned list?', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Is this on the Planned list?'),
        field_option_text='Is this on the Planned list?',
        field_option_tooltip='Is this on the Planned list?',
        mandatory=True,
        field_visible=False,
    )

    request_type = create_Dropdown(
        columns_to_occupy=1.5,
        field_label='Request Type', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Request Type'),
        field_option_text='Request Type',
        field_option_tooltip='Request Type',
        mandatory=True,
        condition={'equal_to': 'Reactive - Appliance Renewal', 'afected_field': [planned_list]}
    )

    request_category = create_Dropdown(
        columns_to_occupy=1.5,
        field_label='Request Category', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Request Category'),
        field_option_text='Request Category',
        field_option_tooltip='Request Category',
        mandatory=True
    )

    date_reported = create_Date(
        page=page,
        columns_to_occupy=1.2,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_label='Date Reported',
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
        mandatory=True
    )

    gas_elec_etc = create_Dropdown(
        columns_to_occupy=1.1,
        field_label='Gas/Electrical ETC', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Gas/Electrical ETC'),
        field_option_text='Gas/Electrical ETC',
        field_option_tooltip='Gas/Electrical ETC',
        mandatory=True,
    )
    
    address = create_Textfield(
        columns_to_occupy=3, 
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_label='Address',
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
        mandatory=True
    )

    uprn = create_Textfield(
        columns_to_occupy=1, 
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_label='UPRN',
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
        mandatory=True
    )

    postcode = create_Textfield(
        columns_to_occupy=1,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_label='Postcode',
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
        mandatory=True
    )

    work_description = create_Textfield(
        columns_to_occupy=3, 
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_label='Description Of Works Required', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
        field_multiline=True, 
        field_maxlines=5,
        mandatory=True,
    )
    
    tenure = create_Dropdown(
        columns_to_occupy=1,
        field_label='Tenure', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Tenure'),
        field_option_text='Tenure',
        field_option_tooltip='Tenure',
        mandatory=True,
    )
    
    property_type = create_Textfield(
        columns_to_occupy=1.5,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_label='Property Type',
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
        mandatory=True
    )

    property_level = create_Textfield(
        columns_to_occupy=1.5,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_label='Property Level',
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
        mandatory=True
    )

    private_landlord = create_Checkbox(
        columns_to_occupy=1,
        field_label='Private Landlord?',
        mandatory=False,
    )

    void_property = create_Checkbox(
        columns_to_occupy=1,
        field_label='Void Property?',
        mandatory=False,
    )

    service_level = create_Dropdown(
        columns_to_occupy=1,
        field_label='Service Level', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Service Level'),
        field_option_text='Service Level',
        field_option_tooltip='Service Level',
        mandatory=True,
    )

    functioning_heating = create_Dropdown(
        columns_to_occupy=3,
        field_label='Does The Property Have Functioning Heating?', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Does The Property Have Functioning Heating?'),
        field_option_text='Does The Property Have Functioning Heating?',
        field_option_tooltip='Does The Property Have Functioning Heating?',
        mandatory=True,
    )

    functioning_hot_water = create_Dropdown(
        columns_to_occupy=3,
        field_label='Does The Property Have Functioning Hot Water?', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Does The Property Have Functioning Hot Water?'),
        field_option_text='Does The Property Have Functioning Hot Water?',
        field_option_tooltip='Does The Property Have Functioning Hot Water?',
        mandatory=True,
    ) 

    temporary_heating = create_Dropdown(
        columns_to_occupy=3,
        field_label='Has The Property Been Left With Temporary Heating?', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Has The Property Been Left With Temporary Heating?'),
        field_option_text='Has The Property Been Left With Temporary Heating?',
        field_option_tooltip='Has The Property Been Left With Temporary Heating?',
        mandatory=True,
    ) 

    meter_location = create_Textfield(
        columns_to_occupy=1.5,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_label='Meter Location',
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
        mandatory=True
    )

    appliance_type = create_Textfield(
    columns_to_occupy=1.5,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='Type of Appliance',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=True
    )

    appliance_make = create_Textfield(
    columns_to_occupy=1.5,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='Current Appliance Make',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=True
    )

    appliance_model = create_Textfield(
    columns_to_occupy=1.5,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='Current Appliance Model',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=True
    )

    condensing_noncondensing = create_Dropdown(
        columns_to_occupy=3,
        field_label='Condensing or Non-Condensing', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Condensing or Non-Condensing'),
        field_option_text='Condensing or Non-Condensing',
        field_option_tooltip='Condensing or Non-Condensing',
        mandatory=True,
    ) 

    reason_no_serial_number = create_Textfield(
    columns_to_occupy=3,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='Reason For No Serial Number',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=True,
    field_multiline=True,
    field_maxlines=3,
    )

    reason_no_gc_number = create_Textfield(
    columns_to_occupy=3,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='Reason For No GC Number',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=True,
    field_multiline=True,
    field_maxlines=3,
    )
    
    serial_number = create_Textfield(
    columns_to_occupy=1,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='Serial Number',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=False,
    condition={'equal_to': '', 'afected_field': [reason_no_serial_number]}
    )

    gc_number = create_Textfield(
    columns_to_occupy=1,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='GC Number',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=False,
    condition={'equal_to': '', 'afected_field': [reason_no_gc_number]}
    )

    age_appliance = create_Textfield(
    columns_to_occupy=1,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='Estimated Age of Appliance',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=True,
    )

    appliance_failures = create_Textfield(
    columns_to_occupy=3,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='Description of Appliance Failures',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=True,
    field_multiline=True,
    field_maxlines=3,
    )

    engineers_comments = create_Textfield(
    columns_to_occupy=3,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='Engineers Comments/Recommendations',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=True,
    field_multiline=True,
    field_maxlines=3,
    )

    fault_history = create_Textfield(
    columns_to_occupy=3,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='Appliance Fault History & Previous Attendance',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=True,
    field_multiline=True,
    field_maxlines=3,
    )

    current_location = create_Textfield(
    columns_to_occupy=3,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='Current Location',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=True,
    )

    number_radiators = create_Textfield(
    columns_to_occupy=1.5,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='No. Of Radiators',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=True,
    )

    water_flow_rate = create_Textfield(
    columns_to_occupy=1.5,
    field_textsize=formatting.get('field_text_size') if formatting != None else None,
    field_label='Mains Water Flow Rate',
    field_labelsize=formatting.get('field_label_size') if formatting != None else None,
    field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
    mandatory=False,
    )

    types_of_control = create_ListCheckbox(
        columns_to_occupy=3,
        field_label='Types Of External Controls On Site',
        field_option_source=field_Options.get_options('Types Of External Controls On Site'),
        field_option_text='Types Of External Controls On Site',
        field_option_tooltip='Types Of External Controls On Site',
        mandatory=True,
    )

    reason_no_evidence = create_Textfield(
        columns_to_occupy=3,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_label='Reason For Lack Of Attached Evidence',
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
        mandatory=True,
        field_multiline=True,
        field_maxlines=3,
        )
    
    evidences = create_Filepicker(
        page=page,
        columns_to_occupy=3,
        upload_directory=upload_directory,
        condition={'equal_to': '', 'afected_field': [reason_no_evidence]}
    )

    additional_flueing = create_Dropdown(
        columns_to_occupy=3,
        field_label='Is There A Need For Additional Flueing?', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Is There A Need For Additional Flueing?'),
        field_option_text='Is There A Need For Additional Flueing?',
        field_option_tooltip='Is There A Need For Additional Flueing?',
        mandatory=True,
    )

    update_gas_supply = create_Dropdown(
        columns_to_occupy=3,
        field_label='Is There Any Requirement To Update The Gas Supply?', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Is There Any Requirement To Update The Gas Supply?'),
        field_option_text='Is There Any Requirement To Update The Gas Supply?',
        field_option_tooltip='Is There Any Requirement To Update The Gas Supply?',
        mandatory=True,
    )

    update_condese = create_Dropdown(
        columns_to_occupy=3,
        field_label='Is There Any Requirement To Update The Condese?', 
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_option_source=field_Options.get_options('Is There Any Requirement To Update The Condese?'),
        field_option_text='Is There Any Requirement To Update The Condese?',
        field_option_tooltip='Is There Any Requirement To Update The Condese?',
        mandatory=True,
    )

    make_new_appliance = create_Textfield(
            columns_to_occupy=1,
            field_textsize=formatting.get('field_text_size') if formatting != None else None,
            field_label='Make Of New Appliance',
            field_labelsize=formatting.get('field_label_size') if formatting != None else None,
            field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
            mandatory=True,
            field_multiline=True,
            field_maxlines=3,
            )

    model_new_appliance = create_Textfield(
            columns_to_occupy=1,
            field_textsize=formatting.get('field_text_size') if formatting != None else None,
            field_label='Model Of New Appliance',
            field_labelsize=formatting.get('field_label_size') if formatting != None else None,
            field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
            mandatory=True,
            field_multiline=True,
            field_maxlines=3,
            )
    
    location_new_appliance = create_Textfield(
            columns_to_occupy=1,
            field_textsize=formatting.get('field_text_size') if formatting != None else None,
            field_label='New Appliance Location',
            field_labelsize=formatting.get('field_label_size') if formatting != None else None,
            field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
            mandatory=True,
            field_multiline=True,
            field_maxlines=3,
            )

    time_to_complete = create_Textfield(
            columns_to_occupy=3,
            field_textsize=formatting.get('field_text_size') if formatting != None else None,
            field_label='Estimated Time To Complete Works',
            field_labelsize=formatting.get('field_label_size') if formatting != None else None,
            field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
            mandatory=True,
            )

    date_to_complete = create_Date(
        page=page,
        columns_to_occupy=3,
        field_textsize=formatting.get('field_text_size') if formatting != None else None,
        field_label='Date of works scheduled to be carried out',
        field_labelsize=formatting.get('field_label_size') if formatting != None else None,
        field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
        mandatory=True
    )

    email = create_Textfield(
            columns_to_occupy=3,
            field_textsize=formatting.get('field_text_size') if formatting != None else None,
            field_label='Email Address to Communicate With',
            field_labelsize=formatting.get('field_label_size') if formatting != None else None,
            field_hintsize=formatting.get('field_hint_size') if formatting != None else None,
            mandatory=True,
            ) 

    all_prices_breakdown = ft.ResponsiveRow(
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
    )

    all_uplifts_miscellaneous = ft.ResponsiveRow(
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
    )
    
    gran_total = ft.ResponsiveRow(
        col=3,
        columns=3,
        alignment=ft.MainAxisAlignment.END,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                value='Total Cost (excl. VAT): ',
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
    )



    # BODY OF THE FORM WITH ALL FIELDS
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
                        
                        contractor_name, gas_elec_etc, date_reported,
                        
                        request_type, request_category,
                        
                        planned_list,
                        
                        address,

                        uprn, postcode, tenure,

                        property_type, property_level,

                        private_landlord, void_property, service_level,
                        
                        functioning_heating,
                        
                        functioning_hot_water,
                        
                        temporary_heating,
                        
                        meter_location, appliance_type,
                        
                        appliance_make, appliance_model,
                        
                        condensing_noncondensing,
                        
                        serial_number, gc_number, age_appliance,

                        reason_no_serial_number,
                        
                        reason_no_gc_number,

                        appliance_failures,
                        
                        engineers_comments,
                        
                        fault_history,

                        current_location, number_radiators, water_flow_rate,

                        types_of_control,

                        # Upload files
                        ft.Divider(color="#2A685A"),
                        ft.Text(
                            value='Pre-works Evidence (Inc Photos) *',
                            size=formatting.get('title') if formatting != None else None,
                            color=ft.colors.GREY_300
                        ),
                        evidences,

                        ft.Divider(color="#2A685A"),

                        reason_no_evidence,
                        
                        work_description,

                        additional_flueing,

                        update_gas_supply,

                        update_condese,

                        make_new_appliance, model_new_appliance, location_new_appliance,

                        ft.Divider(color="#2A685A"),
                        
                        ft.Text(
                            value='Work Quotation Cost Breakdown With SOR Codes',
                            size=formatting.get('title') if formatting != None else None,
                            color=ft.colors.GREY_300
                        ),
                        all_prices_breakdown,
                        
                        ft.Text(
                            value='Uplift - Miscellaneous',
                            size=formatting.get('title') if formatting != None else None,
                            color=ft.colors.GREY_300
                        ),
                        all_uplifts_miscellaneous,
                        
                        ft.Divider(color="#2A685A"),                   
                        
                        gran_total,
                        
                        time_to_complete,
                        
                        date_to_complete,
                        
                        email,


                        ft.Divider(color="#2A685A"),
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

    
    
    page.add(header, form)


ft.app(target=main, assets_dir='assets', upload_dir='assets/uploads', view=ft.AppView.WEB_BROWSER)


#SEARCH BAR https://www.youtube.com/watch?v=S0DfmuCHYGY