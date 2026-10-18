BSD3513 Introduction to Artificial Intelligence — Lab Report 1 _Chan Wan Wen_SD24059

A Streamlit app that runs Breadth-First Search (BFS) and Depth-First Search (DFS) on a directed graph with alphabetical tie-breaking.

Live Application: https://lab-report-1-sodpbfkbxfmtftdtjpfptb.streamlit.app/

<img width="1088" height="514" alt="image" src="https://github.com/user-attachments/assets/fdc3b985-6908-49fd-a184-8ab5df53fa7a" />


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
<img width="1088" height="517" alt="image" src="https://github.com/user-attachments/assets/3220cdb5-e8be-4f33-9ed6-5422f9cf48f0" />
<img width="1088" height="514" alt="image" src="https://github.com/user-attachments/assets/9023be8d-f994-45cb-83ac-1edf5ecbddd1" />
Depth-First Search (DFS)
<img width="1088" height="512" alt="image" src="https://github.com/user-attachments/assets/f03d29aa-6e89-421d-ba90-28f933907375" />
<img width="1088" height="514" alt="image" src="https://github.com/user-attachments/assets/12c20e9d-e22b-4346-afc4-440a9505bae4" />

Comparison between BFS vs DFS
<img width="1088" height="512" alt="image" src="https://github.com/user-attachments/assets/55172769-c19a-4281-8fb0-587939dc5e53" />

The discussion for the level and process path will be done with the assumption of the end goal is H.
<img width="1088" height="472" alt="image" src="https://github.com/user-attachments/assets/41c7608e-6798-42a4-8731-929466c3fc75" />

Breadth-first search (BFS)
<img width="1088" height="478" alt="image" src="https://github.com/user-attachments/assets/e35b114e-e849-4bf1-8e67-89d62692cda6" />
<img width="1088" height="516" alt="image" src="https://github.com/user-attachments/assets/37bdc9a3-e274-41f9-9a86-5c4585e06754" />
Process path: A → B → D → C → E → G → H
Levels: 
L0 {A}
L1 {B, D}
L2 {C, E,G}
L3 {H}
Goal path: A → B  → E → H (3 edges), which is the shortest path from A to H. 

Depth-First Search (DFS)
<img width="1088" height="514" alt="image" src="https://github.com/user-attachments/assets/0779204d-0694-409f-9bf5-a31a558fcdd1" />
<img width="1088" height="503" alt="image" src="https://github.com/user-attachments/assets/d32a1ea9-17df-4066-8b28-8a80f79ac29f" />
Process path: A → B  → C → E → H
Levels: 
L0 {A}
L1 {B}
L2 {C, E}
L3 {H}
Goal path: A → B  → E → H (3 edges), which is the shortest path from A to H. 

Comparison between BFS vs DFS
<img width="1088" height="488" alt="image" src="https://github.com/user-attachments/assets/b8cac566-b11a-48b9-a746-7722c2609656" />
