## Implementing Readers-Writers Problem using semaphores
----------------------------------------------------------------------------

1. Open the directory Assn5-CS20BTECH11037.zip and then extract the Assn5-CS20BTECH11037.zip file to your current directory

2. After that open extracted(Assn5-CS20BTECH11037) directory, now open terminal in that directory

3. Create a file "inp-params.txt". Give the input in following format :

    nw nr kw kr Mu_CS Mu_Rem

    where  nw     : Number of Writer threads 
           nr     : Number of Reader threads 
           kw     : frequency of each Writer thread
           kr     : frequency of each Reader thread
           Mu_CS  : Average of exponential distribution for critical section in milliseconds
           Mu_Rem : Average of exponential distribution for remainder section in milliseconds
    
    Eg:
    10 10 10 10 10 10


4. Compile the source code files as follows :

    g++ Assn5-rw-CS20BTECH11037.cpp -o rw -pthread
    g++ Assn5-frw-CS20BTECH11037.cpp -o frw -pthread

5. Run the generated binaries as follows : 

    ./rw
    ./frw

6. Check "RW-log.txt" for log corresponding to Reader preference algorithm

7. Check "FairRW-log.txt" for log corresponding to Fair algorithm

8. Check "Average_time.txt" for Average time of a thread to entry to CS for both the algorithms

----------------------------------------------------------------------------