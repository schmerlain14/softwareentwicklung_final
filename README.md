# Final project for "Weiterführende Softwareentwicklung"

### Members: Hrönn Kjartansdottir, Katja Rüdiger, Natalie Schmerlaib

## Project Name: softwareentwicklung_final

## Structure
Overall information about the task is provided in *04-exercise-final-challenge.html* and the *README.md* provides this what can be read here.

### Data
Is downloaded automatically when executing run.sh and stored in a folder called eggnog_data-

### Scripts
The project provides 3 scripts, one bash script and two python scripts.

The bash script is called *run.sh* and is the one that needs to be used for producing everything. It is only necessary to call this one because it executes the other two.

The two python scripts *annotate_cogs.py* and *read_members_file.py* have methods and functions to create everything that is done in this project. The *read_members_file.py* script does the parsing of the eggnog_data_members files, selects the OGs matching the pre-defined values and processes the data from the members files. It outputs a list of all matching OGs. The *annotate_cogs.py* script distinguishes the OGs by different functional categories and counts the amount of OGs for each category. It outputs an overview of the occuring categories and the number of occurence.

### Results

In the *results* folder all the result datafiles are stored and can be examined, they are all txt files.


## To Do's

The project was done with Python 3.7.9, so please make sure to use this version.

1. First apply in bash chmod +x to all scripts, if they are not already executable, so that they can be run and used.
2. Then execute the run.sh script (with ./run.sh)


## Answers to questions

1. Which genes are universally required for an organism to survive? More precisely: Which genes (OGs) occur in at least 99% of all genomes in the eggNOG5 database in each domain of life, respectively? (The results should be around 100-300.)

   A. How many such genes did you identify in each domain? [2 points]
       
       Bacteria: 123
       
       Archaea: 175
       
       Eukaryota: 273
   
   
   B. Provide the results as three files (one for each domain), listing the OGs in sorted order (by name). [3 points]
       
       The files are stored in the *results* folder and are called *cogs_DOMAIN_o99.txt*
       


2. Which common bacterial genes occur almost exclusively as single-copy genes? More precisely: Which OGs occur in at least 50% of all bacterial genomes, and in at least 99% thereof as single-copy?

   A. Provide the results as a sorted text file. [3 points]
       
       Here there are 73 and the file is in the *results* folder and is called *cogs_bacteria_o50_u99.txt*
       
   B. How many of these OGs were also identified as universal bacterial OGs (previous question)? [2 points]
   
       The comparison of those two now for bacteria produced files results in the file *cogs_bacteria_o50_u99_universal_OG.txt* in the *results* folder and there were 40 found.



3. Identify all OGs that occur as single-copy in at least 97% of all Archaea.

    A. How many such OGs did you identify? Provide the result as a sorted text file. [2 points]
        
        This result is stored in the file *cogs-arachea_os97.txt* and it hast 121 entries.
    
    B.It would be interesting to know if there are archaeal genomes which substantially deviate from this "default" archaeal gene set. Are there Archaea which lack 4 or more of these universal OGs? Which organism (scientific name) lacks most? [3 points] What is its preferred growing temperature/environment? [0.5 bonus points]
    
         There are 6 Archaea whick lack 4 or more of these universal OGs.
         
         The one which lacks the most OGs (7 OGs) is Pyrococcus horikoshii OT-3, an anaerobe, hyperthermophilic archaeon that was isolated from marine hydrothermal vent at 1395 m depth. The preferred growth conditions are anaerob with a temperature of 95 °C (https://bacdive.dsmz.de/strain/16857)
        


4. Compile an overview of the functional categories of these 121 archaeal OGs.

    A. Provide the result as a text file sorted by the number of the functional categories. [5 points]
        
        This file is also stored in the *results* folder and its name is *cogs_arachaea_os97_functional_categories.txt* it contains the 12 categories that occured,
        ordered by the number of occurence.


___________________________________________________________________________________________________________

## ASCII mirror cat

1. Write a function that creates a mirror image of the ASCII cat. The output should be the same cat looking to the other side. Start with creating a mirror image of cat1. When this works, modify your code so that it also works for cat2. You can use the provided template. [2 bonus points]

         The file *ascii_cat.ipynb* contains a functioning python script that mirrors the ASCII image of a cat.


