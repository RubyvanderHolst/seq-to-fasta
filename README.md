# seq-to-fasta

The goal of this repository is to convert multiple .seq files to a singular .fasta file. 
This manual is written for usage within the command line.
The description lines in the fasta file contain the base name of the seq file and the time the seq file was last edited. Example:<br>
<code>>basefilename|31-12-2021 23:59:59</code><br>

Besides the fasta file two other files are created: <code>added.txt</code> and <code>skipped.txt</code>. 
<code>added.txt</code> contains a list of all the files that are added to the fasta file. 
<code>skipped.txt</code> contains the files from the input directory which were not added to the fasta file. 

##Parameters
- <code>-i, --input</code> Path to input directory (default is current directory)
- <code>-p, --prefix</code> Prefix of the output fasta file (default is “new”)
- <code>-o, --output</code> Path to the output directory (default is current directory). The given directory can be created if it does not exist. This is only possible if the last directory in the path is nonexistent.
- <code>-h --help</code> Display the help text.

##Examples
If the script is run without parameters, the current directory is used as the input and output directory. 
The fasta file name will be “new.fasta”. <br>
The script is run as follows:
<code>python seq_to_fasta.py</code>

###Input
The user can specify the path to the input directory. This can be a relative path or an absolute path. The path can be given as a Unix path or a Windows path. 
Keep in mind that Windows paths use backslashes. This means the path has to be given with double backslashes.<br>
<code>python seq_to_fasta.py -i input_dir</code><br>
Unix path:<br>
<code>python seq_to_fasta.py -i /mnt/c/path/to/dir</code><br>
Windows path:<br>
<code>python seq_to_fasta.py -i C:\\path\\to\\dir</code><br>

###Output
The user can specify the output directory. The same rules apply as for the input directory path.<br>
<code>python seq_to_fasta.py -o output_dir</code><br>
Unix path:<br>
<code>python seq_to_fasta.py -o /mnt/c/path/to/dir</code><br>
Windows path:<br>
<code>python seq_to_fasta.py -o C:\\path\\to\\dir</code><br>
The script can create the output directory if it does not exist yet. 
This is only possible if the last directory in the path does not exist. 
For instance, in <code>/dir1/dir2/input_dir</code> only <code>input_dir</code> cannot exist for it to be created. 

###Prefix
The default name for the new fasta file is <code>new.fasta</code>. 
The user can choose to give this file another prefix. 
For instance, if you want to give the file the name <code>fungal_data.fasta</code>, it can be done as follows:<br>
<code>python seq_to_fasta.py -p fungal_data</code>
