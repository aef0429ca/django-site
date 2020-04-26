import gc
import os
import requests
from io import StringIO, BytesIO
import sys
import pandas as pd
import pandas_profiling as pdp
import numpy as np
import collections
from lxml import etree
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


STATICFILES_DIRS = os.path.join(BASE_DIR, 'static')
DOC_PATH = os.path.join(BASE_DIR, 'media/documents')
FORMAT_XSD = {'zap': 'zap.xsd', 'ingaia': 'ingaia.xsd', 'etica': 'etica.xsd', 'lopes': 'lopes.xsd'}


def parse_zap_to_df(xml_file):
    """Parse the a stripped input XML file and stores the result in a pandas 
    DataFrame with only key columns as specified. 
    
    Concatenates nested image urls into single string.
    
    Function needs to grab dict with format specification to allow for more than one format.
    """

    # Columns that verifies the format
    df_cols = ['CodigoImovel','CodigoCliente','TipoImovel','SubTipoImovel','CategoriaImovel','Cidade','Bairro','Endereco','Numero','Complemento','CEP','PrecoVenda','PrecoLocacao','AreaUtil','AreaTotal','QtdDormitorios','QtdSuites','QtdBanheiros','QtdSalas','QtdVagas','QtdElevador','QtdUnidadesAndar','QtdAndar','AnoConstrucao','EmDestaque','Descricao','UF','Fotos']


    xtree = ET.parse(xml_file)
    xroot = xtree.getroot()
    
    # Get tags below root
    # Use instead of the vista_cols var?
    tags = []
    # this may vary depending on format - be careful
    for child in xroot[0][0]:
        tags.append(child.tag)

    rows = []
    
    for node in xroot[0]:
        res = []
        # res.append(node.attrib.get(df_cols[0]))
        for el in df_cols[0:]:
            if el == 'Fotos' and node is not None and node.find(el) is not None:
                images = []
                for foto in node.find('Fotos'):
                    url = foto.find('URLArquivo').text
                    images.append(url)
                urls = '|'.join(map(str, images)) 
                res.append(urls)
            elif node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else: 
                res.append(None)
        
        rows.append({df_cols[i]: res[i] 
                     for i, _ in enumerate(df_cols)})
    
    df = pd.DataFrame(rows, columns=df_cols)
        
    return df


def parse_gaia_to_df(xml_file):
    """Parse the a stripped input XML file and stores the result in a pandas 
    DataFrame with only key columns as specified. 
    
    Concatenates nested image urls into single string.
    
    Function needs to grab dict with format specification to allow for more than one format.
    """

    # Columns that verifies the format
    df_cols = ['CodigoImovel','TipoImovel','SubTipoImovel','EmDestaque','Endereco','Numero','Complemento','Bairro','Cidade','Uf','CEP','PrecoRevenda','PrecoAluguel','AreaM2Util','AreaM2Total','AreaM2Terreno','QtdDormitorios','QtdSuites','QtdBanheiros','QtdVagas','Descricao','Fotos']

    xtree = ET.parse(xml_file)
    xroot = xtree.getroot()
    
    # Get tags below root
    # Use instead of the vista_cols var?
    tags = []
    # this may vary depending on format - be careful
    for child in xroot[0][0]:
        tags.append(child.tag)

    rows = []
    
    for node in xroot[0]:
        res = []
        # res.append(node.attrib.get(df_cols[0]))
        for el in df_cols[0:]:
            if el == 'Fotos' and node is not None and node.find(el) is not None:
                images = []
                for foto in node.find('Fotos'):
                    url = foto.find('FotoUrl').text
                    images.append(url)
                urls = '|'.join(map(str, images)) 
                res.append(urls)
            elif node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else: 
                res.append(None)
        
        rows.append({df_cols[i]: res[i] 
                     for i, _ in enumerate(df_cols)})
    
    df = pd.DataFrame(rows, columns=df_cols)
        
    return df


