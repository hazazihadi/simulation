from road_network import *
import random

# world definition
seed = 0
W = World(
    name="",
    deltan=1,
    tmax=3600,
    print_mode=1, save_mode=1, show_mode=1,
    random_seed=seed,
    duo_update_time=99999
)
random.seed(seed)

# network definition
J1 = W.addNode("junction1", 0, 0, signal=[50, 50, 50, 50])  # Coordinated timing
J2 = W.addNode("junction2", 1, 0, signal=[50, 50, 50, 50], signal_offset=40)

EE = W.addNode("E", 2, 0)
WW = W.addNode("W", -1, 0)
SS1 = W.addNode("SS1", 0, -1)
SS2 = W.addNode("SS2", 1, -1)
NN1 = W.addNode("NN1", 0, 1)
NN2 = W.addNode("NN2", 1, 1)

# Links between nodes and junctions
W.addLink("W_J1", WW, J1, length=500, free_flow_speed=10, jam_density=0.2, signal_group=0)
W.addLink("N1_J1", NN1, J1, length=500, free_flow_speed=10, jam_density=0.2, signal_group=1)
W.addLink("SS1_J1", SS1, J1, length=500, free_flow_speed=10, jam_density=0.2, signal_group=2)
W.addLink("J2_J1", J2, J1, length=500, free_flow_speed=10, jam_density=0.2, signal_group=3)
W.addLink("J1_W", J1, WW, length=500, free_flow_speed=10, jam_density=0.2)
W.addLink("J1_N1", J1, NN1, length=500, free_flow_speed=10, jam_density=0.2)
W.addLink("J1_SS1", J1, SS1, length=500, free_flow_speed=10, jam_density=0.2)
W.addLink("J1_J2", J1, J2, length=500, free_flow_speed=10, jam_density=0.2, signal_group=0)
W.addLink("N2_J2", NN2, J2, length=500, free_flow_speed=10, jam_density=0.2, signal_group=1)
W.addLink("EE_J2", EE, J2, length=500, free_flow_speed=10, jam_density=0.2, signal_group=2)
W.addLink("SS2_J2", SS2, J2, length=500, free_flow_speed=10, jam_density=0.2, signal_group=3)
W.addLink("J2_N2", J2,NN2, length=500, free_flow_speed=10, jam_density=0.2)
W.addLink("J2_EE", J2, EE, length=500, free_flow_speed=10, jam_density=0.2)
W.addLink("J2_SS2", J2, SS2, length=500, free_flow_speed=10, jam_density=0.2)

# Demand definition: Flow between J1 and J2 and external nodes
dt = 30
for t in range(0, 3600, dt):
    # W.adddemand(NN1, SS1, t, t + dt,  volume=5)  # North of J1 to South of J2
    W.adddemand(NN1, SS2, t, t + dt,  volume=5)  # North of J1 to South of J2
    W.adddemand(NN2, SS2, t, t + dt,  volume=5)    # East of J2 to West of J1
    W.adddemand(WW, EE, t, t + dt,  volume=5)  # North of J1 to South of J2
    W.adddemand(EE, WW, t, t + dt,  volume=20)    # East of J2 to West of J1
    W.adddemand(SS1, NN2, t, t + dt,  random.uniform(0, 0.4))    # East of J2 to West of J1
    # W.adddemand(EE, WW, t, t + dt,  random.uniform(0, 0.6))    # East of J2 to West of J1

# simulation
W.exec_simulation()

# results
W.analyzer.print_simple_stats()

W.analyzer.macroscopic_fundamental_diagram()

# W.analyzer.time_space_diagram_traj(["W_J1", "J1_J2", "SS2_J2"])

# W.analyzer.time_space_diagram_traj_links(["SS1_J1", "J1_J2", "J2_N2"])
# for t in list(range(0,W.TMAX,int(W.TMAX/6))):
#     W.analyzer.network(t, detailed=1, network_font_size=0, figsize=(2,2))

W.analyzer.network_fancy(animation_speed_inverse=2, sample_ratio=1, interval=5, trace_length=3, figsize=6, antialiasing=False)
# display_image_in_notebook("out/2_junction.gif")
