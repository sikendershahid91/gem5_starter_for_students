#!/usr/bin/env bash
#
# This is a run script for
#      x1. setting up gem5
#      x2. setting up architecture
#      3. kicking of cache creation
#      4. running simulation using python script
#      5. reading the statistics of the simulation 
#
#

_file=${0##*/}
error(){ echo "$_file: $@" ; exit 1 ; }

usage=\
"Usage: ./run_script.sh [option]=[type of option] 
	
	-a or --architecture  : ARM X86
	-c or --core          : number of cores
	-cp or --config-path  : path to configuration file 


	example:

	./run_script.sh -a=ARM
	./run_script.sh -a=ARM -c=4 
	./run_script.sh -a=ARM -c=4 -cp=run.config
	./run_script.sh -a=ARM -c=2 -cp=/path-to-file/
"

check_build(){
    #
    # This executable that is created is needed to run
    # python, source, and simulation
    #
    if ! [ -e gem5/build/$architecture/gem5.opt ] ; then
	echo "$_file: Build doesnt exist: Creating build executable ..."
	scons build/$architecture/gem5.opt -j$core || \
	    error "Building executable failed: View error above"
    fi
}

create_single_core_environment(){
    #
    # Creating a single core python configuration script
    # that is used by gem5 
    # uses configuration file 
    #
    cp run_single_core.py gem5/configs/run_single_core.py 
    if ! [ -e $config_path ] ; then error "Configuration file not found !" ; fi    
}

# create_double_core_environment(){
#     #// future work
#     #//  cache coherence
#     #//  l3 capabilities
#     #//  modification of policies
# }

run_build(){
    #
    #
    #
    gem5/build/$architecture/gem5.opt gem5/configs/run_single_core.py run.config |& tee run.log 
}

create_data(){
    #
    # Creating the location to view the data from sim
    #
    if ! [ -d gem5/m5out ] ; then error "output hasnt generated" ; fi
    local data_dir="DATA_RESULT_$(date '+%Y%m%d%H%M%S')"
    mkdir $data_dir 
    cp gem5/m5out/* $data_dir/.
    cp run.log $data_dir/.
}


#default parameters
architecture='X86'
core=2
config_path="run.config"

if [ $# -eq 0 ] ; then error "$usage" ; fi  
for argument in "$@"
do
    case $argument in
	-a=*|--architecture=*)
	    architecture="${argument#*=}"
	    shift ;;
	-c=*|--core=*)
	    core="${argument#*=}"
	    if ! [[ $core =~ ^[0-9]+$ ]] ; then
		echo "$usage" ; error "Invalid numerical value : $argument"
	    fi
	    shift ;;
	-cp=*|--config-path=*)
	    config_path="${argument#*=}"
	    if ! [ -e $config_path ] ; then
		echo "$usage" ; error "Invalid path location : $argument"
	    fi
	    shift ;; 
	*)
	    echo "$usage" ; error "Invalid arguments : $argument "
	    shift ;;
    esac
done

echo "$architecture"  
echo "$core"
echo "$config_path"

check_build
create_single_core_environment
run_build
create_data
