from module_airtable import *

class Field_Options:
    def __init__(self, baseID: str, tableID: str, fields: list):
        self.fields = fields
        try:
            self.records = get_Records(baseID=baseID, tableID=tableID, fields=fields)
        except:
            self.records = []
    
    def get_options(self, field):
        try:
            return [{field: item.get(field)} for item in self.records if item.get(field) is not None]
        except:
            return {field: []}
    






# campo = Field_Options(
#     baseID='appB0phO3KnX4WexS', 
#     tableID='tblycaJHzyRku5gYp',
#     fields=[
#         'Gas/Electrical ETC',
#         'Request Type',
#         'Is this on the Planned list?',
#         'Request Category',
#         'Tenure',
#         'Service Level',
#         'Does The Property Have Functioning Heating?',
#         'Does The Property Have Functioning Hot Water?',
#         'Has The Property Been Left With Temporary Heating?',
#         'Condensing or Non-Condensing',
#         'Types Of External Controls On Site',
#         'Is There A Need For Additional Flueing?',
#         'Is There Any Requirement To Update The Gas Supply?',
#         'Is There Any Requirement To Update The Condese?'
#     ]
# )

# print(campo.get_options('Tenure'))