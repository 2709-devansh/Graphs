from collections import deque
import heapq

class Frontier:
    pass

#creating a graph - adjacency list
def convert_matrix_to_list(G):
    adj_list = {}
    for i in range(n):
        adj_list[i + 1] = []
    n = len(G)
    for i in range(n):
        for j in range(n):
            if G[i][j] == 1:
                adj_list[i + 1].append(j + 1)

class Graph():
    def __init__(self):
        self.adj = {}
        self.V = []

    def add_vertex(self, u):
        if u not in self.adj:
            self.adj[u] = []
        if u not in self.V:
            self.V.append(u)

    def add_edge(self, u, v, directed = False):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(v)
        if not directed:
            self.adj[v].append(u)

    def has_edge(self, u, v):
        return (u in self.adj and v in self.adj[u])

    def edges(self):
        for u in self.adj:
            for v in self.adj[u]:
                yield (u, v)

#generic graph traversal
class Frontier:
    pass

def genericGraphTraversal(G, s, state, parent): #frontier = queue/stack
    traversed = []

    frontier = Frontier()
    frontier.append((None, s))
    state[s] = 'gray'

    while frontier:
        p, u = frontier.popleft()

        if state[u] == 'black':
            continue

        parent[u] = p

        traversed.append(u)

        for v in G.adj[u]:
            if state[v] != 'black':
                state[v] = 'gray'
                frontier.append((u, v))

        state[u] = 'black'

    return traversed, parent

def TraverseAll(G):
    state = {u: None for u in G}
    parent = {u: None for u in G}
    for s in G:
        if state[s] == 'white':
            traversed, parent = genericGraphTraversal(G, s, state, parent)
    return traversed
    
#BFS
def bfs(G, s):
    queue = deque()
    bfs_traversed = []
    dist = {u : None for u in G.adj}
    parent = {u : None for u in G.adj}

    queue.append(s)
    dist[s] = 0

    while queue:
        u = queue.popleft()
        bfs_traversed.append(u)    
        for v in G.adj[u]:
            if dist[v] is None: #dist[v] as None helps to identify the white vertices
                dist[v] = dist[u] + 1
                parent[v] = u
                queue.append(v)

    return bfs_traversed, parent, dist

#DFS
dfs_traversed = []
def dfs(G, u, visited, parent):
    visited[u] = True
    dfs_traversed.append(u)
    for v in G.adj[u]:
        if not visited[v]:
            parent[v] = u
            dfs(G, v, visited, parent)

#bipartiteness
def bipartite(G):
    side = {u : None for u in G.V}
    queue = deque()
    for s in G.V:
        if side[s] == None:
            side[s] = 'red'
            queue.append(s)
            while queue:
                u = queue.popleft()
                for v in G.adj[u]:
                    if side[v] == None:
                        if side[u] == 'red':
                            side[v] = 'blue'
                        else:
                            side[v] = 'red'
                        queue.append(v)
                    elif side[v] == side[u]:
                        return False
    return True

#cycle detection
def visitCycle(G, u, p, visited):
    visited[u] = True
    for v in G.adj[u]:
        if visited[v] == None:
            if visitCycle(G, v, u, visited):
                return True
        elif v != p:
            return True
    return False

def hasCycle(G):
    visited = {u : None for u in G.V}
    for u in G.V:
        if visited[u] == None:
            if visitCycle(G, u, None, visited):
                return True
    return False

def visitCycleDirected(G, u, color):
    color[u] = 'gray'
    for v in G.adj[u]:
        if color[v] == 'white':
            if visitCycleDirected(G, v, color):
                return True
        elif color[v] == 'gray':
            return True
    color[u] = 'black'
    return False

def hasCycleDirected(G):
    color = {u : 'white' for u in G.V}
    for u in G.V:
        if color[u] == 'white':
            if visitCycleDirected(G, u, color):
                return True
    return False

#Kahn's Algorithm
def Kahn(G):
    indeg = {u : 0 for u in G.V}
    for u in G.V:
        for v in G.adj[u]:
            indeg[v] += 1

    queue = deque()
    for u in indeg:
        if indeg[u] == 0:
            queue.append(u)

    l = []

    while queue:
        u = queue.popleft()
        l.append(u)
        for v in G.adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)

    if len(l) < len(G.V):
        print("Cycle Detected")

    return l

#Topological sorting by DFS
def visit(G, u, color):
    color[u] = 'gray'
    l = deque()
    for v in G.adj[u]:
        if color[v] == 'gray':
            print("Cycle detected")
            return
        elif color[v] == 'white':
            visit(G, v, color)
    color[u] = 'black'
    l.append(u)

    return l

def topo_sort_dfs(G):
    color = {u : 'white' for u in G.V}
    for s in G.V:
        if color[s] == 'white':
            visit(G, s, color)

