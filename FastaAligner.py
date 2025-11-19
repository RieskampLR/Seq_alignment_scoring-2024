#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
FastaAligner.py

Description:
This program scores sequence alignments from a fasta file.
For each sequence comparison it returns:
- Sequence IDs
- Identity score (total number and %)
- Gap score (total number and %)
- Alignment score
Gaps in the alignment must be indicated by a "-".
If both sequences have a gap in the same position the base pair is not considered in the scoring.
The parameters and their defaults for the scorings are:
- gap = -1           : Penalty score applied for every gap in the alignment
- identity = +1      : Score applied for every match
- transition = -1    : Penalty score applied for transitions
- transversion = -2  : Penalty score applied for transversion
Parameters can be changed by providing a txt file,
where parameters are assigned as in the following example: gap = -1
The assinged values may be negative, 0, or positive; floating-point numbers or integers.
Values cannot be in string format.
The parameters file may contain comments if indicated by a "#", which will not be considered by the program.
All parameters not assigned in the provided file are set to their default value.
Results can be stored (in text format) by providing an output file name.

User-defined functions: alignment_scores(), description in the docstring of the function
Non-standard modules: None

Procedure:
    1. Defining a function that scores the alignment of two sequences.
    2. Input checks
        1.1 Number of command line arguments
        1.2 Existence of files
        1.3 Size of files
        1.4 File type by name format
    3. Iteration over the fasta file to create a dictionary of the sequences
       using the sequence IDs as keys.
       Fasta file check by content characteristics during the iteration.
    4. Creating a list of the ID´s from the dictionary.
    5. Parameter file content check.
       Setting the parameters for the alignments.
    6. Sequence comparisons using the previously defined function and parameters.
       Printing the resulting scores to the screen and (if given) to the output file.

Input: fasta file , parameters txt file (optional), name of output file (optional)
Output: print to screen, output file (optional)

Usage: FastaAligner.py yourfastafile.fna yourparametersfile.txt youroutputfile.txt

Version: 1.00
Date: 2024-10-21
Author: Lea Rachel Rieskamp

