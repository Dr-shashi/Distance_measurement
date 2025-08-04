import requests
import plotly.graph_objects as go

# Your Google API Key
API_KEY = '"YOUR_API_KEY_HERE"'

origin = 'Srinagar Garhwal, Uttarakhand, India'
destinations = [
    'Pauri, Uttarakhand',
    'Kot, Pauri Garhwal, Uttarakhand',
    'Kaljikhal, Pauri Garhwal, Uttarakhand',
    'Khirsu, Pauri Garhwal, Uttarakhand',
    'Pabo, Pauri Garhwal, Uttarakhand',
    'Thalisain, Pauri Garhwal, Uttarakhand',
    'Bironkhal, Pauri Garhwal, Uttarakhand',
    'Nainidanda, Pauri Garhwal, Uttarakhand',
    'Ekeshwar, Pauri Garhwal, Uttarakhand',
    'Pokhra, Pauri Garhwal, Uttarakhand',
    'Rikhnikhal, Pauri Garhwal, Uttarakhand',
    'Jaiharikhal, Pauri Garhwal, Uttarakhand',
    'Dwarikhal, Pauri Garhwal, Uttarakhand',
    'Dugadda, Pauri Garhwal, Uttarakhand',
    'Yamkeshwar, Pauri Garhwal, Uttarakhand'
]

# Step 1: API Request
dest_str = '|'.join(destinations)
url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={dest_str}&key={API_KEY}"
response = requests.get(url)
data = response.json()
        # Display result
print(f"Distances from Srinagar Garhwal to Block Headquarters:\n")
for i, element in enumerate(data['rows'][0]['elements']):
    if element['status'] == 'OK':
        distance = element['distance']['text']
        duration = element['duration']['text']
        print(f"{destinations[i]}: {distance} ({duration})")
    else:
        print(f"{destinations[i]}: Distance not available ({element['status']})")


# Step 2: Process API response
results = []
for i, element in enumerate(data['rows'][0]['elements']):
    block_name = destinations[i].split(',')[0]
    if element['status'] == 'OK':
        distance_km = float(element['distance']['text'].split()[0])
        duration_text = element['duration']['text']
        duration_value = element['duration']['value']
        results.append((block_name, distance_km, duration_text, duration_value))
    else:
        results.append((block_name, 0.0, 'N/A', float('inf')))

# Step 3: Sort by travel time
results_sorted = sorted(results, key=lambda x: x[3])

# Extract for plotting
block_names = [r[0] for r in results_sorted]
distances_km = [r[1] for r in results_sorted]
durations = [r[2] for r in results_sorted]
hover_labels = [f"{dist} km<br>{dur}" for dist, dur in zip(distances_km, durations)]

# Step 4: Plotly Plot
fig = go.Figure(
    go.Bar(
        x=block_names,
        y=distances_km,
        text=[f"<b>{d} km</b><br><b>{t}</b>" for d, t in zip(distances_km, durations)],
        textfont=dict(size=16),
        textposition='outside',
        marker=dict(
            color=distances_km,
            colorscale='RdYlBu_r',  # Blue for short, red for long
            
        ),
        hovertext=hover_labels,
        hoverinfo='text'
    )
)

fig.update_layout(
    title='Distances from Srinagar Garhwal to Pauri District Block HQs (Sorted by Travel Time)',
    xaxis_title='Block Headquarters',
    yaxis_title='Distance (km)',
    xaxis_tickangle=-45,
    template='plotly_white',
   
    font=dict(
        size=14
    ),
    title_font=dict(size=20),
)

# Show plot
fig.show()

# Step 5: Save as image and HTML

fig.write_html("srinagar_to_blocks_distance.html")

print("Figure saved as  'srinagar_to_blocks_distance.html'")

