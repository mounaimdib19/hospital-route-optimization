# hospital-route-optimization


# README: Healthcare System Optimization - Ambulance Route Optimization in Algiers

## Project Overview
This project aims to optimize ambulance routes, patient transfers, and emergency response times in Algiers using graph search algorithms. The system leverages uninformed, informed, and local search algorithms to find the most efficient route to a hospital or clinic based on the patient's medical needs.

---


## Project Structure
### Key Components
1. **Data Preparation**  
   - Raw data (municipalities, hospitals) and scripts for generating roundabouts are in a dedicated folder.
   - Processed data is stored in `data.py`.
   - Use `createnodes.ipynb` to generate new nodes (roundabouts) and manually update `data.py`.

2. **Search Algorithms**  
   - Implemented algorithms:  
     - Uninformed: BFS, DFS  
     - Informed: A* (with Manhattan distance heuristic)  
     - Local: Hill Climbing  

3. **User Interface**  
   - A simple GUI divides Algiers into East, West, and Center regions for easier navigation.
   - Users select:  
     - Starting region/commune  
     - Medical specialty  
     - Search algorithm  

4. **Output**  
   - Displays the optimal route and total distance (in KM).  
   - Example:  
     ```
     Select Region: East  
     Select Commune: El Hairach  
     Select Specialty: Rheumatology  
     Select Search: DFS  
     Total Distance: 52.6 KM  
     Path: Chu Bent/Messous  
     ```

---

## Key Features
- **Map Abstraction**:  
  - Nodes represent municipalities and roundabouts (added to emulate real shortcuts).  
  - Bidirectional edges with equal distances.  
- **Hospital Data**:  
  - Departments and bed counts collected via web/social media (default: 90 beds if data unavailable).  
- **Algorithm Insights**:  
  - **A***: Optimal but explores more nodes.  
  - **BFS**: Balanced performance in crowded areas.  
  - **DFS**: Space-efficient for sparse regions.  
  - **Hill Climbing**: Prone to plateaus; works best in small spaces.  

---

## Usage Guidelines
1. **Prerequisites**:  
   - Python 3.x  
   - Libraries: `json`, `matplotlib` (for plotting, optional)  

2. **Steps**:  
   - Clone the repository.  
   - Ensure `data.py` contains the latest node/hospital data.  
   - Run the GUI file (`interface.py` or `.ipynb`).  
   - Follow on-screen prompts to select region, commune, specialty, and algorithm.  

3. **Customization**:  
   - Modify `createnodes.ipynb` to add/remove nodes.  
   - Update `data.py` with new hospital/department info.  

---

## Results and Recommendations
- **Rule of Thumb**:  
  - **Sparse areas**: Use DFS for space efficiency.  
  - **Crowded areas**: BFS balances speed and node expansion.  
  - **Optimal routes**: A* is reliable but computationally heavier.  

- **Limitations**:  
  - Traffic data excluded due to inconsistency/unavailability.  
  - Single-patient searches only (no bed competition).  

---

## Future Work
- Integrate real-time traffic data.  
- Extend to multi-patient scenarios.  
- Implement iterative deepening (proposed by Isshak).  

---

## License
This project is open-source. Please attribute the authors if reused.  

For questions, contact:  
- Dib Abdelmounaim: `ABDELMOUNAIM.DIBe@ensia.edu.dz`  
- Team ENSIA S2G7/S2G4
