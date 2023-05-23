#!/usr/bin/env python

#Copyright (C) 2023
#This code is used to get the psrfits header information
#Please report any issues or bugs directly to the authors， xiejintao@zhejianglab.com

import os
import sys
from astropy.io import fits
import filterbank as fil

def Usage():

    print("\n")
    print("-"*10)
    print("\n")
    print("Usage: python header_size.py psrfitfile.fits \n")
    print("-header : output the header \n")
    print("-col : output the psrfits columns information \n")
    print("-datasize : output the data size  in byte\n")
    print("-datasize : output the heaader size in byte\n")
    print("-h : help information \n")
    print("-"*10)
    print("\n")

def get_tsamp(hdu):
    '''
    get time resolution
    '''
    try:
        tbin = hdu[0].header['TBIN']
    except:
        tbin = hdu[1].header['TBIN']
    return tbin


def get_nbit(hdu):
    '''
    get the bit of sample
    '''
    try:
        nbit = hdu[0].header['NBITS']
    except:
        nbit = hdu[1].header['NBITS']
    return nbit

def get_npol(hdu):
    '''
    get the number of polarization
    '''
    
    try:
        npol = hdu[0].header['NPOL']
    except:
        npol = hdu[1].header['NPOL']
    return npol
        
def get_nchan(hdu):
    '''
    get the number of channel
    '''

    try:
        nchan = hdu[0].header['NCHAN']
    except:
        nchan = hdu[1].header['NCHAN']
    return nchan

def get_nsampsubint(hdu):
    '''
    gety the number of sample in each subint
    '''
    try:
        nsampsubint = hdu[0].header['NSBLK']
    except:
        nsampsubint = hdu[1].header['NSBLK']
    return nsampsubint


def get_nsubint(hdu):
    '''
    get the number of subint
    '''
    try:
        nsubint = hdu[0].header['NAXIS2']
    except:
        nsubint = hdu[1].header['NAXIS2']
    return nsubint

def output_header(hdu,pri=False,sub=False):
    '''
    output header information
    '''
    
    if sub == False:
        try:
            header_pri = hdu[0].header
            if pri ==True:
                return header_pri
                #break
            else:
                print("\n")
                print("-"*10,"the primary header infomation","-"*10)
                print("\n")
                print(repr(header_pri)) ## print the primary header
                print("\n")
                print("-"*22,"primary header End","-"*22)
                print("\n")
                
                try:
                    header_sub = hdu[1].header
                    print("\n")
                    print("-"*10,"the sub header infomation","-"*10)
                    print("\n")
                    print(repr(header_sub)) ## print sub table header
                    print("\n")
                    print("-"*22,"sub header End","-"*22)
                    print("\n")
                except:
                    print("Please Check whether the input file is psrfits")
        except:
            print("Please Check whether the input file is psrfits")
    else:
        try:
            header_sub = hdu[1].header
            if sub ==True:
                return header_sub
            else:
                print("\n")
                print("-"*10,"the sub header infomation","-"*10)
                print("\n")
                print(repr(header_sub)) ## print sub table header
                print("\n")
                print("-"*22,"End","-"*22)
                print("\n")
        except:
            print("Please Check whether the input file is psrfits")
        
        
def output_columns(hdu, re = False):
    '''
    output  columns information
    '''
    try:
        columns = hdu[1].columns
        if re == False:
            print("\n")
            print("-"*10,"the column infomation","-"*10)
            print("\n")
            print(repr(columns))
            print("\n")
            print("-"*20,"End","-"*20)
            print("\n")
        else:
            return columns
        
    except:
        print("Please Check whether the input file is psrfits in search mode")


def psrfits_datasize(hdu):
    '''
    Calculate data size
    '''
    nbit = get_nbit(hdu)
    nchan = get_nchan(hdu)
    npol = get_npol(hdu)
    nsubint = get_nsubint(hdu)
    nsampsubint = get_nsampsubint(hdu)
    datasize = nchan*npol*nsubint*nsampsubint*nbit/8
    columns = output_columns(hdu,re=True)
    ncol = len(columns)
    for icol in range(1,ncol):
        iTFORM =hdu[1].header['TFORM'+str(icol)]
        if 'E' in iTFORM:
            datasize += int(int(iTFORM.split("E")[0])*32/8*nsubint)
        elif 'D' in iTFORM:
            datasize += int(int(iTFORM.split("D")[0])*64/8*nsubint)
    #print(type(hdu[1].header))
    #print(len(hdu[1].header))
    #nDAT_SCL = hdu[1].header['TFORM15']
    #print(nDAT_SCL)
    #print(hdu[1].size)
    return int(datasize)
    
    
def psrfits_headersize(hdu):
    '''
    Calculate header size
    '''
    ## header 所包含的字符数量
    #headerpri_size = len(hdu[0].header.tostring())
    #headersub_size = len(hdu[1].header.tostring())
    ## get header
    header_pri = output_header(hdu,pri=True)
    header_sub = output_header(hdu,sub=True)
    ##the number of cards in header
    ncard =  len(header_pri)+len(header_sub)
    return ncard*80
        
def get_filename(arg):
    '''
    get the input file name
    '''
    
    for iarg in arg:
        try:
            suffix = iarg.split('.')[-1]
            if suffix == "fits" or suffix == "sf" or suffix == "fil":
                return iarg
                break
        except:
           pass
            
    print("\n")
    print("-"*10)
    print("\n")
    print("Please Check whether the input file is psrfits \n")
    print("-"*10)
    Usage()
    print("\n")
    return False


if __name__ == '__main__':
    arg = sys.argv
    # 打开一个PSRFITS文件
    filename = get_filename(arg)
    if filename != False:
        print("\n")
        print("-"*10,"the result","-"*10)
        print("\n")
        print(filename)
        hdu = fits.open(filename)
        if "-h" in arg:
            Usage()
        if "-header" in arg:
            output_header(hdu)
        if "-col" in arg:
            output_columns(hdu)
        if "-datasize" in arg:
            datasize = psrfits_datasize(hdu)
            print(f'The total data size of {filename} is {datasize} bytes.')
        if "-headersize" in arg:
            #print(psrfits_headersize(hdu))
            file_size = os.path.getsize(filename)
            headersize = file_size - psrfits_datasize(hdu)
            print(f'The total header size of {filename} is {headersize} bytes.')
        print("\n")
        print("-"*22,"End...","-"*22)
        print("\n")
        hdu.close()
        
