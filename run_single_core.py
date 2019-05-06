#
# parsing configuration file 
#
import sys
if len(sys.argv) is not 2:
    print('Error config path not specified')
    exit(1)    


class Config:
    def __init__(self, config_file):
        print('Parsing configuration file')
        self.dictionary = dict()
        with open(config_file) as file:
            for line in file:
                if not line.startswith('#'):
                    data = line.partition('#')[0]\
                               .rstrip()\
                               .replace(' ','')\
                               .partition('=')
                    if len(data[0]) is not 0:
                        self.dictionary[data[0]] = data[2]
                        
config_data = Config(sys.argv[1])

#
# creating cache objects based on configuration file parameters
#
from m5.objects import Cache
class L1Cache(Cache):
    assoc            = config_data.dictionary['l1_assoc']
    tag_latency      = config_data.dictionary['l1_tag_latency']
    data_latency     = config_data.dictionary['l1_data_latency']
    response_latency = config_data.dictionary['l1_response_latency']
    mshrs            = config_data.dictionary['l1_mshrs']
    tgts_per_mshr    = config_data.dictionary['l1_tgts_per_mshr']
    
    def connectCPU(self, cpu):
        # need to define this in a base class!
        raise NotImplementedError

    def connectBus(self, bus):
        self.mem_side = bus.slave

class L2Cache(Cache):
    size             = config_data.dictionary['l2_total_size']
    assoc            = config_data.dictionary['l2_assoc']
    tag_latency      = config_data.dictionary['l2_tag_latency']
    data_latency     = config_data.dictionary['l2_data_latency']
    response_latency = config_data.dictionary['l2_response_latency']
    mshrs            = config_data.dictionary['l2_mshrs']
    tgts_per_mshr    = config_data.dictionary['l2_tgts_per_mshr']

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.master

    def connectMemSideBus(self, bus):
        self.mem_side = bus.slave 


class L1ICache(L1Cache):
    size = config_data.dictionary['l1_instruction_size'] 

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    size = config_data.dictionary['l1_data_size']
    
    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

#
# Creating system using the cache objects created and
#  based on configuration file
#
import m5
from m5.objects import *
system                  = System()
system.clk_domain       = SrcClockDomain()
system.clk_domain.clock = config_data.dictionary['system_clock']
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode         = config_data.dictionary['timing']
system.mem_ranges = [AddrRange(config_data.dictionary['system_memory'])]
system.cpu = TimingSimpleCPU()
system.membus = SystemXBar()

system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)

system.l2cache.connectMemSideBus(system.membus)

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

if config_data.dictionary['system_memory_control'] == 'DDR3_1600_8x8':
    system.mem_ctrl = DDR3_1600_8x8()
    
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master
process = Process()
process.cmd = [config_data.dictionary['src_path_and_arg']]
system.cpu.workload = process
system.cpu.createThreads()
root = Root(full_system = False, system = system)


m5.instantiate()
print("Beginning simulation !!!")
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
