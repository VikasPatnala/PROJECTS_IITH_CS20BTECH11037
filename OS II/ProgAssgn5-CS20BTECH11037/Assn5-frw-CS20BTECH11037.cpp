#include <iostream>
#include <string>
#include <atomic>
#include <random>
#include <thread>
#include <ctime>
#include <chrono>
#include <sys/time.h>
#include <semaphore.h>
#include <unistd.h>
#include <pthread.h>
#include <fstream>

using namespace std;
using std::chrono::duration_cast;
using std::chrono::milliseconds;
using std::chrono::microseconds;
using std::chrono::seconds;
using std::chrono::system_clock;

/****************************** Global Variables ********************************/

#define TK 1000000
#define THS 1000

/*********** Input file variables *********/
int nw, nr;           // Number of reader and writer threads
int kw, kr;           // frecuency of number of times reader and writer thread enter CS
double Mu_CS, Mu_Rem; // average exponential distribute of delay times randCSTime, randREMTime

/*********** File stream variables **********/
ifstream in_file("inp-params.txt");
FILE *out_file = fopen("FairRW-log.txt", "w");
ofstream avg_out("Average_time.txt", ios::app);

/*********** Time variables *********************/
time_t readers_waiting_time;
time_t writers_waiting_time;
time_t readers_worst_case_waiting_time;
time_t writers_worst_case_waiting_time;

default_random_engine generator1, generator2;
exponential_distribution<double> randCSTime;
exponential_distribution<double> randRemTime;

/****************** SEMAPHORES *******************/

sem_t rw_mutex;
sem_t mutex;
sem_t queue;
int read_count = 0;

/*******************************************************************************/

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
void *writer(void *params);
void *reader(void *params);

int main()
{
    // Taking the file input
    if (in_file.is_open())
    {
        in_file >> nw >> nr >> kw >> kr >> Mu_CS >> Mu_Rem;
    }
    else
    {
        // If unable to open file output error message and terminate
        cout << "Unable to open file 'inp-params.txt'\n";
        return 0;
    }

    randCSTime = exponential_distribution<double>(1.0 / (Mu_CS));
    randRemTime = exponential_distribution<double>(1.0 / (Mu_Rem));

    // semaphores initialization
    sem_init(&rw_mutex, 0, 1);
    sem_init(&mutex, 0, 1);
    sem_init(&queue, 0, 1);

    // delcaring n threads
    pthread_t writers[nw];
    pthread_t readers[nr];

    // creating nw writer threads and passing parameter id to each thread and the value of id is (i + 1)
    for (int i = 0; i < nw; ++i)
    {
        int *id = new int;
        *id = i + 1;
        pthread_create(&writers[i], NULL, writer, (void *)(id));
    }

    // creating nr reader threads and passing parameter id to each thread and the value of id is (i + 1)
    for (int i = 0; i < nr; ++i)
    {
        int *id = new int;
        *id = i + 1;
        pthread_create(&readers[i], NULL, reader, (void *)(id));
    }

    // calling each thread of writers to join after their completion of execution
    for (int i = 0; i < nw; ++i)
    {
        pthread_join(writers[i], NULL);
    }

    // calling each thread of readers to join after their completion of execution
    for (int i = 0; i < nr; ++i)
    {
        pthread_join(readers[i], NULL);
    }

    // calling each thread to join after their completion of execution
    avg_out << "Average Waiting Time of frw : " << (double)(writers_waiting_time + readers_waiting_time) / ((nw * kw + nr * kr) * THS) << " milliseconds\n";
    avg_out << "Average Waiting Time frw writers : " << (double)(writers_waiting_time) / (nw * kw * THS) << " milliseconds\n";
    avg_out << "Average Waiting Time frw readers : " << (double)(readers_waiting_time) / (nr * kr * THS) << " milliseconds\n";
    // cout << "Worst case running Time of writers : " << (double)writers_worst_case_waiting_time / THS << " milliseconds\n";
    // cout << "Worst case running Time of readers : " << (double)readers_worst_case_waiting_time / THS << " milliseconds\n";
}

