import os
import sys
import time
import requests
import subprocess
from urllib.parse import urlsplit, urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import django_project.settings as settings
import logging

from xmltools.models import Document
from .forms import DocumentForm, UrlForm, FormatForm
from .backend import xml_clean, xml_profiling, xsd_validator

XSD_FORMATS = ['zap', 'gaia', 'lopes']

FORMAT_CHOICES = ((0, "UNKNOWN"),
                  (1, "ZAP"),
                  (2, "GAIA"),
                  (3, "LOPES"),
)


@login_required
def home(request):
    return render(request, 'xmltools/index.html')


def xml_upload(request):
    if request.POST:
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            logging.warning(form.cleaned_data)
            form = form.save()
            logging.warning('Form is valid!')
            doc = Document.objects.get(pk=form.id)

            tmp_file = 'temp_'+ str(time.strftime('%Y%m%d%H%M%S')) + '.xml'
            os.rename(doc.document.path, os.path.join(settings.DOC_ROOT, tmp_file))
            # updates the document record with the temporary file name
            doc.file_name = tmp_file
            doc.save(update_fields=['file_name'])
            messages.success(request, 'File uploaded and saved successfully!')

            return redirect('xml_format_test', form.id)
        else:
            logging.warning('Form is invalid!')
            messages.warning(request, 'Please correct form error(s) below.') 
    else:
        form = DocumentForm()
        return render(request, 'xmltools/xml_upload.html', {'form': form })


def xml_fetch(request):
    if request.POST:
        urlform = UrlForm(request.POST)
        if urlform.is_valid():
            form = urlform.save()
            doc = Document.objects.get(pk=form.id)
            tmp_file = 'temp_'+ str(time.strftime('%Y%m%d%H%M%S')) + '.xml'
                
            response = requests.get(doc.url)
            with open(os.path.join(settings.DOC_ROOT, tmp_file), 'wb') as file:
               file.write(response.content)

            # updates the document record with the temporary file name
            doc.file_name = tmp_file
            doc.save(update_fields=['file_name'])
                        
            if os.path.getsize(os.path.join(settings.DOC_ROOT, tmp_file)) == 0:
                messages.error(request, 'File is of size 0! Verify that file exists at origin.')
            else:
                messages.success(request, 'File registered and saved successfully!')
        else:
            messages.warning(request, 'Please correct form error(s) below.') 
        
        # return redirect('xml_format_test.html')
        return render(request, 'xmltools/xml_format_test.html', form.id)
    else:
        urlform = UrlForm()
        return render(request, 'xmltools/xml_fetch.html', {
         'urlform': urlform
         })


def xml_format_test(request, pk):
    request.session['Format_guess'] = 'UNKNOWN'
    logging.warning('Inside xml_format_test func')
    ''' Takes raw input and formats to stripped xml
        outputs to folder /final '''
    if request.POST:
        form = FormatForm(request.POST)
        if form.is_valid():
            format_test = form.save()
            doc = Document.objects.get(pk=pk)
            request.session['Format_guess'] = form.cleaned_data['format_guess']
            
            # xmllint, one tag per row with breaks, outputs to tmp/ dir
            xml_clean.pretty_print(doc.file_name)
            
            if doc.format_guess != 'UNKNOWN':
            # move guessed format to front of list
                XSD_FORMATS.insert(0, XSD_FORMATS.pop(XSD_FORMATS.index(doc.format_guess.lower())))
            else:
                pass
            # test formats one by one as per order in XSD_FORMATS
            # filter on tags for each format and attempt to validate
            for xsd_format in XSD_FORMATS:
                context = {}
                xsd_file = xsd_format.lower() + '.xsd'
                # filters tags and outputs to final/ dir
                xml_clean.filter_tags(doc.file_name, xsd_format)
                # testing validation against xsd    
                validation_test = xsd_validator.validate_xml(os.path.join(settings.FINAL_PATH, doc.file_name), os.path.join(settings.XSD_PATH, xsd_file))
                logging.warning(validation_test)
                
                if validation_test['Status']:
                    # request.session['Format'] = xsd_format.upper()
                    # doc = Document.objects.get(pk=pk)
                    doc.format_valid = validation_test
                    doc.save(update_fields=['format_valid'])

                    logging.warning(xsd_format.upper())
                    break
                else:
                    # request.session['Format'] = 'Unknown'
                    context['Format'] = 'Unknown'
            
            return redirect('xml_analyze.html', form.id)
        else:
            # form is invalid,  stay on same page
            messages.warning(request, 'Please correct form error(s) below.')
            return redirect('xml_analyze.html')
    else:
        # For when GETing the page
        formatform = FormatForm()
        return render(request, 'xmltools/xml_format_test.html', {
        'formatform': formatform
        })



def xml_analyze(request):
    if request.POST:
        pk = request.session['pk']
        doc = Document.objects.get(pk=pk)
        format = request.session['Format']
        # Get file path to cleaned xml
        file_name = os.path.join(settings.FINAL_PATH, doc.file_name)
        # Pass xml into parsing and return df
        if format == 'ZAP':
            df = xml_profiling.parse_zap_to_df(file_name)
        elif format == 'GAIA':
            df = xml_profiling.parse_gaia_to_df(file_name)
        elif format == 'LOPES':
            df = xml_profiling.parse_lopes_to_df(file_name)    
        # Run profiling on df and write to file_name
        profile_file = xml_profiling.create_profile(df, doc.file_name)
        request.session['profile_file'] = os.path.join(settings.PROFILE_URL, profile_file)
        
        return redirect('xml_profile.html')
    else:
        return render(request, 'xmltools/xml_analyze.html')



def xml_profile(request):
    return render(request, 'xmltools/xml_profile.html')