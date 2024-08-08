import flet as ft
from azure_cloud import *
from time import sleep

def main(page: ft.Page):
    

    def onresult(e):
        for file in e.files:
            filename=file.name
            upload_url=page.get_upload_url(filename, 60)

            file_picker.upload(
                files=[
                    ft.FilePickerUploadFile(
                        name=filename,
                        upload_url=upload_url,
                        method='PUT'

                    )
                ]
            )
            print(filename)
            sleep(2)
            print(uploadfile_azure(
                file_name=filename,
                path_file='assets/uploads'
            ))
    
            

    file_picker = ft.FilePicker(
        on_result=onresult,

    )


    page.overlay.append(file_picker)

    btn = ft.ElevatedButton(
        on_click=lambda _: file_picker.pick_files(allow_multiple=True)
    )

    page.add(btn)


ft.app(target=main, assets_dir='assets', upload_dir='assets/uploads')