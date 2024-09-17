import flet as ft
import json
from approval_request import main





def main_cover(page: ft.Page):

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



    ###############################################################################################################################################################################################
    # WINDOW PARAMETERS
    ###############################################################################################################################################################################################
    page.window.always_on_top=True
    page.bgcolor=getattr(ft.colors, general_formatting.get('page_bgcolor'))  # Color grab from Clear Safety website
    page.adaptive=True
    page.title='Clear Safety: Approval Request'
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.vertical_alignment=ft.MainAxisAlignment.START
    page.padding=ft.padding.all(0)
    ###############################################################################################################################################################################################



    ###############################################################################################################################################################################################
    # HEADER
    ###############################################################################################################################################################################################
    header=ft.Container(
        padding=ft.padding.only(bottom=20, right=40, left=40),
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



    # FUNCTION TO DETERMINE WHAT MUST BE DONE IN EACH ROUTE
    def route_change(route):
        
        # Clear the page before calling the other subdomains
        page.controls.clear()

        # Call the specific form based on the contractor
        if page.route == "/":
            page.add(header)
            
        elif page.route == "/ghnctewsb":
            main(page=page, contractor='BSW')
        
        elif page.route == "/ghnctetertaw":
            main(page=page, contractor='Watret')
        
        elif page.route == "/ghnctetk":
            main(page=page, contractor='KT')
        
        else:
            page.add(header)
            page.add(ft.Text("Page not found", size=50, color='white'))

        page.update()


    # CALL THE FUNCTION "route_change" TO IDENTIFY WHAT MUST BE DONE AFTER THE ROUTE CHANGE
    page.on_route_change = route_change


    # IT CALLS THE "/" AS THE INITIAL PAGE. AS CONSEQUENCE OF USING "page.go", "page.on_route_change" WILL BE CALLED
    page.go(page.route)


ft.app(target=main_cover, view=ft.AppView.WEB_BROWSER, assets_dir='assets', upload_dir='assets/uploads')