# gem5 Starter

gem5 is a computer-system simulator. Useful for microarchitecture-level research. User can modify system-level architecture and process their executable to observe performance. gem5 offers key features that makes it standout from other open source projects. more information on gem5 can be found at their site: www.gem5.org/Main_Page


Key Features
-------------------------------
- ISA: alpha, arm, SPARC, x86
- trace-based CPU
- event-driven memory system


The goal of these scripts are the following.
-------------------------------
- Aid installation for debian environment.
- easily configure l1 l2 cache-memory levels.
- run different configuration templates
- easily extract micro-architecture level statistics for your source code depending on the architecture



Use these starter scripts to collect varying performance of l1 and l2 cache designs:
-------------------------------
- compile and note path of your executable in **run.config**. e.g. helloworld program

- edit the parameters in **run.config**
- run the **run_single_core.sh** script. for a desired ISA's first build, this script will run through the gem5 initial build process. The running your configuration files it will create a data directory. The data directory is name DATA_RESULT_YEARMONTHDATEHOURMINUTESECOND. In this folder locate the statistics textfile. This file will contain performance data for running your code with configurations specified, and the ISA used.



for easy out of the box use, use these scripts to help you acquire
data
-------------------------------
To install gem5, run the script

```
sudo bash install.sh or sudo ./install
```

After installation gem5 directory will appear.

### observe the configuration file **run.config**.

In run.config, you can modify l1, l2, and the location of the executable to be processed. You can create as many configurations files you need. The configuration files need to contain the same parameters. These parameters are used in the following python script discussed. 

observe the python script **run_single_core.py**

This script parses the configuration file above. creates the cache models based on the parameters in the configuration file.

observe the run script **run_single_core.sh**

This script is used as a command line tool to build ISA and run different configurations.

Run script to see usage

```
./run_single_core.sh 
```

Things to be done to extend starter files
-------------------------------
- create l3 configurable memory block
- utilize different DRAM controller models
- extend to more cores than single core
- use cache coherence with more than single core memory structure 





