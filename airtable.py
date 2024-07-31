import requests
import os
import json

#token = os.getenv('AIRTABLE_TOKEN')
with open('airtable-token.json', 'r') as file:
    token = json.load(file)
    token = token.get('token')

# FUNCTION USED TO GET A LIST OF RECORDS FROM A CERTAIN AIRTABLE'S TABLE
def get_Records(baseID: str, tableID: str, fields: list=None) -> list:
    '''
    This function fetchs the data from a specific Table from the Airtable.
    It has 3 parameters, but only 2 are mandatories.

    Parameters:
        baseID (str):  ID of the Airtable's Base
        tableID (str): ID of the Airtable's Table
        fields (list, optional): List of all Table's fields (name or ID) to be returned. Ideally use field's ID. If not passed, request will return all fields.
    
    Return:
        list of dicionaries with all records from the Table.
    
    -------------------------------------------------------------------------------------

    Example:
        get_Records(appv8tfNC93wY5Q1b, tblqlw2rABYI2SxOi, ['SOR Description', 'SOR Code'])
        get_Records(appv8tfNC93wY5Q1b, tblqlw2rABYI2SxOi, ['flds8XpOM0LnOHY1Q', 'fldpRToSrBze1EzyI'])

        return [{'SOR Description': 'WET-VAC:SUPPLY TEMPORARY [RATE PER WEEK] DOMESTIC', 'SOR Code': 'EE163607'}, {'SOR Description': 'EQUIPMENT:RESPONSE CALL-OUT REPAIR NO PARTS', 'SOR Code': 'EE150113'}]
    '''

    if fields:
        fields = '&'.join(list(map(lambda x: 'fields%5B%5D=' + x.replace(" ", '%20'), fields)))
        
    
    # FETCH DATA
    def fetch(next: str=None):
        url = f'https://api.airtable.com/v0/{baseID}/{tableID}?{fields}&offset={next}'
        header={'Authorization': token}

        return requests.get(url=url, headers=header)

    records = []
    next = ''
    while True:
        data = fetch(next)
        
        if data.status_code == 200:
            data = data.json()
            content = list(map(lambda x: x.get('fields'), data.get('records')))
            records.extend(content)
            next = data.get('offset')
        if next == None:
            break
            
    return records


# FUNCTION USED TO CREATE A RECORD IN A CERTAIN AIRTABLE'S TABLE
def create_Record(baseID: str, tableID: str, content: dict) -> str:
    '''
    This function creates a record in a specific Table from the Airtable.
    It has 3 parameters.

    Parameters:
        baseID (str):  ID of the Airtable's Base
        tableID (str): ID of the Airtable's Table
        content (dict): Content for each field, following this pattern:
            Field Types: singleLineText, multilineText, singleSelect, phoneNumber, email, url
            Pattern: str: str  ---> example: {'CO': 'Clear Safety'}

            Field Types: number, currency, percent
            Pattern: str: int  ---> example: {'Cost': 100}

            Field Type: date
            Pattern: str: str 'YYYY-MM-DD'  ---> example: {'Date': '2024-07-12'}

            Field Type: multipleSelects
            Pattern: str: list of str  ---> example: {'Options': ['A', 'B']}

            Field Type: checkbox
            Pattern: str: bool  ---> example: {'Sent?': True}

            Field Type: multipleAttachments
            Pattern: str: list of dict  ---> example: {'Photos': [{'url': 'http://wwww.example/api/img.png, 'filename': 'img.png'}, {'url': 'http://wwww.example/api/file1.pdf, 'filename': 'file1.pdf'}]}
    
    Return:
        str with 'Successful' or 'Error: {status_code}'
    
    -------------------------------------------------------------------------------------  

    Example:
        create_Record(appv8tfNC93wY5Q1b, tblqlw2rABYI2SxOi, {['SOR Code': '132456]})

        return 'Successful'
    '''
    
    url = f"https://api.airtable.com/v0/{baseID}/{tableID}"
    header={
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data_content={
        "records": [
            {
                "fields": content
            }
        ]
    }
    
    response = requests.post(
        url=url,
        headers=header,
        json=data_content
    )

    
    if response.status_code == 200:
        return 'Successful'
    else:
        return f'Error: {response.status_code}'


def update_Record(baseID: str, tableID: str, recordID: str, content: dict):
    
    url = f"https://api.airtable.com/v0/{baseID}/{tableID}/{recordID}"
    header={
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data_content={
        "fields": content
    }
    
    response = requests.patch(
        url=url,
        headers=header,
        json=data_content
    )

    if response.status_code == 200:
        return "Successful"
    else:
        return "Error"




def delete_Record(recordID):
    base = "appMcOq1kncqafleI"
    table = "tbloLozTMGyG4s2wp"
    url = f"https://api.airtable.com/v0/{base}/{table}/{recordID}"
    header={"Authorization": token}

    response = requests.delete(
        url=url,
        headers=header
    )

    if response.status_code == 200:
        return "Successful"
    else:
        return "Error"




def table_fields(baseID: str, tabaseID: str):
    url = f'https://api.airtable.com/v0/meta/bases/{baseID}/tables'
    header={'Authorization': token}

    data = requests.get(
        url=url,
        headers=header
    )

    if data.status_code == 200:
        data = data.json()
        return list(filter(lambda x: x.get('id') == tabaseID, data.get('tables')))[0].get('fields')
        
    
    else:
        return f'Error: {data.status_code}'


if __name__ == '__main__':
    print(get_Records(baseID='appB0phO3KnX4WexS', tableID='tblycaJHzyRku5gYp'))