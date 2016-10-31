from pybrain.structure import FeedForwardNetwork,TanhLayer,LinearLayer,BiasUnit,SigmoidLayer, FullConnection
import numpy as np
import csv
def simple_network_builder(layers,partial_path):
    n = FeedForwardNetwork()
    ## create the network
    inlayer = LinearLayer(layers[0], name = "In")
    hidden_one = SigmoidLayer(layers[1], name = "Hidden 1")
    hidden_two = SigmoidLayer(layers[2], name  ="Hidden 2")
    b1 = BiasUnit(name="Bias")
    output = LinearLayer(1,name = "Out")
    n.addInputModule(inlayer)
    n.addModule(hidden_one)
    n.addModule(hidden_two)
    n.addModule(b1)
    n.addOutputModule(output)
    in_to_one = FullConnection(inlayer,hidden_one)
    one_to_two = FullConnection(hidden_one,hidden_two)
    two_to_out = FullConnection(hidden_two,output)
    b1_to_one = FullConnection(b1,hidden_one)
    b2_to_two = FullConnection(b1,hidden_two)
    b3_to_output = FullConnection(b1,output)
    ### load weights and biases
    in_to_one._setParameters(np.array((csv_loader(partial_path + '_w1.csv'))))
    one_to_two._setParameters(np.array(csv_loader(partial_path + '_w2.csv')))
    two_to_out._setParameters(np.array(csv_loader(partial_path + '_w3.csv')))
    b1_to_one._setParameters(np.array(csv_loader(partial_path + '_b1.csv')))
    b2_to_two._setParameters(np.array(csv_loader(partial_path + '_b2.csv')))
    b3_to_output._setParameters(np.array(csv_loader(partial_path + '_b3.csv')))

    ### connect the network topology
    n.addConnection(in_to_one)
    n.addConnection(one_to_two)
    n.addConnection(two_to_out)
#    n.sortModules()

    n.addConnection(b1_to_one)
    n.addConnection(b2_to_two)
    n.addConnection(b3_to_output)

    ### finalize network object
    n.sortModules()

    return n



def network_builder(layers,partial_path):
    n = FeedForwardNetwork()
    ## create the network
    inlayer = LinearLayer(layers[0], name = "In")
    hidden_one = TanhLayer(layers[1], name = "Hidden 1")
    hidden_two = TanhLayer(layers[2], name  ="Hidden 2")
    b1 = BiasUnit(name="Bias")
    output = LinearLayer(1,name = "Out")
    n.addInputModule(inlayer)
    n.addModule(hidden_one)
    n.addModule(hidden_two)
    n.addModule(b1)
    n.addOutputModule(output)
    in_to_one = FullConnection(inlayer,hidden_one)
    one_to_two = FullConnection(hidden_one,hidden_two)
    two_to_out = FullConnection(hidden_two,output)
    b1_to_one = FullConnection(b1,hidden_one)
    b2_to_two = FullConnection(b1,hidden_two)
    b3_to_output = FullConnection(b1,output)
    ### load weights and biases
    in_to_one._setParameters(np.array((csv_loader(partial_path + '_w1.csv'))))
    one_to_two._setParameters(np.array(csv_loader(partial_path + '_w2.csv')))
    two_to_out._setParameters(np.array(csv_loader(partial_path + '_w3.csv')))
    b1_to_one._setParameters(np.array(csv_loader(partial_path + '_b1.csv')))
    b2_to_two._setParameters(np.array(csv_loader(partial_path + '_b2.csv')))
    b3_to_output._setParameters(np.array(csv_loader(partial_path + '_b3.csv')))

    ### connect the network topology
    n.addConnection(in_to_one)
    n.addConnection(one_to_two)
    n.addConnection(two_to_out)
#    n.sortModules()

    n.addConnection(b1_to_one)
    n.addConnection(b2_to_two)
    n.addConnection(b3_to_output)

    ### finalize network object
    n.sortModules()

    return n


def csv_loader(path):
    with open(path,'r') as csvfile:
        csv_lines = csv.reader(csvfile,delimiter= ',')
        ret_list = list()
        for lines in csv_lines:
            print(type(lines))
            print(type(lines[0]))
            this_line = [float(a) for a in lines]
            ret_list += this_line
    return ret_list


test_excitation = [0,0,0,0,1, # metals co/cr/fe/mn/ni                 #1-4
                   0,0.6666666667,0.5,1, #ox/alpha/eqlig charge/axlig charge #5-8
                   0,0,# eq_dent/ax_dent/ #9-10
                   0,0,1,0, # axlig_connect: Cl,N,O,S #10 -14
                   0,0,1,0, # eqliq_connect: Cl,N,O,S #14-18
                   0.95,1, #mdelen, maxdelen #23-24
                   0.333,0.333, #axlig_bo, eqliq_bo #19-20
                   0.465,1.19877]#axlig_ki, eqliq_kii #21-22
#n = network_builder([25,50,51],"nn_split")
n = simple_network_builder([25,4,4],"nn_simple")

split_factors = [-54.19, 142.71]

print(n.activate(test_excitation)*split_factors[1] + split_factors[0])
for c in [connection for connections in n.connections.values() for connection in connections]:
        print("{} -> {} => {}".format(c.inmod.name, c.outmod.name, c.params))
### view weights:
#for mod in n.modules:
#    print("Module:", mod.name)
#    if mod.paramdim > 0:
#        print("--parameters:", mod.params)
#        for conn in net.connections[mod]:
#            print("-connection to", conn.outmod.name)
#            if conn.paramdim > 0:
#                print("- parameters", conn.params)
#                if hasattr(net, "recurrentConns"):
#                    print("Recurrent connections")
#                    for conn in net.recurrentConns:
#                        print("-", conn.inmod.name, " to", conn.outmod.name)
#                        if conn.paramdim > 0:
#                            print("- parameters", conn.params)