def parse_lopes_to_df(xml_file):
    """Parse the a stripped input XML file and stores the result in a pandas 
    DataFrame with only key columns as specified. 
    
    Concatenates nested image urls into single string.
    
    Function needs to grab dict with format specification to allow for more than one format.
    """

    # Columns that verifies the format
    df_cols = ['id','endereco','numero','complemento','bairro','cidade','uf','cep','valordoimovel','valordoaluguel','numerodequartos','QtdSuites','numerodevagas','areaprivada','situacaodoimovel','tipo','subtipo','descricao','fotos']

    xtree = ET.parse(xml_file)
    xroot = xtree.getroot()
    
    rows = []
    
    for node in xroot:
        res = []
        # res.append(node.attrib.get(df_cols[0]))
        for el in df_cols[0:]:
            if el == 'fotos' and node is not None and node.find(el) is not None:
                images = []
                for foto in node.find('fotos'):
                    try:
                        url = foto.text
                    except AttributeError as e:
                        pass
                    images.append(url)
                urls = '|'.join(map(str, images)) 
                res.append(urls)
            elif node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else: 
                res.append(None)
        
        rows.append({df_cols[i]: res[i] 
                     for i, _ in enumerate(df_cols)})
    
    df = pd.DataFrame(rows, columns=df_cols)
        
    return df



def create_profile(df, file_name):
    ''' Run pandas profiling on df to generate file_name as html '''
    profile = pdp.ProfileReport(df)
    # create profile file with html extension
    html_file_name = file_name.split('.')[0] + '.html'
    # write the profile file to this path
    profile_file = os.path.join(STATICFILES_DIRS, 'profiles', html_file_name)
    # create the profile
    profile.to_file(profile_file)
    del df
            
    return html_file_name


def delta_xmls(new_xml_file, old_xml_file, cols, key_cols):
    df_old = parse_XML(old_xml_file, cols)
    df_old = df_old.loc[:, vista_key_cols]
    df_new = parse_XML(new_xml_file, cols)
    df_new = df_new.loc[:, vista_key_cols]
    
    new_listings =  list(set(df_new['CodigoImovel']) - set(df_old['CodigoImovel']))
    unflagged_listings =  list(set(df_old['CodigoImovel']) - set(df_new['CodigoImovel']))
 
    df_new_exists = df_new[~df_new['CodigoImovel'].isin(new_listings)]
    df_old_exists = df_old[~df_old['CodigoImovel'].isin(unflagged_listings)]
    
    df_new_exists = df_new_exists.sort_values(by=['CodigoImovel','PrecoVenda','PrecoLocacao'])
    df_old_exists = df_old_exists.sort_values(by=['CodigoImovel','PrecoVenda','PrecoLocacao'])
    
    df_old_exists.set_index('CodigoImovel', inplace=True)
    df_old_exists.sort_index(inplace=True)
    df_new_exists.set_index('CodigoImovel', inplace=True)
    df_new_exists.sort_index(inplace=True)

    stacked_dfs = (df_old_exists != df_new_exists).stack()
    changed_dfs = stacked_dfs[stacked_dfs]
    changed_dfs.index.names = ['CodigoImovel', 'col']

    difference_locations = np.where(df_old_exists != df_new_exists)
    changed_from = df_old_exists.values[difference_locations]
    changed_to = df_new_exists.values[difference_locations]

    changes = pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed_dfs.index)
    changes = changes[ (changes['from'].notna()) & (changes['to'].notna()) ]
    
    changes2 = changes.reset_index()
    
    result = {'Vol. old XML': df_old.shape[0],
              'Vol. new XML': df_new.shape[0],
              'New Listings': len(new_listings),
              'Unflagged': len(unflagged_listings),
              'Changed Listings': len(set(changes2['CodigoImovel'])),
              'Changed Values': changes2.shape[0]
             }
    
    # result = [[ df_old.shape[0], df_new.shape[0], len(set(changes2['CodigoImovel'])), changes2.shape[0], len(unflagged_listings), len(new_listings)]] 
    # df_results = pd.DataFrame(result, columns = ['Old XML', 'New XML', 'Changed Listings', 'Changed Values', 'Unflagged', 'New']) 
        
    del df_old, df_new, df_new_exists, df_old_exists, stacked_dfs, difference_locations, changed_dfs, changed_from, changed_to, changes
    gc.collect()
    
    return new_listings, unflagged_listings, changes2, result
