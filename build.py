'''
Build cancerdrugs dataset
'''

import logging, os, csv, gzip, json, mimetypes, hashlib, zipfile, glob, re
import concurrent.futures, datetime, os, urllib.request, shutil
import xml.etree.ElementTree as ET
import pandas as pd
from utils import download_file, get_json, create_archive, normalize, snake_to_camel

from dotenv import load_dotenv
load_dotenv()

# Configuration
RELEASE = '2021-03'

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
DIST_FOLDER = os.path.join(BASE_PATH, 'dist')
EXT_FOLDER = os.path.join(BASE_PATH, '.cache')

NCI_ANTINEOPLASTIC_AGENTS = 'https://evs.nci.nih.gov/ftp1/NCI_Thesaurus/Drug_or_Substance/Antineoplastic_Agent.txt'
NCI_THESAURUS_URL = 'http://evs.nci.nih.gov/ftp1/NCI_Thesaurus/Thesaurus.OWL.zip'
EMAR_EPAR_URL = 'https://www.ema.europa.eu/sites/default/files/Medicines_output_european_public_assessment_reports.xlsx'


def parse_nci_antineoplastic_agents(path):
    '''Parse NCI antineoplastic agents.'''
    agents = pd.read_csv(path, delimiter='\t', keep_default_na=False, encoding='cp850')
    agents.rename(columns={
        'Code': 'code',
        'NCIt Preferred Name': 'preferredName',
        'Synonyms': 'synonyms',
        'Definition': 'definition',
        'Semantic Type': 'semanticType'
    }, inplace=True)
    agents['synonyms'] = agents['synonyms'].str.split(pat=r' \|\| ', expand=False)
    return agents


def parse_nci_thesaurus(path, identifiers=[]):
    '''Parse NCI thesaurus.'''
    records = []
    with zipfile.ZipFile(path) as zf:
        with zf.open('Thesaurus.owl') as f:
            for _, elem in ET.iterparse(f, events=('end',)):
                if elem.tag.endswith('Class'):
                    try:
                        identifier = elem.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'].partition('#')[2]
                    except:
                        identifier = ''
                    fda_unii_code = elem.findtext('{http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#}P319', '')
                    if fda_unii_code and identifier in identifiers:
                        subclass_of = []
                        for e in elem.findall('{http://www.w3.org/2000/01/rdf-schema#}subClassOf'):
                            if '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource' in e.attrib:
                                parent = e.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'].partition('#')[2]
                                subclass_of.append(parent)
                        records.append({
                            'identifier': identifier,
                            'subclassOf': subclass_of,
                            'synonyms': [e.text for e in elem.findall('{http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#}P90')],
                            'preferredName': elem.findtext('{http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#}P108', ''),
                            'semanticType': elem.findtext('{http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#}P106', ''),
                            'casRegistry': elem.findtext('{http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#}P210', ''),
                            'chebiId': elem.findtext('{http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#}P368', ''),
                            'chemicalFormula': elem.findtext('{http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#}P350', ''),
                            'definition': elem.findtext('{http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#}P97', '').replace(' (NCI04)', ''),
                            'fdaUniiCode': fda_unii_code
                        })
                elif elem.tag.endswith('Axiom'):
                    elem.clear()
    logging.info(f'Successfully parse NCI thesaurus ({len(records)} records).')
    return pd.DataFrame.from_records(records)


def retrieve_openfda_data(unii, api_key=None):
    '''Retrieve drug labeling from OpenFDA API.'''
    print(f'Querying OpenFDA API for UNII {unii}')
    labels = []
    try:
        url = f'https://api.fda.gov/drug/label.json?search=openfda.unii:{unii}&limit=99'
        if os.environ.get('OPENFDA_API_KEY'):
            url = url + '&api_key=' + os.environ.get('OPENFDA_API_KEY')
        obj = get_json(url, cache_dir=EXT_FOLDER)
        for d in obj['results']:
            labels.append({
                'indication': d['indications_and_usage'][0],
                'brand': d['openfda']['brand_name'][0],
                'manufacturer': d['openfda']['manufacturer_name'][0],
                'splSetId': d['openfda']['spl_set_id'][0]
                })
    except:
        print('error')
    return labels


