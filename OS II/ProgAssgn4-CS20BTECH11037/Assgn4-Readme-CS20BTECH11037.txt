## Implementing TAS, CAS and Bounded Waiting CAS Mutual Exclusion Algorithms
----------------------------------------------------------------------------

1. Open the directory ProgAssgn4-CS20BTECH11037.zip and then extract the ProgAssgn4-CS20BTECH11037.zip file to your current directory

2. After that open extracted(ProgAssgn4-CS20BTECH11037) directory, now open terminal in that directory

3. Create a file "inp-params.txt". Give the input in following format :

    N K L1 L2

    where  N : number of threads
           K : frequency of each thread
           L1 : Average of exponential distribution for critical section
           L2 : Average of exponential distribution for remainder section
    
    Eg:
    10 10 5 20


4. Compile the source code files as follows :

    g++ SrcAssgn4-tas-CS20BTECH11037.cpp -o tas -pthread
    g++ SrcAssgn4-cas-CS20BTECH11037.cpp -o cas -pthread
    g++ SrcAssgn4-cas-bounded-CS20BTECH11037.cpp -o cas-bounded -pthread

5. Run the generated binaries as follows : 

    ./tas
    ./cas
    ./cas-bounded

6. Check "TAS_ME_Output.txt" for log corresponding to TAS

5. Check "CAS_ME_Output.txt" for log corresponding to CAS

6. Check "CAS_Bounded_ME_Output.txt" for log corresponding to CAS Bounded.

----------------------------------------------------------------------------