#SCC
def kosaraju_shirar(G, n):
    #creating the adjacency list and its transpose
    adj = [[] for _ in range(n + 1)]
    adj_t = [[] for _ in range(n + 1)]
    for u, v in G:
        adj[u].append(v)
        adj_t[v].append(u)

    #DFS 1
    visited = [False] * n
    stack = []

    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        stack.append(u)

    for u in range(1, n + 1):
        if not visited[u]:
            dfs1(u)

    #DFS 2
    visited = [False] * n
    sccs = []

    def dfs2(u, comp):
        visited[u] = True
        comp.append(u)
        for v in adj_t[u]:
            if not visited[v]:
                dfs2(v, comp)

    while stack:
        u = stack.pop()
        if not visited[u]:
            comp = []
            dfs2(u, comp)
            sccs.append(comp)
        return sccs

#MST
def Kruskal(n, edges):
    parent = list(range(n + 1))
    rank = [0] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(u, v):
        r, s = find(u), find(v)
        if r == s:
            return
        if rank[r] < rank[s]:
            s, r = r, s
        parent[s] = r
        if rank[r] == rank[s]:
            rank[r] += 1

    mst, total = [], 0
    for w, u, v in sorted(edges):
        r, s = find(u), find(v)
        if r != s:
            union(r, s)
            mst.append((u, v))
            total += w
            if len(mst) == n - 1:
                break

    return mst, total

def Prim(n, adj, r = 0):
    in_tree = [False] * n
    mst, total = [], 0
    hp = [(0, r, -1)]

    while hp:
        w, v, p = heapq.heappop()

        if in_tree[v]:
            continue
        in_tree[v] = True

        if p != -1:
            mst.append((p, v, w))
            total += w

        for x, wx in adj[v]:
            if not in_tree[x]:
                heapq.heappush(hp, (wx, x, v))

    return mst, total

#Single Source Shortest Path
def Kahn(G):
    indeg = {u : 0 for u in G.V}
    for u in G.V:
        for v in G.adj[u]:
            indeg[v] += 1

    queue = deque()
    for u in indeg:
        if indeg[u] == 0:
            queue.append(u)

    topo_order = []
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in G.adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)

    if len(topo_order) < len(G.V):
        print("Cycle Detected")
        return

    return topo_order

def dag_shortest_path(G, s):
    #G is of the form (u, v, w), adj[u] contains tuples (v, w)
    order = Kahn(G)
    inf = float('inf')
    n = len(G.V)

    d, pi = [inf] * n, [-1] * n
    d[s] = 0

    for u in order:
        for v, w in G.adj[u]:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
                pi[v] = u

#Dijkstra's Algorithm
def dijkstra(n, edges, s):
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))

    INF = float('inf')
    d = [INF] * (n + 1)
    pi = [-1] * (n + 1)
    d[s] = 0

    hp = [(0, s)]
    while hp:
        du, u = heapq.heappop(hp)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
                pi[v] = u
                heapq.heappush(hp, (d[v], v))

    return d, pi

def get_path(pi, v):
    path = []
    while v != -1:
        path.append(v)
        v = pi[v]
    return path[::-1]

#Bellman-Ford's Algorithm
def bellman_ford(n, edges, s):
    INF = float('inf')
    d = [INF] * (n + 1)
    pi = [-1] * (n + 1)
    d[s] = 0

    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
                pi[v] = u
                changed = True
        if not changed:
            break

    x = 0
    for u, v, w in edges:
        if d[u] + w < d[v]:
            d[v] = d[u] + w
            pi[v] = u
            x = v

    if x == 0:
        return d, pi, None

    for _ in range(n):
        x = pi[x]

    cycle, y = [x], x
    while y != x:
        y = pi[y]
        cycle.append(y)

    return d, pi, cycle[::-1]

def get_path(pi, v):
    path = []
    while v != -1:
        path.append(v)
        v = pi[v]
    return path[::-1]

#Floyd - Warshall Algorithm
def floyd_warshall(n, edges):
    #Initialization
    INF = float('inf')
    D = [[0 if i == j else INF for j in range(n + 1)] for i in range(n + 1)]
    pi = [[0] * (n + 1) for _ in range(n + 1)]
    nxt = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        nxt[i][i] = i

    for u, v, w in edges:
        D[u][v] = w
        pi[u][v] = u
        nxt[u][v] = v

    #Dynamic Programming
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            if D[i][k] == INF:
                continue
            for j in range(1, n + 1):
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
                    pi[i][j] = pi[k][j]
                    nxt[i][j] = nxt[i][k]

    #Negative Cycle Detection
    for i in range(1, n + 1):
        if D[i][i] < 0:
            return None

    return D, pi, nxt

def get_path_from_pi(pi, i, j):
    if i == j:
        return i
    
    if pi[i][j] == 0:
        return []
    
    path = []
    curr = j
    while curr != 0:
        path.append(curr)
        if curr == i:
            break
        curr = pi[i][curr]

    return path[::-1]

def get_path_from_nxt(nxt, i, j):
    if nxt[i][j] == 0:
        return []

    path = [i]
    while i != j:
        i = nxt[i][j]
        path.append(i)

    return path