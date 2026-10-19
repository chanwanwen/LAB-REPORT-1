BSD3513 Introduction to Artificial Intelligence — Lab Report 1 _Chan Wan Wen_SD24059

A Streamlit app that runs Breadth-First Search (BFS) and Depth-First Search (DFS) on a directed graph with alphabetical tie-breaking.

Live Application: https://lab-report-1-sodpbfkbxfmtftdtjpfptb.streamlit.app/

<img width="1088" height="488" alt="image" src="https://github.com/user-attachments/assets/a631ee75-04db-4318-a94b-c85a09e2a937" />



Features: 
- Editable directed graph.
- BFS traversal using a FIFO queue.
- DFS traversal using a LIFO stack or recursive search.
- Alphabetical tie-breaking for adjacent nodes.
- Step-by-step search trace.
- Graph visualisation highlighting the current and visited nodes.
- Node levels and parent relationships.
- BFS and DFS comparison table.
- Optional goal selection and path display.

The discussion for the level and process path will be done with the assumption of the end goal is no goal.
Breadth-first search (BFS) 
<img width="1088" height="490" alt="image" src="https://github.com/user-attachments/assets/eb917421-3b43-4c7f-8ebd-ebe880acfc65" />

Depth-First Search (DFS)
<img width="1088" height="479" alt="image" src="https://github.com/user-attachments/assets/cda42f66-e366-4529-a9fc-19f6bf4fcc49" />


Comparison between BFS vs DFS
<img width="1916" height="888" alt="image" src="https://github.com/user-attachments/assets/79f0bb76-472d-47d9-8671-8c7455c5b216" />


The discussion for the level and process path will be done with the assumption of the end goal is G.
<img width="1088" height="473" alt="image" src="https://github.com/user-attachments/assets/254408f1-86c6-4fca-a8b3-908ce3ee4779" />


Breadth-first search (BFS)
<img width="1088" height="481" alt="image" src="https://github.com/user-attachments/assets/5330daff-6b69-4c9a-b923-735af1581b85" />

Process path: A → B  → D → C → E → G

Levels: 

L0 {A}

L1 {B, D}

L2 {C, E, G}

Goal path: A → B  → G (2 edges), which is the shortest path from A to G. 

Depth-First Search (DFS)
<img width="1088" height="490" alt="image" src="https://github.com/user-attachments/assets/922ffd70-f759-46c8-a11d-029eabe2386f" />

Process path: A → B  → C → E → H → F → G

Levels: 

L0 {A}

L1 {B}

L2 {C, E}

L3 {H}

L4 {F, G}

Goal path: A → B  → E → H → G (4 edges), which is the shortest path from A to G.  

Comparison between BFS vs DFS
![Uploading image.png…]()

