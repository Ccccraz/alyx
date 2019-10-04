from django.core.management import call_command
from data.models import DatasetType, Dataset

DRY = False

dtypes_old2delte_reassign = [
    # _iblrig_Camera.timestamps
    ('93b79e71-c8f6-4d81-b298-2c8f6aefe192', 'b5ec79de-9c9e-4009-8892-10aa2ddb9638'),
    # __iblrig_Camera.timestamps
    ('169323bd-7f91-4b75-a3e5-69530db33d21', 'b5ec79de-9c9e-4009-8892-10aa2ddb9638'),
    # _iblrig_Camera.raw
    ('b3e9dded-027e-4cf0-8392-2baeb3bfcabd', 'e40899d0-a883-40ac-8214-344bcf249d09'),
    # _iblrig_Camera.raw
    ('df68dbb7-8d0e-4a5b-b829-e2a832a89b62', 'e40899d0-a883-40ac-8214-344bcf249d09'),
]

# load init fixtures
call_command('loaddata',  './data/fixtures/data.dataformat.json')
call_command('loaddata',  './data/fixtures/data.datasettype.json')

for pks in dtypes_old2delte_reassign:
    dt2del = DatasetType.objects.filter(pk=pks[0])
    if not dt2del:
        continue
    # if we find any dataset reassign them to the proper one
    datasets = Dataset.objects.filter(dataset_type=dt2del[0])
    if len(datasets):
        d2new = DatasetType.objects.get(pk=pks[1])
        print(f'reassign {dt2del[0].name} to {d2new.name}')
        if not DRY:
            datasets.update(dataset_type=d2new)
    print(f'delete {dt2del[0].name} ')
    if not DRY:
        dt2del.delete()
