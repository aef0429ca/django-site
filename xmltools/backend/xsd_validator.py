import xml.etree.ElementTree as ET
from lxml import etree
from io import StringIO, BytesIO
import sys
import os
import django_project.settings as settings


def validate_xml(filename_xml, filename_xsd):
    ''' Attempts to parse and validate XML against XSD '''
    output = {}
    output['Status'] = False

    # open and read xml file
    xml = open(filename_xml, "rb").read()
    # open and read schema file
    xsd = open(filename_xsd, "rb").read()
    
    # parse schema file
    xmlschema_doc = etree.parse(BytesIO(xsd))
    xmlschema = etree.XMLSchema(xmlschema_doc)

    # parse xml
    try:
        doc = etree.parse(BytesIO(xml))
        # print('XML well formed, syntax ok.')
        output['XML Well Formed'] = True
        # validate parsed file against schema
        try:
            xmlschema.assertValid(doc)
            # print('XML valid, schema validation ok.')
            output['XML Well Formed'] = True
            output['Status'] = True
        except etree.DocumentInvalid as err:
            # print('Schema validation error, see error_schema.log')
            output['Error'] = 'Fail, invalid format'
            output['Status'] = False
            with open(os.path.join(settings.XMLSCHEMA_LOG_PATH, 'error_schema.log'), 'w') as error_log_file:
                error_log_file.write(str(err.error_log))
            # quit()
        except:
            output['Error'] = 'Unknown error, exiting.'
            output['Status'] = False
            # print('Unknown error, exiting.')
    # check for file IO error
    except IOError as e:
        # print('Invalid File: ', e)
        output['Error'] = 'IO Fail'
        output['Status'] = False
    # check for XML syntax errors
    except etree.XMLSyntaxError as err:
        # print('XML Syntax Error, see error_syntax.log')
        output['Error'] = 'Fail, Syntax Error'
        output['Status'] = False
        with open(os.path.join(settings.XMLSCHEMA_LOG_PATH, 'error_schema.log'), 'w') as error_log_file:
            error_log_file.write(str(err.error_log))
    except:
        print('Unknown error, exiting.')
        output['Error'] = 'Unknown error, exiting.'
        output['Status'] = False
        
    return output
