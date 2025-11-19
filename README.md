README

Lea Rachel Rieskamp
21.10.2024
BINP16 course project - 2
(For complimentary Driver file info see bottom of page)

Program description:
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


Complimentary Driver file: FastaAlignerDriver.py

Driver description:
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