def parse_ema_epar_data(path):
    '''Download and process EMA EPAR data.'''
    ema_epar = pd.read_excel(path, skiprows=8, keep_default_na=False)
    ema_epar_filtered = ema_epar[
        (ema_epar['Category'] == 'Human') &
        (ema_epar['Authorisation status'] == 'Authorised')
        ]
    ema_epar_filtered = pd.DataFrame({
        'medicineName': ema_epar_filtered['Medicine name'],
        #'therapeuticArea': ema_epar_filtered['Therapeutic area'],
        'inn': ema_epar_filtered['International non-proprietary name (INN) / common name'],
        'activeSubstance': ema_epar_filtered['Active substance'],
        #'productNumber': ema_epar_filtered['Product number'],
        #'patientSafety': ema_epar_filtered['Patient safety'],
        #'authorisationStatus': ema_epar_filtered['Authorisation status'],
        #'atcCode': ema_epar_filtered['ATC code'],
        #'additionalMonitoring': ema_epar_filtered['Additional monitoring'],
        #'generic': ema_epar_filtered['Generic'],
        #'biosimilar': ema_epar_filtered['Biosimilar'],
        #'conditionalApproval': ema_epar_filtered['Conditional approval'],
        #'exceptionalCircumstances': ema_epar_filtered['Exceptional circumstances'],
        #'acceleratedAssessment': ema_epar_filtered['Accelerated assessment'],
        #'orphanMedicine': ema_epar_filtered['Orphan medicine'],
        'marketingAuthorisationDate': ema_epar_filtered['Marketing authorisation date'],
        #'dateOfRefusalOfMarketingAuthorisation': ema_epar_filtered['Date of refusal of marketing authorisation'],
        'marketingAuthorisationHolder': ema_epar_filtered['Marketing authorisation holder/company name'],
        #'humanPharmacotherapeuticGroup': ema_epar_filtered['Human pharmacotherapeutic group'],
        #'dateOfOpinion': ema_epar_filtered['Date of opinion'],
        #'decisionDate': ema_epar_filtered['Decision date'],
        #'revisionNumber': ema_epar_filtered['Revision number'],
        'conditionIndication': ema_epar_filtered['Condition / indication'],
        #'firstPublished': ema_epar_filtered['First published'],
        #'revisionDate': ema_epar_filtered['Revision date'],
        'url': ema_epar_filtered['URL']
        })
    logging.info(f'Successfully parsed EMA EPAR data ({len(ema_epar_filtered)} records).')
    return ema_epar_filtered


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logging.info(f'Building cancerdrugs database release {RELEASE}')
    # Create folders
    os.makedirs(EXT_FOLDER, exist_ok=True)
    shutil.rmtree(DIST_FOLDER, ignore_errors=True)
    os.makedirs(os.path.join(DIST_FOLDER, 'drugs'))
    # Load/retrieve external data
    nci_antineiplastic_agents_file, _, _ = download_file(NCI_ANTINEOPLASTIC_AGENTS, path=EXT_FOLDER, filename='Antineoplastic_Agent.txt')
    nci_antineoplastic_agents = parse_nci_antineoplastic_agents(nci_antineiplastic_agents_file)
    
    nci_thesaurus_file, _, _ = download_file(NCI_THESAURUS_URL, path=EXT_FOLDER, filename='Thesaurus.OWL.zip')    
    nci_thesaurus = parse_nci_thesaurus(nci_thesaurus_file, identifiers=nci_antineoplastic_agents['code'].tolist())

    ema_epar_file, _, _ = download_file(EMAR_EPAR_URL, path=EXT_FOLDER, filename='Medicines_output_european_public_assessment_reports.xlsx')
    ema_epar = parse_ema_epar_data(ema_epar_file)
    # Aggregate drug data
    logging.info('Aggregate drug data.')
    index = dict(release=RELEASE, drugs=[])
    for row in nci_thesaurus.to_dict(orient='records'):  
        record = {
            'id': normalize(row['preferredName'])
        }
        record['nciThesaurus'] = row
        record['fdaDrugLabel'] = retrieve_openfda_data(row['fdaUniiCode'])
        record['emaEpar'] =  ema_epar[
                ema_epar['inn'].str.lower() == row['preferredName'].lower()
                ].to_dict(orient='records')
        
        logging.info(f'Write to file dist/drugs/{record["id"]}.json')
        open(os.path.join(DIST_FOLDER, 'drugs', f'{record["id"]}.json'), 'w').write(json.dumps(record, indent=2, sort_keys=True, default=str))

        index['drugs'].append({
            'id': record['id'],
            'preferredName': record['nciThesaurus']['preferredName'],
            'synonyms': record['nciThesaurus']['synonyms'],
            'fdaUniiCode': record['nciThesaurus']['fdaUniiCode']
            })

    with open(os.path.join(DIST_FOLDER, 'index.json'), 'w') as f:
        f.write(json.dumps(index, indent=2, sort_keys=True, default=str))
    
    # Write data to file
    logging.info('Create archive.')
    create_archive(os.path.join(DIST_FOLDER, f'cancerdrugs-{RELEASE}.zip'), DIST_FOLDER, '**/*.json')

    # Finish
    logging.info('Build completed.')