void *writer(void *params)
{
    // restoring the value of id which is sent by the main thread to each thread and storing in id variable
    int *id = (int *)params;

    for (int i = 1; i <= kw; ++i)
    {
        time_t reqTime = duration_cast<microseconds>(system_clock::now().time_since_epoch()).count();
        fprintf(out_file, "%dth CS request by Writer Thread %d at %s\n", i, *id, getSysTime(reqTime/TK).c_str());

        /************ ENTRY SECTION ********************/
        // the first thread which run this while loop
        // will enter the CS first and lock the CS
        // so that next thread will only be able to come to CS
        // after clearing of first threads lock
        sem_wait(&queue);
        sem_wait(&rw_mutex);
        sem_post(&queue);

        /************ CRITICAL SECTION *****************/
        time_t enterTime = duration_cast<microseconds>(system_clock::now().time_since_epoch()).count();
        writers_waiting_time += enterTime - reqTime;
        writers_worst_case_waiting_time = max(writers_worst_case_waiting_time, enterTime - reqTime);

        fprintf(out_file, "%dth CS Entry by Writer Thread %d at %s\n", i, *id, getSysTime(enterTime/TK).c_str());
        usleep(randCSTime(generator1) * THS); // sleeping in the CS

        /************ EXIT SECTION *********************/
        time_t exitTime = duration_cast<microseconds>(system_clock::now().time_since_epoch()).count();
        fprintf(out_file, "%dth CS Exit by Writer Thread %d at %s\n", i, *id, getSysTime(exitTime/TK).c_str());

        // clearing the lock in the sense we are releasin the lock for other threads
        // to enter the CS hence progress is satisfied
        sem_post(&rw_mutex);

        /*********** REMAINDER SECTION *****************/
        usleep(randRemTime(generator2) * THS); // sleeping in the REMAINDER SECTION
    }
    return NULL;
}

void *reader(void *params)
{
    // restoring the value of id which is sent by the main thread to each thread and storing in id variable
    int *id = (int *)params;

    for (int i = 1; i <= kr; ++i)
    {
        time_t reqTime = duration_cast<microseconds>(system_clock::now().time_since_epoch()).count();
        fprintf(out_file, "%dth CS request by Reader Thread %d at %s\n", i, *id, getSysTime(reqTime/TK).c_str());

        /************ ENTRY SECTION ********************/
        // every entering thread will increment the read_count variable
        // using the semaphore rw_mutex and checking if there is any writer
        // is there in the critical section if there then we will wait until it releases
        // and here for achieving fairness we will use semaphore queue
        sem_wait(&queue);
        sem_wait(&mutex);
        read_count++;
        if (read_count == 1)
        {
            sem_wait(&rw_mutex);
        }
        sem_post(&queue);
        sem_post(&mutex);

        /************ READING *****************/
        time_t enterTime = duration_cast<microseconds>(system_clock::now().time_since_epoch()).count();
        readers_waiting_time += enterTime - reqTime;
        readers_worst_case_waiting_time = max(readers_worst_case_waiting_time, enterTime - reqTime);

        fprintf(out_file, "%dth CS Entry by Reader Thread %d at %s\n", i, *id, getSysTime(enterTime/TK).c_str());
        usleep(randCSTime(generator1) * THS); // sleeping in the CS

        /************ EXIT SECTION *********************/
        time_t exitTime = duration_cast<microseconds>(system_clock::now().time_since_epoch()).count();
        fprintf(out_file, "%dth CS Exit by Reader Thread %d at %s\n", i, *id, getSysTime(exitTime/TK).c_str());

        // here when a reader finishes its reading then we will decrement
        // the variable read_count and we will check if any other reader thread is waiting
        // for CS if it waits then we will just go other wise we will signal the writer
        sem_wait(&mutex);
        read_count--;
        if (read_count == 0)
        {
            sem_post(&rw_mutex);
        }
        sem_post(&mutex);

        /*********** REMAINDER SECTION *****************/
        usleep(randRemTime(generator2) * THS); // sleeping in the REMAINDER SECTION
    }
    return NULL;
}
