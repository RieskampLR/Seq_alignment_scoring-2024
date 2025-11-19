#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
FastaAlignerDriver.py

Description:
This program tests the FastaAlignerDriver program for different command line argument inputs.
First part covers cases with user input y (yes).
Second part covers cases with user input n (no).

Procedure:
    1. Creating a list containing lists of different command line arguments
    2. Setting the additional user input to y (yes)
    3. Looping through the list, executing all cases, and returning the results to the screen
    4. Setting the additional user input to n (no)
    5. Looping through the list, executing all cases, and returning the results to the screen

Input: None
Output: Print to screen

Usage: FastaAlignerDriver.py

Version: 1.00
Date: 2024-10-21
Author: Lea Rachel Rieskamp

"""


import subprocess


# List of terminal command lists

commands = [["python","FastaAligner.py","input_fasta.fna","parameters.txt","output_fasta.txt"],     #1 Original files
            ["python","FastaAligner.py","input_fasta.fna","parameters.txt","output_notfound.txt"],  #2 Output file not found
            ["python","FastaAligner.py","input_fasta.fna","parameters.txt"],                        #3 No output file
            ["python","FastaAligner.py","input_fasta.fna","output_fasta.txt","parameters.txt"],     #4 Reversed order of parameters and output files
            ["python","FastaAligner.py","input_fasta.fna","parameters_notfound.txt"],               #5 Parameters file not found
            ["python","FastaAligner.py","input_fasta.fna"],                                         #6 No parameters file
            ["python","FastaAligner.py","input_fasta.fna","driver_parameters_differentformat.txt"], #7 Wrongly formatted parameters file           
            ["python","FastaAligner.py","input_fasta.fna","driver_parameters_empty.txt"],           #8 Empty parameters file
            ["python","FastaAligner.py","input_fasta.fna","driver_parameters_floats.txt"],          #9 Float parameters 
            ["python","FastaAligner.py","input_fasta.fna","driver_parameters_twoparametersonly.txt"], #10 Not all parameters assigned
            ["python","FastaAligner.py","input_fasta.fna","driver_parameters_withComment.txt"],     #11 Comments in parameters file
            ["python","FastaAligner.py","input_fasta.fna","driver_parameters_word.docx"],           #12 Wrong parameters file format
            ["python","FastaAligner.py"],                                                           #13 No fasta file
            ["python","FastaAligner.py","driver_fasta_notfound"],                                   #14 Fasta file not found
            ["python","FastaAligner.py","driver_fasta_fastq.fastq"]]                                #15 Fastq file provided



# Outputs if user input being y (yes)

user_input = "y"


for n, command in enumerate(commands):
    # Capturing output of commands
    result = subprocess.run(command, input=user_input, capture_output=True, text=True)
    # Printing output to screen
    print(f"Test (y) {n+1}: Output: {result.stdout}")
    # For cases raising a python Error
    if result.returncode != 0:
        print(f"Error: {result.stderr}")



# Outouts if user input is n (no)

user_input = "n"


for n, command in enumerate(commands):
    # Capturing output of commands
    result = subprocess.run(command, input=user_input, capture_output=True, text=True)
    # Printing output to screen
    print(f"Test (n) {n+1}: Output: {result.stdout}")
    # For cases raising a python Error
    if result.returncode != 0:
        print(f"Error: {result.stderr}")














