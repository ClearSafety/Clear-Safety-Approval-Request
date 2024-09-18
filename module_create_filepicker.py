import flet as ft
import json
from module_azure_cloud import *
from module_general_functions import *
from time import sleep
from unidecode import unidecode

##############################################################################################
# PULL FILE WITH FORMATTING: get static formatting, which does not change according to device
##############################################################################################
try:
    with open('formatting.json', 'r') as file:
        formatting_file = json.load(file)
    
    general_formatting = formatting_file.get('general')
    
except:
    general_formatting=None
    formatting_file=None
##############################################################################################
class Create_Filepicker:
    
    def __init__(
            self,
            page,
            columns_to_occupy: float=None,
            upload_directory: str=None,
            condition: dict=None,
            field_visible: bool=True,
            mandatory: bool=False,
        ):
        
        self.success_upload = []
        self.error_upload = []

        

        # FUNCTION TO CREATE A BOX DIALOG TO UPDATE FILES INTO THE FORM, UPLOAD INTO AZURE CLOUD AND RETRIEVE PUBLIC_URL
        upload_file_progress=ft.AlertDialog(
                title=ft.Text('Uploading files...'),
                content=ft.ProgressBar(
                width=200,
                height=30,
                value=0
                )
            )


        # Function to delete the uploaded file
        def delete_file(e):
            blob_name = e.control.data
            #Deleting from Card where the upload files are shown
            card_list_files.content.controls = list(filter(lambda item: item.data != blob_name, card_list_files.content.controls))
            card_list_files.update()

            #Delete from the list where there are all updated files data that is used to create record in Airtable
            for idx, item in enumerate(self.success_upload):
                if item.get('blob_name') == blob_name:
                    self.success_upload.pop(idx)
            
            #Deleting from Azure
            try:
                deletefile_azure(blob_name=blob_name)
            except:
                ...

            # TURN THE CONDITIONAL FIELD INVISIBLE
            if condition != None:
                if len(self.success_upload) > 0:
                    for item in condition.get('afected_field'):
                        item.visible=False
                        item.update()
                
                else:
                    for item in condition.get('afected_field'):
                        item.visible=True
                        item.update()
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    


        def on_files_selected(e):        
            if e.files:
                # Open progress bar
                page.open(upload_file_progress) 
                
                # Iterate over all files selected by the user
                for file in e.files:
                    
                    filename = unidecode(file.name)
                    
                    # Check the the selected file has suspicious extension, like '.dll', '.exe' etc
                    
                    if not Filetype().safefiletype(filename):
                        self.error_upload.append({'name': filename})
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
                                self.success_upload.append(
                                    {
                                        'blob_name': public_url.get('blob_name'),
                                        'name': file.name,
                                        'url': public_url.get('url'),
                                    }
                                )
                                break
                        
                        if public_url==None or public_url=='':
                            self.error_upload.append({'name': filename})
                    
                    upload_file_progress.content.value += 1/len(e.files)  # UPDATE PROGRESS BAR
                    upload_file_progress.update()  # UPDATE PROGRESS BAR
                
                # If error happens with the upload file process, a dialog window will be displayed with the file name
                if len(self.error_upload) > 0:
                    def close_dialog(e):
                        upload_error_dialog.open=False
                        self.error_upload.clear()
                        page.update()
                    
                    list_upload_errors = '\n'.join(list(map(lambda item: f' - {item.get("name")}', self.error_upload)))
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
                if len(self.success_upload) > 0:
                    card_list_files.content.controls.clear()
                    for item in self.success_upload:
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
                                    ft.Divider(height=1, visible=True if len(self.success_upload) > 1 else False)
                                ],
                                data=item.get('blob_name')
                            )
                        )
                    card_list_files.update()
                    page.update()
                
                # Close the progress bar when the upload processo is concluded
                page.close(upload_file_progress)  # CLOSE PROGRESS BAR
                upload_file_progress.content.value=0 # RESET PROGRESS BAR
            
            self.files.update()
            

            # TURN THE CONDITIONAL FIELD INVISIBLE
            if condition != None:
                if len(self.success_upload) > 0:
                    for item in condition.get('afected_field'):
                        item.visible=False
                        item.update()
                
                else:
                    for item in condition.get('afected_field'):
                        item.visible=True
                        item.update()



        # THE FILE PICKER OBJECT TO HANDLE THE PICKER
        file_picker = ft.FilePicker(on_result=on_files_selected)
        page.controls.append(file_picker)
        


        # MAIN PROPERTY, WITH THE BUTTON TO UPLOAD AND THE LIST OF UPLOADED FILES
        self.files = ft.ResponsiveRow(
            col=columns_to_occupy,
            columns=3,
            controls=[
                ft.ElevatedButton(
                    col=1,
                    text="Upload Files",
                    on_click=lambda _: file_picker.pick_files(dialog_title='Clear Safety - Select Evidences', allow_multiple=True),
                    height=50,
                    style=ft.ButtonStyle(
                        color=ft.colors.BLACK, 
                        bgcolor=getattr(ft.colors, general_formatting.get('field_bgcolor')) if general_formatting != None else None,
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
            ],
            data=self.success_upload
        )
    
    def delete(self):
        self.success_upload = []
        self.files.data = []
        self.files.data = self.success_upload
        #self.files.update()

    
    
    

    


if __name__ == '__main__':
    ...       
    # def main(page: ft.Page):
        
    #     def printar(e):
    #         texto.value = ''
    #         texto.update()
    #         #sleep(5)
    #         texto.value = files.data
    #         texto.update()


    #     page.add(
    #         files := create_Filepicker(
    #             page=page,
    #             columns_to_occupy=3,
    #             upload_directory='assets/uploads'
    #         ),

    #         ft.ElevatedButton(text='Imprimir', on_click=printar),
    #         texto := ft.Text(value='ok')
    #     )
    
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER, upload_dir='assets/uploads')
