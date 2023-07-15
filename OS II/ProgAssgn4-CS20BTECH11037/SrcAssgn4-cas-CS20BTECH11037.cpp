#include <iostream>
#include <string>
#include <atomic>
#include <random>
#include <ctime>
#include <unistd.h>
#include <pthread.h>
#include <fstream>

using namespace std;

/****************************** Global Variables ********************************/

/*********** Input file variables *********/
int n;                     // number of threads
int k;                     // frequency of each thread
double Lambda_1, Lambda_2; // average exponential distribute of delay times t_1, t_2

/*********** File stream variables **********/
ifstream in_file("inp-params.txt");
FILE *out_file = fopen("CAS_ME_Output.txt", "w");

/*********** Time variables *********************/
time_t waiting_time;
time_t worst_case_waiting_time;

/*******************************************************************************/

atomic<int> lock(0); // atomic int lock is used for locking the Critical Section

/**
 * @brief Get the Sys Time object This function will return the current time in the form of string
 *          so that the caller function can easily output to the output stream file
 * @param time_t t
 * @return string (which is a formated)
 */
string getSysTime(time_t t)
{
    tm *Time = localtime(&t);
    string TIME = "";
    TIME = to_string(Time->tm_hour) + ":" + to_string(Time->tm_min);
    return TIME;
}

/**
 * @brief The function testCS is a function which is called by each thread and each thread will run
 *          this function k times.
 * @param void* params
 * @return void*
 */
void *testCS(void *params);

int main()
{
    // Taking the file input
    if (in_file.is_open())
    {
        in_file >> n >> k >> Lambda_1 >> Lambda_2;
        fprintf(out_file, "CAS ME Output:\n");
    }
    else
    {
        // If unable to open file output error message and terminate
        cout << "Unable to open file 'inp-params.txt'\n";
        return 0;
    }

    // delcaring n threads
    pthread_t threads[n];

    // creating n threads and passing parameter id to each thread and the value of id is (i + 1)
    for (int i = 0; i < n; ++i)
    {
        int *id = new int;
        *id = i + 1;
        pthread_create(&threads[i], NULL, testCS, (void *)(id));
    }

    // calling each thread to join after their completion of execution
    for (int i = 0; i < n; ++i)
    {
        pthread_join(threads[i], NULL);
    }

    // Neccessary values of average waiting time of each process and worst case running time
    // cout << "Average Waiting Time : " << (double)(waiting_time) / (n * k) << "\n";
    // cout << "Worst case running Time : " << worst_case_waiting_time << "\n";
}

void *testCS(void *params)
{
    // restoring the value of id which is sent by the main thread to each thread and storing in id variable
    int *id = (int *)params;

    // these variables are used to find the value of t1 and t2 with the given
    // value of Lambda of exponential distribution
    // As mean of a exponential distribution is inverse of Lambda we are keep here 1/Lambda_1
    default_random_engine generator;
    exponential_distribution<double> t1(1.0 / Lambda_1);
    exponential_distribution<double> t2(1.0 / Lambda_2);

    // These values are required to get the Lock using CAS atomic operation
    int expected = 0, new_value = 1;

    for (int i = 1; i <= k; ++i)
    {
        time_t reqEnterTime = time(NULL);
        fprintf(out_file, "%dth CS Request at %s by thread %d\n", i, getSysTime(reqEnterTime).c_str(), *id);

        /************************* ENTRY SECTION ************************/
        // As the first thread has value of lock to 0 amd expected value to 0
        // it will set the lock to 1 and then go out of this loop
        // Hence we will acheive the mutual exclusion requirement

        while (lock.compare_exchange_strong(expected, new_value) == 0)
        {
            expected = 0;
            new_value = 1;
        }

        /************************* CRITICAL SECTION ************************/
        time_t actEnterTime = time(NULL);
        waiting_time += actEnterTime - reqEnterTime;
        worst_case_waiting_time = max(worst_case_waiting_time, actEnterTime - reqEnterTime);

        fprintf(out_file, "%dth CS Entry at %s by thread %d\n", i, getSysTime(actEnterTime).c_str(), *id);
        usleep(t1(generator) * 1e6); // sleeping in the CS

        /************************* EXIT SECTION ************************/
        time_t exitTime = time(NULL);
        fprintf(out_file, "%dth CS Exit at %s by thread %d\n", i, getSysTime(exitTime).c_str(), *id);

        // again releasing the lock in other words changing the value of lock
        // to 0 hence allowing the other threads to enter the CS hence progress is
        // satisfied
        lock = 0;

        /************************* REMAINDER SECTION ************************/
        usleep(t2(generator) * 1e6); // sleeping in the REMAINDER SECTION
    }
    return NULL;
}