"""


# Imports:

import sys
import re
import os
from pathlib import Path



# Function to score alignments:
  # input: Two aligned sequences, parameters (gap,identity,transition,transversion)
  # output: List containing the sequence length, identity score, identity score in %,
  #         gap score, gap score in %, and alignment score

def alignment_scores(seq,otherseq,gap,identity,transition,transversion) -> list:
    """
    Parameters
    ----------
    seq : str
        Query sequence.
    otherseq : str
        Aligned sequence to compare to query.
    gap : float or int
        Penalty score for gaps.
    identity : float or int
        Score to add for matching base pairs.
    transition : float or int
        Score for transitions.
    transversion : float or int
        Score for transversions.

    Returns
    -------
    list
        [seqlength, identityscore, identitypercent, gapscore, gapspercent, score]
        seqlength: int
            Sequence length in total count of bases.
        identityscore: float or int
            Count of matches
        identitypercent: float or int
            Percentage of matches.
        gapscore: float or int
            Count of gaps.
        gapspercent: float or int
            Percentage of gaps.
        score: float or int
            Overall alignment score.
    """
    identityscore = 0
    gapscore = 0
    score = 0
    doublegap = 0
    # Iterating over base pairs of the sequences stored in seq and otherseq
    for base,otherbase in zip(seq,otherseq):
        if base == "-" and otherbase == "-" :
            doublegap += 1
            continue
        elif base == "-" or otherbase == "-" : # For gaps
            score = score + gap 
            gapscore += 1
        elif base == otherbase:              # For matches
            score = score + identity
            identityscore += 1
        elif (base,otherbase) in {("A","G"),("G","A"),("C","T"),("T","C"),("C","U"),("U","C")}: # For transitions
            score = score + transition
        else:                                # For all other substitutions (transversions)
            score = score + transversion
    # Calculating percentages
    seqlength = len(seq)-doublegap
    identitypercent = round(identityscore/seqlength*100,1)
    gapspercent = round(gapscore/seqlength*100,1)
    # Conversion to integers for whole numbers
    if identitypercent.is_integer():
        identitypercent = int(identitypercent)
    if gapspercent.is_integer():
        gapspercent = int(gapspercent)
    if score.is_integer():
        score = int(score)
    # Results are returned in form of a list
    return [seqlength,identityscore,identitypercent,gapscore,gapspercent,score]



# Input file check - number of arguments:

if len(sys.argv) not in range(2,5):
    print("Incorrect number of command line arguments.\nTry: python FastaAligner.py yourfastafile yourparametersfile youroutputfile.\nParametersfile and outputfile are optional.\nProgram terminated.")
    exit()



# Storing Paths of arguments in variables:
# If optional arguments are not given, their variables are assigned to 0
    
fastafile_unopened = Path(sys.argv[1])
parameters_unopened = 0
outputfile_unopened = 0
for arg in sys.argv[2:]:
    if "parameter" in arg.lower():
        parameters_unopened = Path(arg)
    elif "output" in arg.lower():
        outputfile_unopened = Path(arg)



# Input file check - existence:

if not fastafile_unopened.is_file():
    print(f"{fastafile_unopened} not found.\nProgram terminated.")
    exit()

if parameters_unopened != 0:
    if not parameters_unopened.is_file():
        response_parameters = input(f"{parameters_unopened} not found.\nDo you want to continue with default parameters (gap=-1,identity=+1,transition=-1,transversion=-2)?\nAnswer with y (yes) or n (no) and press enter\n")
        if not response_parameters:
            response_parameters = "n"
        if response_parameters.lower()[0] == "n":
            print("Program terminated.")
            exit()
        else:
            print("Continuing with default parameters.")
            parameters_unopened = 0
            
if outputfile_unopened != 0:
    if outputfile_unopened.is_file():
        response_outputfile = input(f"{outputfile_unopened} already exists. Continue and overwrite existing file?\nAnswer with y (yes) or n (no) and press enter\n")
        if not response_outputfile:
            response_outputfile = "n"
        if response_outputfile.lower()[0] != "y":
            print("Program terminated.")
            exit()



# Input file check - size:
  # 1GB warning for fasta file
  # 2KB limit for parameters file

fnasize = os.path.getsize(fastafile_unopened)
if parameters_unopened != 0:
    parameterssize = os.path.getsize(parameters_unopened)
else:
    parameterssize = 0

bigfilesize = 1073741824
bigparameterfsize = 2048

if fnasize > bigfilesize:
    responsefsize = input(f"{fastafile_unopened} > 1GB.\nDo you want to continue with this file?\nAnswer with y (yes) or n (no) and press enter\n")
    if not response_outputfile:
        response_outputfile = "n"
    if responsefsize.lower()[0] == "n":
        print("Program terminated.")
        exit()

if parameterssize != 0:
    if parameterssize > bigparameterfsize:
        print(f"{parameters_unopened} is > 2KB. It should only contain the parameters you choose to change!\nIt has to be a text file.\nProgram terminated.")
        exit()



# Input file check - file type by name format:

if not str(fastafile_unopened).endswith((".fna",".fasta",".fa")):
    if str(fastafile_unopened).endswith(".fastq"):
        print("You provided a FASTQ file. Please provide a FASTA file instead.\nProgram terminated.")
        exit()
    print(f"{fastafile_unopened} is not a FASTA file. File has to end on .fna, .fasta, or .fa.\nCheck if file is compressed.\nProgram terminated.")
    exit()
    
if outputfile_unopened != 0:
    if not str(parameters_unopened).endswith(".txt"):
        print(f"{parameters_unopened} is not a text file. File has to end on .txt.\nCheck if file is compressed.\nProgram terminated.")
        exit()



# Dictionary of IDs (keys) with sequences (items) from fasta file
# Input file check - fasta file content:
  # has to start with ">"
  # can only contain headers starting on ">" &
  # sequences containing nucleobase abbreviations (A,C,G,T,U) and gap indicators (-)
  # cannot contain a mix of DNA and RNA sequences
  
header_seq_dictionary = {}
fheader = ""
fsequence = ""
dna = 0
rna = 0
with open(fastafile_unopened,"r") as fastafile:
    for fline in fastafile:
        # Extracting the headers
        if fline.startswith(">"):
            fsequence = ""
            fheader = fline.lstrip(">").strip()
        # Extracting the sequences
        elif re.fullmatch("[-AGCTU]+", fline.upper().strip()):
            fsequence += fline.upper().strip()
            # Identifying DNA and RNA
            if "T" in fsequence:
                dna = True
            if "U" in fsequence:
                rna = True
            if dna and rna != 0:
                print("Fasta file cannot contain DNA and RNA sequences.\nPlease choose a file with either DNA or RNA sequences.\nProgram terminated.")
                exit()
            # Adding header:sequence to dictionary
            # If sequence over several lines, entry is overwritten with the final, whole sequence
            header_seq_dictionary[fheader] = fsequence
        else:
            print(f"{fastafile_unopened} is not a FASTA file.\nFile can only contain headers starting with '>' and sequences containing bases (A,C,G,T,U) and gap indicators (-).\nProgram terminated.")
            exit()



# List of sequence IDs from fasta file:

seqidslist = list(header_seq_dictionary.keys())



# Setting scoring parameters from parameter file
# Input file check - parameters file content:
  # identifying parameters given
  # parameters have to be assigned to a number
# Assigning remaining parameters to defaults

if parameters_unopened:
    with open(parameters_unopened,"r") as parameterfile:
       for pline in parameterfile:
           try:
               # Searching for the pattern "parameter = value"
               if "gap" in pline or "identity" in pline or "transition" in pline or "transversion" in pline:
                   assignment = re.match(r"(\w+)\s*=\s*(-?\d+\.?\d*)",pline)
                   if assignment:
                       # Extracting parameter name and value & executing the assignment
                       parameter = assignment.group(1)
                       value = assignment.group(2)
                       globals()[parameter] = float(value)
                   else:
                       print(f"Variables in {parameters_unopened} have to be assigned to a number.\nVariable has to be on the left of the equal sign.\nProgram terminated.")
                       exit()
           except Exception:
               print(f"{parameters_unopened} has the wrong format.\nIt should only contain the parameters you choose to change! It may contain comment lines indicated by #.\nVariables have to be assigned to a number.\nProgram terminated.")
               exit()

try:
    gap
except NameError:
    gap = -1
try:
    identity
except NameError:
    identity = 1
try:
    transition
except NameError:
    transition = -1
try:
    transversion
except NameError:
    transversion = -2



# Clearing output file content in case file already exists:
    
if outputfile_unopened != 0:
    with open(outputfile_unopened,"w") as outputfile:
        outputfile.write("")



# Writing scoring results to screen and output file:
  # 1. Loops through IDs list
  # 2. Finds corresponding sequence in dictionary
  # 3. For each loop, loops again through ID list starting one index after the current loop´s ID,
  #    to compare each sequence to the remaining ones (sequences again taken from dictionary)
  # 4. Sequences are compared using the alignment scoring function
  # 5. Result is formatted and printed to the screen and output file (if given) after every loop

for seqid in seqidslist:
    queryseq = header_seq_dictionary[seqid]
    qseqidindex = seqidslist.index(seqid)
    for alignedseqid in seqidslist[qseqidindex+1:]:
        alignedseq = header_seq_dictionary[alignedseqid]
        scoringslist = alignment_scores(queryseq,alignedseq,gap,identity,transition,transversion)
        scorings = f"{seqid.capitalize()}-{alignedseqid}: Identity: {scoringslist[1]}/{scoringslist[0]} ({scoringslist[2]}%), Gaps: {scoringslist[3]}/{scoringslist[0]} ({scoringslist[4]}%), Score={scoringslist[5]}\n"
        print(scorings)
        if outputfile_unopened:
            with open(outputfile_unopened,"a") as outputfile:
                outputfile.write(scorings)
        




