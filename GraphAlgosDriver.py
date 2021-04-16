import sys
from algos.graphs.DijkstraSingleSourceSP import DijkstraSP
from algos.graphs.PrimMST import PrimMST
from algos.graphs.WeightedGraphs import DirectedEWG, UndirectedEWG


def run_dijkstra_singlesource_sp(args):
    directed_ewg = DirectedEWG(args)
    dijkstra_sp = DijkstraSP(directed_ewg, 0)
    for vertex in directed_ewg.vertices:
        path_to_vertex = dijkstra_sp.path_to(vertex)
        print(f"Path to {vertex} from 0 => {dijkstra_sp.print_spath(path_to_vertex)} : "
              f"Cost = {dijkstra_sp.shortest_path_cost(vertex)}")
    print('completed')


def run_primMST(arg):
    int_arg = None
    try:
        int_arg = int(arg)
    except ValueError:
        pass
    if int_arg is None:
        ewg = UndirectedEWG(arg)
    else:
        ewg = UndirectedEWG(int_arg)
    print(ewg)
    prim_mst = PrimMST(ewg)
    for edge in prim_mst.mst:
        print(edge)
    print("No of vertices: " + str(ewg.get_num_vertices()))
    print("No of edges: " + str(ewg.get_num_edges()))


def main():
    if len(sys.argv) < 3:
        raise Exception("Incorrect no. of arguments. First should be relative path to data file "
                        "and second should be algo type (Dijkstra or PrimMST)")
    args = sys.argv[1]
    algo_to_run = sys.argv[2]
    if algo_to_run.lower() == "dijkstra":
        run_dijkstra_singlesource_sp(args)
    elif algo_to_run.lower() == "primmst":
        run_primMST(args)


if __name__ == "__main__":
    main()
